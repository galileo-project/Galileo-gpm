from subprocess import Popen, PIPE
import shlex
import re
import os
from gpm.utils.console import puts
from gpm.utils.log import Log
from gpm.const.status import Status
from gpm.utils.string import decode as str_decode

class LocalOperation(object):
    _RE_CD = re.compile(r"cd\s([\w\d_\/\s\~\.]+)")

    @classmethod
    def mkdir(cls, paths, *args, **kwargs):
        if not isinstance(paths, list):
            paths = [paths]

        for path in paths:
            if LocalOperation.exist(path):
                paths.remove(path)

        return cls.__exec("mkdir -p %s" % " ".join(paths), *args, **kwargs)

    @classmethod
    def rm(cls, paths, *args, **kwargs):
        if not isinstance(paths, list):
            paths = [paths]

        if paths:
            return cls.__exec("rm -rf %s" % " ".join(paths), *args, **kwargs)
        else:
            return True

    @classmethod
    def ls(cls, path, long = False, hidden = False):
        cmd = "ls %s" % path
        if long:
            cmd = "%s %s" % (cmd, "-l")
        if hidden:
            cmd = "%s %s" % (cmd, "-a")
        ret = cls.__exec(cmd, ret = True)

        if not isinstance(ret, list):
            return []
        return cls.string_clean(ret)

    @classmethod
    def cp(cls, origin, target):
        if not isinstance(origin, list):
            origin = [origin]
        ret = cls.__exec("cp -rf %s %s" % (" ".join(origin), target), ret = True)
        return not ret is False

    @classmethod
    def chmod(cls, mod, path, *args, **kwargs):
        path = LocalOperation.rel2abs(path)
        return cls.__exec("chmod %d %s" % (mod, path), *args, **kwargs)

    @classmethod
    def run(cls, cmd, path = None, *args, **kwargs):
        if path:
            path = cls.rel2abs(path)
        return cls.__exec(cmd, cwd = path, *args, **kwargs)

    @classmethod
    def cat(cls, paths):
        if not isinstance(paths, list):
            paths = [paths]

        ret = cls.__exec("cat %s" % " ".join(paths), ret = True)
        if ret:
            return "\n".join(ret)
        else:
            return None

    @classmethod
    def pwd(cls):
        ret = cls.__exec("pwd", ret = True)
        path = cls.string_clean(ret[0])
        return cls.rel2abs(path)

    @classmethod
    def read(cls, path, *args, **kwargs):
        path = cls.string_clean(path)
        with open(path, "r") as stream:
            lines = [str_decode(line) for line in stream.readlines()]

        return "\n".join(lines)

    @classmethod
    def find(cls, path, name = None, depth = 1, *args, **kwargs):
        if not name:
            target_path = os.path.dirname(path)
        else:
            target_path = path
        target_name = name or os.path.basename(path)
        ret = cls.__exec("find %s -maxdepth %d -name %s" % (target_path, depth, target_name), *args, **kwargs)

        if not isinstance(ret, list):
            return []
        return cls.string_clean(ret)

    @classmethod
    def distr(cls):
        paths = cls.find("/etc/*-release")
        ret = cls.cat(paths)
        re_distri = re.compile(r'PRETTY_NAME=\"(.*?)\"')
        return re_distri.findall(ret)[0]

    @classmethod
    def append(cls, path, contents, *args, **kwargs):
        path = LocalOperation.rel2abs(path)
        content = contents.join("\n")
        return cls.__exec("sed -i '$a %s' %s" % (content, path), *args, **kwargs)

    @classmethod
    def exist(cls, path):
        path = LocalOperation.rel2abs(path)
        return os.path.exists(path)

    @classmethod
    def rel2abs(cls, path = None):
        if path:
            if cls.get_user() == "root":
                path = path.replace("~", "/root")
            else:
                path = path.replace("~", "/home/%s" % cls.get_user())
        return os.path.abspath(path or os.curdir)

    @classmethod
    def add_file(cls, path, content = ""):
        with open(path, "w+") as stream:
            stream.write(content)

    @property
    def user(self):
        return self.get_user()

    @staticmethod
    def get_user():
        return os.getenv("USER")

    @classmethod
    def __exec(cls, cmd, cwd = None, *args, **kwargs):
        if "&&" in cmd:
            cmds = cmd.split("&&")
            ret = False
            path = None
            for cmd in cmds:
                if not path:
                    path = cls.__cd_to_path(cwd)
                    if path: continue
                ret = cls.__exec(cmd, cwd=path or cwd, *args, **kwargs)
                if not ret:
                    return ret
            return ret

        cmd_args = shlex.split(cmd)
        Log.debug(cmd)
        p = Popen(cmd_args, cwd = cwd, stderr=PIPE, stdout=PIPE, shell=False)
        return LocalOperation.__parser(p, *args, **kwargs)

    @classmethod
    def string_clean(cls, strings):
        if isinstance(strings, list):
            ret = []
            for string in strings:
                ret.append(cls.string_clean(string))
            return ret
        else:
            if cls.__is_str(strings):
                strings = strings.replace("\n", "")
                strings = strings.replace("\t", "")
            return strings

    @classmethod
    def __cd_to_path(cls, cmd):
        ret = cls._RE_CD.findall(cmd)
        if ret:
            return cls.rel2abs(ret[0])
        else:
            return None

    @staticmethod
    def __is_str(string):
        try:
            basestring
        except:
            basestring = str

        return isinstance(string, basestring)

    @staticmethod
    def __parser(process, ret = True, output = False, *args, **kwargs):
        res = False
        process.wait()
        code = process.poll()

        if not isinstance(code, int):
            Log.fatal(Status["STAT_EXEC_ERROR"])

        out_strs = [str_decode(line) for line in process.stdout.readlines()]
        err_strs = [str_decode(line) for line in process.stderr.readlines()]

        if ret:
            if code != 0:
                res = False
            else:
                res = out_strs or True

        if output:
            if code != 0:
                puts("\n".join(err_strs))
                res = res or False
            else:
                puts("\n".join(out_strs))
                res = res or True

        return res

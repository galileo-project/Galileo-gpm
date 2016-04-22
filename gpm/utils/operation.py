from subprocess import Popen, PIPE
import shlex
import re
import os
from gpm.utils.console import puts
from gpm.utils.log import Log
from gpm.const.status import Status
from gpm.utils.string import decode as str_decode

class LocalOperation(object):
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
    def cp(cls, origin, target):
        if not isinstance(origin, list):
            origin = [origin]
        ret = cls.__exec("cp -r %s %s", " ".join(origin), target, ret = True)
        return not ret is False

    @classmethod
    def chmod(cls, mod, path, *args, **kwargs):
        path = LocalOperation.rel2abs(path)
        return cls.__exec("chmod %d %s" % (mod, path), *args, **kwargs)

    @classmethod
    def run(cls, cmd, path = None, *args, **kwargs):
        if path:
            abs_path = cls.rel2abs(path)
            if cls.exist(abs_path):
                cmd = "cd %s && %s" % (abs_path, cmd)
            else:
                return False
        return cls.__exec(cmd, *args, **kwargs)

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
        return cls.rel2abs(ret)

    @classmethod
    def read(cls, path, *args, **kwargs):
        path = cls.string_clean(path)
        with open(path, "r") as stream:
            lines = [str_decode(line) for line in stream.readlines()]

        return "\n".join(lines)

    @classmethod
    def find(cls, path, *args, **kwargs):
        target_path = os.path.dirname(path)
        target_name = os.path.basename(path)
        ret = cls.__exec("find %s -name %s" % (target_path, target_name), *args, **kwargs)
        rets = [cls.string_clean(i) for i in ret]

        return rets

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
        return os.path.abspath(path or os.curdir)

    @classmethod
    def add_file(cls, path, content = ""):
        with open(path, "w+") as stream:
            stream.write(content)

    @property
    def user(self):
        return os.getenv("USER")

    @classmethod
    def __exec(cls, cmd, *args, **kwargs):
        cmd_args = shlex.split(cmd)
        Log.debug(cmd_args)
        p = Popen(cmd_args, stderr=PIPE, stdout=PIPE, shell=False)
        return LocalOperation.__parser(p, *args, **kwargs)

    @staticmethod
    def string_clean(string):
        string = string.replace("\n", "")
        string = string.replace("\t", "")
        return string

    @staticmethod
    def __parser(process, ret = True, output = False, *args, **kwargs):
        res = False
        process.wait()
        code = process.poll()

        Log.debug("Exit code %s" % str(code))
        if not isinstance(code, int):
            Log.fatal(Status["STAT_EXEC_ERROR"])

        out_strs = [str_decode(line) for line in process.stdout.readlines()]
        err_strs = [str_decode(line) for line in process.stderr.readlines()]

        Log.debug(out_strs)
        Log.debug(err_strs)

        if ret:
            if code != 0:
                res = False
            else:
                res = out_strs

        if output:
            if code != 0:
                puts("\n".join(err_strs))
                res = res or False
            else:
                puts("\n".join(out_strs))
                res = res or True

        return res

if __name__ == "__main__":
    res = LocalOperation.cat("log.py")
    print(res)
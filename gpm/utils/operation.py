from subprocess import Popen, PIPE
import shlex
import re
import os
from gpm.utils.console import puts
from gpm.utils.log import Log
from gpm.settings.status import Status
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
    def chmod(cls, mod, path, *args, **kwargs):
        path = LocalOperation.rel2abs(path)
        return cls.__exec("chmod %d %s" % (mod, path), *args, **kwargs)

    @classmethod
    def run(cls, *args, **kwargs):
        return cls.__exec(*args, **kwargs)

    @classmethod
    def cat(cls, path, *args, **kwargs):
        path = LocalOperation.rel2abs(path)
        ret = cls.__exec("cat %s" % path, *args, **kwargs)
        if isinstance(ret, list):
            return "\n".join(ret)
        return ret

    @classmethod
    def distr(cls):
        ret = cls.cat("/etc/*-release", ret=True)
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
    def add_file(cls, name, content = ""):
        with open(name, "w+") as stream:
            stream.write(content)

    @property
    def user(self):
        return os.getenv("USER")

    @classmethod
    def __exec(cls, cmd, *args, **kwargs):
        Log.debug(cmd)
        cmd_args = shlex.split(cmd)
        p = Popen(cmd_args, stderr=PIPE, stdout=PIPE, shell=True)
        return LocalOperation.__parser(p, *args, **kwargs)

    @staticmethod
    def __parser(process, ret = True, output = False, *args, **kwargs):
        ret = False
        code = process.poll()
        if not isinstance(code, int):
            Log.debug("Exit code %s" % str(code))
            Log.fatal(Status["STAT_EXEC_ERROR"])

        out_strs = [str_decode(line) for line in process.stdout.readlines()]
        err_strs = [str_decode(line) for line in process.stderr.readlines()]

        Log.debug(out_strs)
        Log.debug(err_strs)

        if ret:
            if code != 0:
                ret = False
            else:
                ret = out_strs

        if output:
            if code != 0:
                puts("\n".join(err_strs))
                ret = False
            else:
                puts("\n".join(out_strs))
                ret = True

        return ret


from subprocess import Popen, PIPE
import shlex
import re
import os
from gpm.utils.console import puts

class LocalOperation(object):
    @classmethod
    def mkdir(cls, paths, *args, **kwargs):
        if not isinstance(paths, list):
            paths = [paths]
        return cls._exec("mkdir -p %s" % paths.join(" "), *args, **kwargs)

    @classmethod
    def rm(cls, paths, *args, **kwargs):
        if not isinstance(paths, list):
            paths = [paths]
        return cls._exec("rm -rf %s" % paths.join(" "), *args, **kwargs)

    @classmethod
    def chmod(cls, mod, path, *args, **kwargs):
        path = LocalOperation.rel2abs(path)
        return cls._exec("chmod %d %s" % (mod, path), *args, **kwargs)

    @classmethod
    def exec(cls, cmd, *args, **kwargs):
        return cls._exec(cmd, *args, **kwargs)

    @classmethod
    def cat(cls, path, *args, **kwargs):
        path = LocalOperation.rel2abs(path)
        ret = cls._exec("cat %s" % path, *args, **kwargs)
        if isinstance(ret, list):
            return ret.join("\n")
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
        return cls._exec("sed -i '$a %s' %s" % (content, path), *args, **kwargs)

    @classmethod
    def exist(cls, path):
        path = LocalOperation.rel2abs(path)
        return os.path.exists(path)

    @staticmethod
    def rel2abs(path = None):
        return os.path.abspath(path or os.curdir)

    @classmethod
    def _exec(cls, cmd, *args, **kwargs):
        args = shlex.split(cmd)
        p = Popen(args, stderr=PIPE, stdout=PIPE, shell=True)
        return cls.__parser(p, *args, **kwargs)

    @classmethod
    def __parser(cls, process, ret = True, output = False, *args, **kwargs):
        code     = process.poll()
        out_strs = process.stdout.readlines()
        err_strs = process.stderr.readlines()

        if ret:
            if code != 0:
                return False
            else:
                return out_strs

        if output:
            if code != 0:
                puts(err_strs.join("\n"))
                return False
            else:
                puts(out_strs.join("\n"))
                return True

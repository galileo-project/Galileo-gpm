from gpm.utils.opt import opt_parser
from gpm.utils.log import Log
from gpm.utils.conf import ConfReader
from gpm.settings import DEFAULT_MOD
from gpm.utils.operation import LocalOperation
import pkgutil
import os

class CLI(object):
    def _default(self, *args, **kwargs):
        self.__getattribute__(self._OPTS["default"])(*args, **kwargs)

    def _run(self, args):
        path = LocalOperation.rel2abs()
        config = ConfReader(path)
        func, kwargs = opt_parser(args, self)
        if func is None:
            func = self._default
        func(config, **kwargs)

def _mods():
    mods = {}
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
        mod = loader.find_module(module_name).load_module(module_name)
        try:
            mods[module_name] = mod._MOD
        except:
            Log.warn("Load %s error." % module_name)
    return mods

def _sub_cmd(args):
    if len(args) < 1:
        return DEFAULT_MOD, []
    elif "-" in args[0]:
        return DEFAULT_MOD, args[1:]
    else:
        return args[0], args[1:]

def run(args):
    mods = _mods()
    sub_cmd, sub_arg = _sub_cmd(args)
    mods[sub_cmd]()._run(sub_arg)
from gpm.utils.opt import opt_parser
from gpm.utils.log import Log
from gpm.utils.conf import GPMConf
from gpm.const import DEFAULT_MOD
from gpm.const.status import Status
import pkgutil

class CLI(object):
    def __init__(self):
        self.config = GPMConf()

    def _default(self, *args, **kwargs):
        self.__getattribute__(self._OPTS["default"])(*args, **kwargs)

    def _run(self, args):
        func, kwargs, args = opt_parser(args, self)
        if func is None:
            func = self._default
        func(*args, **kwargs)

def _mods():
    mods = {}
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
        mod = loader.find_module(module_name).load_module(module_name)
        try:
            mods[module_name] = mod._MOD
        except:
            Log.warn(Status["STAT_LOAD_MOD_ERROR"] % module_name)
    return mods

def _sub_cmd(args):
    if len(args) < 1:
        return DEFAULT_MOD, []
    elif "-" in args[0]:
        return DEFAULT_MOD, args
    else:
        return args[0], args[1:]

def run(args):
    mods = _mods()
    sub_cmd, sub_arg = _sub_cmd(args)
    try:
        mods[sub_cmd]()._run(sub_arg)
    except KeyboardInterrupt:
        Log.puts(Status["STAT_EXIT"])
    except Exception as e:
        Log.fatal(str(e))
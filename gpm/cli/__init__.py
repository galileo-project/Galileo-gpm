from gpm.utils.opt import opt_parser
from gpm.utils.log import Log
import pkgutil

class CLI:
    def __init__(self, args):
        self._args = args

    def _default(self, *args, **kwargs):
        self.__getattribute__(self._DEFAULT)(*args, **kwargs)
        self._mods = {}

    @property
    def mods(self):
        if not self._mods:
            for loader, module_name, is_pkg in pkgutil.walk_packages(__file__):
                mod = loader.find_module(module_name).load_module(module_name)
                try:
                    self._mods[module_name] = mod._MOD
                except:
                    Log.warn("Load %s error." % module_name)
        return self._mods

    def _sub_cmd(self, args):
        if len(args) < 1:
            return "default", []
        elif "-" in args[0]:
            return "default", args[1:]
        else:
            return args[0], args[1:]

    def _run(self, args):
        func, kwargs = opt_parser(args, self)
        if func is None:
            func = self._default
        func(**kwargs)

    def start(self):
        sub_cmd, sub_arg = self._sub_cmd(self._args)
        self.mods[sub_cmd]()._run(sub_arg)

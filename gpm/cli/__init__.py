from gpm.utils.opt import opt_parser
from gpm.utils.log import Log
import pkgutil

class CLI:
    _DEFAULT_MOD = "default"

    def __init__(self, args):
        self._args = args
        self._mods = {}

    def _default(self, *args, **kwargs):
        self.__getattribute__(self._OPTS["default"])(*args, **kwargs)

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
            return self._DEFAULT_MOD, []
        elif "-" in args[0]:
            return self._DEFAULT_MOD, args[1:]
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

import pkgutil
from gpm.utils.opt import opt_parser
from gpm.utils.log import Log
from gpm.config import version
from gpm.utils.console import put

class CLI:
    _OPTS = {"shortcut": "v", "fullname": ["version"], "action": ["_version"]}

    def __init__(self, args):
        self._args = args
        self._mods = {}

    @property
    def mods(self):
        if not self._mods:
            for loader, module_name, is_pkg in pkgutil.walk_packages(__file__):
                mod = loader.find_module(module_name).load_module(module_name)
                try:
                    self._mods[module_name] = mod._NAME
                except:
                    Log.warn("Load %s error." % module_name)
        return self._mods

    def run(self):
        if self._args in self.mods.keys():
            self.mods[self._args[0]](self._args[1:]).run()
        else:
            func, kwargs = opt_parser(self._args, self)
            func(**kwargs)

    def _version(self, *args, **kwargs):
        put(version)

import pkgutil
from utils.opt import opt_parser
from utils.log import Log
import config
from utils.console import put

class CLI:
    def __init__(self, args):
        self._args  = args
        self._mods  = {}
        self.define = {"shortcut": "v", "fullname": ["version"], "action": [self.version]}

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
            func, args = opt_parser(self._args, self, self.define)
            func(*args)

    def version(self, *args, **kwargs):
        put(config.version)

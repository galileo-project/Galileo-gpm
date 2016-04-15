from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.model.package import Packages

class CLIDep(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_dep"}
    __doc__ = """

    """

    def _dep(self, *args, **kwargs):
        pass

    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLIDep
from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.operation import LocalOperation

class CLIUninstall(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_uninstall"}
    __doc__ = """

    """

    def _uninstall(self, *args, **kwargs):
        pass

    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLIUninstall
from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.operation import LocalOperation

class CLIRemove(CLI):
    _OPTS    = {"shortcut": "hy", "name": ["help", "confirm"], "action": ["_help", None], "default": "_remove"}
    __doc__ = """

    """

    def _remove(self, *args, **kwargs):
        pass

    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLIRemove
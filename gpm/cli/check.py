from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.operation import LocalOperation

class CLICheck(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_help"}
    __doc__ = """

    """

    def _help(self, *args, **kwargs):
        puts(self.__doc__)

_MOD = CLICheck
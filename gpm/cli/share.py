from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.operation import LocalOperation

class CLIShare(CLI):
    _OPTS    = {"shortcut": "h", "fullname": ["help"], "action": ["_help"], "default": "_help"}
    __doc__ = """

    """

    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLIShare
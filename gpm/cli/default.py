from gpm import __version__ as version
from gpm import __name__ as name
from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.operation import LocalOperation

class CLIDefault(CLI):
    _OPTS    = {"shortcut": "vh", "fullname": ["version", "help"], "action": ["_version", "_help"], "default": "_version"}
    __doc__ = """

    """

    def _version(self, *args, **kwargs):
        puts(LocalOperation.distr())
        puts("%s %s" % (name, version))

    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLIDefault
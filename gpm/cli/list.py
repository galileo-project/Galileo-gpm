from gpm.cli import CLI
from gpm.utils.package import PackageOpration
from gpm.utils.console import puts


class CLIList(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_list"}
    __doc__ = """
        GPM list
List installed gpm packages
Usage:
    gpm list
Options:
    -h, --help  show gpm list manual
    """

    def _list(self, *args, **kwargs):
        po = PackageOpration()
        po.list()

    @classmethod
    def _help(cls, *args, **kwargs):
        puts(cls.__doc__)


_MOD = CLIList
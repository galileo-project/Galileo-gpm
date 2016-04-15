from gpm.cli import CLI
from gpm.model.package import Packages
from gpm.utils.console import puts


class CLIRemove(CLI):
    _OPTS    = {"shortcut": "hy", "name": ["help", "confirm"], "action": ["_help", None], "default": "_remove"}
    __doc__ = """

    """

    def _remove(self, *args, **kwargs):
        pa = Packages()
        pa.find(args)
        ret = pa.remove()


    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLIRemove
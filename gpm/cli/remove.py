from gpm.cli import CLI
from gpm.utils.package import PackageOpration
from gpm.utils.console import puts


class CLIRemove(CLI):
    _OPTS    = {"shortcut": "hy", "name": ["help", "confirm"], "action": ["_help", None], "default": "_remove"}
    __doc__ = """

    """

    def _remove(self, *args, **kwargs):
        po = PackageOpration()
        if args:
            conf = po.find(args[0])
        else:
            conf = self.config
        po.remove(conf)

    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLIRemove
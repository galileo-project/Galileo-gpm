from gpm.cli import CLI
from gpm.utils.package import PackageOpration
from gpm.utils.console import puts
from gpm.utils.console import confirm

class CLIRemove(CLI):
    _OPTS    = {"shortcut": "hy", "name": ["help", "yes"], "action": ["_help", None], "default": "_remove"}
    __doc__ = """
        GPM remove
Remove a installed gpm package
Usage:
    gpm remove
Options:
    -h, --help  Show gpm remove manual
    -y, --yes   Say yes by default
    """

    def _remove(self, *args, **kwargs):
        if not kwargs.get("yes"):
            if not confirm("Is remove %s ?" % args[0]):
                return

        po = PackageOpration()
        if args:
            conf = po.find(args[0])
        else:
            conf = self.config
        po.remove(conf)

    @classmethod
    def _help(cls, *args, **kwargs):
        puts(cls.__doc__)


_MOD = CLIRemove
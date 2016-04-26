from gpm.cli import CLI
from gpm.utils.package import PackageOpration
from gpm.utils.console import puts


class CLIPublish(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_publish"}
    __doc__ = """
        GPM publish
Publish a gpm package to GitHub
Usage:
    gpm publish
Options:
    -h, --help  Show gpm publish manual
    """

    def _publish(self, *args, **kwargs):
        po = PackageOpration(self.config)
        po.publish()

    @classmethod
    def _help(cls, *args, **kwargs):
        puts(cls.__doc__)


_MOD = CLIPublish
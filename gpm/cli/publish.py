from gpm.cli import CLI
from gpm.utils.package import PackageOpration
from gpm.utils.console import puts


class CLIPublish(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_publish"}
    __doc__ = """

    """

    def _publish(self, *args, **kwargs):
        po = PackageOpration(self.config)
        po.publish()

    def _help(self, *args, **kwargs):
        puts(self.__doc__)


_MOD = CLIPublish
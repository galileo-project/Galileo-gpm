from gpm.utils.console import puts
from gpm.utils.console import confirm
from gpm.cli import CLI
from gpm.utils.log import Log
from gpm.const.status import Status
from gpm.utils.package import PackageOpration

class CLIInstall(CLI):
    _OPTS     = {"shortcut": "hy", "name": ["help", "yes"], "action": ["_help", None], "default": "_install"}
    __doc__ = """
        GPM install
Install gpm package
Usage:
    gpm install
Options:
    -h, --help  show gpm install manual
    -y, --yes   yes by default
    """

    def _install(self, *args, **kwargs):
        if not kwargs.get("yes"):
            if not confirm("Is install %s ?" % self.config.name):
                return

        ret = PackageOpration().install(self.config)
        if not ret:
            Log.fatal(Status["STAT_INSTALL_ERROR"] % self.config.name)
        else:
            Log.success(Status["STAT_INSTALL_SUCCESS"] % self.config.name)

    def _help(self, *args, **kwargs):
        puts(self.__doc__)

_MOD = CLIInstall
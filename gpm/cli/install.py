from gpm.utils.console import puts
from gpm.utils.operation import LocalOperation
from gpm.cli import CLI
from gpm.utils.log import Log
from gpm.const.status import Status

class CLIInstall(CLI):
    _OPTS     = {"shortcut": "h", "fullname": ["help"], "action": ["_help"], "default": "_install"}
    __doc__ = """

    """

    def _install(self, *args, **kwargs):
        cmds = self.config.install
        for cmd in cmds:
            ret = LocalOperation.run(cmd)
            if not ret:
                Log.fatal(Status["STAT_INSTALL_ERROR"] % cmd)

        Log.success(Status["STAT_INSTALL_SUCCESS"])

    def _help(self, *args, **kwargs):
        puts(self.__doc__)

_MOD = CLIInstall
from gpm.utils.console import puts
from gpm.utils.operation import LocalOperation
from gpm.cli import CLI
from gpm.utils.log import Log
from gpm.settings.status import Status

class CLIBuild(CLI):
    _OPTS     = {"shortcut": "h", "fullname": ["help"], "action": ["_help"], "default": "_build"}
    __doc__ = """

    """
    def _build(self, *args, **kwargs):
        cmds = self.config.build
        for cmd in cmds:
            ret = LocalOperation.run(cmd)
            if not ret:
                Log.fatal(Status["STAT_BUILD_ERROR"] % cmd)

        Log.success(Status["STAT_BUILD_SUCCESS"])

    def _help(self, *args, **kwargs):
        puts(self.__doc__)

_MOD = CLIBuild
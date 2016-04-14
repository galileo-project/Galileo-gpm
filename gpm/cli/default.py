from gpm import __version__ as version
from gpm.utils.console import puts
from gpm.cli import CLI

class CLIDefault(CLI):
    _OPTS    = {"shortcut": "vh", "fullname": ["version", "help"], "action": ["_version", "_help"], "default": "_version"}

    def _version(self, config, *args, **kwargs):
        puts(version)

    def _help(self, config, *args, **kwargs):
        pass


_MOD = CLIDefault
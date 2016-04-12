from gpm.config import version
from gpm.utils.console import put
from gpm.cli import CLI

class CLIDefault(CLI):
    _OPTS    = {"shortcut": "vh", "fullname": ["version", "help"], "action": ["_version", "_help"], "default": "_version"}

    def _version(self, config, *args, **kwargs):
        put(version)

    def _help(self, config, *args, **kwargs):
        pass


_MOD = CLIDefault
from gpm.utils.opt import opt_parser
from gpm.utils.log import Log
from gpm.config import version
from gpm.utils.console import put
from gpm.cli import CLI

class CLIDefault(CLI):
    _OPTS    = {"shortcut": "v", "fullname": ["version"], "action": ["_version"]}
    _DEFAULT = "_version"

    def _version(self, *args, **kwargs):
        put(version)


_MOD = CLIDefault
from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.operation import LocalOperation
from gpm.utils.conf import SYSConf

class CLIConfig(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_config"}
    __doc__ = """
        GPM config
Configure user gpm settings
Usage:
    gpm config
Options:
    -h, --help  show gpm config manual
    """

    def _help(self, *args, **kwargs):
        puts(self.__doc__)

    def _config(self):
        conf = SYSConf()
        conf.generate()

_MOD = CLIConfig
from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.conf import GPMConf
from gpm.utils.git_client import GitClient
from gpm.const import GPM_YML
import os

class CLIInit(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_init"}
    __doc__ = """
        GPM init
Create and Init gpm package
Usage:
    gpm init
Options:
    -h, --help  Show gpm init manual
    """

    @classmethod
    def _help(cls, *args, **kwargs):
        puts(cls.__doc__)

    def _init(self, *args, **kwargs):
        conf = GPMConf()
        conf.generate()
        gc   = GitClient(conf)
        gc.init()
        gc.add(os.path.join(conf.name, GPM_YML))
        gc.commit("Init Project with gpm")

_MOD = CLIInit
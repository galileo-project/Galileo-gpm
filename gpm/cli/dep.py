from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.package import PackageOpration

class CLIDep(CLI):
    _OPTS    = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_dep"}
    __doc__ = """
        GPM dep
Install gpm dependency package
Usage:
    gpm dep
Options:
    -h, --help  Show gpm dep manual
    """

    def _dep(self, *args, **kwargs):
        po = PackageOpration(self.config)
        po.dep()

    @classmethod
    def _help(cls, *args, **kwargs):
        puts(cls.__doc__)

_MOD = CLIDep
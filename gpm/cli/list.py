from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.model.package import Packages

class CLIList(CLI):
    _OPTS     = {"shortcut": "h", "name": ["help"], "action": ["_help"], "default": "_list"}
    __doc__ = """

    """

    def _list(self, *args, **kwargs):
        pkgs = Packages().all()
        for pkg in pkgs:
            pkg_config = pkg.values()[0]
            puts("%s - %s" % (pkg_config.name, pkg_config.author))

    def _help(self, *args, **kwargs):
        puts(self.__doc__)

_MOD = CLIList
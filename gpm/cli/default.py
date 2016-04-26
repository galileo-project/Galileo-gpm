from gpm import __version__ as version
from gpm import __name__ as name
from gpm.utils.console import puts
from gpm.cli import CLI
from gpm.utils.operation import LocalOperation

class CLIDefault(CLI):
    _OPTS    = {"shortcut": "vh", "name": ["version", "help"], "action": ["_version", "_help"], "default": "_help"}
    __doc__ = """
            GPM Manual
Usage:
    gpm [COMMAND] [option] [...]
List of commands:
    config:     Config user settings
    init:       Create and init project
    install:    Install gpm package
    test:       Run test commands
    remove:     Remove a gpm package by name
    dep:        Install dependent gpm package
    find:       find installed gpm package by name
    list:       List installed gpm package
    publish:    Publish a gpm package to GitHub
Options:
    -v, --version   Show gpm version
    -h, --help      Show gpm manual
    """

    def _version(self, *args, **kwargs):
        puts(LocalOperation.distr())
        puts("%s %s" % (name, version))

    @classmethod
    def _help(cls, *args, **kwargs):
        puts(cls.__doc__)


_MOD = CLIDefault
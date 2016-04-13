from gpm.utils.console import puts

class CLIBuild:
    _OPTS     = {"shortcut": "h", "fullname": ["help"], "action": ["_help"], "default": "_build"}
    __doc__ = """

    """
    def _build(self, config, *args, **kwargs):
        pass

    def _help(self, config, *args, **kwargs):
        puts(self.__doc__)

_MOD = CLIBuild
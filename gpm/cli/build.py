class CLIBuild:
    _OPTS     = {"shortcut": "h", "fullname": ["help"], "action": ["_help"], "default": "_build"}

    def _build(self, config, *args, **kwargs):
        pass

    def _help(self, config, *args, **kwargs):
        pass

_MOD = CLIBuild
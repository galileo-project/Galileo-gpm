from gpm.utils.opt import opt_parser

class CLIBuild:
    OPTS     = {"shortcut": "", "fullname": [], "action": []}
    _DEFAULT = "_build"

    def __init__(self, args):
        self._args = args

    def run(self):
        func, kwargs = opt_parser(self._args, self)
        func(**kwargs)

    def _build(self):
        pass

_MOD = CLIBuild
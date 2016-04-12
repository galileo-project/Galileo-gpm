from gpm.utils.console import put
from gpm.utils.color import yellow, red, magenta
import sys

class Log:
    @classmethod
    def warn(cls, msg):
        put(yellow("WARN: %s" % msg))

    @classmethod
    def fatal(cls, msg):
        put(red("FATAL: %s" % msg))
        sys.exit(1)

    @classmethod
    def debug(cls, msg):
        put(magenta("DEBUG: %s" % msg))
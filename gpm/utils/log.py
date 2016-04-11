from utils.console import put
from utils.color import yellow, red
import sys

class Log:
    @classmethod
    def warn(cls, msg):
        put(yellow("WARN: %s" % msg))

    @classmethod
    def fatal(cls, msg):
        put(red("FATAL: %s" % msg))
        sys.exit(1)
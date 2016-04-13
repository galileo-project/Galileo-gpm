from gpm.utils.console import puts
from gpm.utils.color import yellow, red, magenta
import sys

class Log(object):
    @classmethod
    def warn(cls, msg):
        puts(yellow("WARN: %s" % msg))

    @classmethod
    def fatal(cls, msg):
        puts(red("FATAL: %s" % msg))
        sys.exit(1)

    @classmethod
    def debug(cls, msg):
        puts(magenta("DEBUG: %s" % msg))
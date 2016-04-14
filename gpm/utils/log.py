import sys
from gpm.utils.console import puts
from gpm.utils.color import yellow, red, magenta, green
from gpm import __debug as debug

class Log(object):
    @classmethod
    def warn(cls, msg):
        puts(yellow("WARN: %s" % msg))

    @classmethod
    def fatal(cls, msg):
        msg =red("FATAL: %s" % msg)
        sys.stderr.write(msg)
        e = SystemExit(1)
        e.message = msg
        raise e

    @classmethod
    def debug(cls, msg):
        if debug:
            puts(magenta("DEBUG: %s" % msg))

    @classmethod
    def success(cls, msg):
        puts(green("SUCCESS: %s" % msg))

    @classmethod
    def puts(cls, msg):
        puts("SUCCESS: %s" % msg)
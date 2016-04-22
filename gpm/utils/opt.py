import getopt
from gpm.utils.log import Log
from gpm.const.status import Status

def get_opt_name(opt):
    if "--" in opt:
        return opt[2:], True
    elif "-" in opt:
        return opt[1:], False
    else:
        return None, False

def opt_parser(args, obj):
    optlist, args = getopt.getopt(args, obj._OPTS["shortcut"], obj._OPTS["name"])
    _dict = {}
    func = None

    for opt in optlist:
        opt_name, opt_type = get_opt_name(opt[0])
        if opt_name and opt_type is True:
            if opt_name in obj._OPTS["name"]:
                index = obj._OPTS["name"].index(opt_name)
            else:
                index = -1
        elif opt_name and opt_type is False:
            index = obj._OPTS["shortcut"].find(opt_name)
        else:
            index = -1

        if index == -1:
            Log.fatal(Status["STAT_OPT_INVALID"])

        func = obj.__getattribute__(obj._OPTS["action"][index])
        if func is None:
            _dict[obj._OPTS["name"]] = opt[1] or True

    return func, _dict, args
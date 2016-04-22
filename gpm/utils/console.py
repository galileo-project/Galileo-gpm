def puts(msg):
    print(msg)

def __gets(msg):
    try:
        return raw_input(msg)
    except NameError:
        return input(msg)

def gets(prompt, default = None):
    if default:
        prompt = "%s(%s):" %(prompt, default)
    else:
        prompt = "%s:" % prompt

    val = __gets(prompt)

    if not val:
        return default
    return val

def confirm(msg, default = False):
    msg = "%s[y/n]" % msg
    default = "y" if default else "n"
    res = gets(msg, default)
    if res and res[0].isalpha() and res[0].upper() == "Y":
        return True
    else:
        return False

def puts(msg):
    print(msg)

def gets(prompt, default = None):
    if default:
        prompt = "%s(%s):" %(prompt, default)
    else:
        prompt = "%s:" % prompt

    val = input(prompt)

    if not val == "":
        return default
    return val
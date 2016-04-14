_ENCODE = ["utf-8", "gbk"]

def decode(byte):
    for e in _ENCODE:
        try:
            string = byte.decode(e)
            return string
        except UnicodeDecodeError:
            pass
    raise Exception()
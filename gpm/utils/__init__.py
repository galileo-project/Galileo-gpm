def GitURL2Dir(url):
    if not url:
        return None
    elif not "/" in url:
        return url
    else:
        suffix = url.split("/")[-1]
        if not "." in  suffix:
            return suffix
        else:
            return suffix.split(".")[0]
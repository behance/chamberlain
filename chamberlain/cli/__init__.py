from sys import version_info

py3 = version_info[0] > 2


def user_confirm(msg, null_confirm=True):
    choice_defaults = "[N/y]"
    if null_confirm:
        choice_defaults = "[Y/n]"
    res = None
    if py3:
        res = input("%s %s: " % (msg, choice_defaults))
    else:
        res = raw_input("%s %s: " % (msg, choice_defaults))
    return (res.lower() == "y") or (len(res.strip()) == 0 and null_confirm)

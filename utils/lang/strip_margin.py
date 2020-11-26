import re


def strip_margin(text):
    return re.sub('\n[ \t]*\|', '\n', text)

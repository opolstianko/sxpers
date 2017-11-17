import re
from urllib.parse import unquote

def extract_mcmid(string):
    string = unquote(string)

    m = re.search('MCMID\|(.*?)\|', string)

    if m:
        return m.group(1)

    return False
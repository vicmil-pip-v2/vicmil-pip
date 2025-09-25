# install latest version of vizpip in this file
import urllib.request
with urllib.request.urlopen('https://raw.githubusercontent.com/vizpip/vizpip/refs/heads/main/vizpip.py') as f:
    html = f.read().decode('utf-8')
    with open(__file__, "w") as this_file:
        this_file.write(html)
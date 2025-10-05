# Bootstrap installer for vicmil-pip
import urllib.request

with urllib.request.urlopen(
    'https://raw.githubusercontent.com/vicmil-pip-v2/vicmil-pip/refs/heads/main/vicmil-pip.py'
) as f:
    code = f.read().decode('utf-8')
    with open(__file__, "w") as this_file:
        this_file.write(code)
import tempfile
import subprocess
import venv
import sys

with tempfile.TemporaryDirectory() as tmpdirname:
    venv.create(tmpdirname, with_pip=True)
    subprocess.run([tmpdirname + '/bin/pip', 'install', 'pyfiglet'])
    subprocess.run([tmpdirname + '/bin/python3', '-m', 'figdate'] + sys.argv[1:])



import locale
import pyfiglet
import sys
from datetime import datetime

def date(fmt="%Y %d %b, %A", font='graceful'):
    locale.setlocale(locale.LC_ALL, '')
    d = datetime.today().strftime(fmt)
    return pyfiglet.figlet_format(d, font=font)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(date())
    elif len(sys.argv) == 2:
        print(date(sys.argv[1]))
    else:
        print(date(sys.argv[1], sys.argv[2]))


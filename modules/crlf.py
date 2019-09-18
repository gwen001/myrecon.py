import sys
import subprocess
from colored import fg, bg, attr


def run( app ):
    sys.stdout.write( '[+] running mod: crlf\n'  )

    try:
        cmd = 'crlf.py -o ' + app.f_hosts
        # print(cmd)
        r = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
    except Exception as e:
        sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )

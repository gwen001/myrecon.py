# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import subprocess
from colored import fg, bg, attr


class Openredirect:
    
    def run( self, app ):
        sys.stdout.write( '[+] running mod: openredirect\n'  )
        cmd = 'open-redirect.py -o ' + app.f_hosts + ' 2>&1 >/dev/null &'
        os.system( cmd )
        # try:
        #     cmd = 'open-redirect.py -o ' + app.f_hosts
        #     # print(cmd)
        #     r = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        # except Exception as e:
        #     sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )



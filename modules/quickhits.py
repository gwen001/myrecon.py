# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import subprocess
from colored import fg, bg, attr


class Quickhits:

    def run( self, app ):
        sys.stdout.write( '[+] running mod: quickhits\n'  )
        cmd = 'quick-hits.py -f /opt/SecLists/mine/myhardw.txt -u ' + app.f_urls + ' 2>&1 >/dev/null &'
        os.system( cmd )
        # try:
        #     cmd = 'quick-hits.py -f /opt/SecLists/mine/myhardw.txt -u ' + app.f_urls
        #     # print(cmd)
        #     r = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        # except Exception as e:
        #     sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )

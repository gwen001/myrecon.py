# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import subprocess
from colored import fg, bg, attr


class Quickhits:

    def run( self, app ):
        sys.stdout.write( '[+] running mod: quickhits\n'  )
        cmd = eval( app.config['quickhits']['command'] )
        os.system( cmd )
        # try:
        #     cmd = 'quick-hits.py -f /opt/SecLists/mine/myhardw.txt -u ' + app.f_urls
        #     # print(cmd)
        #     r = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        # except Exception as e:
        #     sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )


    def getReportDatas( self, app ):
        t_vars = {}
        t_vars['quickhits'] = '-'
        f_output = app.d_output + app.config['quickhits']['output_file']

        if os.path.isfile(f_output):
            cmd = 'egrep "C=200\s*L=[^0]" ' + f_output
            try:
                output = subprocess.check_output( cmd, shell=True ).decode('utf-8')
                t_vars['quickhits'] = output
            except Exception as e:
                ex = 1
                # sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )

        return t_vars


# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import subprocess
from modules import functions as func
from colored import fg, bg, attr


class Openredirect:
    
    def run( self, app ):
        sys.stdout.write( '[+] running mod: %s\n' % self.__class__.__name__.lower() )

        cmd = eval( app.config['openredirect']['command'] )
        sys.stdout.write( '%s[*] %s%s\n' % (fg('dark_gray'),cmd,attr(0)) )
        os.system( cmd )
        # try:
        #     cmd = 'open-redirect.py -o ' + app.f_hosts
        #     # print(cmd)
        #     r = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        # except Exception as e:
        #     sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )


    def getReportDatas( self, app ):
        t_vars = {}
        t_vars['openredirect_vulnerable'] = '-'
        f_output = app.d_output + app.config['openredirect']['output_file']

        if os.path.isfile(f_output):
            cmd = 'egrep VULNERABLE ' + f_output
            sys.stdout.write( '%s[*] %s%s\n' % (fg('dark_gray'),cmd,attr(0)) )
            try:
                output = subprocess.check_output( cmd, shell=True ).decode('utf-8')
                t_vars['openredirect_vulnerable'] = output
            except Exception as e:
                ex = 1
                # sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )

        return t_vars


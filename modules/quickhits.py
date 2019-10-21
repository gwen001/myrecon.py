# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import subprocess
from modules import functions as func
from colored import fg, bg, attr


class Quickhits:

    def run( self, app ):
        sys.stdout.write( '[+] running mod: %s\n' % self.__class__.__name__.lower() )

        f_source = func.generateUrlsFile( app, True, False, False )
        cmd = eval( app.config['quickhits']['command'] )
        # print(cmd)
        os.system( cmd )

        # try:
        #     # r = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        #     output = subprocess.check_output( cmd, shell=True ).decode('utf-8')
        # except Exception as e:
        #     sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )


    def getReportDatas( self, app ):
        t_vars = {}
        t_vars['quickhits'] = '-'
        f_output = app.d_output + app.config['quickhits']['output_file']

        if os.path.isfile(f_output):
            cmd = 'egrep "C=200\s*L=[^0]" ' + f_output + ' | grep -v "T=text/html"'
            try:
                output = subprocess.check_output( cmd, shell=True ).decode('utf-8')
                t_vars['quickhits'] = output
            except Exception as e:
                ex = 1
                # sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )

        return t_vars


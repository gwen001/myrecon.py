# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import subprocess
from colored import fg, bg, attr


class Subto:
    d_output = '/subto'
    f_output = 'output'
    
    def run( self, app ):
        sys.stdout.write( '[+] running mod: %s\n' % self.__class__.__name__.lower() )

        self.d_output = app.d_output + self.d_output
        if not os.path.isdir(self.d_output):
            try:
                os.makedirs( self.d_output )
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                return

        self.f_output = self.d_output + '/' + self.f_output

        cmd = eval( app.config['subto']['command'] )
        sys.stdout.write( '[*] %s\n' % cmd )
        os.system( cmd )
        # try:
        #     # print(cmd)
        #     r = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        # except Exception as e:
        #     sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )


    def getReportDatas( self, app ):
        t_vars = {}
        t_vars['subto_vulnerable'] = '-'
        f_output = app.d_output + app.config['subto']['output_file']

        if os.path.isfile(f_output):
            cmd = 'egrep -v "Not Vulnerable" ' + f_output
            try:
                output = subprocess.check_output( cmd, shell=True ).decode('utf-8')
                t_vars['subto_vulnerable'] = output
            except Exception as e:
                ex = 1
                # sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )

        return t_vars


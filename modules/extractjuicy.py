# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import subprocess
from colored import fg, bg, attr


class Extractjuicy:
    
    def run( self, app ):
        sys.stdout.write( '[+] running mod: %s\n' % self.__class__.__name__.lower() )
        output_file = app.d_output + app.config['extractjuicy']['output_file']
        search_path = app.d_output + os.path.dirname(app.config['quickhits']['output_file'])

        # cmd = eval( app.config['crlf']['command'] )
        for regexp in app.config['extractjuicy']['regexp']:
            # print(regexp)
            cmd = 'grep -hraoE "' + regexp + '" ' + search_path + ' | tee -a "' + output_file + '"'
            # os.system( cmd )
            try:
                print(cmd)
                r = subprocess.check_output( cmd, shell=True )
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )


    def getReportDatas( self, app ):
        t_vars = {}
        t_vars['crlf_vulnerable'] = '-'
        f_output = app.d_output + app.config['crlf']['output_file']

        if os.path.isfile(f_output):
            cmd = 'egrep VULNERABLE ' + f_output
            try:
                output = subprocess.check_output( cmd, shell=True ).decode('utf-8')
                t_vars['crlf_vulnerable'] = output
            except Exception as e:
                ex = 1
                # sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )

        return t_vars


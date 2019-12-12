# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import json
import subprocess
from modules import functions as func
from colored import fg, bg, attr


class Quickhits:

    def run( self, app ):
        sys.stdout.write( '[+] running mod: %s\n' % self.__class__.__name__.lower() )

        cmd = eval( app.config['quickhits']['command'] )
        sys.stdout.write( '[*] %s\n' % cmd )
        os.system( cmd )

        # try:
        #     # r = subprocess.Popen( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT )
        #     output = subprocess.check_output( cmd, shell=True ).decode('utf-8')
        # except Exception as e:
        #     sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )


    def getReportDatas( self, app ):
        return self.getReportDatasFfuf( app )
        # return self.getReportDatasQuickhits( self, app )
    
    
    def getReportDatasFfuf( self, app ):
        t_vars = {}
        t_vars['quickhits'] = '-'
        f_output = app.d_output + app.config['quickhits']['output_file']

        if not os.path.isfile(f_output):
            return t_vars

        with open(f_output) as json_file:
            t_quickhits = json.load( json_file )

        if not 'results' in t_quickhits:
            return t_vars
        
        str_all = str_200 = ''

        for hit in t_quickhits['results']:
            str = "%s\t\t\t\tC=%d\tL=%d\tw=%d\tl=%d\n" % (hit['url'],hit['status'],hit['length'],hit['words'],hit['lines'])
            str_all = str_all + str
            if hit['status'] == 200:
                str_200 = str_200 + str
        
        fp = open( 'quickhits', 'w' )
        fp.write( str_all )
        fp.close
        
        if len(str_200):
            t_vars['quickhits'] = str_200
        
        return t_vars


    
    def getReportDatasQuickhits( self, app ):
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

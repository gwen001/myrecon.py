# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import re
import subprocess
from urllib.parse import urlparse
from modules import functions as func
from colored import fg, bg, attr


class Urls:

    def run( self, app ):
        sys.stdout.write( '[+] creating urls...\n' )

        if not os.path.isfile('hosts_ips'):
            return

        f_source = func.generateTempFile( app, ['hosts','ips'] )

        try:
            cmd = eval( app.config['ishttp']['command'] )
            output = subprocess.check_output( cmd, stderr=subprocess.STDOUT, shell=True ).decode('utf-8')
        except Exception as e:
            sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
            return

        t_urls_ips = []
        t_urls_hosts = []
        t_output = output.split("\n")

        for url in t_output:
            t_url_parse = urlparse( url )
            if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",t_url_parse.netloc):
                t_urls_ips.append( url )
            else:
                t_urls_hosts.append( url )

        fp = open( 'urls_ips', 'w' )
        fp.write( "\n".join(t_urls_ips) )
        fp.close()

        fp = open( 'urls_hosts', 'w' )
        fp.write( "\n".join(t_urls_hosts) )
        fp.close()

        sys.stdout.write( "%s[+] %d urls found.%s\n" % (fg('green'),len(t_urls_hosts)+len(t_urls_ips),attr(0)) )


    def getReportDatas( self, app ):
        t_vars = {}
        if os.path.isfile(app.f_urls):
            t_vars['n_urls'] = sum(1 for line in open(app.f_urls))
        return t_vars


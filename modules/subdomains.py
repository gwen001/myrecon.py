# I don't believe in license.
# You can do whatever you want with this program.

import os
import re
import sys
import subprocess
from colored import fg, bg, attr
from functools import partial
from multiprocessing.dummy import Pool


class Subdomains:
    hosts = []


    def run( self, app ):
        sys.stdout.write( '[+] looking for subdomains...\n' )

        t_multiproc = {
            'n_current': 0,
            'n_total': app.n_domains
        }

        pool = Pool( app.config['subdomains']['threads'] )
        pool.map( partial(self.find,app,t_multiproc), app.domains )
        pool.close()
        pool.join()

        app.setHosts( self.hosts )


    def find( self, app, t_multiproc, domain ):
        sys.stdout.write( 'progress: %d/%d\r' %  (t_multiproc['n_current'],t_multiproc['n_total']) )
        t_multiproc['n_current'] = t_multiproc['n_current'] + 1

        try:
            cmd = eval( app.config['subdomains']['command'] )
            output = subprocess.check_output( cmd, stderr=subprocess.STDOUT, shell=True ).decode('utf-8')
            # print(output)
        except Exception as e:
            sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
            return

        matches = re.findall( '([a-zA-Z0-9\._-]+\.'+domain+')', output)
        if matches:
            for sub in matches:
                sub = sub.strip('._- ')
                if sub not in self.hosts:
                    self.hosts.append( sub )


    def getReportDatas( self, app ):
        t_vars = {}
        if os.path.isfile(app.f_hosts):
            t_vars['n_hosts'] = sum(1 for line in open(app.f_hosts))
        return t_vars


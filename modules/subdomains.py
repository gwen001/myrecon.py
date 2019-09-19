# I don't believe in license.
# You can do whatever you want with this program.

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

        pool = Pool( 3 )
        pool.map( partial(self.find,t_multiproc), app.domains )
        pool.close()
        pool.join()

        app.setHosts( self.hosts )


    def find( self, t_multiproc, domain ):
        sys.stdout.write( 'progress: %d/%d\r' %  (t_multiproc['n_current'],t_multiproc['n_total']) )
        t_multiproc['n_current'] = t_multiproc['n_current'] + 1

        try:
            # cmd = 'findomain -t ' + domain
            cmd = 'assetfinder -subs-only  ' + domain
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

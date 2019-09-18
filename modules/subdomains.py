import re
import sys
import subprocess
from colored import fg, bg, attr
from functools import partial
from multiprocessing.dummy import Pool


class Subdomains( object ):
    hosts = []
    n_hosts = 0

    def run( self, t_domains ):
        sys.stdout.write( '[+] looking for subdomains...\n' )

        t_multiproc = {
            'n_current': 0,
            'n_total': len(t_domains)
        }

        pool = Pool( 3 )
        pool.map( partial(self.find,t_multiproc), t_domains )
        pool.close()
        pool.join()

        self.n_hosts = len(self.hosts)


    def find( self, t_multiproc, domain ):
        sys.stdout.write( 'progress: %d/%d\r' %  (t_multiproc['n_current'],t_multiproc['n_total']) )
        t_multiproc['n_current'] = t_multiproc['n_current'] + 1

        try:
            # cmd = 'sublist3r -d ' + domain
            cmd = 'findomain -t ' + domain
            output = subprocess.check_output( cmd, stderr=subprocess.STDOUT, shell=True ).decode('utf-8')
            # print(output)
        except Exception as e:
            sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
            return

        # matches = re.findall( '92m([a-zA-Z0-9\._-]+\.'+domain+')', output)
        matches = re.findall( '([a-zA-Z0-9\._-]+\.'+domain+')', output)
        if matches:
            for sub in matches:
                sub = sub.strip('._- ')
                if sub not in self.hosts:
                    self.hosts.append( sub )

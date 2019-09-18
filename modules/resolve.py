import re
import sys
import subprocess
from colored import fg, bg, attr
from functools import partial
from multiprocessing.dummy import Pool


class Resolve( object ):
    ips = []
    n_ips = 0
    dead_host = []
    n_dead = 0
    full_output = ''


    def run( self, t_hosts ):
        sys.stdout.write( '[+] running mod: resolve...\n' )

        t_multiproc = {
            'n_current': 0,
            'n_total': len(t_hosts)
        }

        pool = Pool( 10 )
        pool.map( partial(self.resolve,t_multiproc), t_hosts )
        pool.close()
        pool.join()

        self.n_ips = len(self.ips)
        self.n_dead = len(self.dead_host)


    def resolve( self, t_multiproc, host ):
        sys.stdout.write( 'progress: %d/%d\r' %  (t_multiproc['n_current'],t_multiproc['n_total']) )
        t_multiproc['n_current'] = t_multiproc['n_current'] + 1

        try:
            cmd = 'host ' + host
            output = subprocess.check_output( cmd, stderr=subprocess.STDOUT, shell=True ).decode('utf-8')
            # print(output)
            # ip = socket.gethostbyname( host )
        except Exception as e:
            # sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
            return

        self.full_output = self.full_output + output + "\n"

        matches = re.findall( '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', output )
        if matches:
            for ip in matches:
                if not ip in self.ips:
                    self.ips.append( ip )
        else:
            if host not in sef.dead_host:
                self.dead_host.append( host )

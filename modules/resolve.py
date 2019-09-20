# I don't believe in license.
# You can do whatever you want with this program.

import os
import re
import sys
import subprocess
from colored import fg, bg, attr
from functools import partial
from multiprocessing.dummy import Pool


class Resolve:
    ips = []
    dead_host = []
    full_output = ''


    def run( self, app ):
        sys.stdout.write( '[+] resolving...\n' )

        t_multiproc = {
            'n_current': 0,
            'n_total': app.n_hosts
        }

        pool = Pool( app.config['resolve']['threads'] )
        pool.map( partial(self.resolve,app,t_multiproc), app.hosts )
        pool.close()
        pool.join()

        app.setIps( self.ips, self.full_output )
        app.setDeadHosts( self.dead_host )


    def resolve( self, app, t_multiproc, host ):
        sys.stdout.write( 'progress: %d/%d\r' %  (t_multiproc['n_current'],t_multiproc['n_total']) )
        t_multiproc['n_current'] = t_multiproc['n_current'] + 1

        try:
            cmd = eval( app.config['resolve']['command'] )
            # print(cmd)
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
            if host not in self.dead_host:
                self.dead_host.append( host )


    def getReportDatas( self, app ):
        t_vars = {}
        if os.path.isfile(app.f_ips):
            t_vars['n_ips'] = sum(1 for line in open(app.f_ips))
        return t_vars


# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import json
import subprocess
from colored import fg, bg, attr


class Endpoints:

    def run( self, app ):
        sys.stdout.write( '[+] looking for endpoints...\n' )

        for c in app.config['endpoints']['commands']:
            for domain in app.domains:
                try:
                    cmd = eval( c )
                    print(cmd)
                    output = subprocess.check_output( cmd, stderr=subprocess.STDOUT, shell=True ).decode('utf-8')
                    # print(output)
                except Exception as e:
                    sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                    return

                # os.system( cmd )
        
        t_endpoints = []

        if os.path.isfile('endpoints_grabbed'):
            fp = open( 'endpoints_grabbed' )
            t_tmp = fp.read().split('\n')
            fp.close()

            for endpoint in t_tmp:
                if len(endpoint) and not endpoint in t_endpoints and not '>>>' in endpoint:
                    t_endpoints.append( endpoint )
        
        if os.path.isfile('raw_wayback'):
            with open('raw_wayback') as json_file:
                t_tmp = json.load( json_file )
                for endpoint in t_tmp:
                    endpoint = endpoint[0]
                    if len(endpoint) and not endpoint in t_endpoints and not '>>>' in endpoint:
                        t_endpoints.append( endpoint )

        fp = open( app.f_endpoints, 'w' )
        fp.write( "\n".join(t_endpoints) )
        fp.close()

        sys.stdout.write( "%s[+] %d endpoints found.%s\n" % (fg('green'),len(t_endpoints),attr(0)) )


    def getReportDatas( self, app ):
        t_vars = {}
        if os.path.isfile(app.f_urls):
            t_vars['n_endpoints'] = sum(1 for line in open(app.f_urls))
        return t_vars


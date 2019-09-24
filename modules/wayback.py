# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import time
import json
import requests
from colored import fg, bg, attr
from functools import partial
from multiprocessing.dummy import Pool


class Wayback:
    d_output = '/wayback'


    def run( self, app ):
        sys.stdout.write( '[+] running mod: wayback\n'  )

        self.d_output = app.d_output + self.d_output
        if not os.path.isdir(self.d_output):
            try:
                os.makedirs( self.d_output )
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                return
        
        t_multiproc = {
            'n_current': 0,
            'n_total': app.n_domains
        }

        pool = Pool( app.config['wayback']['threads'] )
        pool.map( partial(self.wayback,app,t_multiproc), app.domains )
        pool.close()
        pool.join()


    def wayback( self, app, t_multiproc, domain ):
        time.sleep( 0.2 )
        sys.stdout.write( 'progress: %d/%d\r' %  (t_multiproc['n_current'],t_multiproc['n_total']) )
        t_multiproc['n_current'] = t_multiproc['n_current'] + 1

        if app.config['wayback']['include_subdomains']:
            wildcard = '*.'
        else:
            wildcard = ''

        url = 'http://web.archive.org/cdx/search/cdx?url=' + wildcard + domain + '/*&output=json&fl=original&collapse=urlkey'

        try:
            r = requests.get( url, timeout=3 )
        except Exception as e:
            sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
            return

        # print(type(t_json[1]))
        # print( t_json[1] )
        # output = json.dumps(t_json)
        # print( output )
        # output = "\n".join(t_json[0])
        # print(json.dumps(t_json[1:]))
        t_urls = []
        t_json = r.json()[1:]
        
        for url in t_json:
            if not url[0] in t_urls:
                t_urls.append( url[0] )

        f_output = self.d_output + '/' + domain
        fp = open( f_output, 'w' )
        fp.write( '%s' % "\n".join(sorted(t_urls)) )
        fp.close()


    def getReportDatas( self, app ):
        t_vars = {}
        return t_vars

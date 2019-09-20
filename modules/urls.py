# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
from colored import fg, bg, attr


class Urls:

    def run( self, app ):
        urls = []
        sys.stdout.write( '[+] creating urls...\n' )

        for host in app.hosts:
            urls.append( 'http://'+host )
            urls.append( 'https://'+host )
        for ip in app.ips:
            urls.append( 'http://'+ip )
            urls.append( 'https://'+ip )

        app.setUrls( urls )


    def getReportDatas( self, app ):
        t_vars = {}
        if os.path.isfile(app.f_urls):
            t_vars['n_urls'] = sum(1 for line in open(app.f_urls))
        return t_vars


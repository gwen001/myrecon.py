# I don't believe in license.
# You can do whatever you want with this program.

import sys
from colored import fg, bg, attr


class Resume:

    def run( self, app ):
        sys.stdout.write( '[+] resume session, loading datas...\n'  )

        app.domains = open(app.f_domains).read().split("\n")
        app.hosts = open(app.f_hosts).read().split("\n")
        app.ips = open(app.f_ips).read().split("\n")
        app.urls = open(app.f_urls).read().split("\n")



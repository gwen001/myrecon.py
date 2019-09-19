# I don't believe in license.
# You can do whatever you want with this program.

import os
import imp
import sys
import time
from modules import functions as func
from colored import fg, bg, attr

_config = {
    'available_mods': ['screenshot', 'quickhits', 'crlf', 'openredirect'],
    'mandatory_mods' : ['subdomains', 'resolve', 'urls']
}

class App( object ):
    mods = []
    
    d_output   = ''
    f_domains  = ''
    f_hosts    = ''
    f_tmphosts = ''
    f_dead     = ''
    f_ips      = ''
    f_urls     = ''
    
    domains   = []
    n_domains = 0
    
    hosts    = []
    tmphosts = ''
    n_hosts  = 0
    dead   = []
    n_dead = 0
    
    ips   = []
    n_ips = 0
    
    urls   = []
    n_urls = 0


    def init( self ):
        func.parseargs( self, _config )
    

    def run( self ):
        for mod_name in self.mods:
            mod_name = mod_name.lower()
            filepath = os.path.dirname( os.path.realpath(__file__) ) + '/' + mod_name + '.py'
            py_mod = imp.load_source( mod_name.capitalize(), filepath)
            mod = getattr( py_mod, mod_name.capitalize() )()
            mod.run( self )


    def wait( self ):
        i = 0
        t_chars = ['|','/','-','\\','|','/','-']
        l = len(t_chars)

        sys.stdout.write( "\n\n" )

        for n in range(100000):
            time.sleep( 0.5 )
            sys.stdout.write( ' %s\r' % t_chars[n%l] )


    def setMods( self, t_mods ):
        self.mods = t_mods


    def setOutputDirectory( self, d_output ):
        self.d_output = os.getcwd().rstrip('/')
        sys.stdout.write( '[+] output directory is: %s\n' % self.d_output )
        self.initFilePath()


    def initFilePath( self ):
        self.f_domains  = self.d_output + '/domains'
        self.f_hosts    = self.d_output + '/hosts'
        self.f_tmphosts = self.d_output + '/tmp_hosts'
        self.f_dead     = self.d_output + '/dead'
        self.f_ips      = self.d_output + '/ips'
        self.f_urls     = self.d_output + '/urls'


    def setDomains( self, t_domains ):
        self.domains = t_domains
        self.n_domains = len(t_domains)
        sys.stdout.write( '%s[+] %d domains found.%s\n' %  (fg('green'),self.n_domains,attr(0)) )

        if self.n_domains:
            fp = open( self.f_domains, 'w' )
            fp.write( "\n".join(self.domains) )
            fp.close()
            sys.stdout.write( '[+] saved in %s\n' % self.f_domains )


    def setHosts( self, t_hosts ):
        self.hosts = t_hosts
        self.n_hosts = len(t_hosts)
        sys.stdout.write( '%s[+] %d hosts found.%s\n' %  (fg('green'),self.n_hosts,attr(0)) )

        if self.n_hosts:
            fp = open( self.f_hosts, 'w' )
            fp.write( "\n".join(self.hosts) )
            fp.close()
            sys.stdout.write( '[+] saved in %s\n' % self.f_hosts )


    def setIps( self, t_ips, tmphosts ):
        self.ips = t_ips
        self.n_ips = len(t_ips)
        sys.stdout.write( '%s[+] %d ips found.%s\n' %  (fg('green'),self.n_ips,attr(0)) )

        if self.n_ips:
            fp = open( self.f_ips, 'w' )
            fp.write( "\n".join(t_ips) )
            fp.close()
            sys.stdout.write( '[+] saved in %s\n' % self.f_ips )

        if len(tmphosts):
            fp = open( self.f_tmphosts, 'w' )
            fp.write( tmphosts )
            fp.close()


    def setDeadHosts( self, t_dead ):
        sys.stdout.write( '[+] %d dead hosts found, cleaning...\n' %  len(t_dead) )

        for host in t_dead:
            self.hosts.remove( host )


    def setUrls( self, t_urls ):
        self.urls = t_urls
        self.n_urls = len(t_urls)
        sys.stdout.write( '%s[+] %d urls created.%s\n' %  (fg('green'),self.n_urls,attr(0)) )

        if self.n_urls:
            fp = open( self.f_urls, 'w' )
            fp.write( "\n".join(self.urls) )
            fp.close()
            sys.stdout.write( '[+] saved in %s\n' % self.f_urls )

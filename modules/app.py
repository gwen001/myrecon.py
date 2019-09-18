import os
import sys
import time
from colored import fg, bg, attr


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
    
    hosts   = []
    n_hosts = 0
    
    ips   = []
    n_ips = 0
    
    dead   = []
    n_dead = 0
    
    urls   = []
    n_urls = 0


    def wait( self ):
        i = 0
        t_chars = ['|','/','-','\\','|','/','-']
        l = len(t_chars)

        sys.stdout.write( "\n\n" )

        for n in range(100000):
            time.sleep( 0.5 )
            sys.stdout.write( ' %s\r' % t_chars[n%l] )


    def __init__( self, t_mods ):
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


    def setIps( self, t_ips, full_output ):
        self.ips = t_ips
        self.n_ips = len(t_ips)
        sys.stdout.write( '%s[+] %d ips found.%s\n' %  (fg('green'),self.n_ips,attr(0)) )

        if self.n_ips:
            fp = open( self.f_ips, 'w' )
            fp.write( "\n".join(t_ips) )
            fp.close()
            sys.stdout.write( '[+] saved in %s\n' % self.f_ips )

        fp = open( self.f_tmphosts, 'w' )
        fp.write( full_output )
        fp.close()


    def setDeadHosts( self, t_dead ):
        sys.stdout.write( '[+] %d dead hosts found, cleaning...\n' %  len(t_dead) )

        for host in t_dead:
            self.hosts.remove( host )


    def createUrls( self ):
        sys.stdout.write( '[+] creating urls...\n' )

        for host in self.hosts:
            self.urls.append( 'http://'+host )
            self.urls.append( 'https://'+host )
        for ip in self.ips:
            self.urls.append( 'http://'+ip )
            self.urls.append( 'https://'+ip )

        self.n_urls = len( self.urls )
        sys.stdout.write( '%s[+] %d urls created.%s\n' %  (fg('green'),self.n_urls,attr(0)) )

        if self.urls:
            fp = open( self.f_urls, 'w' )
            fp.write( "\n".join(self.urls) )
            fp.close()
            sys.stdout.write( '[+] saved in %s\n' % self.f_urls )

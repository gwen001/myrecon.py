# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import imp
import time
from modules import functions as func
from colored import fg, bg, attr


class App:
    config = []
    mods = []
    
    d_app      = ''
    d_mods     = ''
    d_output   = ''
    f_report   = ''
    f_domains  = ''
    f_hosts    = ''
    f_tmphosts = ''
    f_alive    = ''
    f_dead     = ''
    f_ips      = ''
    f_urls     = ''
    f_urls_ips     = ''
    f_urls_hosts   = ''
    f_endpoints    = ''
    
    domains   = []
    n_domains = 0
    
    hosts    = []
    tmphosts = ''
    n_hosts  = 0
    alive   = []
    n_alive = 0
    dead   = []
    n_dead = 0
    
    ips   = []
    n_ips = 0
    
    urls   = []
    n_urls = 0


    def __init__( self, config ):
        self.config = config
        self.d_app = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )
        self.d_mods = self.d_app + '/modules'


    def init( self ):
        func.parseargs( self )


    def run( self ):
        for mod_name in self.mods:
            if mod_name in self.config['mandatory_mods'] or 'resume' in self.mods or 'report' in self.mods:
            # if mod_name in self.config['mandatory_mods'] or 'resume' in self.mods:
                self.runMod( mod_name )
            else:
                self.launchMod( mod_name )


    def runMod( self, mod_name ):
        mod_file = self.d_mods + '/' + mod_name + '.py'

        if not os.path.isfile(mod_file):
            sys.stdout.write( "%s[-] error occurred: mod %s not found%s\n" % (fg('red'),mod_name,attr(0)) )
        else:
            py_mod = imp.load_source( mod_name.capitalize(), mod_file)
            mod = getattr( py_mod, mod_name.capitalize() )()
            try:
                mod.run( self )
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
            # if hasattr(mod,'postrun'):
            #     mod.postrun( self )
            # if hasattr(mod,'report'):
            #     mod.report( self )


    def launchMod( self, mod_name ):
        cmd = sys.argv[0] + ' -r -m ' + mod_name + ' 2>&1 &'
        # print( cmd )
        os.system( cmd )


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
        self.d_output = d_output.rstrip('/')
        sys.stdout.write( '[+] output directory is: %s\n' % self.d_output )
        self.initFilePath()


    def initFilePath( self ):
        self.f_report   = self.d_output + '/report'
        self.f_domains  = self.d_output + '/domains'
        self.f_hosts    = self.d_output + '/hosts'
        self.f_tmphosts = self.d_output + '/tmp_hosts'
        self.f_alive    = self.d_output + '/hosts_alive'
        self.f_dead     = self.d_output + '/hosts_dead'
        self.f_ips      = self.d_output + '/ips'
        self.f_urls     = self.d_output + '/urls'
        self.f_urls_ips = self.d_output + '/urls_ips'
        self.f_urls_hosts = self.d_output + '/urls_hosts'
        self.f_endpoints = self.d_output + '/endpoints'


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


    def setAliveHosts( self, t_alive ):
        sys.stdout.write( '[+] %d hosts alive found\n' %  len(t_alive) )

        if len(t_alive):
            for host in t_alive:
                self.hosts.remove( host )
            
            fp = open( self.f_alive, 'w' )
            fp.write( "\n".join(t_alive) )
            fp.close()


    def setDeadHosts( self, t_dead ):
        sys.stdout.write( '[+] %d dead hosts found, cleaning...\n' %  len(t_dead) )

        if len(t_dead):
            for host in t_dead:
                self.hosts.remove( host )
            
            fp = open( self.f_dead, 'w' )
            fp.write( "\n".join(t_dead) )
            fp.close()
        

    def setUrls( self, t_urls ):
        self.urls = t_urls
        self.n_urls = len(t_urls)
        sys.stdout.write( '%s[+] %d urls created.%s\n' %  (fg('green'),self.n_urls,attr(0)) )

        if self.n_urls:
            fp = open( self.f_urls, 'w' )
            fp.write( "\n".join(self.urls) )
            fp.close()
            sys.stdout.write( '[+] saved in %s\n' % self.f_urls )
    
    def setUrlsIps( self, t_new_urls ):
        new_urls = len(t_new_urls)
        sys.stdout.write( '%s[+] %d urls created.%s\n' %  (fg('green'),new_urls,attr(0)) )

        if new_urls:
            fp = open( self.f_urls_ips, 'w' )
            fp.write( "\n".join(t_new_urls) )
            fp.close()
            sys.stdout.write( '[+] saved in %s\n' % self.f_urls_ips )

    def getReportDatas( self ):
        t_vars = {}
        if os.path.isfile(self.f_domains):
            t_vars['n_domains'] = sum(1 for line in open(self.f_domains))
        return t_vars


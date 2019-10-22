# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import time
import subprocess
from goop import goop
import urllib.parse
from colored import fg, bg, attr
from functools import partial
from multiprocessing.dummy import Pool


class Googledorks:
    d_output = '/googledorks'
    f_output = 'output'
    results = {}


    def run( self, app ):
        sys.stdout.write( '[+] running mod: %s\n' % self.__class__.__name__.lower() )

        self.d_output = app.d_output + self.d_output
        if not os.path.isdir(self.d_output):
            try:
                os.makedirs( self.d_output )
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                return

        self.f_output = self.d_output + '/' + self.f_output
        
        if not os.path.exists( app.config['googledorks']['dorks_file']):
            sys.stdout.write( '%s[-] file not found: %s%s\n' % (fg('red'),app.config['googledorks']['dorks_file'],attr(0)) )
            return

        fp = open( app.config['googledorks']['dorks_file'], 'r' )
        t_dorks = fp.read().split("\n")

        t_alldorks = []
        for domain in app.domains:
            for dork in t_dorks:
                t_alldorks.append( dork.strip().replace('__SITE__',domain) )
        
        t_multiproc = {
            'n_current': 0,
            'n_total': len(t_alldorks) * app.config['googledorks']['n_pages']
        }

        pool = Pool( app.config['googledorks']['threads'] )
        pool.map( partial(self.dorkit,app,t_multiproc), t_alldorks )
        pool.close()
        pool.join()

        fp = open( self.f_output, 'w' )

        for dork in sorted(self.results.keys()):
            dork_url = self.getDorkUrl( dork )
            n_results = len(self.results[dork])
            fp.write( '>>> %s (%d)\n' % (dork_url,n_results) )
            fp.write( "%s\n\n" % '\n'.join(self.results[dork]) )
        
        fp.close()
    

    def getReportDatas( self, app ):
        t_vars = {}
        t_vars['googledorks'] = '-'
        self.d_output = app.d_output + self.d_output
        self.f_output = self.d_output + '/' + self.f_output

        output = ''
        if os.path.isfile(self.f_output):
            fp = open( self.f_output, 'r' )
            for line in fp.readlines():
                # print(line)
                if line.startswith('>>>') and not '(0)' in line:
                    output = output + line.replace( '>>> ', '' )
            if len(output):
                t_vars['googledorks'] = output

        return t_vars


    def getDorkUrl( self, dork ):
        return 'https://www.google.com/search?q=' + urllib.parse.quote(dork)


    def dorkit( self, app, t_multiproc, dork ):
        pool = Pool( app.config['googledorks']['threads'] )
        pool.map( partial(self.googleit,app,t_multiproc,dork), range(0,app.config['googledorks']['n_pages']) )
        pool.close()
        pool.join()


    def googleit( self, app, t_multiproc, dork, page ):
        time.sleep( 0.2 )
        sys.stdout.write( 'progress: %d/%d\r' %  (t_multiproc['n_current'],t_multiproc['n_total']) )
        t_multiproc['n_current'] = t_multiproc['n_current'] + 1

        # if not dork in self.results:
        #     self.results[dork] = []
        # self.results[dork].append( 'http://ex.com' )
        # self.results[dork].append( 'http://ex.com' )
        # return

        # cmd = 'google --start 0 --stop=5 --rua ' + dork
        # output = subprocess.check_output( cmd, shell=True ).decode('utf-8')
        # print(output)

        # for link in output.split("\n"):
        #     if app.config['googledorks']['urldecode']:
        #         link = urllib.parse.unquote( link )
        #     if not dork in self.results:
        #         self.results[dork] = []
        #     self.results[dork].append( link )
        
        search_results = goop.search( dork, app.config['googledorks']['fb_cookie'], page, True )
        # print(search_results)

        for i in search_results:
            link = search_results[i]['url']
            if app.config['googledorks']['urldecode']:
                link = urllib.parse.unquote( link )
            if not dork in self.results:
                self.results[dork] = []
            self.results[dork].append( link )

        # print(self.results)
        

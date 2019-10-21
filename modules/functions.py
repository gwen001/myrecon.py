# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import random
import argparse
import tldextract


def parseargs( app ):
    parser = argparse.ArgumentParser()
    parser.add_argument( "-r","--resume",help="resume previous recon", action="store_true" )
    parser.add_argument( "-d","--domain",help="domain, single, multiples or files", action="append" )
    parser.add_argument( "-o","--output",help="output dir" )
    parser.add_argument( "-m","--mod",help="mods to run, can be: report, "+', '.join(app.config['optional_mods'])+". Default: all but report" )
    parser.parse_args()
    args = parser.parse_args()

    if args.output:
        if os.path.isdir(args.output):
            output_dir = args.output
        else:
            try:
                os.makedirs( args.output )
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                exit()
            d_output = args.output
    else:
        d_output = os.getcwd()

    t_mods = []
    if args.mod:
        args.mod = args.mod.lower()
        if args.mod == 'all':
            t_mods = app.config['optional_mods']
            # t_mods.remove( 'report' )
        else:
            args_mods = args.mod.split(',')
            if 'report' in args_mods:
                t_mods = ['report']
            else:
                for m in args_mods:
                    mod_file = os.path.dirname( os.path.realpath(__file__) ) + '/' + m + '.py'
                    if not m in app.config['optional_mods'] or not os.path.isfile(mod_file):
                        parser.error( "[-] error occurred: %s not supported" % m )
                        exit()
                    t_mods.append( m )
    else:
        t_mods = app.config['optional_mods']
        # t_mods.remove( 'report' )
        if not len(t_mods):
            parser.error( 'mod missing' )
    
    t_domains = []
    if args.domain:
        for d in args.domain:
            if os.path.isfile(d):
                sys.stdout.write( '[+] loading file: %s\n' %  d )
                for l in open(d,'r'):
                    l = l.strip()
                    if isDomain(l) and l not in t_domains:
                        t_domains.append( l )
            else:
                if isDomain( d ) and d not in t_domains:
                    t_domains.append( d )
    
    app.setOutputDirectory( d_output )

    if not 'report' in t_mods:
        if args.resume:
            t_mods = ['resume'] + t_mods
        else:
            t_mods = app.config['mandatory_mods'] + t_mods
            if not len(t_domains):
                parser.error( 'domain missing' )
            else:
                app.setDomains( t_domains )
    
    app.setMods( t_mods )


def isDomain( str ):
    t_parse = tldextract.extract( str )
    if t_parse.subdomain == '' and t_parse.domain != '' and t_parse.suffix != '':
        return True
    else:
        return False


def generateUrlsFile( app, hosts, ips, http ):
    t_urls = []
    f_urls = '/tmp/tempurls_' + str(random.randint(1000,9999))

    fp = open( f_urls, 'w' )

    if hosts and len(app.hosts):
        for h in app.hosts:
            fp.write( 'https://'+h+'\n' )
            if http:
                fp.write( 'http://'+h+'\n' )
    
    if ips and len(app.ips):
        for i in app.ips:
            fp.write( 'https://'+i+'\n' )
            if http:
                fp.write( 'http://'+i+'\n' )

    fp.close()

    return f_urls
    
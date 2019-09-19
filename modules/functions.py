# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import argparse
import tldextract


def parseargs( app, config ):
    parser = argparse.ArgumentParser()
    parser.add_argument( "-d","--domain",help="domain, single, multiples or files", action="append" )
    parser.add_argument( "-o","--output",help="output dir" )
    parser.add_argument( "-m","--mod",help="mods to run, can be: "+', '.join(config['available_mods'])+". Default: all" )
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

    if args.domain:
        t_domains = []
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
        if not len(t_domains):
            parser.error( 'domain missing' )
    else:
        parser.error( 'domain missing' )

    if args.mod:
        t_mods = []
        for m in args.mod.split(','):
            if not m in config['available_mods'] and m != 'all':
                parser.error( ("mod '%s' doesn't exist" % m) )
                # sys.stdout.write( "%s[-] mod %s doesn't exist.%s\n" % (fg('red'),m,attr(0)) )
            else:
                if m == 'all':
                    t_mods = config['available_mods']
                    break
                else:
                    t_mods.append( m )
        if not len(t_mods):
            parser.error( 'mod missing' )
    else:
        t_mods = config['available_mods']

    app.setOutputDirectory( d_output )
    app.setDomains( t_domains )
    app.setMods( config['mandatory_mods']+t_mods )


def isDomain( str ):
    t_parse = tldextract.extract( str )
    if t_parse.subdomain == '' and t_parse.domain != '' and t_parse.suffix != '':
        return True
    else:
        return False

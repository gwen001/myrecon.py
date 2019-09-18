#!/usr/bin/python3.5

# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import argparse
from modules import functions as func
from colored import fg, bg, attr


t_available_mods = ['resolve', 'screenshot', 'quickhits', 'crlf', 'openredirect']


#
# Handling command line arguments
#
parser = argparse.ArgumentParser()
parser.add_argument( "-d","--domain",help="domain, single, multiples or files", action="append" )
parser.add_argument( "-o","--output",help="output dir" )
parser.add_argument( "-m","--mod",help="mods to run, can be: resolve, screenshots, quickhits, crlf, openredirect. Default: resolve,screenshots,quickhits" )
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
                if func.isDomain(l) and l not in t_domains:
                    t_domains.append( l )
        else:
            if func.isDomain( d ) and d not in t_domains:
                t_domains.append( d )
    if not len(t_domains):
        parser.error( 'domain missing' )
else:
    parser.error( 'domain missing' )

if args.mod:
    t_mods = []
    for m in args.mod.split(','):
        if not m in t_available_mods and m != 'all':
            parser.error( ("mod '%s' doesn't exist" % m) )
            # sys.stdout.write( "%s[-] mod %s doesn't exist.%s\n" % (fg('red'),m,attr(0)) )
        else:
            if m == 'all':
                t_mods = t_available_mods
                break
            else:
                t_mods.append( m )
    if not len(t_mods):
        parser.error( 'mod missing' )
else:
    t_mods = t_available_mods
#
# ###
#

#
# init app
#
from modules.app import App

app = App( t_mods )
app.setOutputDirectory( d_output )
app.setDomains( t_domains )
#
# ###
#


#
# MOD: subdomains
#
from modules.subdomains import Subdomains

mod = Subdomains()
mod.run( app.domains )

if not mod.n_hosts:
    exit()

app.setHosts( mod.hosts )
#
# ###
#


#
# MOD: resolve
#
if 'resolve' in app.mods:
    from modules.resolve import Resolve

    mod = Resolve()
    mod.run( app.hosts )

    app.setIps( mod.ips, mod.full_output )

    if mod.n_dead:
        app.setDeadHosts( mod.dead_host )
#
# ###
#


#
# create urls used by other tools
#
app.createUrls()
#
# ###
#


#
# optional modules
#
if 'screenshot' in app.mods:
    from modules import screenshot
    screenshot.run( app )

if 'quickhits' in app.mods:
    from modules import quickhits
    quickhits.run( app )

if 'crlf' in app.mods:
    from modules import crlf
    crlf.run( app )

if 'openredirect' in app.mods:
    from modules import openredirect
    openredirect.run( app )
#
# ###
#


app.wait()


# next
# cors
# google dorks
# new subdomains
# endpoints
# gf mykeys
# gf noisy
# gf takeovers
# final report

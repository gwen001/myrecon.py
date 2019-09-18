#!/usr/bin/python3.5

# I don't believe in license.
# You can do whatever you want with this program.

t_available_mods = ['resolve', 'screenshot', 'quickhits', 'crlf', 'openredirect']


#
# init app
#
from modules import functions as func
from modules.app import App

app = App()
func.parseargs( app, t_available_mods )
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


# app.wait()


# next
# cors
# google dorks
# new subdomains
# endpoints
# gf mykeys
# gf noisy
# gf takeovers
# final report

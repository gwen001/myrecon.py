#!/usr/bin/python3.5

# I don't believe in license.
# You can do whatever you want with this program.
import os


config = {
    'available_mods': ['screenshot', 'quickhits', 'crlf', 'openredirect', 'googledorks'],
    'mandatory_mods' : ['subdomains', 'resolve', 'urls'],
    'forbidden_mods' : ['app', 'functions'],
    'report_template': 'report.tpl',
    'subdomains': {
        'threads': 5,
        # 'command': 'assetfinder -subs-only __DOMAIN__'
        # 'command': 'subfinder -d __DOMAIN__'
        # 'command': 'amass -d __DOMAIN__'
        'command': "'findomain -t ' + domain"
    },
    'resolve': {
        'threads': 10,
        'command': "'host ' + host"
    },
    'screenshot': {
        'output_dir': '/screenshot/screens',
        'command': "'EyeWitness --headless -f \"' + app.f_urls + '\" --user-agent \"Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0\" --no-prompt --threads 10 -d \"' + app.d_output + '/screenshot\" 2>&1 >/dev/null &'"
    },
    'crlf': {
        'output_file': '/crlf/output',
        'command': "'crlf.py -o \"' + app.f_hosts + '\" 2>&1 >/dev/null &'"
    },
    'openredirect': {
        'output_file': '/openredirect/output',
        'command': "'open-redirect.py -o \"' + app.f_hosts + '\" 2>&1 >/dev/null &'"
    },
    'quickhits': {
        'output_file': '/quickhits/output',
        'command': "'quick-hits.py -f \"/opt/SecLists/mine/myhardw.txt\" -u \"' + app.f_urls + '\" 2>&1 >/dev/null &'"
    },
    'googledorks': {
        'threads': 5,
        'n_pages': 1,
        'urldecode': True,
        'dorks_file': '/opt/SecLists/mine/gg-dorks.txt',
        'fb_cookie': os.getenv( 'FACEBOOK_COOKIE' )
    }
}


# init
from modules.app import App

# run
app = App( config )
app.init()
app.run()


######### TODO
# waybackurls
# masscan

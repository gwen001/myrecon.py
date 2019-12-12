#!/usr/bin/python3.5

# I don't believe in license.
# You can do whatever you want with this program.
import os


config = {
    'optional_mods': ['screenshot', 'quickhits', 'crlf', 'openredirect', 'cors', 'subto', 'xss', 'smuggling'],
    'mandatory_mods' : ['subdomains', 'resolve', 'urls', 'endpoints'],
    'forbidden_mods' : ['app', 'functions', 'resume'],
    'report_template': 'report.tpl',
    'subdomains': {
        'threads': 5,
        'command': "'assetfinder -subs-only ' + domain"
        # 'command': "'findomain -t ' + domain"
    },
    'endpoints': {
        'commands': [
            "'github-endpoints.py -d ' + domain + ' -s | tee -a raw_github-endpoints endpoints_grabbed 2>&1 >/dev/null &'",
            "'google-search.py -d -e 100 -t \"site:' + domain + '\" | tee -a raw_google-domain endpoints_grabbed 2>&1 >/dev/null &'",
            "'google-search.py -d -e 100 -t \"site:' + domain + ' inurl:&\" | tee -a raw_google-domain endpoints_grabbed 2>&1 >/dev/null &'",
            "'waybackurls ' + domain + ' true ' + os.getcwd() + '/raw_wayback 2>&1 >/dev/null &'",
        ]
    },
    'ishttp': {
        'command': "'cat \"' + f_source + '\" | httprobe -t 2000 -p large | tee -a \"' + app.f_urls + '\" 2>&1 >/dev/null &'"
    },
    'resolve': {
        'threads': 10,
        'command': "'host ' + host"
    },
    'screenshot': {
        # 'output_dir': '/screenshot/screens',
        'output_dir': '/screenshot/screenshots',
        'command': "'cat \"' + app.f_urls + '\" | aquatone -out screenshot 2>&1 >/dev/null &'"
        # 'command': "'EyeWitness --headless -f \"' + f_source + '\" --user-agent \"Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0\" --no-prompt --threads 10 -d \"' + app.d_output + '/screenshot\" 2>&1 >/dev/null &'"
    },
    'smuggling': {
        'output_file': '/smuggler/output',
        'command': "'smuggler.py -v 0 -t 50 -u \"' + app.f_urls_hosts + '\" 2>&1 >/dev/null &'"
    },
    'crlf': {
        'output_file': '/crlf/output',
        'command': "'crlf.py -t 200 -u \"' + app.f_urls_hosts + '\" 2>&1 >/dev/null &'"
    },
    'cors': {
        'output_file': '/cors/output',
        'command': "'cors.py -t 100 -o \"' + app.f_urls_hosts + '\" 2>&1 >/dev/null &'"
    },
    'openredirect': {
        'output_file': '/openredirect/output',
        'command': "'openredirect.py -t 100 -u \"' + app.f_urls_hosts + '\" 2>&1 >/dev/null &'"
    },
    'quickhits': {
        'output_file': '/raw_quickhits',
        # 'command': "'quickhits.py -g -t 100 -f \"/opt/SecLists/mine/myhardw.txt\" -u \"' + f_source + '\" 2>&1 >/dev/null'"
        'command': "'ffuf -u HFUZZ/WFUZZ -w \"' + app.f_urls + '\":HFUZZ -w \"/opt/SecLists/mine/myhardw.txt\":WFUZZ -o raw_quickhits 2>&1 >/dev/null'"
    },
    'googledorks': {
        'threads': 5,
        'n_pages': 1,
        'urldecode': True,
        'dorks_file': '/opt/SecLists/mine/gg-dorks.txt',
        'fb_cookie': os.getenv( 'FACEBOOK_COOKIE' )
    },
    'wayback': {
        'threads': 2,
        'include_subdomains': True,
    },
    'portscan': {
        'output_file': '/portscan/output',
        'command': "'sudo masscan -p0-65535 --rate=10000 --open-only -iL ' + app.f_ips + ' -oX \"portscan/output\" 2>&1 >/dev/null &'"
    },
    'subto': {
        'output_file': '/subto/output',
        'command': "'subjack -a -t 50 -timeout 20 -ssl -c \"/opt/SecLists/mine/subjack_fingerprints.json\" -v -w \"' + app.f_hosts + '\" -o \"subto/output\" 2>&1 >/dev/null &'"
    },
    'xss': {
        'output_file': '/xss/output',
        'command': "'xss.py -t 20 -n \"/usr/local/bin/phantomjs\" -p \"/opt/SecLists/mine/xss-myshort.txt\" -u \"' + app.f_endpoints + '\" 2>&1 >/dev/null &'"
    },
    'extractjuicy': {
        'output_file': '/juicy',
        'regexp': [
            "[a-z0-9._-]*s3[a-z0-9.-]*\\.amazonaws\\.com[\\\\]?/?([a-z0-9._-]+)?",
            "xox[pboa]-[0-9]{10,12}-[0-9]{10,12}(-[0-9]{10,12})?-[a-zA-Z0-9]{24,32}",
            "T[a-zA-Z0-9_]{8}[\\\\]?/B[a-zA-Z0-9_]{8}[\\\\]?/[a-zA-Z0-9_]{24}",
            "(AKIA|A3T|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{12,}",
            "[psr]k_live_[0-9a-zA-Z]{24,34}",
            "(AC|SK)[0-9a-f]{32}",
            "AIza[0-9A-Za-z_-]{35}",
            "[0-9]+-[0-9A-Za-z_]{32}\\.apps\\.googleusercontent\\.com",
            "([gG][oO][oO][gG][lL][eE]).{0,20}[ '\\\"=:(\\[{]+.{0,5}[0-9a-zA-Z_-]{24}",
            "SG\\.[a-zA-Z0-9_-]{22}\\.[a-zA-Z0-9_-]{43}",
            "[0-9a-f]{32}-us[0-9]{1,2}",
            "key-[0-9a-zA-Z]{32}",
            "sq0(atp|csp)-[0-9A-Za-z_-]{22,43}",
            "EAAA[0-9a-zA-Z_-]{60}",
            "access_token\\$(live|production|sandbox)\\$[0-9a-z]{16}\\$[0-9a-f]{32}",
            "[^0-9a-zA-Z_-][AE][0-9a-zA-Z_-]{79}",
            "A21AA[0-9a-zA-Z_-]{92}",
            "([fF][aA][cC][eE][bB][oO][oO][kK]).{0,20}[ '\\\"=:(\\[{]+.{0,5}[0-9a-f]{32}",
            "EAACEdEose0cBA[0-9A-Za-z]+",
            "[0-9]{10,20}\\|[a-zA-Z0-9-]{20,30}",
            "([tT][wW][iI][tT][tT][eE][rR]).{0,20}[ '\\\"=:(\\[{]+.{0,5}[0-9a-zA-Z]{35,44}",
            "([tT][wW][iI][tT][tT][eE][rR]).{0,20}[ '\\\"=:(\\[{]+.{0,5}[1-9][0-9]+-[0-9a-zA-Z]{24,40}",
            "AAAAAAAAAAAAAAAAAAAAA[0-9A-Za-z%=\\+]+",
            "([gG][iI][tT][hH][uU][bB]).{0,20}[ '\\\"=:(\\[{]+.{0,5}[0-9a-zA-Z]{35,40}",
            "([hH][eE][rR][oO][kK][uU]).{0,20}[ '\\\"=:(\\[{]+.{0,5}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
            "[a-z\\+]{3,}:[/]{1,3}[^:'\\\" ]{2,}:[^@'\\\" ]{3,}@[^'\\\" ]+",
            "ya29\\.[0-9A-Za-z_-]+",
            "sk_live_[0-9a-z]{32}",
            "amzn\\.mws\\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            "[a-zA-Z0-9_-]+\\.(firebaseio|azurewebsites|cloudapp|trafficmanager|herokuapp|cloudfront)\\.(com|net)",
            "\\-\\-\\-\\-\\-BEGIN[ ]+[A-Z]*[ ]*PRIVATE[ ]+KEY",
            "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
            "ey[A-Za-z0-9_=-]+\\.ey[A-Za-z0-9_=-]+\\.?[A-Za-z0-9_.+/=-]*"
        ],
    },
}


# init
from modules.app import App

# run
app = App( config )
app.init()
app.run()


######### TODO

# quickhits
    # gf mykeys
    # gf noisy
    # gf takeovers
    # gf dlisting
    # gf ips local
    # gf emails
    # new subdomains

# bucket search (domain)
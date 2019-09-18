import sys
import subprocess
from colored import fg, bg, attr


def run( app ):
    sys.stdout.write( '[+] running mod: screenshots\n' )

    try:
        cmd = 'EyeWitness --headless -f "' + app.f_urls + '" --user-agent "Mozilla/5.0 (X11; Linux i586; rv:63.0) Gecko/20100101 Firefox/63.0" --no-prompt --threads 10 -d ' + app.d_output + '/eye'
        # print(cmd)
        subprocess.Popen( cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL )
    except Exception as e:
        sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )

# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import subprocess
from xml.etree import ElementTree as ET
from colored import fg, bg, attr


class Portscan:
    
    def run( self, app ):
        sys.stdout.write( '[+] running mod: portscan\n'  )

        d_output = app.d_output + os.path.dirname( app.config['portscan']['output_file'] )
        if not os.path.isdir(d_output):
            try:
                os.makedirs( d_output )
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                return
        
        cmd = eval( app.config['portscan']['command'] )
        os.system( cmd )


    def getReportDatas( self, app ):
        t_vars = {}
        t_portscan = {}
        f_output = app.d_output + app.config['portscan']['output_file']

        if os.path.isfile(f_output):
            doc = ET.parse( f_output ).getroot()
            t_hosts = doc.findall('host')
            
            for host in t_hosts:
                t_ips = host.findall('address')
                for ip in t_ips:
                    ip = ip.attrib['addr']
                    if not ip in t_portscan:
                        t_portscan[ip] = []
                t_ports = host.findall('ports/port')
                for port in t_ports:
                    # protocol = port.attrib['protocol']
                    port = int(port.attrib['portid'])
                    if not port in t_portscan[ip]:
                        t_portscan[ip].append( port )

            portscan_open = ''
            for ip in t_portscan.keys():
                portscan_open = portscan_open + ip + ' -> ' + ', '.join(map(str,sorted(t_portscan[ip]))) + "\n"

        else:
            portscan_open = '-'
        
        t_vars['portscan_open'] = portscan_open
        return t_vars


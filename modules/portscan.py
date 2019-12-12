# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import json
import subprocess
from xml.etree import ElementTree as ET
from colored import fg, bg, attr


class Portscan:
    max_ports_open = 10
    ips_hosts = {}
    f_ips_hosts = '/ips_hosts'

    def run( self, app ):
        sys.stdout.write( '[+] running mod: %s\n' % self.__class__.__name__.lower() )

        d_output = app.d_output + os.path.dirname( app.config['portscan']['output_file'] )
        if not os.path.isdir(d_output):
            try:
                os.makedirs( d_output )
            except Exception as e:
                sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                return

        cmd = eval( app.config['portscan']['command'] )
        sys.stdout.write( '%s[*] %s%s\n' % (fg('dark_gray'),cmd,attr(0)) )
        os.system( cmd )


    def getReportDatas( self, app ):
        t_vars = {}
        t_portscan = {}
        f_output = app.d_output + app.config['portscan']['output_file']

        if os.path.isfile(f_output):
            try:
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

            except Exception as e:
                # sys.stdout.write( "%s[-] error occurred: %s%s\n" % (fg('red'),e,attr(0)) )
                portscan_open = '-'

        t_urls = []
        portscan_open = ''

        f_ips_hosts = app.d_output + self.f_ips_hosts
        if os.path.isfile(f_ips_hosts):
            with open(f_ips_hosts) as json_file:
                self.ips_hosts = json.load( json_file )

        for ip in t_portscan.keys():
            if len(t_portscan[ip]) <= self.max_ports_open:
                portscan_open = portscan_open + ip + ' -> ' + ', '.join(map(str,sorted(t_portscan[ip]))) + "\n"
                for port in sorted(t_portscan[ip]):
                    if not port == 80:
                        t_urls.append( 'https://'+ip+':'+str(port) )
                    if not port == 443:
                        t_urls.append( 'http://'+ip+':'+str(port) )
                    if ip in self.ips_hosts:
                        for host in self.ips_hosts[ip]:
                            if not port == 80 and not port == 443:
                                t_urls.append( 'http://'+host+':'+str(port) )
                                t_urls.append( 'https://'+host+':'+str(port) )

        if len(t_urls):
            app.setUrlsIps( t_urls )

        t_vars['portscan_open'] = portscan_open
        return t_vars


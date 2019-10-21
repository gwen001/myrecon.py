# I don't believe in license.
# You can do whatever you want with this program.

import os
import sys
import imp
import subprocess
from colored import fg, bg, attr


class Report:

    def run( self, app ):
        sys.stdout.write( '[+] generating report...\n'  )

        tpl_vars = {}
        # tpl_vars = dict( tpl_vars.items() + app.getReportDatas().items() )
        tpl_vars.update( app.getReportDatas().items() )

        t_mods = app.config['mandatory_mods'] + app.config['optional_mods']

        for mod_name in t_mods:
            mod_name = mod_name.lower()
            # print(mod_name)
            mod_file = app.d_mods + '/' + mod_name + '.py'
            if not os.path.isfile(mod_file):
                sys.stdout.write( "%s[-] error occurred: %s not found%s\n" % (fg('red'),mod_name,attr(0)) )
            else:
                py_mod = imp.load_source( mod_name.capitalize(), mod_file)
                mod = getattr( py_mod, mod_name.capitalize() )()
                tpl_vars.update( mod.getReportDatas(app).items() )

        # print( tpl_vars )

        f_template = app.d_app + '/' + app.config['report_template']
        s_template = open(f_template,'r').read()

        for var_name,var_value in tpl_vars.items():
            var_name = '__' + var_name.upper() + '__'
            s_template = s_template.replace( var_name, str(var_value) )

        fp = open(app.f_report,'w')
        fp.write( s_template )
        fp.close()

        sys.stdout.write( "%s[+] report generated: %s%s\n" % (fg('green'),app.f_report,attr(0)) )


    def run2( self, app ):
        sys.stdout.write( '[+] generating report...\n'  )

        tpl_vars = {}
        # tpl_vars = dict( tpl_vars.items() + app.getReportDatas().items() )
        tpl_vars.update( app.getReportDatas().items() )

        t_mods = app.config['mandatory_mods'] + app.config['optional_mods']

        for mod_name in t_mods:
            mod_name = mod_name.lower()
            mod_file = app.d_mods + '/' + mod_name + '.py'
            if not os.path.isfile(mod_file):
                sys.stdout.write( "%s[-] error occurred: %s not found%s\n" % (fg('red'),mod_name,attr(0)) )
            else:
                py_mod = imp.load_source( mod_name.capitalize(), mod_file)
                mod = getattr( py_mod, mod_name.capitalize() )()
                tpl_vars.update( mod.getReportDatas(app).items() )

        # print( tpl_vars )

        f_template = app.d_app + '/' + app.config['report_template']
        s_template = open(f_template,'r').read()

        for var_name,var_value in tpl_vars.items():
            var_name = '__' + var_name.upper() + '__'
            s_template = s_template.replace( var_name, str(var_value) )

        fp = open(app.f_report,'w')
        fp.write( s_template )
        fp.close()

        sys.stdout.write( "%s[+] report generated: %s%s\n" % (fg('green'),app.f_report,attr(0)) )


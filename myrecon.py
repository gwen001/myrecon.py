#!/usr/bin/python3.5

# I don't believe in license.
# You can do whatever you want with this program.


config = {
    'available_mods': ['screenshot', 'quickhits', 'crlf', 'openredirect'],
    'mandatory_mods' : ['subdomains', 'resolve', 'urls']
}


# init
from modules.app import App

# run
app = App( config )
app.run()

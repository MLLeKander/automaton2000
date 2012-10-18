#!/usr/bin/env python2
import signal
import yaml
import os.path
import logging
import sys

import modules
import bot

# Load settings
## TODO: Change this to /etc/automaton2000
home = os.path.join( os.path.abspath(os.path.curdir), '..', 'home' )
configfile = os.path.join(home, "config.yml")
hconfigfile = open(configfile, 'r')
config = yaml.load(hconfigfile.read())
hconfigfile.close()

# Logger
if '-d' in sys.argv:
   level = logging.DEBUG
else:
   level = logging.INFO
logging.basicConfig(filename=(os.path.join(home, 'automaton2000.log')), level=level)

bots = [bot.IRCBot(s['host'], s['port'], s['channels'], s['nick'], s['modules'], s['trigger'], logging)
         for s in config['servers']]

def handleSigINT():
   # Instruct bots to shut down
   for bot in bots:
      bot.terminate()
signal.signal(signal.SIGINT, handleSigINT)

for bot in bots:
   bot.start()

bots[0].join()

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

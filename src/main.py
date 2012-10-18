#!/usr/bin/env python3
import signal
import yaml
import os.path
import logging
import sys

from daemon import Daemon
from bot import IRCBot

class Automaton2000(Daemon):
   def run(self):
      # Load settings
      #home = os.path.join( os.path.abspath(os.path.curdir), '..', 'home' )
      home = '/etc/automaton2000'
      configfile = os.path.join(home, "config.yml")
      hconfigfile = open(configfile, 'r')
      config = yaml.load(hconfigfile.read())
      hconfigfile.close()


      # Logger
      if 'debug' == config['loglevel']:
         level = logging.DEBUG
      else:
         level = logging.INFO
      logging.basicConfig(filename=('/var/log/automaton2000.log'), level=level)

      logging.debug("Starting set up")

      bots = [IRCBot(s['host'], s['port'], s['channels'], s['nick'], s['modules'], s['trigger'], logging)
               for s in config['servers']]


      #def handleSigINT(sig, frame):
         ## Instruct bots to shut down
         #for bot in bots:
            #bot.stop()
      #signal.signal(signal.SIGINT, handleSigINT)


      for bot in bots:
         bot.daemon = True
         bot.start()

      logging.debug("Set up complete. joining threads.")

      for bot in bots:
         bot.join()


if __name__ == "__main__":
   daemon = Automaton2000('/tmp/automaton2000.pid')
   if len(sys.argv) == 2:
      if 'start' == sys.argv[1]:
         daemon.start()
      if 'stop' == sys.argv[1]:
         daemon.stop()
      if 'restart' == sys.argv[1]:
         daemon.restart()
   else:
      print("usage: %s start|stop|restart" % sys.argv[0])
      sys.exit(2)


# vim:ts=3:sts=3:sw=3:tw=80:sta:et

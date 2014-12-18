#!/usr/bin/env python
import signal
import os.path
import sys
import pwd, grp
from os import execl
import logging
from logging.handlers import SysLogHandler
from time import sleep
import argparse

import yaml
from automaton2000.bot import IRCBot

#{{{ CLI Parsing
parser = argparse.ArgumentParser(description="Starcraft flavoured IRC Bot")
parser.add_argument('--configpath', '-c', default='/etc/automaton2000/config.yml',
      help='Specify the path to config.yml. Defaults to %(default)s', metavar='/path/to/file.yml')
parser.add_argument('--pidfile',    '-p', default='/tmp/automaton2000.pid',
      help='Specify a path to write our pidfile to. Defaults to %(default)s', metavar='/path/to/automaton.pid')
parser.add_argument('--debug',      '-d', action='store_true', default=False,
      help='Verbosity over 9000.')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 0.1')

args = parser.parse_args()
#}}}

#{{{ Logger
logger = logging.getLogger("automaton2000")
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
if not args.debug:
   slh = SysLogHandler('/dev/log', "daemon")
   slh.setFormatter(formatter)
   logger.addHandler(slh)
else:
   sh = logging.StreamHandler(sys.stderr)
   sh.setFormatter(formatter)
   logger.addHandler(sh)
#}}}

#{{{ Load main settings
try:
   configfile = os.path.abspath(args.configpath)
   hconfigfile = open(configfile, 'r')
   config = yaml.load(hconfigfile.read())
   hconfigfile.close()
except IOError:
   sys.stderr.write("Could not open config file at %s" % configfile)
   sys.exit(1)

if args.debug:
   level = 'debug'
else:
   level = config['loglevel']
level = level.upper()

logger.setLevel(level)
if not args.debug:
   slh.setLevel(level)
else:
   sh.setLevel(level)


bots = [IRCBot(s['host'], s['port'], s['channels'], s['nick'], s['modules'], s['trigger'])
         for s in config['servers']]

#}}}

#{{{ Daemonization
if not args.debug:
   try:
      pid = os.fork()
      if pid > 0:
         # exit first parent
         logger.debug('fork #1 worked!\n')
         sys.exit(0)

   except OSError as err:
      logger.debug('fork #1 failed: {0}\n'.format(err))
      sys.exit(1)

   # decouple from parent environment
   os.setsid()
   os.umask(0)

   if os.getuid() == 0 and config['user']:
      # Get uid and gid for the given names.
      try:
         (_,_,uid,_,_,_,_) = pwd.getpwnam(config['user'])
         (_,_,gid,_) = grp.getgrnam(config['group'])
      except KeyError:
         logger.critical("Invalid username/group. Daemon halting.")
         sys.exit(1)

      # Set gid first. After dropping root as uid, we can't change groups any more.
      os.setgid(gid)
      os.setuid(uid)
   os.chdir('/')

   # do second fork
   try:
      pid = os.fork()
      if pid > 0:
         # exit from second parent
         logger.debug('fork #2 worked!\n')
         sys.exit(0)
   except OSError as err:
      logger.debug('fork #2 failed: {0}\n'.format(err))
      sys.exit(1)

   # redirect standard file descriptors
   sys.stdout.flush()
   sys.stderr.flush()
   si = open(os.devnull, 'r')
   so = open(os.devnull, 'a+')
   se = open(os.devnull, 'a+')

   os.dup2(si.fileno(), sys.stdin.fileno())
   os.dup2(so.fileno(), sys.stdout.fileno())
   os.dup2(se.fileno(), sys.stderr.fileno())
#}}}

#{{{ PID file
if not args.debug:
   pidfilep = os.path.abspath(args.pidfile)
   try:
      pidfile = open(pidfilep, 'x')
   except FileExistsError:
      logger.critical("Pidfile %s already exists. Daemon already running?" % pidfilep)
      sys.exit(1)
   else:
      pid = str(os.getpid())
      pidfile.write(pid)
      pidfile.close()
#}}}

#{{{ Set up signal handling
logger.debug("Wiring up signals")
def handleUSR1(sig, frame):
   logger.info("Reloading all bot code!")
   for bot in bots:
      if bot.isAlive():
         bot.stop()

   logger.debug("Bots deactivated. Restarting main thread.")
   os.remove(pidfilep)
   sleep(1)
   # Absolute path!
   execl("automaton2000", "")

signal.signal(signal.SIGUSR1, handleUSR1)

def handleINT(sig, frame):
   for bot in bots:
      if bot.isAlive():
         bot.stop()

signal.signal(signal.SIGINT, handleINT)
signal.signal(signal.SIGQUIT, handleINT)
#}}}

#{{{ Main entry point
def run():
   logger.debug("Main entry point called")

   # And here's the main meat
   logger.debug("Set up complete. Starting botnet")
   for bot in bots:
      bot.daemon = True
      bot.start()


   logger.info("Botnet up and running")
   for bot in bots:
      while bot.isAlive():
         bot.join(timeout=0.1)


   if not args.debug:
      os.remove(pidfilep)
   logger.info("Master thread terminating.")

if __name__=="__main__":
   run()
#}}}

# vim:ts=3:sts=3:sw=3:tw=80:sta:et:fdm=marker

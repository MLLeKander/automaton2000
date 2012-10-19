#!/usr/bin/python3
import signal
import os.path
import sys
import pwd, grp
from os import execl
import logging
from logging.handlers import SysLogHandler
from time import sleep

import yaml
from automaton2000.bot import IRCBot

# Logger
logger = logging.getLogger("automaton2000")
slh = SysLogHandler('/dev/log', "daemon")
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
slh.setFormatter(formatter)
logger.addHandler(slh)

# Load settings
try:
   home = '/etc/automaton2000'
   configfile = os.path.join(home, "config.yml")
   hconfigfile = open(configfile, 'r')
   config = yaml.load(hconfigfile.read())
   hconfigfile.close()
except IOError:
   sys.stderr.write("Could not open config file at %s" % configfile)
   sys.exit(1)

if '-d' in sys.argv:
   level = 'debug'
else:
   level = config['loglevel']
level = level.upper()

logger.setLevel(level)
slh.setLevel(level)

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
   sys.stderr.write("Switched to uid %i and gid %i." % (uid, gid))
else:
   sys.stderr.write("We're not dropping privileges, and running as uid %i" % os.getuid())
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


# Try to create our pidfile. Quit if it exists.
pidfilep = '/var/run/automaton2000/automaton.pid'
try:
   pidfile = open(pidfilep, 'x')
except FileExistsError:
   logger.critical("Pidfile %s already exists. Daemon already running?" % pidfilep)
   sys.exit(1)
else:
   pid = str(os.getpid())
   pidfile.write(pid)
   pidfile.close()


# redirect standard file descriptors
sys.stdout.flush()
sys.stderr.flush()
#si = open(os.devnull, 'r')
#so = open(os.devnull, 'a+')
#se = open(os.devnull, 'a+')

#os.dup2(si.fileno(), sys.stdin.fileno())
#os.dup2(so.fileno(), sys.stdout.fileno())
#os.dup2(se.fileno(), sys.stderr.fileno())


logger.debug("Starting set up")


# Set up signal handling
def handleUSR1(sig, fram):
   logger.info("Reloading all bot code!")
   for bot in bots:
      if bot.isAlive():
         bot.stop()
         bot.join()

   os.remove(pidfilep)
   sleep(1)
   # Absolute path!
   execl("automaton2000", "")

signal.signal(signal.SIGUSR1, handleUSR1)

def handleINT(sig, frame):
   for bot in bots:
      bot.stop()

signal.signal(signal.SIGINT, handleINT)
signal.signal(signal.SIGTERM, handleINT)


def run():
   # And here's the main meat
   bots = [IRCBot(s['host'], s['port'], s['channels'], s['nick'], s['modules'], s['trigger'])
            for s in config['servers']]


   logger.info("Set up complete. Starting botnet")
   for bot in bots:
      bot.daemon = True
      bot.start()


   for bot in bots:
      bot.join()


   os.remove(pidfilep)
   logger.info("Master thread terminating.")

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

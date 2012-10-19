#!/usr/bin/python3
import signal
import os.path
from os import execl
import logging
from logging.handlers import SysLogHandler
import sys
from time import sleep

import yaml
from bot import IRCBot

# Logger
logger = logging.getLogger("automaton2000")
slh = SysLogHandler('/dev/log', "daemon")
formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
slh.setFormatter(formatter)
logger.addHandler(slh)

# Load settings
try:
   home = '/home/chris/dev/automaton2000/home'
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

pidfile = '/var/run/automaton2000/lock.pid'

try:
   with open(pidfile,'r') as pf:
      pid = int(pf.read().strip())

except IOError:
   pid = None

if pid:
   logger.critical("Pidfile %s already exists. Daemon already running?" % pidfile)
   sys.exit(1)

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
os.chdir('/') 
os.setsid() 

# Change our effective user, if we're root and have a target uid.
if os.getuid() == 0 and config['uid']:
   os.setgid(int(config['uid']))
   os.setuid(int(config['gid']))

# Fix the umask
os.umask(0) 

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


# write pidfile
pid = str(os.getpid())
with open(pidfile,'w+') as f:
   f.write(pid + '\n')


logger.debug("Starting set up")


# Set up signal handling
def handleUSR1(sig, fram):
   logger.info("Reloading all bot code!")
   for bot in bots:
      if bot.isAlive():
         bot.stop()
         bot.join()

   os.remove(pidfile)
   sleep(1)
   # Absolute path!
   execl("/home/chris/dev/automaton2000/src/automaton2000.py", "automaton2000")

signal.signal(signal.SIGUSR1, handleUSR1)

def handleINT(sig, frame):
   for bot in bots:
      bot.stop()

signal.signal(signal.SIGINT, handleINT)
signal.signal(signal.SIGTERM, handleINT)


# And here's the main meat
bots = [IRCBot(s['host'], s['port'], s['channels'], s['nick'], s['modules'], s['trigger'])
         for s in config['servers']]


logger.info("Set up complete. Starting botnet")
for bot in bots:
   bot.daemon = True
   bot.start()


for bot in bots:
   bot.join()


os.remove(pidfile)
logger.info("Master thread terminating.")

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

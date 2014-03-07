import re
import importlib
from imp import reload
import socket
import time
import threading
import logging
import automaton2000.modules

regex = ':(?P<nick>[^ ]*)!(?P<user>[^ ]*)@(?P<host>[^ ]*) ' + \
'PRIVMSG (?P<chan>[^ ]*) :{0}(?P<msg>.*)'

re_notrig = re.compile(regex.format(''))

class IRCBot(threading.Thread):
   def __init__(self, server, port, channels, nick, mods, trigger):
      threading.Thread.__init__(self)
      self.server = server
      self.port = port
      self.channels = channels
      self.nick = nick
      self.modules = [importlib.import_module("automaton2000.modules.%s" % m) for m in mods]
      #self.trigger = trigger
      self.logger = logging.getLogger("automaton2000")
      self.re_trig = re.compile(regex.format(re.escape(trigger)))
      self.terminate = threading.Event()
   
   def run(self):
      # Errant connection issues? Just reconnect!
      while not self.terminate.isSet():
         self.logger.debug("Connecting to %s:%i" % (self.server, self.port))
         self._con = socket.socket()
         self._con.connect((self.server, self.port))
         self._con.settimeout(1)
         self.send('USER %s %s %s %s' % (self.nick, self.nick, self.nick, self.nick))
         self.send('NICK %s' % (self.nick))
         for channel in self.channels:
            self.send('JOIN %s' % (channel))
      
         try:
            while not self.terminate.isSet():
               self.receive()

         finally:
            self.logger.debug("Bot quitting")
            self.send('QUIT :Automaton destroyed')
            self._con.close()
            self.logger.info("Socket closed for %s:%i." % (self.server, self.port))
   
   def receive(self):
      while not self.terminate.isSet():
         try:
            data = self._con.recv(1024)
         except socket.timeout:
            return None
         if not data:
            time.sleep(0.5)
            continue
         else:
            try:
               data = data.decode('utf-8')
            except UnicodeDecodeError:
               self.logger.debug("I didn't like that data... "+data)
               continue

            lines = data.split('\r\n')
            for line in lines:
               if line.strip() == '': continue
               self.logger.debug(self.server+" > "+line)
               match = self.match_privmsg(line)
               if match:
                  for module in self.modules:
                     try:
                        module.handle(line, self, match)
                     except Exception, e:
                        self.logger.exception(e)
   
   def match_privmsg(self, line, usetrigger=True):
      re = self.re_trig if usetrigger else re_notrig
      match = re.match(line)
      if not match:
         return None
      return [match.group(key) for key in ['nick','user','host','chan','msg']]
   
   def send(self, line):
      self.logger.debug(self.server+' < '+line.rstrip())
      self._con.send(bytes((line+'\r\n').encode('utf-8')))

   def sendchan(self, chan, line):
      self.send("PRIVMSG %s :%s\r\n" % (chan,line))
   
   def stop(self):
      self.logger.debug("Thread was requested to stop.")
      self.terminate.set()

   def reload(self):
      self.logger.info("Reloading all modules")
      [reload(m) for m in self.modules]

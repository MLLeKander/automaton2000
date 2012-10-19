import re
import importlib
from imp import reload
import socket
import time
import threading
import logging
import automaton2000.modules

regex = ':(?P<nick>[^ ]*)!~(?P<user>[^ ]*)@(?P<host>[^ ]*) ' + \
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
      self.trigger = trigger
      self.logger = logging.getLogger("automaton2000")
      self.re_trig = re.compile(regex.format(re.escape(self.trigger)))
      self.terminate = threading.Event()
      #TODO: Load module specific config
   
   
   def send(self, line):
      self.logger.debug(self.server+' < '+line.rstrip())
      self._con.send(bytes((line+'\r\n').encode('utf-8')))


   def receive(self):
      try:
         data = self._con.recv(1024)
      except socket.timeout:
         return None
      if data:
         data = data.decode('utf-8')
         return data
      else:
         return None
   
   
   def sendchan(self, chan, line):
      self.send("PRIVMSG %s :%s\r\n" % (chan,line))
   

   def match_privmsg(self, line, usetrigger=True):
      re = self.re_trig if usetrigger else re_notrig
      match = re.match(line)
      if not match:
         return [None]*5
      return [match.group(key) for key in ['nick','user','host','chan','msg']]
   
   
   def stop(self):
      self.logger.debug("Thread was requested to stop.")
      self.terminate.set()


   def reload(self):
      self.logger.info("Reloading all modules")
      [reload(m) for m in self.modules]
      #TODO: Reload module config
   
   
   def run(self):
      self._con = socket.socket()
      self._con.connect((self.server, self.port))
      self._con.settimeout(1)
      self.send('USER %s %s %s %s' % (self.nick, self.nick, self.nick, self.nick))
      self.send('NICK %s' % (self.nick))
      for channel in self.channels:
         self.send('JOIN %s' % (channel))
      
      try:
         while not self.terminate.isSet():
            data = self.receive()
            if not data:
               time.sleep(0.5)
               continue
            else:
               lines = data.split('\r\n')
               for line in lines:
                  if line.strip() == '': continue
                  self.logger.debug(self.server+" > "+line)
                  match = self.match_privmsg(line)
                  for module in self.modules:
                     if module.handle(line, self, match, self.logger):
                        break;
      
      finally:
         self.logger.debug("Bot quitting")
         self.send('QUIT :Automaton destroyed')
         self._con.close()
         self.logger.info("Socked closed. Thread terminating immediately.")

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

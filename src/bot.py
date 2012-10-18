import re
import importlib
import socket
import threading
import modules

regex = ':(?P<nick>[^ ]*)!~(?P<user>[^ ]*)@(?P<host>[^ ]*) ' + \
'PRIVMSG (?P<chan>[^ ]*) :{0}(?P<msg>.*)'

re_notrig = re.compile(regex.format(''))

class IRCBot(threading.Thread):
   def __init__(self, server, port, channels, nick, mods, trigger, logger):
      threading.Thread.__init__(self)
      self.server = server
      self.port = port
      self.channels = channels
      self.nick = nick
      self.modules = [importlib.import_module("modules.%s" % m) for m in mods]
      self.trigger = trigger
      self.logger = logger
      self.re_trig = re.compile(regex.format(re.escape(self.trigger)))
      self.terminate = threading.Event()
      #TODO: Load module specific config
   
   
   def send(self, line):
      self.logger.debug(self.server+' < '+line.rstrip())
      self._con.send(bytes((line+'\r\n').encode('utf-8')))
   
   
   def sendchan(self, chan, line):
      self.send("PRIVMSG %s :%s\r\n" % (chan,line))
   

   def match_privmsg(self, line, usetrigger=True):
      re = self.re_trig if usetrigger else re_notrig
      match = re.match(line)
      if not match:
         return [None]*5
      return [match.group(key) for key in ['nick','user','host','chan','msg']]
   
   
   def run(self):
      while not self.terminate.isSet():
         self.run_once()


   def terminate(self):
      self.terminate.set()


   def reload(self):
      [reload(m) for m in self.modules]
      #TODO: Reload module config
   
   
   def run_once(self):
      self._con = socket.socket()
      self._con.connect((self.server, self.port))
      
      self.send('USER %s %s %s %s' % (self.nick, self.nick, self.nick, self.nick))
      self.send('NICK %s' % (self.nick))
      for channel in self.channels:
         self.send('JOIN %s' % (channel))
      
      ircfile = self._con.makefile()

      for line in ircfile:
         line = line.rstrip('\r\n')
         self.logger.debug(self.server+" > "+line)
         match = self.match_privmsg(line)
         for module in self.modules:
            if module.handle(line, self, match, self.logger):
               break;
      
      ircfile.close()
      self._con.close()

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

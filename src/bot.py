import re
import socket
import threading

regex = ':(?P<nick>[^ ]*)!~(?P<user>[^ ]*)@(?P<host>[^ ]*) ' + \
'PRIVMSG (?P<chan>[^ ]*) :{0}(?P<msg>.*)'

re_notrig = re.compile(regex.format(''))

class IRCBot(threading.Thread):
   def __init__(self, server, port, channels, nick, modules, trigger):
      threading.Thread.__init__(self)
      self.server = server
      self.port = port
      self.channels = channels
      self.nick = nick
      self.modules = modules
      self.trigger = trigger
      self.re_trig = re.compile(regex.format(re.escape(self.trigger)))
   
   
   def send(self, line):
      print(self.server+' < '+line.rstrip())
      self._con.send(line+'\r\n')
   
   
   def sendchan(self, chan, line):
      self.send('PRIVMSG {0} :{1}\r\n'.format(chan,line))
   
   
#TODO: Perhaps move this to a utils file
   def match_privmsg(self, line, usetrigger=True):
      re = self.re_trig if usetrigger else re_notrig
      match = re.match(line)
      if not match:
         return [None]*5
      return [match.group(key) for key in ['nick','user','host','chan','msg']]
   
   
   def run(self):
      while True:
         self.run_once()
   
   
   def run_once(self):
      self._con = socket.socket()
      self._con.connect((self.server, self.port))
      
      self.send('USER {0} {0} {0} {0}'.format(self.nick))
      self.send('NICK {0}'.format(self.nick))
      for channel in self.channels:
         self.send('JOIN {0}'.format(channel))
      
      ircfile = self._con.makefile()

      for line in ircfile:
         line = line.rstrip('\r\n')
#TODO: Proper logging
         print(self.server+" > "+line)
         match = self.match_privmsg(line)
         for module in self.modules:
            if module.handle(line, self, match):
               break;
      
      ircfile.close()
      self._con.close()

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
      self.logger = logging.getLogger("automaton2000")
      self.logger.debug("%s: Loading modules." % self.server)
      self.modules = [importlib.import_module("automaton2000.modules.%s" % m) for m in mods]
      #self.trigger = trigger
      self.re_trig = re.compile(regex.format(re.escape(trigger)))
      self.terminate = threading.Event()

   def run(self):
      # Errant connection issues? Just reconnect!
      while not self.terminate.is_set():
         self.logger.info("Connecting to %s:%i" % (self.server, self.port))
         self._con = socket.socket()
         self._con.connect((self.server, self.port))
         self._con.settimeout(0.5)
         self.send('USER %s %s %s %s' % (self.nick, self.nick, self.nick, self.nick))
         self.send('NICK %s' % (self.nick))
         for channel in self.channels:
            self.send('JOIN %s' % (channel))

         try:
            self.receive()

         finally:
            self.logger.debug("%s: Shutting down" % self.server)
            self.send('QUIT :Automaton destroyed')
            self._con.close()
            self.logger.info("Socket closed for %s:%i." % (self.server, self.port))

   def receive(self):
      buffer = ""

      while not self.terminate.is_set():

         # Exhaust buffer before polling for more data
         if "\r\n" in buffer:
            try:
               # FIXME: I'd much rather just filter out any invalid bytes and try to make sense of the rest.
               (line, buffer) = buffer.split("\r\n", 1)
               line = line.decode('utf-8')

            except UnicodeDecodeError:
               self.logger.debug("%s: Line contained invalid unicode, ignoring: %s" % (self.server, line))
               continue

            self.logger.debug(self.server+" > "+line)

            # Pass the line around to our modules
            match = self.match_privmsg(line)
            for module in self.modules:
               try:
                  module.handle(line, self, match)
               except Exception, e:
                  self.logger.exception(e)

         # No data left in buffer, poll socket for more
         else:
            try:
               r = self._con.recv(4096)

               # Check to see if the socket is still alive
               if r == 0:
                  self.logger.debug("%s: Socket was closed externally." % self.server)
                  break
               else:
                  buffer += r

            except socket.timeout:
               pass

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

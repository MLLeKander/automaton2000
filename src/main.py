#!/usr/bin/env python2
import signal
import importlib
#from modules import *
import modules
import bot

server = 'irc.freenode.net'
port = 6667
nick = 'kaibot'
channels = ['##starcraft']
trigger = '!'

#TODO: Automatically generate this from modules/__init__.py ?
#FIXED: There you go
mods = [importlib.import_module("modules.%s" % m) for m in modules.__all__]

a2k = bot.IRCBot(server, port, channels, nick, mods, trigger)

def handleSigINT():
   print "fuck this shit"
   a2k.terminate()
signal.signal(signal.SIGINT, handleSigINT)

a2k.start()

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

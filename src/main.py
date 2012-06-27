#!/usr/bin/env python
from modules import *
import bot

server = 'irc.freenode.net'
port = 6667
nick = 'Automaton2000'
channels = ['#disregardplease']
trigger = '!'

#TODO: Automatically generate this from modules/__init__.py ?
modules = [
             pingModule,
             statsModule,
             ohaiModule,
          ]

#TODO: Currently requires Ctrl+\ to kill
bot.IRCBot(server, port, channels, nick, modules, trigger).start()

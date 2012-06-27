import random

def handle(line, irc, match):
   responses = [
      'I read ya... sir.',
      '{0}, you rang?',
      'What do you want, {0}?',
   ]

   nick,_,_,chan,msg = match
   usetrigger=True
   if not msg:
      usetrigger=False
      nick,_,_,chan,msg = irc.match_privmsg(line, usetrigger=False)
   if msg and msg.find(irc.nick) != -1 or usetrigger and msg.startswith('ohai'):
      irc.sendchan(chan, random.choice(responses).format(nick))

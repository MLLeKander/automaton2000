import random

def handle(line, irc, match, logger):
   responses = [
      'The fuck do you want... sir?',
      '{0}, you are such a noobcock!',
      'Stop talking to me like that, {0}!',
   ]

   nick,_,_,chan,msg = match
   usetrigger=True
   if not msg:
      usetrigger=False
      nick,_,_,chan,msg = irc.match_privmsg(line, usetrigger=False)
   if msg and msg.find(irc.nick) != -1 or usetrigger and msg.startswith('ohai'):
      irc.sendchan(chan, random.choice(responses).format(nick))

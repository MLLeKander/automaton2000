from random import choice

def handle(line, irc, match, logger):
   nick,_,_,chan,msg = match
   if not msg:
      return False

   args = msg.split()

   keys = ['hump']
   if not args[0] in keys:
      return False

   logger.info("Handling hump request: %s" % msg)

   sexual_options = [
         "has crazy ass, electric intercourse that is forbidden in 7 states with %s.",
         "would rather chop his manly wire off than have intercourse with %s, to be honest."
         ]

   if len(args)>1:
      irc.sendchan(chan, ("\x01ACTION " + choice(sexual_options) + "\x01") % " ".join(args[1:]))
   else:
      irc.sendchan(chan, "Who would you like me to have sexy time with, %s?" % nick)

   return True

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

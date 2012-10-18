def handle(line, irc, match, logger):
   nick,_,_,chan,msg = match
   if not msg:
      return False

   args = msg.split()

   keys = ['hump']
   if not args[0] in keys:
      return False


   try:
      irc.sendchan(chan, "/me has crazy ass, sweaty sex that is forbidden in 7 states with %s." % args[1])
   except IndexError:
      irc.sendchan(chan, "That's not gonna work, %s." % nick)


   return True

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

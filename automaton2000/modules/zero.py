def handle(line, irc, match, logger):
   nick,_,_,chan,msg = match
   if not msg:
      return False

   args = msg.split()

   keys = ['zero']
   if not args[0] in keys:
      return False

   irc.sendchan(chan, "Dividing by zero, buckle up...")
   
   1/0
   return True

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

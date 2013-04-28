def handle(line, irc, match, logger):
   nick,_,_,chan,msg = match
   if not msg:
      return False

   args = msg.split()

   keys = ['reload']
   if not args[0] in keys:
      return False

   if nick in ['OMGTallMonster','mkaito']:
      logger.info("Handling module reload request from %s." % nick)
      irc.reload()
   else:
      logger.info("Denying module reload request from %s" % nick)

   return True

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

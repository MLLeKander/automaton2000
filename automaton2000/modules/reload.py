def handle(line, bot, match):
   if not match:
      return False

   nick,_,_,chan,msg = match
   args = msg.split()

   keys = ['reload']
   if not args[0] in keys:
      return False

   if nick in ['OMGTallMonster','mkaito', "tuxdev"]:
      bot.logger.info("Handling module reload request from %s." % nick)
      bot.reload()
   else:
      bot.logger.info("Denying module reload request from %s" % nick)

   return True

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

def handle(line, bot, match):
   nick,_,_,chan,msg = match
   if not msg:
      return False

   args = msg.split()

   keys = ['quit', 'kill', 'harakiri', 'suicide', 'gofuckyourself']
   if not args[0] in keys:
      return False

   if nick in ["mkaito", "OMGTallMonster", "tuxdev", "tuxdev_"]:
      bot.stop()
   else:
      bot.sendchan(chan, "Who do you think you are, telling me what to do!?")

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

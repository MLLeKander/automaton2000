def handle(line, bot, match):
	if not match:
		return False

	nick,_,_,chan,msg = match

	args = msg.split()

	keys = ['quit', 'kill', 'harakiri', 'suicide', 'gofuckyourself']
	if not args[0] in keys:
		return False

	if nick in ["mkaito", "OMGTallMonster", "tuxdev", "tuxdev_"]:
		bot.stop()
	else:
		bot.sendchan(chan, "Who do you think you are, telling me what to do!?")


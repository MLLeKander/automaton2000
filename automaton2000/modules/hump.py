from random import choice

def handle(line, bot, match):
	if not match:
		return False

	nick,_,_,chan,msg = match

	args = msg.split()

	keys = ['hump']
	if not args[0] in keys:
		return False

	bot.logger.info("Handling hump request: %s" % msg)

	sexual_options = [
			"has crazy ass, electric intercourse that is forbidden in 7 states with %s.",
			"would rather chop his manly wire off than have intercourse with %s, to be honest."
			]

	if len(args)>1:
		if args[1] == "me":
			n = [nick]
		elif args[1] in ["you", "yourself"]:
			n = ["himself"]
		else:
			n = args[1:]

		bot.sendchan(chan, ("\x01ACTION " + choice(sexual_options) + "\x01") % " ".join(n))

	else:
		bot.sendchan(chan, "Who would you like me to have sexy time with, %s?" % nick)

	return True

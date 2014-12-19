import random

def handle(line, bot, match):
	if not match:
		return False

	responses = [
		'The fuck do you want... sir?',
		'{0}, you are such a noobcock!',
		'Stop talking to me like that, {0}!',
	]

	nick,_,_,chan,msg = match
	usetrigger=True
	if not msg:
		usetrigger=False
		nick,_,_,chan,msg = bot.match_privmsg(line, usetrigger=False)
	if msg and msg.find(bot.nick) != -1 or usetrigger and msg.startswith('ohai'):
		bot.sendchan(chan, random.choice(responses).format(nick))

def handle(line, bot, match):
    if not match:
        return False

    nick,_,_,chan,msg = match
    args = msg.split()

    keys = ['zero']
    if not args[0] in keys:
        return False

    bot.sendchan(chan, "Dividing by zero, buckle up...")

    1/0
    return True


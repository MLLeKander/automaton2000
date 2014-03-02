def handle(line, bot, match):
    if not line.startswith('PING'):
        return False
    bot.send('PONG '+line[5:]+'\n')
    return True

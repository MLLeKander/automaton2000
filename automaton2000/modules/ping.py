import socket
def handle(line, bot, match):
    hn = socket.gethostname()
    if not line.startswith('PING'):
       return False
    bot.send('PONG %s %s \n' % ( hn, line[6:] ))
    return True

def handle(line, con, match):
   if not line.startswith('PING'):
      return False
   con.send('PONG '+line[5:]+'\n')
   return True

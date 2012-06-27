def handle(line, irc, match):
   _,_,_,chan,msg = match
   keys = ['stats', 'stat']
   if not msg or not msg in keys:
      return False
   
   irc.sendchan(chan, 'Stats here.')
   return True

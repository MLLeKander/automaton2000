from automaton2000 import units

def handle(line, irc, match, logger):
   nick,_,_,chan,msg = match
   
   if not msg or not msg.startswith('htk'):
      return False

   logger.info("Handling htk request from %s: %s" % (nick, msg))
   
   args = msg.split()
   
   atk_up = armor_up = shield_up = 0
   
   counter = 1
   
   try:
      if args[counter].startswith('+'):
         atk_up = int(args[counter][1:])
         counter += 1
      
      attacker = units.get_unit(args[counter])
      if not attacker:
         raise ValueError
      
      counter += 1
      
      if args[counter].startswith('+'):
         if '/' in args[counter]:
            armor_up, shield_up = args[counter].split('/')
            armor_up = int(armor_up.replace('+','0'))
            shield_up = int(shield_up)
         else:
            armor_up = int(args[counter])
         counter += 1
      
      defender = units.get_unit(args[counter])
      if not defender:
         raise ValueError
      
      attack = attacker.can_attack(defender)
      if not attack:
         output = attacker.name+' cannot hit '+defender.name
      else:
         hits = units.htk(attacker, defender, atk_up, armor_up, shield_up)
         output = '%d %s hits for a %s to kill a %s (in %d seconds, with %d' \
                  ' overkill)' % (hits, attack.name, attacker.name, \
                  defender.name, (hits-1)*attack.cooldown, abs(defender.hp))
      
   except ValueError:
      output = nick+': Unknown argument: '+args[counter]
   except IndexError:
      output = nick+': Not enough arguments.'
   
   irc.sendchan(chan, output)
   return True

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

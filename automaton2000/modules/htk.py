from automaton2000 import units

def upgrade_to_str(armor, shield=0):
   if armor == 0 and shield == 0:
      return ""
   
   s = "+"+str(armor)
   if shield != 0:
      s += "/"+str(shield)
   
   return s+" "
   

def handle(line, bot, match):
   nick,_,_,chan,msg = match
   
   if not msg or not msg.startswith('htk'):
      return False

   bot.logger.info("Handling htk request from %s: %s" % (nick, msg))
   
   args = msg.split()
   
   atk_up = armor_up = shield_up = 0
   
   counter = 1
   
   try:
      if not msg.startswith('htkswap'):
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
         
         handle.attacker = attacker
         handle.defender = defender
         handle.atk_up = atk_up
         handle.armor_up = armor_up
         handle.shield_up = shield_up
      else:
         attacker = handle.defender
         defender = handle.attacker
         atk_up = handle.armor_up
         armor_up = handle.atk_up
         shield_up = handle.shield_up
      
      attack = attacker.can_attack(defender)
      if not attack:
         output = attacker.name+' cannot hit '+defender.name
      else:
         hits = units.htk(attacker, defender, atk_up, armor_up, shield_up)
         output = '%d %s hits for a %s%s to kill a %s%s (in %d seconds, with ' \
                  '%d overkill)' % (hits, attack.name, upgrade_to_str(atk_up), \
                  attacker.name, upgrade_to_str(armor_up, shield_up), \
                  defender.name, (hits-1)*attack.cooldown, abs(defender.hp))
      
   except ValueError:
      output = nick+': Unknown argument: '+args[counter]
   except IndexError:
      output = nick+': Not enough arguments.'
   
   bot.sendchan(chan, output)
   return True

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

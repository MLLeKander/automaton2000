# vim: set fileencoding=utf-8:
import units

def handle(line, irc, match):
   _,_,_,chan,msg = match
   if not msg:
      return False

   args = msg.split()

   keys = ['stats', 'stat', 'longstats', 'ls', 's']
   if not args[0] in keys:
      return False

   try:
      unit = units.get_unit(args[1])
   except IndexError:
      irc.sendchan(chan, "Please provide a unit name")
      return True

   if not unit:
      irc.sendchan(chan, "not found")
      #irc.sendchan(chan, "%s: Unknown entity: %s" % (nick, args[1]))
      return True

   else:
      if args[0] in ['longstats', 'ls']:
         # Description
         irc.sendchan(chan, unit.description)

         # Race
         irc.sendchan(chan, "Race: %s" % translate_race(unit.race))
          
         # Cost (minerals, gas, supply, build time)
         costs = []
         if unit.minerals > 0:
            costs.append("%i minerals" % unit.minerals)
         if unit.gas > 0:
            costs.append("%i gas" % unit.gas)
         if unit.supply > 0:
            costs.append("%i supply" % unit.supply)
         if unit.buildtime > 0:
            costs.append("%i seconds" % unit.buildtime)

         if len(costs) > 0:
            output = "Costs: " + (", ".join(costs))
            irc.sendchan(chan, output)

         # Combat
         irc.sendchan(chan, "Attributes: %s" % (", ".join(translate_attrs(unit.attrs))))
         if unit.race == "protoss":
            irc.sendchan(chan, ("HP: %i, %i (%i combined)" % (unit.max_hp, unit.max_shields, (unit.max_hp + unit.max_shields))))
         else:
            irc.sendchan(chan, ("HP: %i" % unit.max_hp))
         
         if unit.attacks:
            irc.sendchan(chan, "Attacks: ")
            for a in unit.attacks:
               irc.sendchan(chan, ("   %s" % a))
         
         # Liquipedia
         if unit.liquipedia:
            irc.sendchan(chan, "Find out more in Liquipedia: %s" % unit.liquipedia)

      else:
         output = ''
         if not unit.description and not unit.liquipedia:
            output = "Unit found, but no stats registered."
         if unit.description:
            output += description
         if unit.liquipedia:
            if unit.description:
               output =+ ' — '
            output += liquipedia
         irc.sendchan(chan, output)
      
      return True

def translate_attrs(attrs):
   translations = {
            "g": "Ground",
            "f": "Flying",
            "a": "Armored",
            "b": "Biological",
            "l": "Light",
            "v": "Massive",
            "m": "Mechanical",
            "p": "Psionic",
            "s": "Structure"
         }

   return [translations.get(k) for k in attrs]

def translate_race(race):
   translations = {
         "p": "Protoss",
         "t": "Terran",
         "z": "Zerg"
         }

   return translations.get(race)

# vim:ts=3:sts=3:sw=3:tw=80:sta:et

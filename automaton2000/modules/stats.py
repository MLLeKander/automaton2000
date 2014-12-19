from automaton2000 import units

def handle(line, bot, match):
    if not match:
        return False

    nick,_,_,chan,msg = match
    args = msg.split()

    keys = ['stats', 'stat', 'longstats', 'ls', 's']
    if not args[0] in keys:
        return False

    bot.logger.info("Handling stats request for %s: %s" % (nick, msg))

    try:
        unit = units.get_unit(args[1])
        bot.logger.info("User %s requested stats for %s" % (nick, args[1]))
    except IndexError:
        bot.sendchan(chan, "Please provide a unit name")
        return True

    if not unit:
        bot.sendchan(chan, "not found")
        #bot.sendchan(chan, "%s: Unknown entity: %s" % (nick, args[1]))
        return True

    else:
        bot.logger.info("User %s requested stats for %s" % (nick, unit.name))
        if args[0] in ['longstats', 'ls']:
            # Description
            bot.sendchan(chan, unit.description)

            # Race
            bot.sendchan(chan, "Race: %s" % translate_race(unit.race))

            # Cost (minerals, gas, supply, build time)
            costs = []
            if unit.minerals > 0:
                costs.append("%i minerals" % unit.minerals)
            if unit.gas > 0:
                costs.append("%i gas" % unit.gas)
            if unit.supply > 0:
                costs.append("%.1f supply" % unit.supply)
            if unit.buildtime > 0:
                costs.append("%i seconds" % unit.buildtime)

            if len(costs) > 0:
                output = "Costs: " + (", ".join(costs)) + "."
                bot.sendchan(chan, output)

            # Combat
            bot.sendchan(chan, "Attributes: %s" % (", ".join(translate_attrs(unit.attrs))))
            if unit.race == "p":
                bot.sendchan(chan, ("HP: %i, %i (%i combined)" % (unit.max_hp, unit.max_shields, (unit.max_hp + unit.max_shields))))
            else:
                bot.sendchan(chan, ("HP: %i" % unit.max_hp))

            if unit.attacks:
                bot.sendchan(chan, "Attacks: ")
                for a in unit.attacks:
                    bot.sendchan(chan, ("   %s" % a))

            # Liquipedia
            if unit.liquipedia:
                bot.sendchan(chan, "Find out more in Liquipedia: %s" % unit.liquipedia)

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
            bot.sendchan(chan, output)

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


# Automaton 2000

The IRC bot at use at `##starcraft@freenode.net`. The name is a reference to a rather [cute critter](http://wiki.teamliquid.net/starcraft2/Critters#Automaton_2000) found in Starcraft 2, a utility robot presumably made by the Terran, which harmlessly roams most space platform maps.

## Installation

Just run `setup.py install` as you normally would. If you happen to be running Arch Linux, a PKGBUILD is included. We currently use hardcoded paths for most things. Please see issue #2.

## Modules

Modules feature a `handle()` method which is invoked with data about the text match when a trigger is found. This method should return `True` when the command was correctly handled, and `False` if it decides it didn't want to handle it after all.

```python
def handle(line, irc, match, logger):
	nick,_,_,chan,msg = match

	if not msg or not msg.startswith('triggertext'):
		return False

	logger.info("Handling command request from %s." % nick)
	irc.sendchan(chan, "Some fancy text in response to our command")
```

We get a string representing the entire IRC line, a reference to the bot that called us, a match object containing the command text, and a reference to the bot logger, a configured logging object.

We make sure we're not trying to handle an empty line, and that our text starts with the required command string. If we return `False` here, the bot will continue to poke other modules until one returns True.

Use the `irc.sendchan(channel, text)` method to send text back to the channel. Logging is always a good idea, but try to keep it to one line per invocation unless something goes wrong.

If you want your module to handle more than one command trigger, for example to handle a short form, or to respond to different variants of the command in different ways, something like this should work:
    
```python
args = msg.split()

keys = ['stats', 'stat', 'longstats', 'ls', 's']
if not args[0] in keys:
	return False
```

We then find the used trigger in `args[0]` and the rest of the arguments in `args[1:]`. Parse them as you see fit.

### The `units` module

This module was written to help other modules perform queries on in-game units. Methods are provided to find units by name and perform a very simplistic one-way combat simmulation. This module is used by the htk and stats modules.

### Included modules

* **htk:** hits to kill between two units. Supports specifying upgrades in the form of `!htk +2 zergling +3 zealot`.
* **hump:** Random sexiness for the long days.
* **kill:** Instructs the bot to go jump out the window. No efforts are taken to restart the process.
* **ohai:** Respond to mentions with random text.
* **ping:** PING is implemented as a module to keep the core lean. This module is required for proper function.
* **reload:** Uses python's built-in code reload mechanics to reload all modules.
* **stats:** Print statistics about game units.

### TODO

Please see the issue tracker on [Github](https://github.com/mkaito/automaton2000/issues). Pull requests are welcome.

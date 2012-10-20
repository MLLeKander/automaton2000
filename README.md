# Automaton 2000

The IRC bot at use at `##starcraft@freenode.net`.

## Installation

Just run `setup.py install` as you normally would. If you happen to be running Arch Linux, a PKGBUILD is included.

## Modules

Modules feature a `handle()` method which is invoked with data about the text match when a trigger is found. This method should return `True` when the command was correctly handled, and `False` if it decides it didn't want to handle it after all.

### Included modules

* **htk:** hits to kill between two units. Supports specifying upgrades in the form of `!htk +2 zergling +3 zealot`.
* **hump:** Random sexiness for the long days.
* **kill:** Instructs the bot to go jump out the window. No efforts are taken to restart the process.
* **ohai:** Respond to mentions with random text.
* **ping:** PING is implemented as a module to keep the core lean. This module is required for proper function.
* **reload:** Uses python's built-in code reload mechanics to reload all modules.
* **stats:** Print statistics about game units.

### TODO

* Modules such as `kill` and `reload` would make good use of some authorization functionality, but it is currently not implemented.
* Move static data to yaml files.
* `stats` and `htk` share the same data structure with unit info. Once this info is moved to a yaml file, some means for data sharing among modules, and between the bot and it's modules, would be of interest.
* A permanent data storage back end for module data.

### Authors
* OMGTallMonster
* Chris "mkaito" Hoeppner <me[at]mkaito[dot]com>

#!/usr/bin/python
from setuptools import setup

setup(
		name = 'automaton2000',
		packages = ['automaton2000', 'automaton2000.modules'],
		data_files = [
			('/etc/automaton2000', ['home/config.yml']),
			],
		version='0.1',
		description='A simple, modular IRC bot',
		author='##starcraft@Freenode',
		install_requires=['pyyaml', 'distribute'],
		zip_safe = True,
		entry_points = {
				'console_scripts': [
						'automaton2000 = automaton2000.main:run'
				]
		}
)

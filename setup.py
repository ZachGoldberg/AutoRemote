#!/usr/bin/env python

from distutils.core import setup

setup(name='AutoRemote',
      version='0.1',
      description='AutoRemote Control Point',
      author='Zach Goldberg',
      author_email='zach@zachgoldberg.com',
      url='http://www.zachgoldberg.com/projects/zhaan/',
      packages=['autoremote', 'autoremote.controllers', 'autoremote.util', 'autoremote.physics', 'autoremote.triggers'],
     )

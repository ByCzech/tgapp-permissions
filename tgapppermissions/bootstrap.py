# -*- coding: utf-8 -*-
"""Setup the tgapppermissions application"""
from __future__ import print_function

from tgapppermissions import model
from tgext.pluggable import app_model

def bootstrap(command, conf, vars):
    print('Bootstrapping tgapppermissions...')

# -*- coding: utf-8 -*-
"""Setup the tgapppermissions application"""
from __future__ import print_function

from tgapppermissions import model
from tgext.pluggable import app_model

def bootstrap(command, conf, vars):
    print('Bootstrapping tgapppermissions...')
    p = app_model.Permission(permission_name='tgapppermissions',
                             description='Permits to manage permissions')
    try:
        model.DBSession.add(p)
    except AttributeError:
        # mute ming complaints
        pass
    model.DBSession.flush()
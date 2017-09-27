# -*- coding: utf-8 -*-
"""Setup the tgapppermissions application"""
import logging
from tgapppermissions import model
from tgext.pluggable import app_model

log = logging.getLogger(__name__)

def bootstrap(command, conf, vars):
    log.info("bootstrapping tgapppermissions")
    p = app_model.Permission(permission_name='tgapppermissions',
                             description='Permits to manage permissions')
    try:
        model.DBSession.add(p)
    except AttributeError:
        # mute ming complaints
        pass
    model.DBSession.flush()
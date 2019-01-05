# -*- coding: utf-8 -*-
"""Setup the tgapppermissions application"""
import logging
from tgapppermissions import model
from tgext.pluggable import app_model

log = logging.getLogger(__name__)

def bootstrap(command, conf, vars):
    log.info("bootstrapping tgapppermissions")
    p1 = app_model.Permission(permission_name='tgapppermissions-admin',
                              description='Permits to manage permissions')
    p2 = app_model.Permission(permission_name='tgapppermissions',
                              description='Permits to assign groups to a user')

    try:  # sqlalchemy
        g = model.DBSession.query(app_model.Group).filter_by(group_name='managers').first()
    except:  # ming
        g = app_model.Group.query.find(dict(group_name='managers')).first()
    
    if g:
        p1.groups = [g]
        p2.groups = [g]

    try:
        model.DBSession.add(p1)
        model.DBSession.add(p2)
    except AttributeError:
        # mute ming complaints
        pass
    model.DBSession.flush()

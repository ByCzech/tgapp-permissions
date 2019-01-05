# -*- coding: utf-8 -*-
"""The tgapp-permissions package"""

from tg.configuration import milestones


def plugme(app_config, options):
    from tgapppermissions import model
    milestones.config_ready.register(model.configure_models)
    if 'exclusive_permissions' not in options:
        options['exclusive_permissions'] = False

    try:
        app_config.update_blueprint({
            '_pluggable_tgapppermissions_config': options
        })
    except AttributeError:        
        app_config['_pluggable_tgapppermissions_config'] = options
    return dict(appid='tgapppermissions', global_helpers=False)

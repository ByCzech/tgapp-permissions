# -*- coding: utf-8 -*-
"""The tgapp-permissions package"""

from tg.configuration import milestones


def plugme(app_config, options):
    from tgapppermissions import model
    milestones.config_ready.register(model.configure_models)
    app_config['_pluggable_tgapppermissions_config'] = options
    return dict(appid='tgapppermissions', global_helpers=False)

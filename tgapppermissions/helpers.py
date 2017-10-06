# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-permissions."""
from tgext.pluggable import app_model
from tgapppermissions import model
import six


def get_primary_field(_model):
    return model.provider.get_primary_field(
        model.provider.get_entity(_model)
    )

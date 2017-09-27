# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-permissions."""
from tgext.pluggable import app_model
from tgapppermissions import model
import six


def get_primary_field(_model):
    if isinstance(_model, six.string_types):
        if _model == 'User':
            _model = app_model.User
        elif _model == 'Permission':
            _model = app_model.Permission
        elif _model == 'Group':
            _model = app_model.Group
        else:
            raise Exception('model string not recognized, give me the model class')
    return model.provider.get_primary_field(_model)

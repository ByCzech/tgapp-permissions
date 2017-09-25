# -*- coding: utf-8 -*-

from tg import config


def get_new_permission_form():
    new_permission_config = config['_pluggable_tgapppermissions_config']
    new_permission_form = new_permission_config.get('new_permission_form_instance')
    if not new_permission_form:
        form_path = new_permission_config.get('new_permission_form', 'tgapppermissions.lib.forms.NewPermission')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        new_permission_form = new_permission_config['new_permission_form_instance'] = form_class()

    return new_permission_form


def get_edit_permission_form():
    edit_permission_config = config['_pluggable_tgapppermissions_config']
    edit_permission_form = edit_permission_config.get('edit_permission_form_instance')
    if not edit_permission_form:
        form_path = edit_permission_config.get('edit_permission_form', 'tgapppermissions.lib.forms.EditPermission')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        edit_permission_form = edit_permission_config['edit_permission_form_instance'] = form_class()

    return edit_permission_form


def get_edit_user_form():
    edit_user_config = config['_pluggable_tgapppermissions_config']
    edit_user_form = edit_user_config.get('edit_user_form_instance')
    if not edit_user_form:
        form_path = edit_user_config.get('edit_user_form', 'tgapppermissions.lib.forms.EditUser')
        module, form_name = form_path.rsplit('.', 1)
        module = __import__(module, fromlist=form_name)
        form_class = getattr(module, form_name)
        edit_user_form = edit_user_config['edit_user_form_instance'] = form_class()

    return edit_user_form

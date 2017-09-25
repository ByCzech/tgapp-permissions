# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, predicates
from tg.decorators import paginate
from tg.i18n import ugettext as _

from tgapppermissions import model
from tgext.pluggable import app_model, plug_url, plug_redirect

from tgapppermissions.lib import get_new_permission_form, get_edit_permission_form, get_edit_user_form
from tgapppermissions.lib import forms

from bson import ObjectId

class RootController(TGController):
    allow_only = predicates.has_permission('tgapppermissions')

    @expose('tgapppermissions.templates.index')
    def index(self):
        permissions = model.provider.query(app_model.Permission)
        return dict(permissions_count=permissions[0],
                    permissions=permissions[1],
                    mount_point=self.mount_point,
                    )

    @expose('tgapppermissions.templates.new_permission')
    def new_permission(self, **kwargs):
        return dict(form=get_new_permission_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgapppermissions', '/create_permission'),
                    values=None,
                    )

    @expose()
    @validate(get_new_permission_form(), error_handler=new_permission)
    def create_permission(self, **kwargs):
        dictionary = {
            'permission_name': kwargs.get('permission_name'),
            'description': kwargs.get('description'),
            'groups': kwargs.get('groups'),
        }
        model.provider.create(app_model.Permission, dictionary)

        flash(_('Permission created.'))
        return redirect(url(self.mount_point))

    @expose('tgapppermissions.templates.edit_permission')
    def edit_permission(self, permission_id, **kwargs):
        __, permissions = model.provider.query(app_model.Permission,
                                               filters={'_id': permission_id})
        permission = permissions[0]
        return dict(form=get_edit_permission_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgapppermissions', '/update_permission/' + permission_id),
                    values=permission,
                    )

    @expose()
    @validate(get_edit_permission_form(), error_handler=edit_permission)
    def update_permission(self, permission_id, **kwargs):
        __, permissions = model.provider.query(app_model.Permission,
                                              filters={'_id': permission_id})
        permission = permissions[0]
        permission.permission_name = kwargs.get('permission_name')
        permission.description = kwargs.get('description')
        permission._groups = kwargs.get('groups')
        flash(_('Permission updated.'))
        return redirect(url(self.mount_point))

    @expose()
    def delete_permission(self, permission_id):
        model.provider.delete(app_model.Permission, dict(_id=permission_id))
        flash(_('Permission deleted'))
        return redirect(url(self.mount_point))

    @expose('tgapppermissions.templates.users')
    @paginate('users', items_per_page=20)
    def users(self, **kwargs):
        print(kwargs)
        if 'search_by' not in kwargs.keys():
            users = model.provider.query(app_model.User)
        else:
            users = model.provider.query(app_model.User,
                                         filters={kwargs.get('search_by'): kwargs.get('search_value')},
                                         substring_filters=[kwargs.get('search_by')],
                                         )
        return dict(mount_point=self.mount_point,
                    users_count=users[0],
                    users=users[1],
                    )

    @expose('tgapppermissions.templates.edit_user')
    def edit_user(self, user_id, **kwargs):
        __, users = model.provider.query(app_model.User,
                                         filters={'_id': user_id})
        user = users[0]
        return dict(form=get_edit_user_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgapppermissions', '/update_user/' + user_id),
                    values=user,
                    )

    @expose()
    @validate(validators={'groups': forms.EditUserValidator()})
    def update_user(self, user_id, **kwargs):
        __, users = model.provider.query(app_model.User,
                                         filters={'_id': user_id})
        user = users[0]
        user._groups = kwargs.get('groups')
        flash(_('User updated.'))
        return redirect(url(self.mount_point + '/users'))

# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController, abort
from tg import expose, flash, require, url, lurl, request, redirect, validate, predicates
from tg.decorators import paginate
from tg.i18n import ugettext as _

from tgapppermissions import model
from tgext.pluggable import app_model, plug_url

from tgapppermissions.lib import get_new_permission_form, get_edit_permission_form, get_edit_user_form
from tgapppermissions.helpers import get_primary_field


class RootController(TGController):
    allow_only = predicates.has_permission('tgapppermissions')

    @expose('tgapppermissions.templates.index')
    def index(self):
        count, permissions = model.provider.query(app_model.Permission)
        return dict(permissions_count=count,
                    permissions=permissions,
                    mount_point=self.mount_point)

    @expose('tgapppermissions.templates.new_permission')
    def new_permission(self, **_):
        return dict(form=get_new_permission_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgapppermissions', '/create_permission'),
                    values=None)

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
    def edit_permission(self, permission_id, **_):
        primary_field = get_primary_field('Permission')
        permission = model.provider.get_obj(app_model.Permission,
                                            {primary_field: permission_id}) or abort(404)
        values = model.provider.dictify(permission)
        values['groups'] = map(lambda x: str(x), permission['_groups'])
        return dict(form=get_edit_permission_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgapppermissions', '/update_permission/' + permission_id),
                    values=values)

    @expose()
    @validate(get_edit_permission_form(), error_handler=edit_permission)
    def update_permission(self, permission_id, **kwargs):
        primary_field = get_primary_field('Permission')
        model.provider.update(app_model.Permission,
                              {primary_field: permission_id,
                               'permission_name': kwargs.get('permission_name'),
                               'description': kwargs.get('description'),
                               'groups': kwargs.get('groups')})
        flash(_('Permission updated.'))
        return redirect(url(self.mount_point))

    @expose()
    def delete_permission(self, permission_id):
        primary_field = get_primary_field('Permission')
        try:
            model.provider.delete(app_model.Permission, {primary_field: permission_id})
        except AttributeError:
            abort(404)
        flash(_('Permission deleted'))
        return redirect(url(self.mount_point))

    @expose('tgapppermissions.templates.users')
    @paginate('users', items_per_page=20)
    def users(self, search_by=None, search_value=None):
        query_args = {}
        if search_by:
            query_args = dict(filters={search_by: search_value},
                              substring_filters=[search_by])
        _, users = model.provider.query(app_model.User, order_by='display_name', **query_args)
        return dict(mount_point=self.mount_point,
                    users=users)

    @expose('tgapppermissions.templates.edit_user')
    def edit_user(self, user_id, **_):
        primary_field = get_primary_field('User')
        user = model.provider.get(app_model.User, {primary_field: user_id}) or abort(404)
        return dict(
            form=get_edit_user_form(),
            mount_point=self.mount_point,
            action=plug_url('tgapppermissions', '/update_user/' + user_id),
            values=user,
        )

    @expose()
    @validate(get_edit_user_form(), error_handler=edit_user)
    def update_user(self, user_id, **kwargs):
        """currently updates ONLY the groups of the user"""
        primary_field = get_primary_field('User')
        model.provider.update(app_model.User,
                              {primary_field: user_id,
                               'groups': kwargs.get('groups')})
        flash(_('User updated.'))
        return redirect(url(self.mount_point + '/users'))

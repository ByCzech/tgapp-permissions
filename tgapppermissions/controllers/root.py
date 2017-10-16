# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController, abort
from tg import expose, flash, require, url, lurl, request, redirect, validate, predicates, config
from tg.decorators import paginate
from tg.i18n import ugettext as _

from tgapppermissions import model
from tgext.pluggable import app_model, plug_url

from tgapppermissions.lib import get_new_permission_form, get_edit_permission_form, get_edit_user_form
from tgapppermissions.helpers import get_primary_field, instance_primary_key


class RootController(TGController):
    @expose('tgapppermissions.templates.index')
    def index(self):
        if predicates.has_permission('tgapppermissions-admin'):
            count, permissions = model.provider.query(app_model.Permission)
            return dict(permissions_count=count,
                        permissions=permissions,
                        mount_point=self.mount_point)
        else:
            return redirect(url(self.mount_point + '/users'))

    @expose('tgapppermissions.templates.new_permission')
    @require(predicates.has_permission('tgapppermissions-admin'))
    def new_permission(self, **_):
        return dict(form=get_new_permission_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgapppermissions', '/create_permission'),
                    values=None)

    @expose()
    @require(predicates.has_permission('tgapppermissions-admin'))
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
    @require(predicates.has_permission('tgapppermissions-admin'))
    def edit_permission(self, permission_id, **_):
        primary_field = get_primary_field('Permission')
        permission = model.provider.get_obj(app_model.Permission,
                                            {primary_field: permission_id}) or abort(404)
        values = model.provider.dictify(permission)
        values['groups'] = [instance_primary_key(g, True) for g in values['groups']]
        return dict(form=get_edit_permission_form(),
                    mount_point=self.mount_point,
                    action=plug_url('tgapppermissions', '/update_permission/' + permission_id),
                    values=values)

    @expose()
    @require(predicates.has_permission('tgapppermissions-admin'))
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
    @require(predicates.has_permission('tgapppermissions-admin'))
    def delete_permission(self, permission_id):
        primary_field = get_primary_field('Permission')
        try:
            model.provider.delete(app_model.Permission, {primary_field: permission_id})
        except AttributeError:
            abort(404)
        flash(_('Permission deleted'))
        return redirect(url(self.mount_point))

    @expose('tgapppermissions.templates.users')
    @require(predicates.has_permission('tgapppermissions'))
    @paginate('users', items_per_page=20)
    def users(self, search_by=None, search_value=None):
        query_args = {}
        if search_by:
            query_args = dict(filters={search_by: search_value},
                              substring_filters=[search_by])
        _, users = model.provider.query(app_model.User, order_by='display_name', **query_args)
        return dict(mount_point=self.mount_point,
                    users=users,
                    search_by=search_by,
                    search_value=search_value)

    @expose()
    @require(predicates.has_permission('tgapppermissions'))
    def toggle_group(self, **kwargs):
        group_id = kwargs.get('group')
        user_id = kwargs.get('user')
        user = model.provider.get_obj(app_model.User,
                                      {get_primary_field('User'): user_id}) or abort(404)
        groups_list = [instance_primary_key(g, True) for g in user.groups]

        if group_id in groups_list:
            groups_list.remove(group_id)
            model.provider.update(app_model.User, {get_primary_field('User'): user_id,
                                                   'groups': groups_list})
        else:
            if config['_pluggable_tgapppermissions_config']['exclusive_permissions']:
                groups_list = [group_id]
            else:
                groups_list.append(group_id)
            model.provider.update(app_model.User, {get_primary_field('User'): user_id,
                                                   'groups': groups_list})
        return redirect(url(self.mount_point + '/users'))

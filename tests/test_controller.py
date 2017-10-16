import tg
from tgext.pluggable import app_model
from tgapppermissions import model
from .base import configure_app, create_app, flush_db_changes
import re
from webtest import AppError
from datetime import datetime
from tgapppermissions.helpers import get_primary_field


find_urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


class RegistrationControllerTests(object):
    def setup(self):
        self.app = create_app(self.app_config, False)

    def test_index(self):
        resp = self.app.get('/')
        assert 'HELLO' in resp.text

    def test_tgapppermissions_index(self):
        resp = self.app.get('/tgapppermissions', extra_environ={'REMOTE_USER': 'manager'})

        assert '/users' in resp.text, resp
        assert '/new_permission' in resp.text, resp

    def test_tgapppermissions_auth(self):
        try:
            self.app.get('/tgapppermissions')
        except AppError as e:
            assert '401' in str(e)

    def test_create_permission(self):
        g_primary = get_primary_field('Group')

        g = model.provider.create(app_model.Group,
                                  {'group_name': 'editors', 'dispaly_name': 'Editors'})
        g_primary_value = getattr(g, g_primary)
        flush_db_changes()

        self.app.get(
            '/tgapppermissions/create_permission',
             params={'permission_name': 'pname',
                     'description': 'descr',
                     'groups': [g_primary_value]},
             extra_environ={'REMOTE_USER': 'manager'},
             status=302,
             )
        count, perms = model.provider.query(app_model.Permission,
                                            filters=dict(permission_name='pname'))

        assert count == 1
        perm = perms[0]
        assert 'pname' == perm.permission_name, perm.permission_name
        assert 'descr' == perm.description, perm.description
        assert g_primary_value == getattr(perm.groups[0], g_primary), perm.groups[0]

    def test_update_permission(self):
        g_primary = get_primary_field('Group')
        p_primary = get_primary_field('Permission')

        g1 = model.provider.create(app_model.Group,
                                   {'group_name': 'editors', 'dispaly_name': 'Editors'})
        g1_primary_value = getattr(g1, g_primary)
        g2 = model.provider.create(app_model.Group,
                                   {'group_name': 'users', 'dispaly_name': 'Users'})
        g2_primary_value = getattr(g2, g_primary)
        flush_db_changes()

        self.app.get(
            '/tgapppermissions/create_permission',
             params={'permission_name': 'pname',
                     'description': 'descr',
                     'groups': []},
             extra_environ={'REMOTE_USER': 'manager'},
             status=302,
             )
        count, perms = model.provider.query(app_model.Permission,
                                            filters=dict(permission_name='pname'))

        assert count == 1
        perm = perms[0]

        self.app.get('/tgapppermissions/update_permission/' + str(getattr(perm, p_primary)),
                     params={'permission_name': 'view',
                             'description': 'perm to view things',
                             'groups': [g1_primary_value, g2_primary_value]},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        count, perms = model.provider.query(app_model.Permission,
                                            filters=dict(permission_name='view'))

        assert count == 1
        perm = perms[0]

        assert 'view' == perm.permission_name, perm.permission_name
        assert 'perm to view things' == perm.description, perm.description
        # assert perm.groups == [g1, g2], perm.groups
        _, groups = model.provider.query(app_model.Group)
        assert set(
            [getattr(g, g_primary) for g in perm.groups]
        ) == set(
            [getattr(g, g_primary) for g in groups]
        )

    def test_delete_permission(self):
        p_primary = get_primary_field('Permission')
        self.app.get(
            '/tgapppermissions/create_permission',
            params={'permission_name': 'pname',
                    'description': 'descr',
                    'groups': []},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        count, perms = model.provider.query(app_model.Permission)

        assert count == 1
        perm = perms[0]

        self.app.get('/tgapppermissions/delete_permission/' + str(getattr(perm, p_primary)),
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302)
        count, perms = model.provider.query(app_model.Permission)

        assert count == 0

    def test_new_permission_form(self):
        resp = self.app.get('/tgapppermissions/new_permission',
                            extra_environ={'REMOTE_USER': 'manager'})

        assert 'name="permission_name"' in resp.text, resp
        assert 'name="description"' in resp.text, resp
        assert 'name="groups"' in resp.text, resp
        assert '/create_permission' in resp.text, resp

    def test_edit_permission_form_without_perm_id(self):
        self.app.get('/tgapppermissions/edit_permission',
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=404)

    def test_edit_permission_form(self):
        p_primary = get_primary_field('Permission')
        self.app.get(
            '/tgapppermissions/create_permission',
            params={'permission_name': 'pname',
                    'description': 'descr',
                    'groups': []},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        count, perms = model.provider.query(app_model.Permission)

        assert count == 1
        perm = perms[0]

        resp = self.app.get('/tgapppermissions/edit_permission/' + str(getattr(perm, p_primary)),
                            extra_environ={'REMOTE_USER': 'manager'})

        assert 'name="permission_name"' in resp.text, resp
        assert 'name="description"' in resp.text, resp
        assert 'name="groups' in resp.text, resp
        assert '/update_permission' in resp.text, resp

    def test_users(self):
        g_primary = get_primary_field('Group')
        u_primary = get_primary_field('User')

        g1 = model.provider.create(app_model.Group,
                                   {'group_name': 'editors', 'display_name': 'Editors'})
        g1_primary_value = getattr(g1, g_primary)
        u1 = model.provider.create(app_model.User,
                                   {'user_name': 'alpha',
                                    'display_name': 'Alpha',
                                    'email_address': 'email@email.email',
                                    'created': datetime.utcnow(),
                                    'groups': [g1_primary_value]})
        u1_primary_value = getattr(u1, u_primary)
        flush_db_changes()

        resp = self.app.get('/tgapppermissions/users',
                            extra_environ={'REMOTE_USER': 'manager'})

        assert 'alpha' in resp.text, resp
        assert 'Alpha' in resp.text, resp
        assert 'email@email.email' in resp.text, resp

    def test_users_search(self):
        model.provider.create(app_model.User,
                              {'user_name': 'alpha',
                               'display_name': 'Alpha',
                               'email_address': 'email@email.email',
                               'created': datetime.utcnow()})
        model.provider.create(app_model.User,
                              {'user_name': 'ciao',
                               'display_name': 'Ciao',
                               'email_address': 'ciao@email.email',
                               'created': datetime.utcnow()})
        model.provider.create(app_model.User,
                              {'user_name': 'miao',
                               'display_name': 'Miao',
                               'email_address': 'miao@email.email',
                               'created': datetime.utcnow()})
        flush_db_changes()

        resp = self.app.get('/tgapppermissions/users/?search_by=user_name&search_value=iao',
                            extra_environ={'REMOTE_USER': 'manager'})

        assert 'Alpha' not in resp.text, resp
        assert 'Ciao' in resp.text, resp
        assert 'Miao' in resp.text, resp

    def test_toggle_group(self):
        g_primary = get_primary_field('Group')
        u_primary = get_primary_field('User')

        u1 = model.provider.create(app_model.User,
                                   {'user_name': 'alpha',
                                    'display_name': 'Alpha',
                                    'email_address': 'email@email.email',
                                    'created': datetime.utcnow()})
        u1_primary_value = getattr(u1, u_primary)
        g1 = model.provider.create(app_model.Group,
                                   {'group_name': 'editors', 'display_name': 'Editors'})
        g1_primary_value = getattr(g1, g_primary)
        flush_db_changes()

        resp = self.app.get('/tgapppermissions/toggle_group',
                            {'user': u1_primary_value,
                             'group': g1_primary_value},
                            extra_environ={'REMOTE_USER': 'manager'},
                            status=302,
                            )

        __, user = model.provider.query(app_model.User, filters=dict(user_name='alpha'))
        user = user[0]
        assert user.groups[0].group_name == 'editors', user.groups

    def test_toggle_group_exlusive(self):
        self.app_config['_pluggable_tgapppermissions_config']['exclusive_permissions'] = True
        g_primary = get_primary_field('Group')
        u_primary = get_primary_field('User')

        u1 = model.provider.create(app_model.User,
                                   {'user_name': 'alpha',
                                    'display_name': 'Alpha',
                                    'email_address': 'email@email.email',
                                    'created': datetime.utcnow()})
        u1_primary_value = getattr(u1, u_primary)
        g1 = model.provider.create(app_model.Group,
                                   {'group_name': 'editors', 'display_name': 'Editors'})
        g1_primary_value = getattr(g1, g_primary)

        g2 = model.provider.create(app_model.Group,
                                   {'group_name': 'contributors', 'display_name': 'Contributors'})
        g2_primary_value = getattr(g2, g_primary)

        flush_db_changes()

        resp = self.app.get('/tgapppermissions/toggle_group',
                            {'user': u1_primary_value,
                             'group': g1_primary_value},
                            extra_environ={'REMOTE_USER': 'manager'},
                            status=302,
                            )

        __, user = model.provider.query(app_model.User, filters=dict(user_name='alpha'))
        user = user[0]
        assert len(user.groups) == 1, user.groups
        assert user.groups[0].group_name == 'editors', user.groups

        resp = self.app.get('/tgapppermissions/toggle_group',
                           {'user': u1_primary_value,
                            'group': g2_primary_value},
                           extra_environ={'REMOTE_USER': 'manager'},
                           status=302,
                           )

        __, user = model.provider.query(app_model.User, filters=dict(user_name='alpha'))
        user = user[0]
        assert len(user.groups) == 1, user.groups
        assert user.groups[0].group_name == 'contributors', user.groups

class TestRegistrationControllerSQLA(RegistrationControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestRegistrationControllerMing(RegistrationControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')

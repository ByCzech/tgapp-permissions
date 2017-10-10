import bson
from webtest import TestApp
import transaction

from tg import AppConfig
from tg.configuration import milestones
from tg.configuration.auth import TGAuthMetadata
from tgext.pluggable import plug, app_model


class FakeAppPackage(object):
    __file__ = __file__
    __name__ = 'tests'

    class lib(object):
        class helpers(object):
            pass
        helpers = helpers()

        class app_globals(object):
            class Globals():
                pass
        app_globals = app_globals()

    class websetup(object):
        def bootstrap(*args, **kwargs):
            pass


class TestAuthMetadata(TGAuthMetadata):
    def authenticate(self, environ, identity):
        return 'user'

    def get_user(self, identity, userid):
        if userid:
            from tg.util import Bunch
            return Bunch(display_name='Fake Manager',
                         user_name='fake_manager',
                         email_address='fake@manager.it',
                         groups=[])

    def get_groups(self, identity, userid):
        if userid:
            return ['managers']
            # return Bunch(group_name='managers',
            #              display_name='Managers',
            #              permissions=[])
        return []

    def get_permissions(self, identity, userid):
        if userid:
            return ['tgapppermissions', 'tgapppermissions-admin']
        return []


def configure_app(using):
    # Simulate starting configuration process from scratch
    milestones._reset_all()

    app_cfg = AppConfig(minimal=True)
    app_cfg.renderers = ['kajiki']
    app_cfg.default_renderer = 'kajiki'
    app_cfg.use_dotted_templatenames = True
    app_cfg.package = FakeAppPackage()
    app_cfg.use_toscawidgets2 = True
    app_cfg.sa_auth.authmetadata = TestAuthMetadata()
    app_cfg['beaker.session.secret'] = app_cfg['session.secret'] = 'SECRET'
    app_cfg.auth_backend = 'ming'

    if using == 'sqlalchemy':
        from . import sqlamodel
        app_cfg.package.model = sqlamodel
        app_cfg.use_sqlalchemy = True
        app_cfg['sqlalchemy.url'] = 'sqlite://'
        app_cfg.use_transaction_manager = True
        app_cfg.SQLASession = app_cfg.package.model.DBSession
    elif using == 'ming':
        from . import mingmodel
        app_cfg.package.model = mingmodel
        app_cfg.use_ming = True
        app_cfg['ming.url'] = 'mim:///fakedb'
        app_cfg.MingSession = app_cfg.package.model.DBSession
    else:
        raise ValueError('Unsupported backend')

    app_cfg.model = app_cfg.package.model
    app_cfg.DBSession = app_cfg.package.model.DBSession

    plug(app_cfg, 'tgapppermissions', plug_bootstrap=True)
    return app_cfg


def create_app(app_config, auth=False):
    app = app_config.make_wsgi_app(skip_authentication=True)

    if auth:
        app = TestApp(app, extra_environ=dict(REMOTE_USER='user'))
    else:
        app = TestApp(app)

    app.get('/non_existing_url_force_app_config_update', status=404)

    if app_config.get('use_ming'):
        datastore = app_config.DBSession.bind
        try:
            # On MIM drop all data
            datastore.conn.drop_all()
        except TypeError:
            # On MongoDB drop database
            datastore.conn.drop_database(datastore.db)
    elif app_config.get('use_sqlalchemy'):
        engine = app_config.DBSession.bind
        model = app_config['package'].model
        model.metadata.drop_all(engine)
        model.metadata.create_all(engine)
    else:
        raise ValueError('Unsupported backend')

    return app


def flush_db_changes():
    app_model.DBSession.flush()
    transaction.commit()

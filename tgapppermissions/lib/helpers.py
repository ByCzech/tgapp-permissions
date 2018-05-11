from tgapppermissions import model
from tgext.pluggable import app_model, instance_primary_key


def query_groups():
    def _query_groups():  # default implementation
        _, groups = model.provider.query(app_model.Group)
        return [(instance_primary_key(group), group.display_name) for group in groups]

    from tg import config
    return config['_pluggable_tgapppermissions_config'].get('query_groups', _query_groups)()

from tgapppermissions import model
from tgext.pluggable import app_model, instance_primary_key


def query_groups():
    _, groups = model.provider.query(app_model.Group)
    return [(instance_primary_key(group), group.display_name) for group in groups]

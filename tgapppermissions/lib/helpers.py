from tgapppermissions import model
from tgext.pluggable import app_model

def query_groups():
    try:
        return [(group._id, group.display_name) for group in model.provider.query(app_model.Group)[1]]
    except Exception as e:
        print('EXCEPTION in query_group helper of tgapppermissions')
        print(e)
        return []

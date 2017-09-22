from tg import expose

@expose('tgapppermissions.templates.little_partial')
def something(name):
    return dict(name=name)
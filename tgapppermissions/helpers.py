# -*- coding: utf-8 -*-

"""WebHelpers used in tgapp-permissions."""

from tgext.pluggable import plug_url
from tgapppermissions.lib.helpers import query_groups
from tg import predicates

from tgapppermissions import model


def get_primary_field(_model):
    return model.provider.get_primary_field(
        model.provider.get_entity(_model)
    )


# waiting for a new version of tgext.pluggable
try:
    from tgext.pluggable.utils import instance_primary_key
except ImportError:  # when tgext.pluggable is not updated
    def instance_primary_key(instance, as_string=False):
        """Returns the value of the primary key of the instance"""
        from tgext.pluggable.utils import primary_key
        p = getattr(instance, primary_key(instance.__class__).name)
        return p if not as_string else str(p)

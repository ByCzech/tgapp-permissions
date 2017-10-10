from formencode.validators import UnicodeString
from tg.i18n import lazy_ugettext as l_
from tw2.forms.widgets import Form, TextField, TextArea, SubmitButton, MultipleSelectField
from tw2.core import Deferred
from axf.bootstrap import BootstrapFormLayout
from tgapppermissions.lib import helpers as h


class KajikiBootstrapFormLayout(BootstrapFormLayout):
    inline_engine_name = 'kajiki'


class NewPermission(Form):
    class child(KajikiBootstrapFormLayout):
        permission_name = TextField(label=l_('Permission Name'), css_class='form-control',
                         validator=UnicodeString(min=3))

        description = TextArea(label=l_('Permission Description'), rows=10, css_class='form-control',
                               validator=UnicodeString(min=3))

        groups = MultipleSelectField(label=l_('Permission Groups'), css_class="form-control",
                                     options=Deferred(h.query_groups))

    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Create'))


class EditPermission(NewPermission):
    submit = SubmitButton(css_class='btn btn-primary pull-right', value=l_('Edit'))

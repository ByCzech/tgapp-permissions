# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _

from tgapppermissions import model
from tgapppermissions.model import DBSession

class RootController(TGController):
    @expose('tgapppermissions.templates.index')
    def index(self):
        sample = DBSession.query(model.Sample).first()
        flash(_("Hello World!"))
        return dict(sample=sample)

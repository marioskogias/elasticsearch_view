# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2013 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
    invenio_demosite.views
    -------------------------------

    Demosite interface.
"""

from flask import render_template, current_app, abort, url_for, Blueprint, \
        request
from flask.helpers import send_from_directory
from werkzeug.utils import cached_property, import_string
#from flask.ext.login import current_user, login_required


from invenio.base.globals import cfg
from invenio.base.i18n import _
from flask.ext.breadcrumbs import (default_breadcrumb_root,
                                   register_breadcrumb,
                                   current_breadcrumbs)
from flask.ext.menu import register_menu

from flask import Blueprint
from invenio.ext.template.context_processor import \
    register_template_context_processor
from invenio.modules.formatter import format_record
from invenio.base.decorators import wash_arguments, templated

blueprint = Blueprint('es_search', __name__, url_prefix='/es',
                      template_folder='templates', static_folder='static')

default_breadcrumb_root(blueprint, '.es_search')

@blueprint.route('/')
@register_menu(blueprint, 'main.es_search', _('New Search'), order=99)
@register_breadcrumb(blueprint, '.', _('ES_search'))
@wash_arguments({'p': (unicode, ''),
    'of': (unicode, 'hb'),
    'so': (unicode, None),
    'rm': (unicode, None)})
def search(p, of, so, rm):
    query = request.args.get("p", "*")
    if not query:
        query = "*"
    facet_filters = []
    for ff in request.args.getlist("facet_filter"):
        facet_filters.append((ff.split(":")))
    res = current_app.extensions.get("elasticsearch").search(query,
            facet_filters=facet_filters)
    class DOC:
        results = res


    @register_template_context_processor
    def index_context():
        return dict(
            format_record=format_record
        )
    return render_template(
            'es_search/index.html', document=DOC,
                    breadcrumbs=current_breadcrumbs)

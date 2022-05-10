# -*- coding: utf-8 -*-
"""
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from flask import g, request
from sqlalchemy import func

from mr.api.app import api, auth
from mr.core.alias import *
import base64

@api.get('/default/Info')
@api.doc("""
Get default Info data.
""")
# @auth.required
def get_default_info():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.FiscalYearStartMonth , DO.SafetyBankBalance
        )

    #if 'OrgName' in filter_data:
    #    query = query.filter(DO.OrgName == (filter_data['OrgName']))

    info = query.filter(DO.DimOrganisationKey == 1).all();

    item = {}
    item['FiscalYearStartMonth'] = info[0][0]
    item['SafetyBankBalance'] = info[0][1]

    return item




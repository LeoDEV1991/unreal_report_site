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

@api.get('/summary/summary')
@api.doc("""
Get summary summary data.
""")
# @auth.required
def get_summary_summary():
    """TODO: Docstring for get_summary_summary.
    :returns: TODO

    """
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            ES.ExecutiveSummaryHTML
        )\
        .outerjoin(DO , ES.DimOrganisationKey == DO.DimOrganisationKey)

    if 'DimDateKey' in filter_data:
        query = query.filter(ES.DimDateKey.in_(filter_data['DimDateKey']))

    summary = query.all()

    resp = []
    for row in summary:
        item = {}
        item['data'] = row[0]
        resp.append(item)

    return resp


@api.get('/summary/setsummary')
@api.doc("""
set summary summary data.
""")
# @auth.required
def get_summary_setsummary():
    """TODO: Docstring for get_summary_summary.
    :returns: TODO

    """
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    _contents = ''
    if 'content' in request.args:
        _contents = (request.args.get('content'))

    query = g.s.query(ES.DimDateKey).filter(ES.DimDateKey == filter_data['DimDateKey'][0])
    result = query.all()

    if len(result) == 0:
        result = g.s.execute('select count(*) + 1 from "FactExecutiveSummary"')
        fnum = 0
        for r in result:
            fnum = (r[0])

        g.s.\
            execute('insert into "FactExecutiveSummary" ("FactExecutiveSummaryKey","DimCompanyKey","DimOrganisationKey","DimDateKey","ExecutiveSummaryHTML"'
                    ',"CreateDate","ModDate") values(' + str(fnum) + ',1,1,' + str(filter_data['DimDateKey'][0]) + ',\'' + _contents + '\' , NOW() , NOW())')
    else:
        g.s.\
            execute('update "FactExecutiveSummary" set "ExecutiveSummaryHTML" = '
                    '\'' + _contents + '\' , "ModDate" = NOW() where "DimDateKey" = ' + str(filter_data['DimDateKey'][0]))

        #query = g.s.\
        #    query(ES).filter(ES.DimDateKey == filter_data['DimDateKey'][0])

        #query.ExecutiveSummaryHTML = _contents
        #query.session.query(ES).update({'ExecutiveSummaryHTML': _contents})

    return [_contents]


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


@api.get('/kpi/summary')
@api.doc("""
Get kpi summary data.
""")
# @auth.required
def get_kpi_summary():
    """TODO: Docstring for get_kpi_summary.
    :returns: TODO

    """
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.DimDate,
            KPI.Category, KPI.Name, KPI.Description, KPI.Priority
            , KPI.DesiredOutcome, KPI.PercentageTolerance, KPI.DisplayFormat
            , KPI.Enable, RE.Target, RE.Result, DO.Upper, DO.Lower
        )\
        .outerjoin(DO, RE.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DD, RE.DimDateKey == DD.DimDateKey)\
        .outerjoin(DCC, RE.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(KPI, RE.DimKeyPerformanceIndicatorKey == KPI.DimKeyPerformanceIndicatorKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    summary = query.order_by(DD.DimDate).all()

    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['Date'] = row[2]
        item['Category'] = row[3]
        item['Name'] = row[4]
        item['Description'] = row[5]
        item['Priority'] = row[6]
        item['DesiredOutcome'] = row[7]
        item['PercentageTolerance'] = row[8]
        item['DisplayFormat'] = row[9]
        item['Enable'] = row[10]
        item['Target'] = row[11]
        item['Result'] = row[12]
        item['Upper'] = row[13]
        item['Lower'] = row[14]

        resp.append(item)

    return resp


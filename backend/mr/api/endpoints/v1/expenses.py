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


@api.get('/expenses/summary')
@api.doc("""
Get expenses summary data.
""")
# @auth.required
def get_expenses_summary():
    """TODO: Docstring for get_expenses_summary.
    :returns: TODO

    """
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth,
            func.sum(GL.ActualExpenses).label("ActualExpenses"),
            func.sum(GL.ForecastExpenses).label("ForecastExpenses")
        )\
        .outerjoin(DO , GL.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DD , GL.DimDateKey == DD.DimDateKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    summary = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth).all()

    result = {}
    result["byActual"] = []
    result["byType"] = []
    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Date'] = row[3]
        item['ActualExpenses'] = row[4]
        item['ForecastExpenses'] = row[5]

        resp.append(item)

    result["byActual"] = resp

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth,DCOA.AccountType,
            func.sum(GL.ActualExpenses).label("ActualExpenses"),
            func.sum(GL.ForecastExpenses).label("ForecastExpenses")
        )\
        .outerjoin(DD , GL.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO , GL.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DCOA , DCOA.DimChartOfAccountsKey == GL.DimChartOfAccountsKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    summary = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth , DCOA.AccountType).order_by(DD.FirstDayOfMonth, DCOA.AccountType).all()

    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Date'] = row[3]
        item['AccountType'] = row[4]
        item['ActualExpenses'] = row[5]
        item['ForecastExpenses'] = row[6]

        resp.append(item)

    result["byType"] = resp
    return result


@api.get('/expenses/detail')
@api.doc("""
Get expenses detail data.
""")
# @auth.required
def get_expenses_detail():
    """TODO: Docstring for get_expenses_detail.
    :returns: TODO

    """
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(DO.OrgName, DD.FY, DD.FirstDayOfMonth, DCOA.AccountNumber, DCOA.AccountName, DCOA.AccountType, DCOA.AccountSubType,
                GL.ActualExpenses, GL.ForecastExpenses
               )\
        .outerjoin(DD , GL.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO , GL.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DCOA, DCOA.DimChartOfAccountsKey == GL.DimChartOfAccountsKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    detail = query.order_by(DCOA.AccountSubType).all()

    resp = []
    for row in detail:
        item = {}
        item['OrgName'] = row[0]
        item['FY'] = row[1]
        item['Date'] = row[2]
        item['AccountNumber'] = row[3]
        item['AccountName'] = row[4]
        item['AccountType'] = row[5]
        item['AccountSubType'] = row[6]
        item['ActualExpenses'] = row[7]
        item['ForecastExpenses'] = row[8]
        resp.append(item)

    return resp

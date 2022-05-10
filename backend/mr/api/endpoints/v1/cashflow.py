# -*- coding: utf-8 -*-
"""
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from flask import g, request
from sqlalchemy import func , or_

from mr.api.app import api, auth
from mr.core.alias import *


@api.get('/cashflow/topdata')
@api.doc("""
Get cashflow data.
""")
# @auth.required
def get_cashflow_topdata():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth,DO.SafetyBankBalance,
            func.sum(GLC.ClosingBalance).label("CashBalance"),DO.FiscalYearStartMonth
        )\
        .outerjoin(COA , GLC.DimChartOfAccountsKey == COA.DimChartOfAccountsKey)\
        .outerjoin(DD , GLC.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO , GLC.DimOrganisationKey == DO.DimOrganisationKey)
    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query = query.filter(or_(COA.AccountNumber == '1000' , COA.AccountNumber == '1004' , COA.AccountNumber == '1001'))

    summary = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, DO.SafetyBankBalance, DO.FiscalYearStartMonth).all()

    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Date'] = row[3]
        item['SafetyBankBalance'] = row[4]
        item['CashBalance'] = row[5]
        item['firstMonth'] = row[6]
        resp.append(item)

    return resp

@api.get('/cashflow/middledata')
@api.doc("""
Get cashflow middledata.
""")
# @auth.required
def get_cashflow_middledata():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth,COA.CashFlowCategory
            ,COA.CashFlowGroup ,  (func.sum(GLC.ChangeDuringPeriod) * -1).label('CashChange'),
            func.sum(GLC.ForecastChangeDuringPeriod).label("ForecastCashChange")
        )\
        .outerjoin(COA, GLC.DimChartOfAccountsKey == COA.DimChartOfAccountsKey)\
        .outerjoin(DD, GLC.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLC.DimOrganisationKey == DO.DimOrganisationKey)
    if 'DimDateKey' in filter_data:
        query = query.filter(DD.DK.in_(filter_data['DimDateKey']))

    query = query.filter(COA.CashFlowGroup != 'NULL')

    summary = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, COA.CashFlowCategory, COA.CashFlowGroup).all()

    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Date'] = row[3]
        item['CashFlowCategory'] = row[4]
        item['CashFlowGroup'] = row[5]
        item['CashChange'] = row[6]
        item['ForecastCashChange'] = row[7]
        resp.append(item)

    return resp

@api.get('/cashflow/bottomdata')
@api.doc("""
Get cashflow bottomdata.
""")
# @auth.required
def get_cashflow_bottomdata():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, DO.SafetyBankBalance,
            func.sum(GLC.ChangeDuringPeriod).label("CashBalance")
        )\
        .outerjoin(COA , GLC.DimChartOfAccountsKey == COA.DimChartOfAccountsKey)\
        .outerjoin(DD , GLC.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO , GLC.DimOrganisationKey == DO.DimOrganisationKey)
    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query = query.filter(or_(COA.AccountNumber == '1000', COA.AccountNumber == '1004' ,COA.AccountNumber == '1001'))

    summary = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, DO.SafetyBankBalance).all()

    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Date'] = row[3]
        item['SafetyBankBalance'] = row[4]
        item['CashBalance'] = row[5]
        resp.append(item)

    return resp

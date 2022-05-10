# -*- coding: utf-8 -*-
"""
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from flask import g, request
from sqlalchemy import func, or_, case

from mr.api.app import api, auth
from mr.core.alias import *


@api.get('/projectedcashflow/topdata')
@api.doc("""
Get projectedcashflow data.
""")
# @auth.required
def get_projectedcashflow_topdata():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    DateKey = filter_data['DateKey'][0]
    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, DO.SafetyBankBalance,
            func.sum(case([[DD.DimDateKey <= DateKey, GLC.ClosingBalance], [DD.DimDateKey > DateKey, GLC.ForecastChangeDuringPeriod], ])).label("CashBalance"),
        )\
        .outerjoin(COA, GLC.DimChartOfAccountsKey == COA.DimChartOfAccountsKey)\
        .outerjoin(DD, GLC.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLC.DimOrganisationKey == DO.DimOrganisationKey)
    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query = query.filter(COA.AccountSubType == 'Cash at Bank')
    #query = query.filter(or_(COA.AccountNumber == '1000' , COA.AccountNumber == '1004' , COA.AccountNumber == '1001'))

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

@api.get('/projectedcashflow/middledata')
@api.doc("""
Get projectedcashflow middledata.
""")
# @auth.required
def get_projectedcashflow_middledata():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    DateKey = filter_data['DateKey'][0]

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, COA.CashFlowCategory
            , COA.CashFlowGroup
            , func.sum(case([[DD.DimDateKey <= DateKey, GLC.ChangeDuringPeriod * -1], [DD.DimDateKey > DateKey, GLC.ForecastChangeDuringPeriod], ])).label("CashChange")
        )\
        .outerjoin(COA, GLC.DimChartOfAccountsKey == COA.DimChartOfAccountsKey)\
        .outerjoin(DD, GLC.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLC.DimOrganisationKey == DO.DimOrganisationKey)
    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query = query.filter(COA.CashFlowGroup != 'NULL')

    summary = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, COA.CashFlowCategory, COA.CashFlowGroup).order_by(DD.FirstDayOfMonth).all()

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
        resp.append(item)

    return resp

@api.get('/projectedcashflow/bottomdata')
@api.doc("""
Get projectedcashflow bottomdata.
""")
# @auth.required
def get_projectedcashflow_bottomdata():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, COA.AccountName,
            func.sum(GLD.DistributionAmount).label("DistributionAmount")
        )\
        .outerjoin(COA, GLD.DimChartOfAccountsKey == COA.DimChartOfAccountsKey)\
        .outerjoin(DD, GLD.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLD.DimOrganisationKey == DO.DimOrganisationKey)
    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query = query.filter(GLD.DistributionAmount > 0)

    summary = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, COA.AccountName).all()

    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Date'] = row[3]
        item['AccountName'] = row[4]
        item['DistributionAmount'] = row[5]
        resp.append(item)

    return resp

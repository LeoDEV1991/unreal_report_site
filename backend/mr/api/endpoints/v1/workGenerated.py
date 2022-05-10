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


@api.get('/workgenerated/query')
@api.doc("""
Get workgenerated summary data.
""")
# @auth.required
def get_workgenerated_query():
    """TODO: Docstring for get_fees_summary.
    :returns: TODO

    """
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth,WG.ExistingOrNew,
            func.sum(WG.WorkGeneratedAmount).label("WorkGeneratedAdmount")
        )\
        .join(DO, WG.DimOrganisationKey == DO.DimOrganisationKey)\
        .join(DD, WG.DimDateKey == DD.DimDateKey)\
        .join(DC, WG.DimCompanyKey == DC.DimCompanyKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query_res = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth, WG.ExistingOrNew).order_by(DD.FirstDayOfMonth).all()

    result = {}
    topresp = []

    for row in query_res:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Date'] = row[3]
        item['ExistingOrNew'] = row[4]
        item['WorkGeneratedAdmount'] = row[5]
        topresp.append(item)

    result['Top'] = topresp

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth,
            DPT.ProjectTypeDescription, DED.EmployeeName, WG.ExistingOrNew,
            func.sum(WG.WorkGeneratedAmount).label("WorkGeneratedAdmount")
        )\
        .join(DO, WG.DimOrganisationKey == DO.DimOrganisationKey)\
        .join(DD, WG.DimDateKey == DD.DimDateKey)\
        .join(DC, WG.DimCompanyKey == DC.DimCompanyKey)\
        .join(DPT, WG.DimProjectTypeKey == DPT.DimProjectTypeKey)\
        .join(DED, WG.DimEmployeeProjectSourceOneKey == DED.DimEmployeeKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query_res = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.FirstDayOfMonth,
                               DPT.ProjectTypeDescription, DED.DimEmployeeKey, WG.ExistingOrNew, DED.EmployeeName).order_by(DD.FirstDayOfMonth).all()

    midlresp = []

    for row in query_res:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Date'] = row[3]
        item['ProjectTypeDescription'] = row[4]
        item['EmployeeName'] = row[5]
        item['ExistingOrNew'] = row[6]
        item['WorkGeneratedAdmount'] = row[7]
        midlresp.append(item)

    result['MiddleLeft'] = midlresp

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, WG.ExistingOrNew,
            func.sum(WG.WorkGeneratedAmount).label("WorkGeneratedAdmount")
        )\
        .join(DO, WG.DimOrganisationKey == DO.DimOrganisationKey)\
        .join(DD, WG.DimDateKey == DD.DimDateKey)\
        .join(DC, WG.DimCompanyKey == DC.DimCompanyKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query_res = query.group_by(DO.OrgId, DO.OrgName, DD.FY, WG.ExistingOrNew).all()

    midrresp = []

    for row in query_res:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['ExistingOrNew'] = row[3]
        item['WorkGeneratedAdmount'] = row[4]
        midrresp.append(item)

    result['MiddleRight'] = midrresp

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY, DP.ProjectId, DP.ProjectName,
            DED.EmployeeInitials,
            DPT.ProjectTypeDescription, WG.ExistingOrNew,
            func.sum(WG.WorkGeneratedAmount).label("WorkGeneratedAdmount"),
            DD.FirstDayOfMonth, DED.EmployeeName
        )\
        .join(DO, WG.DimOrganisationKey == DO.DimOrganisationKey)\
        .join(DD, WG.DimDateKey == DD.DimDateKey)\
        .join(DC, WG.DimCompanyKey == DC.DimCompanyKey)\
        .join(DPT, WG.DimProjectTypeKey == DPT.DimProjectTypeKey)\
        .join(DP, WG.DimProjectKey == DP.DimProjectKey)\
        .join(DED, WG.DimEmployeeProjectSourceOneKey == DED.DimEmployeeKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query_res = query.group_by(DO.OrgId, DO.OrgName, DD.FirstDayOfMonth, DD.FY, DP.ProjectId, DED.EmployeeName,
                               DP.ProjectName, DED.EmployeeInitials, DPT.ProjectTypeDescription, WG.ExistingOrNew).all()

    bottomresp = []

    for row in query_res:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['ProjectId'] = row[3]
        item['ProjectName'] = row[4]
        item['EmployeeInitials'] = row[5]
        item['ProjectTypeDescription'] = row[6]
        item['ExistingOrNew'] = row[7]
        item['WorkGeneratedAdmount'] = row[8]
        item['Date'] = row[9]
        item['EmployeeName'] = row[10]

        bottomresp.append(item)

    result['Bottom'] = bottomresp

    return result


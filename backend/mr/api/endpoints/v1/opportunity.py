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


@api.get('/opportunity/summary')
@api.doc("""
Get opportunity summary data.
""")
# @auth.required
def get_opportunity_summary():
    """TODO: Docstring for get_opportunity_summary.
    :returns: TODO

    """
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DCC.CompanyCode, DO.OrgId, DO.OrgName, DD.FY,
            DD.DimDate, OPP.Status, func.min(OH.TotalHours)
        )\
        .outerjoin(OPP, OH.DimOpportunityKey == OPP.DimOpportunityKey)\
        .outerjoin(DCC, OH.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(DO, OH.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DD, OH.DimDateKey == DD.DimDateKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    summary = query.group_by(DCC.CompanyCode, DO.OrgId, DO.OrgName, DD.FY, DD.DimDate, OPP.Status).all()
    summary_result = {}
    summary_result['Left'] = []
    summary_result['Right'] = []

    for row in summary:
        item = {}
        item['CompanyCode'] = row[0]
        item['OrgId'] = row[1]
        item['OrgName'] = row[2]
        item['FY'] = row[3]
        item['Date'] = row[4]
        item['Status'] = row[5]
        item['Hours'] = row[6]
        summary_result['Left'].append(item)

    query = g.s\
        .query(
            DCC.CompanyCode, DO.OrgId, DO.OrgName, DD.FY,
            OPP.ProbabilityOfSuccess, func.min(OPP.PotentialRevenue), DD.DimDate
        )\
        .outerjoin(OH, OH.DimOpportunityKey == OPP.DimOpportunityKey)\
        .outerjoin(DCC, OH.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(DO, OH.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DD, OH.DimDateKey == DD.DimDateKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    rsummary = query.group_by(DCC.CompanyCode, DO.OrgId, DO.OrgName, DD.FY, OPP.ProbabilityOfSuccess, DD.DimDateKey).order_by(DD.DimDateKey).all()
    for row in rsummary:
        item = {}
        item['CompanyCode'] = row[0]
        item['OrgId'] = row[1]
        item['OrgName'] = row[2]
        item['FY'] = row[3]
        item['ProbabilityOfSuccess'] = row[4]
        item['PotentialRevenue'] = row[5]
        item['Date'] = row[6]
        summary_result['Right'].append(item)

    return summary_result

@api.get('/opportunity/detail')
@api.doc("""
Get opportunity detail data.
""")
# @auth.required
def get_opportunity_detail():
    """TODO: Docstring for get_opportunity_summary.
    :returns: TODO

    """
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DCC.CompanyCode, DO.OrgId, DO.OrgName, DD.FY,
            DD.DimDate, OPP.OpportunityType, OPP.OpportunityId, OPP.Name, OPP.Status,
            OPP.ProbabilityOfSuccess, func.sum(OH.TotalHours)
        )\
        .outerjoin(OPP, OH.DimOpportunityKey == OPP.DimOpportunityKey)\
        .outerjoin(DCC, OH.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(DO, OH.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DD, OH.DimDateKey == DD.DimDateKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    detail = query.group_by(DCC.CompanyCode, DO.OrgId, DO.OrgName,
                            DD.FY, DD.DimDate, OPP.OpportunityType, OPP.OpportunityId, OPP.Name, OPP.Status, OPP.ProbabilityOfSuccess).all()
    detail_result = {}
    detail_result['Left'] = []
    detail_result['Right'] = []

    for row in detail:
        item = {}
        item['CompanyCode'] = row[0]
        item['OrgId'] = row[1]
        item['OrgName'] = row[2]
        item['FY'] = row[3]
        item['Date'] = row[4]
        item['OpportunityType'] = row[5]
        item['OpportunityID'] = row[6]
        item['Name'] = row[7]
        item['Status'] = row[8]
        item['ProbabilityOfSuccess'] = row[9]
        item['Hours'] = row[10]

        detail_result['Left'].append(item)

    query = g.s\
        .query(
            DCC.CompanyCode, DO.OrgId, DO.OrgName, OPP.OpportunityType,
            OPP.OpportunityId, OPP.Name, OPP.Status,  func.min(OPP.WeightedPotentialRevenue),
            OPP.ProbabilityOfSuccess, DED.EmployeeName.label("Director")
        )\
        .outerjoin(OH, OH.DimOpportunityKey == OPP.DimOpportunityKey)\
        .outerjoin(DCC, OH.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(DO, OH.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DD, OH.DimDateKey == DD.DimDateKey)\
        .outerjoin(DED, DED.DimEmployeeKey == OH.DimEmployeeDirectoryKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    rsummary = query.group_by(DCC.CompanyCode, DO.OrgId, DO.OrgName, OPP.OpportunityType, OPP.OpportunityId, OPP.Name, OPP.Status,
                              OPP.ProbabilityOfSuccess, DED.EmployeeName).all()
    for row in rsummary:
        item = {}
        item['CompanyCode'] = row[0]
        item['OrgId'] = row[1]
        item['OrgName'] = row[2]
        item['OpportunityType'] = row[3]
        item['OpportunityId'] = row[4]
        item['Name'] = row[5]
        item['Status'] = row[6]
        item['Revenue'] = row[7]
        item['ProbabilityOfSuccess'] = row[8]
        item['Director'] = row[9]
        detail_result['Right'].append(item)

    return detail_result

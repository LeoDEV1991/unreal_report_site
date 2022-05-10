# -*- coding: utf-8 -*-
"""
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from flask import g, request
from sqlalchemy import func
from sqlalchemy import case
from mr.api.app import api, auth
from mr.core.alias import *


@api.get('/people/summary')
@api.doc("""
    /people/summary
""")
# @auth.required
def get_people_summary():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgName
            , DD.FY
            , DD.DimDate
            , FEF.ActualFees
            , FEF.ForecastFees
            , FEF.ActualFullTimeEmployees
            , FEF.ForecastRequiredFullTimeEmployees
            , FEF.WorkDaysInPeriod
         )\
        .outerjoin(DCC, FEF.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(DO, FEF.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DD, FEF.DimDateKey == DD.DimDateKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    query_result = query.all()
    sum_result = []

    for row in query_result:
        item = {}
        item["OrgName"] = row[0]
        item["FY"] = row[1]
        item["Date"] = row[2]
        item["ActualFees"] = row[3]
        item["ForecastFees"] = row[4]
        item["ActualFullTimeEmployees"] = row[5]
        item["ForecastRequiredFullTimeEmployees"] = row[6]
        item["WorkDaysInPeriod"] = row[7]
        sum_result.append(item)
    
    return sum_result

@api.get('/people/detail')
@api.doc("""
    /people/detail
""")
# @auth.required
def get_people_detail():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId
            , DO.OrgName
            , DD.FY
            , DD.DimDate
            , DES.EmployeeRole
            , func.sum(DES.FteEquivalent).label("FteEquivalent")
            , func.sum(FEU.ActualFteEquivalentMTD).label("ActualFteEquivalentMTD")
            , DES.ItemSort
         )\
        .join(DCC, FEU.DimCompanyKey == DCC.DimCompanyKey)\
        .join(DO, FEU.DimOrganisationKey == DO.DimOrganisationKey)\
        .join(DD, FEU.DimDateKey == DD.DimDateKey)\
        .join(DES, FEU.DimEmployeeKey == DES.DimEmployeeKey)

    if 'DateKeys' in filter_data:
        query = query.filter(DD.DK.in_(filter_data['DateKeys']))

    query_result = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.DimDate, DES.EmployeeRole, DES.ItemSort).all()

    detail_result = {}
    detail_result['Left'] = []
    detail_result['Right'] = []

    for row in query_result:
        item = {}
        item["OrgId"] = row[0]
        item["OrgName"] = row[1]
        item["FY"] = row[2]
        item["Date"] = row[3]
        item["EmployeeRole"] = row[4]
        item["FteEquivalent"] = row[5]
        item["ActualFteEquivalentMTD"] = row[6]
        item["Sort"] = row[7]
        detail_result['Left'].append(item)

        query = g.s\
        .query(
            DO.OrgId
            , DO.OrgName
            , DD.FY
            , DD.DimDate
            , DES.EmployeeRole
            , DES.EmployeeName
            , (func.sum(FEU.ChargeableHoursWorkedMTD) + func.sum(FEU.NonChargeableHoursWorkedMTD)).label("HoursWorked")
            , func.sum(FEU.ChargeableHoursWorkedMTD).label("ChargeableHoursWorkedMTD")
            , func.sum(FEU.NonChargeableHoursWorkedMTD).label("NonChargeableHoursWorkedMTD")
            , FEU.AverageHoursWorkedPerDay
         )\
        .join(DCC, FEU.DimCompanyKey == DCC.DimCompanyKey)\
        .join(DO, FEU.DimOrganisationKey == DO.DimOrganisationKey)\
        .join(DD, FEU.DimDateKey == DD.DimDateKey)\
        .join(DES, FEU.DimEmployeeKey == DES.DimEmployeeKey)

    if 'DateKeys' in filter_data:
        query = query.filter(DD.DK.in_(filter_data['DateKeys']))

    query_result = query.group_by(DO.OrgId, DO.OrgName, DD.FY, DD.DimDate, DES.EmployeeRole, DES.EmployeeName, FEU.AverageHoursWorkedPerDay).all()

    for row in query_result:
        item = {}
        item["OrgId"] = row[0]
        item["OrgName"] = row[1]
        item["FY"] = row[2]
        item["Date"] = row[3]
        item["EmployeeRole"] = row[4]
        item["EmployeeName"] = row[5]
        item["HoursWorked"] = row[6]
        item["ChargeableHoursWorkedMTD"] = row[7]
        item["NonChargeableHoursWorkedMTD"] = row[8]
        item["AverageHoursWorkedPerDay"] = row[9]
        detail_result['Right'].append(item)

    return detail_result

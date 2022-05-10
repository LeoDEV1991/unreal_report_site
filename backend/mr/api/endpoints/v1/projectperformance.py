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


@api.get('/projectperformance/summary')
@api.doc("""
/projectperformance/queyrs
""")
# @auth.required
def get_projectperformance_summary():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
             DO.OrgId 
            ,DO.OrgName
            ,DD.FY
            ,DED.EmployeeName.label("Director")
            ,DEPM.EmployeeName.label("ProjectManager")
            ,DES.EmployeeName.label("Supervisor")
            ,DPT.ProjectTypeDescription
            ,DPST.ProjectSubTypeDescription
            ,FPP.ActualProfitMTD
            ,FPP.ActualProfitYTD
            ,FPP.ActualProfitJTD
            ,DC.ClientName
            ,DP.ProjectName
         )\
        .outerjoin(DP , FPP.DimProjectKey == DP.DimProjectKey)\
        .outerjoin(DC , FPP.DimClientKey == DC.DimClientKey)\
        .outerjoin(DD , FPP.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO , FPP.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DED , FPP.DimEmployeeDirectorKey == DED.DimEmployeeKey)\
        .outerjoin(DEPM , FPP.DimEmployeeProjectManagerKey == DEPM.DimEmployeeKey)\
        .outerjoin(DES , FPP.DimEmployeeSupervisorKey == DES.DimEmployeeKey)\
        .outerjoin(DPT , FPP.DimProjectTypeKey == DPT.DimProjectTypeKey)\
        .outerjoin(DPST , FPP.DimProjectSubTypeKey == DPST.DimProjectSubTypeKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    queryResult = query.all()
    
   
    summarys = []
    for row in queryResult:
        item = {}
        item["OrgId"] = row[0]
        item["OrgName"] = row[1]
        item["FY"] = row[2]
        item["Director"] = row[3]
        item["ProjectManager"] = row[4]
        item["Supervisor"] = row[5]
        item["ProjectTypeDescription"] = row[6]
        item["ProjectSubTypeDescription"] = row[7]
        item["ActualProfitMTD"] = row[8]
        item["ActualProfitYTD"] = row[9]
        item["ActualProfitJTD"] = row[10]
        item["ClientName"] = row[11]
        item["Project"] = row[12]
        summarys.append(item)
    
    return summarys

@api.get('/projectperformance/detail')
@api.doc("""
/projectperformance/detail
""")
# @auth.required
def get_projectperformance_detail():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
             DO.OrgId 
            ,DO.OrgName

            ,DD.FY
            ,DP.ProjectId
            ,DP.ProjectName
            ,DED.EmployeeInitials.label("DirectorInitials")
             
            ,DPT.ProjectTypeDescription
            ,FPP.TotalProjectValue
            ,FPP.ActualHoursMTD
            ,FPP.ActualHoursYTD
            ,FPP.ActualHoursJTD
            ,FPP.ActualFeesInvoicedMTD
            ,FPP.ActualFeesInvoicedYTD
            ,FPP.ActualFeesInvoicedJTD
            ,FPP.ActualCostMTD
            ,FPP.ActualCostYTD
            ,FPP.ActualCostJTD
            ,FPP.ActualProfitMTD
            ,FPP.ActualProfitYTD
            ,FPP.ActualProfitJTD
            ,DED.EmployeeName.label("Director")
            ,DEPM.EmployeeName.label("ProjectManager")
            ,DPST.ProjectSubTypeDescription
            ,DC.ClientName

         )\
        .outerjoin(DD , FPP.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO , FPP.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DED , FPP.DimEmployeeDirectorKey == DED.DimEmployeeKey)\
        .outerjoin(DEPM , FPP.DimEmployeeProjectManagerKey == DEPM.DimEmployeeKey)\
        .outerjoin(DES , FPP.DimEmployeeSupervisorKey == DES.DimEmployeeKey)\
        .outerjoin(DPT , FPP.DimProjectTypeKey == DPT.DimProjectTypeKey)\
        .outerjoin(DP , FPP.DimProjectKey == DP.DimProjectKey)\
        .outerjoin(DC , FPP.DimClientKey == DC.DimClientKey)\
        .outerjoin(DPST , FPP.DimProjectSubTypeKey == DPST.DimProjectSubTypeKey)
    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    queryResult = query.all()
    
   
    details = []
    for row in queryResult:
        item = {}
        item["OrgId"] = row[0];
        item["OrgName"] = row[1];
        item["FY"] = row[2];
        item["ProjectId"] = row[3];
        item["ProjectName"] = row[4];
        item["DirectorInitials"] = row[5];
        item["ProjectTypeDescription"] = row[6];
        item["TotalProjectValue"] = row[7];
        item["ActualHoursMTD"] = row[8];
        item["ActualHoursYTD"] = row[9];
        item["ActualHoursJTD"] = row[10];

        item["ActualFeesInvoicedMTD"] = row[11];
        item["ActualFeesInvoicedYTD"] = row[12];
        item["ActualFeesInvoicedJTD"] = row[13];

        item["ActualCostMTD"] = row[14];
        item["ActualCostYTD"] = row[15];
        item["ActualCostJTD"] = row[16];

        item["ActualProfitMTD"] = row[17];
        item["ActualProfitYTD"] = row[18];
        item["ActualProfitJTD"] = row[19];

        item["Director"] = row[20];
        item["ProjectManager"] = row[21];
        item["ProjectSubTypeDescription"] = row[22];
        item["ClientName"] = row[23];

        details.append(item)
    
    return details

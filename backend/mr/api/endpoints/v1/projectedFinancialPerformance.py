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


@api.get('/projectedFinancialPerformance/summary')
@api.doc("""
Get projectedFinancialPerformance summary data.
""")
# @auth.required
def get_projectedFinancialPerformance_summary():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.DimDateKey, DD.MonthName,
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Actual * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Actual], ])).label("ActualProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Forecast * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Forecast], ])).label("ForecastProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Budget * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Budget], ])).label("BudgetProfit")
         )\
        .outerjoin(DCC, GLIS.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(DD, GLIS.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLIS.DimOrganisationKey == DO.DimOrganisationKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))
    summary = query.group_by(DO.OrgId, DO.OrgName, DD.DimDateKey, DD.MonthName).order_by(DD.DimDateKey).all()
 
    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['DimDateKey'] = row[2]
        item['MonthName'] = row[3]
        item['ActualProfit'] = round(row[4])
        item['ForecastProfit'] = round(row[5])
        item['BudgetProfit'] = round(row[6])

        resp.append(item)

    return resp

@api.get('/projectedFinancialPerformance/detail')
@api.doc("""
projectedFinancialPerformance detail data.
""")
# @auth.required
def get_projectedFinancialPerformance_detail():
  
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(DO.OrgId, 
            DO.OrgName,
            DD.DimDateKey, 
            GLIS.IncomeStatementCategory, 
            GLIS.IncomeStatementSubCategory, 
            GLIS.Actual, 
            GLIS.Budget,
            GLIS.Forecast, 
            GLIS.ActualVsBudgetVariance, 
            GLIS.ActualVsForecastVariance, 
            GLIS.YTDActual,
            GLIS.YTDBudget, 
            GLIS.YTDForecast, 
            GLIS.YTDActualVsBudgetVariance,
            GLIS.YTDActualVsForecastVariance)\
        .outerjoin(DCC, GLIS.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(DD, GLIS.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLIS.DimOrganisationKey == DO.DimOrganisationKey)

    if 'DimDateKeys' in filter_data:
        query = query.filter(DD.DK.in_(filter_data['DimDateKeys']))

    incomeexpense = query.order_by(GLIS.IncomeStatementCategory.desc(), GLIS.IncomeStatementSubCategory).all()
    
    query = g.s\
        .query(DO.OrgId, 
            DO.OrgName,
            DD.DimDateKey, 
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Actual * (-1)], [GLIS.IncomeStatementCategory != "Expense", GLIS.Actual], ])).label("ActualProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Budget * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Budget], ])).label("BudgetProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Forecast * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Forecast], ])).label("ForecastProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.ActualVsBudgetVariance * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.ActualVsBudgetVariance], ])).label("ActualVsBudgetProfitVariance"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.ActualVsForecastVariance * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.ActualVsForecastVariance], ])).label("ActualVsForecastProfitVariance"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDActual * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.YTDActual], ])).label("YTDActualProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDBudget * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.YTDBudget], ])).label("YTDBudgetProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDForecast * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.YTDForecast], ])).label("YTDForecastProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDActualVsBudgetVariance * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.YTDActualVsBudgetVariance], ])).label("YTDActualVsBudgetProfitVariance"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDActualVsForecastVariance * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.YTDActualVsForecastVariance], ])).label("YTDActualVsForecastProfitVariance")
            )\
        .outerjoin(DD, GLIS.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLIS.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DCC, GLIS.DimCompanyKey == DCC.DimCompanyKey)

    if 'DimDateKeys' in filter_data:
        query = query.filter(DD.DK.in_(filter_data['DimDateKeys']))

    profitline = query.group_by(DO.OrgId, DO.OrgName, DD.DimDateKey).all()

    detail = {}
    detail["IncomeExpense"] = []
    detail["Profit"] = []
    resp = []
    for row in incomeexpense:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['DimDateKey'] = row[2]
        item['IncomeStatementCategory'] = row[3]
        item['IncomeStatementSubCategory'] = row[4]
        item['Actual'] = round((row[5]))
        item['Budget'] = round((row[6]))
        item['Forecast'] = round((row[7]))
        item['ActualVsBudgetVariance'] = round((row[8]))
        item['ActualVsForecastVariance'] = round((row[9]))
        item['YTDActual'] = round((row[10]))
        item['YTDBudget'] = round((row[11]))
        item['YTDForecast'] = round((row[12]))
        item['YTDActualVsBudgetVariance'] = round((row[13]))
        item['YTDActualVsForecastVariance'] = round((row[14]))
        resp.append(item)
    detail["IncomeExpense"] = resp
    
    resp = []
    for row in profitline:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['DimDateKey'] = row[2]
        item['ActualProfit'] = round((row[3]))
        item['BudgetProfit'] = round((row[4]))
        item['ForecastProfit'] = round((row[5]))
        item['ActualVsBudgetProfitVariance'] = round(row[6])
        item['ActualVsForecastProfitVariance'] = round((row[7]))
        item['YTDActualProfit'] = round((row[8]))
        item['YTDBudgetProfit'] = round((row[9]))
        item['YTDForecastProfit'] = round((row[10]))
        item['YTDActualVsBudgetProfitVariance'] = round((row[11]))
        item['YTDActualVsForecastProfitVariance'] = round((row[12]))
        resp.append(item)
    detail["Profit"] = resp   
    
    return detail

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
from sqlalchemy import or_ , and_

@api.get('/yearlyfinancialperformanceYTD/summary')
@api.doc("""
Get yearlyfinancial performance summary data.
""")
# @auth.required
def get_yearlyfinancialperformanceYTD_summary():

    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(
            DO.OrgId, DO.OrgName, DD.FY,
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Actual * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Actual], ])).label("Profit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Forecast * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Forecast], ])).label("ForecastProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Income", GLIS.Actual], [GLIS.IncomeStatementCategory != "Income", 0], ])).label("Income")
         )\
        .outerjoin(DC, GLIS.DimCompanyKey == DC.DimCompanyKey)\
        .outerjoin(DD, GLIS.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLIS.DimOrganisationKey == DO.DimOrganisationKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    summary = query.group_by(DO.OrgId, DO.OrgName, DD.FY).order_by(DD.FY).all()
 
    resp = []
    for row in summary:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['Profit'] = (round)(row[3])
        item['ForecastProfit'] = (round)(row[4])
        item['Income'] = (round)(row[5])

        resp.append(item)

    return resp

@api.get('/yearlyfinancialperformanceYTD/detail')
@api.doc("""
yearlyfinancialperformanceYTD detail data.
""")
# @auth.required
def get_yearlyfinancialperformanceYTD_detail():
  
    filter_data = {}
    if 'filter' in request.args:
        filter_data = json.loads(request.args.get('filter'))

    query = g.s\
        .query(DO.OrgId, 
            DO.OrgName,
            DD.FY,
            GLIS.IncomeStatementCategory,
		    GLIS.IncomeStatementSubCategory,
            func.sum(GLIS.Actual).label("Actual"),
            func.sum(GLIS.Budget).label("Budget"),
            func.sum(GLIS.Forecast).label("Forecast"),
            func.sum(GLIS.ActualVsBudgetVariance).label("ActualVsBudgetVariance"),
            func.sum(GLIS.ActualVsForecastVariance).label("ActualVsForecastVariance"),
            func.sum(GLIS.YTDActual).label("YTDActual"),
            func.sum(GLIS.YTDBudget).label("YTDBudget"),
            func.sum(GLIS.YTDForecast).label("YTDForecast"),
            func.sum(GLIS.YTDActualVsBudgetVariance).label("YTDActualVsBudgetVariance"),
            func.sum(GLIS.YTDActualVsForecastVariance).label("YTDActualVsForecastVariance")
        ) \
        .outerjoin(DCC, GLIS.DimCompanyKey == DCC.DimCompanyKey)\
        .outerjoin(DD, GLIS.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLIS.DimOrganisationKey == DO.DimOrganisationKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    if 'defaultYear' in filter_data:
        query = query.filter(or_(and_(DD.Month == (DO.FiscalYearStartMonth - 1), DD.FY != (filter_data['defaultYear'] + case([(filter_data['defaultMonth'] >= DO.FiscalYearStartMonth, 1)], else_=0))),
                                  and_(DD.Month == filter_data['defaultMonth'], DD.FY == (filter_data['defaultYear'] + case([(filter_data['defaultMonth'] >= DO.FiscalYearStartMonth, 1)], else_=0)))))

    incomeexpense = query.group_by(DO.OrgId, DO.OrgName, DD.FY, GLIS.IncomeStatementCategory, GLIS.IncomeStatementSubCategory).\
        order_by(DD.FY, GLIS.IncomeStatementCategory.desc(), GLIS.IncomeStatementSubCategory).all()
    
    query = g.s\
        .query(DO.OrgId, 
            DO.OrgName,
            DD.FY,
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Actual * (-1)], [GLIS.IncomeStatementCategory != "Expense", GLIS.Actual], ])).label("ActualProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Budget * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Budget], ])).label("BudgetProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.Forecast * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.Forecast], ])).label("ForecastProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.ActualVsBudgetVariance * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.ActualVsBudgetVariance], ])).label("ActualVsBudgetProfitVariance"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.ActualVsForecastVariance * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.ActualVsForecastVariance], ])).label("ActualVsForecastProfitVariance"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDActual * -1], [GLIS.IncomeStatementCategory != "Expense",GLIS.YTDActual], ])).label("YTDActualProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDBudget * -1], [GLIS.IncomeStatementCategory != "Expense",GLIS.YTDBudget], ])).label("YTDBudgetProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDForecast * -1], [GLIS.IncomeStatementCategory != "Expense",GLIS.YTDForecast], ])).label("YTDForecastProfit"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDActualVsBudgetVariance * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.YTDActualVsBudgetVariance], ])).label("YTDActualVsBudgetProfitVariance"),
            func.sum(case([[GLIS.IncomeStatementCategory == "Expense", GLIS.YTDActualVsForecastVariance * -1], [GLIS.IncomeStatementCategory != "Expense", GLIS.YTDActualVsForecastVariance], ])).label("YTDActualVsForecastProfitVariance")
            )\
        .outerjoin(DD, GLIS.DimDateKey == DD.DimDateKey)\
        .outerjoin(DO, GLIS.DimOrganisationKey == DO.DimOrganisationKey)\
        .outerjoin(DCC, GLIS.DimCompanyKey == DCC.DimCompanyKey)

    if 'FYs' in filter_data:
        query = query.filter(DD.FY.in_(filter_data['FYs']))

    if 'defaultYear' in filter_data:
        query = query.filter(or_(and_(DD.Month == (DO.FiscalYearStartMonth - 1), DD.FY != (filter_data['defaultYear'] + case([(filter_data['defaultMonth'] >= DO.FiscalYearStartMonth, 1)], else_=0))),
                                  and_(DD.Month == filter_data['defaultMonth'], DD.FY == (filter_data['defaultYear'] + case([(filter_data['defaultMonth'] >= DO.FiscalYearStartMonth, 1)], else_=0)))))

    profitline = query.group_by(DO.OrgId, DO.OrgName, DD.FY).all()

    detail = {}
    detail["IncomeExpense"] = []
    detail["Profit"] = []
    resp = []
    for row in incomeexpense:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['IncomeStatementCategory'] = row[3]
        item['IncomeStatementSubCategory'] = row[4]
        item['Actual'] = round((float)(row[5]))
        item['Budget'] = round((float)(row[6]))
        item['Forecast'] = round((float)(row[7]))
        item['ActualVsBudgetVariance'] = round((float)(row[8]))
        item['ActualVsForecastVariance'] = round((float)(row[9]))
        item['YTDActual'] = round((float)(row[10]))
        item['YTDBudget'] = round((float)(row[11]))
        item['YTDForecast'] = round((float)(row[12]))
        item['YTDActualVsBudgetVariance'] = round((float)(row[13]))
        item['YTDActualVsForecastVariance'] = round((float)(row[14]))
        resp.append(item)
    detail["IncomeExpense"] = resp
    
    resp = []
    for row in profitline:
        item = {}
        item['OrgId'] = row[0]
        item['OrgName'] = row[1]
        item['FY'] = row[2]
        item['ActualProfit'] = round((float)(row[3]))
        item['BudgetProfit'] = round((float)(row[4]))
        item['ForecastProfit'] = round((float)(row[5]))
        item['ActualVsBudgetProfitVariance'] = round((float)(row[6]))
        item['ActualVsForecastProfitVariance'] = round((float)(row[7]))
        item['YTDActualProfit'] = round((float)(row[8]))
        item['YTDBudgetProfit'] = round((float)(row[9]))
        item['YTDForecastProfit'] = round((float)(row[10]))
        item['YTDActualVsBudgetProfitVariance'] = round((float)(row[11]))
        item['YTDActualVsForecastProfitVariance'] = round((float)(row[12]))
        resp.append(item)
    detail["Profit"] = resp   
    
    return detail

# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey, Date , Numeric
from datetime import datetime
from sqlalchemy.dialects.postgresql import BIT
from .base import Base


class FactProjectPerformanceSummary(Base):

    """Docstring for FactProjectPerformanceSummary. """

    __tablename__ = 'FactProjectPerformanceSummary'

    FactProjectSummaryKey  = Column(Integer, primary_key=True, autoincrement=True)
    DimProjectKey = Column(Integer, ForeignKey('DimProject.DimProjectKey'), nullable=False)
    DimCompanyKey = Column(Integer, ForeignKey('DimCompany.DimCompanyKey'), nullable=False)
    DimOrganisationKey = Column(Integer, ForeignKey('DimOrganisation.DimOrganisationKey'), nullable=False)
    DimClientKey = Column(Integer, ForeignKey('DimClient.DimClientKey'))
    DimEmployeeDirectorKey = Column(Integer, ForeignKey('DimEmployee.DimEmployeeKey'))
    DimEmployeeProjectManagerKey = Column(Integer, ForeignKey('DimEmployee.DimEmployeeKey'))
    DimEmployeeSupervisorKey = Column(Integer, ForeignKey('DimEmployee.DimEmployeeKey'))
    DimProjectTypeKey = Column(Integer, ForeignKey('DimProjectType.DimProjectTypeKey'))
    DimProjectSubTypeKey = Column(Integer, ForeignKey('DimProjectSubType.DimProjectSubTypeKey'))
    DimDateKey = Column(Integer, ForeignKey('DimDate.DimDateKey'), nullable=False)

    TotalProjectValue = Column(Numeric(precision=12, scale=2))
    InvoicedToDate = Column(Numeric(precision=12, scale=2))
    AmountYetToInvoice = Column(Numeric(precision=12, scale=2))
    InvoiceForecast12Months = Column(Numeric(precision=12, scale=2))
    InvoiceForecastGreaterThan12Months = Column(Numeric(precision=12, scale=2))
    
    ActualFeesInvoicedMTD = Column(Numeric(precision=12, scale=2));
    ActualFeesInvoicedYTD  = Column(Numeric(precision=12, scale=2));
    ActualFeesInvoicedJTD  = Column(Numeric(precision=12, scale=2));
    ActualCostMTD  = Column(Numeric(precision=12, scale=2));
    ActualCostYTD  = Column(Numeric(precision=12, scale=2));
    ActualCostJTD  = Column(Numeric(precision=12, scale=2));
    ActualProfitMTD  = Column(Numeric(precision=12, scale=2));
    ActualProfitYTD  = Column(Numeric(precision=12, scale=2));
    ActualProfitJTD  = Column(Numeric(precision=12, scale=2));
    ActualHoursMTD  = Column(Numeric(precision=12, scale=2));
    ActualHoursYTD  = Column(Numeric(precision=12, scale=2));
    ActualHoursJTD  = Column(Numeric(precision=12, scale=2));
    FeeVarianceFromForecastMTD  = Column(Numeric(precision=12, scale=2));
    FeeVarianceFromForecastYTD  = Column(Numeric(precision=12, scale=2));
    FeeVarianceFromForecastJTD  = Column(Numeric(precision=12, scale=2));
    
    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'FactProjectPerformanceSummary({})'.format(self.FactProjectPerformanceSummary)

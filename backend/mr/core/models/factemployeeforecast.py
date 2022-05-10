# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, Numeric, ForeignKey
from .base import Base


class FactEmployeeForecast(Base):

    """Docstring for FactEmployeeForecast. """

    __tablename__ = 'FactEmployeeForecast'

    FactEmployeeForecastKey = Column(Integer, primary_key=True, autoincrement=True)
    DimCompanyKey = Column(Integer, ForeignKey('DimCompany.DimCompanyKey'), nullable=False)
    DimOrganisationKey = Column(Integer, ForeignKey('DimOrganisation.DimOrganisationKey'), nullable=False)
    DimDateKey = Column(Integer, ForeignKey('DimDate.DimDateKey'), nullable=False)
    ActualFees = Column(Numeric(precision=19, scale=2))
    ForecastFees = Column(Numeric(precision=19, scale=2))
    ActualFullTimeEmployees = Column(Integer)
    ForecastRequiredFullTimeEmployees = Column(Integer)
    WorkDaysInPeriod = Column(Integer)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'FactEmployeeForecast({})'.format(self.FactEmployeeForecastKey)

# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, Numeric, ForeignKey
from .base import Base


class FactEmployeeUtilisation(Base):

    """Docstring for FactEmployeeForecast. """

    __tablename__ = 'FactEmployeeUtilisation'

    FactEmployeeUtilisationKey = Column(Integer, primary_key=True, autoincrement=True)
    DimCompanyKey = Column(Integer, ForeignKey('DimCompany.DimCompanyKey'), nullable=False)
    DimOrganisationKey = Column(Integer, ForeignKey('DimOrganisation.DimOrganisationKey'), nullable=False)
    DimDateKey = Column(Integer, ForeignKey('DimDate.DimDateKey'), nullable=False)
    DimEmployeeKey = Column(Integer)
    AverageHoursWorkedPerDay = Column(Numeric(precision=10, scale=2))
    ActualFteEquivalentMTD = Column(Numeric(precision=10, scale=2))
    HoursWorkedMTD = Column(Numeric(precision=10, scale=2))
    ChargeableHoursWorkedMTD = Column(Numeric(precision=10, scale=2))
    NonChargeableHoursWorkedMTD = Column(Numeric(precision=10, scale=2))


    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'FactEmployeeUtilisation({})'.format(self.FactEmployeeUtilisationKey)

# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, Unicode, Numeric, DateTime
from datetime import datetime
from sqlalchemy.dialects.postgresql import BIT
from .base import Base


class FactOpportunityHours(Base):

    """Docstring for FactOpportunityHours. """

    __tablename__ = 'FactOpportunityHours'

    FactOpportunityHoursKey = Column(Integer, primary_key=True, autoincrement=True)
    DimOpportunityKey = Column(Integer)
    DimCompanyKey = Column(Integer)
    DimOrganisationKey = Column(Integer)
    DimClientKey = Column(Integer)
    DimEmployeeDirectoryKey = Column(Integer)
    DimEmployeeProjectManagerKey = Column(Integer)
    DimEmployeeSupervisorKey = Column(Integer)
    DimEmployeeOpportunitySourceOneKey = Column(Integer)
    DimEmployeeOpportunitySourceTwoKey = Column(Integer)
    DimDateKey = Column(Integer)
    TotalHours = Column(Numeric(precision=10, scale=2))


    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'FactOpportunityHoursKey({})'.format(self.FactOpportunityHoursKey)

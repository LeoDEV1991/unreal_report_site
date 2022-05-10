# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, Numeric, ForeignKey, Unicode, DateTime
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import BIT
from datetime import datetime

class FactWorkGenerated(Base):

    """Docstring for FactProjectFees. """

    __tablename__ = 'FactWorkGenerated'

    FactWorkGeneratedKey = Column(Integer, primary_key=True, autoincrement=True)
    DimCompanyKey = Column(Integer, ForeignKey('DimCompany.DimCompanyKey'), nullable=False)
    DimOrganisationKey = Column(Integer, ForeignKey('DimOrganisation.DimOrganisationKey'), nullable=False)
    DimProjectKey = Column(Integer, ForeignKey('DimProject.DimProjectKey'))
    DimClientKey = Column(Integer, ForeignKey('DimClient.DimClientKey'))
    DimProjectTypeKey = Column(Integer, ForeignKey('DimProjectType.DimProjectTypeKey'))
    DimProjectSubTypeKey = Column(Integer, ForeignKey('DimProjectSubType.DimProjectSubTypeKey'))
    DimEmployeeProjectSourceOneKey = Column(Integer)
    DimEmployeeProjectSourceTwoKey = Column(Integer)
    DimDateKey = Column(Integer, ForeignKey('DimDate.DimDateKey'), nullable=False)

    ProjectStatus = Column(Unicode(10))
    ProjectFee = Column(Numeric(precision=19, scale=2))
    WorkGeneratedAmount = Column(Numeric(precision=19, scale=2))
    ExistingOrNew = Column(Unicode(20))
    IsActive = Column(BIT)
    CreateDate = Column(DateTime, default=datetime.utcnow)
    ModDate = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'FactWorkGenerated({})'.format(self.FactWorkGenerated)

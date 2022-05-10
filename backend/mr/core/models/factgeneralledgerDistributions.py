# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, Numeric, DateTime
from .base import Base
from sqlalchemy.dialects.postgresql import BIT
from datetime import datetime

class FactGeneralLedgerDistributions(Base):

    """Docstring for FactGeneralLedgerDistributions. """

    __tablename__ = 'FactGeneralLedgerDistributions'

    FactGeneralLedgerDistributionsKey = Column(Integer, primary_key=True, autoincrement=True)
    DimCompanyKey = Column(Integer, nullable=False)
    DimOrganisationKey = Column(Integer, nullable=False)
    DimDateKey = Column(Integer, nullable=False)
    DimChartOfAccountsKey = Column(Integer, nullable=False)
    DistributionAmount = Column(Numeric(precision=19, scale=2))
    IsActive = Column(BIT)
    CreateDate = Column(DateTime, default=datetime.utcnow)
    ModDate = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'FactGeneralLedgerDistributions({})'.format(self.FactGeneralLedgerDistributionsKey)

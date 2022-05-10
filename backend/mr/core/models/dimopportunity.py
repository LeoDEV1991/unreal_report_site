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


class DimOpportunity(Base):

    """Docstring for DimOpportunity. """

    __tablename__ = 'DimOpportunity'

    DimOpportunityKey = Column(Integer, primary_key=True, autoincrement=True)
    OpportunityId = Column(Unicode(50))
    Name = Column(Unicode(100))
    Status = Column(Unicode(50))
    PotentialRevenue = Column(Numeric(precision=19, scale=2))
    ProbabilityOfSuccess = Column(Numeric(precision=5, scale=2))
    WeightedPotentialRevenue = Column(Numeric(precision=19, scale=2))
    OpportunityType = Column(Unicode(50))
    OpportunitySubType = Column(Unicode(50))
    OpenedDate = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    ClosedDate = Column(DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    ReasonClosed = Column(Unicode(20))

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'DimOpportunityKey({})'.format(self.DimOpportunityKey)

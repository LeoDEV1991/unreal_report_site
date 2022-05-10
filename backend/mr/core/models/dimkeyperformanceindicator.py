# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, Unicode, Numeric
from sqlalchemy.dialects.postgresql import BIT
from .base import Base


class DimKeyPerformanceIndicator(Base):

    """Docstring for DimKeyPerformanceIndicator. """

    __tablename__ = 'DimKeyPerformanceIndicator'

    DimKeyPerformanceIndicatorKey = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(Unicode(225))
    Category = Column(Unicode(50))
    Description = Column(Unicode(5000))
    Priority = Column(Unicode(20))
    Target = Column(Numeric(precision=19, scale=2))
    DesiredOutcome = Column(Unicode(12))
    PercentageTolerance = Column(Numeric(precision=10, scale=2))
    DisplayFormat = Column(Unicode(20))
    Enable = Column(BIT)

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'DimKeyPerformanceIndicator({})'.format(self.DimKeyPerformanceIndicatorKey)

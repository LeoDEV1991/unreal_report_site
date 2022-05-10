# -*- coding: utf-8 -*-
"""
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

from sqlalchemy import Column, Integer, Numeric , Text
from .base import Base


class FactExecutiveSummary(Base):

    """Docstring for FactGeneralLedgerExpenses. """

    __tablename__ = 'FactExecutiveSummary'

    FactExecutiveSummaryKey = Column(Integer, primary_key=True, autoincrement=True)
    DimCompanyKey = Column(Integer, nullable=False)
    DimOrganisationKey = Column(Integer, nullable=False)
    DimDateKey = Column(Integer, nullable=False)
    ExecutiveSummaryHTML = Column(Text, nullable=False)
    CreateDate = Column(Numeric(precision=12, scale=2))
    ModDate = Column(Numeric(precision=12, scale=2))

    def __repr__(self):
        """TODO: Docstring for __repr__.
        :returns: TODO

        """
        return 'FactExecutiveSummary({})'.format(self.FactExecutiveSummary)

"""
This module provides common type definitions along with a comprehensive resource identifier catalogue.
"""

__all__ = [
    "AccountId",
    "AccountMngtFeeSchemeId",
    "ActionId",
    "AgentId",
    "AnalyticalTypeId",
    "ArtifactId",
    "AssetClassId",
    "Currency",
    "Date",
    "DateTime",
    "GUID",
    "GroupId",
    "InstitutionId",
    "PortfolioGroupId",
    "PortfolioId",
    "QuantId",
    "RiskProfileId",
    "SharingId",
    "StrategyId",
    "Tags",
    "TeamId",
    "TimeDelta",
    "UserId",
    "_LaterI",
    "_LaterS",
]

from datetime import date as Date
from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
from typing import NewType, Set

#: Defines a type alias for globally unique resource identifiers.
GUID = NewType("GUID", str)

#: Defines a new-type for currency codes.
Currency = NewType("Currency", str)

#: Defines a type alias for standard set of tags.
Tags = Set[str]

#: Defines a new-type for DECAF quant resource identifier.
QuantId = NewType("QuantId", int)

#: Defines a new-type for DECAF artifact resource identifier.
ArtifactId = NewType("ArtifactId", int)

#: Defines a new-type for DECAF action resource identifier.
ActionId = NewType("ActionId", int)

#: Defines a new-type for DECAF account resource identifier.
AccountId = NewType("AccountId", int)

#: Defines a new-type for DECAF agent resource identifier.
AgentId = NewType("AgentId", int)

#: Defines a new-type for DECAF institution resource identifier.
InstitutionId = NewType("InstitutionId", int)

#: Defines a new-type for DECAF strategy resource identifier.
StrategyId = NewType("StrategyId", int)

#: Defines a new-type for DECAF risk profile resource identifier.
RiskProfileId = NewType("RiskProfileId", int)

#: Defines a new-type for DECAF asset class resource identifier.
AssetClassId = NewType("AssetClassId", int)

#: Defines a new-type for DECAF portfolio resource identifier.
PortfolioId = NewType("PortfolioId", int)

#: Defines a new-type for DECAF account management fee scheme resource identifier.
AccountMngtFeeSchemeId = NewType("AccountMngtFeeSchemeId", int)

#: Defines a new-type for DECAF analytical type resource identifier.
AnalyticalTypeId = NewType("AnalyticalTypeId", int)

#: Defines a new-type for DECAF institution sharing resource identifier.
SharingId = NewType("SharingId", int)

#: Defines a new-type for DECAF user resource identifier.
UserId = NewType("UserId", int)

#: Defines a new-type for DECAF team resource identifier.
TeamId = NewType("TeamId", int)

#: Defines a new-type for DECAF group resource identifier.
GroupId = NewType("GroupId", int)

#: Defines a new-type for DECAF portfolio group resource identifier.
PortfolioGroupId = NewType("PortfolioGroupId", int)

#: Defines a new-type for DECAF resource identifiers which are yet to be declared (of :py:class:`int` type).
_LaterI = NewType("_LaterI", int)

#: Defines a new-type for DECAF resource identifiers which are yet to be declared (of :py:class:`str` type).
_LaterS = NewType("_LaterS", int)

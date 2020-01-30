__all__ = [
    "Currencies",
    "CurrencyResource",
]

from decimal import Decimal
from typing import Optional

from pydantic import validator

from decaf.api.client.machinery import BaseResource, ResourceListEndpoint, ResourceRetrieveEndpoint, command
from decaf.api.client.types import Currency, Date


class CurrencyResource(BaseResource):
    code: Currency
    name: str
    decimals: Optional[int]

    @validator("decimals")
    def decimals_can_be_optional(cls, v: int) -> Optional[int]:
        return v if v >= 0 else None


class Currencies(ResourceListEndpoint[CurrencyResource], ResourceRetrieveEndpoint[Currency, CurrencyResource]):
    endpoint = "currencies"
    resource = CurrencyResource

    @command
    def conversion(self, ccy1: Currency, ccy2: Currency, date: Date, qty: Decimal = Decimal(1)) -> Decimal:
        return self.client.request(  # type: ignore
            "GET",
            [self.endpoint, "conversion"],
            params={"ccy1": ccy1, "ccy2": ccy2, "asof": str(date), "qty": str(qty)},
        )["value"]

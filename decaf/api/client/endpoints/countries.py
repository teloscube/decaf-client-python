__all__ = [
    "Countries",
    "CountryResource",
]

from decaf.api.client.machinery import BaseResource, ResourceListEndpoint, ResourceRetrieveEndpoint
from decaf.api.client.types import CountryId


class CountryResource(BaseResource):
    id: CountryId
    name: str


class Countries(ResourceListEndpoint[CountryResource], ResourceRetrieveEndpoint[CountryId, CountryResource]):
    endpoint = "countries"
    resource = CountryResource

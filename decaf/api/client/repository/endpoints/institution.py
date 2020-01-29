__all__ = [
    "InstitutionResource",
    "InstitutionCreateForm",
    "InstitutionUpdateForm",
    "InstitutionPatchForm",
    "Institutions",
]

from decimal import Decimal
from typing import List, Optional, Union

from decaf.api.client.repository.commons import (
    BaseCreateForm,
    BasePatchForm,
    BaseRepository,
    BaseResource,
    BaseUpdateForm,
    DateTime,
    Missing,
)
from decaf.api.client.repository.types import GUID, AccountId, InstitutionId, SharingId, _LaterI


class InstitutionResource(BaseResource):
    id: InstitutionId
    guid: GUID
    created: DateTime
    creator: Optional[_LaterI]
    updated: DateTime
    updater: Optional[_LaterI]
    name: str
    accounts: List[AccountId]
    sharings: List[SharingId]
    sharing: Optional[Decimal]
    kickback: Optional[Decimal]


class InstitutionCreateForm(BaseCreateForm):
    name: str


class InstitutionUpdateForm(BaseUpdateForm):
    id: InstitutionId
    name: str


class InstitutionPatchForm(BasePatchForm):
    id: InstitutionId
    name: Union[str, Missing] = Missing.field()


class Institutions(
    BaseRepository[
        InstitutionId, InstitutionResource, InstitutionCreateForm, InstitutionUpdateForm, InstitutionPatchForm
    ]
):
    endpoint = "institutions"
    identifier = InstitutionId
    resource = InstitutionResource
    form_create = InstitutionCreateForm
    form_update = InstitutionUpdateForm
    form_patch = InstitutionPatchForm

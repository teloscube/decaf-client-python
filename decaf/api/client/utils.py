__all__ = ["make_lookup_table"]

from typing import Dict, Iterable, TypeVar
from typing_extensions import Protocol

#: Defines a type alias for resource identifiers.
_Id = TypeVar("_Id")


class WithId(Protocol[_Id]):
    """
    Provides a generic protocol for models with ``id`` attribute.
    """

    #: Unique identifier of the instance.
    id: _Id


def make_lookup_table(iterable: Iterable[WithId[_Id]]) -> Dict[_Id, WithId[_Id]]:
    return {r.id: r for r in iterable}

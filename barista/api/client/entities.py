from dataclasses import dataclass, fields
from typing import TypeVar, Type, Dict, Any, List

from barista.api.client.machinery import Client


#: Defines a generic type variable for entity subclasses.
E = TypeVar("E", bound="Entity")


#: Defines a type alias for primary identifier of entity instances.
ID = int


@dataclass(frozen=True)
class Entity:
    """
    Provides the base class for ordinary remote entity models.
    """

    #: Defines the identifier of the entity.
    id: ID

    #: Defines the globally unique identifier of the entity.
    guid: str

    def __init_subclass__(cls, **kwargs: Any) -> None:
        ## Get the endpoint URI path segment:
        try:
            endpoint = kwargs.pop("endpoint")
        except KeyError:
            raise TypeError("Entity implementation is missing the 'endpoint' specifier.")

        ## Promote the endpoint to the class:
        cls.__endpoint = endpoint

        ## Proceed with the initialization:
        super().__init_subclass__()

    @classmethod
    def of(cls: Type[E], data: Dict[str, Any]) -> E:
        """
        Creates an instance of entity from the given data.
        """
        return cls(**{f.name: data[f.name] for f in fields(cls)})


@dataclass(frozen=True)
class Account(Entity, endpoint="accounts"):
    #: Defines the name of the account.
    name: str

    #: Defines the reference currency of the account.
    rccy: str

    #: Defines the portfolio `ID` which the account belongs to.
    portfolio: int

    #: Defines the institution `ID` which the account is custodied by.
    custodian: int


@dataclass(frozen=True)
class Institution(Entity, endpoint="institutions"):
    #: Defines the name of the institution.
    name: str


@dataclass(frozen=True)
class Portfolio(Entity, endpoint="portfolios"):
    #: Defines the name of the portfolio.
    name: str

    #: Defines the team `ID` which the portfolio is managed by.
    team: ID


@dataclass(frozen=True)
class Team(Entity, endpoint="teams"):
    #: Defines the name of the team.
    name: str


def get_all_entities(client: Client, etype: Type[E]) -> List[E]:
    """
    Returns all entities for the given :class:`Entity` type.
    """
    return [etype.of(d) for d in client.get(getattr(etype, "_endpoint"), params={"page_size": "-1"})]


def get_entities_table(client: Client, etype: Type[E]) -> Dict[int, E]:
    """
    Returns a lookup table for ``entity id -> entity instance`` mapping.
    """
    return {e.id: e for e in get_all_entities(client, etype)}

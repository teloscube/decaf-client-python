"""
This module provides data, type and function definitions which could be useful on import-side. Some of there are used
internally in this library, too.
"""

__all__ = [
    "WithId",
    "identity",
    "make_lookup_table",
    "parse_isodate",
    "percentify",
    "remove_microseconds",
    "skipnone",
    "sort_and_group_by",
]

from decimal import Decimal
from itertools import groupby
from typing import Callable, Dict, Iterable, Optional, Tuple, TypeVar, Union

from typing_extensions import Protocol

from .types import Date, DateTime

#: Defines a generic type alias.
_T = TypeVar("_T")


def identity(x: _T) -> _T:
    """
    Provides an identity function.

    Return value type is inferred the same as the parameter type.

    :param x: Value.
    :return: Value.

    >>> identity(1)
    1
    >>> identity("value")
    'value'
    """
    return x


def skipnone(func: Callable[[_T], _T]) -> Callable[[Optional[_T]], Optional[_T]]:
    """
    Provides a function decorator for avoiding function application if the value is ``None``.

    :param func: Function to decorate.
    :return: Decorated function

    >>> add1: Callable[[int], int] = lambda x: x + 1
    >>> add1(1)
    2
    >>> add1(None)
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
    >>> skipnone(add1)(1)
    2
    >>> skipnone(add1)(None)
    >>>

    You can define a new function using the decorator (note the function signature):

    >>> safe_add1: Callable[[Optional[int]], Optional[int]] = skipnone(add1)
    >>> safe_add1(1)
    2
    >>> safe_add1(None)
    >>>

    ... or decorate functions as such:

    >>> @skipnone
    ... def double(x: int) -> int:
    ...     return x * 2
    >>> double(1)
    2
    >>> double(None)
    >>>
    """
    return lambda x: x if x is None else func(x)


def remove_microseconds(x: DateTime) -> DateTime:
    """
    Removes microseconds from the given :py:class:`datetime.datetime` instance.

    :param x: :py:class:`datetime.datetime` instance
    :return: A new :py:class:`datetime.datetime` instance with microseconds set to ``0``.

    >>> DateTime(2019, 1, 2, 3, 4, 5, 6789)
    datetime.datetime(2019, 1, 2, 3, 4, 5, 6789)
    >>> remove_microseconds(DateTime(2019, 1, 2, 3, 4, 5, 6789))
    datetime.datetime(2019, 1, 2, 3, 4, 5)
    """
    return x.replace(microsecond=0)


def percentify(x: Union[float, int, str, Decimal]) -> Decimal:
    """
    Consumes a value representing a number and returns its percentage points as a :py:class:`Decimal` instance.

    :param x: A value representing a number.
    :return: Percentage points as a :py:class:`Decimal` instance.
    :raises decimal.InvalidOperation: In case that parameter can not be converted to valid :py:class:`Decimal` instance.

    >>> percentify(0.01)
    Decimal('1.00')
    >>> percentify(0)
    Decimal('0')
    >>> percentify("0.01")
    Decimal('1.00')
    >>> percentify(Decimal("0.01"))
    Decimal('1.00')
    >>> percentify(1.0)
    Decimal('100.0')
    >>> percentify(1)
    Decimal('100')
    >>> percentify("1")
    Decimal('100')
    >>> percentify(Decimal(1))
    Decimal('100')
    >>> percentify("xyz")
    Traceback (most recent call last):
    ...
    decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]
    """
    return Decimal(str(x)) * Decimal(100)


def parse_isodate(x: str) -> Date:
    """
    Attempts to parse an ISO formatted date string and returns it as a :py:class:`datetime.date` instance.

    :param x: ISO formatted date string
    :return: A :py:class:`datetime.date` instance, if parsing is successful.
    :raises ValueError: If the parameter does not represent a valid date or is not formatted as a valid ISO date string.

    >>> parse_isodate("2019-01-02")
    datetime.date(2019, 1, 2)
    >>> parse_isodate("2019-02-29")
    Traceback (most recent call last):
    ...
    ValueError: day is out of range for month
    >>> parse_isodate("20190228")
    Traceback (most recent call last):
    ...
    ValueError: time data '20190228' does not match format '%Y-%m-%d'
    """
    return DateTime.strptime(x, "%Y-%m-%d").date()


class WithId(Protocol[_T]):
    """
    Provides a generic protocol for models with ``id`` attribute.
    """

    #: Unique identifier of the instance.
    id: _T


def make_lookup_table(records: Iterable[WithId[_T]]) -> Dict[_T, WithId[_T]]:
    """
    Creates a lookup table from a iterable of records following :py:class:`WithId` protocol.

    :param records: Iterable of records.
    :return: A lookup table of record id to record.

    >>> make_lookup_table([])
    {}
    >>> from dataclasses import dataclass
    >>> @dataclass
    ... class A:
    ...     id: int
    ...     value: bool
    >>> records = [A(1, True), A(2, False)]
    >>> table = make_lookup_table(records)
    >>> table[1].value
    True
    >>> table[2].value
    False
    """
    return {r.id: r for r in records}


#: Defines a generic type alias.
_K = TypeVar("_K")

#: Defines a generic type alias.
_V = TypeVar("_V")


def sort_and_group_by(x: Iterable[_V], key: Callable[[_V], _K]) -> Iterable[Tuple[_K, Iterable[_V]]]:
    """
    Sorts and groups an iterable of values by the same key.

    :param x: Iterable of values.
    :param key: Function to compute the key from a given value.
    :return: An iterable of tuples of key and iterable of values for the key.
    """
    return groupby(sorted(x, key=key), key=key)  # type: ignore

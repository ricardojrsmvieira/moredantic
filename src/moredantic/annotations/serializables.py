"""Serializables annotations module."""

# ---> Standard library imports <--- #
from typing import Annotated, Any

# ---> Third party imports <--- #
from pydantic import PlainSerializer, TypeAdapter


type SerializableTypeAnt = Annotated[
  type,
  PlainSerializer(lambda v: v.__name__)
]

type SerializableTypeAdapterAnt = Annotated[
  TypeAdapter[Any],
  PlainSerializer(str)
]

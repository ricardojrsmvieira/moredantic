"""Strings annotations module."""

# ---> Standard library imports <--- #
from typing import Annotated

# ---> Third party imports <--- #
from pydantic import BeforeValidator, Field


type StripStrAnt = Annotated[
  str,
  Field(min_length = 1),
  BeforeValidator(lambda v: v.strip())
]

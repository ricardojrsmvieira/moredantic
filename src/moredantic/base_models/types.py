"""Types for the base models."""

# ---> Standard library imports <--- #
from typing import TypedDict

# ---> First party imports <--- #
from moredantic.types import BaseClassModelSelfConfigType


# ! IMPORTANT : Whatever you add to one, add to the other ->
class DefaultBaseModelSelfConfigType(TypedDict):
  """Default Base Model Self Config Type."""
  get_identifier: str | tuple[str, ...] | None
class ModelSelfConfigType(BaseClassModelSelfConfigType, total = False):
  """Model Self Config Type."""
  get_identifier: str | tuple[str, ...] | None
# <- Whatever you add to one, add to the other : IMPORTANT !

class RootModelSelfConfigType(BaseClassModelSelfConfigType, total = False):
  """Root Model Self Config Type."""

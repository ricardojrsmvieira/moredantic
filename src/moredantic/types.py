"""Types for the mydantic package."""

# ---> Standard library imports <--- #
from typing import TypedDict


# ! IMPORTANT : Whatever you add to one, add to the other ->
class DefaultBaseClassModelSelfConfigType(TypedDict):
  """DefaultBaseClassModelSelfConfigType TypedDict."""
  is_abstract_base_class: bool
  needs_subclassing: bool
class BaseClassModelSelfConfigType(TypedDict, total = False):
  """BaseClassModelSelfConfigType TypedDict."""
  is_abstract_base_class: bool
  needs_subclassing: bool
# <- Whatever you add to one, add to the other : IMPORTANT !

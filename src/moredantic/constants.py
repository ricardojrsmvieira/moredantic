"""Constants for the mydantic package."""

# ---> Local imports <--- #
from .types import DefaultBaseClassModelSelfConfigType


DEFAULT_BASE_CLASS_MODEL_SELF_CONFIG = DefaultBaseClassModelSelfConfigType(
  is_abstract_base_class = False,
  needs_subclassing = False
)

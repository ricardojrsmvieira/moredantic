"""Constants for the base models package."""

# ---> Third party imports <--- #
from pydantic import ConfigDict

# ---> First party imports <--- #
from moredantic.decorators.base_decorator import base_decorator

# ---> Local imports <--- #
from .types import DefaultBaseModelSelfConfigType


BASE_CONFIG_DICT = ConfigDict(
  extra = 'forbid',
  strict = True,
  frozen = True,
  ignored_types = (base_decorator, )
)
ROOT_CONFIG_DICT = {k: v for k, v in BASE_CONFIG_DICT.items() if k != 'extra'}


DEFAULT_BASE_MODEL_SELF_CONFIG: DefaultBaseModelSelfConfigType = {
  'get_identifier': None
}

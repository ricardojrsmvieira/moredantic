"""Moredantic package."""

#################################### Actual moredantic package #####################################
# ---> Local imports <--- #
from .annotations import (
  SerializableTypeAdapterAnt as SerializableTypeAdapterAnt,
  SerializableTypeAnt as SerializableTypeAnt,
  StripStrAnt as StripStrAnt,
)
from .base_models import (
  BaseModel as BaseModel,
  ModelSelfConfigType as ModelSelfConfigType,
  RootArbitraryModel as RootArbitraryModel,
  RootModel as RootModel,
)
from .data_shapes import (
  LiterallyValidatedDict as LiterallyValidatedDict,
  RecursiveDictBaseClass as RecursiveDictBaseClass,
  RecursiveDictStr as RecursiveDictStr,
)
from .decorators import instance_docstring as instance_docstring

# pyright: reportImportCycles = false
# # ruff: noqa: E402
"""Moredantic package."""


################################ Handle DebugManager initialization ################################
# ---> Third party imports <--- #
from debug_group import DebugManager as _DebugManager


if _DebugManager._instance is None: # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
  print('WARNING: DebugManager is not initialized. Moredantic will initialize DebugManager with'  # noqa: T201
        'default settings. If you want to customize DebugManager settings, please initialize'
        'DebugManager before importing Moredantic. If you do not do so, no debug prints will'
        'be shown, neither for moredantic nor for any other package or your own code.')
  _MyDebugManager = _DebugManager({})
else:
  _MyDebugManager = _DebugManager._instance # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
_MyDebugGroup = _MyDebugManager.MyDebugGroup
_NONE_DEBUG_GROUP = _MyDebugManager.NONE_DEBUG_GROUP


del (
  _DebugManager,
  _MyDebugManager,
  _MyDebugGroup,
  _NONE_DEBUG_GROUP
)


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


__all__ = [
  'BaseModel',
  'LiterallyValidatedDict',
  'ModelSelfConfigType',
  'RecursiveDictBaseClass',
  'RecursiveDictStr',
  'RootArbitraryModel',
  'RootModel',
  'SerializableTypeAdapterAnt',
  'SerializableTypeAnt',
  'StripStrAnt',
  'instance_docstring'
]

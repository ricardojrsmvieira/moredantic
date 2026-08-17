"""Root Model module."""

# ---> Standard library imports <--- #
from abc import ABC
from typing import ClassVar, override

# ---> Third party imports <--- #
from pydantic import RootModel as PydanticRootModel

# ---> First party imports <--- #
from moredantic.base_class import BaseClass

# ---> Local imports <--- #
from .constants import ROOT_CONFIG_DICT
from .types import RootModelSelfConfigType


class RootModel[T](BaseClass, PydanticRootModel[T], ABC):
  """Root Model class."""
  #region Model Config + Class Variables
  # Safe since we are just removing 'extra' from CONFIG_DICT to comply with RootModel
  model_config = ROOT_CONFIG_DICT # pyright: ignore[reportAssignmentType]
  model_self_config: ClassVar[RootModelSelfConfigType]
  #endregion Model Config + Class Variables


  #region Instance Fields + Properties
  #endregion Instance Fields + Properties


  #region Init Subclass + Abstract Methods
  #endregion Init Subclass + Abstract Methods


  #region Class + Static Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Class + Static Methods


  #region New + Init + Post Init + Validators Methods
  @override
  def __init__(self, root: T) -> None:
    if not type(self).is_instantiatable:
      msg = (f'Cannot instantiate generic class {type(self).__name__} with unbound type variables '
             'OR if it needs subclassing.')
      raise TypeError(msg)
    # ruff: disable[SLF001] # Private because not supposed to be used outside of this class, but we need to access it here
    if type(self)._is_intermediate and not type(self).generic_types:
      type(self)._debug_group.print('Intermediate class instance detected, first instance, '
                                    'saving generic types for', type(self).__name__, '...')
      type(self)._save_generic_types_converting_typealiastype(self.__pydantic_generic_metadata__['args'])
      type(self)._after_generic_types_populated()
    # ruff: enable[SLF001]

    super().__init__(root) # pyright: ignore[reportUnknownMemberType]
  #endregion New + Init + Post Init + Validators Methods


  #region Instance Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Instance Methods

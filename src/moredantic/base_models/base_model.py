"""Base Model module."""

# ---> Standard library imports <--- #
from abc import ABC
from functools import cached_property
from typing import Any, ClassVar, Literal, LiteralString, Self, get_args, override

# ---> Third party imports <--- #
from pydantic import BaseModel as PydanticBaseModel

# ---> First party imports <--- #
from moredantic.base_class import BaseClass

# ---> Local imports <--- #
from .constants import BASE_CONFIG_DICT, DEFAULT_BASE_MODEL_SELF_CONFIG
from .types import ModelSelfConfigType


class BaseModel[
  getIdentifierNameType: LiteralString | str = str,
](BaseClass, PydanticBaseModel, ABC):
  """Base model class that extends Pydantic's BaseModel and adds additional functionality."""
  #region Model Config + Class Variables
  model_config = BASE_CONFIG_DICT
  model_self_config: ClassVar[ModelSelfConfigType]

  # If set, it means that this class is used to create instances that are identified by the value of
  # the field with the name of get_identifier, so it should be unique among all instances created
  # from this class. Also, a get() method will be added to the class to get the instance by the
  # value of the identifier field.
  _get_identifier: ClassVar[tuple[str, ...] | None] = None
  _get_identifier_name_list: ClassVar[list[str] | None] = None
  #endregion Model Config + Class Variables


  #region Instance Fields + Properties
  @cached_property
  def names_list(self) -> list[getIdentifierNameType] | None:
    """
    Returns a list of the names of the fields that are used as identifiers for this instance.

    If no identifier fields are set, returns None.
    """
    if self._get_identifier:
      if type(self).generic_types[0] is str:
        msg = (f'Class {type(self).__name__} has a get_identifier field, '
               f'but no generic type is specified for the identifier.')
        raise TypeError(msg)
    else:
      if type(self).generic_types[0] is not str:
        msg = (f'Class {type(self).__name__} does not have a get_identifier field, '
               f'but a generic type is specified.')
        raise TypeError(msg)

      return None

    return [getattr(self, identifier) for identifier in self._get_identifier]
  #endregion Instance Fields + Properties


  #region Init Subclass + Abstract Methods
  @override
  def __init_subclass__(cls, **kwargs: Any) -> None:
    if 'model_self_config' in cls.__dict__:
      config = cls.__dict__['model_self_config']
      for config_name, config_default in DEFAULT_BASE_MODEL_SELF_CONFIG.items():
        setattr(cls, f'_{config_name}', config.get(config_name, config_default))
        config.pop(config_name, None)
      if isinstance(cls._get_identifier, str):
        cls._get_identifier = (cls._get_identifier,)
      cls.model_self_config = config
    else:
      for config_name, config_default in DEFAULT_BASE_MODEL_SELF_CONFIG.items():
        setattr(cls, f'_{config_name}', config_default)

    super().__init_subclass__(**kwargs)

    cls.__list__: dict[getIdentifierNameType, Self] = {}
    if cls._get_identifier:
      # The fields can be defined in parent classes or in the class itself.
      # We need to check both places for the fields that are used as identifiers.
      available_fields = set(cls.model_fields.keys()) | set(cls.__annotations__.keys())
      for identifier in cls._get_identifier:
        if identifier not in available_fields:
          msg = (f'Field name {identifier} cannot be used as identifier for class {cls.__name__} '
                 f'instances because it does not exist in the instances fields.')
          raise TypeError(msg)

      if cls.generic_types and cls.generic_types[0] is Literal:
        cls._get_identifier_name_list = list(get_args(cls.generic_types[0]))
      else:
        cls._get_identifier_name_list = None

    else:
      cls._get_identifier_name_list = None

  #endregion Init Subclass + Abstract Methods


  #region Class + Static Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  @classmethod
  def get(cls, identifier: getIdentifierNameType) -> Self | None:
    """Return the instance of the class that has the specified identifier."""
    if not cls._get_identifier:
      msg = f'Class {cls.__name__} cannot use the get() method without a get_identifier field.'
      raise TypeError(msg)

    if cls._get_identifier_name_list:
      if identifier not in cls._get_identifier_name_list:
        msg = (f"Identifier '{identifier}' is not a valid identifier for class {cls.__name__}. "
               f"Valid identifiers are: {cls._get_identifier_name_list}")
        raise ValueError(msg)
      return cls.__list__[identifier]

    return cls.__list__.get(identifier, None)
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Class + Static Methods


  # ruff: disable[SLF001] # Private because not supposed to be used outside of this class, but we need to access it here
  #region New + Init + Post Init + Validators Methods
  @override
  def __init__(self, **data: Any) -> None:
    if not type(self).is_instantiatable:
      msg = f'Cannot instantiate generic class {type(self).__name__} with unbound type variables'
      raise TypeError(msg)

    if type(self)._is_intermediate and not type(self).generic_types:
      type(self)._debug_group.print(f'Intermediate class instance detected, first instance, saving '
                                    f'generic types for: {type(self).__name__}...')
      type(self)._save_generic_types_converting_typealiastype(self.__pydantic_generic_metadata__['args'])
      type(self)._after_generic_types_populated()

    super().__init__(**data)


  @override
  def model_post_init(self, context: Any) -> None:
    if type(self)._get_identifier:
      # It's never None, we just verified it here
      final_identifier = '.'.join(value for value in (
                                    getattr(self, identifier) for identifier in
                                      type(self)._get_identifier)) # pyright: ignore[reportOptionalIterable]
      if final_identifier in type(self).__list__:
        msg = (f"Instance with identifier '{final_identifier}' already exists in class "
               f"{type(self).__name__}. Cannot create another instance with the same identifier.")
        raise ValueError(msg)

      names_accepted = type(self)._get_identifier_name_list
      if names_accepted and final_identifier not in names_accepted:
        msg = (f"Identifier '{final_identifier}' is not a valid identifier for class "
               f"{type(self).__name__}. Valid identifiers are: {names_accepted}")
        raise ValueError(msg)

      # We raise an error above if the identifier is not valid, so we can assume it is valid here
      type(self).__list__[final_identifier] = self # pyright: ignore[reportArgumentType]

    super().model_post_init(context)
  # ruff: enable[SLF001]
  #endregion New + Init + Post Init + Validators Methods


  #region Instance Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Instance Methods

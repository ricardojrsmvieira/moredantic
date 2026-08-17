"""BaseClass module for Moredantic models."""

# ---> Standard library imports <--- #
import re
from collections.abc import Sequence
from typing import Any, ClassVar, NoDefault, TypeAliasType, get_args, override

# ---> First party imports <--- #
from moredantic import (
  _NONE_DEBUG_GROUP as NONE_DEBUG_GROUP,  # pyright: ignore[reportPrivateUsage]
  _MyDebugGroup as MyDebugGroup,  # pyright: ignore[reportPrivateUsage]
  _MyDebugManager as MyDebugManager,  # pyright: ignore[reportPrivateUsage]
)

# ---> Local imports <--- #
from .constants import DEFAULT_BASE_CLASS_MODEL_SELF_CONFIG


class BaseClass:
  """Base class that contains common added functionality for all models."""
  #region Model Config + Class Variables
  # Data handled by this class. Public since that can be helpfull outside.
  is_instantiatable: ClassVar[bool] = False
  generic_types: ClassVar[tuple[type, ...]] = ()
  # Data handled by this class. Private since it's only for internal use.
  _is_abstract_base_class: ClassVar[bool] = True
  _needs_subclassing: ClassVar[bool] = False # Only used if _father_is_generic is True
  _is_generic: ClassVar[bool] = False
  _number_of_non_default_type_params: int = 0 # Only used if _is_generic is True
  _is_intermediate: ClassVar[bool] = False
  _generic_name: ClassVar[str] = '' # Only used if _father_is_generic is True
  _cls: Any = None

  _father_is_abstract_base_class: ClassVar[bool] = False
  _father_needs_subclassing: ClassVar[bool] = False
  _father_is_generic: ClassVar[bool] = False
  _father_number_of_non_default_type_params: int = 0
  _father_is_intermediate: ClassVar[bool] = False
  _father_cls: Any = None

  _debug_group: ClassVar[MyDebugGroup] = NONE_DEBUG_GROUP
  #endregion Model Config + Class Variables


  #region Instance Fields + Properties
  #endregion Instance Fields + Properties


  #region Init Subclass + Abstract Methods
  @override
  def __init_subclass__(cls, **kwargs: Any) -> None:
    cls._debug_group = MyDebugManager.new_group(f'Initializing subclass {cls.__name__}',
                                                '__moredantic_dg__')
    # Get the values from the father class before setting the values for the current class
    # We'll need this info later
    cls._father_is_abstract_base_class = cls._is_abstract_base_class
    cls._father_needs_subclassing = cls._needs_subclassing
    cls._father_is_generic = cls._is_generic
    cls._father_number_of_non_default_type_params = cls._number_of_non_default_type_params
    cls._father_is_intermediate = cls._is_intermediate
    cls._father_cls = cls._cls
    cls._cls = cls

    # Apply the config for this class, if it exists, otherwise apply the default config
    if 'model_self_config' in cls.__dict__:
      config = cls.__dict__['model_self_config']
      cls._debug_group.print(f'Found model_self_config in class definition, applying config: '
                             f'{config}')
      for config_name, config_default in DEFAULT_BASE_CLASS_MODEL_SELF_CONFIG.items():
        setattr(cls, f'_{config_name}', config.get(config_name, config_default))
      delattr(cls, 'model_self_config')
    else:
      cls._debug_group.print(f'No model_self_config found in class definition, applying default '
                             f'config: {DEFAULT_BASE_CLASS_MODEL_SELF_CONFIG}')
      for config_name, config_default in DEFAULT_BASE_CLASS_MODEL_SELF_CONFIG.items():
        setattr(cls, f'_{config_name}', config_default)

    super().__init_subclass__(**kwargs)

    # When and only when the subclass has new generic types and didn't explicitly set the
    # generic types of it's parent, pydantic is not able to deal with it properly. This is the fix!
    pydantic_metadata = getattr(cls, '__pydantic_generic_metadata__', {}).copy()
    type_params = getattr(cls, '__type_params__', None)
    if pydantic_metadata.get('parameters', None) and type_params:
      final_args = ()
      final_params = ()
      for param in pydantic_metadata['parameters']:
        if param.__default__ is NoDefault:
          final_params += (param, )
        else:
          final_args += (param.__default__, )

      pydantic_metadata['args'] = final_args
      pydantic_metadata['origin'] = cls._father_cls
      pydantic_metadata['parameters'] = final_params
      if final_args:
        cls.__orig_bases__ = (cls._father_cls[final_args], *cls.__orig_bases__[-len(type_params):]) # pyright: ignore[reportUnknownMemberType]
      cls.__pydantic_generic_metadata__ = pydantic_metadata


    # Somes checks and info saving are needed
    if cls._not_typed_from_generic_father():
      msg = (f'Cannot create subclass from generic class {cls._generic_name} '
             f'with unbound type variables')
      raise TypeError(msg)

    cls._save_generic_types()
    cls.is_instantiatable = cls._am_i_instantiatable()
    cls._debug_group.end()
  #endregion Init Subclass + Abstract Methods


  #region Class + Static Methods
  #region _Internal Helper Methods
  @classmethod
  def _am_i_generic(cls) -> bool:
    return bool(getattr(cls, '__parameters__', None))


  @classmethod
  def _not_typed_from_generic_father(cls) -> bool:
    cls._debug_group.print('Checking if ', cls.__name__, ' is not typed from generic')
    cls._debug_group.print('args: ', get_args(cls))
    cls._debug_group.print('parameters: ', getattr(cls, '__parameters__', None))
    cls._debug_group.print('type_params: ', getattr(cls, '__type_params__', None))
    cls._debug_group.print('origins: ', getattr(cls, '__orig_bases__', None))
    cls._debug_group.print('__pydantic_generic_metadata__: ',
                           getattr(cls, '__pydantic_generic_metadata__', None))

    if not cls._number_of_non_default_type_params:
      return False

    regex_params = ', '.join(['.+' for _ in range(cls._number_of_non_default_type_params)])
    pattern = re.compile(f'^{cls._generic_name}\\[{regex_params}\\]$')
    cls._debug_group.print('Checking if class name matches pattern: ', pattern.pattern)

    return not pattern.match(cls.__name__)


  # Verify that all type variables are bound
  @classmethod
  def _am_i_instantiatable(cls) -> bool:
    cls._number_of_non_default_type_params = 0
    if cls._am_i_generic():
      cls._debug_group.print("It's generic, not instantiatable")
      cls._is_generic = True
      for tp in cls.__type_params__:
        if tp.__default__ is NoDefault:
          cls._number_of_non_default_type_params += 1
        else:
          break

      cls._debug_group.print('Number of non default type parameters: ',
                             cls._number_of_non_default_type_params)
      cls._generic_name = cls.__name__
      return False

    cls._is_generic = False

    if cls._is_abstract_base_class:
      cls._debug_group.print("It's an abstract base model, not instantiatable")
      return False

    if cls._father_needs_subclassing:
      if cls._father_is_generic:
        cls._debug_group.print("Needs subclassing, I'm just the intermediary, not instantiatable")
        return False

      msg = f'Class {cls.__name__} needs subclassing but is not marked as generic nor from generic'
      raise TypeError(msg)

    cls._debug_group.print("It's not base nor generic nor intermediate, therefore instantiatable!")
    return True


  @classmethod
  def _save_generic_types_converting_typealiastype(
    cls,
    new_generics: Sequence[type | TypeAliasType]
  ) -> None:
    final_generics: list[type] = []
    for generic in new_generics:
      if isinstance(generic, TypeAliasType):
        final_generics.append(generic.__value__)
      else:
        final_generics.append(generic)
    cls.generic_types = tuple(final_generics)


  @classmethod
  def _save_generic_types(cls) -> None:
    metadata = getattr(cls, '__pydantic_generic_metadata__', None)
    if cls._father_is_generic and (not metadata or metadata.get('parameters', None)):
      # WORKARROUND:
      # If class is directly from a generic (Ex: LiteralFieldsModel[Literal["a", "b"]]) metadata
      # does not contain args. Around the code I might call this the "intermediate" class, and then
      # call "subclass" to the final class that binds the type variables
      # (Ex: MyLiteralFieldsModel(LiteralFieldsModel[Literal["a", "b"]])).
      # If it's already the subclass, metadata will contain the correct args, hence the else branch.
      # There might be a better way to do this, but after trying several things this was the only
      # that worked in all situations.
      # WORKARROUND LOGIC:
      # Since I cound not find a way to get the args from the intermediate class, I create a method
      # that is able to get them when creating an instance (I found a way to get them from there),
      # and save them in a class variable so I can use them later.
      # This only runs for the first instance created from the intermediate class to save time.
      # See __init__ methods in BaseModel and RootModel.
      cls._is_intermediate = True
      cls.generic_types = ()
    else:
      cls._is_intermediate = False
      if not metadata:
        cls.generic_types = ()
      else:
        cls._save_generic_types_converting_typealiastype(metadata['args'])
        cls._debug_group.print('-> Saved generic types for', cls.__name__,
                               'from __pydantic_generic_metadata__:',
                               cls.generic_types, ' <-')
        cls._after_generic_types_populated()
  #endregion _Internal Helper Methods

  #region Normal Methods
  @classmethod
  def _after_generic_types_populated(cls) -> None:
    # Placeholder for child classes to implement any logic needed if needed
    # It's supposed to not be abstract method and to not implement anything here
    pass
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Class + Static Methods


  #region New + Init + Post Init + Validators Methods
  #endregion New + Init + Post Init + Validators Methods


  #region Instance Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Instance Methods

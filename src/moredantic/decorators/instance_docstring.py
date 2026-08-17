"""InstanceDocstring decorator module."""

# ---> Standard library imports <--- #
from collections.abc import Callable
from typing import Any, override

# ---> First party imports <--- #
from chatbot_app import MyDebugManager
from chatbot_app.utils.strings import safe_format

# ---> Local imports <--- #
from .base_decorator import base_decorator


# General idea: we create an instance of the instance_docstring decorator per instance of the class
# The decorator's __get__ method is called when the method is accessed via the class instance
# In the __get__, we format the docstring using the instance's attributes, set it to the method,
# set the updated method back to the instance method name (thus removing the instance_docstring
# instance), and return it
# This way, the docstring is updated per instance dynamically, only once and cached, and the
# instance_docstring instance is no longer stored in the instance
class instance_docstring(base_decorator):  # noqa: N801
  """
  Decorator to dynamically create the docstring of an instance method based on it's attributes.

  This decorator is designed to be used on instance methods of classes that have attributes that can
  be used to format the docstring and therefore provide more context and information about the
  method's behavior based on the instance's properties.
  """
  #region Model Config + Class Variables
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
  def __init__(self, func: Callable[..., Any]) -> None:
    super().__init__(func)
    self._original_doc = func.__doc__ or ''
  #endregion New + Init + Post Init + Validators Methods


  #region Instance Methods
  #region _Internal Helper Methods
  @override
  def __get__(self, instance: object, instance_cls: type) -> Callable[..., Any]:
    wrapped = super().__get__(instance, instance_cls)
    if instance is None: # Accessed via class
      return wrapped

    dg = MyDebugManager.new_group(
      f'Creating instance docstring for methood {self.func.__name__} of class {instance_cls.__name__}.',  # noqa: E501
      '__instance_docstring_creation_dg__'
    )
    wrapped.__doc__ = safe_format(self._original_doc,
                                  instance.model_dump(), # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]
                                  mode = '***',
                                  validate_extra_keys = False,
                                  debug_group = dg)
    # Since the models can be frozen, we set directly in __dict__
    instance.__dict__[self.func.__name__] = wrapped
    dg.end()
    return wrapped
  #endregion _Internal Helper Methods

  #region Normal Methods
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Instance Methods

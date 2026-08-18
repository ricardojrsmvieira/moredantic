"""Base decorator module."""

# ---> Standard library imports <--- #
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class base_decorator(ABC):  # noqa: N801
  """Base decorator class for all decorators in the package."""
  #region Model Config + Class Variables
  #endregion Model Config + Class Variables


  #region Instance Fields + Properties
  #endregion Instance Fields + Properties


  #region Init Subclass + Abstract Methods
  @abstractmethod
  def __init__(self, func: Callable[..., Any]) -> None:
    self.func = func


  @abstractmethod
  def __get__(self, instance: object, _class: type) -> Callable[..., Any]:
    """Return the wrapped method with the docstring updated with the instance context."""
    if instance is None: # Accessed via class
      return self.func

    def wrapped(*args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
      return self.func(instance, *args, **kwargs)

    return wrapped
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
  #endregion New + Init + Post Init + Validators Methods


  #region Instance Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Instance Methods

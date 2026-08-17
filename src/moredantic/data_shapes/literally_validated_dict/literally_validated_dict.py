"""Literally Validated Dict module."""

# ---> Standard library imports <--- #
from collections.abc import ItemsView
from typing import Literal, Self, get_args, get_origin

# ---> Third party imports <--- #
from pydantic import model_validator

# ---> First party imports <--- #
from chatbot_app.mydantic.base_models import RootArbitraryModel


class LiterallyValidatedDict[keysT: str, valuesT](RootArbitraryModel[dict[keysT, valuesT]]):
  """
  A dictionary that is validated to have ALL AND ONLY the keys defined in the generic type.

  Note that this will not return an actual dict, but rather a pydantic model with a root field
  that is a dict.
  """
  #region Model Config + Class Variables
  model_config = RootArbitraryModel.model_config | { 'arbitrary_types_allowed': True }
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
  @model_validator(mode='after')
  def validate_keys_from_generic_type(self) -> Self:
    """Validate that the keys of the dict are exactly the keys defined in the generic type."""
    # Next line only worked for instances created directly from the generic class, not subclasses
    # key_type = self.__pydantic_generic_metadata__["args"][0]  # noqa: ERA001
    # This worked but after I had to save generic_types in BaseModel so might as well use it here
    # key_type = get_args(type(self).model_fields['root'].annotation)[0]  # noqa: ERA001
    # Final solution: use the saved generic_types from BaseModel
    key_type = type(self).generic_types[0]

    if get_origin(key_type) is not Literal:
      msg = 'Key type is not a Literal'
      raise TypeError(msg)

    generic_defined_keys: set[keysT] = set(get_args(key_type))
    actual_dict_keys: set[keysT] = set(self.root.keys())
    missing_keys = generic_defined_keys - actual_dict_keys
    # Check for extra keys is not needed as we already define that the dict has keysT keys only
    if missing_keys:
      msg = f'Missing keys: {missing_keys}'
      raise ValueError(msg)
    return self
  #endregion New + Init + Post Init + Validators Methods


  #region Instance Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  # Methods defined because type checkers can't infer them properly ->
  def __getitem__(self, key: keysT) -> valuesT:
    """Get the value associated with the given key."""
    return self.root[key]

  def items(self) -> ItemsView[keysT, valuesT]:
    """Return a set-like object providing a view on the dictionary's items."""
    return self.root.items()
  # <- Methods defined because type checkers can't infer them properly
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Instance Methods

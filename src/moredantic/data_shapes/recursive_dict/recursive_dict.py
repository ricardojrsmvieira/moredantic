"""Recursive Dict base class."""

# ---> Standard library imports <--- #
from collections.abc import Iterator
from functools import cached_property
from typing import ClassVar, Never, is_typeddict, override

# ---> First party imports <--- #
from chatbot_app.mydantic.base_models import RootModel


class RecursiveDictBaseClass[
  keyT, # Must be the first [0] generic type
  leafT, # Must be the second [1] generic type
  rootValueT, # selfT | leafT, preferentially with a Discriminator if some is not a base type
](RootModel[dict[keyT, rootValueT]]):
  """Base class for recursive dicts."""
  #region Model Config + Class Variables
  _key_type: ClassVar[type]
  _leaf_type: ClassVar[type]
  #endregion Model Config + Class Variables


  #region Instance Fields + Properties
  @cached_property
  def leafs(self) -> list[leafT]:
    """Returns a list of all leaf values in the recursive dict."""
    my_leafs: list[leafT] = []
    for branch in self.values():
      if isinstance(branch, type(self)._leaf_type):  # noqa: SLF001
        my_leafs.append(branch) # pyright: ignore[reportArgumentType]
      elif isinstance(branch, type(self)):
        my_leafs.extend(branch.leafs)
    return my_leafs


  @cached_property
  def max_depth(self) -> int:
    """Returns the maximum depth of the recursive dict."""
    current_max = 0 # if only has leaf children
    for branch in self.values():
      if isinstance(branch, type(self)):
        depth = branch.max_depth
        current_max = max(current_max, depth)
    return current_max + 1


  @cached_property
  def num_leafs(self) -> int:
    """Returns the number of leaf values in the recursive dict."""
    return len(self.leafs)
  #endregion Instance Fields + Properties


  #region Init Subclass + Abstract Methods
  #endregion Init Subclass + Abstract Methods


  #region Class + Static Methods
  #region _Internal Helper Methods
  @override
  @classmethod
  def _after_generic_types_populated(cls) -> None:
    if cls.__name__ == 'RecursiveDictBaseClass':
      return

    my_types = cls.generic_types
    cls._key_type = my_types[0]
    if is_typeddict(my_types[1]):
      cls._leaf_type = dict
    else:
      cls._leaf_type = my_types[1]
  #endregion _Internal Helper Methods


  #region Normal Methods
  def iter_over_depthness(
      self,
      depth: int,
      current_depth: int = 0
    ) -> Iterator[tuple[int, keyT, rootValueT]]:
    """Iterate over the recursive dict up to a specified depth."""
    if depth < 0:
      msg = 'Depth must be non-negative'
      raise ValueError(msg)
    if current_depth > depth:
      return
    if current_depth == depth:
      yield from ((current_depth, key, branch) for key, branch in self.items())
      return
    for name, branch in self.items():
      if isinstance(branch, type(self)):
        yield from branch.iter_over_depthness(depth, current_depth + 1)
      elif isinstance(branch, type(self)._leaf_type):  # noqa: SLF001
        yield current_depth, name, branch
      else:
        msg = (f'Somehow a non-leaf/non-RecursiveDict branch exists in RecursiveDict. '
               f'Got type: {type(branch)}')
        raise TypeError(msg)
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Class + Static Methods


  #region New + Init + Post Init + Validators Methods
  # We need To define **kwargs because recursivly Pydantic models/Discriminators pass all keys as
  # kwargs instead of a single dict that was deconstructed (when we define the recursive dict as a
  # dict of dicts)
  # This way typecheckers will warn us if we pass more than just the root (as intended)
  # but at runtime we can merge both and the recursion works as intended
  def __init__(self, root: rootValueT | None = None, **kwargs: Never) -> None:
    real_root = root if root is not None else kwargs
    super().__init__(real_root) # pyright: ignore[reportArgumentType]
  #endregion New + Init + Post Init + Validators Methods


  #region Instance Methods
  #region _Internal Helper Methods
  #endregion _Internal Helper Methods

  #region Normal Methods
  # Methods defined because type checkers can't infer them properly ->
  def __getitem__(self, key: keyT) -> rootValueT:
    """Get the value associated with the given key."""
    return self.root[key]

  def __setitem__(self, key: keyT, value: rootValueT) -> None:
    """Set the value associated with the given key."""
    self.root[key] = value

  def items(self) -> list[tuple[keyT, rootValueT]]:
    """Return a list of the dictionary's items."""
    return list(self.root.items())

  def values(self) -> list[rootValueT]:
    """Return a list of the dictionary's values."""
    return list(self.root.values())
  # <- Methods defined because type checkers can't infer them properly
  #endregion Normal Methods

  #region Custom Tool Methods
  #endregion Custom Tool Methods
  #endregion Instance Methods

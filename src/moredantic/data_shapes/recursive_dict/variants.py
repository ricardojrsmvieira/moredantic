"""Variants module of Recursive Dict."""

# ---> Local imports <--- #
from .recursive_dict import RecursiveDictBaseClass


class RecursiveDictStr(RecursiveDictBaseClass[
  # "RecursiveDictStr", # selfT
  str, # keyT
  str, # leafT
  'RecursiveDictStr | str', # selfT | leafT
]):
  """Recursive Dict with str keys and str leaf values."""

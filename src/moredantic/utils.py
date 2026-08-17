# ---> Standard library imports <--- #
import json
import re
from typing import Any, Literal

# ---> Third party imports <--- #
from pydantic import BaseModel

# ---> First party imports <--- #
from moredantic import _MyDebugGroup as MyDebugGroup  # pyright: ignore[reportPrivateUsage]

# ---> Local imports <--- #
from .regex import call_dict_key_regex


def obj_to_pretty_str(
  obj: dict[Any, Any] | list[Any] | BaseModel,
  indent: int = 2,
  separators: tuple[str, str] = (',', ': _VALUE_')
) -> str:
  """
  Convert a Python object (dict, list, or Pydantic BaseModel) to a pretty-printed JSON string.

  Parameters
  ----------
  obj : dict[Any, Any] | list[Any] | BaseModel
      The object to convert to a JSON string.
  indent : int, default 2
      The number of spaces to use for indentation.
  separators : tuple[str, str], default (',', ': _VALUE_')
      The separators to use for items and key-value pairs.

  Returns
  -------
  str :
      The pretty-printed JSON string.
  """
  if isinstance(obj, BaseModel):
    obj = obj.model_dump()

  return json.dumps(obj, indent = indent, separators = separators, default = str)


type WrapperModeType = Literal['***'] | None
def _get_wrapper_regex(mode: WrapperModeType) -> str:
  """
  Get the regex pattern for the specified formatting mode.

  Parameters
  ----------
  mode : WrapperModeType
      The formatting mode to use.

  Returns
  -------
  str :
      The regex pattern for the specified mode.
  """
  if mode is None:
    return r'\{(.*?)\}'
  if mode == '***':
    return r'\*\*\*(.*?)\*\*\*'

  msg = f'Unsupported mode: {mode}' # pyright: ignore[reportUnreachable] # It is if the typing is respected. Here just for safety.
  raise ValueError(msg)


# README/TODO: It can receive more than strings at the end.
# One example is lists or integers, but with str(value) conversion it should be fine.
# Anyway, not perfectly typed right now.
type SubstitutionsType = dict[str, str | SubstitutionsType]
def safe_format(
  text: str,
  substitutions: SubstitutionsType,
  mode: WrapperModeType = None,
  *,
  validate_extra_keys: bool = True,
  debug_group: MyDebugGroup | None = None
) -> str:
  """
  Safely format a string with the provided substitutions, supporting different formatting modes.

  Parameters
  ----------
  text : str
      The string to format.
  substitutions : dict[str, str | SubstitutionsType]
      A dictionary containing the substitutions to apply to the string.
  mode : WrapperModeType, default None
      The formatting mode to use.
      If None, it will use the standard Python string formatting (e.g., '{key}').
  validate_extra_keys : bool, default True
      If True, the function will raise an error if there are extra keys in the substitutions
      dictionary that are not used in the text.
  debug_group : DebugGroup | None, optional
      An optional DebugGroup instance for logging debug information.

  Returns
  -------
  str :
      The formatted string with the substitutions applied.
  """
  if debug_group is not None:
    debug_group.print(f'Safe_format called with text:|BG|{text}|EG|\n'
                      f'And substitutions:|BG|{obj_to_pretty_str(substitutions)}|EG|')

  wrapper_regex = _get_wrapper_regex(mode)

  keys_to_replace = re.findall(wrapper_regex, text)
  keys_received = substitutions.keys()
  missing_keys = [key for key in keys_to_replace if key not in keys_received]
  for missing_key in missing_keys:
    dict_calling = re.fullmatch(call_dict_key_regex, missing_key)
    if dict_calling:
      dict_name = dict_calling.group(1)
      sub_key = dict_calling.group(3)
      if (
        dict_name in substitutions
        and isinstance(substitutions[dict_name], dict)
        and sub_key in substitutions[dict_name]
      ):
        missing_keys.remove(missing_key)
        keys_to_replace.remove(missing_key)
        text = text.replace(f'***{missing_key}***', str(substitutions[dict_name][sub_key])) # pyright: ignore[reportArgumentType]
  if missing_keys:
    msg = f'Missing keys for formatting: {missing_keys}'
    raise ValueError(msg)
  if validate_extra_keys:
    extra_keys = [key for key in keys_received if key not in keys_to_replace]
    if extra_keys:
      msg = f'Extra keys provided for formatting: {extra_keys}'
      raise ValueError(msg)

  if mode == '***':
    for key in keys_to_replace:
      text = text.replace(f'***{key}***', str(substitutions[key]))
  else: # mode is None
    text = text.format(**substitutions)

  return text

"""MyDebugGroup module."""

# ---> Third party imports <--- #
from debug_group import DebugManager


if DebugManager._instance is None: # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
  print('WARNING: DebugManager is not initialized. Moredantic will initialize DebugManager with'  # noqa: T201
        'default settings. If you want to customize DebugManager settings, please initialize'
        'DebugManager before importing Moredantic. If you do not do so, no debug prints will'
        'be shown, neither for moredantic nor for any other package or your own code.')
  MyDebugManager = DebugManager({})
else:
  MyDebugManager = DebugManager._instance # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
MyDebugGroup = MyDebugManager.MyDebugGroup
NONE_DEBUG_GROUP = MyDebugManager.NONE_DEBUG_GROUP

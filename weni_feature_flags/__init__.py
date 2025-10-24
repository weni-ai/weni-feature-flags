# Backward compatibility package for weni_feature_flags
# This package redirects all imports to the new weni.feature_flags namespace

import sys
import pkgutil
from importlib import import_module

# Store reference to the new module
_new_module = import_module("weni.feature_flags")

# Make all attributes from the new module available at this package level
for attr_name in dir(_new_module):
    if not attr_name.startswith("_"):
        setattr(sys.modules[__name__], attr_name, getattr(_new_module, attr_name))


# Automatically discover and forward all submodules
def __getattr__(name):
    """
    Handle dynamic imports for any submodule automatically:
    - from weni_feature_flags.services import FeatureFlagsService
    - from weni_feature_flags.models import FeatureFlagSnapshot
    - from weni_feature_flags.integrations.growthbook.clients import GrowthBookClient
    """
    try:
        # Try to import the submodule from the new namespace
        submodule_name = f"weni.feature_flags.{name}"
        submodule = import_module(submodule_name)
        return submodule
    except ImportError:
        # If the submodule doesn't exist, raise AttributeError
        raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Dynamically build __all__ by discovering all submodules
def _discover_submodules():
    """Discover all submodules in the new namespace package"""
    submodules = []
    try:
        for importer, modname, ispkg in pkgutil.walk_packages(
            _new_module.__path__, _new_module.__name__ + "."
        ):
            # Extract just the submodule name (e.g., 'services' from 'weni.feature_flags.services')
            submodule_name = modname.split(".")[-1]
            if submodule_name not in submodules:
                submodules.append(submodule_name)
    except (AttributeError, ImportError):
        # Fallback if discovery fails
        pass
    return submodules


# Set __all__ dynamically
__all__ = _discover_submodules()

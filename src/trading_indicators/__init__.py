from trading_indicators.base import Indicator
from trading_indicators.registry import discover_plugins, get, list_indicators, register

# Import built-ins so they register on first import of the package
import trading_indicators.builtin  # noqa: F401

__all__ = ["Indicator", "register", "get", "list_indicators", "discover_plugins"]

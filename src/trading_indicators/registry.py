import importlib
import importlib.util
import pathlib

_registry: dict = {}


def register(cls):
    """Decorator that registers an Indicator subclass by its name."""
    _registry[cls.name] = cls
    return cls


def get(name: str):
    """Look up a registered indicator by name and return an instance."""
    if name not in _registry:
        raise KeyError(f"Indicator '{name}' not found. Available: {list(_registry.keys())}")
    return _registry[name]()


def list_indicators() -> list[str]:
    """Return sorted list of all registered indicator names."""
    return sorted(_registry.keys())


def discover_plugins(path: str) -> None:
    """Scan a directory for .py files and import them to trigger registration."""
    plugin_dir = pathlib.Path(path)
    if not plugin_dir.is_dir():
        raise FileNotFoundError(f"Plugin directory not found: {path}")

    for py_file in plugin_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
        module_name = f"trading_indicators_plugin_{py_file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

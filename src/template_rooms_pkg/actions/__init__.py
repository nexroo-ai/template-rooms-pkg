import importlib
from pathlib import Path

def _discover_actions():
    """Dynamically discover and import all action functions."""
    actions_dir = Path(__file__).parent
    actions = {}
    
    for file_path in actions_dir.glob("*.py"):
        if file_path.name not in ["__init__.py", "base.py"]:
            module_name = file_path.stem
            try:
                module = importlib.import_module(f".{module_name}", package=__name__)
                # Only import function with same name as file
                if hasattr(module, module_name):
                    action_func = getattr(module, module_name)
                    if callable(action_func):
                        actions[module_name] = action_func
            except ImportError:
                pass
    
    return actions

def __getattr__(name: str):
    """Dynamically import actions on demand."""
    actions_dir = Path(__file__).parent
    action_file = actions_dir / f"{name}.py"
    
    if action_file.exists():
        try:
            module = importlib.import_module(f".{name}", package=__name__)
            if hasattr(module, name):
                return getattr(module, name)
        except ImportError:
            pass
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

def __dir__():
    """Show all available actions when using dir()."""
    actions_dir = Path(__file__).parent
    return [f.stem for f in actions_dir.glob("*.py") 
            if f.name not in ["__init__.py", "base.py"]]

# Auto-discover and make available for import
_actions = _discover_actions()
globals().update(_actions)
__all__ = list(_actions.keys())
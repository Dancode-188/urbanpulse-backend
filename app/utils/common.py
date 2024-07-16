import re
from datetime import datetime, timezone
from typing import Any, Dict

def validate_email(email: str) -> bool:
    """Validate an email address."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def to_camel(string: str) -> str:
    """Convert snake_case to camelCase."""
    components = string.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def to_snake(string: str) -> str:
    """Convert camelCase to snake_case."""
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', string).lower()

def utc_now() -> datetime:
    """Return current UTC time."""
    return datetime.now(timezone.utc)

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flatten a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def truncate_string(s: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate a string to a maximum length."""
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix
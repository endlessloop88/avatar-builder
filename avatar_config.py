"""Reading and validating the avatar config.

Pure helpers with no python-avatars import, so they are easy to test.
"""
import json
import re
from pathlib import Path

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")
PARTS = ("top", "eyebrows", "eyes", "nose", "mouth", "facial_hair", "accessory", "clothing")
COLORS = ("skin_color", "hair_color", "facial_hair_color", "clothing_color", "background_color")


class ConfigError(ValueError):
    """The config file is missing something or contains an invalid value."""


def load_config(path):
    """Read a JSON config file and return it validated and normalised."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ConfigError(f"config file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ConfigError(f"config file is not valid JSON: {error}") from error
    return validate_config(data)


def validate_config(data):
    """Check the structure and return {'parts': {name: [candidates]}, 'colors': {...}}."""
    parts = data.get("parts")
    if not isinstance(parts, dict):
        raise ConfigError("'parts' must be an object")

    missing = [part for part in PARTS if part not in parts]
    if missing:
        raise ConfigError(f"missing parts: {', '.join(missing)}")
    unknown = [part for part in parts if part not in PARTS]
    if unknown:
        raise ConfigError(f"unknown parts: {', '.join(unknown)}")

    normalised = {}
    for name, value in parts.items():
        candidates = [value] if isinstance(value, str) else value
        if not isinstance(candidates, list) or not candidates or not all(isinstance(c, str) for c in candidates):
            raise ConfigError(f"'{name}' needs a name or a non-empty list of names")
        normalised[name] = candidates

    colors = data.get("colors", {})
    for key, value in colors.items():
        if key not in COLORS:
            raise ConfigError(f"unknown colour '{key}'")
        if not isinstance(value, str) or not HEX_COLOR.match(value):
            raise ConfigError(f"'{key}' must be a hex colour such as #AABBCC")

    return {"parts": normalised, "colors": dict(colors)}


def first_available(options, candidates):
    """Return (name, value) of the first candidate that exists on `options`, else (None, None)."""
    for name in candidates:
        value = getattr(options, name, None)
        if value is not None:
            return name, value
    return None, None

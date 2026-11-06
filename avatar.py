"""Build a personalised SVG avatar from a JSON config, using python-avatars.

Usage:
    python avatar.py                      # reads avatar.json, writes avatar.svg
    python avatar.py --config my.json --out me.svg
    python avatar.py --list               # show every part name you can use
"""
import argparse
import sys

import python_avatars as pa

from avatar_config import ConfigError, first_available, load_config

PART_TYPES = {
    "top": pa.HairType,
    "eyebrows": pa.EyebrowType,
    "eyes": pa.EyeType,
    "nose": pa.NoseType,
    "mouth": pa.MouthType,
    "facial_hair": pa.FacialHairType,
    "accessory": pa.AccessoryType,
    "clothing": pa.ClothingType,
}


def list_options():
    """Print every available name for each part."""
    for part, options in PART_TYPES.items():
        print(f"{part}: " + ", ".join(member.name for member in options))
    print("hat (use instead of top): " + ", ".join(member.name for member in pa.HatType))


def build_avatar(config):
    """Create an Avatar. For each part, the first candidate name that exists is used."""
    chosen = {}
    for part, candidates in config["parts"].items():
        name, value = first_available(PART_TYPES[part], candidates)
        if value is None:
            valid = ", ".join(member.name for member in PART_TYPES[part])
            raise ConfigError(f"{part}: none of {candidates} exist. Valid names: {valid}")
        print(f"{part}: {name}")
        chosen[part] = value
    return pa.Avatar(style=pa.AvatarStyle.CIRCLE, **chosen, **config["colors"])


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build a personalised SVG avatar from a JSON config.")
    parser.add_argument("--config", default="avatar.json", help="config file (default: avatar.json)")
    parser.add_argument("--out", default="avatar.svg", help="output file (default: avatar.svg)")
    parser.add_argument("--list", action="store_true", help="list all available part names and exit")
    args = parser.parse_args(argv)

    if args.list:
        list_options()
        return 0
    try:
        avatar = build_avatar(load_config(args.config))
    except ConfigError as error:
        print(f"Config error: {error}", file=sys.stderr)
        return 1
    avatar.render(args.out)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

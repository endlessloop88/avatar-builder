# avatar-builder

Build a personalised SVG avatar from a JSON file. A small layer on top of
[python-avatars](https://github.com/ibonn/python_avatars) that adds a config file, validation,
fallback names and unit tests.

![Example avatar](examples/avatar.png)

## Why

`python-avatars` expects enum objects in code. This project moves the choices into
`avatar.json`, so changing a hairstyle or a colour is a one-line edit, and a typo gives a clear error
instead of a stack trace.

## Install and run

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows. On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python avatar.py --list         # every part name you can use
python avatar.py                # reads avatar.json, writes avatar.svg
python avatar.py --config my.json --out me.svg
```

## Config

```json
{
  "parts": {
    "top": ["SHORT_WAVED", "SHORT_FLAT"],
    "facial_hair": ["NONE"]
  },
  "colors": { "skin_color": "#F1C6A0", "hair_color": "#2A1A14" }
}
```

- Every part (`top`, `eyebrows`, `eyes`, `nose`, `mouth`, `facial_hair`, `accessory`, `clothing`)
  takes one name or a list. With a list, the first name that exists in the installed library wins, and
  the chosen name is printed.
- Colours are hex codes. Allowed keys: `skin_color`, `hair_color`, `facial_hair_color`,
  `clothing_color`, `background_color`.
- See `avatar.json` for a complete example.

## Project layout

| File | Purpose |
| --- | --- |
| `avatar_config.py` | Loads and validates the config. Pure functions, no `python-avatars` import. |
| `avatar.py` | Command line entry point that builds and renders the avatar. |
| `tests/test_config.py` | 14 unit tests for the config code. |

## Tests

```bash
python -m unittest
```

The tests cover config validation only, so they need no network and no extra packages.

## Notes

- Written with AI-assisted tooling. I chose the structure and the config format, then ran, reviewed and
  tested it myself.
- The example avatar is a stylised cartoon, not a likeness.
- Part names come from `python-avatars` 1.4.1, which is pinned in `requirements.txt`. Other versions may
  name parts differently, which is why the fallback lists exist.

## Credits and licence

- Code: MIT, see `LICENSE`.
- [python-avatars](https://github.com/ibonn/python_avatars) is MIT licensed. Its artwork was designed by
  [Pablo Stanley](https://avataaars.com/). Check the artwork's terms before using avatars commercially.

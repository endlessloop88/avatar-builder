import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from avatar_config import ConfigError, first_available, load_config, validate_config

VALID = {
    "parts": {
        "top": ["SHORT_WAVED", "SHORT_FLAT"],
        "eyebrows": "DEFAULT_NATURAL",
        "eyes": "DEFAULT",
        "nose": "DEFAULT",
        "mouth": ["SERIOUS"],
        "facial_hair": "NONE",
        "accessory": "NONE",
        "clothing": "HOODIE",
    },
    "colors": {"skin_color": "#F1C6A0", "hair_color": "#2A1A14"},
}


def copy_of_valid():
    return json.loads(json.dumps(VALID))


class ValidateConfigTests(unittest.TestCase):
    def test_valid_config_is_normalised(self):
        config = validate_config(copy_of_valid())
        self.assertEqual(config["parts"]["eyes"], ["DEFAULT"])  # a single name becomes a list
        self.assertEqual(config["parts"]["top"], ["SHORT_WAVED", "SHORT_FLAT"])
        self.assertEqual(config["colors"]["skin_color"], "#F1C6A0")

    def test_colors_are_optional(self):
        data = copy_of_valid()
        del data["colors"]
        self.assertEqual(validate_config(data)["colors"], {})

    def test_missing_part_is_rejected(self):
        data = copy_of_valid()
        del data["parts"]["nose"]
        with self.assertRaisesRegex(ConfigError, "missing parts: nose"):
            validate_config(data)

    def test_unknown_part_is_rejected(self):
        data = copy_of_valid()
        data["parts"]["cape"] = "RED"
        with self.assertRaisesRegex(ConfigError, "unknown parts: cape"):
            validate_config(data)

    def test_empty_candidate_list_is_rejected(self):
        data = copy_of_valid()
        data["parts"]["eyes"] = []
        with self.assertRaisesRegex(ConfigError, "eyes"):
            validate_config(data)

    def test_bad_hex_colours_are_rejected(self):
        for bad in ["red", "#FFF", "#GGGGGG", "F1C6A0", 123]:
            with self.subTest(bad=bad):
                data = copy_of_valid()
                data["colors"]["skin_color"] = bad
                with self.assertRaisesRegex(ConfigError, "skin_color"):
                    validate_config(data)

    def test_unknown_colour_key_is_rejected(self):
        data = copy_of_valid()
        data["colors"]["eye_color"] = "#000000"
        with self.assertRaisesRegex(ConfigError, "unknown colour"):
            validate_config(data)

    def test_parts_must_be_an_object(self):
        with self.assertRaisesRegex(ConfigError, "'parts' must be an object"):
            validate_config({"parts": []})


class LoadConfigTests(unittest.TestCase):
    def test_reads_a_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "avatar.json"
            path.write_text(json.dumps(VALID), encoding="utf-8")
            self.assertEqual(load_config(path)["parts"]["clothing"], ["HOODIE"])

    def test_reports_missing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ConfigError, "not found"):
                load_config(Path(folder) / "nope.json")

    def test_reports_invalid_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "avatar.json"
            path.write_text("{ not json", encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "not valid JSON"):
                load_config(path)

    def test_shipped_example_config_is_valid(self):
        example = Path(__file__).resolve().parent.parent / "avatar.json"
        self.assertEqual(set(load_config(example)["parts"]), set(VALID["parts"]))


class FirstAvailableTests(unittest.TestCase):
    def test_prefers_the_first_existing_name(self):
        options = SimpleNamespace(B="b-value", C="c-value")
        self.assertEqual(first_available(options, ["A", "B", "C"]), ("B", "b-value"))

    def test_returns_none_when_nothing_matches(self):
        self.assertEqual(first_available(SimpleNamespace(A=1), ["X", "Y"]), (None, None))


if __name__ == "__main__":
    unittest.main()

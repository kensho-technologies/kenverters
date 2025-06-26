import json
import os
from typing import Any, ClassVar
from unittest import TestCase

from ..convert_output_visual_formatted import convert_output_to_str_formatted

OUTPUT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "extract_output.json"
)
EXPECTED_TXT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "visually_converted_output.txt"
)
EXPECTED_RESIZED_TXT_FILE_PATH = os.path.join(
    os.path.dirname(__file__), "data", "visually_converted_resized_output.txt"
)


class TestVisuallyFormattedText(TestCase):
    extract_output: ClassVar[dict[str, Any]]
    expected_converted_text: ClassVar[str]

    @classmethod
    def setUpClass(cls) -> None:
        with open(OUTPUT_FILE_PATH, "r") as f:
            cls.extract_output = json.load(f)
        with open(EXPECTED_TXT_FILE_PATH, "r") as f:
            cls.expected_converted_text = f.read()

    def test_convert_output_to_str_formatted(self) -> None:
        converted_text = convert_output_to_str_formatted(self.extract_output)
        self.assertEqual(converted_text[0], self.expected_converted_text)

    def test_convert_output_to_str_formatted_too_small(self) -> None:
        # Test that words are cut off if we force it to be too small
        converted_text = convert_output_to_str_formatted(
            self.extract_output, page_height=100, page_width=450, resize=False
        )
        self.assertNotEqual(converted_text[0], self.expected_converted_text)

    def test_convert_output_to_str_formatted_too_small_resize(self) -> None:
        # Test that words are not cut off if too small but we allow resize
        converted_text = convert_output_to_str_formatted(
            self.extract_output, page_height=100, page_width=450, resize=True
        )
        with open(EXPECTED_RESIZED_TXT_FILE_PATH, "r") as f:
            expected_converted_text = f.read()
        self.assertEqual(converted_text[0], expected_converted_text)

# ============================================================
# Vidhi-AI | Unit Tests — Utility Functions
# ============================================================

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from utils import clean_ai_output, sanitize_filename, html_escape


class TestCleanAIOutput(unittest.TestCase):
    """Test the clean_ai_output function that strips leaked
    training tags from LLM output."""

    def test_strips_mapping_tags(self):
        """Should remove map:ipc_bns:X.X style tags."""
        text = "BNS Section 103 replaces IPC 302. map:ipc_bns:1.0"
        result = clean_ai_output(text)
        self.assertNotIn("map:ipc_bns", result)
        self.assertIn("BNS Section 103", result)

    def test_strips_version_numbers(self):
        """Should remove v1.0, v2.1 style version tags."""
        text = "Under the BNS v2.1, murder is punished under Section 103."
        result = clean_ai_output(text)
        self.assertNotIn("v2.1", result)
        self.assertIn("Section 103", result)

    def test_preserves_normal_text(self):
        """Normal legal text without tags should be unchanged."""
        text = "IPC Section 302 is now BNS Section 103 under the 2023 reforms."
        result = clean_ai_output(text)
        self.assertEqual(result, text)

    def test_collapses_extra_spaces(self):
        """Should reduce multiple spaces to single space."""
        text = "BNS  Section   103  covers  murder."
        result = clean_ai_output(text)
        self.assertNotIn("  ", result)

    def test_removes_blank_lines(self):
        """Should remove lines that are only whitespace."""
        text = "Line one.\n   \n\nLine two."
        result = clean_ai_output(text)
        self.assertEqual(result, "Line one.\nLine two.")

    def test_empty_input(self):
        """Empty string should return empty string."""
        self.assertEqual(clean_ai_output(""), "")


class TestSanitizeFilename(unittest.TestCase):
    """Test the sanitize_filename function for security."""

    def test_strips_directory_traversal(self):
        """Should remove path traversal components."""
        self.assertNotIn("..", sanitize_filename("../../etc/passwd"))
        self.assertNotIn("/", sanitize_filename("../../etc/passwd"))

    def test_removes_null_bytes(self):
        """Should remove null bytes from filenames."""
        result = sanitize_filename("file\x00.pdf")
        self.assertNotIn("\x00", result)

    def test_preserves_normal_filename(self):
        """Normal filenames should pass through."""
        self.assertEqual(sanitize_filename("fir_report.pdf"), "fir_report.pdf")

    def test_replaces_special_characters(self):
        """Unsafe characters should be replaced with underscores."""
        result = sanitize_filename("file<>name|test.pdf")
        self.assertNotIn("<", result)
        self.assertNotIn(">", result)
        self.assertNotIn("|", result)

    def test_limits_length(self):
        """Extremely long filenames should be truncated."""
        long_name = "a" * 300 + ".pdf"
        result = sanitize_filename(long_name)
        self.assertLessEqual(len(result), 204)  # 200 + .pdf

    def test_empty_filename_returns_default(self):
        """Empty filename should return a safe default."""
        self.assertEqual(sanitize_filename(""), "uploaded_file.pdf")

    def test_windows_path_traversal(self):
        """Should handle Windows-style path traversal."""
        result = sanitize_filename("..\\..\\windows\\system32\\cmd.exe")
        self.assertNotIn("..\\", result)
        self.assertNotIn("system32", result)


class TestHtmlEscape(unittest.TestCase):
    """Test the html_escape function."""

    def test_escapes_ampersand(self):
        self.assertEqual(html_escape("a & b"), "a &amp; b")

    def test_escapes_less_than(self):
        self.assertEqual(html_escape("<script>"), "&lt;script&gt;")

    def test_escapes_greater_than(self):
        self.assertEqual(html_escape("a > b"), "a &gt; b")

    def test_preserves_normal_text(self):
        self.assertEqual(html_escape("Hello World"), "Hello World")

    def test_multiple_special_chars(self):
        result = html_escape("<b>A & B</b>")
        self.assertEqual(result, "&lt;b&gt;A &amp; B&lt;/b&gt;")


if __name__ == "__main__":
    unittest.main()

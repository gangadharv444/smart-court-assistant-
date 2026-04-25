# ============================================================
# Vidhi-AI | Unit Tests — Loaders
# ============================================================

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest


class TestBNSCSVRows(unittest.TestCase):
    """Test the CSV data loading (without Streamlit dependency)."""

    def setUp(self):
        """Load CSV rows directly without Streamlit cache."""
        import csv
        csv_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "bns_sections.csv",
        )
        self.rows = []
        if os.path.exists(csv_path):
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.rows.append({
                        "section": row.get("Section", "").strip(),
                        "section_name": row.get("Section _name", "").strip(),
                        "description": row.get("Description", "").strip(),
                        "chapter": row.get("Chapter", "").strip(),
                        "chapter_name": row.get("Chapter_name", "").strip(),
                    })

    def test_csv_has_rows(self):
        """CSV should have at least 300 rows."""
        if not self.rows:
            self.skipTest("bns_sections.csv not found")
        self.assertGreaterEqual(len(self.rows), 300)

    def test_row_structure(self):
        """Each row should have required keys."""
        if not self.rows:
            self.skipTest("bns_sections.csv not found")
        required_keys = {"section", "section_name", "description",
                         "chapter", "chapter_name"}
        for row in self.rows[:5]:
            self.assertTrue(required_keys.issubset(row.keys()))

    def test_section_numbers_not_empty(self):
        """Section numbers should not be empty strings."""
        if not self.rows:
            self.skipTest("bns_sections.csv not found")
        for row in self.rows:
            self.assertTrue(
                row["section"].strip(),
                f"Empty section found: {row}"
            )


class TestOllamaHealthCheck(unittest.TestCase):
    """Test the Ollama health check handles errors gracefully."""

    def test_health_check_returns_bool(self):
        """check_ollama_health should return a boolean."""
        from loaders import check_ollama_health
        result = check_ollama_health()
        self.assertIsInstance(result, bool)

    def test_health_check_no_exception(self):
        """Health check should never raise, even if Ollama is down."""
        from loaders import check_ollama_health
        try:
            check_ollama_health()
        except Exception as e:
            self.fail(
                f"check_ollama_health raised {type(e).__name__}: {e}"
            )


if __name__ == "__main__":
    unittest.main()

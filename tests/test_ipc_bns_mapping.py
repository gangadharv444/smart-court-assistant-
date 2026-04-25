# ============================================================
# Vidhi-AI | Unit Tests — IPC-to-BNS Mapping
# ============================================================

import sys
import os

# Add parent directory to path so we can import project modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from ipc_bns_mapping import (
    IPC_TO_BNS, lookup_ipc_to_bns, get_ipc_section_name, contextual_rerank,
)


class TestIPCToBNSMapping(unittest.TestCase):
    """Test the deterministic IPC-to-BNS mapping dictionary."""

    def test_known_murder_mapping(self):
        """IPC 302 (Murder) should map to BNS 103."""
        self.assertEqual(IPC_TO_BNS.get("302"), "103")

    def test_known_cheating_mapping(self):
        """IPC 420 (Cheating) should map to BNS 318."""
        self.assertEqual(IPC_TO_BNS.get("420"), "318")

    def test_known_attempt_to_murder(self):
        """IPC 307 (Attempt to Murder) should map to BNS 109."""
        self.assertEqual(IPC_TO_BNS.get("307"), "109")

    def test_known_sedition_mapping(self):
        """IPC 124A (Sedition) should map to BNS 152."""
        self.assertEqual(IPC_TO_BNS.get("124A"), "152")

    def test_known_rape_mapping(self):
        """IPC 375 (Rape) should map to BNS 63."""
        self.assertEqual(IPC_TO_BNS.get("375"), "63")

    def test_known_theft_mapping(self):
        """IPC 378/379 (Theft) should map to BNS 303."""
        self.assertEqual(IPC_TO_BNS.get("378"), "303")
        self.assertEqual(IPC_TO_BNS.get("379"), "303")

    def test_known_criminal_conspiracy(self):
        """IPC 120B (Criminal Conspiracy) should map to BNS 61."""
        self.assertEqual(IPC_TO_BNS.get("120B"), "61")

    def test_known_defamation(self):
        """IPC 499 (Defamation) should map to BNS 356."""
        self.assertEqual(IPC_TO_BNS.get("499"), "356")

    def test_known_dowry_death(self):
        """IPC 304B (Dowry Death) should map to BNS 80."""
        self.assertEqual(IPC_TO_BNS.get("304B"), "80")

    def test_unknown_section_returns_none(self):
        """A non-existent IPC section should return None."""
        self.assertIsNone(IPC_TO_BNS.get("999"))
        self.assertIsNone(IPC_TO_BNS.get("0"))
        self.assertIsNone(IPC_TO_BNS.get("ABC"))

    def test_mapping_has_minimum_entries(self):
        """The mapping should have at least 200 entries."""
        self.assertGreaterEqual(len(IPC_TO_BNS), 200)


class TestLookupIPCToBNS(unittest.TestCase):
    """Test the lookup_ipc_to_bns function with mock CSV data."""

    def setUp(self):
        """Create mock CSV rows for testing."""
        self.mock_rows = [
            {"section": "103", "section_name": "Murder",
             "description": "Whoever commits murder...",
             "chapter": "VI", "chapter_name": "Offences Affecting Life"},
            {"section": "109", "section_name": "Attempt to Murder",
             "description": "Whoever attempts to murder...",
             "chapter": "VI", "chapter_name": "Offences Affecting Life"},
            {"section": "318", "section_name": "Cheating",
             "description": "Whoever cheats...",
             "chapter": "XVII", "chapter_name": "Offences Against Property"},
        ]

    def test_lookup_murder(self):
        """IPC 302 should find BNS 103 in the CSV rows."""
        result = lookup_ipc_to_bns("302", self.mock_rows)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["section"], "103")
        self.assertEqual(result[0]["section_name"], "Murder")

    def test_lookup_cheating(self):
        """IPC 420 should find BNS 318 in the CSV rows."""
        result = lookup_ipc_to_bns("420", self.mock_rows)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["section"], "318")

    def test_lookup_unknown_returns_empty(self):
        """Unknown IPC section should return empty list."""
        result = lookup_ipc_to_bns("999", self.mock_rows)
        self.assertEqual(result, [])

    def test_lookup_attempt_to_murder(self):
        """IPC 307 should find BNS 109."""
        result = lookup_ipc_to_bns("307", self.mock_rows)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["section"], "109")


class TestGetIPCSectionName(unittest.TestCase):
    """Test the get_ipc_section_name function."""

    def test_known_section_names(self):
        self.assertEqual(get_ipc_section_name("302"), "Punishment for Murder")
        self.assertEqual(get_ipc_section_name("420"), "Cheating and Dishonestly Inducing Delivery")
        self.assertEqual(get_ipc_section_name("124A"), "Sedition")

    def test_unknown_section_returns_default(self):
        result = get_ipc_section_name("999")
        self.assertEqual(result, "IPC Section 999")


class TestContextualRerank(unittest.TestCase):
    """Test the contextual_rerank function."""

    def setUp(self):
        self.rows = [
            {"section": "100", "section_name": "Culpable Homicide",
             "description": "Culpable homicide not amounting to murder"},
            {"section": "101", "section_name": "Murder",
             "description": "Whoever commits murder shall be punished"},
            {"section": "109", "section_name": "Attempt to Murder",
             "description": "Whoever attempts to commit murder"},
        ]

    def test_rerank_with_attempt_keyword(self):
        """Query mentioning 'attempt' should boost the attempt row."""
        result = contextual_rerank("attempt to murder", self.rows)
        self.assertEqual(result[0]["section"], "109")

    def test_rerank_no_keywords_preserves_order(self):
        """Query without context keywords should preserve order."""
        result = contextual_rerank("section 100", self.rows)
        self.assertEqual(result, self.rows)

    def test_rerank_empty_query(self):
        """Empty query should return rows unchanged."""
        result = contextual_rerank("", self.rows)
        self.assertEqual(result, self.rows)


if __name__ == "__main__":
    unittest.main()

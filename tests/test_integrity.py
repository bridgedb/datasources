"""Test the integrity of the datasources references."""

import csv
import unittest
from pathlib import Path

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
HEADERS_PATH = ROOT.joinpath("datasources_headers.tsv")
DATASOURCES_PATH = ROOT.joinpath("datasources.tsv")


class TestIntegrity(unittest.TestCase):
    """Test data integrity."""

    @classmethod
    def setUpClass(cls) -> None:
        """Load the data sources rows."""
        with HEADERS_PATH.open() as file:
            _, *cls.columns = [row[1] for row in csv.reader(file, delimiter="\t")]
        with DATASOURCES_PATH.open() as file:
            cls.rows = list(csv.reader(file, delimiter="\t"))

    def test_lengths(self):
        """Test the row lengths."""
        for i, line in enumerate(self.rows, start=1):
            self.assertEqual(
                len(self.columns), len(line), msg=f"Row {i} has the wrong number of columns"
            )

    def test_valid_bioregistry(self):
        """Test that Bioregistry prefixes are valid."""

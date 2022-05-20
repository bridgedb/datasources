import csv
import unittest
from pathlib import Path

from bioregistry.external.miriam import get_miriam

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
HEADERS = ROOT.joinpath("headers.tsv")
DATASOURCES = ROOT.joinpath("datasources.tsv")

#: The number of columns. Change if more columns are added.
N_COLUMNS = 12


class TestIntegrity(unittest.TestCase):
    """Test data integrity."""

    def setUp(self) -> None:
        """Load the data sources rows."""
        with DATASOURCES.open() as file:
            self.rows = list(csv.reader(file, delimiter="\t"))

    def test_lengths(self):
        """Test the row lengths."""
        for i, line in enumerate(self.rows, start=1):
            self.assertEqual(
                N_COLUMNS, len(line), msg=f"Row {i} has the wrong number of columns"
            )

    def test_valid_miriam(self):
        """Test that MIRIAM prefixes are valid."""
        valid_miriam_prefixes = set(get_miriam())
        for i, line in enumerate(self.rows, start=1):
            resource, uri = line[0], line[8]
            if not uri.startswith("urn:miriam"):
                continue
            miriam_prefix = uri.removeprefix("urn:miriam:")
            with self.subTest(resource=resource, miriam=miriam_prefix):
                self.assertIn(
                    miriam_prefix,
                    valid_miriam_prefixes,
                    msg=f"\n\t[line {i}] Invalid MIRIAM prefix for {resource}: {uri}",
                )

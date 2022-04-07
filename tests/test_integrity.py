import csv
import unittest
from pathlib import Path

from bioregistry.external.miriam import get_miriam

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
HEADERS = ROOT.joinpath("headers.tsv")
DATASOURCES = ROOT.joinpath("datasources.tsv")


class TestIntegrity(unittest.TestCase):
    """Test data integrity."""

    def test_valid_miriam(self):
        """Test that MIRIAM prefixes are valid."""
        valid_miriam_prefixes = set(get_miriam())
        with DATASOURCES.open() as file:
            reader = csv.reader(file, delimiter='\t')
            for i, line in enumerate(reader):
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

from pathlib import Path

import pandas as pd

import bioregistry

HERE = Path(__file__).parent.resolve()
COLUMNS = HERE.joinpath("datasources_headers.tsv")
DATASOURCES = HERE.joinpath("datasources.tsv")

MIRIAM_MAP = bioregistry.get_registry_invmap("miriam")
print(MIRIAM_MAP)


def map_uri(s: str):
    if s.startswith("urn:miriam:"):
        return MIRIAM_MAP.get(s.removeprefix("urn:miriam:"))
    return None


def main():
    headers_df = pd.read_csv(COLUMNS, sep='\t')
    df = pd.read_csv(DATASOURCES, sep='\t', names=list(headers_df["header"]))
    df["bioregistry"] = df["uri"].map(map_uri, na_action="ignore")
    df.to_csv(DATASOURCES, sep='\t', index=False, header=False)


if __name__ == '__main__':
    main()

from pathlib import Path

import pandas as pd
from tqdm import tqdm

import bioregistry

HERE = Path(__file__).parent.resolve()
COLUMNS = HERE.joinpath("datasources_headers.tsv")
DATASOURCES = HERE.joinpath("datasources.tsv")
CURATION = HERE.joinpath("curation.tsv")

MIRIAM_MAP = bioregistry.get_registry_invmap("miriam")
WIKIDATA_MAP = bioregistry.get_registry_invmap("wikidata")

#: System code to bioregistry
MANUAL = {
    "ICD9": "icd9",
    "ICD10": "icd10",
    "ICD11": "icd11",
    "Eco": "eco",
    "Ip": "interpro",
    "Mc": "metacyc.reaction",
    "PATO": "pato",
    "Sbo": "sbo",
    "Up": "upa",
    "Rfam": "rfam",
    "MaizeGDB": "maizegdb.locus",
    "SwissLipids": "swisslipid",
    "VMH metabolite": "vmhmetabolite",
    "XMetDB": "xmetdb",
    "Brl": "brenda.ligand",
    "Gg": "gramene.gene",
}
SKIP = {
    "Other",
}


def main():
    headers_df = pd.read_csv(COLUMNS, sep="\t")
    df = pd.read_csv(DATASOURCES, sep="\t", names=list(headers_df["header"]))

    # Check MANUAL curation
    for key, value in MANUAL.items():
        if value != bioregistry.normalize_prefix(value):
            raise ValueError(f"Invalid bioregistry prefix in manual mapping: {value}")

    rows = []
    for _, row in tqdm(df.iterrows()):
        system_code = row["system_code"]
        datasource_name = row["datasource_name"]
        if datasource_name in SKIP or system_code in SKIP:
            continue

        uri = row["uri"]
        if pd.notna(uri) and uri.startswith("urn:miriam:"):
            miriam_prefix = uri.removeprefix("urn:miriam:")
            br_prefix = MIRIAM_MAP.get(miriam_prefix)
            if br_prefix is not None:
                continue

        wikidata_prop = row["wikidata_property"]
        if pd.notna(wikidata_prop):
            if wikidata_prop in WIKIDATA_MAP:
                continue

        if system_code in MANUAL:
            continue
        norm_sys_code = bioregistry.normalize_prefix(system_code)
        if norm_sys_code:
            raise ValueError(f'need to add: "{system_code}": "{norm_sys_code}",')

        if datasource_name in MANUAL:
            continue
        norm_datasource_name = bioregistry.normalize_prefix(datasource_name)
        if norm_datasource_name:
            raise ValueError(
                f'need to add: "{datasource_name}": "{norm_datasource_name}",'
            )

        rows.append(row)

    curation_df = pd.DataFrame(rows, columns=df.columns)
    curation_df.to_csv(CURATION, sep="\t", index=False)


if __name__ == "__main__":
    main()

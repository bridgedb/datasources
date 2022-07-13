from pathlib import Path

import pandas as pd
from tqdm import tqdm

import bioregistry
from tabulate import tabulate

HERE = Path(__file__).parent.resolve()
ROOT = HERE.parent.resolve()
COLUMNS = ROOT.joinpath("datasources_headers.tsv")
DATASOURCES = ROOT.joinpath("datasources.tsv")
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
    "Ob": "oryzabase.gene",
    "SPRINT": "sprint",
    "Gl": "gramene.reference",
}
SKIP = {
    "Other",
    "BIND",  # doesn't exist anymore
    "OpenTargets",  # is a provider for ensembl gene
}


def main():
    headers_df = pd.read_csv(COLUMNS, sep="\t")
    df = pd.read_csv(DATASOURCES, sep="\t", names=list(headers_df["header"]))

    # Check MANUAL curation
    for key, value in MANUAL.items():
        if value != bioregistry.normalize_prefix(value):
            raise ValueError(f"Invalid bioregistry prefix in manual mapping: {value}")

    rows = []
    prefixes = []
    for _, row in tqdm(df.iterrows()):
        bioregistry_prefix = row.get("bioregistry")
        if pd.notna(bioregistry_prefix):
            prefixes.append(bioregistry_prefix)
            continue

        if pd.isna(row.get("linkout_pattern")):
            prefixes.append(None)
            continue

        system_code = row["system_code"]
        datasource_name = row["datasource_name"]
        if datasource_name in SKIP or system_code in SKIP:
            prefixes.append(None)
            continue

        uri = row["uri"]
        if pd.notna(uri) and uri.startswith("urn:miriam:"):
            miriam_prefix = uri.removeprefix("urn:miriam:")
            br_prefix = MIRIAM_MAP.get(miriam_prefix)
            if br_prefix is not None:
                prefixes.append(br_prefix)
                continue

        wikidata_prop = row["wikidata_property"]
        if pd.notna(wikidata_prop):
            if wikidata_prop in WIKIDATA_MAP:
                prefixes.append(WIKIDATA_MAP[wikidata_prop])
                continue

        if system_code in MANUAL:
            prefixes.append(MANUAL[system_code])
            continue
        norm_sys_code = bioregistry.normalize_prefix(system_code)
        if norm_sys_code:
            raise ValueError(f'need to add: "{system_code}": "{norm_sys_code}",')

        if datasource_name in MANUAL:
            prefixes.append(MANUAL[datasource_name])
            continue
        norm_datasource_name = bioregistry.normalize_prefix(datasource_name)
        if norm_datasource_name:
            raise ValueError(
                f'need to add: "{datasource_name}": "{norm_datasource_name}",'
            )

        prefixes.append(None)
        rows.append(row)

    df["bioregistry"] = prefixes
    df.to_csv(DATASOURCES, index=False, header=False, sep="\t")

    curation_df = pd.DataFrame(rows, columns=df.columns)
    print(
        tabulate(
            curation_df.values, headers=list(curation_df.columns), tablefmt="github"
        )
    )
    for key in [
        "entity_identified",
        "bioregistry",
        "system_code",
        "uri",
        "identifier_type",
        "wikidata_property",
    ]:
        del curation_df[key]
    curation_df.to_csv(CURATION, sep="\t", index=False)


if __name__ == "__main__":
    main()

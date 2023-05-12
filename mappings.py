import itertools as itt
import pandas as pd
from more_itertools import chunked
import requests
from textwrap import dedent
from tqdm.auto import tqdm

#: The URL of the OpenCheck ORCID-Twitter follow graph
url = "https://opencheck.is/scitwitter/orcidgraph"

#: Wikidata SPARQL endpoint. See https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service#Interfacing
WIKIDATA_ENDPOINT = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"


def query_wikidata(sparql: str) -> list[dict[str, any]]:
    """Query Wikidata's sparql service."""
    res = requests.get(WIKIDATA_ENDPOINT, params={"query": sparql, "format": "json"})
    res.raise_for_status()
    res_json = res.json()
    return [
        {
            key: value["value"].removeprefix("http://www.wikidata.org/entity/")
            for key, value in bindings.items()
        }
        for bindings in res_json["results"]["bindings"]
    ]


def main(chunksize: int = 150) -> None:
    twitter_df = pd.read_csv(url, header=None)
    orcids = set(itt.chain.from_iterable(twitter_df.values))
    print(f"There are {len(orcids):,} unique ORCID identifiers")
    records = []
    for group in tqdm(chunked(orcids, chunksize)):
        values = " ".join(f"'{orcid}'" for orcid in group)
        sparql = dedent(f"""\
            SELECT DISTINCT ?orcid ?wikidata ?twitter ?github
            WHERE {{
                VALUES ?orcid {{{ values }}}
                OPTIONAL {{
                    ?wikidata wdt:P496 ?orcid .
                    OPTIONAL {{ ?wikidata wdt:P2002 ?twitter }}
                    OPTIONAL {{ ?wikidata wdt:P2037 ?github }}
                }}
            }}
        """)
        records.extend(query_wikidata(sparql))
    df = pd.DataFrame(records)
    df.to_csv("mappings.tsv", sep='\t', index=False)


if __name__ == '__main__':
    main()

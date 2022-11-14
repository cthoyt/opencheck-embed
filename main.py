"""Embed OpenCheck with GRAPE."""

from pathlib import Path

import click
import matplotlib.pyplot as plt
import pandas as pd
import pystow
from grape import Graph, GraphVisualizer
from grape.embedders import SecondOrderLINEEnsmallen

HERE = Path(__file__).parent.resolve()
EMBEDDINGS_DIRECTORY = HERE.joinpath("embeddings")
EMBEDDINGS_DIRECTORY.mkdir(exist_ok=True, parents=True)

url = "https://opencheck.is/scitwitter/orcidgraph"


models = [
    ("line", SecondOrderLINEEnsmallen, dict(embedding_size=32)),
]


@click.command()
def main():
    """Embed OpenCheck with GRAPE."""
    edge_path = pystow.ensure("opencheck", url=url, name="edges.tsv", force=True)
    # TODO is it possible to load from pandas dataframe?
    graph = Graph.from_csv(
        edge_path=str(edge_path),
        edge_list_separator=",",
        edge_list_header=False,
        sources_column_number=0,
        destinations_column_number=1,
        edge_list_numeric_node_ids=False,
        directed=True,
        name="OpenCheck",
    )
    for name, model_cls, kwargs in models:
        embedding = model_cls(**kwargs).fit_transform(graph)
        df = embedding.get_all_node_embedding()[0]
        df.index.name = "orcid"
        df.to_csv(EMBEDDINGS_DIRECTORY.joinpath(f"{name}.tsv"), sep="\t")


if __name__ == "__main__":
    main()

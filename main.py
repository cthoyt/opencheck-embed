"""Embed OpenCheck with GRAPE."""

from pathlib import Path

import click
import matplotlib.pyplot as plt
import pystow
from embiggen.embedders import SecondOrderLINEEnsmallen
from embiggen.visualizations import GraphVisualizer
from ensmallen import Graph

HERE = Path(__file__).parent.resolve()
EMBEDDINGS_DIRECTORY = HERE.joinpath("embeddings")
EMBEDDINGS_DIRECTORY.mkdir(exist_ok=True, parents=True)

#: The URL of the OpenCheck ORCID-Twitter follow graph
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
        stub = EMBEDDINGS_DIRECTORY.joinpath(name)
        embedding = model_cls(**kwargs).fit_transform(graph)
        df = embedding.get_all_node_embedding()[0].sort_index()
        df.index.name = "orcid"
        df.to_csv(stub.with_suffix(".tsv"), sep="\t")
        visualizer = GraphVisualizer(graph)
        fig, *_ = visualizer.fit_and_plot_all(embedding)
        plt.savefig(stub.with_suffix(".png"), dpi=300)
        plt.close(fig)


if __name__ == "__main__":
    main()

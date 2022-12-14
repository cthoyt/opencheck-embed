# OpenCheck Embeddings

[OpenCheck](https://opencheck.is) is currently working to map Twitter handles to [ORCID identifiers](https://orcid.org)
and capture the follow graph of researchers on Twitter (in case the service becomes unusable in the near future).
Data available under CC0 [here](https://opencheck.is/scitwitter/orcidgraph).

This repository uses [GRAPE](https://github.com/AnacletoLAB/grape) to embedding the OpenCheck ORCID graph (which is
a *directed graph*) and assign to each ORCID identifier a low-dimensional vector of real numbers that can be used
for various tasks such as clustering, classification. These embeddings can be downloaded as a TSV
file [here](embeddings/line.tsv) and are regenerated nightly using GitHub Actions.

## Summary

![](embeddings/line.png)

## Running

The code in this repository is completely reproducible. It is wrapped in `tox` to abstract all
installation and commands so the embeddings can be recreated with the following commands:

```shell
git clone https://github.com/cthoyt/opencheck-embed.git
cd opencheck-embed
pip install tox
tox
```

## License

Code in this repository is licensed under the MIT license. The embeddings and charts are licensed under CC0.

## Citation

If you like GRAPE, please cite:

```bibtex
@misc{cappelletti2021grape,
    title = {GRAPE: fast and scalable Graph Processing and Embedding},
    author = {Luca Cappelletti and Tommaso Fontana and Elena Casiraghi and Vida Ravanmehr and Tiffany J. Callahan and Marcin P. Joachimiak and Christopher J. Mungall and Peter N. Robinson and Justin Reese and Giorgio Valentini},
    year = {2021},
    eprint = {2110.06196},
    archivePrefix = {arXiv},
    primaryClass = {cs.LG}
}
```

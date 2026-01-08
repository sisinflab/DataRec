# DataRec Documentation

<img src="./images/datarec_architecture.png"  width="600">


This is the official documentation for *"DataRec: A Python Library for Standardized and Reproducible Data Management in Recommender Systems"* (SIGIR 2025).

## Table of Contents

- [What is DataRec](#what-is-datarec)
- [Quickstart](#quickstart)
- [Filtering Strategies](#filtering-strategies)
- [Splitting Strategies](#splitting-strategies)
- [Authors](#authors)

## What is DataRec
DataRec is a Python library that focuses on the **data management** phase of recommendation systems. It promotes **standardization**, **interoperability**, and **best practices** for processing and analyzing recommendation datasets.

**Key links:**
- [Get started](get_started.md)
- [Datasets](datasets_nav.md)
- [Pipeline](documentation/pipeline.md)
- [Processing](documentation/processing.md)
- [Splitters](documentation/splitters.md)

## Quickstart

```python
from datarec.datasets import AmazonOffice
from datarec.processing import FilterOutDuplicatedInteractions, UserItemIterativeKCore
from datarec.splitters import RandomHoldOut

data = AmazonOffice(version="2014").prepare_and_load()
data = FilterOutDuplicatedInteractions().run(data)
data = UserItemIterativeKCore(cores=5).run(data)

splits = RandomHoldOut(test_ratio=0.2, val_ratio=0.1, seed=42).run(data)
train, val, test = splits["train"], splits["val"], splits["test"]
```

## Filtering Strategies
DataRec provides **preprocessing filters** to clean and shape interaction data before modeling. See the
`Processing` section for the full list of filtering operations.

## Splitting Strategies
DataRec includes multiple **splitting strategies** (uniform, user‑stratified, temporal) to build
train/validation/test splits. See the `Splitters` section for details.

### Features
- Dataset Management: Supports reading and writing various data formats and allows dynamic format specification.
- Reference Datasets: Include commonly used recommendation datasets with traceable sources and versioning.
- Filtering Strategies: Implements popular filtering techniques.
- Splitting Strategies: Implements widely used data splitting strategies.
- Data Characteristics Analysis: Enables computing data characteristics that impact recommendation performance.
- Interoperability: Designed to be modular and compatible with existing recommendation frameworks by allowing dataset export in various formats.

## Authors

- Alberto Carlo Maria Mancino (alberto.mancino@poliba.it)
- Salvatore Bufi (salvatore.bufi@poliba.it)
- Angela Di Fazio (angela.difazio@poliba.it)
- Daniele Malitesta (daniele.malitesta@centralesupelec.fr)
- Antonio Ferrara (antonio.ferrara@poliba.it)
- Claudio Pomo (claudio.pomo@poliba.it)
- Tommaso Di Noia (tommaso.dinoia@poliba.it)

## Contributors

- [Alberto C. M. Mancino](https://github.com/AlbertoMancino)
- [Angela Di Fazio](https://github.com/a-difazio)
- [Salvatore Bufi](https://github.com/salvatore-bufi)
- [Giuseppe Fasano](https://github.com/GiuseppeFasano)
- [Gianluca Colonna](https://github.com/GianLu210)
- [Maria L. N. De Bonis](https://github.com/MariaLuigiaN)
- [Marco Valentini](https://github.com/Marco-Valentini)

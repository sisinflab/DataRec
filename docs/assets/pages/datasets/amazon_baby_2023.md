# Amazon Baby

## Overview

**Dataset name:** Amazon Baby  
**Latest version:** 2023  
**Available versions:** 2023  
**Source:** https://amazon-reviews-2023.github.io/

A large-scale Amazon Reviews dataset, collected by McAuley Lab

---

## Citation

```bibtex
@article{DBLP:journals/corr/abs-2403-03952,
author       = {Yupeng Hou and
                Jiacheng Li and
                Zhankui He and
                An Yan and
                Xiusi Chen and
                Julian J. McAuley},
title        = {Bridging Language and Items for Retrieval and Recommendation},
journal      = {CoRR},
volume       = {abs/2403.03952},
year         = {2024}
}
```

---

## Version: 2023

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Baby_Products.csv.gz | md5:644025598b2e4eb6dc69b55a7f23c8ae |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Baby_Products.csv`

**Schema**

```yaml
sep: ','
user_col: user_id
item_col: parent_asin
rating_col: rating
timestamp_col: timestamp
header: 0
```

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 3386206 |
| n_items | 217654 |
| n_interactions | 5953891 |
| space_size | 858.4994354826333 |
| space_size_log | 2.933740013921096 |
| shape | 15.557747617778677 |
| shape_log | 1.1919467219611264 |
| density | 8.078316265374725e-06 |
| density_log | -5.092679148242243 |
| gini_item | 0.8648800449385958 |
| gini_user | 0.36108985080926276 |
| ratings_per_user | 1.7582778484238704 |
| ratings_per_item | 27.354843007709484 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/

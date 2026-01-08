# Amazon Office

## Overview

**Dataset name:** Amazon Office  
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
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Office_Products.csv.gz | md5:d4c05697d3acd22d1c23a01b64b25a16 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Office_Products.csv`

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
| n_users | 7613158 |
| n_items | 710403 |
| n_interactions | 12689349 |
| space_size | 2325.5989083833865 |
| space_size_log | 3.3665348149082335 |
| shape | 10.716674901429188 |
| shape_log | 1.030060056255404 |
| density | 2.346225292975775e-06 |
| density_log | -5.6296302877028435 |
| gini_item | 0.8377877061123389 |
| gini_user | 0.3341419828184234 |
| ratings_per_user | 1.6667654868058694 |
| ratings_per_item | 17.862183859020867 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/

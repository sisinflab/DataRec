# Amazon Sports and Outdoors

## Overview

**Dataset name:** Amazon Sports and Outdoors  
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
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Sports_and_Outdoors.csv.gz | md5:75e1dfbb3b3014fab914832b734922e6 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Sports_and_Outdoors.csv`

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
| n_users | 10331141 |
| n_items | 1587219 |
| n_interactions | 19349403 |
| space_size | 4049.4176478697527 |
| space_size_log | 3.607392571238953 |
| shape | 6.5089574910582595 |
| shape_log | 0.813511435244585 |
| density | 1.1800011417081474e-06 |
| density_log | -5.9281175724927655 |
| gini_item | 0.8232507097140822 |
| gini_user | 0.38244082486129133 |
| ratings_per_user | 1.8729202321408642 |
| ratings_per_item | 12.190758175147852 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/

# Amazon Clothing

## Overview

**Dataset name:** Amazon Clothing  
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
| ratings | HttpSource | gz | https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/benchmark/0core/rating_only/Clothing_Shoes_and_Jewelry.csv.gz | md5:ce282bf3fdd269717486960be26b92e2 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `Clothing_Shoes_and_Jewelry.csv`

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
| n_users | 22553370 |
| n_items | 7216886 |
| n_interactions | 65179586 |
| space_size | 12757.942632173104 |
| space_size_log | 4.105780644954536 |
| shape | 3.1250833115557044 |
| shape_log | 0.49486159968541643 |
| density | 4.004518531158031e-07 |
| density_log | -6.397449692271609 |
| gini_item | 0.8263247764145355 |
| gini_user | 0.4949939818552991 |
| ratings_per_user | 2.8900153724254958 |
| ratings_per_item | 9.03153881050636 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://amazon-reviews-2023.github.io/

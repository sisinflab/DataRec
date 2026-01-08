# CiaoDVD

## Overview

**Dataset name:** CiaoDVD  
**Latest version:** v1  
**Available versions:** v1  
**Source:** https://guoguibing.github.io/librec/datasets.html

CiaoDVD is a dataset for DVDs recommendation.

---

## Citation

```bibtex
@inproceedings{DBLP:conf/asunam/GuoZTY14,
  author       = {Guibing Guo and
                  Jie Zhang and
                  Daniel Thalmann and
                  Neil Yorke{-}Smith},
  title        = {{ETAF:} An extended trust antecedents framework for trust prediction},
  booktitle    = {{ASONAM}},
  pages        = {540--547},
  publisher    = {{IEEE} Computer Society},
  year         = {2014}
}
```

---

## Version: v1

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| github_archive | HttpSource | zip | https://guoguibing.github.io/librec/datasets/CiaoDVD.zip | md5:43a39e068e3fc494a7f7f7581293e2c2 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `github_archive`
- **Filename:** `movie-ratings.txt`

**Schema**

```yaml
sep: ','
user_col: 0
item_col: 1
rating_col: 4
timestamp_col: 5
```

#### reviews

- **Type:** content
- **Format:** `tabular`
- **Source:** `github_archive`
- **Filename:** `review-ratings.txt`
- **About:** items

#### friendships

- **Type:** content
- **Format:** `tabular`
- **Source:** `github_archive`
- **Filename:** `trusts.txt`
- **About:** users

#### readme

- **Type:** documentation
- **Format:** `plaintext`
- **Source:** `github_archive`
- **Filename:** `readme.txt`

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 17615 |
| n_items | 16121 |
| n_interactions | 72665 |
| space_size | 16.851451421168445 |
| space_size_log | 1.2266373127478747 |
| shape | 1.0926741517275602 |
| shape_log | 0.0384906695387733 |
| density | 0.0002558884315873835 |
| density_log | -3.5919493476076516 |
| gini_item | 0.6557512489633792 |
| gini_user | 0.6631267979210606 |
| ratings_per_user | 4.12517740562021 |
| ratings_per_item | 4.507474722411761 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://guoguibing.github.io/librec/datasets.html

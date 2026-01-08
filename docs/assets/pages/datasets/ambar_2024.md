# Ambar

## Overview

**Dataset name:** Ambar  
**Latest version:** 2024  
**Available versions:** 2024  
**Source:** https://github.com/davidcontrerasaguilar/AMBAR

The AMBAR dataset is a dataset in the music domain. It contains both user feedback and attributes, including sensitive features. The users have been anonymized.

---

## Citation

```bibtex
@inproceedings{DBLP:conf/recsys/GomezCBS24,
author       = {Elizabeth G{\'{o}}mez and
                David Contreras and
                Ludovico Boratto and
                Maria Salam{\'{o}}},
title        = {{AMBAR:} {A} dataset for Assessing Multiple Beyond-Accuracy Recommenders},
booktitle    = {RecSys},
pages        = {137--147},
publisher    = {{ACM}},
year         = {2024}
}
```

---

## Version: 2024

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| ratings | HttpSource | False | https://raw.githubusercontent.com/davidcontrerasaguilar/AMBAR/refs/heads/main/data/AMBAR/ratings_info.csv | md5:c4ee943350b7ee42b167a3f3ee525005 |
| artists | HttpSource | False | https://raw.githubusercontent.com/davidcontrerasaguilar/AMBAR/refs/heads/main/data/AMBAR/artists_info.csv | md5:8c15a03f15f8a926e41f0689ca66c650 |
| tracks | HttpSource | False | https://raw.githubusercontent.com/davidcontrerasaguilar/AMBAR/refs/heads/main/data/AMBAR/tracks_info.csv | md5:872e2375da31c56e0d26ead87343fb71 |
| users | HttpSource | False | https://raw.githubusercontent.com/davidcontrerasaguilar/AMBAR/refs/heads/main/data/AMBAR/users_info.csv | md5:d17cd7396ed88915495fc58537490d4b |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `ratings_info.csv`

**Schema**

```yaml
sep: ','
user_col: user_id
item_col: track_id
rating_col: rating
header: 0
```

#### artists

- **Type:** content
- **Source:** `artists`
- **Filename:** `artists_info.csv`
- **About:** items

#### tracks

- **Type:** content
- **Source:** `tracks`
- **Filename:** `tracks_info.csv`
- **About:** items

#### users

- **Type:** content
- **Source:** `users`
- **Filename:** `users_info.csv`
- **About:** users

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 31013 |
| n_items | 443921 |
| n_interactions | 3311462 |
| space_size | 117.33423188907831 |
| space_size_log | 2.069424734636089 |
| shape | 0.06986152941627001 |
| shape_log | -1.1557619109718333 |
| density | 0.00024053058441535148 |
| density_log | -3.618829693517537 |
| gini_item | 0.7527298907837248 |
| gini_user | 0.26300532146144723 |
| ratings_per_user | 106.77657756424725 |
| ratings_per_item | 7.4595750144732955 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://github.com/davidcontrerasaguilar/AMBAR

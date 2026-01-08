# Gowalla

## Overview

**Dataset name:** Gowalla  
**Latest version:** checkins  
**Available versions:** checkins, friendships  
**Source:** https://snap.stanford.edu/data/loc-gowalla.html

Gowalla is a location-based social networking website where users share their locations by checking-in.

---

## Citation

```bibtex
@inproceedings{DBLP:conf/kdd/ChoML11,
  author       = {Eunjoon Cho and
                  Seth A. Myers and
                  Jure Leskovec},
  editor       = {Chid Apt{\'{e}} and
                  Joydeep Ghosh and
                  Padhraic Smyth},
  title        = {Friendship and mobility: user movement in location-based social networks},
  booktitle    = {Proceedings of the 17th {ACM} {SIGKDD} International Conference on
                  Knowledge Discovery and Data Mining, San Diego, CA, USA, August 21-24,
                  2011},
  pages        = {1082--1090},
  publisher    = {{ACM}},
  year         = {2011},
  url          = {https://doi.org/10.1145/2020408.2020579},
  doi          = {10.1145/2020408.2020579},
  timestamp    = {Sun, 02 Jun 2019 21:11:54 +0200},
  biburl       = {https://dblp.org/rec/conf/kdd/ChoML11.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```

---

## Version: checkins

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| checkins | HttpSource | gz | https://snap.stanford.edu/data/loc-gowalla_totalCheckins.txt.gz | md5:8ebd5ed2dd376d8982987c49429cb9f9 |

---

### Resources

#### checkins

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `checkins`
- **Filename:** `loc-gowalla_totalCheckins.txt`

**Schema**

```yaml
sep: "\t"
user_col: 0
item_col: 4
timestamp_col: 1
```

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 107092 |
| n_items | 1280969 |
| n_interactions | 6442892 |
| space_size | 370.3802534531235 |
| space_size_log | 2.5686478245408155 |
| shape | 0.08360233541951445 |
| shape_log | -1.0777815904360875 |
| density | 4.696617612528927e-05 |
| density_log | -4.32821479760447 |
| gini_item | 0.6297417387377424 |
| gini_user | 0.6915022878282465 |
| ratings_per_user | 60.16221566503567 |
| ratings_per_item | 5.029701733609478 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://snap.stanford.edu/data/loc-gowalla.html

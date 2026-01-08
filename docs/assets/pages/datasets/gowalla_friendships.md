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

## Version: friendships

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| friendships | HttpSource | gz | https://snap.stanford.edu/data/loc-gowalla_edges.txt.gz | md5:68bce8dc51609fe32bbd95e668aaf65e |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `friendships`
- **Filename:** `loc-gowalla_edges.txt`

**Schema**

```yaml
sep: "\t"
user_col: 0
item_col: 1
```

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 196591 |
| n_items | 196591 |
| n_interactions | 1900654 |
| space_size | 196.591 |
| space_size_log | 2.2935636318083987 |
| shape | 1.0 |
| shape_log | 0.0 |
| density | 4.917855913452399e-05 |
| density_log | -4.308224199653671 |
| gini_item | 0.6833529689546158 |
| gini_user | 0.6833529689546158 |
| ratings_per_user | 9.668062118815206 |
| ratings_per_item | 9.668062118815206 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://snap.stanford.edu/data/loc-gowalla.html

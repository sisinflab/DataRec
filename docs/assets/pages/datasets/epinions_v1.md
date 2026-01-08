# Epinions

## Overview

**Dataset name:** Epinions  
**Latest version:** v1  
**Available versions:** v1  
**Source:** https://snap.stanford.edu/data/soc-Epinions1.html

Epinions is a dataset for product recommendation research.

---

## Citation

```bibtex
@inproceedings{DBLP:conf/semweb/RichardsonAD03,
  author       = {Matthew Richardson and
                  Rakesh Agrawal and
                  Pedro M. Domingos},
  editor       = {Dieter Fensel and
                  Katia P. Sycara and
                  John Mylopoulos},
  title        = {Trust Management for the Semantic Web},
  booktitle    = {The Semantic Web - {ISWC} 2003, Second International Semantic Web
                  Conference, Sanibel Island, FL, USA, October 20-23, 2003, Proceedings},
  series       = {Lecture Notes in Computer Science},
  volume       = {2870},
  pages        = {351--368},
  publisher    = {Springer},
  year         = {2003},
  url          = {https://doi.org/10.1007/978-3-540-39718-2\_23},
  doi          = {10.1007/978-3-540-39718-2\_23},
  timestamp    = {Tue, 07 Sep 2021 13:48:16 +0200},
  biburl       = {https://dblp.org/rec/conf/semweb/RichardsonAD03.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```

---

## Version: v1

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| trust | HttpSource | gz | https://snap.stanford.edu/data/soc-Epinions1.txt.gz | md5:8df7433d4486ba68eb25e623feacff04 |

---

### Resources

#### trust

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `trust`
- **Filename:** `soc-Epinions1.txt`

**Schema**

```yaml
sep: "\t"
user_col: 0
item_col: 1
skiprows: 4
```

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 60341 |
| n_items | 51957 |
| n_interactions | 508837 |
| space_size | 55.99229712201492 |
| space_size_log | 1.7481282850865338 |
| shape | 1.161364205015686 |
| shape_log | 0.06496843629715585 |
| density | 0.00016230134290924048 |
| density_log | -3.789677886731624 |
| gini_item | 0.7921899552346756 |
| gini_user | 0.7644161705431212 |
| ratings_per_user | 8.432690873535407 |
| ratings_per_item | 9.793425332486478 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://snap.stanford.edu/data/soc-Epinions1.html

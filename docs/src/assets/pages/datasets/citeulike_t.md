# CiteULike

## Overview

**Dataset name:** CiteULike  
**Latest version:** t  
**Available versions:** a, t  
**Source:** http://www.citeulike.ort/faq/data.adp

CiteULike allows users to create their own collections of articles. There are abstracts, titles, and tags for each article.

---

## Citation

```bibtex
@inproceedings{DBLP:conf/kdd/WangB11,
author       = {Chong Wang and
                David M. Blei},
editor       = {Chid Apt{\'{e}} and
                Joydeep Ghosh and
                Padhraic Smyth},
title        = {Collaborative topic modeling for recommending scientific articles},
booktitle    = {Proceedings of the 17th {ACM} {SIGKDD} International Conference on
                Knowledge Discovery and Data Mining, San Diego, CA, USA, August 21-24,
                2011},
pages        = {448--456},
publisher    = {{ACM}},
year         = {2011},
url          = {https://doi.org/10.1145/2020408.2020480},
doi          = {10.1145/2020408.2020480},
timestamp    = {Tue, 06 Nov 2018 16:59:35 +0100},
biburl       = {https://dblp.org/rec/conf/kdd/WangB11.bib},
bibsource    = {dblp computer science bibliography, https://dblp.org}
}

@inproceedings{DBLP:conf/ijcai/WangCL13,
author       = {Hao Wang and
                Binyi Chen and
                Wu{-}Jun Li},
editor       = {Francesca Rossi},
title        = {Collaborative Topic Regression with Social Regularization for Tag
                Recommendation},
booktitle    = {{IJCAI} 2013, Proceedings of the 23rd International Joint Conference
                on Artificial Intelligence, Beijing, China, August 3-9, 2013},
pages        = {2719--2725},
publisher    = {{IJCAI/AAAI}},
year         = {2013},
url          = {http://www.aaai.org/ocs/index.php/IJCAI/IJCAI13/paper/view/7006},
timestamp    = {Tue, 23 Jan 2024 13:25:46 +0100},
biburl       = {https://dblp.org/rec/conf/ijcai/WangCL13.bib},
bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```

---

## Version: t

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| ratings | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-t/refs/heads/master/users.dat | md5:4e6b896cc923445803c1b8f12eb1c3bd |
| citations | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-t/refs/heads/master/citations.dat | md5:e9678798a607e613f9070d0734bde515 |
| tag-item | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-t/refs/heads/master/tag-item.dat | md5:91f0997a6199f7129b55e0f98a3caa02 |
| mult | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-t/refs/heads/master/mult.dat | md5:b8fdefb63bdd4c9b56bc5b7c488b3184 |
| tags | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-t/refs/heads/master/tags.dat | md5:23043d13aae074ae5977d7a8aae1790c |
| vocabulary | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-t/refs/heads/master/vocabulary.dat | md5:83b7909eaeb1ce5d3400d48b412edc70 |
| rawtext | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-t/refs/heads/master/rawtext.dat | md5:129dad5e7059057036c561569b58a47b |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `sequence_tabular_implicit`
- **Required:** yes
- **Source:** `ratings`
- **Filename:** `users.data`

**Schema**

```yaml
col_sep: ' '
```

#### citations

- **Type:** content
- **Source:** `citations`
- **Filename:** `citation.dat`

#### tag-item

- **Type:** content
- **Source:** `tag-item`
- **Filename:** `tag-item.dat`

#### mult

- **Type:** content
- **Source:** `mult`
- **Filename:** `mult.dat`

#### tags

- **Type:** content
- **Source:** `tags`
- **Filename:** `tags.dat`

#### vocabulary

- **Type:** content
- **Source:** `vocabulary`
- **Filename:** `vocabulary.dat`

#### rawtext

- **Type:** content
- **Source:** `rawtext`
- **Filename:** `rawtext.dat`

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 7947 |
| n_items | 25584 |
| n_interactions | 134860 |
| space_size | 14.258893645721606 |
| space_size_log | 1.1540858297095264 |
| shape | 0.3106238273921201 |
| shape_log | -0.507765233385266 |
| density | 0.000663302288858182 |
| density_log | -3.1782885040784317 |
| gini_item | 0.5197283261904477 |
| gini_user | 0.6368531036879522 |
| ratings_per_user | 16.969925758147728 |
| ratings_per_item | 5.271263289555972 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
http://www.citeulike.ort/faq/data.adp

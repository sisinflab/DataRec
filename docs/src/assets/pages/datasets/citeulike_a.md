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

## Version: a

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| ratings | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-a/refs/heads/master/users.dat | md5:b384e22f3b6cd9d0c8e11a13066fe70e |
| citations | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-a/refs/heads/master/citations.dat | md5:6635e40fc71f862d7338a6990535b99c |
| item-tag | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-a/refs/heads/master/item-tag.dat | md5:600433234dda44e846a40aeb2b211ca3 |
| mult | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-a/refs/heads/master/mult.dat | md5:63cca7f5fee224c60eb79a92f1fbecd9 |
| tags | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-a/refs/heads/master/tags.dat | md5:406562795523497ec00aaa9121cc9b39 |
| vocabulary | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-a/refs/heads/master/vocabulary.dat | md5:4834ecd48c7d073180cdf30973937093 |
| raw-data | HttpSource | False | https://raw.githubusercontent.com/js05212/citeulike-a/refs/heads/master/raw-data.csv | md5:ebef07c3e0eebd93b3adaf7ef710b58f |

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

#### item-tag

- **Type:** content
- **Source:** `item-tag`
- **Filename:** `item-tag.dat`

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

#### raw-data

- **Type:** content
- **Source:** `raw-data`
- **Filename:** `raw-data.csv`

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 5551 |
| n_items | 16980 |
| n_interactions | 204986 |
| space_size | 9.708551900257834 |
| space_size_log | 0.9871544566198973 |
| shape | 0.32691401648998825 |
| shape_log | -0.48556645857607317 |
| density | 0.002174779785855497 |
| density_log | -2.662584712332187 |
| gini_item | 0.3696468161800518 |
| gini_user | 0.4706337006537276 |
| ratings_per_user | 36.927760763826335 |
| ratings_per_item | 12.072202591283864 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
http://www.citeulike.ort/faq/data.adp

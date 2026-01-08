# Alibaba iFashion

## Overview

**Dataset name:** Alibaba iFashion  
**Latest version:** v1  
**Available versions:** v1  
**Source:** https://drive.google.com/drive/folders/1xFdx5xuNXHGsUVG2VIohFTXf9S7G5veq

Alibaba-iFashion is a dataset for fashion recommendation.

---

## Citation

```bibtex
@inproceedings{DBLP:conf/kdd/ChenHXGGSLPZZ19,
  author       = {Wen Chen and
                  Pipei Huang and
                  Jiaming Xu and
                  Xin Guo and
                  Cheng Guo and
                  Fei Sun and
                  Chao Li and
                  Andreas Pfadler and
                  Huan Zhao and
                  Binqiang Zhao},
  editor       = {Ankur Teredesai and
                  Vipin Kumar and
                  Ying Li and
                  R{\'{o}}mer Rosales and
                  Evimaria Terzi and
                  George Karypis},
  title        = {{POG:} Personalized Outfit Generation for Fashion Recommendation at
                  Alibaba iFashion},
  booktitle    = {Proceedings of the 25th {ACM} {SIGKDD} International Conference on
                  Knowledge Discovery {\&} Data Mining, {KDD} 2019, Anchorage, AK,
                  USA, August 4-8, 2019},
  pages        = {2662--2670},
  publisher    = {{ACM}},
  year         = {2019},
  url          = {https://doi.org/10.1145/3292500.3330652},
  doi          = {10.1145/3292500.3330652},
  timestamp    = {Tue, 16 Aug 2022 23:04:27 +0200},
  biburl       = {https://dblp.org/rec/conf/kdd/ChenHXGGSLPZZ19.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
```

---

## Version: v1

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| user_data_archive | GdownSource | 7z | https://drive.google.com/uc?id=1G_1SV9H7fQMPPJOBmZpCnCkgifSsb9Ar | md5:2ff9254d67fb13d04824621ca1387622 |
| item_data_archive | GdownSource | zip | https://drive.google.com/uc?id=17MAGl20_mf9V8j0-J6c7T3ayfZd-dIx8 | md5:f501244e784ae33defb71b3478d1125c |
| outfit_data_archive | GdownSource | zip | https://drive.google.com/uc?id=1HFKUqBe5oMizU0lxy6sQE5Er1w9x-cC4 | md5:f24078606235c122bd1d1c988766e83f |

---

### Resources

#### interactions

- **Type:** interactions
- **Format:** `sequence_tabular_inline`
- **Required:** yes
- **Source:** `user_data_archive`
- **Filename:** `user_data.txt`

**Schema**

```yaml
cols:
- user
- item
- outfit
user_col: user
sequence_col: item
col_sep: ','
sequence_sep: ;
stream: true
encode_ids: true
```

#### item_data

- **Type:** content
- **Source:** `item_data_archive`
- **Filename:** `item_data.txt`

#### outfit_data

- **Type:** content
- **Source:** `outfit_data_archive`
- **Filename:** `outfit_data.txt`

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 3569112 |
| n_items | 4463302 |
| n_interactions | 620880083 |
| space_size | 3991.2435064556007 |
| space_size_log | 3.6011082249736726 |
| shape | 0.799657294084066 |
| shape_log | -0.09709609697870838 |
| density | 3.8975462600227275e-05 |
| density_log | -4.40920872146218 |
| gini_item | 0.8774026297117475 |
| gini_user | 0.4029096347976372 |
| ratings_per_user | 173.9592601745196 |
| ratings_per_item | 139.10779127202238 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://drive.google.com/drive/folders/1xFdx5xuNXHGsUVG2VIohFTXf9S7G5veq

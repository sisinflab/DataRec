# Mind

## Overview

**Dataset name:** Mind  
**Latest version:** large  
**Available versions:** small, large  
**Source:** https://msnews.github.io/

MIcrosoft News Dataset (MIND) is a large-scale dataset for news recommendation research.

---

## Citation

```bibtex
@inproceedings{DBLP:conf/acl/WuQCWQLLXGWZ20,
  author       = {Fangzhao Wu and
                  Ying Qiao and
                  Jiun{-}Hung Chen and
                  Chuhan Wu and
                  Tao Qi and
                  Jianxun Lian and
                  Danyang Liu and
                  Xing Xie and
                  Jianfeng Gao and
                  Winnie Wu and
                  Ming Zhou},
  title        = {{MIND:} {A} Large-scale Dataset for News Recommendation},
  booktitle    = {{ACL}},
  pages        = {3597--3606},
  publisher    = {Association for Computational Linguistics},
  year         = {2020}
}
```

---

## Version: small

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| train_archive | ManualSource | zip |  | md5:bd6ae77fa15949653f39829e946d327c |
| validation_archive | ManualSource | zip |  | md5:1c9e798fe440c1999547211cd5245e3e |

---

### Resources

#### train

- **Type:** interactions
- **Format:** `sequence_tabular_inline`
- **Required:** yes
- **Source:** `train_archive`
- **Filename:** `behaviors.tsv`

**Schema**

```yaml
user_col: user
sequence_col: sequence
timestamp_col: time
cols:
- impression_id
- user
- time
- sequence
- impressions
col_sep: "\t"
sequence_sep: ' '
```

#### validation

- **Type:** interactions
- **Format:** `sequence_tabular_inline`
- **Source:** `validation_archive`
- **Filename:** `behaviors.tsv`

**Schema**

```yaml
user_col: user
sequence_col: sequence
timestamp_col: time
cols:
- impression_id
- user
- time
- sequence
- impressions
col_sep: "\t"
sequence_sep: ' '
```

---

## Dataset Characteristics

Computed at: **2025-12-16**

| Metric | Value |
|---|---|
| n_users | 49108 |
| n_items | 33195 |
| n_interactions | 5107630 |
| space_size | 40.37499300309537 |
| space_size_log | 1.6061124600768104 |
| shape | 1.4793794246121403 |
| shape_log | 0.17007957418774253 |
| density | 0.00313324610892637 |
| density_log | -2.5040054909941873 |
| gini_item | 0.8403493747706466 |
| gini_user | 0.7792197590761297 |
| ratings_per_user | 104.00810458581087 |
| ratings_per_item | 153.8674499171562 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://msnews.github.io/

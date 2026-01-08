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

## Version: large

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| train_archive | ManualSource | zip |  | md5:0bfe5f08404a69b2bd76721e7b7f7d5d |
| validation_archive | ManualSource | zip |  | md5:64b9fc265c16814ba0f470542ef6cd69 |
| test_archive | ManualSource | zip |  | md5:081f0b249f9d7927cb0c78fb37db833a |

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

#### test

- **Type:** interactions
- **Format:** `sequence_tabular_inline`
- **Source:** `test_archive`
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
| n_users | 698365 |
| n_items | 79546 |
| n_interactions | 73629852 |
| space_size | 235.69501965463758 |
| space_size_log | 2.3723504057769302 |
| shape | 8.779385512785055 |
| shape_log | 0.9434641198074959 |
| density | 0.001325418768112102 |
| density_log | -2.8776468840317686 |
| gini_item | 0.9249633473855028 |
| gini_user | 0.778868062516292 |
| ratings_per_user | 105.43176132824526 |
| ratings_per_item | 925.6260779926081 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://msnews.github.io/

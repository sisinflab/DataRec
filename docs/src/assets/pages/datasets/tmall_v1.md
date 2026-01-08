# Tmall

## Overview

**Dataset name:** Tmall  
**Latest version:** v1  
**Available versions:** v1  
**Source:** https://tianchi.aliyun.com/dataset/42

This dataset is from IJCAI 2015 Contest: https://tianchi.aliyun.com/competition/entrance/231674/information
The data set contains anonymized users' shopping logs in the past 6 months before and on the "Double 11" day,and the label information indicating whether they are repeated buyers. 
Due to privacy issue, data is sampled in a biased way, so the statistical result on this data set would deviate from the actual of Tmall.com.

---

## Citation

```bibtex
@misc{
    title={IJCAI-15 Repeat Buyers Prediction Dataset}
    url={https://tianchi.aliyun.com/dataset/dataDetail?dataId=42},
    author={Tianchi},
    year={2018}
    }
```

---

## Version: v1

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| main_archive | ManualSource | zip |  | md5:b8143773b800c7420b201d04bc7a9c15 |

---

### Resources

#### train

- **Type:** interactions
- **Format:** `sequence_tabular_inline`
- **Required:** yes
- **Source:** `main_archive`
- **Filename:** `train_format2.csv`

**Schema**

```yaml
cols:
- user_id
- age_range
- gender
- merchant_id
- label
- activity_log
user_col: user_id
sequence_col: activity_log
col_sep: ','
sequence_sep: '#'
header: 0
```

#### test

- **Type:** interactions
- **Format:** `sequence_tabular_inline`
- **Source:** `main_archive`
- **Filename:** `train_format2.csv`

**Schema**

```yaml
cols:
- user_id
- age_range
- gender
- merchant_id
- label
- activity_log
user_col: user_id
sequence_col: activity_log
col_sep: ','
sequence_sep: '#'
header: 0
```

---

## Dataset Characteristics

Computed at: **2025-12-16**

| Metric | Value |
|---|---|
| n_users | 212062 |
| n_items | 9790396 |
| n_interactions | 27384139 |
| space_size | 1440.8924167168068 |
| space_size_log | 3.1586315557130478 |
| shape | 0.02166020659429915 |
| shape_log | -1.6643374054052402 |
| density | 1.318973223933264e-05 |
| density_log | -4.879764020841857 |
| gini_item | 0.5585949565188277 |
| gini_user | 0.5412012856445343 |
| ratings_per_user | 129.13270175703332 |
| ratings_per_item | 2.797040998137358 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://tianchi.aliyun.com/dataset/42

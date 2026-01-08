# Yelp

## Overview

**Dataset name:** Yelp  
**Latest version:** v1  
**Available versions:** v1  
**Source:** https://business.yelp.com/data/resources/open-dataset/

The Yelp dataset is a subset of Yelp's businesses, reviews, and user data for academic research.

---

## Citation

_No citation provided._

---

## Version: v1

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| main_archive | ManualSource | zip |  | md5:b0c36fe2d00a52d8de44fa3b2513c9d2 |
| data_archive | NestedSource | tar |  | md5:0bc8cc1481ccbbd140d2aba2909a928a |

---

### Resources

#### review

- **Type:** interactions
- **Format:** `transactions_jsonl`
- **Required:** yes
- **Source:** `data_archive`
- **Filename:** `yelp_academic_dataset_review.json`

**Schema**

```yaml
user_col: user_id
item_col: business_id
rating_col: stars
timestamp_col: date
```

#### business

- **Type:** content
- **Format:** `json`
- **Source:** `data_archive`
- **Filename:** `yelp_academic_dataset_business.json`

#### checkin

- **Type:** content
- **Format:** `json`
- **Source:** `data_archive`
- **Filename:** `yelp_academic_dataset_checkin.json`

#### tip

- **Type:** content
- **Format:** `json`
- **Source:** `data_archive`
- **Filename:** `yelp_academic_dataset_tip.json`

#### user

- **Type:** content
- **Format:** `json`
- **Source:** `data_archive`
- **Filename:** `yelp_academic_dataset_user.json`

#### terms_of_use

- **Type:** content
- **Format:** `pdf`
- **Source:** `data_archive`
- **Filename:** `Dataset_User_Agreement.pdf`

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 1987929 |
| n_items | 150346 |
| n_interactions | 6990280 |
| space_size | 546.6966008985239 |
| space_size_log | 2.737746373661808 |
| shape | 13.222360421960012 |
| shape_log | 1.1213089912105905 |
| density | 2.3388470653961263e-05 |
| density_log | -4.630998175294749 |
| gini_item | 0.678351072470664 |
| gini_user | 0.6115362253305341 |
| ratings_per_user | 3.51636300894046 |
| ratings_per_item | 46.49461907865856 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://business.yelp.com/data/resources/open-dataset/

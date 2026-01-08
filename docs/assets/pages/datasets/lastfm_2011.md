# LastFM

## Overview

**Dataset name:** LastFM  
**Latest version:** 2011  
**Available versions:** 2011  
**Source:** https://grouplens.org/datasets/hetrec-2011/

Last.fm dataset provided for the 2nd International Workshop on Information Heterogeneity and Fusion in Recommender Systems (HetRec 2011). The full archive contains multiple files (user-friends, tags, etc.), but this loader specifically processes the `user_artists.dat` file, which contains artists listened to by each user and a corresponding listening count (`weight`).

---

## Citation

```bibtex
@inproceedings{Cantador:RecSys2011,
   author = {Cantador, Iv\'{a}n and Brusilovsky, Peter and Kuflik, Tsvi},
   title = {2nd Workshop on Information Heterogeneity and Fusion in Recommender Systems (HetRec 2011)},
   booktitle = {Proceedings of the 5th ACM conference on Recommender systems},
   series = {RecSys 2011},
   year = {2011},
   location = {Chicago, IL, USA},
   publisher = {ACM},
   address = {New York, NY, USA},
   keywords = {information heterogeneity, information integration, recommender systems},
}
```

---

## Version: 2011

### Data Sources

| Name | Source type | Archive | URL | Checksum |
|---|---|---|---|---|
| lastfm-2k.zip | HttpSource | zip | https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip | md5:296d61afe4e8632b173fc2dd3be20ce2 |

---

### Resources

#### ratings

- **Type:** interactions
- **Format:** `transactions_tabular`
- **Required:** yes
- **Source:** `lastfm-2k.zip`
- **Filename:** `user_artists.dat`

**Schema**

```yaml
sep: "\t"
user_col: userID
item_col: artistID
rating_col: weight
header: 0
```

#### tags

- **Type:** content
- **Source:** `lastfm-2k.zip`
- **Filename:** `tags.dat`
- **About:** items

#### artists

- **Type:** content
- **Source:** `lastfm-2k.zip`
- **Filename:** `artists.dat`
- **About:** users

#### user_taggedartists

- **Type:** content
- **Source:** `lastfm-2k.zip`
- **Filename:** `user_taggedartists.dat`
- **About:** users

#### user_taggedartists_timestamps

- **Type:** content
- **Source:** `lastfm-2k.zip`
- **Filename:** `user_taggedartists_timestamps.dat`
- **About:** users

#### user_friends

- **Type:** content
- **Source:** `lastfm-2k.zip`
- **Filename:** `user_friends.dat`
- **About:** users

---

## Dataset Characteristics

Computed at: **2025-12-15**

| Metric | Value |
|---|---|
| n_users | 1892 |
| n_items | 17632 |
| n_interactions | 92834 |
| space_size | 5.77578946984739 |
| space_size_log | 0.7616113546187324 |
| shape | 0.10730490018148821 |
| shape_log | -0.969380445105917 |
| density | 0.002782815119924182 |
| density_log | -2.555515645647218 |
| gini_item | 0.7300996009718888 |
| gini_user | 0.01859984137728208 |
| ratings_per_user | 49.06659619450317 |
| ratings_per_item | 5.265086206896552 |

---

## License & Usage

Please refer to the official dataset page for licensing and usage restrictions.
https://grouplens.org/datasets/hetrec-2011/

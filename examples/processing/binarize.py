from datarec.processing.binarizer import Binarize
from datarec.datasets import Movielens


data = Movielens(version="1m").prepare_and_load()

# Keep only positive interactions and drop rating column
flt_positive_implicit = Binarize(threshold=4, keep='positive', drop_rating_col=True)

print(flt_positive_implicit.run(data))

# Keep all interactions and binarize ratings
flt_all_explicit = Binarize(threshold=4, keep='all', drop_rating_col=False, over_threshold=1, under_threshold=0)
print(flt_all_explicit.run(data))

# Keep only negative interactions and binarize ratings
flt_negative = Binarize(threshold=4, keep='negative', drop_rating_col=False, over_threshold=1, under_threshold=0)
print(flt_negative.run(data))

# Legacy implicit behavior (kept for backward compatibility)
flt_legacy_implicit = Binarize(threshold=4, implicit=True)
print(flt_legacy_implicit.run(data))

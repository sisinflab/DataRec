import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.processing.rating import FilterByRatingThreshold, FilterByUserMeanRating


@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'user': [1, 1, 2, 2, 3, 3, 3, 4],
        'item': [10, 20, 30, 40, 50, 60, 70, 80],
        'rating': [5, 2, 3, 4, 1, 5, 2, 4],
        'timestamp': [111, 112, 113, 114, 115, 116, 117, 118]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


def test_filter_by_rating_threshold(sample_data):
    filter_ratings = FilterByRatingThreshold(rating_threshold=3)
    new_datarec = filter_ratings.run(sample_data)

    assert all(new_datarec.data['rating'] >= 3)
    assert not ((new_datarec.data['user_id'] == 3) & (new_datarec.data['rating'] == 1)).any()


def test_filter_by_rating_threshold_no_filter(sample_data):
    filter_ratings = FilterByRatingThreshold(rating_threshold=1)
    new_datarec = filter_ratings.run(sample_data)

    assert new_datarec.data.equals(sample_data.data)


def test_filter_by_rating_threshold_invalid():
    with pytest.raises(ValueError):
        FilterByRatingThreshold(rating_threshold=-1)


def test_filter_by_user_mean_rating(sample_data):
    filter_mean_ratings = FilterByUserMeanRating()
    new_datarec = filter_mean_ratings.run(sample_data)

    user_means = sample_data.data.groupby('user_id')['rating'].mean()

    for _, row in new_datarec.data.iterrows():
        assert row['rating'] >= user_means[row['user_id']]


def test_filter_by_user_mean_rating_no_filter(sample_data):
    new_data = pd.DataFrame({
        'user': [1, 1, 2, 2, 3, 3],
        'item': [10, 20, 30, 40, 50, 60],
        'rating': [3, 3, 4, 4, 5, 5],
        'timestamp': [111, 112, 113, 114, 115, 116]
    })
    new_datarec = DataRec(RawData(new_data, user='user', item='item', rating='rating', timestamp='timestamp'))

    filter_mean_ratings = FilterByUserMeanRating()
    filtered_datarec = filter_mean_ratings.run(new_datarec)

    assert filtered_datarec.data.equals(new_datarec.data)


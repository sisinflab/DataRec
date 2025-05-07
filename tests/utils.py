import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def dummy_random_dataset():
    # Parameters for the dummy dataset
    num_users = 10  # Number of unique users
    num_items = 15  # Number of unique items
    num_ratings = 50  # Total number of ratings
    start_date = datetime(2023, 1, 1)  # Start date for timestamps
    end_date = datetime(2023, 12, 31)  # End date for timestamps

    # Generate random data
    np.random.seed(42)  # For reproducibility
    user_ids = np.random.randint(1, num_users + 1, size=num_ratings)
    item_ids = np.random.randint(1, num_items + 1, size=num_ratings)
    ratings = np.random.randint(1, 6, size=num_ratings)  # Ratings between 1 and 5
    timestamps = [
        start_date + timedelta(seconds=np.random.randint(0, int((end_date - start_date).total_seconds())))
        for _ in range(num_ratings)
    ]

    # Create a DataFrame
    dummy_df = pd.DataFrame({
        "user_id": user_ids,
        "item_id": item_ids,
        "rating": ratings,
        "timestamp": timestamps
    })

    return dummy_df


def dummy_fixed_dataset():
    data = {
        "user_id": [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        "item_id": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        "rating": [5, 4, 3, 5, 2, 3, 4, 2, 5, 1],
        "timestamp": [
            "2023-01-01 10:00:00",
            "2023-01-02 12:00:00",
            "2023-01-03 14:00:00",
            "2023-01-04 16:00:00",
            "2023-01-05 18:00:00",
            "2023-01-06 10:30:00",
            "2023-01-07 11:00:00",
            "2023-01-08 12:30:00",
            "2023-01-09 14:15:00",
            "2023-01-10 15:45:00",
        ]
    }

    return {
        'data': pd.DataFrame(data),
        'user': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        'item': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
        'rating': [5, 4, 3, 5, 2, 3, 4, 2, 5, 1],
        'timestamp': [
            "2023-01-01 10:00:00",
            "2023-01-02 12:00:00",
            "2023-01-03 14:00:00",
            "2023-01-04 16:00:00",
            "2023-01-05 18:00:00",
            "2023-01-06 10:30:00",
            "2023-01-07 11:00:00",
            "2023-01-08 12:30:00",
            "2023-01-09 14:15:00",
            "2023-01-10 15:45:00"],
        'len': 10}

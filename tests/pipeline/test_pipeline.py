import pytest
import pandas as pd
from datarec import DataRec, RawData
from datarec.processing import (Binarize,
                                ColdFilter,
                                UserKCore,
                                ItemKCore,
                                UserItemIterativeKCore,
                                UserItemNRoundsKCore,
                                FilterByRatingThreshold,
                                FilterByUserMeanRating,
                                FilterByTime)

from datarec.splitters import (RandomHoldOut,
                               TemporalHoldOut,
                               TemporalThresholdSplit,
                               UserStratifiedHoldOut,
                               LeaveNOut,
                               LeaveOneOut,
                               LeaveRatioOut,
                               LeaveNLast,
                               LeaveRatioLast,
                               LeaveOneLast)


PROCESSORS = [
    # (ProcessorClass, init_params, expected_operation_name)
    (Binarize, {'threshold': 3.0, 'keep': 'positive', 'drop_rating_col': True, 'over_threshold': 1, 'under_threshold': 0}),
    (ColdFilter, {'interactions': 2, 'mode': 'user'}),
    (UserKCore, {'core': 2}),
    (ItemKCore, {'core': 2}),
    (UserItemIterativeKCore, {'user_core': 2, 'item_core': 2}),
    (UserItemNRoundsKCore, {'user_core': 2, 'item_core': 2, 'rounds': 2}),
    (FilterByRatingThreshold, {'rating_threshold': 2}),
    #(FilterByUserMeanRating, {}), #TODO: manage classes whithout parameters
    (FilterByTime, {'time_threshold': 0, 'drop': 'after'})
]



@pytest.fixture
def sample_data():
    data = pd.DataFrame({
        'user': [1, 1, 2, 3, 3, 3, 4],
        'item': [10, 20, 30, 40, 50, 70, 70],
        'rating': [5, 4, 3, 5, 2, 1, 4],
        'timestamp': [111, 112, 113, 114, 115, 116, 117]
    })
    return DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


@pytest.mark.parametrize("processor_class, params", PROCESSORS)
def test_processor_adds_pipeline_step(processor_class, params, sample_data: DataRec):
    original_pipeline_len = len(sample_data.pipeline.steps)

    processor_instance = processor_class(**params)

    result_datarec = processor_instance.run(sample_data)

    assert len(result_datarec.pipeline.steps) == original_pipeline_len + 1
    assert len(sample_data.pipeline.steps) == original_pipeline_len


@pytest.mark.parametrize("processor_class, params", PROCESSORS)
def test_pipeline_step_is_correct(processor_class, params, sample_data: DataRec):
    processor_instance = processor_class(**params)
    result_datarec = processor_instance.run(sample_data)

    last_step = result_datarec.pipeline.steps[-1]

    assert last_step.name == 'process'
    assert last_step.operation == processor_class.__name__
    assert last_step.params == params


def test_processors_chain_pipeline(sample_data):
    processor1 = Binarize(threshold=3)
    datarec1 = processor1.run(sample_data)

    assert len(datarec1.pipeline.steps) == 1
    assert datarec1.pipeline.steps[0].operation == 'Binarize'

    processor2 = ItemKCore(core=2)
    datarec2 = processor2.run(datarec1)

    assert len(datarec2.pipeline.steps) == 2
    assert datarec2.pipeline.steps[0].operation == 'Binarize'
    assert datarec2.pipeline.steps[1].operation == 'ItemKCore'


@pytest.fixture
def sample_data_for_splitting():
    data = pd.DataFrame({
        'user':   [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3],
        'item':   [10, 20, 30, 40, 50, 10, 20, 60, 70, 80, 30, 40, 50, 90, 100],
        'rating':    [5, 4, 3, 2, 1, 5, 4, 3, 2, 1, 5, 4, 3, 2, 1],
        'timestamp': [101, 102, 103, 104, 105, 201, 202, 203, 204, 205, 301, 302, 303, 304, 305]
    })
    return  DataRec(RawData(data, user='user', item='item', rating='rating', timestamp='timestamp'))


SPLITTERS = [
    (RandomHoldOut, {'test_ratio': 0.2, 'val_ratio': 0.1, 'seed': 42}),
    (TemporalHoldOut, {'test_ratio': 0.2, 'val_ratio': 0.1}),
    (TemporalThresholdSplit, {'val_threshold': 105, 'test_threshold': 205}),
    (UserStratifiedHoldOut, {'test_ratio': 0.1, 'val_ratio': 0.1, 'seed': 42}),
    (LeaveNOut, {'test_n': 1, 'validation_n': 1, 'seed': 42}),
    (LeaveOneOut, {'test': True, 'validation': True, 'seed': 42}),
    (LeaveRatioOut, {'test_ratio': 0.2, 'val_ratio': 0.1, 'seed': 42}),
    (LeaveNLast, {'test_n': 1, 'validation_n': 1, 'seed': 42}),
    (LeaveRatioLast, {'test_ratio': 0.2, 'val_ratio': 0.1, 'seed': 42}),
    (LeaveOneLast, {'test': True, 'validation': True, 'seed': 42})
]

@pytest.mark.parametrize("splitter_class, params", SPLITTERS)
def test_splitter_adds_pipeline_step_to_all_outputs(splitter_class, params, sample_data_for_splitting):
    original_pipeline_len = len(sample_data_for_splitting.pipeline.steps)

    splitter_instance = splitter_class(**params)
    result_dict = splitter_instance.run(sample_data_for_splitting)

    assert isinstance(result_dict, dict)
    assert len(result_dict) > 0

    for split_name, result_datarec in result_dict.items():
        assert isinstance(result_datarec, DataRec)
        assert len(result_datarec.pipeline.steps) == original_pipeline_len + 1

    assert len(sample_data_for_splitting.pipeline.steps) == original_pipeline_len


@pytest.mark.parametrize("splitter_class, params", SPLITTERS)
def test_splitter_pipeline_step_is_correct(splitter_class, params, sample_data_for_splitting):
    print("\n\n--- parameters:", splitter_class, params)
    splitter_instance = splitter_class(**params)
    result_dict = splitter_instance.run(sample_data_for_splitting)

    first_split_datarec = list(result_dict.values())[0]
    last_step = first_split_datarec.pipeline.steps[-1]

    assert last_step.name == 'split'
    assert last_step.operation == splitter_class.__name__
    assert last_step.params == params


def test_splitter_chains_after_processor(sample_data_for_splitting):
    processor = UserKCore(core=1)
    processed_datarec = processor.run(sample_data_for_splitting)

    assert len(processed_datarec.pipeline.steps) == 1
    assert processed_datarec.pipeline.steps[0].operation == 'UserKCore'

    splitter = RandomHoldOut(test_ratio=0.25)
    result_dict = splitter.run(processed_datarec)

    train_datarec = result_dict['train']
    test_datarec = result_dict['test']

    assert len(train_datarec.pipeline.steps) == 2
    assert train_datarec.pipeline.steps[0].operation == 'UserKCore'
    assert train_datarec.pipeline.steps[1].operation == 'RandomHoldOut'
    assert train_datarec.pipeline.steps[1].name == 'split'

    assert len(test_datarec.pipeline.steps) == 2
    assert test_datarec.pipeline.steps[0].operation == 'UserKCore'
    assert test_datarec.pipeline.steps[1].operation == 'RandomHoldOut'
    assert test_datarec.pipeline.steps[1].name == 'split'

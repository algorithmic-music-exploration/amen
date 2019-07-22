#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
import numpy as np
import pandas as pd
import pytest

from pandas.util.testing import assert_frame_equal

from amen.audio import Audio
from amen.feature import Feature
from amen.feature import FeatureCollection
from amen.timing import TimeSlice
from amen.utils import example_audio_file
from amen.exceptions import FeatureError

EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)

test_times = np.linspace(0, 10, num=1000)
test_index = pd.to_timedelta(test_times, unit='s')

test_dataframe = pd.DataFrame(data=audio.analysis_samples[:1000], index=test_index)
test_feature = Feature(test_dataframe)


def test_data_validation():
    with pytest.raises(AssertionError):
        f = Feature([1, 2, 3])


def test_data():
    assert_frame_equal(test_feature.data, test_dataframe)


def test_default_aggregate():
    assert test_feature.aggregate == np.mean


def test_default_base():
    assert test_feature.base == None


def test_default_name():
    assert test_feature.name == test_dataframe.keys()[0]


def test_aggregate():
    test_feature = Feature(test_dataframe, aggregate=np.median)
    assert test_feature.aggregate == np.median


def test_base():
    base_feature = Feature(test_dataframe)
    test_feature = Feature(test_dataframe, base=base_feature)
    assert test_feature.base == base_feature


def test_base_validation():
    with pytest.raises(AssertionError):
        f = Feature(test_dataframe, np.mean, [1, 2, 3])


# Test list wrappers
def test_iter():
    looped_data = []
    for d in test_feature:
        looped_data.append(d)
    assert looped_data == test_feature.data[test_feature.name].tolist()


def test_getitem():
    assert test_feature[0] == test_feature.data[test_feature.name][0]


# Test __repr__
def test_repr():
    repr_string = '<Feature, {0}>'.format((test_feature.name))
    assert test_feature.__repr__() == repr_string


# Test at()
time_slices = [TimeSlice(0, 0.5, audio), TimeSlice(1, 0.5, audio)]
feature_at = test_feature.at(time_slices)

test_slice = time_slices[0]
slice_index = (test_slice.time <= test_feature.data.index) & (
    test_feature.data.index < test_slice.time + test_slice.duration
)
target_data = test_feature.aggregate(test_feature.data[slice_index], axis=0)


def test_default_aggregate():
    assert feature_at.aggregate == test_feature.aggregate


def test_default_base():
    assert feature_at.base == test_feature


def test_default_data():
    assert feature_at.data.loc[test_slice.time].all() == target_data.all()


def test_default_length():
    assert len(feature_at.data) == len(time_slices)


def test_base_with_second_resample():
    feature_again = feature_at.at(time_slices[0])
    assert feature_at.base == test_feature


def test_base_with_second_resample():
    feature_again = feature_at.at(time_slices[0])
    assert feature_again.data.loc[test_slice.time].all() == target_data.all()


def test_with_single_slice():
    feature_at = test_feature.at(time_slices[0])
    assert len(feature_at.data) == 1


# Test with_time
def test_with_time_raises():
    def test():
        with pytest.raises(FeatureError):
            for beat, feature in test_feature.with_time():
                pass


def test_with_time_beats():
    beats = []
    for beat, feature in feature_at.with_time():
        beats.append(beat)
    assert beats == time_slices


def test_with_time_features():
    looped_features = []
    for feature in feature_at:
        looped_features.append(feature)

    features = []
    for beat, feature in feature_at.with_time():
        features.append(feature)
    assert features == looped_features


# Test FeatureCollection
feature_collection = FeatureCollection()
feature_collection['test'] = test_feature
feature_collection['another_test'] = test_feature


def test_iter():
    looped_data = []
    for data in feature_collection:
        looped_data.append(data)

    test_data = []
    length = len(test_feature)
    for i in range(length):
        res = {}
        for key, feature in feature_collection.items():
            res[key] = feature.data[feature.name][i]
            test_data.append(res)
        assert res == looped_data[i]


def test_len():
    key = list(feature_collection.keys())[0]
    length = len(feature_collection[key])
    assert len(feature_collection) == length


def test_at():
    feature_collection_at = feature_collection.at(time_slices)
    assert (
        feature_collection_at['test'].data.loc[test_slice.time].all()
        == target_data.all()
    )


def test_get():
    # Casting to list for Python 3
    new_feature_collection = feature_collection.get('another_test')
    assert list(new_feature_collection.keys()) == ['another_test']


def test_get_with_list():
    # Casting to list for Python 3
    new_feature_collection = feature_collection.get(['another_test'])
    assert list(new_feature_collection.keys()) == ['another_test']


# Test with_time
def test_feature_collection_with_time_raises():
    def test():
        with pytest.raises(FeatureError):
            for beat, feature in feature_collection.with_time():
                pass


def test_feature_collection_with_time_beats():
    feature_collection_at = feature_collection.at(time_slices)
    beats = []
    for beat, feature in feature_collection_at.with_time():
        beats.append(beat)
    assert beats == time_slices


def test_feature_collection_with_time_features():
    feature_collection_at = feature_collection.at(time_slices)
    looped_features = []
    for feature in feature_collection_at:
        looped_features.append(feature)

    features = []
    for beat, feature in feature_collection_at.with_time():
        features.append(feature)
    assert features == looped_features

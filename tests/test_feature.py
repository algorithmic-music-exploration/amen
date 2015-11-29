#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
import numpy as np
import pandas as pd

from nose.tools import assert_raises
from pandas.util.testing import assert_frame_equal

from amen.audio import Audio
from amen.feature import Feature
from amen.feature import FeatureCollection
from amen.time import TimeSlice
from amen.utils import example_audio_file

EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)

test_times = np.linspace(0, 10, num=1000)
test_index = pd.to_timedelta(test_times, unit='s')
test_data = np.swapaxes(audio.raw_samples[0:1, 0:1000], 0, 1)

test_dataframe = pd.DataFrame(data=test_data, index=test_index)
test_feature = Feature(test_dataframe)

# Test init
def test_data_validation():
    # Makes sure that we can't pass lousy data.
    assert_raises(AssertionError, Feature, [1, 2, 3])

def test_data():
    assert_frame_equal(test_feature.data, test_dataframe)

def test_default_aggregate():
    assert(test_feature.aggregate == np.mean)

def test_default_base():
    assert(test_feature.base == None)

def test_aggregate():
    test_feature = Feature(test_dataframe, aggregate=np.median)
    assert(test_feature.aggregate == np.median)

def test_base():
    base_feature = Feature(test_dataframe)
    test_feature = Feature(test_dataframe, base=base_feature)
    assert(test_feature.base == base_feature)

def test_base_validation():
    assert_raises(AssertionError, Feature, test_dataframe, np.mean, [1, 2, 3])


# Test at()
time_slices = [TimeSlice(0, 0.5), TimeSlice(1, 0.5)]
feature_at = test_feature.at(time_slices)

test_slice = time_slices[0]
slice_index = ((test_slice.time <= test_feature.data.index) &
              (test_feature.data.index < test_slice.time + test_slice.duration))
target_data = test_feature.aggregate(test_feature.data[slice_index], axis=0)

def test_default_aggregate():
    assert(feature_at.aggregate == test_feature.aggregate)

def test_default_base():
    assert(feature_at.base == test_feature)

def test_default_data():
    assert(feature_at.data.loc[test_slice.time].all() == target_data.all())

def test_default_length():
    assert(len(feature_at.data) == len(time_slices))

def test_base_with_second_resample():
    feature_again = feature_at.at(time_slices[0])
    assert(feature_at.base == test_feature)

def test_base_with_second_resample():
    feature_again = feature_at.at(time_slices[0])
    assert(feature_again.data.loc[test_slice.time].all() == target_data.all())

def test_with_single_slice():
    feature_at = test_feature.at(time_slices[0])
    assert(len(feature_at.data) == 1)

# Test FeatureCollection
feature_collection = FeatureCollection()
feature_collection['test'] = test_feature
feature_collection['another_test'] = test_feature

def test_at():
    feature_collection_at = feature_collection.at(time_slices)
    assert(feature_collection_at['test'].data.loc[test_slice.time].all() == target_data.all())

def test_get():
    new_feature_collection = feature_collection.get('another_test')
    assert(new_feature_collection.keys() == ['another_test'])

def test_get_with_list():
    new_feature_collection = feature_collection.get(['another_test'])
    assert(new_feature_collection.keys() == ['another_test'])


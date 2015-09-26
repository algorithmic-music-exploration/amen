#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
import numpy as np
import pandas as pd

from nose.tools import assert_raises
from pandas.util.testing import assert_frame_equal

from amen.audio import Audio
from amen.utils import example_audio_file
from amen.feature import Feature

EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)
test_dataframe = pd.DataFrame(audio.raw_samples[0:10])
test_feature = Feature(test_dataframe)

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


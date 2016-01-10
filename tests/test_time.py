#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.time import TimeSlice

t = 5
d = 10
dummy_audio = None


time_slice = TimeSlice(t, d, dummy_audio)

def test_time():
    assert(time_slice.time == pd.to_timedelta(t, 's'))

def test_duration():
    assert(time_slice.duration == pd.to_timedelta(d, 's'))

def test_units():
    time_slice = TimeSlice(t, d, dummy_audio, unit='ms')
    assert(time_slice.time == pd.to_timedelta(t, 'ms'))

def test_get_offsets():
    faux_audio = np.array([[1,-1, 0, 1, 0, -1, 1],
                           [0, 0, 0, 0, 0, 0, 0]])
    time_slice = TimeSlice(t, d, None)
    res = time_slice._get_offsets(faux_audio[0], 3, 4)
    assert(res == (-1, 1))


# need tests for get_samples!
EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)

def test_offset_samples():
    res = audio.timings['beats'][0]._offset_samples(1, 2, (-1, 1), (-1, 1))
    assert(res.shape == (2, 3))

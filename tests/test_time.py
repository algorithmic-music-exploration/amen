#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import librosa
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

samples, left_offset, right_offset  = audio.timings['beats'][5].get_samples()
def test_get_samples_shape():
    duration = audio.timings['beats'][5].duration.delta * 1e-9
    starting_sample, ending_sample = librosa.time_to_samples([0, duration], audio.sample_rate)

    initial_length = ending_sample -starting_sample
    left_offset_length = initial_length - left_offset[0] + left_offset[1]
    right_offset_length = initial_length - right_offset[0] + right_offset[1]

    assert(len(samples[0]) == left_offset_length)
    assert(len(samples[1]) == right_offset_length)

def test_get_samples_audio():
    start = left_offset[0] * -1
    end = len(samples[0]) - left_offset[1]
    reset_samples = samples[0][start : end]

    start = audio.timings['beats'][5].time.delta * 1e-9
    duration = audio.timings['beats'][5].duration.delta * 1e-9
    starting_sample, ending_sample = librosa.time_to_samples([start, start + duration], audio.sample_rate)
    original_samples = audio.raw_samples[0, starting_sample : ending_sample]

    assert(np.array_equiv(reset_samples, original_samples))

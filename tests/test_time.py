#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
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


# need tests for _offset_samples, get_samples, and _get_offsets 

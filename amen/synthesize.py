#!/usr/bin/env python
# -*- coding: utf-8 -*-

import types
import librosa
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from amen.audio import Audio
from amen.time import TimingList
from amen.exceptions import SynthesizeError

def synthesize(inputs):
    """
    Function to generate new Audios for output or further remixing

    This currently takes too many damn things.
    We eventually get to a list/generator that outputs (TimeSlice, time)

    synthesize(time_slices)
    # assumes a single list of time slices, that should play back-to-back.  
    # it is our job to find the timings and zip them to be a list of (ts, t)

    synthesize((time_slices, timings))
    # assumes a tuple of slices and times, as parallel lists.
    # it is our job zip them

    # should we also support lists of tuples, zipped by the user?  aiii...

    synthesize(some_generator(time_slices))
    # assumes a generator that returns tuples of slices and times

    """

    # First we organize our inputs.
    proper_list = []
    if type(inputs) == TimingList or type(inputs) == list:
        time_index = pd.to_timedelta(0.0, 's')
        timings = []
        for time_slice in inputs:
            timings.append(time_index)
            time_index = time_index + time_slice.duration
        proper_list = zip(inputs, timings)
    elif type(inputs) == tuple:
        proper_list = zip(inputs[0], inputs[1])
    elif isinstance(inputs, types.GeneratorType):
        proper_list = inputs

    max_time = 0.0
    array_length = 20 * 60 # 20 minutes!
    array_shape = (2, 44100 * array_length)
    sparse_array = csr_matrix(array_shape)

    for time_slice, start_time in proper_list:
        start_time = start_time.delta * 1e-9
        duration = time_slice.duration.delta * 1e-9
        if start_time + duration > max_time:
            max_time = start_time + duration
        elif start_time + duration > array_length
            raise SynthesizeError("Amen can only synthesize up to 20 minutes of audio.")

        resampled_audio = time_slice.get_samples()

        # get the right samples in the sparse array.
        sample_index = librosa.time_to_samples([start_time, start_time + duration], sr=time_slice.audio.sample_rate)
        target = sparse_array[:, sample_index[0]:sample_index[1]]
        target += resampled_audio


    max_samples = librosa.time_to_samples([max_time], sr=time_slice.audio.sample_rate)
    truncated_array = sparse_array[:, 0:max_samples]
    output = Audio(raw_samples=truncated_array)
    return output

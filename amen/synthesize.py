#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
import pandas as pd
import numpy as np
from amen.audio import Audio

def synthesize(inputs):
    """
    Function to generate new Audios that can easily be written to disk

    synthesize(time_slices) # assumes a single list or generator that just return beats
    synthesize((time_slices, timings)) # assumes a tuple of slices and times, or a generator that returns audio and times
    synthesize([(ts1, t1), (ts2, t2), ...]) # assumes a list of tuples, or a list of generators

    ?where and how do we do the resample?
    """

    # First we organize our inputs.
    # We want to end up with a list of tuples / generators that give tuples, 
    # regardless of the input type
    tuple_list = []
    if type(inputs) == list:
        tuple_list = inputs
    elif type(inputs) == tuple:
        tuple_list = [inputs]
    else:
        time_index = 0.0
        timings = []
        for time_slice in inputs:
            timings.append(time_index)
            time_index = time_index + time_slice.duration.delta * 1e-9
        tuple_list = [(inputs, timings)]

    max_time = 0.0
    array_shape = (2, 22050 * 60 * 20)
    sparse_array = np.zeros(array_shape)

    for time_slices, timings in tuple_list:
        for index, time_slice in enumerate(time_slices):
            start_time = timings[index] # parallel lists: note that timings is in seconds
            duration = time_slice.duration.delta * 1e-9

            # check to see where we need to truncate our array to
            if start_time + duration > max_time:
                max_time = start_time + duration

            resampled_audio = time_slice.get_samples() 

            # get the right samples in the sparse array.
            # what about clipping, etc?  also need to try/catch array out of bound things here
            sample_index = librosa.time_to_samples([start_time, start_time + duration]) 
            target = sparse_array[:, sample_index[0]:sample_index[1]]
            print "----"
            print index, start_time, duration, sample_index[0], sample_index[1]
            print len(target[0]), len(resampled_audio[0])
            target += resampled_audio


    max_samples = librosa.time_to_samples([max_time])
    truncated_array = sparse_array[:, 0:max_samples]
    output = Audio(raw_samples=truncated_array)
    return output

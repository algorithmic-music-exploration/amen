#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
import pandas as pd
import numpy as np

def synthesize(inputs):
    """
    Function to generate new arrays of audio that we can then write to disk.

    synthesize(time_slices) # assumes a single list with no silences
    synthesize((time_slices, timings)) # assumes a tuple of slices and times
    synthesize([(ts1, t1), (ts2, t2), ...]) # assumes a list of tuples
    """

    # First we organize our inputs
    tuple_list = []
    if type(inputs) == list:
        tuple_list = inputs
    elif type(inputs) == tuple
        tuple_list = [inputs]
    else
        time_index = 0.0
        timings = []
        for time_slice in inputs:
            timings.append(time_index)
            time_index = time_index + time_slice.duration
        tuple_list = [(inputs, timings)]

    # now we do the same thing to everything
    sparse_array = np.zeros(2, (44100 * 60 * 20)) # stereo, 44.1, 20 minutes max
    for (time_slices, timings) in tuple_list:
        for index in range(len(time_slices)): # parallel lists!
            time_slice = time_slices[index]
            start_time = start_times[index]
            resampled_audio = time_slice.get_audio() # need this function and the resample!
            ## what about clipping, etc?  also need to try/catch array out of bound things here
            sparse_array[start_time.to_samples] += resample_audio


    # truncate the array
    an_array = truncate(sparse_array)
    return an_array


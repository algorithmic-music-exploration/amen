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
    elif type(inputs) == tuple:
        tuple_list = [inputs]
    else:
        time_index = 0.0
        timings = []
        for time_slice in inputs:
            timings.append(time_index)
            time_index = time_index + time_slice.duration.delta * 1e-9
        tuple_list = [(inputs, timings)]

    # Get the maximum size we'll need
    max_time = 0.0
    for (time_slices, timings) in tuple_list:
        for index in range(len(time_slices)):
            time_slice = time_slices[index]
            start_time = timings[index]
            duration = time_slice.duration.delta * 1e-9

            if start_time + duration > max_time:
                max_time = start_time + duration

    max_samples = librosa.time_to_samples([max_time])
     
    # now we do the same thing to everything
    # where and how do we do the resample?
    sparse_array = np.zeros((2, max_samples))
    for (time_slices, timings) in tuple_list:
        for index in range(len(time_slices)): # parallel lists: note that timings is in seconds
            time_slice = time_slices[index]
            start_time = timings[index]

            resampled_audio = time_slice.get_samples() 

            # get the right samples in the sparse array.
            # what about clipping, etc?  also need to try/catch array out of bound things here
            duration = time_slice.duration.delta * 1e-9
            sample_index = librosa.time_to_samples([start_time, start_time + duration]) 
            target = sparse_array[:, sample_index[0]:sample_index[1]]
            print "----"
            print index, start_time, duration, sample_index[0], sample_index[1]
            print len(target[0]), len(resampled_audio[0])
            target += resampled_audio

    return sparse_array

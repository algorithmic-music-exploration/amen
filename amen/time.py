#!/usr/bin/env python

import six
from bisect import bisect_left
from bisect import bisect_right
import librosa
import numpy as np
import pandas as pd

class TimeSlice(object):
    """
    A slice of time:  has a start time, a duration, and a reference to an Audio object.
    """

    def __init__(self, time, duration, audio, unit='s'):
        self.time = pd.to_timedelta(time, unit=unit)
        self.duration = pd.to_timedelta(duration, unit=unit)
        self.audio = audio

    def __repr__(self):
        args = self.time.delta * 1e-9, self.duration.delta * 1e-9
        return '<TimeSlice, start: {0:.2f}, duration: {1:.2f}>'.format(*args)

    def get_samples(self):
        """
        Gets the samples corresponding to this TimeSlice from the parent audio object.
        """
        start = self.time.delta * 1e-9
        duration = self.duration.delta * 1e-9
        starting_sample, ending_sample = librosa.time_to_samples([start, start + duration], self.audio.sample_rate)

        left_offsets, right_offsets = self._get_offsets(starting_sample, ending_sample)

        samples = self._offset_samples(starting_sample, ending_sample, left_offsets, right_offsets)

        return samples, left_offsets, right_offsets

    def _get_offsets(self, starting_sample, ending_sample):
        left_offsets = ()
        right_offsets = ()
        for channel_index in [0, 1]:
            channel = self.audio.raw_samples[channel_index]
            zero_crossings = librosa.zero_crossings(channel)
            zero_indexes = np.nonzero(zero_crossings)[0]
    
            starting_crossing = zero_indexes[bisect_left(zero_indexes, starting_sample) - 1]
            starting_offset = starting_crossing - starting_sample
    
            ending_crossing = zero_indexes[bisect_right(zero_indexes, ending_sample)]
            ending_offset = ending_crossing - ending_sample
            if channel_index == 0:
                left_offsets = (starting_offset, ending_offset)
            elif channel_index == 1:
                right_offsets = (starting_offset, ending_offset)

        return (left_offsets, right_offsets)

    def _offset_samples(self, starting_sample, ending_sample, left_offsets, right_offsets):
        left_channel = self.audio.raw_samples[0, starting_sample + left_offsets[0] : ending_sample + left_offsets[1]]
        right_channel = self.audio.raw_samples[1, starting_sample + right_offsets[0] : ending_sample + right_offsets[1]]
        return np.array([left_channel, right_channel])
        

class TimingList(list):
    """
    A list of TimeSlices.  
    """

    def __init__(self, name, timings, audio, unit='s'):
        self.name = name
        for (start, duration) in timings:
            time_slice = TimeSlice(start, duration, audio, unit=unit)
            self.append(time_slice)


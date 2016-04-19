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

    def get_samples(self, zero_indexes=None):
        """
        Gets the samples corresponding to this TimeSlice from the parent audio object.
        """
        start = self.time.delta * 1e-9
        duration = self.duration.delta * 1e-9
        starting_sample, ending_sample = librosa.time_to_samples([start, start + duration], self.audio.sample_rate)

        left_offsets, right_offsets, zero_indexes = self._get_offsets(starting_sample, 
            ending_sample, self.audio.num_channels, zero_indexes)

        samples = self._offset_samples(starting_sample, ending_sample, left_offsets, right_offsets, self.audio.num_channels)

        return samples, left_offsets[0], right_offsets[0], zero_indexes

    def _get_offsets(self, starting_sample, ending_sample, num_channels, zero_indexes=None):
        """
        Find the offset to the next zero-crossing, for each channel.
        This is where we return the zero indexes, which are cached in synthesize.py
        """
        offsets = []
        if not zero_indexes:
            zero_indexes = []

        for channel_index in range(num_channels):
            channel = self.audio.raw_samples[channel_index]
            # if we don't have zero indexes, make them
            if len(zero_indexes) <= channel_index:
                zero_crossings = librosa.zero_crossings(channel)
                zero_index = np.nonzero(zero_crossings)[0]
                zero_indexes.append(zero_index)
            else:
                zero_index = zero_indexes[channel_index]

            index = bisect_left(zero_index, starting_sample) - 1
            if index < 0:
                starting_offset = 0
            else:
                starting_crossing = zero_index[index]
                starting_offset = starting_crossing - starting_sample
    
            index = bisect_left(zero_index, ending_sample)
            if index >= len(zero_index):
                ending_offset = 0
            else:
                ending_crossing = zero_index[bisect_right(zero_index, ending_sample)]
                ending_offset = ending_crossing - ending_sample

            offsets.append((starting_offset, ending_offset))

        if num_channels == 1:
            results = (offsets[0], offsets[0], zero_indexes)
        elif num_channels == 2:
            results = (offsets[0], offsets[1], zero_indexes)

        return results


    def _offset_samples(self, starting_sample, ending_sample, left_offsets, right_offsets, num_channels):
        """
        Does the offset itself.
        """
        left_channel = self.audio.raw_samples[0, starting_sample + left_offsets[0] : ending_sample + left_offsets[1]]
        if num_channels == 1:
            right_channel = left_channel
        elif num_channels == 2:
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


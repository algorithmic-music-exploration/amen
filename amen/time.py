#!/usr/bin/env python

import six
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
        return '<TimeSlice, start: {0:.2f}, duration: {1:.2f}'.format(*args)

class TimingList(list):
    """
    A list of TimeSlices.  
    """

    def __init__(self, name, timings, audio, unit='s'):
        self.name = name
        for (start, duration) in timings:
            time_slice = TimeSlice(start, duration, audio, unit=unit)
            self.append(time_slice)

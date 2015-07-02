#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TimingList(list):
    """
    A list of TimeSlices.  
    """

    def __init__(self, name, timings, audio):
        # This assumes that we're going to get a list of tuples (start, duration) from librosa,
        # which may or may not be true.
        self.name = name
        for (start, duration) in timings:
            slice = new TimeSlice(start, duration, audio)
            self.append(slice)

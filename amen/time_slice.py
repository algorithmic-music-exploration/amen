#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TimeSlice(object):
    """
    A slice of time:  has a start time, a duration, and a reference to an Audio object.
    """

    def __init__(self, start, duration, audio):
        self.start = start
        self.duration = duration
        self.audio = audio

    # def __str__(self):
    def __repr__(self):
    	return '<TimeSlice, start:{0:.2f}, duration:{1:.2f}'.format(self.start, self.duration)

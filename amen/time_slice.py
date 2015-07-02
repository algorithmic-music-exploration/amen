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

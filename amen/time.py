#!/usr/bin/env python

import six
import numpy as np
import pandas as pd


class TimeSlice(object):
    '''A time slice object'''

    def __init__(self, time, duration, unit='s'):

        self.time = pd.to_timedelta(time, unit=unit)
        self.duration = pd.to_timedelta(duration, unit=unit)

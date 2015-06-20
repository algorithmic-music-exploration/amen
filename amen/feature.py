#!/usr/bin/env python

import six
import numpy as np
import pandas as pd


class Feature(object):
    '''Core feature container object.

    Handles indexing and time-slicing
    '''
    def __init__(self, data, aggregate=np.mean):
        '''
        Parameters
        ----------
        data : pd.DataFrame
            Time-indexed data frame of features

        aggregate : function
            resample-aggregation function

        '''

        # Check that the arguments have the right types
        assert six.isinstance(data, pd.DataFrame)
        assert six.callable(aggregate)

        self.data = data
        self.aggregate = aggregate


    def at(self, time_slices):
        '''Resample the data at a new time slice index.

        Parameters
        ----------
        time_slices : TimeSlice collection
            The time slices at which to index this feature object

        Returns
        -------
        feature_at : Feature
            The resampled feature data
        '''

        # TODO


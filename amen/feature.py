#!/usr/bin/env python
'''Container classes for feature analysis'''

import numpy as np
import pandas as pd
import six

from .timing import TimeSlice
from .exceptions import FeatureError

class Feature(object):
    """
    Core feature container object.  Handles indexing and time-slicing.

    Attributes
    ---------

    Methods
    ------
    at(time_slices)
        Resample the feature at the given TimeSlices
    """
    def __init__(self, data, aggregate=np.mean, base=None, time_slices=None):
        """
        Constructor for feature object

        Parameters
        ----------
        data: pandas.DataFrame
            Time-indexed data frame of features

        aggregate: function
            resample-aggregation function or mapping

        Returns
        ------
        A Feature object
        """

        # Check that the arguments have the right types
        assert isinstance(data, pd.DataFrame)

        self.data = data
        self.aggregate = aggregate
        self.time_slices = time_slices
        # Not sure that this is the right way to do it - I feel like we're outsmarting pandas
        # pandas supports multiple keys in a dataframe, whereas this only allows one.
        # Should we replace FeatureCollection with something like that?
        self.name = data.keys()[0]

        if base is not None:
            assert isinstance(base, Feature)

        self.base = base

    def __repr__(self):
        args = (self.name)
        return '<Feature, {0}>'.format(args)

    def __iter__(self):
        """
        Wrapper to allow easy access to the internal data of the pandas dataframe
        """
        for datum in self.data[self.name]:
            yield datum

    def __getitem__(self, x):
        """
        Wrapper to allow easy access to the internal data of the pandas dataframe
        """
        return self.data[self.name][x]

    def __len__(self):
        """
        Wrapper to allow easy access to the internal data of the pandas dataframe
        """
        return len(self.data[self.name])

    def with_time(self):
        """
        Allows iteration over a time-indexed feature and the associated timeslices.
        """
        if self.time_slices is None:
            raise FeatureError("Feature has no time reference.")

        for i, datum in enumerate(self.data[self.name]):
            yield (self.time_slices[i], datum)

    def at(self, time_slices):
        """
        Resample the data at a new time slice index.

        Parameters
        ----------
        time_slices: TimeSlice or TimeSlice collection
            The time slices at which to index this feature object

        Returns
        -------
        Feature
            The resampled feature data
        """

        if self.base is not None:
            return self.base.at(time_slices)

        if isinstance(time_slices, TimeSlice):
            time_slices = [time_slices]

        # join the time slice values
        timed_data = pd.DataFrame(columns=self.data.columns)

        # make the new data
        for slice_t in time_slices:
            slice_index = ((slice_t.time <= self.data.index) &
                           (self.data.index < slice_t.time + slice_t.duration))
            timed_data.loc[slice_t.time] = self.aggregate(self.data[slice_index], axis=0)

        # return the new feature object
        return Feature(data=timed_data, aggregate=self.aggregate, base=self, time_slices=time_slices)


class FeatureCollection(dict):
    """
    A dictionary of features.

    Delegates `.at` to the features it contains.

    Allows for selection of multiple keys, which returns a smaller feature collection.
    """

    def at(self, time_slices):
        """
        Resample each feature at a new time slice index.

        Parameters
        ----------
        time_slices : TimeSlice or TimeSlice collection
            The time slices at which to index this feature object

        Returns
        -------
        new_features : FeatureCollection
            The resampled feature data
        """
        new_features = FeatureCollection()
        for key in self.keys():
            new_features[key] = self[key].at(time_slices)
        return new_features

    def __iter__(self):
        """
        Wrapper to avoid making the user deal with parallel lists
        """
        key = list(self.keys())[0]
        length = len(self[key])
        for i in range(length):
            res = {}
            for key, feature in self.items():
                res[key] = feature.data[feature.name][i]
            yield res

    def __len__(self):
        """
        Wrapper to avoid making the user deal with parallel lists
        """
        key = list(self.keys())[0]
        feature = self[key]
        return len(feature)

    def with_time(self):
        """
        Allows iteration over a time-indexed feature and the associated timeslices.
        """
        key = list(self.keys())[0]
        length = len(self[key])
        time_slices = self[key].time_slices

        if time_slices is None:
            raise FeatureError("FeatureCollection has no time reference.")

        for i in range(length):
            res = {}
            for key, feature in self.items():
                res[key] = feature.data[feature.name][i]
            yield (time_slices[i], res)

    def get(self, keys):
        """
        Get a subset of the keys in the correct feature collection

        Parameters
        ----------
        keys : A string or list of strings
            The keys to return from the current feature collection

        Returns
        -------
        new_features : FeatureCollection
            The subset of keys
        """
        if isinstance(keys, six.string_types):
            keys = [keys]

        new_features = FeatureCollection()
        for key in keys:
            if key in self:
                new_features[key] = self[key]
        return new_features


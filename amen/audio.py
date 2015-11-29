#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
import pandas as pd
import numpy as np

from amen.feature import Feature
from amen.feature import FeatureCollection

class Audio(object):
    """
    The base Audio object:  wraps the ouput from librosa, and provides access to features

    Attributes
    ----------
        sample_rate: number
            sample rate
        raw_samples: numpy array
            raw samples from the audio
        num_channels: integer
            number of channels of the audio
        duration: float
            duration, in seconds
        features: dict
            collection of named feature objects
    """

    def __init__(self, file_path, convert_to_mono=False, sample_rate=22050):
        """
        Audio constructor.
        Opens a file path, loads the audio with librosa, and prepares the features

        Parameters
        ----------

        file_path: string
            path to the audio file to load

        convert_to_mono: boolean
            (optional) converts the file to mono on loading

        sample_rate: number > 0 [scalar]
            (optional) sample rate to pass to librosa.


        Returns
        ------
        An Audio object
        """

        self.file_path = file_path
        y, sr = librosa.load(file_path, mono=convert_to_mono, sr=sample_rate)
        self.sample_rate = float(sr)
        self.raw_samples = y
        self.num_channels = y.ndim
        self.duration = librosa.get_duration(y=y, sr=sr)
        self.features = self._create_features()

    def _create_features(self):
        """
        Creates the FeatureCollection, and loads each feature.

        Parameters
        ---------

        Returns
        -----
        FeatureCollection
            FeatureCollection with each Amen.Feature object named correctly
        """
        features = FeatureCollection()
        features['centroid'] = self._get_centroid()
        features['amplitude'] = self._get_amplitude()
        return features

    def _get_centroid(self):
        """
        Gets spectral centroid data from librosa, and returns it as a Feature

        Parameters
        ---------

        Returns
        -----
        Feature 
        """
        mono_samples = librosa.to_mono(self.raw_samples)
        centroids = librosa.feature.spectral_centroid(mono_samples)
        data = self._convert_to_dataframe(centroids, ['spectral_centroid'])
        feature = Feature(data)
        return feature

    def _get_amplitude(self):
        """
        Gets amplitude data from librosa, and returns it as a Feature

        Parameters
        ---------

        Returns
        -----
        Feature 
        """
        mono_samples = librosa.to_mono(self.raw_samples)
        amplitudes = librosa.feature.rmse(mono_samples)
        data = self._convert_to_dataframe(amplitudes, ['amplitude'])
        feature = Feature(data)
        return feature

    def _convert_to_dataframe(self, feature_data, columns):
        """
        Take raw librosa feature data, convert to a pandas dataframe.

        Parameters
        ---------
        feature_data: numpy array
            a N by T array, where N is the number of features, and T is the number of time dimensions

        columns: list [strings]
            a list of column names of length N, the same as the N dimension of feature_data

        Returns
        -----
        pandas.DataFrame        
        """
        feature_data = feature_data.transpose()
        frame_numbers = np.arange(len(feature_data))
        indexes = librosa.frames_to_time(frame_numbers)
        indexes = pd.to_timedelta(indexes, unit='s')
        data = pd.DataFrame(data=feature_data, index=indexes, columns=columns)
        return data


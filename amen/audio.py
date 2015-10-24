#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
import pandas as pd
from amen.feature import Feature

class Audio(object):
    """
    Audio object: should wrap the output from libRosa.
    """

    def __init__(self, file_path, convert_to_mono=False, sample_rate=22050):
        """
        Opens a file path, loads it with librosa.
        """
        self.file_path = file_path
        y, sr = librosa.load(file_path, mono=convert_to_mono, sr=sample_rate)
        self.sample_rate = float(sr)
        self.raw_samples = y
        self.num_channels = y.ndim
        self.duration = librosa.get_duration(y=y, sr=sr)
        self.features = self.create_features()

    def create_features(self):
        """
        Creates the various features in the features dict.
        """
        features = {}
        features['centroid'] = self.get_centroid()
        features['amplitude'] = self.get_amplitude()
        return features

    def get_centroid(self):
        """
        Gets spectral centroid data from librosa and loads it into a feature.
        """
        mono_samples = librosa.to_mono(self.raw_samples)
        centroid = librosa.feature.spectral_centroid(mono_samples)
        centroid = centroid[0]

        frame_numbers = range(len(centroid))
        indexes = librosa.frames_to_time(frame_numbers)
        indexes = pd.to_timedelta(indexes, unit='s')

        data = pd.DataFrame(data=centroid, index=indexes, columns=['spectral_centroid'])
        return data

    def get_amplitude(self):
        """
        Gets amplitude data from librosa and loads it into a feature.
        """
        mono_samples = librosa.to_mono(self.raw_samples)
        amplitudes = librosa.feature.rmse(mono_samples)
        amplitudes = amplitudes[0]
            
        frame_numbers = range(len(amplitudes))
        indexes = librosa.frames_to_time(frame_numbers)
        indexes = pd.to_timedelta(indexes, unit='s')

        data = pd.DataFrame(data=amplitudes, index=indexes, columns=['amplitude'])
        return data





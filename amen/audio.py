#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
import pandas as pd
import numpy as np
from amen.feature import Feature
from amen.time import TimingList

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
        self.timings = self.create_timings()
        self.features = self.create_features()

    def create_timings(self):
        """
        Create timings in a timings dict.
        """
        timings = {}
        timings['beats'] = TimingList('beats', self.get_beats(), self)
        return timings

    def get_beats(self):
        """
        Gets beats using librosa's beat tracker.
        """
        y_mono = librosa.to_mono(self.raw_samples)
        tempo, beat_frames = librosa.beat.beat_track(
            y=y_mono, sr=self.sample_rate, trim=False)

        # convert frames to times
        beat_times = librosa.frames_to_time(beat_frames, sr=self.sample_rate)
        # pad beat times to full duration
        beat_times = librosa.util.fix_frames(beat_times, x_min=None, x_max=self.duration)

        # make the list of (start, duration) tuples that TimingList expects
        starts_durs = [(s, t-s) for (s,t) in zip(beat_times, beat_times[1:])]

        return starts_durs

    def create_features(self):
        """
        Creates the various features in the features dict.
        """
        features = {}
        features['centroid'] = Feature(self.get_centroid())
        features['amplitude'] = Feature(self.get_amplitude())
        return features

    def get_centroid(self):
        """
        Gets spectral centroid data from librosa and loads it into a feature.
        """
        mono_samples = librosa.to_mono(self.raw_samples)
        centroids = librosa.feature.spectral_centroid(mono_samples)
        data = self._convert_to_dataframe(centroids, ['spectral_centroid'])
        return data

    def get_amplitude(self):
        """
        Gets amplitude data from librosa and loads it into a feature.
        """
        mono_samples = librosa.to_mono(self.raw_samples)
        amplitudes = librosa.feature.rmse(mono_samples)
        data = self._convert_to_dataframe(amplitudes, ['amplitude'])

        return data

    def _convert_to_dataframe(self, feature_data, columns):
        """
        Take feature data, convert to a pandas dataframe.
        """
        feature_data = feature_data.transpose()
        frame_numbers = np.arange(len(feature_data))
        indexes = librosa.frames_to_time(frame_numbers)
        indexes = pd.to_timedelta(indexes, unit='s')
        data = pd.DataFrame(data=feature_data, index=indexes, columns=columns)
        return data

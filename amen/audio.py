#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Audio analysis
'''

import os
import pandas as pd
import numpy as np
import soundfile as sf

import librosa

from .feature import Feature, FeatureCollection
from .timing import TimingList

class Audio(object):
    """
    The base Audio object:  wraps the ouput from librosa, and provides access to features

    Attributes
    ----------
        sample_rate: number
            sample rate
        raw_samples: numpy array
            raw samples from the audio
        analysis_samples: numpy array
            downsampled samples for analysis
        num_channels: integer
            number of channels of the audio
        duration: float
            duration, in seconds
        features: dict
            collection of named feature objects
    """

    def __init__(self, file_path=None, raw_samples=None, convert_to_mono=False,
                 sample_rate=44100, analysis_sample_rate=22050):
        """
        Audio constructor.
        Opens a file path, loads the audio with librosa, and prepares the features

        Parameters
        ----------

        file_path: string
            path to the audio file to load

        raw_samples: np.array
            samples to use for audio output

        convert_to_mono: boolean
            (optional) converts the file to mono on loading

        sample_rate: number > 0 [scalar]
            (optional) sample rate to pass to librosa.


        Returns
        ------
        An Audio object
        """

        if file_path:
            y, sr = librosa.load(file_path, mono=convert_to_mono, sr=sample_rate)
        elif raw_samples is not None:
            # This assumes that we're passing in raw_samples
            # directly from another Audio's raw_samples.
            y = raw_samples
            sr = sample_rate

        self.file_path = file_path
        self.sample_rate = float(sr)
        self.analysis_sample_rate = float(analysis_sample_rate)
        self.num_channels = y.ndim
        self.duration = librosa.get_duration(y=y, sr=sr)

        self.analysis_samples = librosa.resample(librosa.to_mono(y),
                                                 sr, self.analysis_sample_rate,
                                                 res_type='kaiser_best')
        self.raw_samples = np.atleast_2d(y)

        self.zero_indexes = self._create_zero_indexes()
        self.features = self._create_features()
        self.timings = self._create_timings()

    def __repr__(self):
        file_name = os.path.split(self.file_path)[-1]
        args = file_name, self.duration
        return '<Audio, file: {0:s}, duration: {1:.2f}>'.format(*args)

    def output(self, filename, format=None):
        """
        Write the samples out to the given filename.

        Parameters
        ----------
        filename : str
            The path to write the audio on disk.
            This can be any format supported by `pysoundfile`, including
            `WAV`, `FLAC`, or `OGG` (but not `mp3`).

        format : str
            If provided, explicitly set the output encoding format.
            See `soundfile.available_formats`.
        """
        sf.write(filename, self.raw_samples.T, int(self.sample_rate), format=format)

    def _create_zero_indexes(self):
        """
        Create zero crossing indexes.
        We use these in synthesis, and it is easier to make them here.
        """
        zero_indexes = []
        for channel_index in range(self.num_channels):
            channel = self.raw_samples[channel_index]
            zero_crossings = librosa.zero_crossings(channel)
            zero_index = np.nonzero(zero_crossings)[0]
            zero_indexes.append(zero_index)
        return zero_indexes

    def _create_timings(self):
        """
        Create timings in a timings dict.
        """
        timings = {}
        timings['track'] = TimingList('track', [(0, self.duration)], self)
        timings['beats'] = TimingList('beats', self._get_beats(), self)
        timings['segments'] = TimingList('segments', self._get_segments(), self)
        return timings

    def _get_beats(self):
        """
        Gets beats using librosa's beat tracker.
        """
        _, beat_frames = librosa.beat.beat_track(y=self.analysis_samples,
                                                 sr=self.analysis_sample_rate,
                                                 trim=False)

        # pad beat times to full duration
        f_max = librosa.time_to_frames(self.duration, sr=self.analysis_sample_rate)
        beat_frames = librosa.util.fix_frames(beat_frames, x_min=0, x_max=f_max)

        # convert frames to times
        beat_times = librosa.frames_to_time(beat_frames, sr=self.analysis_sample_rate)

        # make the list of (start, duration) tuples that TimingList expects
        starts_durs = [(s, t-s) for (s, t) in zip(beat_times, beat_times[1:])]

        return starts_durs

    def _get_segments(self):
        """
        Gets Echo Nest style segments using librosa's onset detection and backtracking.
        """

        onset_frames  = librosa.onset.onset_detect(y=self.analysis_samples,
                                                sr=self.analysis_sample_rate,
                                                backtrack=True)
        segment_times = librosa.frames_to_time(onset_frames,
                                               sr=self.analysis_sample_rate)

        # make the list of (start, duration) tuples that TimingList expects
        starts_durs = [(s, t-s) for (s, t) in zip(segment_times, segment_times[1:])]

        return starts_durs

    def _create_features(self):
        """
        Creates the FeatureCollection, and loads each feature.

        Parameters
        ---------

        Returns
        -----
        FeatureCollection
            FeatureCollection with each Amen.Feature object named correctly.
            Note that _get_chroma returns a FeatureCollection of chroma features.
        """
        features = FeatureCollection()
        features['centroid'] = self._get_centroid()
        features['amplitude'] = self._get_amplitude()
        features['timbre'] = self._get_timbre()
        features['chroma'] = self._get_chroma()
        features['tempo'] = self._get_tempo()
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
        centroids = librosa.feature.spectral_centroid(self.analysis_samples)
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
        amplitudes = librosa.feature.rmse(self.analysis_samples)
        data = self._convert_to_dataframe(amplitudes, ['amplitude'])
        feature = Feature(data)
        return feature

    def _get_timbre(self):
        """
        Gets timbre (MFCC) data, taking the first 20.
        Note that the keys to the Feature are "mffc_<index>", 
        to avoid having a dict-like object with numeric keys.

        Parameters
        ---------

        Returns
        -----
        Feature
        """
        mfccs = librosa.feature.mfcc(y=self.analysis_samples, sr=self.analysis_sample_rate, n_mfcc=12)
        feature = FeatureCollection()
        for index, mfcc in enumerate(mfccs):
            data = self._convert_to_dataframe(mfcc, ['timbre'])
            key = 'mfcc_%s' % (index)
            feature[key] = Feature(data)

        return feature

    def _get_chroma(self):
        """
        Gets chroma data from librosa, and returns it as a FeatureCollection,
        with 12 features.

        Parameters
        ---------

        Returns
        -----
        FeatureCollection
        """
        feature = FeatureCollection()
        pitch_names = ['c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'ab', 'a', 'bb', 'b']
        chroma_cq = librosa.feature.chroma_cqt(self.analysis_samples)
        for chroma, pitch in zip(chroma_cq, pitch_names):
            data = self._convert_to_dataframe(chroma, [pitch])
            feature[pitch] = Feature(data)

        # Enharmonic aliases
        feature['db'] = feature['c#']
        feature['d#'] = feature['eb']
        feature['gb'] = feature['f#']
        feature['g#'] = feature['ab']
        feature['a#'] = feature['bb']

        return feature

    def _get_tempo(self):
        """
        Gets tempo data from librosa, and returns it as a feature collection.
        Note that the tempo feature uses median aggregation, as opposed to the
        default mean.

        Parameters
        ---------

        Returns
        -----
        FeatureCollection
        """
        onset_env = librosa.onset.onset_strength(self.analysis_samples, sr=self.analysis_sample_rate)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=self.analysis_sample_rate, aggregate=None)
        data = self._convert_to_dataframe(tempo, ['tempo'])
        feature = Feature(data, aggregate=np.median)

        return feature

    @classmethod
    def _convert_to_dataframe(cls, feature_data, columns):
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

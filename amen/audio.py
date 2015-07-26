#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa

from amen.timing_list import TimingList, Beats

class Audio(object):
    """
    container for raw audio samples and some basic data bout em
    """
    def __init__(self, file_path, sample_rate=22050):
        self.file_path = file_path
        y, sr = librosa.load(file_path, sr=sample_rate)
        self.sample_rate = sr
        self.raw_samples = y
        self.duration = librosa.get_duration(y=self.raw_samples, sr=self.sample_rate)
    

class Analysis(object):
    """
    Analyis object: should wrap the output from libRosa.
    """

    def __init__(self, file_path, sample_rate=22050):
        """
        Opens a file path, passes it to libRosa,
        and builds up the analysis.
        """
        self.audio = Audio(file_path, sample_rate)
        # do some analysis
        self.beats = Beats(self.audio)



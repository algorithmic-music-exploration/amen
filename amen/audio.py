#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa

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
        self.sample_rate = sr
        self.raw_samples = y
        if convert_to_mono:
            self.num_channels = 1
        else:
            self.num_channels = 2
        self.duration = len(self.raw_samples) / self.sample_rate

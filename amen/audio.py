#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa

class Analysis(object):
    """
    Analyis object: should wrap the output from libRosa.
    """

    def __init__(self, file_path, sample_rate=22050):
        """
        Opens a file path, passes it to libRosa,
        and builds up the analysis.
        """
        self.file_path = file_path
        y, sr = librosa.load(file_path, sr=sample_rate)
        self.sample_rate = sr
        self.raw_samples = y

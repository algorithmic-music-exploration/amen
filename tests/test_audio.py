#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
from amen.audio import Analysis
from amen.utils import example_audio_file

EXAMPLE_FILE = example_audio_file()
analysis = Analysis(EXAMPLE_FILE)

def test_default_sample_rate():
    assert(analysis.sample_rate == 22050)

def test_file_path():
    assert(analysis.file_path == EXAMPLE_FILE)

def test_sample_data():
    y, sr = librosa.load(EXAMPLE_FILE)
    assert(analysis.raw_samples.all() == y.all())

def test_sample_rate():
    analysis = Analysis(EXAMPLE_FILE, sample_rate=44100)
    assert(analysis.sample_rate == 44100)

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import tempfile
import numpy as np
import librosa
from amen.audio import Audio
from amen.feature import FeatureCollection
from amen.utils import example_audio_file

EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)
mono_audio = Audio(EXAMPLE_FILE, convert_to_mono=True, sample_rate=44100)

def test_default_sample_rate():
    assert isinstance(audio.sample_rate, float)
    assert(audio.sample_rate == 44100)

def test_default_channels():
    assert(audio.num_channels == 2)

def test_duration():
    duration = audio.raw_samples.shape[-1] / float(audio.sample_rate)
    assert(audio.duration == duration)

def test_file_path():
    assert(audio.file_path == EXAMPLE_FILE)

def test_sample_data():
    y, sr = librosa.load(EXAMPLE_FILE)
    assert(audio.analysis_samples.all() == y.all())

def test_sample_rate():
    assert(mono_audio.sample_rate == 44100)

def test_channels():
    assert(mono_audio.num_channels == 1)

def test_has_feature_collection():
    assert(type(mono_audio.features) == FeatureCollection)

def test_has_amplitude_feature():
    res = librosa.feature.rmse(mono_audio.analysis_samples)[0]
    assert(mono_audio.features["amplitude"].data.iloc[0].item() == res[0])

def test_has_centroid_feature():
    res = librosa.feature.spectral_centroid(mono_audio.analysis_samples)[0]
    assert(mono_audio.features["centroid"].data.iloc[0].item() == res[0])

def test_has_chroma_feature():
    res = librosa.feature.chroma_cqt(mono_audio.analysis_samples)[0]
    assert(mono_audio.features["chroma"]["c"].data.iloc[0].item() == res[0])

def test_to_wav():
    n, tempfilename = tempfile.mkstemp()
    audio.to_wav(tempfilename)
    new_samples, new_sample_rate = librosa.load(tempfilename, sr=audio.sample_rate)
    os.unlink(tempfilename)

    assert np.allclose(audio.sample_rate, new_sample_rate)
    assert np.allclose(audio.raw_samples, new_samples, rtol=1e-3, atol=1e-4)

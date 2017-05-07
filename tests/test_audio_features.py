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

def test_has_feature_collection():
    assert(type(mono_audio.features) == FeatureCollection)

def test_has_amplitude_feature():
    res = librosa.feature.rmse(mono_audio.analysis_samples)[0]
    assert(mono_audio.features["amplitude"].data.iloc[0].item() == res[0])

def test_has_centroid_feature():
    res = librosa.feature.spectral_centroid(mono_audio.analysis_samples)[0]
    assert(mono_audio.features["centroid"].data.iloc[0].item() == res[0])

def test_has_timbre_feature():
    res = librosa.feature.mfcc(y=mono_audio.analysis_samples, sr=mono_audio.analysis_sample_rate, n_mfcc=20)[0]
    assert(mono_audio.features["timbre"]["mfcc_0"].data.iloc[0].item() == res[0])

def test_has_chroma_feature():
    res = librosa.feature.chroma_cqt(mono_audio.analysis_samples)[0]
    assert(mono_audio.features["chroma"]["c"].data.iloc[0].item() == res[0])

def test_has_chroma_feature_aliases():
    res = librosa.feature.chroma_cqt(mono_audio.analysis_samples)[1]
    assert(mono_audio.features["chroma"]["db"].data.iloc[0].item() == res[0])

def test_has_tempo_feature():
    onset_env = librosa.onset.onset_strength(mono_audio.analysis_samples, sr=mono_audio.analysis_sample_rate)
    res  = librosa.beat.tempo(onset_envelope=onset_env, sr=mono_audio.analysis_sample_rate, aggregate=None)
    assert(mono_audio.features["tempo"].data.iloc[0].item() == res[0])

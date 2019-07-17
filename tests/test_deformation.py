#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import librosa
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.deformation import time_stretch
from amen.deformation import pitch_shift
from amen.deformation import harmonic_separation
from amen.deformation import percussive_separation

EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)
mono_audio = Audio(EXAMPLE_FILE, convert_to_mono=True, sample_rate=44100)


def test_time_stretch():
    stretch_amount = 1.5
    time_stretch_audio = time_stretch(mono_audio, stretch_amount)
    test_time_stretch = librosa.effects.time_stretch(
        librosa.to_mono(mono_audio.raw_samples), stretch_amount
    )
    test_time_stretch_audio = Audio(
        raw_samples=test_time_stretch, sample_rate=mono_audio.sample_rate
    )
    assert np.allclose(
        time_stretch_audio.raw_samples,
        test_time_stretch_audio.raw_samples,
        rtol=1e-3,
        atol=1e-4,
    )


def test_pitch_shift():
    shift_amount = 4
    step_size = 24
    pitch_shift_audio = pitch_shift(mono_audio, shift_amount, step_size=step_size)
    test_pitch_shift = librosa.effects.pitch_shift(
        librosa.to_mono(mono_audio.raw_samples),
        mono_audio.sample_rate,
        shift_amount,
        bins_per_octave=step_size,
    )
    test_pitch_shift_audio = Audio(
        raw_samples=test_pitch_shift, sample_rate=mono_audio.sample_rate
    )
    assert np.allclose(
        pitch_shift_audio.raw_samples,
        test_pitch_shift_audio.raw_samples,
        rtol=1e-3,
        atol=1e-4,
    )


def test_harmonic():
    harmonic_audio = harmonic_separation(mono_audio)
    test_harmonic = librosa.effects.harmonic(
        librosa.to_mono(mono_audio.raw_samples), margin=3.0
    )
    test_harmonic_audio = Audio(
        raw_samples=test_harmonic, sample_rate=mono_audio.sample_rate
    )
    assert np.allclose(
        harmonic_audio.raw_samples,
        test_harmonic_audio.raw_samples,
        rtol=1e-3,
        atol=1e-4,
    )


def test_percussive():
    percussive_audio = percussive_separation(mono_audio)
    test_percussive = librosa.effects.percussive(
        librosa.to_mono(mono_audio.raw_samples), margin=3.0
    )
    test_percussive_audio = Audio(
        raw_samples=test_percussive, sample_rate=mono_audio.sample_rate
    )
    assert np.allclose(
        percussive_audio.raw_samples,
        test_percussive_audio.raw_samples,
        rtol=1e-3,
        atol=1e-4,
    )

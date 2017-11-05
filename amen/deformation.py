#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Deformation functions for Amen.
All functions act on an Audio object and return a modified Audio object.
"""

import librosa

from .audio import Audio


def time_stretch(audio, rate):
    """
    Wraps librosa's `time_stretch` function, and returns a new Audio object.
    Note that this folds to mono.

    Parameters
    ---------
    audio : Audio
        The Audio object to act on.

    rate : float
        The stretch factor
        If rate is > 1, then the audio is sped up.
        If rate is < 1, then the audio is slowed down.
        A rate of `2.0` will result in audio that is twice as fast.
    """
    stretched = librosa.effects.time_stretch(librosa.to_mono(audio.raw_samples), rate=rate)
    stretched_audio = Audio(raw_samples=stretched, sample_rate=audio.sample_rate)

    return stretched_audio

def harmonic_separation(audio, margin=3.0):
    """
    Wraps librosa's `harmonic` function, and returns a new Audio object.
    Note that this folds to mono.

    Parameters
    ---------
    audio : Audio
        The Audio object to act on.

    margin : float
        The larger the margin, the larger the separation.
        The default is `3.0`.
    """
    harmonic = librosa.effects.harmonic(librosa.to_mono(audio.raw_samples), margin=margin)
    harmonic_audio = Audio(raw_samples=harmonic, sample_rate=audio.sample_rate)

    return harmonic_audio

def percussive_separation(audio, margin=3.0):
    """
    Wraps librosa's `percussive` function, and returns a new Audio object.
    Note that this folds to mono.

    Parameters
    ---------
    audio : Audio
        The Audio object to act on.

    margin : float
        The larger the margin, the larger the separation.
        The default is `3.0`.
    """
    percussive = librosa.effects.percussive(librosa.to_mono(audio.raw_samples), margin=margin)
    percussive_audio = Audio(raw_samples=percussive, sample_rate=audio.sample_rate)

    return percussive_audio

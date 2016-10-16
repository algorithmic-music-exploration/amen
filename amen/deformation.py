#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Deformation functions for Amen.
All functions act on an Audio object and return a modified Audio object.
"""

import librosa

from .audio import Audio

def harmonic_separation(audio, margin=3.0):
    """
    Wraps librosa's `harmonic` function, and returns a new Audio object.
    Note that this folds to mono.

    Parameters
    ---------
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
    margin : float
        The larger the margin, the larger the separation.
        The default is `3.0`.
    """
    percussive = librosa.effects.percussive(librosa.to_mono(audio.raw_samples), margin=margin)
    percussive_audio = Audio(raw_samples=percussive, sample_rate=audio.sample_rate)

    return percussive_audio

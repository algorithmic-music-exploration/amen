#!/usr/bin/env python
# -*- coding: utf-8 -*-

from amen.audio import Audio
from amen.utils import example_audio_file
from amen.timing import TimingList

EXAMPLE_FILE = example_audio_file()
AUDIO = Audio(EXAMPLE_FILE)


def test_track():
    track = AUDIO.timings['track']
    assert isinstance(track, TimingList)
    assert len(track) == 1


def test_beats():
    beats = AUDIO.timings['beats']
    assert isinstance(beats, TimingList)
    assert len(beats) == 11


def test_segments():
    segments = AUDIO.timings['segments']
    assert isinstance(segments, TimingList)
    assert len(segments) == 42

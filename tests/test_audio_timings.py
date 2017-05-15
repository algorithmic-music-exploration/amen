#!/usr/bin/env python
# -*- coding: utf-8 -*-

from amen.audio import Audio
from amen.utils import example_audio_file
from amen.timing import TimingList
from nose.tools import eq_

EXAMPLE_FILE = example_audio_file()
AUDIO = Audio(EXAMPLE_FILE)

def test_track():
    track = AUDIO.timings['track']
    assert isinstance(track, TimingList)
    eq_(len(track), 1)

def test_beats():
    beats = AUDIO.timings['beats']
    assert isinstance(beats, TimingList)
    eq_(len(beats), 11)

def test_segments():
    segments = AUDIO.timings['segments']
    assert isinstance(segments, TimingList)
    eq_(len(segments), 42)

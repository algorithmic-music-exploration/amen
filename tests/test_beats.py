#!/usr/bin/env python
# -*- coding: utf-8 -*-

from amen.audio import Audio
from amen.utils import example_audio_file
from amen.time import TimingList
from nose.tools import eq_

EXAMPLE_FILE = example_audio_file()
AUDIO = Audio(EXAMPLE_FILE)

def test_beats():
    beats = AUDIO.timings['beats']
    assert isinstance(beats, TimingList), type(beats)
    eq_(len(beats), 11)

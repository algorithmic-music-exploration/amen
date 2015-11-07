#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.timing_list import TimingList

EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)

def test_beats():
    beats = audio.timings['beats']
    assert isinstance(beats, TimingList)
    assert len(beats) == 10, 'expected 10 beats, found %d' % len(beats)

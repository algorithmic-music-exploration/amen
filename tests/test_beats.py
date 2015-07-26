#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
from amen.audio import Analysis
from amen.utils import example_audio_file
from amen.timing_list import TimingList

EXAMPLE_FILE = example_audio_file()
analysis = Analysis(EXAMPLE_FILE)

def test_beats():
    assert(isinstance(analysis.beats, TimingList))
    assert(len(analysis.beats) == 12)


#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
from amen.audio import Audio
from amen.utils import example_audio_file

EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)

# need to split the organizer function out and write a test for it.
# need to test that synthesize gives back an Audio object
# need to test that re-synthesizing all of amen.beats is (basically) the same as the input file
# need to test that it fails if you try to write over 20 minutes of audio

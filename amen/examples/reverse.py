#!/usr/bin/env python
# encoding: utf=8

"""
reverse.py : Reverse the beats of a song.
"""

import sys
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.synthesize import snthesize

audio_file = sys.argv[1]
audio = Audio(audio_file)

beats = audio.timings['beats']
beats.reverse()

out = synthesize(beats)
out.to_wav('reversed.wav')


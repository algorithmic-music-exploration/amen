#!/usr/bin/env python
# encoding: utf=8

"""
iterate.py : Iterate through the beats of a song, and keep some, but not others
"""

import sys
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.synthesize import synthesize

audio_file = example_audio_file()
audio = Audio(audio_file)

beats = audio.timings['beats']
new_beats = []
for i, beat in enumerate(beats):
    if i % 4 == 0:
        new_beats.append(beat)

out = synthesize(new_beats)
out.output('iterate.wav')

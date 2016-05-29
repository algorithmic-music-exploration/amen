#!/usr/bin/env python
# encoding: utf=8

"""
iterate_feature.py : Iterate through the beats of a song, and keep some,
                     but not others, based on an audio feature.
"""

import sys
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.synthesize import synthesize

audio_file = example_audio_file()
audio = Audio(audio_file)

beats = audio.timings['beats']
amplitudes = audio.features['amplitude'].at(beats)

new_beats = []
for beat, amp in amplitudes.with_time():
    if amp > 2.5:
        new_beats.append(beat)

out = synthesize(new_beats)
out.output('iterate-feature.wav')

#!/usr/bin/env python
# encoding: utf=8

"""
reverse.py : Reverse the beats of a song.
"""

import sys
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.synthesize import synthesize

audio_file = example_audio_file()
#audio = Audio(audio_file)
audio = Audio("../../Desktop/onefourfiveone.mp3")

beats = audio.timings['beats']
beats.reverse()

out = synthesize(beats)
out.to_wav('reversed.wav')


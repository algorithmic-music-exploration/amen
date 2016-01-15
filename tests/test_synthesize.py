#!/usr/bin/env python
# -*- coding: utf-8 -*-

import six
import pandas as pd
import librosa
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.synthesize import _format_inputs

EXAMPLE_FILE = example_audio_file()
audio = Audio(EXAMPLE_FILE)

def test_format_inputs_length():
    formatted_inputs = _format_inputs(audio.timings['beats'])
    formatted_inputs = list(formatted_inputs)
    assert(len(audio.timings['beats']) == len(formatted_inputs))

def test_format_inputs_list():
    formatted_inputs = _format_inputs(audio.timings['beats'])
    formatted_inputs = list(formatted_inputs)
    beat = audio.timings['beats'][0]
    assert(formatted_inputs[0] == (audio.timings['beats'][0], beat.time))

def test_format_inputs_parallel_list():
    times = [beat.time for beat in audio.timings['beats']]
    formatted_inputs = _format_inputs((audio.timings['beats'], times))
    formatted_inputs = list(formatted_inputs)
    assert(formatted_inputs[0] == (audio.timings['beats'][0], times[0]))

def test_format_inputs_generator():
    def the_generator():
        for beat in audio.timings['beats']:
            yield beat, beat.time
    formatted_inputs = _format_inputs(the_generator())
    assert(six.next(formatted_inputs) == six.next(the_generator()))

    
    
    
# need to test that synthesize gives back an Audio object
# need to test that re-synthesizing all of amen.beats is (basically) the same as the input file
# need to test that it fails if you try to write over 20 minutes of audio

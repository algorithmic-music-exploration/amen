#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nose.tools import assert_raises
import six
import pandas as pd
import numpy as np
import librosa
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.synthesize import _format_inputs
from amen.synthesize import synthesize
from amen.exceptions import SynthesizeError

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

synthesized_audio = synthesize(audio.timings['beats'])
def test_synthesize_returns():
    assert isinstance(synthesized_audio, Audio)

def test_synthesize_sample_output():
    assert(np.isclose(audio.raw_samples[0][100], synthesized_audio.raw_samples[0][100]))

def test_synthesize_fails_if_too_long():
    time = pd.to_timedelta(21 * 60, unit='s')
    assert_raises(SynthesizeError, synthesize, ([audio.timings['beats'][5]], [time]))

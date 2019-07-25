#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import librosa
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.utils import example_mono_audio_file
from amen.timing import TimeSlice

t = 5
d = 10
dummy_audio = None
time_slice = TimeSlice(t, d, dummy_audio)


def test_time():
    assert time_slice.time == pd.to_timedelta(t, 's')


def test_duration():
    assert time_slice.duration == pd.to_timedelta(d, 's')


def test_units():
    time_slice = TimeSlice(t, d, dummy_audio, unit='ms')
    assert time_slice.time == pd.to_timedelta(t, 'ms')


EXAMPLE_FILE = example_audio_file()
stereo_audio = Audio(EXAMPLE_FILE)
time_slice = TimeSlice(t, d, stereo_audio)
EXAMPLE_MONO_FILE = example_mono_audio_file()
mono_audio = Audio(EXAMPLE_FILE)


def test_get_offsets():
    left, right = time_slice._get_offsets(3, 4, stereo_audio.num_channels)
    assert left == (-1, 3)


def test_offset_samples_mono():
    res = mono_audio.timings['beats'][0]._offset_samples(
        1, 2, (-1, 1), (-1, 1), mono_audio.num_channels
    )
    assert res.shape == (2, 3)


def test_offset_samples_stereo():
    res = stereo_audio.timings['beats'][0]._offset_samples(
        1, 2, (-1, 1), (-1, 1), stereo_audio.num_channels
    )
    assert res.shape == (2, 3)


def test_get_samples_shape_both_stereo_and_mono():
    def get_samples(audio):
        beat = audio.timings['beats'][0]

        start = beat.time.delta * 1e-9
        duration = beat.duration.delta * 1e-9
        starting_sample, ending_sample = librosa.time_to_samples(
            [start, start + duration], beat.audio.sample_rate
        )

        samples, left_offset, right_offset = beat.get_samples()
        left_offsets, right_offsets = beat._get_offsets(
            starting_sample, ending_sample, beat.audio.num_channels
        )

        duration = beat.duration.delta * 1e-9
        starting_sample, ending_sample = librosa.time_to_samples(
            [0, duration], audio.sample_rate
        )

        initial_length = ending_sample - starting_sample
        left_offset_length = initial_length - left_offsets[0] + left_offsets[1]
        right_offset_length = initial_length - right_offsets[0] + right_offsets[1]

        return samples, left_offset_length, right_offset_length

    mono_samples, mono_left_offset_length, mono_right_offset_length = get_samples(
        mono_audio
    )
    assert len(mono_samples[0]) == mono_left_offset_length
    assert len(mono_samples[1]) == mono_right_offset_length

    stereo_samples, stereo_left_offset_length, stereo_right_offset_length = get_samples(
        stereo_audio
    )
    assert len(stereo_samples[0]) == stereo_left_offset_length
    assert len(stereo_samples[1]) == stereo_right_offset_length


def test_get_samples_audio():
    def get_samples_audio(audio):
        beat = audio.timings['beats'][0]
        samples, left_offset, right_offset = beat.get_samples()

        start = beat.time.delta * 1e-9
        duration = beat.duration.delta * 1e-9
        starting_sample, ending_sample = librosa.time_to_samples(
            [start, start + duration], beat.audio.sample_rate
        )
        left_offsets, right_offsets = beat._get_offsets(
            starting_sample, ending_sample, beat.audio.num_channels
        )

        start_sample = left_offsets[0] * -1
        end_sample = len(samples[0]) - left_offsets[1]
        reset_samples = samples[0][start_sample:end_sample]

        original_samples = audio.raw_samples[0, starting_sample:ending_sample]

        return reset_samples, original_samples

    mono_reset_samples, mono_original_samples = get_samples_audio(mono_audio)
    assert np.array_equiv(mono_reset_samples, mono_original_samples)

    stereo_reset_samples, stereo_original_samples = get_samples_audio(stereo_audio)
    assert np.array_equiv(stereo_reset_samples, stereo_original_samples)

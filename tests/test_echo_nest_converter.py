#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from amen.audio import Audio
from amen.utils import example_audio_file
from amen.echo_nest_converter import AudioAnalysis
from amen.echo_nest_converter import AudioQuantum
from amen.echo_nest_converter import AudioQuantumList

EXAMPLE_FILE = example_audio_file()
AUDIO = Audio(EXAMPLE_FILE)
ANALYSIS = AudioAnalysis(AUDIO)


def test_beats():
    beats = ANALYSIS.beats
    assert isinstance(beats, AudioQuantumList), type(beats)
    for beat in beats:
        assert isinstance(beat, AudioQuantum), type(beat)


def test_serializable():
    serializable = ANALYSIS.as_serializable()
    try:
        json.dumps(serializable)
    except:
        assert False, 'as_serializable object cannot be parsed by JSON'


def test_json():
    encoded = ANALYSIS.to_json()
    try:
        deserialized = json.loads(encoded)
    except:
        assert False, 'to_json string cannot be parsed by JSON'
    quantums = ['sections', 'bars', 'beats', 'tatums', 'segments']
    assert all(quantum in deserialized for quantum in quantums)
    for segment in deserialized['segments']:
        assert isinstance(segment['pitches'], list), type(segment['pitches'])
        assert isinstance(segment['timbre'], list), type(segment['timbre'])
        assert len(segment['timbre']) == 12
        assert isinstance(segment['loudness_max'], float), type(segment['loudness_max'])
        assert isinstance(segment['loudness_max_time'], float), type(segment['loudness_max_time'])
        assert isinstance(segment['loudness_start'], float), type(segment['loudness_start'])

    assert isinstance(deserialized['tempo'], float)

#!/usr/bin/env python
# encoding: utf=8

"""
echo_nest_json.py : Write Echo Nest shaped JSON to a file
"""

import json
from amen.audio import Audio
from amen.utils import example_audio_file
from amen.echo_nest_converter import AudioAnalysis

audio_file = example_audio_file()
audio = Audio(audio_file)

remix_audio = AudioAnalysis(audio)
r = remix_audio.as_serializable()

with open('remix-json.json', 'w') as f:
    json.dump(remix_audio.to_json(), f)


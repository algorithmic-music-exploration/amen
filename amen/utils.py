#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pkg_resources

def example_audio_file():
    """Get the included example file"""
    path = 'examples/audio/amen.wav'
    return pkg_resources.resource_filename(__name__, path)

def example_mono_audio_file():
    """Get the included example file"""
    path = 'examples/audio/amen-mono.wav'
    return pkg_resources.resource_filename(__name__, path)

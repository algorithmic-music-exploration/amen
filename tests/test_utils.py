#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import amen.utils


def test_example_audio_file():
    path = amen.utils.example_audio_file()
    path_array = path.split(os.path.sep)
    set_path = path_array[-2:]
    assert (set_path) == ['example_audio', 'amen.wav']

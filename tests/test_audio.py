#!/usr/bin/env python
# -*- coding: utf-8 -*-

import amen.audio

def test_audio():
    analysis = amen.audio.Analysis('some_file_path.mp3')
    assert(analysis)

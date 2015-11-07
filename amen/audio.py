#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa
from amen.timing_list import TimingList

class Audio(object):
    """
    Audio object: should wrap the output from libRosa.
    """

    def __init__(self, file_path, convert_to_mono=False, sample_rate=22050):
        """
        Opens a file path, loads it with librosa.
        """
        self.file_path = file_path
        y, sr = librosa.load(file_path, mono=convert_to_mono, sr=sample_rate)
        self.sample_rate = sr
        self.raw_samples = y
        if convert_to_mono:
            self.num_channels = 1
        else:
            self.num_channels = 2
        self.duration = len(self.raw_samples) / self.sample_rate
        self.timings = self.create_timings()

    def create_timings(self):
        timings = {}
        timings['beats'] = TimingList('beats', self.get_beats(), self)
        return timings

    def get_beats(self):
        y_mono = librosa.to_mono(self.raw_samples)
        tempo, beat_frames = librosa.beat.beat_track(
            y=y_mono, sr=self.sample_rate, trim=False)
        # convert frames to times
        beat_times = librosa.frames_to_time(beat_frames, sr=self.sample_rate)
        # make the list of (start, duration)s that TimingList expects
        starts_durs = []
        for i, start in enumerate(beat_times[:-1]):
            starts_durs.append((start, beat_times[i+1] - start))
        # now get the last one
        starts_durs.append((beat_times[-1], self.duration - beat_times[-1]))

        return starts_durs

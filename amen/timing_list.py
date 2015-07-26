#!/usr/bin/env python
# -*- coding: utf-8 -*-

import librosa

from amen.time_slice import TimeSlice

class TimingList(list):
    """
    A list of TimeSlices.  
    """

    def __init__(self, name, timings, audio):
        # This assumes that we're going to get a list of tuples (start, duration) from librosa,
        # which may or may not be true.
        self.name = name
        for (start, duration) in timings:
            slice = TimeSlice(start, duration, audio)
            self.append(slice)

class Beats(TimingList):
    
    def __init__(self, audio):
        """
        Does HPSS, uses the percussive part as input to 
        libRosa's beat tracker.
        """
        y_harmonic, y_percussive = librosa.effects.hpss(audio.raw_samples)
        # beat_frames is an array of frame numbers
        tempo, beat_frames = librosa.beat.beat_track(
            y=y_percussive, sr=audio.sample_rate, trim=False)
        # convert frames to times
        beat_times = librosa.frames_to_time(beat_frames, sr=audio.sample_rate)
        # make the list of (start, duration)s that TimingList expects
        timings = []
        for i, start in enumerate(beat_times[:-1]):
            timings.append((start, beat_times[i+1] - start))
        timings.append((beat_times[-1], audio.duration - beat_times[-1]))

        super(Beats, self).__init__('beats', timings, audio)
        
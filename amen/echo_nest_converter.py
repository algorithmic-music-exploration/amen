import json
import datetime
import collections

import amen.audio
import amen.feature


class AudioAnalysis(object):
    """
    An Analysis object compatible with EchoNest Remix
    """
    def __init__(self, audio_object):
        """
        AudioAnalysis constructor.
        Create an EchoNest compatible Analysis object from an Audio object

        Parameters
        ----------
        audio_object: Audio object

        Returns
        ------
        An AudioAnalysis object
        """
        self.audio = audio_object
        self.sections = AudioQuantumList(kind='sections')
        self.bars = AudioQuantumList(kind='bars')
        self.beats = AudioQuantumList(kind='beats')
        self.tatums = AudioQuantumList(kind='tatums')
        self.segments = AudioQuantumList(kind='segments')

        for key in self.audio.timings:
            # Track-level attributes are dealt with below
            if key == 'track':
                continue
            else:
                setattr(self, key, self._get_quantums(key))

        # TODO: stub segments to be same as beats for now
        self.segments = self._get_quantums('beats')
        self.segments.kind = 'segments'
        for quantum in self.segments:
            quantum.kind = 'segment'

        # Set track-level attributes
        track_level = self.audio.timings['track']
        self.tempo = self.audio.features['tempo'].at(track_level)

    def _get_quantums(self, kind):
        """
        Format Audio Beats to be compatible with EchoNest Remix

        Parameters
        ----------
        kind: String, one of {beats, bars, tatums, sections, segments}

        Returns
        ------
        An AudioQuantumList
        """
        q_list = AudioQuantumList(kind=kind)
        time_slices = self.audio.timings[kind]
        for time_slice in time_slices:
            features = {}
            for key, feature in self.audio.features.items():
                feature = feature.at(time_slice)
                features[key] = feature
            quantum = AudioQuantum(
                kind[:-1],
                time_slice.time,
                time_slice.duration,
                features
            )
            q_list.append(quantum)
        return q_list

    def as_serializable(self):
        """
        Return this object as a serializable dict that contains only dicts,
        lists, and primitives.

        This may be useful, for instance, if you would like to use
        flask.jsonify(analysis.as_serializable())
        instead of the built-in to_json()
        """
        def as_dict(obj):
            # Convert timedeltas to float
            if isinstance(obj, datetime.timedelta):
                return obj.total_seconds()
            # Convert Audio objects to string
            if isinstance(obj, amen.audio.Audio):
                return obj.file_path
            # Convert Feature objects to list
            if isinstance(obj, amen.feature.Feature):
                return as_dict(obj.data.values.tolist())
            if isinstance(obj, collections.Sequence):
                if isinstance(obj, (str, bytes)):
                    return obj
                items = []
                for item in obj:
                    items.append(as_dict(item))
                # Extract if list contains only 1 item
                while (isinstance(items, collections.Sequence)
                       and len(items) == 1):
                    items = items[0]
                return items
            if hasattr(obj, '__dict__'):
                result = {}
                for key, value in obj.__dict__.items():
                    if key.startswith('_'):
                        continue
                    result[key] = as_dict(value)
                return result
            # default
            return obj

        return as_dict(self)

    def to_json(self):
        """
        Return this object as a JSON encoded string.
        """
        return json.dumps(self.as_serializable())


class AudioQuantum(object):
    def __init__(self, kind, start, duration, features, confidence=None):
        self.kind = kind
        self.start = start
        self.duration = duration
        self.confidence = confidence
        # Map Amen feature names to Remix names
        for feature, value in features.items():
            key = feature
            if feature == 'chroma':
                # pitches are a list in Remix
                key = 'pitches'
                pitch_names = ['c', 'c#', 'd', 'eb', 'e', 'f', 'f#', 'g', 'ab',
                               'a', 'bb', 'b']
                value = [value[pitch] for pitch in pitch_names]
            elif feature == 'timbre':
                # timbre is a list of 12 PCA things in Remix
                # we take the first 12 MFCCs
                timbre_dimensions = range(12)
                value = [value["mfcc_%s" % t] for t in timbre_dimensions]

            setattr(self, key, value)
        # TODO: stub fake loudness_max values from RMS energy
        self.loudness_max = features.get('amplitude')
        self.loudness_max_time = start
        self.loudness_start = start


class AudioQuantumList(list):
    def __init__(self, initial=[], kind=None):
        list.__init__(self)
        self.kind = kind
        self.extend(initial)

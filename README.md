[![Build Status](https://travis-ci.org/algorithmic-music-exploration/amen.svg?branch=master)](https://travis-ci.org/algorithmic-music-exploration/amen)
[![Coverage Status](https://coveralls.io/repos/github/algorithmic-music-exploration/amen/badge.svg?branch=master)](https://coveralls.io/github/algorithmic-music-exploration/amen?branch=master)
[![Documentation Status](https://readthedocs.org/projects/amen/badge/?version=latest)](http://amen.readthedocs.io/en/latest/?badge=latest)
[![GitHub license](https://img.shields.io/badge/license-BSD-blue.svg)](https://raw.githubusercontent.com/algorithmic-music-exploration/amen/master/LICENSE)

# amen
A toolbox for algorithmic remixing, after Echo Nest Remix.

# Platforms
Amen is developed on Ubuntu 14.04 and higher.  OS X should be workable.  Windows users should install Ubuntu.

# Installation
Amen is pretty simple, but it stands on top of some complex stuff.

If you are on Linux, you'll need `libsoundfile`:  `sudo apt-get install libsoundfile1`.  If you're on OS X, read on.

Next, you should install Anaconda, (https://www.continuum.io/downloads) which will get you all of the dependencies.

Then, install via pip:  `pip install amen`.  That should be it!

(If you're a serious Python cat, you can just get Amen from pip, without Anaconda - but that will require installing numpy, scipy, a fortran compiler, and so on.)

# Testing the Installation
After installation is finished, open up a Python interpreter and run the following (or run it from a file):
```
from amen.utils import example_audio_file
from amen.audio import Audio
from amen.synthesize import synthesize

audio_file = example_audio_file()
audio = Audio(audio_file)

beats = audio.timings['beats']
beats.reverse()

out = synthesize(beats)
out.output('reversed.wav')
```

If all that works, you just need to play the resulting `reversed.wav` file, and you're on your way!

# Examples

We've got a few other examples in the `examples` folder - most involve editing a file based on the audio features thereof.  We'll try to add more as we go.

# Contributing
Welcome aboard!  Please see CONTRIBUTING.md, or open an issue if things don't work right.

# Thanks
Amen owes a very large debt to Echo Nest Remix.  Contributors to that most esteemed library include:
* Chris Angelico
* Yannick Antoine
* Adam Baratz
* Ryan Berdeen
* Dave DesRoches
* Dan Foreman-Mackey
* Tristan Jehan
* Joshua Lifton
* Adam Lindsay
* Aaron Mandel
* Nicola Montecchio
* Rob Oschorn
* Jason Sundram
* Brian Whitman

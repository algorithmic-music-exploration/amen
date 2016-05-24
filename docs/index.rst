.. AMEN documentation master file, created by
   sphinx-quickstart on Sat May 21 16:07:22 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AMEN
====

A toolbox for algorithmic remixing, after Echo Nest Remix.

Platforms
---------
Amen is developed on Ubuntu 14.04 and higher.  OS X should be workable.  Windows users should install Ubuntu.

Installation
------------
Amen is pretty simple, but it stands on top of some complex stuff.

If you are on Linux, you'll need ``libsoundfile``:  ``sudo apt-get install libsndfile1``.  If you're on OS X, read on.

Next, you should install Anaconda, (https://www.continuum.io/downloads) which will get you all of the dependencies.

Then, install via pip:  ``pip install amen``.  That should be it!

(If you're a serious Python cat, you can just get Amen from pip, without Anaconda: but that will require installing numpy, scipy, a fortran compiler, and so on.)


Testing the Installation
------------------------
After installation is finished, open up a Python interpreter and run the following (or run it from a file)::

  from amen.utils import example_audio_file
  from amen.audio import Audio
  from amen.synthesize import synthesize
  
  audio_file = example_audio_file()
  audio = Audio(audio_file)
  
  beats = audio.timings['beats']
  beats.reverse()
  
  out = synthesize(beats)
  out.output('reversed.wav')

If all that works, just play the resulting ``reversed.wav`` file, and you're on your way!



API Reference
=============
.. toctree::
   :maxdepth: 2

   api

Contribute
==========
- `Issue Tracker <http://github.com/algorithmic-music-exploration/amen/issues>`_
- `Source Code <http://github.com/algorithmic-music-exploration/amen>`_


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


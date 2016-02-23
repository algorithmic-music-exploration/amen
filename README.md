# amen
A toolbox for algorithmic remixing, after Echo Nest Remix.

# Platforms
Amen is developed on Ubuntu 14.04 and higher.  OS X is probably workable.  Windows users should install Ubuntu.

# Installation
Amen is pretty simple, but it stands on top of some complex stuff.

First, you'll need our favorite basic resampler, `libsamplerate`  You get get it with `apt-get`, or the package manager of your choice.

Then, you'll need to get our own version of it `pip install git+https://github.com/bmcfee/samplerate.git`

Now, if you're a serious Python nerd, you can just get Amen from pip:  `pip install amen`.

If not, read on for faster, more user-friendly installation process.

First, you should install Anaconda, (https://www.continuum.io/downloads) which will get you all of the dependencies.

Then, install via pip:  `pip install amen`.

# Testing the Installation
After installation is finished, run `python amen/examples/reverse.py amen/examples/audio/amen./wav`.
Play the resulting `reversed.wav` file, and you're on your way!

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

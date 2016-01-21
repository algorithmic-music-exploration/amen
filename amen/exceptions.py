#!/usr/bin/env python
# -*- encoding: utf-8 -*-

class AmenError(Exception):
    """
    The root amen exception class
    """
    pass

class SynthesizeError(AmenError):
    """
    Exception class for errors in synthesize.py
    """
    pass

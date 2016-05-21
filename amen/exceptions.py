#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''AMEN Exception classes'''

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

class FeatureError(AmenError):
    """
    Exception class for errors in feature.py
    """
    pass

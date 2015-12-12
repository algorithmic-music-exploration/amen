#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''Exception classes for amen'''

class AmenError(Exception):
    '''The root amenexception class'''
    pass

class SynthesizeError(LibrosaError):
    '''Exception class for errors in the synthesize'''
    pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TimingList(list):
    """
    A list of TimeSlices.  
    """

    def __init__(self, name):
        self.name = name

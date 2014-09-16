# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 15:21:51 2014

@author: schriste
"""
from datetime import timedelta, datetime

def convert_time(t):
    """Convert a heroes time float
    """
    return timedelta(seconds=t) - timedelta(seconds=60*60*24*2730) + datetime(2013, 9, 21)
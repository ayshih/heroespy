# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
HEROESPy Lightcurve Routines
"""

from __future__ import absolute_import

class lightcurve(object):
    """Simple light curve"""
    def __init__(self, events, timerange, energyrange, freq='5T'):
        self.data = events[timerange[0]:timerange[1]].copy()
        self.data['count'] = self.data['energy']
        a = self.data
        a['count'] = (a['count'].values > energyrange[1]) * (a['count'].values > energyrange[0])
        #a.resample(freq, how='sum')
        self.data = self.data.resample(freq, how='sum')
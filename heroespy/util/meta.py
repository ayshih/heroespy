"""
A place to put information about the mission.
"""

from __future__ import absolute_import
from astropy.time import Time

# mission times
times = {'launch': Time("2013-09-21T11:58:00.0", format='isot', scale='utc'),
          'atfloat': Time("2013-09-21T14:49:00.0", format='isot', scale='utc'),
          'sas_pyasf_on': Time(("2013-09-21T15:21:04.896474", "2013-09-21T22:35:54.476023"), format='isot', scale='utc'),
         'sas_pyasr_on': (Time(("2013-09-21T15:21:33.292299", "2013-09-21T18:55:00.00"), format='isot', scale='utc'),
                         Time(("2013-09-21T18:51:00.0000", "2013-09-21T22:35:37.092514"), format='isot', scale='utc')),
         'sas_pyasr_wrongtarget': Time(("2013-09-21T18:49:00.0", "2013-09-21T19:54:00.0"), format='isot', scale='utc'),
         'solarobs_target1': Time(("2013-09-21T15:22:00.00", "2013-09-21T15:33:00.0"), format='isot', scale='utc'),
         'solarobs_target2': Time(("2013-09-21T15:35:00.0", "2013-09-21T22:33:00.0"), format='isot', scale='utc'),
         'shutdowm': Time("2013-09-22T14:18:00.0", format='isot', scale='utc')
         }

#ras_on = (parse_time("2013-09-21 14:49:00.0"), parse_time("2013-09-21 14:49:00.0"))

# solar target command was received
#solar_target_change = (datetime(2013, 9, 21, 15, 33, 8), datetime(2013, 9, 21, 15, 33, 16))
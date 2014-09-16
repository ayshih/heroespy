"""
A place to put information about the mission.
"""

from __future__ import absolute_import
from sunpy.time import parse_time
from heroespy.util import convert_time

from astropy.io import fits
from astropy.units import Unit as u
import pandas

from datetime import timedelta, datetime

DATA_DIR = heroespy.config.get("data", "data_dir")

# mission times
times = {'launch': parse_time("2013/09/21 11:58:00.0"), 
         'atfloat': parse_time("2013/09/21 14:49:00.0"),
         'sas_pyasf_on': (parse_time("2013/09/21 15:21:04.896474"), parse_time("2013/09/21 22:35:54.476023")), 
        'sas_pyasr_on': (parse_time("2013/09/21 15:21:33.292299"), parse_time("2013/09/21 18:55:00.00"), 
                         parse_time("2013/09/21 18:51:00.0000"), parse_time("2013/09/21 22:35:37.092514")),
        'sas_pyasr_wrongtarget': (parse_time("2013/09/21 18:49:00.0"), parse_time("2013/09/21 19:54:00.0")),
        'solarobs_target1': (parse_time("2013/09/21 15:22:00.00"), parse_time("2013/09/21 15:33:00.0")),
        'solarobs_target2': (parse_time("2013/09/21 15:35:00.0"), parse_time("2013/09/21 22:33:00.0")),
        'shutdowm': parse_time("2013/09/22 14:18:00.0")
        }
#ras_on = (parse_time("2013/09/21 14:49:00.0"), parse_time("2013/09/21 14:49:00.0"))

# solar target command was received
#solar_target_change = (datetime(2013, 9, 21, 15, 33, 8), datetime(2013, 9, 21, 15, 33, 16))

class detector(object):
    def __init__(self, number):
        self.raw_center = _detector_raw_center[number]

_detector_raw_center = [[320., 280.], 
                        [320., 300.],
                        [295., 250.],
                        [330., 300.],
                        [280., 280.],
                        [305., 280.],
                        [280., 290.],
                        [330., 290.]]

class payload(object):
    def __init__(self):
        self.location = self._load_location_data()
        self.pointing = self._load_pointing_data()
        
    def _load_location_data(self):
        file = DATADIR + 'f13_gps.fits'

        f = fits.open(file)
        time = f[1].data['time']
        height = f[1].data['height']
        longitude = f[1].data['longitude']
        latitude = f[1].data['latitude']

        times = [convert_time(t) for t in time]
        dict = {'time': times, 'height': height, 'latitude': latitude, 'longitude': longitude}

        d = pandas.DataFrame(dict)
        d.index = d['time']
        d.units = (u('m'), u('deg'), u('deg'))
        return d
    
    def _load_pointing_data(self):
        file = DATA_DIR + 'f13_aid.fits'

        f = fits.open(file)
        altitude = f[1].data['targetalt'].byteswap().newbyteorder()
        time = f[1].data['stime'].byteswap().newbyteorder()
        ra = f[1].data['TargetRA'].byteswap().newbyteorder()
        dec = f[1].data['TargetDEC'].byteswap().newbyteorder()
        az = f[1].data['TargetAz'].byteswap().newbyteorder()

        times = [timedelta(seconds=t) - timedelta(seconds=60*60*24*2730+8*60*60) + datetime.datetime(2013, 9, 21) for t in time]

        target = {'time': times, 'ra':ra, 'dec': dec, 'az':az, 'alt':altitude}
        target.units = (u('deg'), u('deg'), u('deg'), u('deg'))
        target = pandas.DataFrame(dict)
        target.index = target['time']
        return target
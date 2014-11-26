"""This module holds information about the science payload"""
from __future__ import absolute_import

from astropy.units import Unit as u
from astropy.units import Quantity
from astropy.io import fits
import pandas
import numpy as np
from scipy.interpolate import interp2d
from datetime import timedelta, datetime

from heroespy.util import convert_time

import heroespy
DATA_DIR = heroespy.config.get("data", "data_dir")

_plate_scape = Quantity(3.4, 'arcsec/pix')
_detector_raw_center = Quantity(np.array([[320., 280.],
                        [320., 300.],
                        [295., 250.],
                        [330., 300.],
                        [280., 280.],
                        [305., 280.],
                        [280., 290.],
                        [330., 290.]]), 'pix')

_detector_ids = (0, 1, 2, 3, 4, 5, 6, 7, 8)
_optics_ids = (0, 1, 2, 3, 4, 5, 6, 7, 8)
_telescopes_id = (0, 1, 2, 3, 4, 5, 6, 7)

class telescope(object):
    """A telescope module"""
    def __init__(self, identifier):
        self.detector = detector(identifier)
        self.optic = optic(identifier)
        self.identifier = identifier

class detector(object):
    def __init__(self, identifier):
        self.raw_center = _detector_raw_center[number]
        self.plate_scale = _plate_scape
        self.identifier = identifier

    def pixel_to_world(self, pixelxy):
        """Convert a pixel position to physical coordinates

        Parameters
        ----------
        pixelxy : `astropy.units.Quantity` (pixels)

        Returns
        -------
        result : `astropy.units.Quantity` (physical)
        """
        return (pixelxy - self.raw_center + 0.5 * u('pix')) * self.plate_scale

    def get_events(self):
        """Get the list of detector events.

        Parameters
        ----------
        detector_number : int

        Returns
        -------
        result : `pandas.Dataframe`
        """
        filename = DATA_DIR + 'det0' + str(self.identifier) + 's_gc.fits'
        f = fits.open(filename)

        heroes_times = f[1].data['time']
        energy = f[1].data['energy']
        rawx = f[1].data['rawx']
        rawy = f[1].data['rawy']

        times = [convert_time(t) for t in heroes_times]

        event_list = pandas.DataFrame({'energy': energy, 'rawx': rawx, 'rawy':rawy}, index=times)
        return event_list


class optic(object):
    """An x-ray optic"""
    def __init__(self, identifier):
        if number == 5:
            self.num_shells = 13
        else:
            self.num_shells = 14
        self.identifier = identifier

        # Correct effective area for 10% obstructions
        self.obstruction_factor = 0.9

    def effective_area(energy_index, off_axis_angle):
        """Get the effective area provided by the HEROES optics

        Parameters
        ----------
        energy_index : `astropy.units.Quantity`

        off_axis_angle : `astropy.units.Quantity`

        Returns
        -------
        result : Spectrum
        """

        data_file = DATA_DIR + 'aeff_' + num_shells + 'shells_sky.dat.dat'

        data = np.genfromtxt(data_file, skip_header=2)
        off_axis_angles = Quantity(np.arange(0,13,1), 'arcmin')
        energy = Quantity(data[:,0], 'keV')
        effective_area_cm2 = data[:,1:] * obstruction_factor
        f = interp2d(energy.value, off_axis_angles.value, effective_area_cm2)

        return Spectrum(energy, Quantity(f(energy.value, off_axis_angle), 'cm**2'))


class payload(object):
    """An object to hold all of the physical information about the HEROES payload"""
    def __init__(self):
        self.location = self._load_location_data()
        self.pointing = self._load_pointing_data()
        self.telescope = []
        for telescope_id in _telescopes_id:
            self.telescope.append(telescope(telescope_id))

    def _load_location_data(self):
        file = DATA_DIR + 'f13_gps.fits'

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

        times = [timedelta(seconds=t) - timedelta(seconds=60*60*24*2730+8*60*60) + datetime(2013, 9, 21) for t in time]

        target_data = {'time': times, 'ra':ra, 'dec': dec, 'az':az, 'alt':altitude}
        target = pandas.DataFrame(target_data)
        target.index = target['time']
        #target['units'] = (u('deg'), u('deg'), u('deg'), u('deg'))

        return target
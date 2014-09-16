# -*- coding: utf-8 -*-
"""
HEROES Procedures for Spectrum
"""
from __future__ import absolute_import

import pandas
import numpy as np
from astropy.units import Quantity
from scipy.interpolate import interp2d
from heroespy.util import convert_time
import heroespy

from astropy.io import fits

energy_index = Quantity(np.arange(20, 80, 1), 'keV')

import heroespy
DATA_DIR = heroespy.config.get("data", "data_dir")

class Spectrum(object):
    """A class to hold a spectrum which includes an energy and a flux"""
    def __init__(self, energy, flux):
        self._data = pandas.DataFrame({'energy': energy.value, 'flux': flux.value})
        self._units = {'energy': energy[0].unit, 'flux': flux[0].unit}
        
    @property
    def energy(self):
        return Quantity(self._data['energy'], self._units.get('energy'))
    
    @property
    def flux(self):
        return Quantity(self._data['flux'], self._units.get('flux'))
    
    def energy_to(self, unit):
        """Convert the units of the energy"""
        self._data.index = Quantity(self._data['energy'], self._units.get('energy')).to(unit).value
        
    def flux_to(self, unit):
        """Convert the units of the flux"""
        self._data['flux'] = Quantity(self._data['flux'], self._units.get('flux')).to(unit).value  
    
    def plot(self, **plot_args):
        self._data.plot(**plot_args)

def get_atten_coefficients(energy_index):
    """Returns the attenuation coefficient of air as a function of energy

    Parameters
    ----------
        energy_index : `astropy.units.Quantity`
        
    Returns
    -------
        result : `Spectrum`
    """

    data_file = DATA_DIR + 'air_mass_atten_coefs_xcom.txt'
    names = ('coherent', 'incoherent', 'photoelectric', 'nuclear', 'electron', 'total w', 'total wo', 'blah')
    data = pandas.read_csv(data_file, delimiter='|', skiprows=[0, 1, 2, 3], index_col=0, names=names)
    # the following code does a log-space interpolation 
    log_data = np.log10(data)
    log_data.index = np.log10(data.index)
    log_result = log_data.reindex(index=np.log10(energy_index.to('MeV').value), columns=['total w']).interpolate(method='quadratic')

    # returns back to normal space
    result = 10 ** log_result
    result.index = 10 ** log_result.index

    atten_coef = Spectrum(Quantity(result.index * 1000.0, 'keV'), Quantity(result['total w'], 'cm**2 g**-1'))
    return atten_coef

def atmospheric_column_density(altitude):
    """Returns the atmospheric column density or air mass thickness. 
       This formulad is based on MAXIS Antarctic Balloon flight.
    
    Parameters
    ----------
    altitude : `astropy.units.Quantity`
    
    Returns 
    -------
    result : `astropy.units.Quantity`
    """
    return Quantity(23.5 - 0.5 * altitude.to('km').value, 'g*cm**-2')
    
def atmospheric_transmission(altitude, source_elevation):
    """Returns the atmospheric 
    
    Parameters
    ----------
    altitude : `astropy.units.Quantity`
    
    Returns
    -------
    result : `astropy.units.Quantity`
    """
    atten_coeff = get_atten_coefficients(energy_index)
    result = [ calculate_transmission(atmospheric_column_density(altitude), source_elevation, this_mass_atten) for this_mass_atten in atten_coeff.flux]
    return Spectrum(energy_index, Quantity(result, ''))

def calculate_transmission(column_density, elevation, mass_atten):
    """Calculate the transmision of X-rays through a column density of air at
    an incident angle (90 degrees is straight through).
    
    Parameters
    ----------
    column_density : `astropy.units.Quantity`
    
    elevation : `astropy.units.Quantity`
    
    Returns
    -------
    result : `astropy.units.Quantity` dimensionless (0 to 1)
    """
    return Quantity(np.exp(-column_density / np.sin(elevation.to('deg')) * mass_atten), '')
    
def get_optics_effective_area(energy_index, off_axis_angle, module_number=0):
    """Get the effective area provided by the HEROES optics
    
    Parameters
    ----------
    energy_index : `astropy.units.Quantity`
    
    off_axis_angle : `astropy.units.Quantity`
    
    module_number : 13 or 14
    
    Returns
    -------
    result : Spectrum
    """
    if module_number == 5:
        num_shells = 13
    else:
        num_shells == 14

    # Correct effective area for 10% obstructions
    obstruction_factor = 0.9

    data_file = DATA_DIR + 'aeff_' + num_shells + 'shells_sky.dat.dat'
    
    data = np.genfromtxt(data_file, skip_header=2)
    off_axis_angles = Quantity(np.arange(0,13,1), 'arcmin')    
    energy = Quantity(data[:,0], 'keV')
    effective_area_cm2 = data[:,1:] * obstruction_factor
    f = interp2d(energy.value, off_axis_angles.value, effective_area_cm2)    
    
    return Spectrum(energy, Quantity(f(energy.value, off_axis_angle), 'cm**2'))
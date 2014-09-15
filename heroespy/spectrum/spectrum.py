# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 11:45:33 2014

@author: schriste
"""
import pandas
import numpy as np
from astropy.units import Unit as u
from astropy.units import Quantity

import heroespy

energy_index = Quantity(np.arange(20, 80, 1), 'keV')

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
    
def get_optics_effective_area(energy_index):
    
    data_file = DATA_DIR + 'aeff_14shells_sky.dat.dat'
    a = pandas.read_csv(data_file, delim_whitespace=True, skiprows=[0], index_col=0)
    
    return a
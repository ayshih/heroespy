# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 11:45:33 2014

@author: schriste
"""
import pandas
from astropy.units import Unit as u
from astropy.units import Quantity

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
    
    file = '/Users/schriste/heroes/txt_files/air_mass_atten_coefs.txt'
    data = pandas.read_csv(file, delim_whitespace=True, index_col=0)
    
    # the following code does a log-space interpolation 
    log_data = np.log10(data)
    log_data.index = np.log10(data.index)
    log_result = log_data.reindex(index=energy_index.to('MeV').value, columns=['mu/rho']).interpolate(method='quadratic')
    
    # returns back to normal space
    result = 10**log_result
    result.index = 10**log_result.index    
    
    atten_coef = Spectrum(Quantity(result.index*1000, 'keV'), Quantity(result['mu/rho'], 'm**-3'))
    return atten_coef

def atmospheric_col_density(altitude):
    """Returns the atmospheric column density or air mass thickness.
    
    Parameters
    ----------
    altitude : `astropy.units.Quantity`
    
    Returns 
    -------
    result : `astropy.units.Quantity`
    """
    return Quantity(23.5 - 0.5 * balloon_altitude.to('km').value, 'g*cm**-2')
    
def atmospheric_transmission(atten_coef, colum_density, source_elevation):
    np.exp(-atm_col_density / sin(source_elevation * !dtor) * interp_mass_atten[tmp2])
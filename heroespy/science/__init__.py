from __future__ import absolute_import

import heroespy
DATA_DIR = heroespy.config.get("data", "data_dir")
from astropy.io import fits
from heroespy.util import convert_time
import pandas

def get_events_list(detector_number=0):
    """Get the list of detector events.
    
    Parameters
    ----------
    detector_number : int
    
    Returns
    -------
    result : `pandas.Dataframe`
    """
    filename = DATA_DIR + 'det0' + str(detector_number) + 's_gc.fits'
    f = fits.open(filename)
    
    heroes_times = f[1].data['time']
    energy = f[1].data['energy']
    rawx = f[1].data['rawx']
    rawy = f[1].data['rawy']

    times = [convert_time(t) for t in heroes_times]

    event_list = pandas.DataFrame({'energy': energy, 'rawx': rawx, 'rawy':rawy}, index=times)
    return event_list
import heroespy.science.spectrum as spec
from astropy.units import Unit as u

print(spec.atmospheric_column_density(40 * u('km')))
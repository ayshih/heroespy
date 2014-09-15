"""
HEROESpy
=====

An open-source Python library for the analysis of the High Energy Replicated
Optics to Explore the Sun telescope data.

Web Links
---------
Homepage: https://plus.google.com/116746714590125162836/posts
Documentation: http://heroespy.readthedocs.org/en/latest/index.html
"""
from __future__ import absolute_import

#import warnings

__version__ = '0.1'

#try:
#    from sunpy.version import version as __version__
#except ImportError:
#    warnings.warn('Missing version.py; you need to run setup.py', Warning)

from heroespy.util.config import load_config

# Load user configuration
config = load_config()
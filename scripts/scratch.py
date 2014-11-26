import heroespy
DATA_DIR = heroespy.config.get("data", "data_dir")

import heroespy.science
import heroespy.aspect

from heroespy.payload import payload
heroes = payload()

pyas_aspect = heroespy.aspect.get_pyas_aspect()

for telescope in heroes.telescope:
    raw_events = telescope.detector.get_events()
    x, y = telescope.detector.pixel_to_world(raw_events['rawx'], raw_events['rawy'])


import heroespy
DATA_DIR = heroespy.config.get("data", "data_dir")

import heroespy.science
import heroespy.aspect

pyas_aspect = heroespy.aspect.get_pyas_aspect()

for telescope in telescopes:
    raw_events = heroespy.science.get_events_list(telescope)
    x, y = telescope.detector.pixel_to_world(raw_events['rawx'], raw_events['rawy'])


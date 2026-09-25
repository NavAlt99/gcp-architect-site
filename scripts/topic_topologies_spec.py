"""
topic_topologies_spec.py - Master repository of authentic per-topic topologies.
Aggregates specs across:
- spec_p0_p1 (Phase 0 & 1)
- spec_p2 (Phase 2)
- spec_p3_p4 (Phase 3 & 4)
- spec_p5_p6 (Phase 5 & 6)
- spec_p7_cs (Phase 7 & Cheat Sheets)
"""

import spec_p0_p1
import spec_p2
import spec_p3_p4
import spec_p5_p6
import spec_p7_cs

TOPIC_SPECS = {}
TOPIC_SPECS.update(spec_p0_p1.get_specs())
TOPIC_SPECS.update(spec_p2.get_specs())
TOPIC_SPECS.update(spec_p3_p4.get_specs())
TOPIC_SPECS.update(spec_p5_p6.get_specs())
TOPIC_SPECS.update(spec_p7_cs.get_specs())

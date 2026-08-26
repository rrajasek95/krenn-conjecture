#!/usr/bin/env python3
import json
from pathlib import Path

data = json.loads((Path(__file__).parent / "results_rep3_referee.json").read_text())
assert data["status"] == "ACCEPT_REP3_CORRECTED_DIAGONAL_INCIDENCE_CLOSURE"
assert data["chart_referee"]["coordinate_entry_cases"] == 27
assert data["chart_referee"]["S3_then_S2_orbits"] == [[0, 0], [0, 1], [1, 0], [1, 1], [1, 2]]
assert data["chart_referee"]["exact_Q_units"] == 5
assert data["scope"]["representative_3_only"] is True
assert data["scope"]["full_family_only"] is True
assert data["scope"]["no_other_representative_transport"] is True
print("PASS independent rep3 corrected incidence referee")

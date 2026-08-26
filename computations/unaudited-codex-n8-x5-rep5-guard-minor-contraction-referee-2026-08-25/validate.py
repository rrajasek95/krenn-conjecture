#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[1]
producer = root / "computations/unaudited-codex-n8-x5-rep5-guard-minor-contraction-design-2026-08-25"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

r = json.loads((here / "results_independent_referee.json").read_text())
p = json.loads((here / "HELD_MODULAR_PILOT.json").read_text())
assert r["status"] == "PASS_INDEPENDENT_EXACT_DESIGN_NO_IDEAL_RUN"
assert r["counts"] == {"old_variables":100,"old_generators":6586,"new_variables":91,"new_generators":6577,"full_x5":6561,"remaining_guard":15,"combined_saturation":1}
assert r["charts"] == {"raw":972,"orbits":162,"orbit_size":6,"y_orbits":81,"z_orbits":81}
assert r["cramer"]["identities"] == 12 and r["cramer"]["z_dependency_acyclic"] is True
assert r["orientation"]["elimination"] == "A36=-A37*A26^T"
assert r["orientation"]["guards"] == ["A06*A37^T=0","(I-A17*A26)*A37^T=0"]
assert r["scope"] == {"ideal_runs":0,"rep5_closed":False,"transport_claimed":False,"pilot_launched":False}
assert all(r["hostile_tests"].values())
for kind, expected in {"y":"33716adb0c1e2e9064e8c68e8cd60df305fe88781153c195853dba8131838c97","z":"cf9d4eafc3b25a59f848a3f3be942cd92c1e1758682cd83d3163a9e757ba3ce7"}.items():
    assert r["regenerated_programs"][kind]["sha256"] == expected
    assert sha(producer / f"rep5_guard_minor_tiny_{kind}_p32003.sing") == expected
assert p["status"] == "HELD_NOT_LAUNCHED" and p["scope"] == {"launched":False,"ideal_runs":0}
assert p["source"]["sha256"] == r["regenerated_programs"]["y"]["sha256"]
assert p["lane"]["rss_observer"].startswith("Darwin libproc")
assert "automatic relaunch" in p["forbidden"] and "Q lane" in p["forbidden"]
print(json.dumps({"status":"PASS","manifest_entries_checked":6,"ideal_runs":0,"pilot_launched":False},sort_keys=True))

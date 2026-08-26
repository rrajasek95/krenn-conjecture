#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
path = here / "results_referee.json"
result = json.loads(path.read_text())
assert result["status"] == "PASS_EXACT_Q_UNIT_IDEAL_RANK3_TWO_LIFTS_ONLY"
assert result["producer_manifest_sha256"] == "586df8668047a5d62a2714825807f246792df2a11d616515d5c658bd79d49b80"
assert result["producer_result_sha256"] == "c742220543ab6a45c9c751e7454031146c62e7ea85f62f7d3de34d47aedea081"
assert result["source_Q_sha256"] == "e2739688ea9986d59c56e17e6f0058154d9ddb7930bf9617a1d3a3a8167538f5"
assert (result["variables"], result["input_generators"], result["groebner_basis_size"], result["unit_remainder"]) == (56, 6563, 1, 0)
assert result["wall_seconds"] == 0.519554 and result["peak_rss_kib"] == 23160
assert result["atomic_no_tmp"] is True and result["observed_second_lane_or_relaunch"] is False
assert result["scope"]["closed"] == [
    "rank(A47)=3 adjugate chart", "A12-absent amplitude-inactive lift", "A12-present amplitude-inactive lift"
]
assert "rank(A47)<=2" in result["scope"]["not_closed"]
assert "the full conjecture" in result["scope"]["not_closed"]
print(json.dumps({"status": "PASS", "result_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, sort_keys=True))

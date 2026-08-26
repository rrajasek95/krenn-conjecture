#!/usr/bin/env python3
"""Read-only validation of the exact rep5 k2/t1 torus cover."""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


result = json.loads((HERE / "results_design.json").read_text())
assert result["status"] == "PASS_EXACT_16_CHART_73_VARIABLE_COVER_ZERO_SOLVES"
assert result["original"] == {
    "generators": 6562,
    "order": "dp",
    "ring_transport_to_p32003_byte_exact": True,
    "source_bytes": 4434943,
    "source_sha256": "1e2f72c9b4fda5e87fbec18469a6378cc7430f7b06676bd69db215055d8b1c7e",
    "variables": 84,
}
assert result["grading"]["rank"] == 74 and result["grading"]["nullity"] == 10
assert abs(result["grading"]["selected_minor_determinant"]) == 1
assert result["global_gauge"]["variables_after_global_gauge_and_saturation_elimination"] == 77
cover = result["residual_cover"]
assert cover["charts"] == 16 and cover["variables_each"] == 73 and cover["generators_each"] == 6561
assignments = set()
for record in cover["sources"]:
    path = HERE / record["path"]
    assert path.is_file() and sha(path) == record["sha256"]
    text = path.read_text()
    assert "ring r=0,(" in text and "),dp;" in text
    assert "slimgb" not in text and "ideal G=" not in text
    variables = text.split("ring r=0,(", 1)[1].split("),dp;", 1)[0].split(",")
    body = text.split("ideal I=", 1)[1].split(';\nprint("INPUT_VARIABLES=', 1)[0]
    depth = 0
    count = 1
    for character in body:
        if character == "(": depth += 1
        elif character == ")": depth -= 1
        elif character == "," and depth == 0: count += 1
        assert depth >= 0
    assert depth == 0 and len(variables) == 73 and count == 6561
    tokens = set(re.findall(r"\b(?:a\d\d_\d\d|xn\d|yn\d|zn\d|abar|beta|t\d|sat)\b", body))
    assert tokens <= set(variables)
    assignment = tuple(int(record["residual_assignment"][name]) for name in ("yn1", "yn2", "t0", "t2"))
    assignments.add(assignment)
assert assignments == set(__import__("itertools").product((0, 1), repeat=4))
scope = result["order_and_scope"]
assert scope["singular_runs"] == scope["ideal_runs"] == scope["modular_retries"] == 0
assert scope["mathematical_coverage"] is scope["rep5_closed"] is False
checked = 0
manifest = HERE / "MANIFEST.sha256"
if manifest.exists():
    for line in manifest.read_text().splitlines():
        digest, relative = line.split(None, 1)
        path = (HERE / relative.strip()).resolve()
        assert path.is_file() and sha(path) == digest
        checked += 1
print(json.dumps({"status": "PASS_EXACT_DESIGN_VALIDATED_ZERO_RUN", "charts": 16, "manifest_lines_checked": checked}, sort_keys=True))

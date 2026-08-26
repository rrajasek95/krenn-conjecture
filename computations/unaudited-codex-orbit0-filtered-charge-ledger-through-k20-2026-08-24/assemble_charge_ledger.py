#!/usr/bin/env python3
"""Assemble the corrected complete irreducible charge ledger through K20."""
from fractions import Fraction
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FILES = {
    16: ROOT / "computations/unaudited-codex-orbit0-filtered-k16-referee-2026-08-23/results_filtered_k16_referee.json",
    17: ROOT / "computations/unaudited-codex-orbit0-filtered-k16-run-2026-08-23/results_filtered_k17_run.json",
    18: ROOT / "computations/unaudited-codex-orbit0-hidden-k16-k18-complete-charge-2026-08-23/results_complete_k18_charge.json",
    19: ROOT / "computations/unaudited-codex-orbit0-k19-complete-charge-2026-08-23/results_complete_k19_charge.json",
    20: ROOT / "computations/unaudited-codex-orbit0-k20-222-consumer-design-2026-08-23/results_complete_k20_36path_charge.json",
}
def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def q(s): return Fraction(s)
def fq(x): return {"numerator":x.numerator,"denominator":x.denominator,"text":str(x)}

d = {k:load(v) for k,v in FILES.items()}
assert d[16]["status"] == "PASS_EXACT_FILTERED_K16_STREAMING_REFEREE"
assert d[17]["status"] == "PASS one bounded exact filtered reduction through completed K17"
assert d[18]["status"] == "PASS_COMPLETE_K18_PATH_CHARGE_ASSEMBLY" and d[18]["dag_coverage"]["covered_K18_paths"] == 17
assert d[19]["status"] == "PASS_COMPLETE_K19_PATH_CHARGE_ASSEMBLY" and d[19]["dag_coverage"]["covered_K19_paths"] == 24
assert d[20]["status"] == "PASS_COMPLETE_K20_36_ID_EXACT_Q" and d[20]["covered_paths"] == 36 and d[20]["complete_K20_claim"]

charges = {
    14: Fraction(0),
    15: Fraction(0),
    16: Fraction(d[16]["reduced_K16"]["integer_77_cycle_charge"]),
    17: q(d[17]["cycle_replay"]["components"]["combined"]["cycle_pairing"]),
    18: q(d[18]["K18"]["corrected_complete_17_path_total"]["irreducible"]["text"]),
    19: q(d[19]["K19"]["corrected_complete_24_path_total"]["irreducible"]["text"]),
    20: q(d[20]["irreducible"]["text"]),
}
assert charges == {
    14: Fraction(0), 15: Fraction(0), 16: Fraction(375127296),
    17: Fraction(-9747200926208,6545),
    18: Fraction(109863564487489024,24838275),
    19: Fraction(-2117855228554753792,173867925),
    20: Fraction(12162234158979734656,521603775),
}
cumulative = sum(charges.values(), Fraction())
assert cumulative == Fraction(7534667963437738624,521603775)
result = {
    "status":"PASS_CORRECTED_COMPLETE_CHARGE_LEDGER_THROUGH_K20",
    "charges":{f"K{k}":fq(v) for k,v in charges.items()},
    "cumulative_K14_through_K20":fq(cumulative),
    "required_aggregate_K21_through_K24_compensation":fq(-cumulative),
    "coverage":{"K18":17,"K19":24,"K20":36},
    "sources":{str(k):{"path":str(v.relative_to(ROOT)),"sha256":sha(v)} for k,v in FILES.items()},
    "scope":"Exact 77-cycle conservation ledger under the frozen filtered convention; aggregate only, not a degreewise prediction, residual checkpoint, or ideal-membership verdict.",
}
tmp=HERE/"results_charge_ledger_through_k20.json.tmp"; out=HERE/"results_charge_ledger_through_k20.json"
tmp.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");tmp.replace(out)
print(json.dumps(result,sort_keys=True))

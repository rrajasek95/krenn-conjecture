#!/usr/bin/env python3
"""Independent arithmetic/source referee for the direct-K19 permutation repair."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

OLD_SOURCE = ROOT / "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/merge_and_charge_k19.rs"
OLD_RESULT = ROOT / "computations/unaudited-codex-orbit0-k19-charge-2026-08-23/results_k19_charge.json"
COMPLETE_K19 = ROOT / "computations/unaudited-codex-orbit0-k19-complete-charge-2026-08-23/results_complete_k19_charge.json"
REPAIR_DIR = ROOT / "computations/unaudited-codex-orbit0-k19-direct-conservation-audit-2026-08-24"
REPAIR_SOURCE = REPAIR_DIR / "recompute_d19_parent_charge.rs"
REPAIR_TRANSCRIPT = REPAIR_DIR / "results_recompute_d19_parent_charge.txt"
DIRECT_SOURCE = REPAIR_DIR / "recompute_all_direct_packet_charges.rs"
DIRECT_TRANSCRIPT = REPAIR_DIR / "results_recompute_all_direct_packet_charges.txt"
K21_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k21-charge-assembly-2026-08-24/k21_manifest_complete_52.json"
K22_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k22-charge-assembly-2026-08-24/k22_manifest_complete_76.json"
K23_MANIFEST = ROOT / "computations/unaudited-codex-orbit0-k23-direct-k15-production-interface-2026-08-24/k23_manifest_complete_59_of_59.json"
OLD_K24_AUDIT = ROOT / "computations/unaudited-codex-orbit0-k24-complete35-conservation-audit-2026-08-24/results_k24_complete35_conservation.json"
CUTOFF_R8 = ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/results_orbit0_cutoff9_sparse_r8.json"
ANCHOR_R8 = ROOT / "computations/unaudited-codex-n8-dangerous-chart-bridge-2026-08-20/results_orbit0_anchor_times_r8_unary.json"
CYCLE_QUOTIENT = ROOT / "computations/unaudited-codex-orbit0-k16-weighted-dafsa-2026-08-23/results_k16_cycle_partition_quotient.json"
GLOBAL_INTERFACE = ROOT / "computations/unaudited-codex-orbit0-global-residual-interface-audit-2026-08-23/results_global_residual_interface.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(path: Path):
    return json.loads(path.read_text())


def frac(text: str) -> Fraction:
    return Fraction(text)


def all_dicts(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from all_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from all_dicts(child)


def group_with_ids(document, ids: set[str]):
    matches = []
    for item in all_dicts(document):
        actual = set(item.get("ids", []))
        if actual == ids and "full" in item:
            matches.append(item)
    require(matches, f"missing group {sorted(ids)}")
    first = matches[0]
    require(all(frac(item["full"]) == frac(first["full"]) for item in matches), "ambiguous group scalar")
    return first


def parse_parent_transcript(text: str):
    pattern = re.compile(
        r"^(corrected|historical) rows=(\d+) irreducible_rows=(\d+) "
        r"full=(-?\d+) irreducible=(-?\d+) pivotable=(-?\d+)$"
    )
    delta_pattern = re.compile(r"^delta full=(-?\d+) irreducible=(-?\d+) pivotable=(-?\d+)$")
    out = {}
    for line in text.splitlines():
        if match := pattern.match(line):
            name = match.group(1)
            out[name] = {
                "rows": int(match.group(2)),
                "irreducible_rows": int(match.group(3)),
                "full": int(match.group(4)),
                "irreducible": int(match.group(5)),
                "pivotable": int(match.group(6)),
            }
        elif match := delta_pattern.match(line):
            out["delta"] = {
                "full": int(match.group(1)),
                "irreducible": int(match.group(2)),
                "pivotable": int(match.group(3)),
            }
    require(set(out) == {"corrected", "historical", "delta"}, "incomplete parent transcript")
    return out


def parse_direct_transcript(text: str):
    bucket_pattern = re.compile(r"^K(1[4-9]|20) rows=(\d+) charge=(-?\d+)$")
    total_pattern = re.compile(r"^total_charge=(-?\d+)$")
    buckets = {}
    total = None
    for line in text.splitlines():
        if match := bucket_pattern.match(line):
            buckets[int(match.group(1))] = {"rows": int(match.group(2)), "charge": int(match.group(3))}
        elif match := total_pattern.match(line):
            total = int(match.group(1))
    require(set(buckets) == set(range(14, 21)), "direct transcript bucket coverage")
    require(total is not None, "direct transcript total")
    require(sum(item["charge"] for item in buckets.values()) == total, "direct bucket sum")
    return buckets, total


def main() -> None:
    old_source = OLD_SOURCE.read_text()
    compact_old = "".join(old_source.split())
    require("forhiin0..3" in compact_old, "historical high loop missing")
    require("e.factor[o[0]][1]" in compact_old, "historical K3 selector changed")
    require("e.factor[o[1]][2]" in compact_old and "e.factor[hi][2]" in compact_old, "historical K4 selectors changed")

    # For hi=0,1,2, o[0] is respectively factor 1,0,0.  Thus factor 0 is
    # duplicated as the K3 family and factor 2 is absent.
    historical_k3_factor_by_iteration = [1, 0, 0]
    require(historical_k3_factor_by_iteration.count(0) == 2, "factor-0 duplication")
    require(2 not in historical_k3_factor_by_iteration, "factor-2 omission")

    repair_source = REPAIR_SOURCE.read_text()
    compact_repair = "".join(repair_source.split())
    require("forlowin0..3" in compact_repair, "corrected low loop missing")
    require("e.factor[low][1]" in compact_repair, "corrected K3 selector missing")

    parent = parse_parent_transcript(REPAIR_TRANSCRIPT.read_text())
    corrected = parent["corrected"]
    historical = parent["historical"]
    delta = parent["delta"]
    require(corrected["rows"] == historical["rows"] == 167_616_000, "row-count equality")
    require(corrected["irreducible_rows"] == historical["irreducible_rows"] == 55_872_000, "irreducible-count equality")
    require(corrected["full"] - corrected["irreducible"] == corrected["pivotable"], "corrected decomposition")
    require(historical["full"] - historical["irreducible"] == historical["pivotable"], "historical decomposition")
    for key in ("full", "irreducible", "pivotable"):
        require(corrected[key] - historical[key] == delta[key], f"delta {key}")

    old_result = load(OLD_RESULT)["components"]["direct_k19"]
    require(int(old_result["full_charge"]["numerator"]) == historical["full"], "historical full pin")
    require(int(old_result["K19_irreducible_charge"]["numerator"]) == historical["irreducible"], "historical irreducible pin")

    d19_r2 = {"D19:344|R:2", "D19:434|R:2", "D19:443|R:2"}
    d19_r3 = {"D19:344|R:3", "D19:434|R:3", "D19:443|R:3"}
    d19_r4 = {"D19:344|R:4", "D19:434|R:4", "D19:443|R:4"}
    child_groups = {
        "K21_D19_R2": group_with_ids(load(K21_MANIFEST), d19_r2),
        "K22_D19_R3": group_with_ids(load(K22_MANIFEST), d19_r3),
        "K23_D19_R4": group_with_ids(load(K23_MANIFEST), d19_r4),
    }
    child_full = {name: frac(group["full"]) for name, group in child_groups.items()}
    child_sum = sum(child_full.values(), Fraction())
    require(child_sum.denominator == 1, "D19 child sum integrality")
    require(child_sum == corrected["pivotable"], "corrected local identity")
    historical_local_residual = Fraction(historical["pivotable"]) - child_sum
    require(historical_local_residual == 12_662_784, "historical local defect")

    direct_buckets, direct_total = parse_direct_transcript(DIRECT_TRANSCRIPT.read_text())
    require(direct_buckets[19]["charge"] == corrected["full"], "generic/direct corrected K19 agreement")
    require(direct_total == 4_564_224, "leading-input charge")

    old_complete_k19 = load(COMPLETE_K19)["K19"]["corrected_complete_24_path_total"]
    corrected_complete_k19 = {
        "full": frac(old_complete_k19["full"]["text"]) + delta["full"],
        "irreducible": frac(old_complete_k19["irreducible"]["text"]) + delta["irreducible"],
    }

    old_terminal = frac(load(OLD_K24_AUDIT)["cumulative_K14_through_K24"]["text"])
    corrected_terminal = old_terminal + delta["irreducible"]
    require(old_terminal == 19_715_328, "old terminal value")
    require(corrected_terminal == direct_total, "terminal equals actual recurrence input")

    cutoff = load(CUTOFF_R8)
    anchor = load(ANCHOR_R8)
    cycle = load(CYCLE_QUOTIENT)
    global_interface = load(GLOBAL_INTERFACE)
    require(cutoff["cutoff"] == 9 and cutoff["residual_K_degree"] == 8, "R8prime cutoff scope")
    require("modulo I_mix+K^9" in cutoff["conclusion"], "R8prime is only a cutoff representative")
    require("does not yet put the full a*T" in anchor["scope_guard"], "missing full-target guard")
    require("K9 tail" in anchor["scope_guard"], "missing K9-tail guard")
    require(cycle["original_structured_aT_pairing"] == 0, "structured target pairing")
    require(global_interface["exact_input"]["identity"] == "full pre-reduction residual is -R8prime*E0*E1*E2", "recurrence input identity")
    require("undefined from the archive" in global_interface["requested_global_charge"], "global charge scope")

    pins = {}
    for path in (
        OLD_SOURCE, OLD_RESULT, COMPLETE_K19, REPAIR_SOURCE, REPAIR_TRANSCRIPT,
        DIRECT_SOURCE, DIRECT_TRANSCRIPT, K21_MANIFEST, K22_MANIFEST, K23_MANIFEST,
        OLD_K24_AUDIT, CUTOFF_R8, ANCHOR_R8, CYCLE_QUOTIENT, GLOBAL_INTERFACE,
    ):
        pins[str(path.relative_to(ROOT))] = digest(path)

    def rational(value: Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator, "text": str(value)}

    result = {
        "status": "PASS_INDEPENDENT_K19_PERMUTATION_REPAIR_AND_CORRECTED_CONSERVATION",
        "bug": {
            "historical_K3_factor_sequence": historical_k3_factor_by_iteration,
            "duplicated_K3_factor": 0,
            "omitted_K3_factor": 2,
            "why_counts_matched": "all three factor families have identical K3/K4 cardinalities; the bad multiset [1,0,0] and correct [0,1,2] both enumerate 3*32*60*60 rows per R8prime record",
        },
        "direct_K19": {"historical": historical, "corrected": corrected, "delta": delta},
        "local_identity": {
            "rule": "parent full - parent irreducible = sum of signed full charges of all K2/K3/K4 children",
            "child_full": {key: rational(value) for key, value in child_full.items()},
            "child_full_sum": rational(child_sum),
            "corrected_parent_pivotable": corrected["pivotable"],
            "corrected_residual": 0,
            "historical_residual": int(historical_local_residual),
        },
        "terminal_ledger_distinction": {
            "old_cumulative_K14_K24": rational(old_terminal),
            "ledger_relevant_correction_is_irreducible_delta": delta["irreducible"],
            "not_the_pivotable_delta": delta["pivotable"],
            "corrected_cumulative_K14_K24": rational(corrected_terminal),
            "corrected_complete_K19": {key: rational(value) for key, value in corrected_complete_k19.items()},
        },
        "actual_input": {
            "polynomial": "P=-R8prime*E0*E1*E2",
            "direct_buckets": {str(key): value for key, value in direct_buckets.items()},
            "exact_charge": direct_total,
            "corrected_terminal_equals_input": corrected_terminal == direct_total,
        },
        "theorem_scope": {
            "original_structured_aT_pairing": cycle["original_structured_aT_pairing"],
            "R8prime_scope": "T is congruent to R8prime only modulo I_mix+K^9; the omitted K9 tail is not in the bounded P stream",
            "zero_conservation_applies_to_complete_aT_stream": True,
            "zero_conservation_applies_to_bounded_P_stream": False,
            "conclusion": "the prior +19715328 zero-baseline obstruction is superseded; after the K19 irreducible correction the bounded terminal ledger conserves its actual input charge +4564224 exactly",
        },
        "scope_guard": "This validates scalar charge conservation for the frozen orbit-zero P recurrence. It does not reconstruct the missing a*T K9-tail stream, produce a literal K24 residual/span certificate, globalize to the other charts, or decide the Krenn-Gu conjecture.",
        "source_sha256": pins,
    }
    out = HERE / "results_k19_permutation_conservation_referee.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()

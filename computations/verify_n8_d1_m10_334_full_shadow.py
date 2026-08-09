#!/usr/bin/env python3
"""Exact complete-shadow closure of the N=8 D1 m=10 3+3+4 family."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
from collections import Counter
from functools import lru_cache
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_433_SHA256 = (
    "463627051b215c4c21bf96978376aaef512a98177562bf467993dce2e340a87f"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_433_full_shadow.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest() == PINNED_433_SHA256,
            "the committed 4+3+3 closure source changed")
G = importlib.import_module("verify_n8_d1_m10_433_full_shadow")
H, F, I, A, D = G.H, G.F, G.I, G.A, G.D

PINNED_CANDIDATE_CLOSURE_SHA256 = (
    "884a453002824eb99fe4cda57f1adfbf14d64f636d91cef441b4721c63d96fe5"
)
CLOSURE_SOURCE = os.path.join(
    HERE, "verify_n8_d1_m10_334_branch63_ideal_closure.py"
)
with open(CLOSURE_SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_CANDIDATE_CLOSURE_SHA256,
            "the committed branch-63 ideal closure changed")
K = importlib.import_module("verify_n8_d1_m10_334_branch63_ideal_closure")
CANDIDATE_EXTRAS = K.C.candidate_input()[1]

PALETTE_PATH = os.path.join(
    HERE, "certificates", "n8_d1_m10_334_rup_palettes.json"
)
EXPECTED_PALETTE_SHA256 = (
    "5af17387cf56780b0f358ba91b393e7658047197425164ee49057d4205d4ad27"
)
EXPECTED_LEDGER_SHA256 = (
    "be640c9830a68b5a671fbc403f646ae8e6ce80f63e7896899ef083203fa0907a"
)


@lru_cache(maxsize=1)
def family_branches():
    branches, admissible, sigma, off_sigma = I.surviving_branches()
    rows = [(index, state) for family, index, state in branches
            if family == "334"]
    require(len(rows) == 131, "the 3+3+4 symbolic frontier changed")
    return rows, admissible, sigma, off_sigma


def dynamic_residuals(state, admissible, sigma, off_sigma):
    initial, anchor_units = state
    seen, residuals = set(), set()
    stats = Counter()

    def search(base, remaining):
        key = base, remaining
        if key in seen:
            return
        seen.add(key)
        stats["nodes"] += 1
        certificate = F.choose_dynamic_repair(
            (base, anchor_units), remaining,
            admissible, sigma, off_sigma,
        )
        if certificate is not None and certificate["repair"] is None:
            stats["dynamic_unique_closures"] += 1
            return
        if remaining == 0:
            residuals.add(base)
            return
        if certificate is not None:
            stats["repair_DNF_nodes"] += 1
            for repair in certificate["repair"]:
                search(frozenset(set(base) | set(repair)),
                       remaining - len(repair))
            return
        stats["free_extension_nodes"] += 1
        for entry in sorted(off_sigma - set(base)):
            search(base | {entry}, remaining - 1)

    search(initial, 4)
    return sorted(residuals, key=lambda row: tuple(sorted(row))), stats


def check_branch(index, palettes, discover=False):
    branches, admissible, sigma, off_sigma = family_branches()
    state = dict(branches)[index]
    supports, stats = dynamic_residuals(
        state, admissible, sigma, off_sigma
    )
    union = frozenset().union(*palettes) if palettes else frozenset()
    hits, direct, coefficient = 0, 0, 0
    for support in supports:
        certificate = F.direct_complete_support_certificate(
            (support, state[1]), admissible, sigma
        )
        if certificate is not None:
            direct += 1
            continue
        if union:
            compact = F.build_fixed_full_shadow(
                support, state[1], admissible, sigma, off_sigma, union
            )
            if A.M8.unit_refutation(compact.clauses) is not None:
                hits += 1
                continue
        if index in (63, 79):
            require(support == CANDIDATE_EXTRAS,
                    "a known coefficient survivor changed support")
            coefficient += 1
            continue
        require(discover,
                "branch 334:%d has a complete-shadow survivor" % index)
        full = F.build_fixed_full_shadow(
            support, state[1], admissible, sigma, off_sigma
        )
        core = F.unit_refutation_core_fibres(full)
        require(core is not None,
                "branch 334:%d has a complete-shadow SAT support" % index)
        palette = core["fibres"]
        compact = F.build_fixed_full_shadow(
            support, state[1], admissible, sigma, off_sigma, palette
        )
        require(A.M8.unit_refutation(compact.clauses) is not None,
                "an extracted 3+3+4 RUP palette failed its check")
        palettes.append(palette)
        union = frozenset(set(union) | set(palette))
        hits += 1
    require(direct + hits + coefficient == len(supports),
            "a 3+3+4 complete support was not closed")
    return {
        "branch": index,
        "dynamic_nodes": stats["nodes"],
        "dynamic_unique_closures": stats["dynamic_unique_closures"],
        "repair_DNF_nodes": stats["repair_DNF_nodes"],
        "free_extension_nodes": stats["free_extension_nodes"],
        "complete_support_residuals": len(supports),
        "direct_complete_support_closures": direct,
        "palette_RUP_closures": hits,
        "coefficient_ideal_closures": coefficient,
    }, palettes


def worker_command(index, discover):
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend([os.path.abspath(__file__), "--worker", str(index)])
    if discover:
        command.append("--discover")
    return command


def run_worker(index, palettes, discover=False):
    payload = json.dumps(H.encode_palettes(palettes), separators=(",", ":"))
    result = subprocess.run(
        worker_command(index, discover), input=payload, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        cwd=HERE,
    )
    require(result.returncode == 0,
            "334:%d worker failed: %s" % (index, result.stderr.strip()))
    output = json.loads(result.stdout)
    return output["row"], H.decode_palettes(output["palettes"])


def audit(rows):
    started = monotonic()
    closure_ledger, closure_digest, _seconds = K.audit()
    with open(PALETTE_PATH, "rb") as handle:
        raw = handle.read()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_PALETTE_SHA256,
            "the frozen 3+3+4 RUP palettes changed")
    palettes = H.decode_palettes(json.loads(raw.decode("ascii")))
    require(len(rows) == 131, "the complete 3+3+4 batch census changed")
    ledger = {
        "pinned_433_sha256": PINNED_433_SHA256,
        "pinned_candidate_closure_sha256": PINNED_CANDIDATE_CLOSURE_SHA256,
        "candidate_closure_ledger_sha256": closure_digest,
        "palette_sha256": hashlib.sha256(raw).hexdigest(),
        "inherited_433_palettes": 30,
        "total_root_RUP_palettes": len(palettes),
        "palette_sizes": [len(palette) for palette in palettes],
        "symbolic_branches_closed": len(rows),
        "dynamic_nodes": sum(row["dynamic_nodes"] for row in rows),
        "dynamic_unique_closures": sum(
            row["dynamic_unique_closures"] for row in rows
        ),
        "complete_support_residuals": sum(
            row["complete_support_residuals"] for row in rows
        ),
        "direct_complete_support_closures": sum(
            row["direct_complete_support_closures"] for row in rows
        ),
        "palette_RUP_closures": sum(
            row["palette_RUP_closures"] for row in rows
        ),
        "coefficient_ideal_closures": sum(
            row["coefficient_ideal_closures"] for row in rows
        ),
        "coefficient_survivor_branches": [
            row["branch"] for row in rows
            if row["coefficient_ideal_closures"]
        ],
        "distinct_coefficient_supports": 1,
        "branch_rows": rows,
        "remaining_m10_symbolic_branches": 0,
        "characteristic_scope": closure_ledger["characteristic_scope"],
        "status": ("the complete m=10 D1 frontier is empty over every "
                   "field of characteristic != 2"),
    }
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "the complete 3+3+4 shadow ledger changed")
    return ledger, digest, monotonic() - started


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--worker", type=int)
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--batch-start", type=int)
    parser.add_argument("--batch-end", type=int)
    parser.add_argument("--batch-output")
    parser.add_argument("--aggregate-dir")
    args = parser.parse_args()
    if args.worker is not None:
        palettes = H.decode_palettes(json.loads(sys.stdin.read()))
        row, palettes = check_branch(args.worker, palettes, args.discover)
        print(json.dumps({"row": row,
                          "palettes": H.encode_palettes(palettes)},
                         sort_keys=True, separators=(",", ":")))
        return
    if args.batch_start is not None:
        require(args.batch_end is not None,
                "a batch end is required with a batch start")
        with open(PALETTE_PATH, "rb") as handle:
            palettes = H.decode_palettes(json.loads(handle.read()))
        branches, _admissible, _sigma, _off_sigma = family_branches()
        rows = []
        for index, _state in branches[args.batch_start:args.batch_end]:
            row, returned = check_branch(index, list(palettes), False)
            require(returned == palettes,
                    "a checking worker mutated the frozen palettes")
            rows.append(row)
        payload = json.dumps(rows, sort_keys=True, separators=(",", ":"))
        if args.batch_output:
            with open(args.batch_output, "w") as handle:
                handle.write(payload)
        else:
            print(payload)
        return
    require(args.aggregate_dir is not None,
            "use --aggregate-dir after checking isolated batches")
    rows = []
    for filename in sorted(os.listdir(args.aggregate_dir),
                           key=lambda value: int(value.split(".")[0])):
        with open(os.path.join(args.aggregate_dir, filename), "r") as handle:
            rows.extend(json.load(handle))
    ledger, digest, seconds = audit(rows)
    print("n8 D1 m=10 complete 3+3+4 shadow: PASS (exact)")
    print("branches closed:", ledger["symbolic_branches_closed"])
    print("dynamic nodes:", ledger["dynamic_nodes"])
    print("complete supports:", ledger["complete_support_residuals"])
    print("RUP palettes:", ledger["total_root_RUP_palettes"])
    print("coefficient support occurrences closed:",
          ledger["coefficient_ideal_closures"])
    print("remaining m=10 symbolic branches: 0")
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()

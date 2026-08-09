#!/usr/bin/env python3
"""Exact complete-shadow closure of the N=8 D1 m=10 3+4+3 family."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
from collections import Counter
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINNED_PAIR_CLOSURE_SHA256 = (
    "5f1a425d341d05e1d62d06e831bfe440de36588417989a59a6bb2cbf61de6c78"
)
SOURCE = os.path.join(HERE, "verify_n8_d1_m10_442_4_full_shadow.py")
with open(SOURCE, "rb") as handle:
    require(hashlib.sha256(handle.read()).hexdigest()
            == PINNED_PAIR_CLOSURE_SHA256,
            "the committed pair-shadow source changed")
F = importlib.import_module("verify_n8_d1_m10_442_4_full_shadow")
I, A, V, D = F.I, F.A, F.V, F.D

PALETTE_PATH = os.path.join(
    HERE, "certificates", "n8_d1_m10_343_rup_palettes.json"
)
EXPECTED_PALETTE_SHA256 = (
    "bd415532c49edad0df200a6a59debea79cba89a54389a79f99e6a5565ff11319"
)
EXPECTED_LEDGER_SHA256 = (
    "3c0dcf1d30ce34e4daf3f8f5389bd7084ba178b27b4c62c8b519e8338a6af6f2"
)


def encode_palettes(palettes):
    return [[ [list(domain), list(values), pure]
              for domain, values, pure in sorted(
                  palette, key=lambda row: (row[0], row[1], row[2]))]
            for palette in palettes]


def decode_palettes(payload):
    return [frozenset((tuple(domain), tuple(values), pure)
                      for domain, values, pure in palette)
            for palette in payload]


def family_branches():
    branches, admissible, sigma, off_sigma = I.surviving_branches()
    rows = [(index, state) for family, index, state in branches
            if family == "343"]
    require(len(rows) == 58, "the 3+4+3 symbolic frontier changed")
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

    search(initial, 3)
    return sorted(residuals, key=lambda row: tuple(sorted(row))), stats


def check_branch(index, palettes, discover=False):
    branches, admissible, sigma, off_sigma = family_branches()
    state = dict(branches)[index]
    supports, stats = dynamic_residuals(
        state, admissible, sigma, off_sigma
    )
    hits = Counter()
    direct = 0
    combined_palette = frozenset().union(*palettes) if palettes else frozenset()
    for support in supports:
        complete_state = support, state[1]
        certificate = F.direct_complete_support_certificate(
            complete_state, admissible, sigma
        )
        if certificate is not None:
            direct += 1
            continue
        if combined_palette:
            cnf = F.build_fixed_full_shadow(
                support, state[1], admissible, sigma, off_sigma,
                combined_palette,
            )
            if A.M8.unit_refutation(cnf.clauses) is not None:
                hits["union"] += 1
                continue
        if not discover:
            require(False,
                    "branch 343:%d has a complete-shadow survivor" % index)
        else:
            full = F.build_fixed_full_shadow(
                support, state[1], admissible, sigma, off_sigma
            )
            core = F.unit_refutation_core_fibres(full)
            require(core is not None,
                    "branch 343:%d has a complete-shadow SAT support" % index)
            palette = core["fibres"]
            compact = F.build_fixed_full_shadow(
                support, state[1], admissible, sigma, off_sigma, palette
            )
            require(A.M8.unit_refutation(compact.clauses) is not None,
                    "an extracted root-RUP palette failed its check")
            palettes.append(palette)
            combined_palette = frozenset(set(combined_palette) | set(palette))
            hits["union"] += 1
    row = {
        "branch": index,
        "dynamic_nodes": stats["nodes"],
        "dynamic_unique_closures": stats["dynamic_unique_closures"],
        "repair_DNF_nodes": stats["repair_DNF_nodes"],
        "free_extension_nodes": stats["free_extension_nodes"],
        "complete_support_residuals": len(supports),
        "direct_complete_support_closures": direct,
        "palette_RUP_closures": sum(hits.values()),
        "palette_hit_histogram": dict(sorted(hits.items())),
    }
    require(direct + sum(hits.values()) == len(supports),
            "a 3+4+3 complete support was not closed")
    return row, palettes


def worker_command(index, discover):
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend([os.path.abspath(__file__), "--worker", str(index)])
    if discover:
        command.append("--discover")
    return command


def run_worker(index, palettes, discover=False):
    payload = json.dumps(encode_palettes(palettes), separators=(",", ":"))
    result = subprocess.run(
        worker_command(index, discover), input=payload, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
        cwd=HERE,
    )
    require(result.returncode == 0,
            "343:%d worker failed: %s" % (index, result.stderr.strip()))
    output = json.loads(result.stdout)
    return output["row"], decode_palettes(output["palettes"])


def run_batch(start, end, palettes):
    command = [sys.executable]
    if sys.flags.optimize:
        command.append("-O")
    command.extend([os.path.abspath(__file__), "--batch-start", str(start),
                    "--batch-end", str(end)])
    result = subprocess.run(
        command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False, cwd=HERE,
    )
    require(result.returncode == 0,
            "343 batch %d:%d failed: %s"
            % (start, end, result.stderr.strip()))
    return json.loads(result.stdout)


def audit(rows=None):
    started = monotonic()
    with open(PALETTE_PATH, "rb") as handle:
        raw = handle.read()
    if EXPECTED_PALETTE_SHA256 != "TO_BE_FROZEN":
        require(hashlib.sha256(raw).hexdigest() == EXPECTED_PALETTE_SHA256,
                "the frozen 3+4+3 RUP palettes changed")
    palettes = decode_palettes(json.loads(raw.decode("ascii")))
    branches, _admissible, _sigma, _off_sigma = family_branches()
    if rows is None:
        rows = []
        for start in range(0, len(branches), 3):
            rows.extend(run_batch(start, min(start + 3, len(branches)),
                                  palettes))
    require(len(rows) == 58
            and sum(row["complete_support_residuals"] for row in rows) > 0,
            "the 3+4+3 complete-shadow census changed")
    ledger = {
        "pinned_pair_closure_sha256": PINNED_PAIR_CLOSURE_SHA256,
        "palette_sha256": hashlib.sha256(raw).hexdigest(),
        "root_RUP_palettes": len(palettes),
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
        "branch_rows": rows,
        "remaining_m10_symbolic_branches": 185,
        "status": ("the complete m=10 3+4+3 support-shadow family is "
                   "empty; only 3+3+4 and 4+3+3 remain"),
    }
    digest = D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "the complete 3+4+3 shadow ledger changed")
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
        palettes = decode_palettes(json.loads(sys.stdin.read()))
        row, palettes = check_branch(
            args.worker, palettes, discover=args.discover
        )
        print(json.dumps({"row": row,
                          "palettes": encode_palettes(palettes)},
                         sort_keys=True, separators=(",", ":")))
        return
    if args.batch_start is not None:
        require(args.batch_end is not None,
                "a batch end is required with a batch start")
        with open(PALETTE_PATH, "rb") as handle:
            palettes = decode_palettes(json.loads(handle.read()))
        branches, _admissible, _sigma, _off_sigma = family_branches()
        rows = []
        for index, _state in branches[args.batch_start:args.batch_end]:
            row, returned = check_branch(
                index, list(palettes), discover=False
            )
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
    rows = None
    if args.aggregate_dir:
        rows = []
        for filename in sorted(os.listdir(args.aggregate_dir),
                               key=lambda value: int(value.split(".")[0])):
            with open(os.path.join(args.aggregate_dir, filename), "r") as handle:
                rows.extend(json.load(handle))
    ledger, digest, seconds = audit(rows)
    print("n8 D1 m=10 complete 3+4+3 shadow: PASS (exact)")
    print("branches closed:", ledger["symbolic_branches_closed"])
    print("dynamic nodes:", ledger["dynamic_nodes"])
    print("complete supports:", ledger["complete_support_residuals"])
    print("RUP palettes:", ledger["root_RUP_palettes"])
    print("remaining m=10 symbolic branches: 185")
    print("ledger sha256:", digest)
    print("total: %.1f s" % seconds)


if __name__ == "__main__":
    main()

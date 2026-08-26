#!/usr/bin/env python3
"""Bounded exact sweep of small fixed loci for one site/color permutation.

Conjugacy classes in S_8 x S_3 are indexed by a partition of 8 and a
partition of 3.  For each class, a consecutive-cycle representative acts on
the 252 endpoint-ordered cells.  Its fixed linear subspace has one coordinate
per cell orbit.  This script exhausts, up to conjugacy, every class having at
most 33 such coordinates, builds all raw X4 equations, and asks Singular for
an exact characteristic-zero decision under a declared timeout.

UNIT means the entire fixed locus is X4-empty.  NONUNIT means the reduced
ideal is proper and hence has a Qbar point, but coordinates/carriers still
need extraction.  TIMEOUT is no verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
from collections import Counter
from itertools import product
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import classify_equivariant as CE  # noqa: E402


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def partitions(n, maximum=None):
    if n == 0:
        yield ()
        return
    maximum = n if maximum is None else min(n, maximum)
    for first in range(maximum, 0, -1):
        for tail in partitions(n - first, first):
            yield (first,) + tail


def permutation(cycle_type):
    answer = [None] * sum(cycle_type)
    start = 0
    for length in cycle_type:
        cycle = tuple(range(start, start + length))
        for index, value in enumerate(cycle):
            answer[value] = cycle[(index + 1) % length]
        start += length
    return tuple(answer)


def transformed(cell, site_perm, color_perm):
    u, v, a, b = cell
    u, v, a, b = site_perm[u], site_perm[v], color_perm[a], color_perm[b]
    return (u, v, a, b) if u < v else (v, u, b, a)


def quotient(site_type, color_type):
    site_perm, color_perm = permutation(site_type), permutation(color_type)
    raw_representatives = []
    orbit_sizes = {}
    for raw in CE.CELLS:
        orbit, current = [], raw
        while current not in orbit:
            orbit.append(current)
            current = transformed(current, site_perm, color_perm)
        representative = min(CE.INDEX[cell] for cell in orbit)
        raw_representatives.append(representative)
        orbit_sizes[representative] = len(orbit)
    representatives = sorted(set(raw_representatives))
    compact = {representative: index for index, representative in enumerate(representatives)}
    qmap = tuple(compact[representative] for representative in raw_representatives)
    require(sum(orbit_sizes.values()) == 252, "cell orbits do not partition")
    return qmap, representatives, orbit_sizes


def endpoint_transpose_mutation_control():
    """Omit the required color-index swap when a site edge reverses."""
    site_perm, color_perm = permutation((8,)), permutation((3,))
    image = []
    for u, v, a, b in CE.CELLS:
        pu, pv, pa, pb = site_perm[u], site_perm[v], color_perm[a], color_perm[b]
        mutant = (pu, pv, pa, pb) if pu < pv else (pv, pu, pa, pb)
        image.append(CE.INDEX[mutant])
    require(len(set(image)) == 252, "endpoint mutant is not a permutation")
    seen, sizes = set(), []
    for start in range(252):
        if start in seen:
            continue
        current, size = start, 0
        while current not in seen:
            seen.add(current)
            current = image[current]
            size += 1
        sizes.append(size)
    histogram = dict(sorted(Counter(sizes).items()))
    require(len(sizes) == 12 and histogram == {12: 3, 24: 9}, histogram)
    return {
        "mutation": "endpoint reversal without transposing color indices",
        "mutant_quotient_variables": len(sizes),
        "mutant_orbit_histogram": histogram,
        "correct_quotient_variables": 11,
        "fired": len(sizes) != 11,
    }


def generators(qmap, variable_count):
    polynomials = {}
    raw_counts = Counter()
    for word in product(CE.COLORS, repeat=8):
        word = tuple(word)
        off = CE.off_count(word)
        if off > 4:
            continue
        raw_counts[off] += 1
        polynomial = CE.polynomial(word, qmap, variable_count)
        if polynomial:
            polynomials.setdefault(polynomial, word)
    return list(polynomials), polynomials, dict(sorted(raw_counts.items()))


def singular_decision(generator_list, variable_count, timeout):
    names = ",".join(f"x{i + 1}" for i in range(variable_count))
    code = f"ring R=0,({names}),dp; option(redSB);\n"
    code += "ideal I=" + ",\n".join(CE.emit_poly(g) for g in generator_list) + ";\n"
    code += "ideal G=slimgb(I);\n"
    code += '"UNIT:",(size(G)==1 && G[1]==1);\n"DIM:",dim(G);\n"GSIZE:",size(G);\n'
    try:
        completed = subprocess.run(
            ["Singular", "-q", "--no-warn"], input=code, text=True,
            capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "timeout_seconds": timeout}
    require(completed.returncode == 0, completed.stderr or completed.stdout[-2000:])
    require(not any(line.lstrip().startswith("?") for line in completed.stdout.splitlines()),
            completed.stdout[-2000:])
    parsed = {}
    for line in completed.stdout.splitlines():
        for key in ("UNIT", "DIM", "GSIZE"):
            if line.startswith(key + ":"):
                parsed[key] = int(line.split(":", 1)[1])
    require(set(parsed) == {"UNIT", "DIM", "GSIZE"}, completed.stdout)
    return {
        "status": "UNIT" if parsed["UNIT"] else "NONUNIT",
        "dimension": parsed["DIM"],
        "groebner_size": parsed["GSIZE"],
    }


def singular_unit_lift(generator_list, variable_count, timeout):
    names = ",".join(f"x{i + 1}" for i in range(variable_count))
    code = f"ring R=0,({names}),dp; option(redSB);\n"
    code += "ideal I=" + ",\n".join(CE.emit_poly(g) for g in generator_list) + ";\n"
    code += "ideal T=1; matrix L=lift(I,T);\n"
    code += (
        "if(nrows(L)!=size(I) || ncols(L)!=1)"
        "{ print(\"UNIT_LIFT_SHAPE_FAILED\"); exit(1); }\n"
        "if(matrix(I)*L-matrix(T)!=0)"
        "{ print(\"SOURCE_IDENTITY_FAILED\"); exit(1); }\n"
    )
    code += "int i; int nz=0; for(i=1;i<=nrows(L);i++){if(L[i,1]!=0){nz=nz+1;}}\n"
    code += 'print("NONZERO"); print(nz); print("BEGIN_LIFT"); L; print("END_LIFT");\n'
    try:
        completed = subprocess.run(
            ["Singular", "-q", "--no-warn"], input=code, text=True,
            capture_output=True, timeout=timeout, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "timeout_seconds": timeout}
    if completed.returncode != 0 or "SOURCE_IDENTITY_FAILED" in completed.stdout \
            or "UNIT_LIFT_SHAPE_FAILED" in completed.stdout:
        marker = ("SOURCE_IDENTITY_FAILED" if "SOURCE_IDENTITY_FAILED" in completed.stdout
                  else "UNIT_LIFT_SHAPE_FAILED" if "UNIT_LIFT_SHAPE_FAILED" in completed.stdout
                  else f"RETURN_CODE_{completed.returncode}")
        return {"status": "FAILED", "reason": marker}
    lines = completed.stdout.splitlines()
    marker = lines.index("NONZERO")
    nonzero = int(lines[marker + 1])
    lift_text = completed.stdout.split("BEGIN_LIFT\n", 1)[1].split("\nEND_LIFT", 1)[0]
    return {"status": "VERIFIED", "active_rows": nonzero,
            "lift_sha256": hashlib.sha256(lift_text.encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-variables", type=int, default=0)
    parser.add_argument("--max-variables", type=int, default=33)
    parser.add_argument("--decision-timeout", type=int, default=10)
    parser.add_argument("--lift-timeout", type=int, default=30)
    args = parser.parse_args()
    all_classes = []
    for site_type in partitions(8):
        for color_type in partitions(3):
            qmap, representatives, orbit_sizes = quotient(site_type, color_type)
            all_classes.append((site_type, color_type, qmap, representatives, orbit_sizes))
    require(len(all_classes) == 66, len(all_classes))
    selected = [record for record in all_classes
                if args.min_variables <= len(record[3]) <= args.max_variables]
    if args.min_variables == 0 and args.max_variables == 33:
        require(len(selected) == 12, len(selected))
        expected = {
            ((8,), (3,)), ((7, 1), (3,)), ((5, 2, 1), (3,)),
            ((5, 3), (2, 1)), ((7, 1), (2, 1)), ((4, 4), (3,)),
            ((5, 1, 1, 1), (3,)), ((5, 3), (3,)),
            ((4, 2, 2), (3,)), ((4, 2, 1, 1), (3,)),
            ((8,), (1, 1, 1)), ((8,), (2, 1)),
        }
        require({(row[0], row[1]) for row in selected} == expected,
                "selected conjugacy class list changed")

    records = []
    for site_type, color_type, qmap, representatives, orbit_sizes in sorted(
        selected, key=lambda item: (len(item[3]), item[0], item[1])
    ):
        generator_list, polynomial_words, raw_counts = generators(qmap, len(representatives))
        decision = singular_decision(generator_list, len(representatives), args.decision_timeout)
        lift = None
        if decision["status"] == "UNIT":
            lift = singular_unit_lift(generator_list, len(representatives), args.lift_timeout)
        record = {
            "site_cycle_type": list(site_type),
            "color_cycle_type": list(color_type),
            "action_order": math.lcm(*site_type, *color_type),
            "quotient_variables": len(representatives),
            "cell_orbit_size_histogram": dict(sorted(Counter(orbit_sizes.values()).items())),
            "distinct_nonzero_generators": len(generator_list),
            "raw_X4_word_counts": raw_counts,
            "generator_sha256": hashlib.sha256(
                "\n".join(CE.emit_poly(g) for g in generator_list).encode()
            ).hexdigest(),
            "decision": decision,
            "unit_lift": lift,
        }
        records.append(record)
        print(site_type, color_type, "vars", len(representatives),
              "gens", len(generator_list), decision["status"],
              "lift", None if lift is None else lift["status"], flush=True)

    if args.min_variables <= 11 <= args.max_variables:
        cycle012 = next(
            row for row in records
            if row["site_cycle_type"] == [8] and row["color_cycle_type"] == [3]
        )
        require(cycle012["quotient_variables"] == 11
                and cycle012["distinct_nonzero_generators"] == 121
                and cycle012["decision"]["status"] == "UNIT",
                cycle012)
    counts = Counter(row["decision"]["status"] for row in records)
    result = {
        "status": "UNAUDITED_BOUNDED_EXACT_CONJUGACY_SWEEP",
        "group": "S8 x S3 acting covariantly on endpoint cells",
        "exhaustiveness": "Conjugacy classes are exactly pairs of partitions of 8 and 3; all 66 were enumerated and all fixed loci with orbit count <= max_variables retained.",
        "parameters": vars(args),
        "all_conjugacy_classes": len(all_classes),
        "selected_classes": len(selected),
        "decision_histogram": dict(sorted(counts.items())),
        "mutation_controls": {
            "endpoint_transpose": endpoint_transpose_mutation_control(),
            "class_list_exact": True,
        },
        "records": records,
        "scope_warning": "Fixed-locus falsifier coverage only; this is not a universal X4 argument. NONUNIT requires point extraction and carrier audit; TIMEOUT is no verdict.",
    }
    output_name = ("results_equivariant_sweep.json"
                   if args.min_variables == 0 and args.max_variables == 33
                   else f"results_equivariant_sweep_{args.min_variables}_{args.max_variables}.json")
    (HERE / output_name).write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print("SWEEP HISTOGRAM", dict(sorted(counts.items())))


if __name__ == "__main__":
    main()

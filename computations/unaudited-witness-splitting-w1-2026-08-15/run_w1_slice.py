#!/usr/bin/env python3
"""UNAUDITED PROBE (W1, task C) -- COLOUR-SLICE exactness, certificates, blocking.

Pinned HEAD: 26ba69f7e643694c6a58464af6e9e1de9ec92f01

Six-site sources are never exact (Theorem 1.1,
proofs/six-site-arbitrary-complex-obstruction.md), so a six-site J.1 must
be stated on a SUBSYSTEM of the GHZ equations.  The star linearisation
supplies a canonical maximal one.

For a site p the 729 words partition into three COLOUR SLICES
    Slice(p,c) = { w : w_p = c },
and by the star identity the equations of Slice(p,c) involve ONLY the
fifteen star coordinates x = (A_{pv}[c][j])_{v,j} -- linearly:

    H_w = <row(w), x>,   row(w) in Q^15,   for every w in Slice(p,c).

All mixed rows carry right-hand side 0, so the mixed part of a slice is a
HOMOGENEOUS system: it is always solvable (x = 0).  The whole slice
(mixed = 0 and pure = 1) is solvable if and only if

    row(c^6)  is NOT in the span of  { row(w) : w in Slice(p,c) mixed }.  (D)

When (D) fails there is an exact rational certificate lambda with
row(c^6) = sum_w lambda_w row(w), and then for EVERY source with the same
ten blocks off the star at p

    H_{c^6} = sum_{w mixed in Slice(p,c)} lambda_w H_w,                 (L)

so exactness on the mixed part of one colour slice KILLS that colour's GHZ
pure coefficient.  (L) is verified here against the independent coefficient
routine.  Theorem 1.1 says the three slices at a site cannot all be
feasible; this script checks that as a control and measures, per source,

    n_feasible(p) = #{c : slice (p,c) is exactable}

against the witness/blocking status -- the six-site form of the J.1
question: does "every live pair blocked" coincide with "no slice is
exactable"?

Usage: python3 run_w1_slice.py [--samples 20] [--jobs 12]
"""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import as_completed, ProcessPoolExecutor
from fractions import Fraction
import json
import random
import time

from w1_core import (IncSystem, PAIRS, PURE_WORDS, SITES, STAR_DIM, Source,
                     WORDS, all_coefficients, apply_star, blocking_metrics,
                     cofactor_tables, exactness_metrics, matrix_rank, require,
                     star_row, star_vector, structure_metrics, support_fibres)
from run_w1_push import load_shadows
from run_w1_nearexact import build, FAMILIES


def slice_analysis(source, p, colour, tables):
    """Decide (D) for Slice(p,colour); return certificate or solution.

    Exact.  `basis` carries, for every pivot row of the mixed span, the
    combination of original mixed rows producing it, so a dependency of the
    pure row yields the certificate lambda of (L) directly.
    """
    words = [w for w in WORDS if w[p] == colour]
    require(len(words) == 243, "a colour slice has 3^5 words")
    fibres = support_fibres(source)
    mixed = sorted((w for w in words if len(set(w)) > 1),
                   key=lambda w: (fibres[w], w))
    pivots, rows, combos = [], [], []
    for word in mixed:
        row = star_row(tables, p, word)
        combo = {word: Fraction(1)}
        for pivot, base, base_combo in zip(pivots, rows, combos):
            if row[pivot]:
                factor = row[pivot] / base[pivot]
                row = [a - factor * b for a, b in zip(row, base)]
                for key, value in base_combo.items():
                    combo[key] = combo.get(key, Fraction(0)) - factor * value
        pivot = next((n for n, value in enumerate(row) if value), None)
        if pivot is None:
            continue
        pivots.append(pivot)
        rows.append(row)
        combos.append({k: v for k, v in combo.items() if v})
    # reduce the pure row against the mixed span
    pure = star_row(tables, p, PURE_WORDS[colour])
    residual = list(pure)
    certificate = {}
    for pivot, base, combo in zip(pivots, rows, combos):
        if residual[pivot]:
            factor = residual[pivot] / base[pivot]
            residual = [a - factor * b for a, b in zip(residual, base)]
            for key, value in combo.items():
                certificate[key] = certificate.get(key, Fraction(0)) + factor * value
    dependent = not any(residual)
    out = {"colour": colour, "mixed_rank": len(pivots), "feasible": not dependent}
    if dependent:
        out["certificate"] = {k: v for k, v in certificate.items() if v}
    else:
        system = IncSystem(STAR_DIM)
        require(system.add_row(pure, Fraction(1)), "pure row")
        for word in mixed:
            require(system.add_row(star_row(tables, p, word), Fraction(0)),
                    "an independent slice must accept every mixed row")
        out["vector"] = system.project(star_vector(source, p, colour))
        out["solution_rank"] = system.rank()
    return out


def verify_certificate(source, coefficients, certificate, colour):
    """(L) checked with the independent coefficient routine."""
    total = sum(value * coefficients[word]
                for word, value in certificate.items())
    return total == coefficients[PURE_WORDS[colour]]


def analyse_source(entry):
    label, source = entry["label"], entry["source"]
    coefficients = all_coefficients(source)
    structure = structure_metrics(source)
    blocking = blocking_metrics(source, max_degree=2, timeout=30)
    out = {"label": label, "stratum": entry.get("stratum"),
           "base": {"fraction": round(
                        exactness_metrics(source)["mixed_satisfied_fraction"], 6),
                    "noncoordinate": structure["noncoordinate_rank1"],
                    "rank1": structure["rank1_blocks"],
                    "support": structure["support_size"],
                    "live": blocking["live_pairs"],
                    "witness": blocking["witness_pairs"],
                    "all_blocked": blocking["all_live_blocked"]},
           "sites": [], "certificates_verified": 0, "certificate_sizes": []}
    total_feasible = 0
    for p in SITES:
        tables = cofactor_tables(source, p)
        slices = [slice_analysis(source, p, c, tables) for c in range(3)]
        feasible = [item for item in slices if item["feasible"]]
        require(len(feasible) <= 2,
                f"THEOREM 1.1 CONTROL VIOLATED at site {p} of {label}")
        total_feasible += len(feasible)
        record = {"site": p, "n_feasible": len(feasible),
                  "feasible_colours": [item["colour"] for item in feasible],
                  "mixed_ranks": [item["mixed_rank"] for item in slices],
                  "impositions": []}
        for item in slices:
            if item["feasible"]:
                continue
            require(verify_certificate(source, coefficients,
                                       item["certificate"], item["colour"]),
                    f"certificate (L) failed at {label} site {p} "
                    f"colour {item['colour']}")
            out["certificates_verified"] += 1
            out["certificate_sizes"].append(len(item["certificate"]))
        for size in (1, 2):
            if len(feasible) < size:
                continue
            chosen = feasible[:size]
            vectors = {c: star_vector(source, p, c) for c in range(3)}
            for item in chosen:
                vectors[item["colour"]] = item["vector"]
            moved = apply_star(source, p, vectors)
            check = all_coefficients(moved)
            for item in chosen:
                colour = item["colour"]
                bad = [w for w in WORDS if w[p] == colour
                       and check[w] != (1 if len(set(w)) == 1 else 0)]
                require(not bad, f"slice imposition failed at {label} "
                                 f"site {p} colour {colour}")
            metrics = blocking_metrics(moved, max_degree=3, timeout=30)
            struct = structure_metrics(moved)
            exact = exactness_metrics(moved)
            at_p = [list(pair) for pair in PAIRS if p in pair]
            witness_at_p = [pair for pair in at_p
                            if pair in metrics["witness_pair_list"]]
            live_at_p = [pair for pair in at_p
                         if matrix_rank(moved.blocks[tuple(pair)]) > 0]
            record["impositions"].append({
                "colours": [item["colour"] for item in chosen],
                "fraction": round(exact["mixed_satisfied_fraction"], 6),
                "live": metrics["live_pairs"],
                "witness": metrics["witness_pairs"],
                "all_blocked": metrics["all_live_blocked"],
                "live_at_p": len(live_at_p),
                "witness_at_p": len(witness_at_p),
                "noncoordinate": struct["noncoordinate_rank1"],
                "rank1": struct["rank1_blocks"],
                "kinds": struct["kinds"],
                "singletons": exact["singleton_mixed_fibres"],
                "support": struct["support_size"],
                "min_degrees": metrics["min_block_degrees"],
            })
        out["sites"].append(record)
    out["n_feasible_total"] = total_feasible
    return out


def _run(entry):
    start = time.time()
    out = analyse_source(entry)
    out["seconds"] = round(time.time() - start, 1)
    return out


def fleet(samples):
    entries = []
    for shadow in load_shadows():
        entries.append({"label": f"shadow:{shadow['id']}",
                        "stratum": shadow["stratum"],
                        "source": shadow["source"]})
    for order, kind in enumerate(FAMILIES):
        for index in range(samples):
            source, name = build(kind, 70000 + 13 * index + 7 * order)
            if source is None:
                continue
            entries.append({"label": f"{kind}:{index}", "stratum": name,
                            "source": source})
    return entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=12)
    parser.add_argument("--jobs", type=int, default=12)
    parser.add_argument("--out", default="results_slice.json")
    args = parser.parse_args()

    entries = fleet(args.samples)
    print(f"fleet: {len(entries)}", flush=True)
    start = time.time()
    results = []
    handle = open(args.out + ".jsonl", "a")
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(_run, job) for job in entries]
        for number, future in enumerate(as_completed(futures), 1):
            try:
                result = future.result()
            except Exception as error:                      # keep partials
                print(f"  job failed: {type(error).__name__} {error}",
                      flush=True)
                continue
            if result is None:
                continue
            results.append(result)
            handle.write(json.dumps(result) + "\n")
            handle.flush()
            print(f"  {number}/{len(futures)} ({time.time()-start:.0f}s)",
                  flush=True)
    handle.close()

    impositions = [(row, imposition)
                   for row in results for site in row["sites"]
                   for imposition in site["impositions"]]
    single = [item for item in impositions if len(item[1]["colours"]) == 1]
    double = [item for item in impositions if len(item[1]["colours"]) == 2]
    blocked_sources = [row for row in results if row["base"]["all_blocked"]]
    open_sources = [row for row in results if not row["base"]["all_blocked"]]
    summary = {
        "sources": len(results),
        "certificates_verified": sum(row["certificates_verified"]
                                     for row in results),
        "certificate_size_range": [
            min((v for row in results for v in row["certificate_sizes"]),
                default=None),
            max((v for row in results for v in row["certificate_sizes"]),
                default=None)],
        "feasible_slices_per_site": dict(Counter(
            site["n_feasible"] for row in results for site in row["sites"])),
        "max_feasible_slices_per_site": max(
            site["n_feasible"] for row in results for site in row["sites"]),
        "all_blocked_sources": len(blocked_sources),
        "all_blocked_with_a_feasible_slice": sum(
            1 for row in blocked_sources if row["n_feasible_total"] > 0),
        "open_sources": len(open_sources),
        "open_with_a_feasible_slice": sum(
            1 for row in open_sources if row["n_feasible_total"] > 0),
        "n_feasible_total_histogram_blocked": dict(Counter(
            row["n_feasible_total"] for row in blocked_sources)),
        "n_feasible_total_histogram_open": dict(Counter(
            row["n_feasible_total"] for row in open_sources)),
        "single_slice": {
            "cases": len(single),
            "all_blocked": sum(1 for item in single if item[1]["all_blocked"]),
            "no_witness_at_p": sum(1 for item in single
                                   if item[1]["witness_at_p"] == 0),
            "no_witness_at_p_with_live_pairs": sum(
                1 for item in single
                if item[1]["witness_at_p"] == 0 and item[1]["live_at_p"] > 0),
            "blocked_and_noncoordinate": sum(
                1 for item in single
                if item[1]["all_blocked"] and item[1]["noncoordinate"] > 0),
            "witness_histogram": dict(Counter(item[1]["witness"]
                                              for item in single)),
            "live_at_p_histogram": dict(Counter(item[1]["live_at_p"]
                                                for item in single)),
            "noncoordinate_histogram": dict(Counter(item[1]["noncoordinate"]
                                                    for item in single)),
        },
        "double_slice": {
            "cases": len(double),
            "all_blocked": sum(1 for item in double if item[1]["all_blocked"]),
            "no_witness_at_p": sum(1 for item in double
                                   if item[1]["witness_at_p"] == 0),
            "witness_histogram": dict(Counter(item[1]["witness"]
                                              for item in double)),
        },
    }
    with open(args.out, "w") as handle:
        json.dump({"summary": summary, "results": results}, handle, indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()

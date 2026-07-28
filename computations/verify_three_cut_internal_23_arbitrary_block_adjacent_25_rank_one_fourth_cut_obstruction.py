#!/usr/bin/env python3
"""Exact local obstruction for A23 arbitrary and A25 = E00 + t*E10 / E20.

For each rank-one direction c in {1, 2} the moving block

    A25 = E00 + t*Ec0 = (e0 + t*e_c) (x) e0

keeps site 5 on colour 0, so its torus weight is dependent and no chart
can normalize t.  Instead of charts, this verifier certifies, with all
nine A23 entries and t polynomial variables:

* W := C2 cap C3 is the span of the nine coordinate tensors e_ab, two
  sigma tails, and the explicit plane tensor D (constant unit 72-minor,
  exact memberships, identity restriction matrix, three M3 relations);
* H = sum x_ab e_ab + D, and H lies in every cylinder;
* probe identities force W cap C5 = <H> and W cap C0 = W cap C1 = <H, D>
  for every complex X and t;
* D lies in C4 exactly on the degenerate locus
  D_full = V(t*x00 - x_c0, t*x02 - x_c2, x_other0, x_other2)
  (six factored 43-minors of [C4|D] with radical certificates, three M4
  relations bounding rank C4 <= 42, and an explicit on-locus
  representation over the linear parameterization of D_full);
* therefore C2 cap C3 cap C4 cap C5 = <H> everywhere, and for z in
  {0, 1} the four-cylinder intersection is <H> off D_full and
  span{H, D} on D_full (a plane except at X = 0, where H = D);
* characteristic-zero shared-star unit ideals close both normal shapes:
  the line packet on all of Q[x00..x22, t] (split into x00-invertible
  and x00 = 0 cases only to bound Groebner time) and the plane packet on
  the parameterization of D_full.

No torus normalization is used and t = 0 is covered outright.  The
conclusion is local to the displayed fixed six-site interior.  It is not
a theorem for arbitrary A25 and not the global Krenn conjecture.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import itertools
import shutil
import subprocess
import time

import sympy as sp

import derive_three_cut_internal_23_adjacent_25_rank_one_w_structure as wstruct
import explore_three_cut_internal_23_adjacent_25_11 as adjacent
import explore_three_cut_internal_23_adjacent_25_rank_one_directions as rankone
import explore_three_cut_internal_23_full_supports as full
import explore_three_cut_internal_23_perturbation as equations
import test_three_cut_internal_23_adjacent_25_rank_one_star_ideals as ideals


Q = full.Q
T = rankone.T
EXPECTED_RANK_LEDGER_SHA256 = (
    "72a5c3f2af1fe08fae615009be255eb02f1217b88a2f8edf1a8c1d885b85fde0"
)
EXPECTED_IDEAL_LEDGER_SHA256 = (
    "f5e5f91e56d29c86d4e0db85eb9a70a36b5f65488b0c8feb20cf25edd0385154"
)


def audit_direction_geometry(key):
    spec = rankone.select_direction(key)
    adjacent.no_mixed_x_t_terms()
    assert len(adjacent.T_BLOCK) == 35
    assert tuple(adjacent.T_DETAILS) == ((0, 3), (0, 4), (1, 3), (3, 4))
    sample = {cell: Q(bit + 2) for bit, cell in enumerate(full.CELLS)}
    assert adjacent.blocks_for(sample, Q(0)) == full.blocks_for_coefficients(sample)
    x_rows, t_row = rankone.stabilizer_data(key)
    assert sp.Matrix.vstack(*x_rows).rank() == 5
    dependence = t_row - x_rows[spec["x_bit"]] + x_rows[0]
    assert dependence.is_zero_matrix
    return spec


def audit_literal_boundary_identity(key):
    rankone.select_direction(key)
    coefficients = {cell: Q(2001 + bit) for bit, cell in enumerate(full.CELLS)}
    internal = adjacent.blocks_for(coefficients, Q(2501))
    p = {
        (a, i, c): Q(1 + 100 * a + 10 * i + c)
        for a in full.COLOURS for i in full.SIX for c in full.COLOURS
    }
    q = {
        (b, i, c): Q(701 + 100 * b + 10 * i + c)
        for b in full.COLOURS for i in full.SIX for c in full.COLOURS
    }
    r = {
        (a, b): Q(1301 + 10 * a + b)
        for a in full.COLOURS for b in full.COLOURS
    }
    blocks = {edge: dict(block) for edge, block in internal.items()}
    for i in full.SIX:
        blocks[i, 6] = {
            (c, a): p[a, i, c] for c in full.COLOURS for a in full.COLOURS
        }
        blocks[i, 7] = {
            (c, b): q[b, i, c] for c in full.COLOURS for b in full.COLOURS
        }
    blocks[6, 7] = dict(r)
    observed_full = equations.cylinders.matching_tensor(tuple(range(8)), blocks)
    hs = equations.cylinders.matching_tensor(full.SIX, internal)
    word_terms = equations.reconstruct_word_terms(internal)
    for a, b in itertools.product(full.COLOURS, repeat=2):
        observed = {
            word[:6]: value for word, value in observed_full.items()
            if word[6:] == (a, b)
        }
        expected = {}
        for word, value in hs.items():
            equations.cylinders.add(expected, word, r[a, b] * value)
        for word, values in word_terms.items():
            total = Q(0)
            for ((i, c), (j, d)), value in values:
                total += value * (
                    p[a, i, c] * q[b, j, d] + p[a, j, d] * q[b, i, c]
                )
            equations.cylinders.add(expected, word, total)
        assert observed == expected


def rank_certificates(key):
    records = []
    determinant, nonzeros, labels, members = wstruct.w_structure(key)
    records.append((
        "w_minor", key, str(determinant), nonzeros,
        hashlib.sha256(repr(labels).encode()).hexdigest(),
    ))
    wstruct.h_tail_identity(key)
    wstruct.h_in_every_cylinder(key)
    records.append(("h_identities", key, "tail+cylinders", len(members)))
    extra5 = wstruct.verify_probe_cut5(key)
    n0 = wstruct.verify_probe_cut01(key, 0)
    n1 = wstruct.verify_probe_cut01(key, 1)
    records.append(("probes", key, extra5, n0, n1))
    wstruct.d_full_parameterization_matches(key)
    for point, det, rows, cols in wstruct.c4_minor_determinants(key):
        records.append((
            "c4_minor", key, point, det,
            hashlib.sha256(repr((rows, cols)).encode()).hexdigest(),
        ))
    coefficients = wstruct.d_in_c4_on_locus(key)
    records.append((
        "d_in_c4_on_locus", key,
        tuple((index, str(value)) for index, value in sorted(
            coefficients.items()
        )),
    ))
    return records


def marker(output, name):
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    return int(lines[lines.index(name) + 1])


def run_program(program, timeout):
    singular = shutil.which("Singular")
    if singular is None:
        raise SystemExit("Singular is required")
    started = time.monotonic()
    completed = subprocess.run(
        [singular, "-q"], input=program, text=True, capture_output=True,
        check=True, timeout=timeout,
    )
    if completed.stderr.strip():
        raise AssertionError(completed.stderr)
    unit = marker(completed.stdout, "UNIT")
    size = marker(completed.stdout, "GBSIZE")
    assert (unit, size) == (1, 1), (unit, size)
    return time.monotonic() - started


def build_all_singular_jobs():
    jobs = []
    for key in ("10", "20"):
        for generator, program in wstruct.radical_programs(key):
            jobs.append({
                "name": f"radical_{key}_{generator}",
                "coverage": "V(c4_minors) inside D_full",
                "program": program,
                "sha256": hashlib.sha256(program.encode()).hexdigest(),
            })
    for job in ideals.all_jobs(split=True):
        jobs.append({
            "name": job["name"],
            "coverage": "star packet",
            "program": job["program"],
            "sha256": job["sha256"],
        })
    return jobs


def ledger_hash(rows):
    return hashlib.sha256("\n".join(map(repr, rows)).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry-only", action="store_true")
    parser.add_argument("--skip-singular", action="store_true")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=14400)
    args = parser.parse_args()

    started_all = time.monotonic()
    rank_records = []
    for key in ("10", "20"):
        audit_direction_geometry(key)
        audit_literal_boundary_identity(key)
        print(f"GEOMETRY direction={key} pass=1", flush=True)
    if args.geometry_only:
        return

    for key in ("10", "20"):
        rank_records.extend(rank_certificates(key))
        print(f"CERTIFICATES direction={key} pass=1", flush=True)
    rank_digest = ledger_hash(rank_records)
    for record in rank_records:
        print("RANK", repr(record), flush=True)
    print("RANK_LEDGER_SHA256", rank_digest, flush=True)
    if EXPECTED_RANK_LEDGER_SHA256:
        assert rank_digest == EXPECTED_RANK_LEDGER_SHA256, rank_digest

    jobs = build_all_singular_jobs()
    ideal_digest = ledger_hash([
        (job["name"], job["coverage"], job["sha256"]) for job in jobs
    ])
    for job in jobs:
        print(
            "IDEAL", job["name"], job["coverage"],
            f'sha256={job["sha256"]}', flush=True,
        )
    print("IDEAL_LEDGER_SHA256", ideal_digest, flush=True)
    if EXPECTED_IDEAL_LEDGER_SHA256:
        assert ideal_digest == EXPECTED_IDEAL_LEDGER_SHA256, ideal_digest
    if args.skip_singular:
        return

    started_exact = time.monotonic()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        elapsed = list(executor.map(
            lambda job: run_program(job["program"], args.timeout), jobs,
        ))
    exact_wall = time.monotonic() - started_exact
    print("A23 arbitrary plus A25=E00+tE10 and E00+tE20 local fourth-cut obstruction: PASS")
    print("uniform in all complex X and t, including t=0, with no torus charts: PASS")
    print("W=C2^C3 basis, probe identities, D-in-C4 characterization: PASS")
    print(f"{len(jobs)} characteristic-zero Singular jobs, all unit: PASS")
    print("endpoint order, shared stars, ordered fibres, arbitrary A67: PASS")
    print(f"rank ledger SHA256: {rank_digest}")
    print(f"ideal ledger SHA256: {ideal_digest}")
    print(f"maximum Singular time: {max(elapsed):.3f}s")
    print(f"parallel Singular wall time: {exact_wall:.3f}s")
    print(f"total wall time: {time.monotonic()-started_all:.3f}s")


if __name__ == "__main__":
    main()

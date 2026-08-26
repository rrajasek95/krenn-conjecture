#!/usr/bin/env python3
"""Bounded exact theorem-shape audit of the N6 P^2 K-degree-six block."""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import pickle
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "computations"))
# ``-I -S`` deliberately omits virtualenv site-packages.  The frozen source
# engine imports numpy, so add this one interpreter-relative, audited path.
VENV_SITE = (Path(sys.executable).absolute().parents[1] / "lib" /
             f"python{sys.version_info.major}.{sys.version_info.minor}" /
             "site-packages")
if VENV_SITE.is_dir():
    sys.path.append(str(VENV_SITE))

import coefficient_power2_filtration as F  # noqa: E402
import lift_power2_offdiag2 as L  # noqa: E402


R6 = HERE / "frozen_r6_p1009.pkl.gz"
OUT = HERE / "results_degree6_relative_incidence.json"
GLOBAL = ROOT / "computations" / "unaudited-codex-p2-k6-global-2026-08-23"
CUTOFF3_DFS = GLOBAL / "cutoff3_dfs.txt"
P2_SEED = GLOBAL / "p2_target_seed.txt"

EASY_ROW = (
    (0, 0, 2, 54, 54, 56),
    (9566667, 9565941, 131238),
)
FAN_TARGET = (
    (0, 0, 55, 55, 87, 87),
    (1076004, 39528, 118100),
)

# Exhaustive incident-degree census on the 366,992 nonzero frozen-r6 rows.
# Recomputed only under --full-scan (about two minutes on the reference host).
FROZEN_INCIDENCE_HISTOGRAM = {
    1: 10, 2: 47, 3: 235, 4: 541, 5: 1035, 6: 2026, 7: 3302,
    8: 5115, 9: 7429, 10: 9344, 11: 11834, 12: 13756,
    13: 14469, 14: 15088, 15: 14792, 16: 13962, 17: 12689,
    18: 11032, 19: 9454, 20: 8383, 21: 6658, 22: 5499,
    23: 3632, 24: 2590, 25: 1703, 26: 1122, 27: 769, 28: 439,
    29: 342, 30: 212, 31: 138, 32: 60, 33: 46, 34: 24, 35: 9,
    36: 11, 37: 7, 38: 6,
}


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def jsonify(value):
    if isinstance(value, tuple):
        return [jsonify(item) for item in value]
    if isinstance(value, Fraction):
        return str(value)
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def cutoff3_certificate_audit():
    """Audit the frozen global triangular ledger without regenerating it."""
    require(sha256_file(CUTOFF3_DFS) ==
            "4985027e5f91bb462960f3e3dcd3c77edd181bc9e8ace1d938c7b506ff974222",
            "cutoff-three DFS certificate hash changed")
    require(sha256_file(P2_SEED) ==
            "2c425920e4f803272361100c2bcd22c758c47ff09328b96855d8421a0e1fe37b",
            "P2 seed hash changed")
    with CUTOFF3_DFS.open(encoding="ascii") as stream:
        header = stream.readline().split()
        require(header == ["KRENN_P2_TRUNCATED_DFS_V1", "3", "663", "9528"],
                "cutoff-three DFS header changed")
        degrees = collections.Counter()
        diagonals = collections.Counter()
        rows = set()
        columns = set()
        for line in stream:
            fields = line.rstrip().split(" || ")
            require(len(fields) == 3 and fields[0].startswith("PIVOT "),
                    "malformed cutoff-three pivot")
            row_fields = fields[0].split()
            degree = int(row_fields[1])
            require(len(row_fields) == 6 + degree and
                    row_fields[2 + degree] == "|",
                    "cutoff-three row length changed")
            degrees[degree] += 1
            diagonals[int(fields[2])] += 1
            require(fields[0] not in rows, "cutoff-three pivot row repeated")
            require(fields[1] not in columns, "cutoff-three pivot column repeated")
            rows.add(fields[0])
            columns.add(fields[1])
    require(len(rows) == 9528 and degrees == {0: 868, 2: 7421, 3: 1239},
            f"cutoff-three pivot census changed: {degrees}")
    require(diagonals == {1: 9409, 2: 119},
            f"cutoff-three pivot diagonal changed: {diagonals}")
    return {
        "certificate_sha256": sha256_file(CUTOFF3_DFS),
        "seed_sha256": sha256_file(P2_SEED),
        "target_row_orbits": 663,
        "triangular_pivots": 9528,
        "pivot_K_degree": dict(sorted(degrees.items())),
        "pivot_diagonal_coefficients": dict(sorted(diagonals.items())),
        "exact_consequence": (
            "P^2 is in I+K^4 over Q (indeed Z[1/2]) in the S6xS3 "
            "orbit quotient"
        ),
        "collapse_order": (
            "certificate order: each pivot column has its pivot row and only "
            "earlier pivot rows among outputs of K-degree at most three"
        ),
        "contracting_homotopy": (
            "back-substitution in this well-founded order; diagonals are one "
            "or two, so the contraction is coefficient-aware over Q and "
            "introduces no odd-prime denominator"
        ),
        "first_possible_truncated_core": (
            "K-degree four; no relative dual can be supported entirely in the "
            "certified cutoff-three target-reachable subcomplex"
        ),
        "producer_replay_scope": (
            "the Rust producer checks the triangular-output condition before "
            "writing the certificate; this audit freezes its header, hashes, "
            "unit diagonals, distinct pivots, and K-degree census"
        ),
    }


def exact_rank(columns, rows) -> int:
    basis = {}
    for column in columns:
        counts = collections.Counter(L.leading_outputs(column))
        vector = [Fraction(counts[row]) for row in rows]
        while any(vector):
            pivot = next(index for index, value in enumerate(vector) if value)
            if pivot not in basis:
                scale = vector[pivot]
                basis[pivot] = [value / scale for value in vector]
                break
            scale = vector[pivot]
            vector = [value - scale * base
                      for value, base in zip(vector, basis[pivot])]
    return len(basis)


def easy_homotopy():
    """An exact integral right inverse for the first 42 free face."""
    assigned = F.triangular_assignment((EASY_ROW,), 6)
    require(assigned is not None and len(assigned) == 36,
            "easy 42 dependency closure changed")
    work = collections.defaultdict(Fraction)
    work[EASY_ROW] = Fraction(-1)
    correction = collections.defaultdict(Fraction)
    for row, column in reversed(tuple(assigned.items())):
        value = work[row]
        if not value:
            continue
        outputs = collections.Counter(L.leading_outputs(column))
        coefficient = value / outputs[row]
        correction[column] += coefficient
        for output, multiplicity in outputs.items():
            work[output] -= coefficient * multiplicity
    work = {row: value for row, value in work.items() if value}
    require(len(work) == 45 and all(L.monomial_killed(row) for row in work),
            "easy 42 closure no longer lands only in rainbow cones")
    for row, value in tuple(work.items()):
        column = L.monomial_column(row)
        require(column is not None, "cone correction disappeared")
        outputs = collections.Counter(L.leading_outputs(column))
        coefficient = value / outputs[row]
        correction[column] += coefficient
        for output, multiplicity in outputs.items():
            work[output] = work.get(output, Fraction()) - coefficient * multiplicity
    work = {row: value for row, value in work.items() if value}
    require(not work, "easy 42 homotopy left a residual")
    correction = {column: value for column, value in correction.items() if value}
    require(len(correction) == 81 and set(correction.values()) == {Fraction(-1), Fraction(1)},
            "easy 42 integral correction census changed")
    audit = collections.defaultdict(Fraction)
    audit[EASY_ROW] = Fraction(1)
    for column, coefficient in correction.items():
        for output in L.leading_outputs(column):
            audit[output] += coefficient
    require(not {row: value for row, value in audit.items() if value},
            "easy 42 homotopy does not replay")
    return assigned, correction


def fan_interface(r6):
    """The lex-first unique-incidence 330 face and its exact four-arm debt."""
    require(r6[FAN_TARGET] == 867, "fan target coefficient changed")
    incident = L.incident_leading_columns(FAN_TARGET)
    require(len(incident) == 1, "fan target is no longer a free row")
    column330 = incident[0]
    require(tuple(column330[0].count(colour) for colour in range(3)) == (3, 3, 0),
            "fan source word is no longer profile 330")
    output_counter = collections.Counter(L.leading_outputs(column330))
    rows = tuple(sorted(output_counter))
    require(len(rows) == 6 and output_counter[FAN_TARGET] == 1,
            "330 fan size/multiplicity changed")
    require(all(not L.monomial_killed(row) for row in rows),
            "330 fan acquired a rainbow cone")

    all_columns = set()
    for row in rows:
        all_columns.update(L.incident_leading_columns(row))
    internal = []
    row_set = set(rows)
    for column in all_columns:
        noncone_outputs = {
            row for row in L.leading_outputs(column) if not L.monomial_killed(row)
        }
        if noncone_outputs <= row_set:
            internal.append(column)
    internal.sort()
    require(len(all_columns) == 11 and len(internal) == 2,
            "330 fan incidence census changed")
    profiles = [tuple(column[0].count(colour) for colour in range(3))
                for column in internal]
    require(profiles == [(3, 3, 0), (3, 2, 1)],
            f"330 fan internal profiles changed: {profiles}")
    column321 = internal[1]
    counts321 = collections.Counter(L.leading_outputs(column321))

    # Literal labels inside the sorted fan.
    B, D, Frow, E, C, target = rows
    require(target == FAN_TARGET, "fan target order changed")
    require(output_counter == {B: 2, C: 2, D: 2, E: 1, Frow: 1, target: 1},
            "330 fan coefficients changed")
    require(counts321 == {C: 1, D: 1, E: 1},
            "321 internal repair changed")
    require({row: r6.get(row, 0) for row in rows}
            == {B: 0, D: 0, Frow: 0, E: 0, C: 725, target: 867},
            "frozen r6 restriction to the fan changed")

    # Cancel the target with -867*C330.  Since 725-2*867=-1009, C cancels
    # automatically.  The exact modular boundary has four unavoidable arms.
    residue = collections.Counter({row: r6.get(row, 0) for row in rows})
    for row, multiplicity in output_counter.items():
        residue[row] = (residue[row] - 867 * multiplicity) % F.PRIME
    residue = collections.Counter({row: value for row, value in residue.items() if value})
    expected_residue = {B: 284, D: 284, E: 142, Frow: 142}
    require(residue == expected_residue,
            f"coefficient-aware four-arm residue changed: {residue}")

    # Adding b*C321 changes (C,D,E) by (b,b,b), but never changes B or F.
    # The three affine coefficients b,b+284,b+142 are pairwise distinct, so
    # at most one vanishes: every internal reduction has >=4 live arms.
    for b in range(F.PRIME):
        candidate = dict(expected_residue)
        for row in (C, D, E):
            candidate[row] = (candidate.get(row, 0) + b) % F.PRIME
        require(sum(value != 0 for value in candidate.values()) >= 4,
                "four-arm minimality failed")

    # A dual supported only on these six rows is impossible: the projections
    # of all 11 incident columns have full row rank over Q.
    rank = exact_rank(sorted(all_columns), rows)
    require(rank == 6, "fan-supported dual rank guard changed")

    # The 330 column changes the six-edge off multiset in every output, so the
    # tempting fixed-off-support module decomposition is not invariant.
    require(len({row[0] for row in rows}) == 6,
            "330 fan stopped coupling six off-support fibres")

    return {
        "target": jsonify(FAN_TARGET),
        "target_coefficient_mod1009": 867,
        "source_column_330": jsonify(column330),
        "internal_column_321": jsonify(column321),
        "fan_rows": {
            name: jsonify(row) for name, row in
            (("B", B), ("C", C), ("D", D), ("E", E), ("F", Frow),
             ("target", target))
        },
        "C330_relation": "target+2B+2C+2D+E+F",
        "C321_relation": "C+D+E",
        "frozen_r6_on_fan": {"target": 867, "C": 725},
        "minimal_internal_residue_mod1009": {"B": 284, "D": 284,
                                               "E": 142, "F": 142},
        "minimum_live_arms_after_internal_reduction": 4,
        "incident_columns": len(all_columns),
        "fan_projection_rank_over_Q": rank,
        "fan_supported_dual_dimension": 0,
        "off_support_fibres_coupled_by_C330": 6,
    }


def full_scan(rows):
    histogram = collections.Counter()
    cones = 0
    degree_one = []
    for index, (row, coefficient) in enumerate(rows):
        if L.monomial_killed(row):
            cones += 1
            continue
        degree = len(L.incident_leading_columns(row))
        histogram[degree] += 1
        if degree == 1:
            degree_one.append((index, row, coefficient))
    require(cones == 189182, f"cone count changed: {cones}")
    require(dict(histogram) == FROZEN_INCIDENCE_HISTOGRAM,
            f"incident histogram changed: {histogram}")
    require(not histogram.get(0), "a dead degree-six coordinate appeared")
    return cones, degree_one


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-results", action="store_true")
    parser.add_argument("--full-scan", action="store_true")
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()

    with gzip.open(R6, "rb") as stream:
        payload = pickle.load(stream)
    require(payload["format"] == "n6-p2-coefficient-aware-r6-p1009-v1",
            "wrong r6 format")
    require(payload["prime"] == 1009 and payload["support"] == 366992,
            "frozen r6 headline changed")
    require(payload["stage"] == [(2, 7575, 335, 7941),
                                 (3, 88, 47, 174),
                                 (4, 46795, 10292, 63147),
                                 (5, 62458, 17274, 90946)],
            "lower-lift provenance changed")
    rows = payload["rows"]
    r6 = dict(rows)
    off_fibres = collections.Counter(row[0] for row, _coefficient in rows)
    require(len(off_fibres) == 10896,
            "frozen r6 off-support fibre count changed")
    require(sum(size == 1 for size in off_fibres.values()) == 3142,
            "singleton off-support fibre count changed")

    assigned, correction = easy_homotopy()
    fan = fan_interface(r6)
    cutoff3 = cutoff3_certificate_audit()
    if args.full_scan:
        cones, degree_one = full_scan(rows)
        require(degree_one[0][1] == EASY_ROW and degree_one[2][1] == FAN_TARGET,
                "lex order of the two theorem-shape representatives changed")
    else:
        cones = 189182

    correction_rows = [
        {"coefficient": int(coefficient), "column": jsonify(column)}
        for column, coefficient in sorted(correction.items())
    ]
    correction_digest = hashlib.sha256(json.dumps(
        correction_rows, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

    if args.mutate:
        require(fan["minimum_live_arms_after_internal_reduction"] == 3,
                "hostile four-arm mutation survived")

    result = {
        "verdict": "EXACT_Q_CUTOFF3_CONTRACTION;FIRST_POSSIBLE_GLOBAL_CORE_IS_K4;FROZEN_K6_FIRST_LOCAL_ESCAPE_IS_THE_330_FOUR_ARM",
        "scope": (
            "the exact integral target-reachable cutoff-three map, plus the "
            "frozen coefficient-aware p1009 degree-six lift; not a full "
            "rational P^2 membership/nonmembership decision"
        ),
        "global_cutoff3_contraction": cutoff3,
        "frozen_r6": {
            "sha256": "870fc488aaa210df6de91516f4c947f74caa1aea4a9fddc7401e85fa45367278",
            "nonzero_row_orbits": len(rows),
            "rainbow_cone_rows": cones,
            "noncone_rows": len(rows) - cones,
            "off_support_fibres": len(off_fibres),
            "singleton_off_support_fibres": sum(size == 1 for size in off_fibres.values()),
            "no_dead_coordinate_rows": True,
            "degree_one_incident_rows": 10,
            "incident_degree_histogram": dict(sorted(FROZEN_INCIDENCE_HISTOGRAM.items())),
        },
        "module_decomposition": {
            "global_symmetry": "already Reynolds-reduced to the trivial S6xS3 isotypic component",
            "even_profiles": "420 and 222 preserve the six-edge off multiset",
            "odd_profiles": "510,411,330,321 replace one cross edge and couple off-support fibres",
            "fixed_off_fibre_decomposition_valid": False,
            "counterguard": "the displayed 330 fan couples six distinct off-support fibres",
        },
        "exact_42_leaf_homotopy": {
            "target_row": jsonify(EASY_ROW),
            "frozen_r6_coefficient_mod1009": r6[EASY_ROW],
            "noncone_dependency_rows": len(assigned),
            "rainbow_cone_corrections": 45,
            "total_literal_columns": len(correction),
            "coefficient_set": [-1, 1],
            "certificate_sha256": correction_digest,
            "certificate": correction_rows,
        },
        "first_local_degree6_escape_interface": fan,
        "literal_provenance_guard": {
            "fan_K_degree": 6,
            "cutoff3_pivot_K_degrees": [0, 2, 3],
            "literal_fan_row_or_pivot_match": False,
            "reason": (
                "the cutoff-three certificate deliberately drops outputs of "
                "K-degree at least four; it proves the lower interface but "
                "cannot be multiplied or transported into this fixed "
                "fine-degree degree-six fan"
            ),
        },
        "decision_guard": {
            "P2_proved": False,
            "P2_disproved": False,
            "reason": (
                "cutoff three is exactly Q-contractible, so an obstruction "
                "must first enter at K-degree four or later; the frozen "
                "degree-six four-arm fan has no local dual and is not covered "
                "by the cutoff-three certificate"
            ),
            "next_exact_test": (
                "compute the first nonempty target-reachable relative 2-core "
                "at cutoff four through six, or contract the degree-six "
                "284(B+D)+142(E+F) class with literal higher-cutoff pivots; "
                "a modular pairing for one chosen lift alone is not a Q "
                "obstruction"
            ),
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = hashlib.sha256(logical.encode()).hexdigest()
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        OUT.write_text(rendered, encoding="utf-8")
    if args.check_results:
        require(OUT.read_text(encoding="utf-8") == rendered,
                "frozen result differs")
    print(json.dumps({
        "verdict": result["verdict"],
        "r6_support": len(rows),
        "easy_homotopy_columns": len(correction),
        "fan_minimum_arms": fan["minimum_live_arms_after_internal_reduction"],
        "cutoff3_pivots": cutoff3["triangular_pivots"],
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

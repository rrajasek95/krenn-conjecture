#!/usr/bin/env python3
"""Exact audit of the symmetry-compressed N=8 response-carrier residual.

This script deliberately rebuilds endpoint-ordered response rows and raw
hafnians.  It does not import the response-star implementation.  Its main
checks are:

* the four-way carrier blocker disjunction is exactly one quartic
  ideal-membership test;
* every carrier row space is a sum of 15 atomic response-edge row spaces;
* all 219 X4 slice identities per pair hold on W40 and expose W25 as outside
  X4;
* W40 and W25 reproduce the required positive/negative carrier controls.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import sys


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SITES = tuple(range(8))
COLORS = tuple(range(3))
EDGES = tuple(combinations(SITES, 2))
W40_PATH = ROOT / "computations/unaudited-x4general-w40-2026-08-20/results_t3.json"
W25_PATH = (ROOT / "computations/unaudited-x3core-w25-2026-08-15"
            / "OBJECT_W25-F8_n8_allblocked_X3.json")
PINNED = {
    W40_PATH: "30ad242d62b5cb905858842ce4e8255b105862dc21a65c73c080557fa8c1617f",
    W25_PATH: "46d6e207e392deaa7e0bfc4221c7f5cc6735f11a2a14cc388292ca6850dd33f6",
}

DECLARED_CONTROLS = {
    "pinned_inputs",
    "raw_x4_boundary",
    "atomic_carrier_reconstruction",
    "quartic_disjunction_equivalence",
    "slice_identity_x4_consumption",
    "endpoint_order_mutation",
    "activity_factor_mutation",
    "site_color_covariance",
    "diagonal_outside_x4",
    "twisted_binary_boundary",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    out = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in matchings(rest):
            out.append(((first, second),) + tail)
    return tuple(out)


def parse_source(blocks):
    source = {}
    for key, matrix in blocks.items():
        u, v = [int(piece.strip()) for piece in key.strip().strip("()").split(",")]
        require(u < v, key)
        source[(u, v)] = tuple(
            tuple(Fraction(str(value)) for value in row) for row in matrix
        )
    require(set(source) == set(EDGES), "source edge set")
    return source


def zero_source():
    return {edge: tuple(tuple(Fraction(0) for _ in COLORS) for _ in COLORS)
            for edge in EDGES}


def mutable_copy(source):
    return {edge: [list(row) for row in matrix] for edge, matrix in source.items()}


def freeze(source):
    return {edge: tuple(tuple(row) for row in matrix) for edge, matrix in source.items()}


def load_controls():
    for path, expected in PINNED.items():
        require(digest(path) == expected, (path, "digest changed"))
    w40_data = json.loads(W40_PATH.read_text())
    w25_data = json.loads(W25_PATH.read_text())
    return (
        parse_source(w40_data["engine_audit"]["witness_B_integral"]["source"]),
        parse_source(w25_data["blocks"]),
    )


def cell(source, u, v, a, b):
    if u < v:
        return source[(u, v)][a][b]
    return source[(v, u)][b][a]


def haf(source, word, vertices):
    total = Fraction(0)
    for matching in matchings(tuple(vertices)):
        term = Fraction(1)
        for u, v in matching:
            term *= cell(source, u, v, word[u], word[v])
            if not term:
                break
        total += term
    return total


def off_count(word):
    return 8 - max(word.count(c) for c in COLORS)


def raw_profile(source):
    failures = Counter()
    pures = []
    for word in product(COLORS, repeat=8):
        value = haf(source, word, SITES)
        target = Fraction(1) if len(set(word)) == 1 else Fraction(0)
        if value != target:
            failures[off_count(word)] += 1
        if len(set(word)) == 1:
            pures.append(value)
    return pures, failures


def response_edge(source, p, q, a, b, *, mutant=False):
    """The nine rows of K -> R_ab(K), in residual-cell order."""
    rows = []
    for alpha in COLORS:
        for beta in COLORS:
            row = []
            for i in COLORS:
                for j in COLORS:
                    first = cell(source, p, a, i, alpha) * cell(
                        source, q, b, j, beta)
                    if mutant:
                        second = cell(source, p, b, i, alpha) * cell(
                            source, q, a, j, beta)
                    else:
                        second = cell(source, p, b, i, beta) * cell(
                            source, q, a, j, alpha)
                    row.append(first + second)
            rows.append(row)
    return rows


def activity(source, p, q):
    rows = []
    for c in COLORS:
        row = [Fraction(0)] * 9
        row[3 * c + c] = Fraction(1)
        rows.append(row)
    rows.append([cell(source, p, q, i, j) for i in COLORS for j in COLORS])
    return rows


def rref(rows, ncols=9):
    work = [list(map(Fraction, row)) for row in rows if any(row)]
    pivots = []
    lead = 0
    row_index = 0
    while row_index < len(work) and lead < ncols:
        pivot = next((r for r in range(row_index, len(work)) if work[r][lead]), None)
        if pivot is None:
            lead += 1
            continue
        work[row_index], work[pivot] = work[pivot], work[row_index]
        scale = work[row_index][lead]
        work[row_index] = [value / scale for value in work[row_index]]
        for other in range(len(work)):
            if other == row_index or not work[other][lead]:
                continue
            scale = work[other][lead]
            work[other] = [x - scale * y for x, y in zip(work[other], work[row_index])]
        pivots.append(lead)
        row_index += 1
        lead += 1
    return tuple(tuple(row) for row in work[:row_index]), tuple(pivots)


def nullspace(rows):
    reduced, pivots = rref(rows)
    free = [column for column in range(9) if column not in pivots]
    basis = []
    for column in free:
        vector = [Fraction(0)] * 9
        vector[column] = Fraction(1)
        for row, pivot in zip(reduced, pivots):
            vector[pivot] = -row[column]
        basis.append(tuple(vector))
    return tuple(basis)


def dot(left, right):
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def restrict_linear(functional, basis):
    return tuple(dot(functional, vector) for vector in basis)


def multiply_linear_forms(forms):
    """Coefficient dictionary for a product of linear forms."""
    if not forms or not forms[0]:
        return {}
    poly = {(0,) * len(forms[0]): Fraction(1)}
    for form in forms:
        nxt = {}
        for exponent, coefficient in poly.items():
            for variable, value in enumerate(form):
                if not value:
                    continue
                new_exp = list(exponent)
                new_exp[variable] += 1
                new_exp = tuple(new_exp)
                nxt[new_exp] = nxt.get(new_exp, Fraction(0)) + coefficient * value
                if not nxt[new_exp]:
                    del nxt[new_exp]
        poly = nxt
    return poly


def carrier_data(source, p, q, carrier_type, carrier, atomic=None):
    residual = tuple(v for v in SITES if v not in (p, q))
    edges = tuple(combinations(residual, 2))
    if atomic is None:
        atomic = {edge: response_edge(source, p, q, *edge) for edge in edges}
    if carrier_type == "star":
        allowed = {edge for edge in edges if carrier in edge}
    elif carrier_type == "triangle":
        triangle = set(carrier)
        allowed = {edge for edge in edges if set(edge).issubset(triangle)}
    else:
        raise ValueError(carrier_type)
    forbidden = tuple(edge for edge in edges if edge not in allowed)
    rows = [row for edge in forbidden for row in atomic[edge]]
    reduced, _ = rref(rows)
    basis = nullspace(reduced)
    acts = activity(source, p, q)
    restrictions = [restrict_linear(functional, basis) for functional in acts]
    memberships = tuple(not any(values) for values in restrictions)
    quartic = multiply_linear_forms(restrictions)
    passes = not any(memberships)
    # F[V] is a domain: the restricted product is zero iff a factor is zero.
    require(bool(quartic) == passes,
            (p, q, carrier_type, carrier, memberships, quartic))
    return {
        "rank": len(reduced),
        "kernel_dimension": len(basis),
        "memberships": memberships,
        "quartic_nonzero": bool(quartic),
        "quartic_terms": len(quartic),
        "passes": passes,
        "rowspace": reduced,
    }


def all_carriers(source):
    records = []
    atomic_checks = 0
    for p, q in EDGES:
        residual = tuple(v for v in SITES if v not in (p, q))
        atomic = {edge: response_edge(source, p, q, *edge)
                  for edge in combinations(residual, 2)}
        for centre in residual:
            record = carrier_data(source, p, q, "star", centre, atomic)
            records.append(("star", (p, q), (centre,), record))
            # Reconstruct independently, rather than merely slicing atomic.
            direct = []
            for a, b in combinations(residual, 2):
                if centre not in (a, b):
                    direct.extend(response_edge(source, p, q, a, b))
            require(rref(direct)[0] == record["rowspace"],
                    (p, q, centre, "atomic star mismatch"))
            atomic_checks += 1
        for triangle in combinations(residual, 3):
            record = carrier_data(source, p, q, "triangle", triangle, atomic)
            records.append(("triangle", (p, q), triangle, record))
            direct = []
            allowed = set(combinations(triangle, 2))
            for edge in combinations(residual, 2):
                if edge not in allowed:
                    direct.extend(response_edge(source, p, q, *edge))
            require(rref(direct)[0] == record["rowspace"],
                    (p, q, triangle, "atomic triangle mismatch"))
            atomic_checks += 1
    require(len(records) == 728, len(records))
    return records, atomic_checks


def carrier_summary(records):
    answer = {}
    for kind in ("star", "triangle"):
        chosen = [record for record in records if record[0] == kind]
        passed = [record for record in chosen if record[3]["passes"]]
        answer[kind] = {
            "choices": len(chosen),
            "passing": len(passed),
            "pass_labels": [
                {"pair": list(pair), "carrier": list(carrier),
                 "rank": data["rank"]}
                for _, pair, carrier, data in passed
            ],
            "rank_histogram": dict(sorted(Counter(
                data["rank"] for _, _, _, data in chosen).items())),
            "kernel_dimension_histogram": dict(sorted(Counter(
                data["kernel_dimension"] for _, _, _, data in chosen).items())),
            "blocker_pattern_histogram": {
                "".join("1" if bit else "0" for bit in pattern): count
                for pattern, count in sorted(Counter(
                    data["memberships"] for _, _, _, data in chosen).items())
            },
        }
    return answer


def write_compressed_ledger(path, named_records):
    with path.open("w") as handle:
        for source_name, records in named_records.items():
            for kind, pair, carrier, data in records:
                rowspace_payload = [[str(value) for value in row]
                                    for row in data["rowspace"]]
                record = {
                    "source": source_name,
                    "carrier_type": kind,
                    "pair": list(pair),
                    "carrier": list(carrier),
                    "rank": data["rank"],
                    "kernel_dimension": data["kernel_dimension"],
                    "activity_in_rowspace": list(data["memberships"]),
                    "quartic_nonzero_on_kernel": data["quartic_nonzero"],
                    "quartic_term_count": data["quartic_terms"],
                    "canonical_rowspace": rowspace_payload,
                    "canonical_rowspace_sha256": sha256(
                        json.dumps(rowspace_payload, separators=(",", ":")).encode()
                    ).hexdigest(),
                }
                handle.write(json.dumps(record, sort_keys=True) + "\n")


def residual_words(p, q):
    residual = tuple(v for v in SITES if v not in (p, q))
    for values in product(COLORS, repeat=6):
        if max(values.count(c) for c in COLORS) < 4:
            continue
        word = [None] * 8
        for site, value in zip(residual, values):
            word[site] = value
        yield residual, tuple(word)


def slice_identity_defects(source):
    """Check the 219 endpoint-expansion identities per cap pair.

    For residual z with a color appearing at least four times, all nine
    extensions (i,j,z) are X4 rows.  Contracting them against K gives

      delta_z = H6(z) ell_3 + sum_ab H4(z without a,b) rho_ab(z_a,z_b).
    """
    defects = []
    checked = 0
    for p, q in EDGES:
        residual = tuple(v for v in SITES if v not in (p, q))
        atomic = {edge: response_edge(source, p, q, *edge)
                  for edge in combinations(residual, 2)}
        ell3 = activity(source, p, q)[3]
        for _, partial in residual_words(p, q):
            checked += 1
            residual_values = [partial[v] for v in residual]
            target = [Fraction(0)] * 9
            if len(set(residual_values)) == 1:
                c = residual_values[0]
                target[3 * c + c] = Fraction(1)
            h6 = haf(source, partial, residual)
            rhs = [h6 * value for value in ell3]
            for edge in combinations(residual, 2):
                a, b = edge
                rest = tuple(v for v in residual if v not in edge)
                h4 = haf(source, partial, rest)
                row = atomic[edge][3 * partial[a] + partial[b]]
                rhs = [x + h4 * y for x, y in zip(rhs, row)]
            defect = tuple(x - y for x, y in zip(target, rhs))
            if any(defect):
                defects.append({
                    "pair": [p, q],
                    "residual_word": "".join(str(partial[v]) for v in residual),
                    "defect": [str(value) for value in defect],
                })
    require(checked == 28 * 219, checked)
    return checked, defects


def relabel_source(source, site_perm, color_perm):
    mutable = mutable_copy(zero_source())
    for u, v in EDGES:
        for a, b in product(COLORS, repeat=2):
            nu, nv = site_perm[u], site_perm[v]
            na, nb = color_perm[a], color_perm[b]
            if nu < nv:
                mutable[(nu, nv)][na][nb] = cell(source, u, v, a, b)
            else:
                mutable[(nv, nu)][nb][na] = cell(source, u, v, a, b)
    return freeze(mutable)


def mapped_label(pair, carrier, site_perm):
    p, q = pair
    np, nq = site_perm[p], site_perm[q]
    if np > nq:
        np, nq = nq, np
    return (np, nq), tuple(sorted(site_perm[v] for v in carrier))


def records_by_label(records):
    return {(kind, pair, tuple(carrier)): data
            for kind, pair, carrier, data in records}


def covariance_check(source, records):
    """Check generators of site/color relabeling on a spanning carrier sample."""
    original = records_by_label(records)
    transforms = [
        ((1, 0, 2, 3, 4, 5, 6, 7), (0, 1, 2)),
        ((1, 2, 3, 4, 5, 6, 7, 0), (0, 1, 2)),
        ((0, 1, 2, 3, 4, 5, 6, 7), (1, 0, 2)),
        ((0, 1, 2, 3, 4, 5, 6, 7), (1, 2, 0)),
    ]
    # A deterministic sample meeting both carrier orbits and all source pairs.
    sample = []
    for record in records:
        kind, pair, carrier, _ = record
        if kind == "star" and carrier[0] == next(v for v in SITES if v not in pair):
            sample.append(record)
        elif kind == "triangle":
            residual = tuple(v for v in SITES if v not in pair)
            if tuple(carrier) == tuple(residual[:3]):
                sample.append(record)
    require(len(sample) == 56, len(sample))
    checked = 0
    for site_perm, color_perm in transforms:
        transformed = relabel_source(source, site_perm, color_perm)
        for kind, pair, carrier, data in sample:
            new_pair, new_carrier = mapped_label(pair, carrier, site_perm)
            atomic = None
            transformed_data = carrier_data(
                transformed, *new_pair, kind,
                new_carrier[0] if kind == "star" else new_carrier,
                atomic,
            )
            require(transformed_data["rank"] == data["rank"],
                    (kind, pair, carrier, "rank covariance"))
            require(transformed_data["passes"] == data["passes"],
                    (kind, pair, carrier, "pass covariance"))
            require(sorted(transformed_data["memberships"][:3])
                    == sorted(data["memberships"][:3]),
                    (kind, pair, carrier, "color blocker covariance"))
            require(transformed_data["memberships"][3] == data["memberships"][3],
                    (kind, pair, carrier, "scalar blocker covariance"))
            checked += 1
    return checked


def diagonal_boundary():
    """Pure-normalized diagonal common-matching point, intentionally not X4."""
    mutable = mutable_copy(zero_source())
    for u, v in ((0, 1), (2, 3), (4, 5), (6, 7)):
        for c in COLORS:
            mutable[(u, v)][c][c] = Fraction(1)
    return freeze(mutable)


def twisted_binary_boundary():
    """Fixed W33-D5 binary representative, with the color-2 face set to zero."""
    mutable = mutable_copy(zero_source())
    entries = {
        (0, 1, 0, 0): 1, (2, 3, 0, 0): 1,
        (4, 5, 0, 0): 1, (6, 7, 0, 0): 1,
        (0, 3, 1, 1): 1, (1, 2, 1, 1): 1,
        (4, 7, 1, 1): 1, (5, 6, 1, 1): 1,
        (0, 4, 0, 1): 1, (0, 5, 1, 0): 1,
        (1, 7, 0, 1): -1, (3, 4, 1, 0): -1,
    }
    for u, v, a, b in entries:
        mutable[(u, v)][a][b] = Fraction(entries[(u, v, a, b)])
    return freeze(mutable)


def dimension_table():
    # dim Sym^d(F^n) = C(n+d-1,d).  The degree-four part of the ideal of
    # an r-plane W in C* has codimension Sym^4(C*/W).
    out = []
    for rank in range(10):
        kernel = 9 - rank
        quotient_coefficients = 0 if kernel == 0 else _choose(kernel + 3, 4)
        ideal_degree4_dimension = 495 - quotient_coefficients
        out.append({
            "rank_L": rank,
            "kernel_dimension": kernel,
            "quartic_quotient_coefficients": quotient_coefficients,
            "degree4_ideal_dimension": ideal_degree4_dimension,
        })
    return out


def _choose(n, k):
    if k < 0 or k > n:
        return 0
    value = 1
    for j in range(1, k + 1):
        value = value * (n - k + j) // j
    return value


def main():
    controls = set()
    w40, w25 = load_controls()
    controls.add("pinned_inputs")

    p40, fail40 = raw_profile(w40)
    p25, fail25 = raw_profile(w25)
    require(p40 == [1, 1, 1] and not sum(v for k, v in fail40.items() if k <= 4),
            (p40, fail40))
    require(p25 == [1, 1, 1] and fail25[4] == 78, (p25, fail25))
    controls.add("raw_x4_boundary")

    profiles = {}
    all_records = {}
    for name, source in (("W40", w40), ("W25-F8", w25)):
        records, atomic_checks = all_carriers(source)
        profiles[name] = carrier_summary(records)
        profiles[name]["atomic_reconstruction_checks"] = atomic_checks
        all_records[name] = records
    require(profiles["W40"]["star"]["passing"] == 6, profiles["W40"])
    require(profiles["W40"]["triangle"]["passing"] == 0, profiles["W40"])
    require(profiles["W25-F8"]["star"]["passing"] == 0, profiles["W25-F8"])
    require(profiles["W25-F8"]["triangle"]["passing"] == 0, profiles["W25-F8"])
    ledger_path = HERE / "compressed_carrier_ledger.jsonl"
    write_compressed_ledger(ledger_path, all_records)
    controls.add("atomic_carrier_reconstruction")
    controls.add("quartic_disjunction_equivalence")

    slices = {}
    for name, source in (("W40", w40), ("W25-F8", w25)):
        checked, defects = slice_identity_defects(source)
        slices[name] = {
            "identities_checked": checked,
            "defect_count": len(defects),
            "first_defects": defects[:12],
        }
    require(slices["W40"]["defect_count"] == 0, slices["W40"])
    require(slices["W25-F8"]["defect_count"] > 0, slices["W25-F8"])
    controls.add("slice_identity_x4_consumption")

    # Endpoint-order mutation must change a literal response row.
    changed = 0
    for p, q in EDGES:
        residual = tuple(v for v in SITES if v not in (p, q))
        for a, b in combinations(residual, 2):
            changed += response_edge(w40, p, q, a, b) != response_edge(
                w40, p, q, a, b, mutant=True)
    require(changed > 0, "endpoint-order mutant survived")
    controls.add("endpoint_order_mutation")

    # Dropping one required diagonal activity factor incorrectly admits at
    # least one W25 carrier (there are carriers blocked only by that factor).
    mutant_admissions = 0
    for kind, pair, carrier, data in all_records["W25-F8"]:
        basis = nullspace(data["rowspace"])
        acts = activity(w25, *pair)
        mutant = multiply_linear_forms([
            restrict_linear(acts[index], basis) for index in (0, 1, 3)
        ])
        mutant_admissions += bool(mutant) and not data["passes"]
    require(mutant_admissions > 0, "activity-factor mutant did not fire")
    controls.add("activity_factor_mutation")

    covariance = {
        "W40": covariance_check(w40, all_records["W40"]),
        "W25-F8": covariance_check(w25, all_records["W25-F8"]),
    }
    controls.add("site_color_covariance")

    diagonal = diagonal_boundary()
    pd, fd = raw_profile(diagonal)
    require(pd == [1, 1, 1] and sum(v for k, v in fd.items() if k <= 4) > 0,
            (pd, fd))
    controls.add("diagonal_outside_x4")

    twisted = twisted_binary_boundary()
    pt, ft = raw_profile(twisted)
    require(pt == [1, 1, 0], (pt, ft))
    controls.add("twisted_binary_boundary")

    require(controls == DECLARED_CONTROLS,
            {"missing": sorted(DECLARED_CONTROLS - controls),
             "extra": sorted(controls - DECLARED_CONTROLS)})

    result = {
        "status": "PASS",
        "scope": (
            "exact symmetry-compressed residual over an infinite field; "
            "no universal X4-to-cap proof"
        ),
        "theorem": {
            "carrier_failure": (
                "q_pq=k00*k11*k22*<K,A_pq> belongs to "
                "rowspan(L_C)*Sym^3(C*)"
            ),
            "atomic_compression": (
                "rowspan(L_C) is the sum of forbidden atomic response-edge "
                "rowspaces among 15 blocks per pair"
            ),
            "orbit_templates": {
                "star": {"representative": "(pair 01, centre 2)", "orbit_size": 168},
                "triangle": {"representative": "(pair 01, triangle 234)", "orbit_size": 560},
            },
            "slice_identity": (
                "delta_z=H6(z)*ell3+sum_ab H4(z\\{a,b})*rho_ab(z_a,z_b), "
                "for each residual z with max color multiplicity at least 4"
            ),
            "slice_identities_per_pair": 219,
            "rank_strata": dimension_table(),
        },
        "controls": {
            "declared": sorted(DECLARED_CONTROLS),
            "executed": sorted(controls),
            "endpoint_mutant_changed_atomic_blocks": changed,
            "activity_mutant_false_admissions": mutant_admissions,
            "covariance_checks": covariance,
        },
        "calibration": {
            "W40": {
                "pure_values": [str(v) for v in p40],
                "raw_failure_histogram": dict(sorted(fail40.items())),
                "carriers": profiles["W40"],
                "slices": slices["W40"],
            },
            "W25-F8": {
                "pure_values": [str(v) for v in p25],
                "raw_failure_histogram": dict(sorted(fail25.items())),
                "carriers": profiles["W25-F8"],
                "slices": slices["W25-F8"],
            },
            "diagonal_common_matching": {
                "pure_values": [str(v) for v in pd],
                "raw_failure_histogram": dict(sorted(fd.items())),
                "meaning": "pure-normalized diagonal boundary, outside X4",
            },
            "twisted44_binary_face": {
                "pure_values": [str(v) for v in pt],
                "raw_failure_histogram": dict(sorted(ft.items())),
                "meaning": (
                    "fixed binary twisted-4+4 representative with color-2 "
                    "face zero; W40 is its relevant pure-normalized X4 extension"
                ),
            },
        },
        "input_hashes": {str(path.relative_to(ROOT)): value for path, value in PINNED.items()},
        "compressed_ledger": {
            "path": ledger_path.name,
            "records": 2 * 728,
            "sha256": digest(ledger_path),
        },
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    (HERE / "results.json").write_text(payload)
    print(json.dumps({
        "status": result["status"],
        "W40_star_passes": profiles["W40"]["star"]["passing"],
        "W25_all_carrier_passes": (
            profiles["W25-F8"]["star"]["passing"]
            + profiles["W25-F8"]["triangle"]["passing"]
        ),
        "W40_slice_defects": slices["W40"]["defect_count"],
        "W25_slice_defects": slices["W25-F8"]["defect_count"],
        "result_sha256": sha256(payload.encode()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()

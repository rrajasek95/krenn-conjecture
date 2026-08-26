#!/usr/bin/env python3
"""Exact Q(sqrt(2)) branch census for all 86 class-0,30,45 shadows."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPORTER = HERE / "export_class_03045_laurent_interface.py"
SHADOW = (ROOT / "computations/unaudited-codex-x5-zero-tail-assembly-2026-08-21" /
          "results_extended_diagonal_packet_support_shadow.json")
PACKET = (ROOT / "computations/unaudited-codex-x5-zero-tail-assembly-2026-08-21" /
          "extended_diagonal_packet_1566.json")
OUT = HERE / "results_class_03045_exact_branches.json"


def load_exporter():
    spec = importlib.util.spec_from_file_location("class03045_exporter", EXPORTER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


M = load_exporter()


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


# Elements a+b*r with r^2=2.
def nf(a=0, b=0):
    return Fraction(a), Fraction(b)


def nf_add(left, right):
    return left[0]+right[0], left[1]+right[1]


def nf_mul(left, right):
    return (left[0]*right[0] + 2*left[1]*right[1],
            left[0]*right[1] + left[1]*right[0])


def nf_inv(value):
    norm = value[0]*value[0] - 2*value[1]*value[1]
    require(norm, "division by zero in Q(sqrt2)")
    return value[0]/norm, -value[1]/norm


def nf_pow(value, exponent):
    if exponent < 0:
        return nf_pow(nf_inv(value), -exponent)
    answer = nf(1)
    while exponent:
        if exponent & 1:
            answer = nf_mul(answer, value)
        value = nf_mul(value, value)
        exponent >>= 1
    return answer


def nf_json(value):
    return [[value[0].numerator, value[0].denominator],
            [value[1].numerator, value[1].denominator]]


def evaluate(poly, values):
    answer = nf()
    for exponents, coefficient in poly.items():
        term = nf(coefficient)
        for value, exponent in zip(values, exponents):
            if exponent:
                term = nf_mul(term, nf_pow(value, exponent))
        answer = nf_add(answer, term)
    return answer


def scale(poly, scalar):
    return M.clean(Counter({exponents: scalar * coefficient
                            for exponents, coefficient in poly.items()}))


def variable(index, exponent=1):
    return M.laurent_variable(index, exponent)


def sparse_unit_certificate(masks, source_label):
    """Verify a four-term integer Laurent identity for each residual."""
    one = M.constant(1)
    two = M.constant(2)
    source = M.word_expr(source_label)
    u1, v1, w1 = variable(3), variable(4), variable(5)
    s = M.multiply(v1, variable(3, -1), variable(5, -1))
    g = M.add(M.multiply(s, s), scale(s, -2), M.constant(-1))
    if tuple(masks) == (11, 11, 11):
        x = variable(0)  # u0
        f = M.add(M.multiply(x, x), scale(x, 2), M.constant(-1))
        multiplier = scale(M.multiply(M.add(x, M.constant(3)),
                                      M.add(s, M.constant(-3)),
                                      v1, variable(5, -1)), -1)
        rhs = M.add(M.multiply(multiplier, source),
                    M.multiply(M.add(two, scale(g, -1)), f),
                    scale(g, 2))
        identity = (
            "4=-(u0+3)*(s-3)*(v1/w1)*P +(2-g)*f +2*g; "
            "f=u0^2+2*u0-1=-u0*t0_012, "
            "g=s^2-2*s-1=s*t1_123, s=v1/(u1*w1)")
        triangle_sources = ["t0_012", "t1_123"]
    else:
        require(tuple(masks) == (18, 63, 33), "unknown residual mask")
        x = variable(1)  # v0
        f = M.add(M.multiply(x, x), scale(x, 2), M.constant(-1))
        multiplier = scale(M.multiply(M.add(x, M.constant(3)),
                                      M.add(s, M.constant(-1)), v1), -1)
        rhs = M.add(M.multiply(multiplier, source),
                    M.multiply(M.add(two, g), f), scale(g, -2))
        identity = (
            "4=-(v0+3)*(s-1)*v1*P +(2+g)*f -2*g; "
            "f=v0^2+2*v0-1=-v0*t0_013, "
            "g=s^2-2*s-1=s*t1_123, s=v1/(u1*w1)")
        triangle_sources = ["t0_013", "t1_123"]
    require(rhs == M.constant(4), "sparse Laurent unit identity failed")
    return {
        "source_label_P": source_label,
        "triangle_source_labels": triangle_sources,
        "identity": identity,
        "integer_identity_verified_exactly": True,
        "P_terms": len(source),
        "multiplier_terms": len(multiplier),
        "f_terms": len(f),
        "g_terms": len(g),
        "P_sha256": sha256(json.dumps(M.serialize(source), sort_keys=True,
                                       separators=(",", ":")).encode("ascii")).hexdigest(),
    }


CUT_MASKS = {0, 7, 25, 30, 42, 45, 51, 52}
ODD_TRIANGLE_MASKS = {63 ^ mask for mask in CUT_MASKS}
TYPE_A = {11, 12, 56, 63}
TYPE_B = {18, 21, 33, 38}
Z_ROOTS = (nf(-1, 1), nf(-1, -1))
BRANCH_BITS = {
    "A": ((0, 0, 0), (0, 0, 1), (0, 1, 1),
          (1, 0, 0), (1, 1, 0), (1, 1, 1)),
    "B": ((0, 0, 0), (0, 0, 1), (0, 1, 0),
          (1, 0, 1), (1, 1, 0), (1, 1, 1)),
}


def local_branches(mask):
    require(mask in ODD_TRIANGLE_MASKS, "asked for branches on even triangle mask")
    kind = "A" if mask in TYPE_A else "B"
    return tuple(tuple(Z_ROOTS[index] for index in bits)
                 for bits in BRANCH_BITS[kind])


def all_literal_rows(packet):
    rows = [(row["label"], row["orbit"]) for row in packet["explicit_rows"]]
    rows.extend((row["label"], "exact_e_multiple")
                for row in packet["omitted_exact_e_multiple_orbit"]["rows"])
    require(len(rows) == 1638, "packet row count changed")
    return sorted(rows)


def minimum_cover(coverages, full_mask):
    unique = {}
    for label, mask in coverages.items():
        if mask:
            unique.setdefault(mask, label)
    records = sorted((label, mask) for mask, label in unique.items())
    for label, mask in records:
        if mask == full_mask:
            return [label]
    for index, (left_label, left_mask) in enumerate(records):
        missing = full_mask ^ (full_mask & left_mask)
        for right_label, right_mask in records[index+1:]:
            if right_mask & missing == missing:
                return [left_label, right_label]
    # Greedy fallback is explicitly labelled if a two-row cover is absent.
    chosen, covered = [], 0
    while covered != full_mask:
        label, mask = max(records, key=lambda row: (row[1] & ~covered).bit_count())
        require((mask & ~covered).bit_count(), "cover stalled")
        chosen.append(label)
        covered |= mask
    return chosen


def build_state_interface(masks, q_cuts, rows):
    M.X_RELATIONS = tuple(masks)
    M.hafnian.cache_clear()
    row_polys = {label: M.word_expr(label) for label, _ in rows}
    h_polys = [M.hafnian(colour, tuple(range(8))) for colour in range(3)]
    q_polys, c_polys, selected = {}, {}, set()
    for colour, cut in enumerate(q_cuts):
        for orientation in M.q_orientation_pair(cut):
            selected.add((colour, tuple(2*vertex+int(bit)
                                        for vertex, bit in enumerate(orientation))))
        for sites in combinations(range(8), 4):
            q_polys[(colour, sites)] = M.q_value(colour, sites)
        for omitted in combinations(range(8), 2):
            c_polys[(colour, omitted)] = M.c_value(colour, omitted)
    return row_polys, h_polys, q_polys, c_polys, selected


def solve_residual_state(record, rows):
    masks = tuple(record["x_relation_masks_e01_e02_e03_e12_e13_e23"])
    q_cuts = tuple(record["q_pair_cut_masks_e01_e02_e03_e12_e13_e23"])
    row_polys, h_polys, q_polys, c_polys, selected = build_state_interface(
        masks, q_cuts, rows)
    local = [local_branches(mask) for mask in masks]
    assignments = [left+middle+right
                   for left, middle, right in product(*local)]
    require(len(assignments) == 216, "local root branch count changed")

    # Replay all triangle equations independently on every advertised branch.
    for values in assignments:
        for colour in range(3):
            for triple in combinations(range(4), 3):
                sites = tuple(site for vertex in triple for site in M.PAIRING[vertex])
                require(evaluate(M.hafnian(colour, sites), values) == nf(),
                        "advertised root branch failed a triangle")

    coverages = {label: 0 for label, _ in rows}
    packet_survivors, h_live_packet = [], 0
    signature_survivors = []
    first_failure_histogram = Counter()
    h_histogram = Counter()
    for branch_index, values in enumerate(assignments):
        live_h = tuple(evaluate(poly, values) != nf() for poly in h_polys)
        h_histogram["".join("1" if bit else "0" for bit in live_h)] += 1
        failed = []
        for label, _ in rows:
            if evaluate(row_polys[label], values) != nf():
                coverages[label] |= 1 << branch_index
                failed.append(label)
        if not failed:
            packet_survivors.append(branch_index)
            if all(live_h):
                h_live_packet += 1
        else:
            first_failure_histogram[min(failed)] += 1

        exact_signature = True
        for key, poly in q_polys.items():
            value = evaluate(poly, values)
            if (key in selected) != (value != nf()):
                exact_signature = False
                break
        if exact_signature:
            exact_signature = all(evaluate(poly, values) == nf()
                                  for poly in c_polys.values())
        if exact_signature:
            signature_survivors.append(branch_index)

    full_mask = (1 << len(assignments)) - 1
    cover = minimum_cover(coverages, full_mask)
    cover_records = []
    for label in cover:
        values = sorted({evaluate(row_polys[label], assignment)
                         for assignment in assignments})
        cover_records.append({
            "source_label": label,
            "branches_killed": coverages[label].bit_count(),
            "distinct_values": [nf_json(value) for value in values],
            "laurent_polynomial": M.serialize(row_polys[label]),
        })
    require(len(cover) == 1, "residual did not have a one-row source cover")
    unit_certificate = sparse_unit_certificate(masks, cover[0])
    return {
        "x_relation_masks": list(masks),
        "support_orbit_size": record["orbit_size"],
        "support_stabilizer_order_in_faithful_B4_times_S3":
            1152 // record["orbit_size"],
        "local_branch_types": ["A" if mask in TYPE_A else "B" for mask in masks],
        "local_root_branches_per_colour": [len(branches) for branches in local],
        "combined_root_branches": len(assignments),
        "H_liveness_histogram": dict(h_histogram),
        "full_packet_survivors": packet_survivors,
        "full_packet_H_live_survivors": h_live_packet,
        "exact_minimal_X_C_Q_signature_survivors": signature_survivors,
        "minimum_literal_source_cover": cover_records,
        "sparse_Laurent_Nullstellensatz": unit_certificate,
        "first_failure_histogram": dict(first_failure_histogram),
        "survivor_orbits_under_support_stabilizer": 0,
    }


def main():
    shadow = json.loads(SHADOW.read_text())
    packet = json.loads(PACKET.read_text())
    rows = all_literal_rows(packet)
    records = [row for row in shadow["support_shadow"]
               ["minimal_surviving_support_signature_antichain"]
               if row["q_pair_cut_masks_e01_e02_e03_e12_e13_e23"] == [0, 30, 45]]
    require(len(records) == 86, "0,30,45 refinement count changed")
    triangle_histogram = Counter()
    residual = []
    parity_certificates = []
    for record in records:
        masks = tuple(record["x_relation_masks_e01_e02_e03_e12_e13_e23"])
        good = sum(mask in ODD_TRIANGLE_MASKS for mask in masks)
        triangle_histogram[good] += 1
        if good == 3:
            residual.append(record)
            continue
        bad_colour = next(index for index, mask in enumerate(masks)
                          if mask not in ODD_TRIANGLE_MASKS)
        bad_mask = masks[bad_colour]
        bad_triangle = next(triple for triple in combinations(range(4), 3)
                            if sum((bad_mask >> M.EDGE_INDEX[edge]) & 1
                                   for edge in combinations(triple, 2)) % 2 == 0)
        M.X_RELATIONS = masks
        M.hafnian.cache_clear()
        bad_sites = tuple(site for vertex in bad_triangle for site in M.PAIRING[vertex])
        require(M.hafnian(bad_colour, bad_sites) == M.constant(-2),
                "triangle-parity unit did not replay as literal t=-2")
        parity_certificates.append({
            "x_relation_masks": list(masks),
            "bad_colour": bad_colour,
            "bad_triangle": list(bad_triangle),
            "identity": "t_c,ijk=-2, hence (-1/2)*t_c,ijk=1",
        })
    require(triangle_histogram == {0: 64, 1: 16, 2: 4, 3: 2},
            "triangle-parity refinement histogram changed")
    require([row["x_relation_masks_e01_e02_e03_e12_e13_e23"]
             for row in residual] == [[11, 11, 11], [18, 63, 33]],
            "triangle-compatible residual list changed")

    residual_results = [solve_residual_state(record, rows) for record in residual]
    require(all(not result["full_packet_survivors"] and
                not result["exact_minimal_X_C_Q_signature_survivors"]
                for result in residual_results),
            "a 0,30,45 coefficient branch survived")
    payload = {
        "status": "PASS exact class-0,30,45 Laurent branch inconsistency",
        "support_refinements": len(records),
        "triangle_compatible_colour_count_histogram": dict(triangle_histogram),
        "parity_unit_certificates": parity_certificates,
        "triangle_compatible_residuals": residual_results,
        "theorem": (
            "No minimal support refinement in the Q-geometry 0,30,45 is "
            "realizable by an H-live e=t=0 point satisfying the full 1,638-row "
            "diagonal packet over Qbar."),
        "proof_structure": (
            "Triangle parity gives a literal Laurent unit t=-2 on 84 support "
            "orbits. The remaining two have six exact Q(sqrt2) branches per "
            "colour; all 216 combined branches are killed by the recorded "
            "literal-source covers. No modular or Groebner inference is used."),
        "source_hashes": {
            str(EXPORTER.relative_to(ROOT)): file_sha(EXPORTER),
            str(SHADOW.relative_to(ROOT)): file_sha(SHADOW),
            str(PACKET.relative_to(ROOT)): file_sha(PACKET),
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    if "--check-results" in sys.argv:
        require(OUT.read_text() == text, "exact branch result replay mismatch")
    print(json.dumps({
        "status": payload["status"],
        "triangle_histogram": payload["triangle_compatible_colour_count_histogram"],
        "residuals": [{"masks": row["x_relation_masks"],
                       "branches": row["combined_root_branches"],
                       "packet_survivors": len(row["full_packet_survivors"]),
                       "cover": [item["source_label"]
                                 for item in row["minimum_literal_source_cover"]]}
                      for row in residual_results],
        "logical_sha256": payload["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

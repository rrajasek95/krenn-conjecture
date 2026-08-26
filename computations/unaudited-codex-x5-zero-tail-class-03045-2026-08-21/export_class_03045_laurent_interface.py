#!/usr/bin/env python3
"""Export the exact Laurent interface for the canonical 0,30,45 shadow.

This dependency-free script only constructs and profiles equations; it does
not solve them. Permanent equations are built into sparse 2x2 block forms,
and the residual anchor-preserving clone gauge sets b01=b02=b03=1.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import gcd
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ASSEMBLY = (ROOT / "computations/unaudited-codex-x5-zero-tail-assembly-2026-08-21" /
            "extended_diagonal_packet_1566.json")
SHADOW = (ROOT / "computations/unaudited-codex-x5-zero-tail-assembly-2026-08-21" /
          "results_extended_diagonal_packet_support_shadow.json")
OUT = HERE / "results_class_03045_laurent_interface.json"

PAIRING = ((0, 1), (2, 3), (4, 5), (6, 7))
SUPER_EDGES = tuple(combinations(range(4), 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(SUPER_EDGES)}
Q_CUTS = (0, 30, 45)
X_RELATIONS = (0, 18, 45)
VARS = ("u0", "v0", "w0", "u1", "v1", "w1", "u2", "v2", "w2")
ZERO_EXP = (0,) * len(VARS)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode("ascii")).hexdigest()


def clean(poly):
    return Counter({exponents: coefficient for exponents, coefficient
                    in poly.items() if coefficient})


def constant(value):
    return Counter({ZERO_EXP: value}) if value else Counter()


def add(*polys):
    answer = Counter()
    for poly in polys:
        answer.update(poly)
    return clean(answer)


def multiply(*polys):
    answer = constant(1)
    for poly in polys:
        updated = Counter()
        for left, left_coefficient in answer.items():
            for right, right_coefficient in poly.items():
                updated[tuple(a+b for a, b in zip(left, right))] += (
                    left_coefficient * right_coefficient)
        answer = clean(updated)
    return answer


def laurent_variable(index, exponent=1, coefficient=1):
    powers = [0] * len(VARS)
    powers[index] = exponent
    return Counter({tuple(powers): coefficient})


def mask_bits(mask):
    return [int(bool(mask & (1 << index))) for index in range(6)]


def cut_mask(bits):
    return sum((bits[i] ^ bits[j]) << index
               for index, (i, j) in enumerate(SUPER_EDGES))


def q_orientation_pair(mask):
    words = []
    for raw in range(16):
        bits = tuple((raw >> (3-index)) & 1 for index in range(4))
        if cut_mask(bits) == mask:
            words.append("".join(map(str, bits)))
    require(len(words) == 2 and
            tuple(1-int(bit) for bit in words[0]) == tuple(map(int, words[1])),
            "Q cut did not give a complement pair")
    return sorted(words)


def block_parameter(colour, super_edge, inverse=False, coefficient=1):
    if super_edge[0] == 0:
        return constant(coefficient)
    variable_index = 3 * colour + EDGE_INDEX[super_edge] - 3
    return laurent_variable(variable_index, -1 if inverse else 1, coefficient)


def entry(colour, site_left, site_right):
    if site_left > site_right:
        site_left, site_right = site_right, site_left
    super_left, clone_left = divmod(site_left, 2)
    super_right, clone_right = divmod(site_right, 2)
    if super_left == super_right:
        return constant(1)
    edge = (super_left, super_right)
    relation = (X_RELATIONS[colour] >> EDGE_INDEX[edge]) & 1
    if relation == 0:
        if (clone_left, clone_right) == (0, 0):
            return block_parameter(colour, edge)
        if (clone_left, clone_right) == (1, 1):
            return block_parameter(colour, edge, inverse=True, coefficient=-1)
        return Counter()
    if (clone_left, clone_right) == (0, 1):
        return block_parameter(colour, edge)
    if (clone_left, clone_right) == (1, 0):
        return block_parameter(colour, edge, inverse=True, coefficient=-1)
    return Counter()


@lru_cache(maxsize=None)
def hafnian(colour, sites):
    sites = tuple(sites)
    if not sites:
        return constant(1)
    first = sites[0]
    answer = Counter()
    for index in range(1, len(sites)):
        second = sites[index]
        rest = sites[1:index] + sites[index+1:]
        answer = add(answer, multiply(entry(colour, first, second),
                                      hafnian(colour, rest)))
    return answer


def q_value(colour, sites):
    return hafnian(colour, tuple(sorted(sites)))


def c_value(colour, omitted):
    sites = tuple(site for site in range(8) if site not in omitted)
    return hafnian(colour, sites)


def word_expr(label):
    word = tuple(map(int, label))
    answer = constant(1)
    for colour in range(3):
        sites = tuple(index for index, value in enumerate(word)
                      if value == colour)
        if not sites:
            continue
        if len(sites) == 2:
            factor = entry(colour, *sites)
        elif len(sites) == 4:
            factor = q_value(colour, sites)
        elif len(sites) == 6:
            omitted = tuple(index for index in range(8) if index not in sites)
            factor = c_value(colour, omitted)
        else:
            raise RuntimeError("unexpected word profile")
        answer = multiply(answer, factor)
        if not answer:
            return answer
    return answer


def canonical(poly):
    poly = clean(poly)
    if not poly:
        return Counter()
    minima = tuple(min(exponents[index] for exponents in poly)
                   for index in range(len(VARS)))
    shifted = Counter({tuple(value-minima[index]
                             for index, value in enumerate(exponents)): coefficient
                       for exponents, coefficient in poly.items()})
    content = 0
    for coefficient in shifted.values():
        content = gcd(content, abs(coefficient))
    require(content > 0, "zero Laurent content")
    shifted = Counter({exponents: coefficient // content
                       for exponents, coefficient in shifted.items()})
    leading = max(shifted, key=lambda exponents: (sum(exponents), exponents))
    if shifted[leading] < 0:
        shifted = Counter({exponents: -coefficient
                           for exponents, coefficient in shifted.items()})
    return clean(shifted)


def serialize(poly):
    return [{"exponents": list(exponents), "coefficient": coefficient}
            for exponents, coefficient in sorted(canonical(poly).items())]


def expression_record(poly):
    serialized = serialize(poly)
    if not serialized:
        return None
    used = [index for index in range(len(VARS))
            if any(row["exponents"][index] for row in serialized)]
    text = json.dumps(serialized, sort_keys=True, separators=(",", ":"))
    return {
        "terms": len(serialized),
        "total_degree": max(sum(row["exponents"]) for row in serialized),
        "variables": [VARS[index] for index in used],
        "sha256": sha256(text.encode("ascii")).hexdigest(),
        "polynomial": serialized,
    }


def main():
    packet = json.loads(ASSEMBLY.read_text())
    shadow = json.loads(SHADOW.read_text())
    representative = next(
        row for row in shadow["support_shadow"]
        ["minimal_surviving_support_signature_antichain"]
        if row["q_pair_cut_masks_e01_e02_e03_e12_e13_e23"] == list(Q_CUTS)
        and row["x_relation_masks_e01_e02_e03_e12_e13_e23"] == list(X_RELATIONS))
    require(representative["orbit_size"] == 288,
            "canonical 0,30,45 representative changed")

    e_values, t_values, h_values, q_values, c_values = {}, {}, {}, {}, {}
    for colour in range(3):
        for edge in SUPER_EDGES:
            sites = PAIRING[edge[0]] + PAIRING[edge[1]]
            e_values[f"e{colour}_{edge[0]}{edge[1]}"] = q_value(colour, sites)
        for triple in combinations(range(4), 3):
            sites = tuple(site for vertex in triple for site in PAIRING[vertex])
            t_values[f"t{colour}_{''.join(map(str, triple))}"] = hafnian(colour, sites)
        h_values[f"H{colour}"] = hafnian(colour, tuple(range(8)))
        for sites in combinations(range(8), 4):
            q_values[(colour, sites)] = q_value(colour, sites)
        for omitted in combinations(range(8), 2):
            c_values[(colour, omitted)] = c_value(colour, omitted)
    require(all(not value for value in e_values.values()),
            "a built-in permanent equation failed")

    selected_q, selected_q_labels = set(), {}
    for colour, mask in enumerate(Q_CUTS):
        orientations = q_orientation_pair(mask)
        selected_q_labels[str(colour)] = orientations
        for orientation in orientations:
            selected_q.add((colour, tuple(2*vertex + int(bit)
                                           for vertex, bit in enumerate(orientation))))

    support_zero_equations, selected_q_records = {}, {}
    for key, value in q_values.items():
        label = f"Q{key[0]}_{''.join(map(str, key[1]))}"
        if key in selected_q:
            selected_q_records[label] = expression_record(value)
        else:
            record = expression_record(value)
            if record is not None:
                support_zero_equations[label] = record
    for key, value in c_values.items():
        record = expression_record(value)
        if record is not None:
            support_zero_equations[f"C{key[0]}_{key[1][0]}{key[1][1]}"] = record

    literal_rows = packet["explicit_rows"] + [
        {"label": row["label"], "profile": "4+2+2", "orbit": "exact_e_multiple"}
        for row in packet["omitted_exact_e_multiple_orbit"]["rows"]]
    require(len(literal_rows) == 1638, "literal packet count changed")
    nonzero_by_orbit, nonzero_by_profile = Counter(), Counter()
    cross_records, cross_sources = {}, defaultdict(list)
    for row in literal_rows:
        record = expression_record(word_expr(row["label"]))
        if record is None:
            continue
        nonzero_by_orbit[row["orbit"]] += 1
        nonzero_by_profile[row["profile"]] += 1
        cross_records.setdefault(record["sha256"], record)
        cross_sources[record["sha256"]].append(row["label"])

    one_colour_records = {}
    for label, value in t_values.items():
        record = expression_record(value)
        require(record is not None, f"triangle {label} vanished structurally")
        one_colour_records[label] = record
    all_equation_shas = (set(row["sha256"] for row in one_colour_records.values()) |
                         set(cross_records) |
                         set(row["sha256"] for row in support_zero_equations.values()))

    live_factors = {}
    for label, record in selected_q_records.items():
        require(record is not None, f"selected live {label} vanished structurally")
        live_factors[label] = record
    for label, value in h_values.items():
        record = expression_record(value)
        require(record is not None, f"{label} vanished structurally")
        live_factors[label] = record

    payload = {
        "status": "PASS exact canonical 0,30,45 Laurent interface export (unsolved)",
        "canonical_support": {
            "q_cut_masks": list(Q_CUTS),
            "q_orientation_pairs": selected_q_labels,
            "x_relation_masks": list(X_RELATIONS),
            "x_relation_bits_e01_e02_e03_e12_e13_e23":
                [mask_bits(mask) for mask in X_RELATIONS],
            "B4_times_S3_orbit_size": representative["orbit_size"],
            "entry_support": ("In each block relation 0 retains x00,x11; relation 1 "
                              "retains x01,x10. All retained entries are Laurent-live."),
        },
        "gauge": {
            "anchor_entries": 12,
            "live_cross_entries_before_permanent_solve": 36,
            "permanent_equations_built_in": 18,
            "block_parameters_after_permanent_solve": 18,
            "residual_clone_gauges_used": 9,
            "normalizations": "b_c,01=b_c,02=b_c,03=1 for c=0,1,2",
            "Laurent_variables": list(VARS),
            "ambient_Laurent_dimension": len(VARS),
        },
        "one_colour_equations": {
            "triangle_literal_count": len(t_values),
            "unique_numerators": len({row["sha256"] for row in one_colour_records.values()}),
            "records": one_colour_records,
        },
        "cross_packet_after_entry_support": {
            "literal_rows": len(literal_rows),
            "structurally_nonzero_literal_rows": sum(nonzero_by_orbit.values()),
            "nonzero_by_profile": dict(nonzero_by_profile),
            "nonzero_by_orbit": dict(nonzero_by_orbit),
            "unique_numerators": len(cross_records),
            "records": [dict(record, source_count=len(cross_sources[key]),
                             first_source=min(cross_sources[key]))
                        for key, record in sorted(cross_records.items())],
        },
        "exact_minimal_signature_conditions": {
            "zero_Q_or_C_expressions_nontrivial": len(support_zero_equations),
            "unique_zero_numerators": len({row["sha256"]
                                           for row in support_zero_equations.values()}),
            "selected_live_Q_count": len(selected_q_records),
            "H_live_count": len(h_values),
            "zero_records": support_zero_equations,
            "live_records": live_factors,
        },
        "combined_unique_equation_numerators": len(all_equation_shas),
        "solve_launched": False,
        "scope_guard": ("This is the exact Laurent coefficient interface for one "
                        "minimal support stratum. No equation count or support "
                        "survivor is a realizability claim."),
        "source_hashes": {
            str(ASSEMBLY.relative_to(ROOT)): file_sha(ASSEMBLY),
            str(SHADOW.relative_to(ROOT)): file_sha(SHADOW),
        },
    }
    payload["logical_sha256"] = logical_sha(payload)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if "--write-results" in sys.argv:
        OUT.write_text(text)
    if "--check-results" in sys.argv:
        require(OUT.read_text() == text, "Laurent interface replay mismatch")
    print(json.dumps({
        "status": payload["status"],
        "canonical_support": payload["canonical_support"],
        "gauge": payload["gauge"],
        "one_colour_unique": payload["one_colour_equations"]["unique_numerators"],
        "cross_nonzero_literal": payload["cross_packet_after_entry_support"]
            ["structurally_nonzero_literal_rows"],
        "cross_unique": payload["cross_packet_after_entry_support"]["unique_numerators"],
        "signature_zero_unique": payload["exact_minimal_signature_conditions"]
            ["unique_zero_numerators"],
        "combined_unique": payload["combined_unique_equation_numerators"],
        "logical_sha256": payload["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

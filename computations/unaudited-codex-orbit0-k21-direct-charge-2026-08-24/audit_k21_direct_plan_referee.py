#!/usr/bin/env python3
"""Independent signature-level referee for the direct-parent K21 plan.

This does not evaluate the cycle functional.  It compresses the 485 R8-prime
records and the three E-factor packets by their twelve-anchor signatures,
which is sufficient to count parents, dividing pivots, and K21 tail
occurrences exactly.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import struct


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STRUCTURE = (ROOT / "computations"
             / "unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
             / "filtered_k16_structure.bin")
AUX = (ROOT / "computations"
       / "unaudited-codex-orbit0-filtered-k16-run-2026-08-23"
       / "filtered_k17_aux.bin")
K4 = (ROOT / "computations"
      / "unaudited-codex-orbit0-filtered-k18-charge-2026-08-23"
      / "filtered_k18_k4.bin")
DAG = (ROOT / "computations"
       / "unaudited-codex-orbit0-k14-k24-recurrence-dag-2026-08-23"
       / "results_recurrence_dag.json")
OUT = HERE / "results_k21_direct_plan_referee.json"

U = 400_591_699_200
TAIL_COUNTS = {2: 12, 3: 32, 4: 60}
ZERO = (0,) * 12

PACKETS = (
    ("D17:234|R:4", (2, 3, 4), 4),
    ("D17:243|R:4", (2, 4, 3), 4),
    ("D17:324|R:4", (3, 2, 4), 4),
    ("D17:333|R:4", (3, 3, 3), 4),
    ("D17:342|R:4", (3, 4, 2), 4),
    ("D17:423|R:4", (4, 2, 3), 4),
    ("D17:432|R:4", (4, 3, 2), 4),
    ("D18:244|R:3", (2, 4, 4), 3),
    ("D18:334|R:3", (3, 3, 4), 3),
    ("D18:343|R:3", (3, 4, 3), 3),
    ("D18:424|R:3", (4, 2, 4), 3),
    ("D18:433|R:3", (4, 3, 3), 3),
    ("D18:442|R:3", (4, 4, 2), 3),
    ("D19:344|R:2", (3, 4, 4), 2),
    ("D19:434|R:2", (4, 3, 4), 2),
    ("D19:443|R:2", (4, 4, 3), 2),
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as source:
        while block := source.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def signature(row: bytes, anchor_position: dict[int, int]) -> tuple[int, ...]:
    out = [0] * 12
    for cell in row:
        if cell in anchor_position:
            out[anchor_position[cell]] += 1
    return tuple(out)


def convolve(left: Counter, right: Counter) -> Counter:
    out = Counter()
    for a, ca in left.items():
        for b, cb in right.items():
            out[add(a, b)] += ca * cb
    return out


def parse_structure():
    data = STRUCTURE.read_bytes()
    require(data[:11] == b"K16DIRECT1\0", data[:11])
    offset = 11
    nt, nr, np, na = struct.unpack_from("<IIII", data, offset)
    offset += 16
    require((nt, nr, np, na) == (384, 485, 78, 12), (nt, nr, np, na))
    anchor_colours = data[offset:offset + 12]
    offset += 12
    anchor_position = {cell: i for i, cell in enumerate(anchor_colours)}
    require(len(anchor_position) == 12, anchor_colours.hex())

    # Each transform stores a 252-cell permutation and a 12-anchor permutation.
    offset += nt * (252 + 12)
    records = []
    for _ in range(nr):
        row = data[offset:offset + 12]
        size = struct.unpack_from("<I", data, offset + 12)[0]
        coefficient = struct.unpack_from("<q", data, offset + 16)[0]
        offset += 24
        records.append((signature(row, anchor_position), size * coefficient))

    pivots = []
    for _ in range(np):
        pivots.append(tuple(data[offset:offset + 12]))
        offset += 12

    factors = [[None] * 3 for _ in range(3)]
    factor_cardinalities = [[0] * 3 for _ in range(3)]
    for factor in range(3):
        for degree_index in range(3):
            count = struct.unpack_from("<I", data, offset)[0]
            offset += 4
            terms = []
            for _ in range(count):
                term = data[offset:offset + 4]
                offset += 4
                terms.append(signature(term, anchor_position))
            factors[factor][degree_index] = Counter(terms)
            factor_cardinalities[factor][degree_index] = count
    require(offset == len(data), (offset, len(data)))
    require(factor_cardinalities == [[12, 32, 60]] * 3,
            factor_cardinalities)
    return anchor_position, records, pivots, factors, factor_cardinalities


def parse_pivot_tails(anchor_position):
    data = AUX.read_bytes()
    require(data[:8] == b"K17AUX1\0", data[:8])
    offset = 8
    scale, = struct.unpack_from("<Q", data, offset)
    offset += 8
    cover_count, pivot_count = struct.unpack_from("<II", data, offset)
    offset += 8
    require((scale, cover_count, pivot_count) == (281_801_520, 25, 78),
            (scale, cover_count, pivot_count))
    offset += 12 * cover_count
    tails = [{2: None, 3: None, 4: None} for _ in range(pivot_count)]
    anchors = []
    for pivot in range(pivot_count):
        anchors.append(bytes(data[offset:offset + 4]))
        offset += 4
        for degree, count in ((2, 12), (3, 32)):
            terms = []
            for _ in range(count):
                term = data[offset:offset + 4]
                offset += 4
                terms.append(signature(term, anchor_position))
            tails[pivot][degree] = Counter(terms)
    require(offset == len(data), (offset, len(data)))

    k4 = K4.read_bytes()
    require(k4[:7] == b"K18K4A1", k4[:7])
    offset = 7
    for pivot in range(pivot_count):
        terms = []
        for _ in range(60):
            term = k4[offset:offset + 4]
            offset += 4
            terms.append(signature(term, anchor_position))
        tails[pivot][4] = Counter(terms)
    require(offset == len(k4), (offset, len(k4)))
    require(all(sum(tails[p][d].values()) == TAIL_COUNTS[d]
                for p in range(78) for d in (2, 3, 4)), "tail cardinality drift")
    return anchors, tails


def available(sig, pivots):
    return tuple(i for i, pivot in enumerate(pivots)
                 if all(value >= need
                        for value, need in zip(sig, pivot, strict=True)))


def packet_signature_mass(records, factors, degrees):
    factor_mass = Counter({ZERO: 1})
    for factor, degree in enumerate(degrees):
        factor_mass = convolve(factor_mass, factors[factor][degree - 2])
    # Preserve R8 mass because exact U-clearing is an occurrence-level guard.
    out = Counter()
    for r_sig, mass in records:
        for e_sig, multiplicity in factor_mass.items():
            out[(add(r_sig, e_sig), mass)] += multiplicity
    return factor_mass, out


def audit_packet(packet_id, degrees, tail_degree, records, factors, pivots, tails):
    factor_mass, parents = packet_signature_mass(records, factors, degrees)
    parent_count = pivotable = pivot_uses = irreducible_tail_occurrences = 0
    pivot_histogram = Counter()
    bad_divisions = []
    for (sig, mass), multiplicity in parents.items():
        ps = available(sig, pivots)
        m = len(ps)
        parent_count += multiplicity
        pivot_histogram[m] += multiplicity
        if not m:
            continue
        pivotable += multiplicity
        pivot_uses += multiplicity * m
        if (mass * U) % m:
            bad_divisions.append({
                "signature": list(sig), "R8prime_mass": mass,
                "pivot_count": m, "remainder": (mass * U) % m,
            })
        for pivot in ps:
            for tail_sig, tail_multiplicity in tails[pivot][tail_degree].items():
                child = tuple(sig[i] - pivots[pivot][i] + tail_sig[i]
                              for i in range(12))
                if not available(child, pivots):
                    irreducible_tail_occurrences += (
                        multiplicity * tail_multiplicity)
    require(not bad_divisions, bad_divisions[:3])
    terms_per_slice = 1
    for degree in degrees:
        terms_per_slice *= TAIL_COUNTS[degree]
    require(sum(factor_mass.values()) == terms_per_slice,
            (packet_id, sum(factor_mass.values()), terms_per_slice))
    require(parent_count == 485 * terms_per_slice,
            (packet_id, parent_count, 485 * terms_per_slice))
    full_tail_occurrences = TAIL_COUNTS[tail_degree] * pivot_uses
    return {
        "id": packet_id,
        "direct_degrees": list(degrees),
        "response_tail_degree": tail_degree,
        "response_terms_per_pivot": TAIL_COUNTS[tail_degree],
        "parent_formula": f"485*{'*'.join(str(TAIL_COUNTS[d]) for d in degrees)}",
        "terms_per_R8prime_slice": terms_per_slice,
        "raw_parents": parent_count,
        "pivotable_parents": pivotable,
        "irreducible_parents": parent_count - pivotable,
        "pivot_uses": pivot_uses,
        "full_K21_tail_occurrences": full_tail_occurrences,
        "irreducible_K21_tail_occurrences": irreducible_tail_occurrences,
        "pivot_count_histogram": {
            str(count): frequency
            for count, frequency in sorted(pivot_histogram.items())
        },
        "U_clears_every_scaled_occurrence": True,
    }


def aggregate(packets, degree):
    chosen = [packet for packet in packets
              if int(packet["id"][1:3]) == degree]
    keys = ("raw_parents", "pivotable_parents", "irreducible_parents",
            "pivot_uses", "full_K21_tail_occurrences",
            "irreducible_K21_tail_occurrences")
    return {
        "source_degree": degree,
        "ids": [packet["id"] for packet in chosen],
        **{key: sum(packet[key] for packet in chosen) for key in keys},
    }


def main():
    anchor_position, records, pivots, factors, cardinalities = parse_structure()
    _, tails = parse_pivot_tails(anchor_position)
    packets = [audit_packet(packet_id, degrees, tail_degree,
                            records, factors, pivots, tails)
               for packet_id, degrees, tail_degree in PACKETS]
    groups = [aggregate(packets, degree) for degree in (17, 18, 19)]

    expected = {
        17: (82_938_880, 81_076_480, 267_564_800),
        18: (152_251_200, 137_817_600, 260_736_000),
        19: (167_616_000, 111_744_000, None),
    }
    for group in groups:
        values = (group["raw_parents"], group["pivotable_parents"],
                  group["pivot_uses"])
        wanted = expected[group["source_degree"]]
        require(all(w is None or v == w for v, w in zip(values, wanted, strict=True)),
                (group["source_degree"], values, wanted))

    dag = json.loads(DAG.read_text())
    required_k21 = set(dag["required_reachable_lineage_ids_by_degree"]["21"])
    covered = {packet["id"] for packet in packets}
    require(covered <= required_k21, sorted(covered - required_k21))
    require(len(covered) == 16 and len(required_k21) == 52,
            (len(covered), len(required_k21)))

    result = {
        "schema": "orbit0-k21-direct-plan-referee-v1",
        "status": "PASS_EXACT_SIGNATURE_LEVEL_DIRECT_K21_PLAN_REFEREE",
        "scope": ("Design/count/sign referee for the 16 one-response direct-parent "
                  "K21 paths only; no cycle-charge evaluation and no K21 row collection."),
        "convention": {
            "target": "P=-R8prime*E0*E1*E2",
            "direct_parent_coefficient": "c=-M_r, where M_r=orbit_size_r*R8prime_coefficient_r",
            "pivot_policy": "all literal dividing K0 pivots",
            "response_rule": "each of m dividing pivots emits every selected tail with coefficient -c/m=+M_r/m",
            "scaled_child_coefficient": "U*M_r/m",
            "scale_U": U,
            "charge_formula_scaled": ("sum_occ U*M_r/m * sum_{p dividing parent} "
                                      "sum_{t in T_shift(p)} lambda(parent-anchor_p+t)"),
            "sign_relative_to_signed_R8prime_mass": "positive for all 16 paths",
        },
        "factor_cardinalities_by_labelled_factor_K2_K3_K4": cardinalities,
        "R8prime_slices": len(records),
        "literal_K0_pivots": len(pivots),
        "packets": packets,
        "groups": groups,
        "coverage": {
            "covered_direct_response_K21_ids": sorted(covered),
            "covered_count": len(covered),
            "required_K21_count": len(required_k21),
            "is_complete_K21_page": covered == required_k21,
            "uncovered_required_K21_count": len(required_k21 - covered),
            "guard": "The planned run is a 16-path subtotal, not the complete 52-path K21 page.",
        },
        "pinned_inputs": {
            str(path.relative_to(ROOT)): digest(path)
            for path in (STRUCTURE, AUX, K4, DAG)
        },
    }
    logical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["logical_sha256"] = sha256(logical).hexdigest()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "groups": groups,
        "covered": len(covered),
        "required_K21": len(required_k21),
        "logical_sha256": result["logical_sha256"],
    }, indent=2))


if __name__ == "__main__":
    main()

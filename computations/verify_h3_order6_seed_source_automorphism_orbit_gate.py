#!/usr/bin/env python3
"""Test the natural source-automorphism orbit of the first seed family.

The seed family is every order-six operator containing the first forbidden
pair (01:11) wedge (07:11).  Its two homogeneous word pieces are the pure
and mixed seed types.  We close their constrained D2 images under the three
committed source symmetries relevant to this packet:

* residual-site swap s=(0 1),
* endpoint transpose theta=(0 1)(6 7), and
* simultaneous tail Weyl recolouring at sites 2 and 5.

Only transformations whose transported vectors remain in the fixed pinned
rank-153 image count as internal naturality.  Transformations which land in
a conjugate word/fine/direct-free component are recorded, not projected
back by forgetting labels.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py":
        "f1bc7a9f8fdb9148fde5c4d79a4b7f59a3bd03cd6ff00dc1c2fb3c0e7f511ea9",
    "computations/verify_h3_order6_first_forbidden_face_exact_seed_cycle_gate.py":
        "0c3367ab48327bfbe308dc81191019d094eec054a04c3d1f2bd38f0e69faa2e9",
    "computations/verify_h3_physical_cartan_source_orbit_descent.py":
        "c92667c38c57c69dff18fd7570fa154db7e1a634a83f462dfde6bd5553128a3a",
    "computations/verify_h3_trapped_hessian_to_six_term_endpoint_polarization_gate.py":
        "a51b8f091a25624d17443c70ac70b60eb257c8b11dafb0b9ad3f17962dc07390",
}
EXPECTED_LEDGER_SHA256 = "5cfe95d4a768a60242099e32c5b41edec5a8a5b6e8394a2e94fdb2399707533b"

FIRST_ROW = (2, ((0, 1, 1, 1), (0, 7, 1, 1)))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        require(expected != "TO_BE_PINNED", ("unfrozen pin", relative))
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def projected_constrained_basis(site, columns, shifts, direct_free_pair,
                                prime):
    by_shift = defaultdict(list)
    for column, shift in zip(columns, shifts, strict=True):
        by_shift[repr(shift)].append(column)
    constrained = []
    for key in sorted(by_shift):
        basis = {}
        for column in by_shift[key]:
            added, pivot = site.insert(dict(column), basis, prime)
            if added and pivot[0] == 2:
                require(all(row[0] == 2 for row in basis[pivot]),
                        ("constrained vector retained a lower row", pivot))
                constrained.append(basis[pivot])
    shadow_basis = {}
    for vector in constrained:
        site.insert(dict(vector), shadow_basis, prime)
    projected = {}
    hit = set()
    for vector in shadow_basis.values():
        nonphysical = {
            row: value for row, value in vector.items()
            if not site.physical_pair(row[1], direct_free_pair)
        }
        hit.update(nonphysical)
        site.insert(nonphysical, projected, prime)
    return projected, hit, len(shadow_basis)


def transform_cell(cell, flip01: bool, flip67: bool, tail_weyl: bool):
    left, right, a, b = cell
    permutation = {}
    if flip01:
        permutation.update({0: 1, 1: 0})
    if flip67:
        permutation.update({6: 7, 7: 6})
    left = permutation.get(left, left)
    right = permutation.get(right, right)
    if tail_weyl:
        if left in (2, 5) and a in (1, 2):
            a = 3 - a
        if right in (2, 5) and b in (1, 2):
            b = 3 - b
    if left < right:
        return left, right, a, b
    return right, left, b, a


def transform_vector(vector, flip01, flip67, tail_weyl, prime):
    answer = {}
    for row, value in vector.items():
        require(row[0] == 2, row)
        pair = tuple(sorted(
            transform_cell(cell, flip01, flip67, tail_weyl)
            for cell in row[1]
        ))
        target = (2, pair)
        result = (answer.get(target, 0) + value) % prime
        if result:
            answer[target] = result
        else:
            answer.pop(target, None)
    return answer


def group_elements():
    records = []
    for flip01 in (False, True):
        for flip67 in (False, True):
            for tail_weyl in (False, True):
                site_name = {
                    (False, False): "1",
                    (True, False): "s=(01)",
                    (False, True): "r=(67)",
                    (True, True): "theta=(01)(67)",
                }[(flip01, flip67)]
                name = site_name + (" * w_tail" if tail_weyl else "")
                records.append((name, flip01, flip67, tail_weyl))
    return tuple(records)


def quotient_pair_signature(row, direct_free_pair):
    require(row[0] == 2 and len(row[1]) == 2, row)
    left, right = row[1]
    left_sites = frozenset(left[:2])
    right_sites = frozenset(right[:2])
    return (
        f"shared_sites={len(left_sites & right_sites)};"
        f"direct_free_cells={sum(edge == direct_free_pair for edge in (left_sites, right_sites))};"
        f"same_uncoloured_edge={int(left_sites == right_sites)};"
        f"same_decorated_cell={int(left == right)}"
    )


def canonical_quotient_complement(site, seed_basis, full_basis,
                                  direct_free_pair, prime):
    combined = {}
    for vector in seed_basis.values():
        site.insert(dict(vector), combined, prime)
    require(len(combined) == 76, (prime, len(combined)))
    pivots = []
    added_vectors = []
    for pivot in sorted(full_basis, key=repr):
        added, new_pivot = site.insert(dict(full_basis[pivot]), combined, prime)
        if added:
            pivots.append(new_pivot)
            added_vectors.append(combined[new_pivot])
    require(len(combined) == 153 and len(pivots) == 77,
            (prime, len(combined), len(pivots)))
    histogram = defaultdict(int)
    for pivot in pivots:
        histogram[quotient_pair_signature(pivot, direct_free_pair)] += 1
    encoded = [repr(pivot) for pivot in pivots]
    return {
        "seed_basis_rank": 76,
        "canonical_added_monic_vectors": len(added_vectors),
        "combined_rank": len(combined),
        "minimal_additional_linear_generators": len(pivots),
        "quotient_pivot_rows_sha256": sha256(json.dumps(
            encoded, separators=(",", ":")
        ).encode()).hexdigest(),
        "first_ten_quotient_pivot_rows": encoded[:10],
        "quotient_pivot_type_histogram": dict(sorted(histogram.items())),
        "meaning": (
            "a canonical lexicographic modular complement: each added full "
            "source-derived constrained vector is monic on its displayed "
            "pivot modulo the preceding seed/complement vectors"
        ),
    }


def prime_orbit_audit(site, columns, shifts, direct_free_pair, prime):
    full_basis, full_hit, full_shadow_rank = projected_constrained_basis(
        site, columns, shifts, direct_free_pair, prime)
    require((full_shadow_rank, len(full_hit), len(full_basis))
            == (488, 159, 153),
            (prime, full_shadow_rank, len(full_hit), len(full_basis)))

    seed_indices = tuple(index for index, column in enumerate(columns)
                         if column.get(FIRST_ROW))
    seed_columns = [columns[index] for index in seed_indices]
    seed_shifts = [shifts[index] for index in seed_indices]
    seed_basis, seed_hit, seed_shadow_rank = projected_constrained_basis(
        site, seed_columns, seed_shifts, direct_free_pair, prime)
    require((len(seed_indices), seed_shadow_rank,
             len(seed_hit), len(seed_basis)) == (819, 178, 84, 76),
            (len(seed_indices), seed_shadow_rank,
             len(seed_hit), len(seed_basis)))

    records = []
    internal_vectors = []
    all_orbit_vectors = []
    for name, flip01, flip67, tail_weyl in group_elements():
        vectors = [transform_vector(
            vector, flip01, flip67, tail_weyl, prime,
        ) for vector in seed_basis.values()]
        support = set().union(*(set(vector) for vector in vectors))
        residues = [site.reduce_mod(vector, full_basis, prime)[0]
                    for vector in vectors]
        internal = not any(residues)
        transported_rank_basis = {}
        for vector in vectors:
            site.insert(vector, transported_rank_basis, prime)
        records.append({
            "element": name,
            "transported_rank": len(transported_rank_basis),
            "coordinate_support": len(support),
            "support_inside_fixed_full159": len(support & full_hit),
            "support_outside_fixed_full159": len(support - full_hit),
            "every_vector_in_fixed_rank153_image": internal,
        })
        all_orbit_vectors.extend(vectors)
        if internal:
            internal_vectors.extend(vectors)

    internal_basis = {}
    for vector in internal_vectors:
        site.insert(vector, internal_basis, prime)
    all_orbit_basis = {}
    for vector in all_orbit_vectors:
        site.insert(vector, all_orbit_basis, prime)
    internal_names = [record["element"] for record in records
                      if record["every_vector_in_fixed_rank153_image"]]
    complement = canonical_quotient_complement(
        site, seed_basis, full_basis, direct_free_pair, prime)
    outside_counts = sorted(record["support_outside_fixed_full159"]
                            for record in records if record["element"] != "1")
    require(internal_names == ["1"]
            and len(internal_basis) == 76
            and len(all_orbit_basis) == 200
            and outside_counts == [17, 25, 26, 38, 55, 58, 61],
            (prime, internal_names, len(internal_basis),
             len(all_orbit_basis), outside_counts))
    return {
        "prime": prime,
        "full_fixed_projection_rank": len(full_basis),
        "seed_projection_rank": len(seed_basis),
        "group_order": len(records),
        "element_records": records,
        "internal_fixed_grade_elements": internal_names,
        "rank_of_internal_naturality_orbit": len(internal_basis),
        "rank_defect_inside_fixed_image": len(full_basis) - len(internal_basis),
        "rank_of_all_conjugate_orbit_vectors_before_grade_identification":
            len(all_orbit_basis),
        "canonical_fixed_grade_complement": complement,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    site = load(
        "computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py",
        "seed_source_orbit_site",
    )
    loaded = site.modules()
    columns, shifts = site.build_operator_columns(loaded)
    require(len(columns) == len(shifts) == 8580, "column count changed")
    prime_records = [prime_orbit_audit(
        site, columns, shifts, loaded["base"].DIRECT_FREE_PAIR, prime,
    ) for prime in site.PRIMES]
    require(prime_records[0]["canonical_fixed_grade_complement"]
            ["quotient_pivot_rows_sha256"]
            == prime_records[1]["canonical_fixed_grade_complement"]
            ["quotient_pivot_rows_sha256"],
            "the two primes produced different quotient pivot rows")
    ledger = {
        "theorem": "h3 order-six first-seed source-automorphism orbit gate",
        "pins": PINS,
        "group_generators": [
            "residual-site swap s=(0 1)",
            "endpoint transpose theta=(0 1)(6 7)",
            "simultaneous tail Weyl recolouring at sites 2 and 5",
        ],
        "group_order": 8,
        "prime_audits": prime_records,
        "minimal_fixed_grade_response_envelope": {
            "seed_family_generators": 76,
            "additional_canonical_quotient_generators": 77,
            "total_rank": 153,
            "interpretation": (
                "within the fixed labelled component the two seed types and "
                "all their seed-containing multipliers do not suffice.  A "
                "minimal linear presentation needs 77 further monic "
                "constrained vectors, or a new natural constructor whose "
                "internal orbit supplies their quotient"
            ),
        },
        "verdict": (
            "The committed residual swap, endpoint transpose and tail Weyl "
            "do not enlarge the first seed family inside the fixed labelled "
            "rank-153 component.  Only the identity sends every seed vector "
            "back into that image; each nonidentity exports labelled rows to "
            "a conjugate component.  The internal orbit therefore remains "
            "rank 76 and a matching rank-77 quotient survives at both "
            "primes.  Canonical elimination supplies 77 monic quotient "
            "pivots, the minimal additional fixed-grade linear generating "
            "certificate.  A shifted grade-identification constructor could "
            "change this conclusion, but none is currently present"
        ),
        "scope": (
            "the literal source-automorphism group generated by the three "
            "pinned symmetries, with no forgetting of word/fine/direct-free "
            "labels.  Conjugate-grade vectors are recorded separately"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("seed orbit ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("full", "structural"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    if arguments.mode == "structural":
        pin_dependencies()
        print("h3 seed source-automorphism orbit structural gate: PASS")
        return
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"ledger": ledger, "sha256": digest},
                         indent=2, sort_keys=True))
    else:
        print("h3 seed source-automorphism orbit gate: PASS")
        for record in ledger["prime_audits"]:
            print(record["prime"],
                  "internal_rank", record["rank_of_internal_naturality_orbit"],
                  "defect", record["rank_defect_inside_fixed_image"],
                  "internal", record["internal_fixed_grade_elements"])
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

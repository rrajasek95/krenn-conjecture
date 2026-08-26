#!/usr/bin/env python3
"""Literal identification of the 23-row K10..K16 replacement dual.

This is an overlap/contraction audit only.  It does not enumerate another
incident page.  It compares the frozen 23-row cochain with the full labelled
supports of the cutoff-nine 37-row dual and sparse R8' representative, and
with the five same-head K14/K16 columns at its canonical factorized head.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
import argparse
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NEXT_DIR = (ROOT / "computations"
            / "unaudited-codex-orbit0-k16-smallest-dual-next-page-2026-08-23")
NEXT_SCRIPT = NEXT_DIR / "audit_k16_smallest_dual_next_page.py"
NEXT_RESULT = NEXT_DIR / "results_k16_smallest_dual_next_page.json"
CUTOFF_DIR = (ROOT / "computations"
              / "unaudited-codex-n8-dangerous-chart-bridge-2026-08-20")
CUTOFF_SCRIPT = CUTOFF_DIR / "audit_orbit0_cutoff9_exact_dual.py"
CUTOFF_RESULT = CUTOFF_DIR / "results_orbit0_cutoff9_exact_dual_audit.json"
R8_RESULT = CUTOFF_DIR / "results_orbit0_cutoff9_sparse_r8.json"
RESULT = HERE / "results_k16_dual_class_identification.json"


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


NEXT = load("k16_dual_class_next", NEXT_SCRIPT)
CUTOFF = load("k16_dual_class_cutoff", CUTOFF_SCRIPT)


def move_cutoff_row(row, action):
    sites, colours = CUTOFF.EXPORT.STABILIZER[action]
    return bytes(sorted(
        CUTOFF.BASE.CELL_ID[CUTOFF.EXPORT.transform_cell(
            CUTOFF.BASE.CELLS[cell], sites, colours)]
        for cell in row
    ))


def expand_cutoff_orbits(representatives):
    answer = {}
    for row, coefficient in representatives.items():
        for action in range(len(CUTOFF.EXPORT.STABILIZER)):
            moved = move_cutoff_row(row, action)
            require(moved not in answer or answer[moved] == coefficient,
                    "orbit coefficient collision")
            answer[moved] = coefficient
    return answer


def divides(divisor, row):
    left = Counter(divisor)
    right = Counter(row)
    return all(right[cell] >= multiplicity
               for cell, multiplicity in left.items())


def quotient(row, divisor):
    value = Counter(row)
    value.subtract(divisor)
    require(all(multiplicity >= 0 for multiplicity in value.values()),
            "nondividing quotient")
    return bytes(sorted(cell for cell, multiplicity in value.items()
                        for _ in range(multiplicity)))


def multiset_gcd(rows):
    common = Counter(rows[0])
    for row in rows[1:]:
        current = Counter(row)
        for cell in tuple(common):
            common[cell] = min(common[cell], current[cell])
            if not common[cell]:
                del common[cell]
    return bytes(sorted(cell for cell, multiplicity in common.items()
                        for _ in range(multiplicity)))


def difference_columns(columns):
    reference = Counter(columns[0])
    answer = []
    for column in columns[1:]:
        value = Counter(column)
        value.subtract(reference)
        answer.append({row: coefficient for row, coefficient in value.items()
                       if coefficient})
    return tuple(answer)


def build(mutate=False):
    pinned = {
        NEXT_SCRIPT: "409be1569ea132ce7c564076be08f81bd9fd211d457207bbfb439e7d36fb1906",
        NEXT_RESULT: "6926b86320967b0af1e8017accede210aa4e7fb4bc412cf1f704c6539f9c46fb",
        CUTOFF_SCRIPT: "a227da3ad893d3524964e1a9d04388931b83da2a764a6affca659aee76c35207",
        CUTOFF_RESULT: "3157241033f43b8f3c4cbb7a87cf24b8c84eb451e34ec9ddd29bcef44803d55d",
        R8_RESULT: "62013c8a8453ffe68e6ef08740859db6efecaf825f121c19dc885b6afa7feb4b",
    }
    for path, expected in pinned.items():
        require(file_sha256(path) == expected, f"frozen input drift: {path}")

    next_result = json.loads(NEXT_RESULT.read_text())
    require(next_result["logical_sha256"]
            == "c2dcada21b5904500e2d979bb4759cefbf6bdf449f81bef87ffb71b9827e7199",
            "23-row theorem drift")
    mu = {
        bytes.fromhex(record["row"]): Fraction(*record["coefficient"])
        for record in next_result["next_dual"]["support"]
    }
    q = bytes.fromhex(next_result["input"]["literal_q"])
    signature = tuple(next_result["input"]["canonical_anchor_signature"])
    require(len(mu) == 23 and mu[q] == 1, "23-row interface changed")
    if mutate:
        mu[q] += 1

    cutoff_result = json.loads(CUTOFF_RESULT.read_text())
    with CUTOFF.INTERFACE.open() as handle:
        header = json.loads(next(handle))
    cutoff_rows = tuple(bytes.fromhex(value) for value in header["rows_hex"])
    cutoff_representatives = {
        cutoff_rows[index]: Fraction(numerator, denominator)
        for index, numerator, denominator in cutoff_result["dual"]
    }
    cutoff_labelled = expand_cutoff_orbits(cutoff_representatives)

    r8_result = json.loads(R8_RESULT.read_text())
    r8_representatives = {
        bytes.fromhex(row): Fraction(coefficient)
        for row, _orbit_mass, coefficient in r8_result["residual"]
    }
    r8_labelled = expand_cutoff_orbits(r8_representatives)
    common = set(cutoff_labelled) & set(r8_labelled)
    require(len(cutoff_labelled) == 69264
            and len(r8_labelled) == 148176 and len(common) == 2304,
            "old labelled support census changed")
    require({cutoff_labelled[row] for row in common} == {Fraction(1)}
            and {r8_labelled[row] for row in common} == {Fraction(1)},
            "common old orbit coefficient changed")
    common_canonicals = {
        min(move_cutoff_row(row, action)
            for action in range(len(CUTOFF.EXPORT.STABILIZER)))
        for row in common
    }
    require(len(common_canonicals) == 1,
            "cutoff/R8' intersection is no longer one full orbit")

    contraction = []
    residual = []
    for row, coefficient in sorted(mu.items()):
        cutoff_divisors = tuple(value for value in cutoff_labelled
                                if divides(value, row))
        r8_divisors = tuple(value for value in r8_labelled
                            if divides(value, row))
        if cutoff_divisors or r8_divisors:
            require(len(cutoff_divisors) == len(r8_divisors) == 1
                    and cutoff_divisors == r8_divisors
                    and cutoff_divisors[0] in common,
                    "new row has a non-common or nonunique old divisor")
            divisor = cutoff_divisors[0]
            contraction.append({
                "row": row.hex(),
                "coefficient": [coefficient.numerator, coefficient.denominator],
                "divisor": divisor.hex(),
                "quotient": quotient(row, divisor).hex(),
            })
        else:
            residual.append({
                "row": row.hex(),
                "coefficient": [coefficient.numerator, coefficient.denominator],
            })
    require(len(contraction) == 8 and len(residual) == 15,
            "8+15 contraction split changed")
    require(len({record["divisor"] for record in contraction}) == 1,
            "eight old-shadow rows stopped sharing one literal divisor")

    _anchors, k6_packet, factor_H = NEXT.PREVIOUS.factor_data()
    k6_packet = set(k6_packet)
    require(len(k6_packet) == 1728 and len(factor_H) == 384,
            "frozen factor packet changed")
    k6_hits = sum(bytes.fromhex(record["quotient"]) in k6_packet
                  for record in contraction)
    require(k6_hits == 1, "old-shadow K6 quotient census changed")

    # The numerical support size 15 suggests a six-site hafnian fibre, but a
    # literal such fibre in this degree would be a fixed degree-21 multiplier
    # times the 15 three-cell perfect matchings.  Multiset gcd is invariant
    # under H.  The actual residual gcd has only degree 11; already the
    # displayed pair below has gcd degree 16, giving a two-row counterguard.
    residual_rows = tuple(bytes.fromhex(record["row"]) for record in residual)
    residual_gcd = multiset_gcd(residual_rows)
    pair_data = []
    for left_index in range(len(residual_rows)):
        for right_index in range(left_index + 1, len(residual_rows)):
            common_pair = bytes(sorted((Counter(residual_rows[left_index])
                                        & Counter(residual_rows[right_index]))
                                       .elements()))
            pair_data.append((len(common_pair), left_index, right_index,
                              common_pair))
    minimum_pair = min(pair_data)
    require(len(residual_gcd) == 11 and minimum_pair[0] == 16,
            "six-site-fibre counterguard changed")

    # H-module ranks are exact without elimination.  Every row below has a
    # free H-orbit and the 23 seed rows occupy distinct H-orbits.  Projection
    # to any one occupied orbit is therefore a 384x384 permutation matrix
    # times a nonzero scalar.  The old-product and residual coordinate sets
    # are disjoint H-stable sets, so their sum has rank 384+384.
    H = tuple(factor_H)
    row_orbits = {
        row: frozenset(NEXT.F.move_row(row, action) for action in H)
        for row in mu
    }
    require(all(len(orbit) == 384 for orbit in row_orbits.values())
            and len({min(orbit) for orbit in row_orbits.values()}) == 23,
            "23 rows stopped being distinct free H-orbit seeds")
    old_rows = {bytes.fromhex(record["row"]) for record in contraction}
    new_rows = set(mu) - old_rows
    require(old_rows and new_rows, "empty H-module summand")
    module_ranks = {
        "full_23_cochain_H_span": 384,
        "old_shadow_H_span": 384,
        "new_residual_H_span": 384,
        "old_shadow_plus_new_residual": 768,
        "proof": ("Each part contains a nonzero coefficient on a free "
                  "H-orbit; all 23 occupied row orbits are distinct. The "
                  "old-divisible coordinate set and its complement are "
                  "disjoint H-stable coordinate blocks."),
    }

    previous = json.loads(NEXT.PREVIOUS_RESULT.read_text())
    type_record = previous["types"][6]
    old_literal = {bytes.fromhex(record["row"])
                   for record in type_record["literal_dual_support"]}
    replacement = {bytes.fromhex(record["row"])
                   for record in next_result["input"]["replacement_dual"]}
    require(len(set(mu) & old_literal) == 0
            and set(mu) & replacement == {q},
            "direct prior-dual overlap changed")

    # Reconstruct both raw and post-second-singleton same-head tail columns.
    pivots = NEXT.PREVIOUS.mixed_pivots()
    raw_columns = []
    irreducible_columns = []
    pivot_labels = []
    for pivot in pivots:
        anchor_vector = pivot["anchor_vector"]
        if not all(left >= right for left, right
                   in zip(signature, anchor_vector, strict=True)):
            continue
        base = NEXT.PREVIOUS.quotient(q, pivot["anchor"])
        raw = Counter()
        irreducible = Counter()
        for tail, tail_vector in zip(pivot["tails"], pivot["tail_vectors"],
                                     strict=True):
            literal = bytes(sorted(base + tail))
            raw[literal] += 1
            projected = tuple(left - middle + right
                              for left, middle, right
                              in zip(signature, anchor_vector, tail_vector,
                                     strict=True))
            reducible = any(all(left >= right for left, right
                                in zip(projected, other["anchor_vector"],
                                       strict=True))
                            for other in pivots)
            if not reducible:
                irreducible[literal] += 1
        raw_columns.append(dict(raw))
        irreducible_columns.append(dict(irreducible))
        pivot_labels.append("".join(str(value) for value in pivot["colours"]))
    require(len(raw_columns) == len(irreducible_columns) == 5,
            "type-6 pivot count changed")

    def pairing(column):
        return sum(coefficient * mu.get(row, 0)
                   for row, coefficient in column.items())

    raw_pairings = tuple(pairing(column) for column in raw_columns)
    irreducible_pairings = tuple(pairing(column)
                                 for column in irreducible_columns)
    source_pairings = tuple(mu[q] + value for value in raw_pairings)
    raw_differences = difference_columns(raw_columns)
    irreducible_differences = difference_columns(irreducible_columns)
    raw_rank = NEXT.PREVIOUS.sparse_row_span(raw_columns, {})[0]
    irreducible_rank = NEXT.PREVIOUS.sparse_row_span(
        irreducible_columns, {})[0]
    raw_difference_rank = NEXT.PREVIOUS.sparse_row_span(raw_differences, {})[0]
    irreducible_difference_rank = NEXT.PREVIOUS.sparse_row_span(
        irreducible_differences, {})[0]
    require(raw_pairings == (Fraction(-1),) * 5
            and source_pairings == (Fraction(0),) * 5
            and irreducible_pairings == (Fraction(0),) * 5
            and all(pairing(column) == 0 for column in raw_differences)
            and all(pairing(column) == 0
                    for column in irreducible_differences),
            "hostile mutation/transfer invariance failed")
    require((raw_rank, irreducible_rank, raw_difference_rank,
             irreducible_difference_rank) == (5, 4, 4, 3),
            "same-head transfer ranks changed")

    result = {
        "format": "n8-orbit0-k16-dual-class-identification-v1",
        "status": "UNAUDITED exact literal overlap/contraction theorem",
        "pinned": {str(path.relative_to(ROOT)): digest
                   for path, digest in pinned.items()},
        "old_interfaces": {
            "cutoff9_dual_representatives": 37,
            "cutoff9_labelled_support": len(cutoff_labelled),
            "sparse_R8_prime_representatives": 120,
            "sparse_R8_prime_labelled_support": len(r8_labelled),
            "literal_support_intersection": len(common),
            "intersection_full_group_orbits": len(common_canonicals),
            "intersection_canonical_row": min(common_canonicals).hex(),
            "intersection_coefficient_in_both": [1, 1],
        },
        "new_23_cochain": {
            "support": len(mu),
            "common_multiset_factor": multiset_gcd(tuple(mu)).hex(),
            "common_multiset_factor_degree": len(multiset_gcd(tuple(mu))),
            "direct_overlap_old_type6_literal_dual": 0,
            "direct_overlap_four_row_replacement": 1,
            "old_shadow_rows": len(contraction),
            "genuinely_new_rows": len(residual),
            "old_shadow_common_literal_divisor": contraction[0]["divisor"],
            "old_shadow_K6_packet_quotients": k6_hits,
            "contraction": contraction,
            "residual": residual,
        },
        "H_action": {
            "order": len(H),
            "free_row_orbits": len(mu),
            "distinct_row_orbits": len({min(value)
                                         for value in row_orbits.values()}),
            "exact_module_ranks": module_ranks,
        },
        "same_head_transfer": {
            "pivot_labels": pivot_labels,
            "pivot_count": len(raw_columns),
            "raw_tail_rows": len(set().union(*(set(c) for c in raw_columns))),
            "raw_tail_column_rank": raw_rank,
            "raw_difference_rank": raw_difference_rank,
            "raw_tail_pairings": [[x.numerator, x.denominator]
                                    for x in raw_pairings],
            "q_plus_raw_tail_pairings": [[x.numerator, x.denominator]
                                          for x in source_pairings],
            "post_second_singleton_tail_rows": len(set().union(
                *(set(c) for c in irreducible_columns))),
            "post_second_singleton_column_rank": irreducible_rank,
            "post_second_singleton_difference_rank": irreducible_difference_rank,
            "post_second_singleton_pairings": [
                [x.numerator, x.denominator] for x in irreducible_pairings],
            "interpretation": ("The new functional is invariant under all "
                               "five same-head choices: it evaluates every "
                               "raw tail at -1 and q+tail at 0, while its "
                               "restriction to the post-second-singleton "
                               "irreducible tails is zero."),
        },
        "six_site_fibre_hypothesis": {
            "verdict": "FALSE",
            "residual_rows": len(residual_rows),
            "required_common_multiplier_degree": 21,
            "actual_maximal_common_multiplier_degree": len(residual_gcd),
            "actual_maximal_common_multiplier": residual_gcd.hex(),
            "smallest_pairwise_gcd_degree": minimum_pair[0],
            "smallest_pairwise_counterguard": {
                "left": residual_rows[minimum_pair[1]].hex(),
                "right": residual_rows[minimum_pair[2]].hex(),
                "gcd": minimum_pair[3].hex(),
            },
            "reason": ("A literal six-site word contributes three-cell PM "
                       "terms, hence its degree-24 translate has one common "
                       "degree-21 multiplier. H transport preserves multiset "
                       "gcd degree. The residual gcd degree is only 11, so "
                       "the count 15 is accidental rather than one PM6 fibre, "
                       "including any signed puncturing of that fibre."),
        },
        "verdict": {
            "classification": "GENUINELY_NEW_CLASS_WITH_OLD_EIGHT_ROW_SHADOW",
            "positive_overlap": ("Eight rows contract through one literal "
                                 "row in the unique cutoff9/R8' common orbit."),
            "decisive_counterguard": ("Fifteen nonzero rows have no literal "
                                      "divisor anywhere in the complete "
                                      "cutoff9 or R8' labelled supports. Their "
                                      "free H-orbits form a disjoint exact "
                                      "rank-384 summand, so the full cochain "
                                      "cannot be an old separator product or "
                                      "an H-transport of one."),
            "transfer_relation": ("It is nevertheless a persistent descendant "
                                  "with respect to the local K14/K16 same-head "
                                  "kernel, since every transfer difference pairs "
                                  "zero."),
        },
        "scope_guard": ("Literal support, contraction, H-action, and the one "
                        "canonical type-6 same-head star only. No claim of a "
                        "canonical isomorphism between the cutoff-nine and "
                        "K16 cohomology groups, and no next incident page."),
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["logical_sha256"] = sha256(payload.encode("ascii")).hexdigest()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mutate", action="store_true")
    args = parser.parse_args()
    result = build(mutate=args.mutate)
    RESULT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("K16 dual class identification: PASS")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify exact two-row units on all two-cell E14 extensions.

Expand each of the nine minimal E14 charts once with every absent internal
cell formal.  Restriction of those universal rows to two variables audits
all 57,291 unordered two-cell extensions without treating them as unrelated
support faces.  Four complete-row tiers close every pair: the original G11
row, another G11 row, a unary row, or (for one eight-pair K4,2 defect type)
one G22 row.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
E14_PATH = "computations/verify_h3_c6_e14_minimal_enlargement_unit.py"
UNARY_PATH = "computations/verify_h3_c6_e14_pure11_unary_unit.py"
PINS = {
    E14_PATH:
        "d5682f9134ff3dafddb4908707e5ceaacb25ff8b37632e57d9f9f3a4b62f84a8",
    "notes/h3-c6-e14-minimal-enlargement-unit.md":
        "552adf8a24410d4b8a09e61809c9a40c40274ad9c49a7ffe01b7ceb0d5ea22a7",
    "computations/verify_h3_c6_e14_mixed10_companion_row_unit.py":
        "4bdc70c34be6cd96c2521c97a3302acea6dd7db0e11bd6a7d5b6d74fbbcb2ba4",
    "notes/h3-c6-e14-mixed10-companion-row-unit.md":
        "842660467a4a39cf4d2002a1f3adf0e1591fc4031b7101b0f8a2d403062bf9ee",
    UNARY_PATH:
        "07160a67a4a16885fe481265ce67a372117b323dea82819e220cbe79e131df2d",
    "notes/h3-c6-e14-pure11-unary-unit.md":
        "cc9603e2f63e5b3de3b80dbf144a4f559f6e21f168fd9dfe9d5f95c4c7467ec4",
}
EXPECTED_LEDGER_SHA256 = (
    "bc05d86692dbf405ae8f961d0eab0d4e27a45e891e47ff38892a7497eebfe22d"
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(path, name):
    spec = spec_from_file_location(name, ROOT / path)
    require(spec is not None and spec.loader is not None,
            f"cannot load dependency {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def universal(e14, b4, first_index, second_index):
    q_cells, _added, _selected = e14.q_inventory(
        b4, first_index, second_index
    )
    candidates = []
    candidate_names = set()
    for left, right in combinations(range(6), 2):
        physical = (left, right)
        for left_colour in range(3):
            for right_colour in range(3):
                decoration = (left_colour, right_colour)
                if decoration in q_cells.get(physical, {}):
                    continue
                name = f"v{left}{right}{left_colour}{right_colour}"
                q_cells.setdefault(physical, {})[decoration] = {
                    (name,): Q(1)
                }
                candidates.append(((left, right,
                                    left_colour, right_colour), name))
                candidate_names.add(name)

    responses = e14.response_11(b4, q_cells)
    unary = {}
    for tail in b4.perfect_matchings(range(6)):
        choices = [q_cells[physical] for physical in tail]
        for decorations in product(*[tuple(options) for options in choices]):
            word = [None] * 6
            coefficient = {(): Q(1)}
            for physical, decoration in zip(
                    tail, decorations, strict=True):
                word[physical[0]], word[physical[1]] = decoration
                coefficient = e14.multiply(
                    coefficient, q_cells[physical][decoration]
                )
            word = tuple(word)
            unary[word] = e14.add(unary.get(word, {}), coefficient)
    return candidates, candidate_names, responses, unary


def restrict_polynomial(polynomial, allowed, candidate_names):
    return tuple(sorted(
        (monomial, coefficient)
        for monomial, coefficient in polynomial.items()
        if (set(monomial) & candidate_names) <= allowed
    ))


def restrict_row(row, allowed, candidate_names):
    answer = []
    for endpoint, polynomial in row.items():
        restricted = restrict_polynomial(
            polynomial, allowed, candidate_names
        )
        if restricted:
            answer.append((endpoint, restricted))
    return tuple(sorted(answer))


def negate_polynomial(polynomial):
    return tuple((monomial, -coefficient)
                 for monomial, coefficient in polynomial)


def negate_row(row):
    return tuple((endpoint, negate_polynomial(polynomial))
                 for endpoint, polynomial in row)


def first_row_witness(rows, words, target, allowed, candidate_names):
    negative_target = negate_row(target)
    for word in words:
        candidate = restrict_row(rows[word], allowed, candidate_names)
        if candidate == target:
            return word, 1
        if candidate == negative_target:
            return word, -1
    return None


def first_polynomial_witness(rows, words, target, allowed, candidate_names):
    negative_target = negate_polynomial(target)
    for word in words:
        candidate = restrict_polynomial(
            rows[word], allowed, candidate_names
        )
        if candidate == target:
            return word, 1
        if candidate == negative_target:
            return word, -1
    return None


def audit():
    pin_dependencies()
    e14 = load(E14_PATH, "e14_two_cell")
    b4 = e14.load(e14.B4_PATH, "b4")
    chart_counts = {}
    tier_counts = Counter()
    last_tier_records = []
    classification_hash = sha256()
    for first_index in (1, 2, 3):
        for second_index in (1, 2, 3):
            candidates, names, responses, unary = universal(
                e14, b4, first_index, second_index
            )
            response_words = tuple(
                word for word in responses if word != (1,) * 6
            )
            response22_words = tuple(
                word for word in responses if word != (2,) * 6
            )
            unary_words = tuple(word for word in unary if word != (0,) * 6)
            modes = Counter()
            for (first_cell, first_name), (second_cell, second_name) in (
                    combinations(candidates, 2)):
                allowed = {first_name, second_name}
                response_target = restrict_row(
                    responses[(1,) * 6], allowed, names
                )
                base_zero = restrict_row(
                    responses[e14.ZERO_WORD[first_index]], allowed, names
                )
                if base_zero == response_target:
                    tier = "base_G11_parallel"
                    witness_word, sign = e14.ZERO_WORD[first_index], 1
                else:
                    witness = first_row_witness(
                        responses, response_words, response_target,
                        allowed, names
                    )
                    if witness is not None:
                        tier = "alternate_G11_parallel_or_antiparallel"
                        witness_word, sign = witness
                    else:
                        unary_target = restrict_polynomial(
                            unary[(0,) * 6], allowed, names
                        )
                        witness = first_polynomial_witness(
                            unary, unary_words, unary_target, allowed, names
                        )
                        if witness is not None:
                            tier = "unary_parallel_or_antiparallel"
                            witness_word, sign = witness
                        else:
                            response22_target = restrict_row(
                                responses[(2,) * 6], allowed, names
                            )
                            witness = first_row_witness(
                                responses, response22_words,
                                response22_target, allowed, names
                            )
                            require(witness is not None,
                                    "a two-cell extension escaped all four tiers")
                            tier = "final_G22_parallel"
                            witness_word, sign = witness
                            require(witness_word in {
                                        (0, 2, 2, 2, 2, 0),
                                        (2, 0, 0, 2, 2, 2),
                                    }
                                    and sign == 1,
                                    f"the final G22 companion changed: "
                                    f"{witness_word}, {sign}")
                            last_tier_records.append({
                                "X1_tail_index": first_index,
                                "X2_tail_index": second_index,
                                "first_cell": list(first_cell),
                                "second_cell": list(second_cell),
                                "G22_zero_word":
                                    "".join(map(str, witness_word)),
                                "ordinary_source_identity":
                                    "F_G22[zero]-F_G22[222222]=1",
                            })

                modes[tier] += 1
                tier_counts[tier] += 1
                record = (
                    f"{first_index},{second_index};{first_cell};{second_cell};"
                    f"{tier};{''.join(map(str, witness_word))};{sign}\n"
                )
                classification_hash.update(record.encode())

            pair_count = len(candidates) * (len(candidates) - 1) // 2
            require(sum(modes.values()) == pair_count,
                    "a chart pair count escaped the tier census")
            chart_counts[f"{first_index},{second_index}"] = {
                "candidate_cell_count": len(candidates),
                "two_cell_pair_count": pair_count,
                "tier_counts": dict(sorted(modes.items())),
            }

    require(tier_counts == Counter({
        "base_G11_parallel": 51615,
        "alternate_G11_parallel_or_antiparallel": 2850,
        "unary_parallel_or_antiparallel": 2818,
        "final_G22_parallel": 8,
    }), f"the global two-cell tier split changed: {tier_counts}")
    total = sum(tier_counts.values())
    require(total == 57291,
            f"the two-cell extension universe changed: {total}")
    require(len(last_tier_records) == 8,
            "the final K4,2 residual count changed")
    expected_pure = {
        (0, 2, 1, 1), (1, 2, 1, 1),
        (2, 4, 1, 1), (2, 5, 1, 1),
    }
    expected_bridge = {(1, 3, 2, 0), (3, 4, 0, 1)}
    for record in last_tier_records:
        require((record["X1_tail_index"], record["X2_tail_index"])
                == (1, 3),
                "the last tier left its unique bright chart")
        cells = {tuple(record["first_cell"]), tuple(record["second_cell"])}
        require(len(cells & expected_pure) == 1
                and len(cells & expected_bridge) == 1,
                "the final defect stopped being the K4,2 cell type")

    ledger = {
        "pins": PINS,
        "chart_counts": chart_counts,
        "two_cell_extension_count": total,
        "ordinary_source_unit_count": total,
        "tier_counts": dict(sorted(tier_counts.items())),
        "classification_stream_sha256": classification_hash.hexdigest(),
        "final_G22_record_count": len(last_tier_records),
        "final_G22_records": last_tier_records,
        "theorem": (
            "every unordered simultaneous two-new-internal-cell extension "
            "of every minimal E14 bright chart has an ordinary two-row "
            "source unit in G11, the unary equation, or G22"
        ),
        "last_defect_type": (
            "before G22, exactly eight chart-(1,3) pairs remain: one pure-"
            "11 cell in {02,12,24,25} and one bridge in {q13:20,q34:01}. "
            "A complete G22 zero row (022220 or 200222) equals the target "
            "row and closes all eight"
        ),
        "scope": (
            "this closes exactly two simultaneous new internal cells on the "
            "canonical minimal E14 coefficient fibre, with all core endpoint "
            "components retained by the complete response rows.  It does "
            "not cover three or more new cells, outside-core endpoints, "
            "arbitrary global source components, active-rank landing, or "
            "termination"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"two-cell unit ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 C6 E14 two-cell unit frontier: PASS (exact)")
    print(f"extensions={ledger['two_cell_extension_count']}")
    print(f"tiers={ledger['tier_counts']}")
    print(f"final_G22_records={ledger['final_G22_record_count']}")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()

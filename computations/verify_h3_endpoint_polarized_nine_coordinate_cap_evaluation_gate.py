#!/usr/bin/env python3
"""Construct the endpoint-polarized nine-coordinate marked cap evaluation.

Keep the response word 11110000, the cap pair (6,7), the internal cap word
012112, the direct-free pair 36, and the marked parent/fine carrier.  Vary
the two endpoint colours through all nine ordered pairs.  The corresponding
products of local root operators map every matching term coefficient-one to
the same matching in word 012112ab.  Trigger-dependent divided roots extend
all nine maps over the marked collision resolution.

Thus the full word family supplies all nine matrix coefficients of an
arbitrary physical cap K.  The coordinate maps have common graph support and
commute with q23/q45 deletion and reinsertion.  They occupy nine distinct
word/colour-fine summands; their physical direct sum is covariant, while no
single fixed Gamma word contains it.

This linear completion does not choose an active clean K.  On the diagonal
subfamily, the h=3 clean error is cubic and has seven mixed polarization
coefficients in addition to the three coordinate cubics.  Those seven are
the first exact cross-colour conditions not supplied by coordinatewise
marked naturality.
"""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_marked_parent_endpoint_coordinate_cap_activity_gate.py":
        "5996feac9d555cee0783e9601311b614396b0f0211bc60ecb380c249565fa6f9",
    "computations/verify_h3_six_root_marked_collision_word_section.py":
        "d0da0f1473fc1032416c3758ffc932531ac71698c2370ee67224baedd2e13f95",
    "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py":
        "9b387023ee8cac6bb000d6936a8985cbc16bbad0a9f7deb3613c1f44c233a1f8",
    "computations/verify_clean_pair_cap_exact_descent_symbolic.py":
        "d6507c2afa341ce5c15056feddf92b9a171e2a5c80652617b595c7c7cf35acf5",
    "computations/verify_cap_line_cubic_activity_dichotomy.py":
        "39a0b8ee22e4eec56b1174d200e29679a3baeae1a814ec422f69b6a9725f1300",
}
EXPECTED_LEDGER_SHA256 = (
    "2aa36b361952f824c0951fd3c4a0e916ecea91ac91b0ba8e9e00cfd8c7b32750"
)

SITES = tuple(range(8))
COLOURS = tuple(range(3))
P, QSITE, RCHART = 6, 7, 3
DIRECT_FREE_EDGE = (RCHART, P)
RESPONSE_WORD = tuple(map(int, "11110000"))
CAP_INTERNAL_WORD = tuple(map(int, "012112"))
CUTS = ((2, 3), (4, 5))


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


def edge_key(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(remainder):
            yield (edge_key(first, second),) + tail


def cap_word(a: int, b: int) -> tuple[int, ...]:
    return CAP_INTERNAL_WORD + (a, b)


def decorated_monomial(word, matching):
    return tuple(sorted(
        (left, right, word[left], word[right])
        for left, right in matching
    ))


def apply_site_root(monomial, site: int, old: int, new: int):
    outputs = []
    for position, cell in enumerate(monomial):
        left, right, left_colour, right_colour = cell
        changed = None
        if left == site and left_colour == old:
            changed = (left, right, new, right_colour)
        elif right == site and right_colour == old:
            changed = (left, right, left_colour, new)
        if changed is None:
            continue
        output = list(monomial)
        output[position] = changed
        outputs.append(tuple(sorted(output)))
    return tuple(outputs)


def apply_root_product(monomial, target_word, omitted=()):
    terms = {tuple(monomial): Q(1)}
    omitted = frozenset(omitted)
    for site, (old, new) in enumerate(zip(RESPONSE_WORD, target_word,
                                          strict=True)):
        if old == new or site in omitted:
            continue
        following = Counter()
        for term, coefficient in terms.items():
            for output in apply_site_root(term, site, old, new):
                following[output] += coefficient
        terms = {term: coefficient for term, coefficient in following.items()
                 if coefficient}
    return terms


def remove_cell(monomial, edge):
    edge = edge_key(*edge)
    cells = [cell for cell in monomial if cell[:2] == edge]
    require(len(cells) == 1, (edge, monomial))
    answer = list(monomial)
    answer.remove(cells[0])
    return tuple(answer), cells[0]


def internal_tail(monomial):
    return tuple(cell for cell in monomial
                 if P not in cell[:2] and QSITE not in cell[:2])


def sparse_rank(columns) -> int:
    basis = {}
    for original in columns:
        vector = {row: Q(value) for row, value in original.items() if value}
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                coefficient = vector[pivot]
                basis[pivot] = {row: value / coefficient
                                for row, value in vector.items()}
                break
            coefficient = vector[pivot]
            for row, value in basis[pivot].items():
                residue = vector.get(row, Q(0)) - coefficient * value
                if residue:
                    vector[row] = residue
                else:
                    vector.pop(row, None)
    return len(basis)


def nine_coordinate_word_and_support_audit():
    matchings = tuple(perfect_matchings(SITES))
    parents = tuple(matching for matching in matchings
                    if DIRECT_FREE_EDGE not in matching)
    require(len(matchings) == 105 and len(parents) == 90,
            (len(matchings), len(parents)))

    coordinate_columns = []
    all_targets = set()
    changed_site_histogram = Counter()
    direct_free_term_maps = 0
    common_tail_checks = 0
    remote_cofactor_squares = 0
    cut_squares = Counter()

    for a in COLOURS:
        for b in COLOURS:
            word = cap_word(a, b)
            changed = tuple(site for site, values in enumerate(zip(
                RESPONSE_WORD, word, strict=True)) if values[0] != values[1])
            changed_site_histogram[len(changed)] += 1
            require({RESPONSE_WORD[site] for site in changed} == {0, 1},
                    (a, b, changed))
            require(len(set(word)) > 1, word)

            coordinate_index = 3 * a + b
            coordinate_columns.append({coordinate_index: Q(1)})
            for matching in matchings:
                source = decorated_monomial(RESPONSE_WORD, matching)
                target = decorated_monomial(word, matching)
                require(apply_root_product(source, word) == {target: Q(1)},
                        (a, b, matching))
                tagged_target = (a, b, target)
                require(tagged_target not in all_targets, tagged_target)
                all_targets.add(tagged_target)

            for matching in parents:
                source = decorated_monomial(RESPONSE_WORD, matching)
                target = decorated_monomial(word, matching)
                direct_free_term_maps += 1

                # Endpoint recolouring changes only cells incident to p or q.
                # The untouched internal matching tail is literally common.
                source_reference = decorated_monomial(cap_word(0, 0), matching)
                require(internal_tail(target) == internal_tail(source_reference),
                        (a, b, matching))
                common_tail_checks += 1

                for edge in matching:
                    if P in edge or QSITE in edge:
                        continue
                    source_lower, source_cell = remove_cell(source, edge)
                    target_lower, target_cell = remove_cell(target, edge)
                    lower = apply_root_product(source_lower, word, omitted=edge)
                    require(lower == {target_lower: Q(1)},
                            ("cofactor/root square", a, b, edge, matching))
                    require(source_cell[:2] == target_cell[:2] == edge,
                            (source_cell, target_cell))
                    remote_cofactor_squares += 1
                    if edge in CUTS:
                        cut_squares[(a, b, edge)] += 1

    require(changed_site_histogram == {4: 1, 5: 4, 6: 4},
            changed_site_histogram)
    require(sparse_rank(coordinate_columns) == 9, coordinate_columns)
    require(len(all_targets) == 9 * 105, len(all_targets))
    require(direct_free_term_maps == common_tail_checks == 9 * 90,
            (direct_free_term_maps, common_tail_checks))
    require(remote_cofactor_squares == 9 * 195,
            remote_cofactor_squares)
    require(all(cut_squares[(a, b, (2, 3))] == 15
                and cut_squares[(a, b, (4, 5))] == 12
                for a in COLOURS for b in COLOURS), cut_squares)
    return {
        "response_word": "".join(map(str, RESPONSE_WORD)),
        "cap_word_family": ["".join(map(str, cap_word(a, b)))
                            for a in COLOURS for b in COLOURS],
        "common_physical_pair": [P, QSITE],
        "common_direct_free_pair": list(DIRECT_FREE_EDGE),
        "common_internal_word": "".join(map(str, CAP_INTERNAL_WORD)),
        "coordinate_word_map_rank": 9,
        "complete_matching_term_maps": len(all_targets),
        "direct_free_parent_term_maps": direct_free_term_maps,
        "changed_site_count_histogram": dict(changed_site_histogram),
        "common_internal_tail_checks": common_tail_checks,
        "remote_cofactor_reinsertion_squares": remote_cofactor_squares,
        "q23_squares_per_coordinate": 15,
        "q45_squares_per_coordinate": 12,
        "target_safe": True,
        "physical_interpretation": (
            "the direct sum over words 012112ab is the nine-coordinate "
            "endpoint-polarized evaluation K=sum_ab K_ab E_ab"
        ),
    }


def marked_collision_naturality_audit(p2):
    coordinate_records = []
    total_trigger_squares = 0
    total_deleted_faces = 0
    total_order_histogram = Counter()
    for a in COLOURS:
        for b in COLOURS:
            word = cap_word(a, b)
            root = SimpleNamespace(
                RESPONSE_WORD=RESPONSE_WORD,
                CAP_WORD=word,
                SITES=SITES,
                DIRECT_FREE_EDGE=DIRECT_FREE_EDGE,
                perfect_matchings=perfect_matchings,
                decorated_monomial=decorated_monomial,
            )
            record = p2.trigger_dependent_divided_naturality_audit(root)
            require(record["parent_to_collision_trigger_squares"] == 540
                    and record["marked_P3K2_deletion_faces"] == 1080
                    and record["trigger_commutator_on_every_parent_branch"] == 0,
                    (a, b, record))
            total_trigger_squares += record[
                "parent_to_collision_trigger_squares"]
            total_deleted_faces += record["marked_P3K2_deletion_faces"]
            total_order_histogram.update({
                int(order): count for order, count in
                record["branch_total_divided_root_order_histogram"].items()
            })
            coordinate_records.append({
                "coordinate": f"K_{a}{b}",
                "word": "".join(map(str, word)),
                "changed_sites": [site for site, values in enumerate(zip(
                    RESPONSE_WORD, word, strict=True))
                                  if values[0] != values[1]],
                "trigger_squares": 540,
                "marked_deleted_faces": 1080,
            })
    require(total_trigger_squares == 4860
            and total_deleted_faces == 9720,
            (total_trigger_squares, total_deleted_faces))
    return {
        "coordinate_records": coordinate_records,
        "all_coordinate_trigger_squares": total_trigger_squares,
        "all_coordinate_marked_P3K2_faces": total_deleted_faces,
        "aggregate_divided_root_order_histogram":
            dict(sorted(total_order_histogram.items())),
        "common_parent_missing_site_fine_repeated_carrier": True,
        "coefficient_on_every_branch_and_face": 1,
        "conclusion": (
            "the other eight endpoint coefficients require no new collision "
            "constructor; they are the endpoint-colour polarizations of the "
            "same divided-root natural transformation"
        ),
    }


def poly_add(left, right):
    answer = Counter(left)
    answer.update(right)
    return Counter({term: value for term, value in answer.items() if value})


def poly_scale(scalar, value):
    return Counter({term: scalar * coefficient
                    for term, coefficient in value.items()
                    if scalar * coefficient})


def poly_multiply(left, right):
    answer = Counter()
    for (left_lambda, left_atoms), left_coefficient in left.items():
        for (right_lambda, right_atoms), right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(
                left_lambda, right_lambda, strict=True))
            atoms = tuple(sorted(left_atoms + right_atoms))
            answer[(exponent, atoms)] += left_coefficient * right_coefficient
    return Counter({term: value for term, value in answer.items() if value})


def linear_symbol(kind: str):
    answer = Counter()
    for colour in COLOURS:
        exponent = tuple(Q(index == colour) for index in COLOURS)
        answer[(exponent, (f"{kind}{colour}",))] = Q(1)
    return answer


def diagonal_clean_polarization_audit():
    # At h=3, 6E(K)=3*s(K)*r(K)^2*x+r(K)^3.  Expand for
    # K=lambda_0 E00+lambda_1 E11+lambda_2 E22 using independent formal
    # symbols s_i and r_i.  Coordinatewise cleanliness controls only the
    # three pure cubes; the remaining seven lambda monomials are independent
    # cross-colour conditions.
    scalar = linear_symbol("s")
    response = linear_symbol("r")
    x = Counter({((Q(0), Q(0), Q(0)), ("x",)): Q(1)})
    sr2x = poly_multiply(poly_multiply(poly_multiply(
        scalar, response), response), x)
    r3 = poly_multiply(poly_multiply(response, response), response)
    error6 = poly_add(poly_scale(Q(3), sr2x), r3)
    by_lambda = Counter()
    for (exponent, _atoms), coefficient in error6.items():
        by_lambda[exponent] += abs(coefficient)
    expected_exponents = {
        (Q(i), Q(j), Q(3 - i - j))
        for i in range(4) for j in range(4 - i)
    }
    require(set(by_lambda) == expected_exponents and len(by_lambda) == 10,
            by_lambda)
    pure = {(Q(3), Q(0), Q(0)), (Q(0), Q(3), Q(0)),
            (Q(0), Q(0), Q(3))}
    mixed = set(by_lambda) - pure
    require(len(mixed) == 7
            and (Q(1), Q(1), Q(1)) in mixed,
            mixed)

    # Pin the exact ordered i^2*j and triple coefficient formulas by an
    # independent combinatorial count in the expansion.
    for i in COLOURS:
        for j in COLOURS:
            if i == j:
                continue
            exponent = tuple(Q(2 if colour == i else 1 if colour == j else 0)
                             for colour in COLOURS)
            terms = {atoms: coefficient
                     for (power, atoms), coefficient in error6.items()
                     if power == exponent}
            wanted = {
                tuple(sorted((f"r{i}", f"r{i}", f"s{j}", "x"))): Q(3),
                tuple(sorted((f"r{i}", f"r{j}", f"s{i}", "x"))): Q(6),
                tuple(sorted((f"r{i}", f"r{i}", f"r{j}"))): Q(3),
            }
            require(terms == wanted, (i, j, terms, wanted))
    triple_terms = {atoms: coefficient
                    for (power, atoms), coefficient in error6.items()
                    if power == (Q(1), Q(1), Q(1))}
    wanted_triple = {
        tuple(sorted(("r1", "r2", "s0", "x"))): Q(6),
        tuple(sorted(("r0", "r2", "s1", "x"))): Q(6),
        tuple(sorted(("r0", "r1", "s2", "x"))): Q(6),
        tuple(sorted(("r0", "r1", "r2"))): Q(6),
    }
    require(triple_terms == wanted_triple,
            (triple_terms, wanted_triple))
    return {
        "diagonal_cap": "K=sum_c lambda_c E_cc",
        "activity_conditions": [
            "lambda_0*lambda_1*lambda_2 != 0",
            "s=sum_c lambda_c A_67[cc] != 0",
        ],
        "h3_clean_error": "6E(K)=3*s(K)*r(K)^2*x+r(K)^3",
        "diagonal_cubic_lambda_monomials": len(by_lambda),
        "coordinate_pure_cubics": 3,
        "new_mixed_polarization_conditions": 7,
        "mixed_types": [
            "six ordered lambda_i^2*lambda_j coefficients",
            "one lambda_0*lambda_1*lambda_2 coefficient",
        ],
        "first_exact_cross_colour_condition": (
            "the seven mixed polarizations of E must vanish; coordinatewise "
            "cleanliness of E_00,E_11,E_22 controls only the three pure cubes"
        ),
        "identity_completion": (
            "lambda=(1,1,1) gives K=I; activity is tr(A_67)!=0 and the "
            "remaining clean condition is E_67(I)=0"
        ),
    }


def grade_and_constructive_scope_audit():
    return {
        "same_literal_data_across_coordinates": [
            "physical pair 67",
            "direct-free pair 36",
            "matching parent and graph support",
            "missing-site/reinsertion mark",
            "P3+K2 repeated type",
            "q23/q45 operation pattern",
        ],
        "covariantly_varied_data": [
            "endpoint word 012112ab",
            "endpoint colour-fine entries",
            "endpoint root matrix units and their divided orders",
        ],
        "physical_total_word_family": (
            "the nine summands assemble canonically as an arbitrary cap "
            "covector once K_ab are supplied"
        ),
        "fixed_Gamma_star_warning": (
            "they do not become nine coordinates inside the single word "
            "01211222; collapsing the nine word grades would be a new "
            "non-conservative operation"
        ),
        "constructive_consequence": (
            "common pair/fine-support compatibility does not block the 9D "
            "evaluation.  What remains is selection of coefficients K_ab "
            "satisfying activity and the nonlinear clean equations"
        ),
        "terminal_consequence": (
            "a single-Gamma Fredholm terminal still sees only K_22 unless "
            "its row functor is enlarged to the endpoint-polarized word sum"
        ),
    }


def audit():
    pin_dependencies()
    p2 = load(
        "computations/verify_h3_six_root_marked_collision_p2_restriction_reinsertion.py",
        "endpoint_polarized_p2",
    )
    ledger = {
        "theorem": (
            "endpoint-colour polarization of the marked collision section "
            "constructs all nine physical cap-coordinate evaluations on a "
            "common pair, matching support and marked P2 carrier.  The first "
            "cross-colour obstruction is nonlinear: seven mixed cubic clean-"
            "error polarizations, plus activity nonvanishing, are not implied "
            "by the nine linear coordinate maps"
        ),
        "pins": PINS,
        "nine_coordinate_word_family":
            nine_coordinate_word_and_support_audit(),
        "marked_collision_naturality": marked_collision_naturality_audit(p2),
        "diagonal_clean_cross_colour_gate":
            diagonal_clean_polarization_audit(),
        "grade_and_constructive_scope": grade_and_constructive_scope_audit(),
        "scope": (
            "exact rational h=3 endpoint-polarized word family, all 945 "
            "complete matching maps, 810 direct-free parents, 4,860 marked "
            "trigger squares, 9,720 P3+K2 faces and all q23/q45 cofactor "
            "squares.  It constructs evaluation natural in a supplied K; it "
            "does not select K or prove activity/cleanliness"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="full")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger changed", digest, EXPECTED_LEDGER_SHA256))
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "ledger_sha256": digest}, indent=2, sort_keys=True))
    else:
        print("h3 endpoint-polarized cap evaluation: LINEAR 9D YES")
        print("mode", arguments.mode)
        print("nine coordinate word/root/collision maps: CONSTRUCTED")
        print("common pair/support/P2 compatibility: PASS")
        print("first cross-colour gate: 7 mixed cubic clean polarizations")
        print("active clean K selected: NO")
        print("ledger_sha256", digest)


if __name__ == "__main__":
    main()

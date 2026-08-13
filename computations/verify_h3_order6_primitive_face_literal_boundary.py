#!/usr/bin/env python3
"""Audit the literal polynomial output of the primitive order-six face.

The order-six secondary class has symbolic pair face

    07:11 wedge 24:11.

This checker removes those two directions from every selected sixth-order
operator, applies the remaining four derivatives to each of the three
quadratic source products, and retains the quadratic coefficient.  The
result is the actual fourth-derivative polynomial face, rather than its
sixteen-coordinate Hasse symbol.

For each fine degree, every possible old physical source boundary of the
same site profile is a complete eight-site row multiplied by a decorated
two-edge perfect matching on the doubled sites.  The checker enumerates all
such columns.  Each of the three primitive outputs has a monomial absent
from every compatible old column, so none is in their span.  Thus the
primitive order-six face genuinely requires the relative/bar comparison;
it is not a disguised old ninety-term correction column.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "computations/verify_h3_residual_q_order6_complete_hasse_incidence.py":
        "164d67345fe7a83d0ace581ba4417b31e3166dc5a88e487bd5ee6f2a15e5c824",
    "computations/verify_h3_residual_q_order5_generator_repair.py":
        "f4b338f557729313fa70da78caec17de861738275b89e7dc9dc97d7e2ae83267",
    "computations/verify_h3_residual_q_covariance_curvature_commutator.py":
        "46a3b6595ab147a17e80908157571a33b61e7faed32deb996506068e206baee9",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}
EXPECTED_LEDGER_SHA256 = "b19c30d4d54a08c920dd53bc37e17606f4d6f29057aa89057e71f7c7d8c5e0df"
PRIMITIVE_PAIR = ((0, 7, 1, 1), (2, 4, 1, 1))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load(relative: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(spec is not None and spec.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def oriented_edge(left: int, right: int, a: int, b: int):
    if left < right:
        return left, right, a, b
    return right, left, b, a


def matchings(sites: tuple[int, int, int, int]):
    a, b, c, d = sorted(sites)
    return (
        ((a, b), (c, d)),
        ((a, c), (b, d)),
        ((a, d), (b, c)),
    )


def degrees(monomial):
    site = [0] * 8
    colour = [0] * 24
    for left, right, a, b in monomial:
        site[left] += 1
        site[right] += 1
        colour[3 * left + a] += 1
        colour[3 * right + b] += 1
    return tuple(site), tuple(colour)


def compatible_old_columns(base, site_degree, colour_degree):
    doubled = tuple(site for site, value in enumerate(site_degree)
                    if value == 2)
    require(len(doubled) == 4
            and all(value in (1, 2) for value in site_degree),
            ("unexpected primitive site profile", site_degree))
    columns = []
    labels = []
    for matching in matchings(doubled):
        for decorations in product(range(3), repeat=4):
            by_site = dict(zip(doubled, decorations, strict=True))
            multiplier = tuple(sorted(
                oriented_edge(left, right, by_site[left], by_site[right])
                for left, right in matching
            ))
            remainder = list(colour_degree)
            for left, right, a, b in multiplier:
                remainder[3 * left + a] -= 1
                remainder[3 * right + b] -= 1
            if any(value < 0 for value in remainder):
                continue
            word = []
            for site in range(8):
                local = remainder[3 * site:3 * site + 3]
                if sum(local) != 1 or any(value not in (0, 1)
                                           for value in local):
                    break
                word.append(local.index(1))
            else:
                word = tuple(word)
                column = frozenset(
                    tuple(sorted(multiplier + term))
                    for term in base.full_row(word)
                )
                columns.append(column)
                labels.append((word, multiplier))
    return columns, labels


def exact_solution_context():
    """Reconstruct the order-six solution and retain its existing system.

    The upstream helper returns only the 188 terms and then this checker used
    to rebuild all three quadratic products.  On constrained runners that
    needlessly doubles the peak allocator footprint.  This generator-level
    replay performs the exact same solve once and returns the already-built
    source system for the literal-face audit.
    """
    order6 = load(
        "computations/verify_h3_residual_q_order6_missing_face_probe.py",
        "primitive_literal_order6",
    )
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "primitive_literal_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "primitive_literal_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "primitive_literal_base",
    )
    system = repair.build_system(base, commutator)
    derivatives = order6.build_exact_sixth_derivatives(system)
    missing = frozenset(PRIMITIVE_PAIR)
    metadata = set()
    for _product, directions in derivatives:
        if not missing.issubset(directions):
            continue
        for coefficient in order6.eligible_coefficients(
                repair, commutator, directions):
            metadata.add((coefficient, directions))

    columns = []
    for coefficient, directions in sorted(metadata, key=repr):
        column = Counter()
        for product_index in range(3):
            for remainder, value in derivatives.get(
                    (product_index, directions), {}).items():
                column[(product_index,
                        tuple(sorted(remainder + coefficient)))] += value
        shadow = {row: value for row, value in column.items() if value}
        for left, right in combinations(range(6), 2):
            pair = tuple(sorted((directions[left], directions[right])))
            shadow[(3, pair)] = shadow.get((3, pair), 0) + 1
        columns.append(((coefficient, directions), shadow))
    basis = repair.select_modular_basis(columns)
    target = {(3, pair): int(value) for pair, value in
              commutator.expected_second_shadow().items()}
    solution, picked = repair.exact_solution(columns, basis, target)
    terms = [(weight, picked[index][0], picked[index][1])
             for index, weight in solution.items()]
    require(len(terms) == 188, "the exact order-six solution changed")
    return (terms, commutator.expected_second_shadow(), repair, base, system)


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual))

    terms, pair_shadow, repair, base, system = exact_solution_context()
    require(pair_shadow[tuple(sorted(PRIMITIVE_PAIR))] == 1,
            "the primitive symbolic face coefficient changed")

    records = []
    expected_supports = (167, 343, 191)
    expected_l1 = (Q(3272, 3), Q(3029, 3), Q(950))
    expected_fine_counts = (1, 2, 1)
    # The mixed product has two fine degrees.  They contribute six and three
    # compatible columns, respectively, and must not be collapsed merely
    # because their undecorated two-edge matchings coincide.
    expected_candidate_counts = (3, 9, 6)
    for product_index, source_product in enumerate(system["products"]):
        output = Counter()
        for weight, coefficient, directions in terms:
            remaining = list(directions)
            for selected in PRIMITIVE_PAIR:
                require(selected in remaining,
                        ("solution term lost primitive face", selected))
                remaining.remove(selected)
            require(len(remaining) == 4,
                    "primitive face stopped leaving four derivatives")
            for tail, value in repair.derivatives(
                    source_product, tuple(remaining)).items():
                output[tuple(sorted(coefficient + tail))] += weight * value
        # Counter.__pos__ discards negative entries as well as zeros.  The
        # primitive polynomial is signed, so filter only actual zeros.
        output = Counter({monomial: value for monomial, value in output.items()
                          if value})
        require(len(output) == expected_supports[product_index]
                and sum(abs(value) for value in output.values())
                == expected_l1[product_index],
                ("primitive literal output changed", product_index))

        by_degree = {}
        for monomial in output:
            key = degrees(monomial)
            by_degree.setdefault(key, []).append(monomial)
        require(len(by_degree) == expected_fine_counts[product_index],
                ("primitive fine-degree count changed", product_index))

        all_columns = []
        all_labels = []
        for (site_degree, colour_degree), _monomials in by_degree.items():
            columns, labels = compatible_old_columns(
                base, site_degree, colour_degree)
            all_columns.extend(columns)
            all_labels.extend(labels)
        require(len(all_columns) == expected_candidate_counts[product_index],
                ("compatible old-column count changed", product_index))
        covered = set().union(*all_columns) if all_columns else set()
        private = sorted(
            (monomial for monomial in output if monomial not in covered),
            key=repr,
        )
        require(private,
                ("primitive face entered the old full-row span", product_index))
        first = private[0]
        records.append({
            "source_product": product_index,
            "literal_support": len(output),
            "literal_l1": str(sum(abs(value) for value in output.values())),
            "fine_degrees": len(by_degree),
            "site_profiles": [
                list(site_degree)
                for site_degree in sorted({
                    site_degree for site_degree, _colour_degree in by_degree
                })
            ],
            "compatible_full_row_times_two_edge_columns": len(all_columns),
            "private_monomials": len(private),
            "first_private_monomial": repr(first),
            "first_private_coefficient": str(output[first]),
            "in_compatible_old_span": False,
        })

    ledger = {
        "theorem": "literal primitive order-six face boundary",
        "primitive_pair": [list(cell) for cell in PRIMITIVE_PAIR],
        "symbolic_pair_coefficient": "1",
        "records": records,
        "conclusion": (
            "the primitive order-six Hasse symbol does not directly equal "
            "an old physical correction column; its actual fourth-derivative "
            "outputs have private monomials outside every compatible complete "
            "source-row times two-edge multiplier column"
        ),
        "proof_frontier": (
            "retain the primitive face in the canonical relative/bar cone; "
            "do not identify it with the repeated-grade mapping-cone boundary "
            "without the source-typed comparison"
        ),
        "scope": (
            "the exact selected 188-term order-six representative and its "
            "common primitive pair on the three quadratic source products; "
            "this does not exclude a higher relative boundary or the dual "
            "separator branch in the exhaustive cone"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("primitive literal ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("h3 order-six primitive literal face: SHARP RELATIVE BOUNDARY")
    print("supports=" + ",".join(
        str(record["literal_support"]) for record in ledger["records"]
    ))
    print("old full-row multiplier membership=NO on all three products")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

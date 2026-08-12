#!/usr/bin/env python3
"""Audit the top multiaffine (three-new-cell) E14 support layer.

For h=3, a response coefficient contains at most two internal q cells and a
unary coefficient contains at most three.  Instead of rebuilding every
three-cell specialization, this checker records, for every possible complete
row comparison, the antichain of candidate-cell supports on which its defect
is nonzero.  A comparison is an identity on a triple T exactly when none of
its defect supports is contained in T.

Every triple is closed by a literal two-row unit.  This does *not* by itself
give a full-support unit: the witness changes with T, and the universal G11
target contains target-private monomials absent from every G11 zero row.  The
checker freezes both the top-degree closure and this exact gluing boundary.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TWO_CELL_PATH = "computations/verify_h3_c6_e14_two_cell_unit_frontier.py"
PINS = {
    TWO_CELL_PATH:
        "b5a2609b64f5a0bf1720a3c571c6c4d28aa316df00129f5b4574e0f32b8c3971",
    "notes/h3-c6-e14-two-cell-unit-frontier.md":
        "07593c3ebeb95b76461792c9835810f2b81e2b2ba701a9c910ea75c2b63809f1",
}
EXPECTED_LEDGER_SHA256 = (
    "4a12d1fde5028d591e8f8fc19425ade2cb30016472dd1d1554d254fcd23de221"
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


def subtract(left, right, sign):
    answer = defaultdict(Q, left)
    for monomial, coefficient in right.items():
        answer[monomial] -= sign * coefficient
    return {monomial: coefficient
            for monomial, coefficient in answer.items() if coefficient}


def support_antichain(supports):
    supports = set(supports)
    return tuple(sorted(
        (support for support in supports
         if not any(smaller < support for smaller in supports)),
        key=lambda support: (len(support), tuple(sorted(support))),
    ))


def polynomial_defect_supports(left, right, sign, candidate_names):
    return support_antichain(
        frozenset(set(monomial) & candidate_names)
        for monomial in subtract(left, right, sign)
    )


def row_defect_supports(left, right, sign, candidate_names):
    supports = []
    for endpoint in set(left) | set(right):
        supports.extend(
            frozenset(set(monomial) & candidate_names)
            for monomial in subtract(
                left.get(endpoint, {}), right.get(endpoint, {}), sign
            )
        )
    return support_antichain(supports)


def comparison_family(rows, target_word, candidate_names, row_valued):
    target = rows[target_word]
    family = []
    for word, candidate in rows.items():
        if word == target_word:
            continue
        for sign in (1, -1):
            if row_valued:
                supports = row_defect_supports(
                    candidate, target, sign, candidate_names
                )
            else:
                supports = polynomial_defect_supports(
                    candidate, target, sign, candidate_names
                )
            # An empty support means the comparison already differs on the
            # base chart, so it can never become an identity by restricting
            # candidate cells.
            if frozenset() not in supports:
                family.append((word, sign, supports))
    return tuple(family)


def polynomial_candidate_degree(polynomial, candidate_names):
    return max((len(set(monomial) & candidate_names)
                for monomial in polynomial), default=0)


def row_candidate_degree(row, candidate_names):
    return max((polynomial_candidate_degree(polynomial, candidate_names)
                for polynomial in row.values()), default=0)


def response_monomials(row):
    return {
        (endpoint, monomial)
        for endpoint, polynomial in row.items()
        for monomial in polynomial
    }


def audit():
    pin_dependencies()
    two = load(TWO_CELL_PATH, "e14_three_cell_two")
    e14 = two.load(two.E14_PATH, "e14_three_cell_base")
    b4 = e14.load(e14.B4_PATH, "e14_three_cell_b4")

    chart_records = {}
    tier_counts = Counter()
    classification_hash = sha256()
    total = 0
    universal_identity_count = 0

    for first_index in (1, 2, 3):
        for second_index in (1, 2, 3):
            candidates, names, responses, unary = two.universal(
                e14, b4, first_index, second_index
            )

            response_degree = max(
                row_candidate_degree(row, names)
                for row in responses.values()
            )
            unary_degree = max(
                polynomial_candidate_degree(row, names)
                for row in unary.values()
            )
            require(response_degree <= 2,
                    "an h=3 response row exceeded internal degree two")
            require(unary_degree <= 3,
                    "an h=3 unary row exceeded internal degree three")

            families = (
                ("G11", comparison_family(
                    responses, (1,) * 6, names, True)),
                ("unary", comparison_family(
                    unary, (0,) * 6, names, False)),
                ("G22", comparison_family(
                    responses, (2,) * 6, names, True)),
            )
            universal_identity_count += sum(
                1 for _tier, family in families
                for _word, _sign, supports in family if not supports
            )

            modes = Counter()
            for triple in combinations(candidates, 3):
                allowed = frozenset(item[1] for item in triple)
                witness = None
                for tier, family in families:
                    for word, sign, defect_supports in family:
                        if all(not support <= allowed
                               for support in defect_supports):
                            witness = (tier, word, sign)
                            break
                    if witness is not None:
                        break
                require(witness is not None,
                        f"three-cell survivor in chart "
                        f"{(first_index, second_index)}: {triple}")
                tier, word, sign = witness
                modes[tier] += 1
                tier_counts[tier] += 1
                total += 1
                cells = tuple(item[0] for item in triple)
                classification_hash.update(
                    (f"{first_index},{second_index};{cells};{tier};"
                     f"{''.join(map(str, word))};{sign}\n").encode()
                )

            target = response_monomials(responses[(1,) * 6])
            zero_union = set().union(*(
                response_monomials(row)
                for word, row in responses.items() if word != (1,) * 6
            ))
            private = target - zero_union
            require(private,
                    "the universal G11 target lost its private monomials")
            private_degrees = sorted({
                len(set(monomial) & names)
                for _endpoint, monomial in private
            })
            require(private_degrees == [1, 2],
                    "the target-private degree boundary changed")

            count = len(candidates) * (len(candidates) - 1) * (
                len(candidates) - 2
            ) // 6
            require(sum(modes.values()) == count,
                    "the chart triple count changed")
            first_private = min(private)
            chart_records[f"{first_index},{second_index}"] = {
                "candidate_cell_count": len(candidates),
                "triple_count": count,
                "tier_counts": dict(sorted(modes.items())),
                "response_candidate_degree": response_degree,
                "unary_candidate_degree": unary_degree,
                "admissible_comparison_count": sum(
                    len(family) for _tier, family in families
                ),
                "G11_target_private_monomial_count": len(private),
                "G11_target_private_candidate_degrees": private_degrees,
                "first_G11_target_private_monomial": [
                    list(first_private[0]), list(first_private[1])
                ],
            }

    require(total == 2_126_208,
            f"the top-degree triple universe changed: {total}")
    require(tier_counts == Counter({
        "G11": 1_962_267,
        "unary": 162_982,
        "G22": 959,
    }), f"the triple tier split changed: {tier_counts}")
    require(universal_identity_count == 0,
            "a universal two-row identity appeared")

    ledger = {
        "pins": PINS,
        "chart_records": chart_records,
        "three_cell_extension_count": total,
        "ordinary_two_row_unit_count": total,
        "tier_counts": dict(sorted(tier_counts.items())),
        "classification_stream_sha256": classification_hash.hexdigest(),
        "universal_two_row_identity_count": universal_identity_count,
        "theorem": (
            "all 2,126,208 unordered three-new-internal-cell "
            "specializations of the nine minimal E14 charts have a literal "
            "ordinary two-row unit; this is the final internal monomial "
            "degree because response rows have degree at most two and unary "
            "rows degree at most three"
        ),
        "promotion_boundary": (
            "the witness depends on the chosen triple.  In every universal "
            "chart the G11 target has 24 or 26 endpoint/q monomials absent "
            "from every G11 zero row, already in candidate degrees one and "
            "two.  Thus degree <=3 exhausts monomial types but does not glue "
            "the support-specific units into a constant-coefficient "
            "full-support identity"
        ),
        "minimal_missing_input": (
            "a source-valid triangular/standard-basis or Rees landing that "
            "eliminates the target-private monomials while preserving the "
            "target constant; multiaffine degree alone is insufficient"
        ),
        "scope": (
            "exact for triples of new internal q cells on the nine canonical "
            "minimal E14 charts with complete core response and unary rows. "
            "It is not arbitrary-simultaneous-cell emptiness, a full-source "
            "counterexample, or a theorem about outside-core endpoints"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"three-cell top-degree ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 C6 E14 three-cell top-degree boundary: PASS (exact)")
    print(f"triples={ledger['three_cell_extension_count']}")
    print(f"tiers={ledger['tier_counts']}")
    print("universal_two_row_identity_count="
          f"{ledger['universal_two_row_identity_count']}")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()

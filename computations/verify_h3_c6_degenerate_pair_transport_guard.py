#!/usr/bin/env python3
"""Exact support-degenerate boundary of the canonical C6 transgression.

The dense odd-holonomy certificate of 3836903 uses eight unary matching
classes at z=012111.  The three selected response rows and the unary row
split them into four signed pairs.  M and N are selected, so two pairs are
always occupied.  This checker classifies the remaining two pair supports,
verifies the unique toric dependency, and source-types the only positive
transport: the Q2/Q5 pair contains q13:11 and hence the literal C4 chord of
the complete response packet.  The Q3/Q6 pair instead contains q14:11 and
is response-visible only after a genuine hole-14 endpoint companion exists.

The checker also records the exact contamination identity for the two-row
unit of 7320475.  Proportional extra tails preserve the unit.  Otherwise the
normalized target/zero difference is a nonzero source-labelled polynomial;
at a source point at least one of its literal matching terms is occupied.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_c6_dense_bright_spoke_hole_odd_holonomy.py":
        "580819325ea918cb8ecda6590cb9b50d403542bd0cbee9d9b39236d81edd8b39",
    "notes/h3-c6-dense-bright-spoke-hole-odd-holonomy.md":
        "bca9977dbac7ab5a5fa1da86008b2a29cfd5a88485583532dfa89937ba02f04f",
    "computations/verify_h3_silent_c6_full_core_port_unit.py":
        "2b757f57d92722363f340b2a6105b82e091fc083726e1277569056e8a2ddf56a",
    "notes/h3-silent-c6-full-core-port-unit.md":
        "b16c29d16133e1c00cf58b8ee9305a9c53044fd127b3146b709728275157ff08",
    "computations/verify_h3_four_base_silent_c6_response_lock.py":
        "dc4daa2d200f184b5d00d29c4db175320935a189f5590836afa0c724d3fdac8a",
    "notes/h3-four-base-silent-c6-response-lock.md":
        "54d7278e49e8195ed2262fa37cc89936f718b3bcd192884c6473c736a68354b8",
    "computations/verify_h3_c6_endpoint_visibility_augmented_map_gate.py":
        "589d88020b87c5892be832758c74c73832747c265f4139b6917069685dcd9375",
    "notes/h3-c6-endpoint-visibility-augmented-map-gate.md":
        "e9cf5650023588c7a94b37b98912898cc5120dab9968c2d860a72dce60faa48e",
}
EXPECTED_LEDGER_SHA256 = (
    "06224f08840a7c1211c47fd59efecf18e05787813af4f0252bdc1229d88d0e4e"
)

Z = (0, 1, 2, 1, 1, 1)
MATCHINGS = {
    "M": ((0, 1), (2, 3), (4, 5)),
    "N": ((0, 5), (1, 2), (3, 4)),
    "Q1": ((0, 1), (2, 4), (3, 5)),
    "Q2": ((0, 2), (1, 3), (4, 5)),
    "Q3": ((0, 2), (1, 4), (3, 5)),
    "Q4": ((0, 2), (1, 5), (3, 4)),
    "Q5": ((0, 5), (1, 3), (2, 4)),
    "Q6": ((0, 5), (1, 4), (2, 3)),
}
SIGNED_PAIRS = (
    ("E01", "M", "Q1"),
    ("E13", "Q2", "Q5"),
    ("E34", "N", "Q4"),
    ("E14", "Q3", "Q6"),
)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def cell(physical):
    left, right = physical
    return physical, (Z[left], Z[right])


def decorated(name):
    return tuple(cell(physical) for physical in MATCHINGS[name])


def exponent_counter(names):
    answer = Counter()
    for name in names:
        answer.update(decorated(name))
    return answer


def is_c4(left, right):
    return len(set(MATCHINGS[left]) ^ set(MATCHINGS[right])) == 4


def components(names):
    unseen = set(names)
    answer = []
    while unseen:
        seed = min(unseen)
        todo = [seed]
        component = set()
        while todo:
            current = todo.pop()
            if current in component:
                continue
            component.add(current)
            unseen.discard(current)
            todo.extend(other for other in names
                        if other not in component and is_c4(current, other))
        answer.append(tuple(sorted(component)))
    return tuple(sorted(answer))


def monomial_value(name, values):
    value = Q(1)
    for item in decorated(name):
        value *= values[item]
    return value


def rational_guards():
    # The four-pair core.  M=1,Q1=-1 and N=1,Q4=-1.
    core_values = {
        cell((0, 1)): Q(1),
        cell((2, 3)): Q(1),
        cell((4, 5)): Q(1),
        cell((2, 4)): Q(-1),
        cell((3, 5)): Q(1),
        cell((0, 5)): Q(1),
        cell((1, 2)): Q(1),
        cell((3, 4)): Q(1),
        cell((0, 2)): Q(1),
        cell((1, 5)): Q(-1),
    }
    core = {name: monomial_value(name, core_values)
            for name in ("M", "Q1", "N", "Q4")}
    require(core == {"M": Q(1), "Q1": Q(-1),
                     "N": Q(1), "Q4": Q(-1)},
            f"the four-class rational guard changed: {core}")

    # A six-class response-silent E14 guard.  Adjust the shared M tail by
    # two signs, and add q14:11, so Q3=1,Q6=-1 while the core equations stay.
    e14_values = dict(core_values)
    e14_values[cell((2, 3))] = Q(-1)
    e14_values[cell((4, 5))] = Q(-1)
    e14_values[cell((1, 4))] = Q(1)
    e14 = {name: monomial_value(name, e14_values)
           for name in ("M", "Q1", "N", "Q4", "Q3", "Q6")}
    require(e14 == {"M": Q(1), "Q1": Q(-1),
                    "N": Q(1), "Q4": Q(-1),
                    "Q3": Q(1), "Q6": Q(-1)},
            f"the E14 rational guard changed: {e14}")
    return {
        "four_class": {name: str(value) for name, value in core.items()},
        "six_class_E14": {name: str(value) for name, value in e14.items()},
    }


def audit_pair_supports():
    # The exact toric dependency underlying 3836903.
    require(exponent_counter(("Q1", "Q2", "Q6"))
            == exponent_counter(("M", "Q3", "Q5")),
            "the dense C6 toric dependency changed")

    # M,N are selected units.  Each binomial pair therefore has either both
    # entries occupied or neither.  E01 and E34 are mandatory.  Both optional
    # pairs are impossible by the odd sign in the toric dependency.
    records = []
    for has_e13 in (False, True):
        for has_e14 in (False, True):
            support = {"M", "Q1", "N", "Q4"}
            if has_e13:
                support.update(("Q2", "Q5"))
            if has_e14:
                support.update(("Q3", "Q6"))
            dense_unit = has_e13 and has_e14
            records.append({
                "E13_pair": has_e13,
                "E14_pair": has_e14,
                "support": sorted(support),
                "matching_C4_components": [list(item)
                                             for item in components(support)],
                "dense_odd_holonomy_unit": dense_unit,
                "survives_pair_level": not dense_unit,
            })
    require(sum(record["survives_pair_level"] for record in records) == 3,
            "the degenerate support trichotomy changed")

    minimal = next(record for record in records
                   if not record["E13_pair"] and not record["E14_pair"])
    require(minimal["matching_C4_components"]
            == [["M", "Q1"], ["N", "Q4"]],
            "the minimal guard stopped being two disconnected C4s")

    e13 = next(record for record in records
               if record["E13_pair"] and not record["E14_pair"])
    require(len(e13["matching_C4_components"]) == 1,
            "the E13 pair stopped joining the matching graph")
    require(set(decorated("Q2")) & set(decorated("Q5"))
            == {cell((1, 3))},
            "the E13 pair lost its common q13:11 chord")

    e14 = next(record for record in records
               if record["E14_pair"] and not record["E13_pair"])
    require(len(e14["matching_C4_components"]) == 1,
            "the E14 pair stopped joining the matching graph")
    require(set(decorated("Q3")) & set(decorated("Q6"))
            == {cell((1, 4))},
            "the E14 pair lost its common q14:11 edge")
    return records


def audit_hole14_companion():
    # A literal G11[z] endpoint hole 14 leaves sites 0,2,3,5.  Its three
    # residual tails are Q3/q14, Q6/q14, and the sole third matching.
    remainder = (0, 2, 3, 5)
    tails = (
        ((0, 2), (3, 5)),
        ((0, 3), (2, 5)),
        ((0, 5), (2, 3)),
    )
    require(set(tails) == {
        tuple(edge for edge in MATCHINGS["Q3"] if edge != (1, 4)),
        tuple(edge for edge in MATCHINGS["Q6"] if edge != (1, 4)),
        ((0, 3), (2, 5)),
    }, "the hole-14 companion tails changed")
    return {
        "row": "G11[012111]",
        "ordered_hole": [1, 4],
        "required_endpoint_product": (
            "p1_1:1*s1_4:1 or p1_4:1*s1_1:1"
        ),
        "common_internal_cell": "q14:11",
        "retained_tails": ["Q3/q14", "Q6/q14"],
        "third_tail": "q03:01*q25:21",
        "consequence": (
            "a nonzero hole-14 endpoint product makes the E14 pair a literal "
            "response column; without it the connected matching graph is "
            "still response-silent and is a genuine spoke-to-hole guard"
        ),
        "remainder_sites": list(remainder),
    }


def add(left, right, scale=Q(1)):
    answer = dict(left)
    for monomial, coefficient in right.items():
        answer[monomial] = answer.get(monomial, Q(0)) + scale * coefficient
        if not answer[monomial]:
            del answer[monomial]
    return answer


def scale(polynomial, scalar):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items() if coefficient}


def audit_unit_contamination():
    # F_t=aP+A-1 and F_z=bP+B.  The source-row combination normalized to
    # unit constant is (a/b)F_z-F_t=1+(a/b)B-A.  Equivalently, dividing
    # by a gives b^-1 F_z-a^-1 F_t=1/a+B/b-A/a.  The first form avoids the
    # easy normalization mistake of calling the latter constant one.
    a, b = Q(2), Q(-3)
    p = {"u": Q(5), "v": Q(-2)}
    contamination_target = {"r": Q(7), "s": Q(1)}
    contamination_zero = {"r": Q(-6), "t": Q(4)}
    target = add(scale(p, a), contamination_target)
    target = add(target, {"1": Q(-1)})
    zero = add(scale(p, b), contamination_zero)
    combination = add(scale(zero, a / b), target, scale=Q(-1))
    expected = add({"1": Q(1)},
                   add(scale(contamination_zero, a / b),
                       contamination_target, scale=Q(-1)))
    require(combination == expected,
            "the normalized contamination identity changed")

    proportional_zero = scale(contamination_target, b / a)
    proportional = add({"1": Q(1)},
                       add(scale(proportional_zero, a / b),
                           contamination_target, scale=Q(-1)))
    require(proportional == {"1": Q(1)},
            "proportional contamination stopped preserving the unit")
    return {
        "identity": (
            "(a/b)*F_zero-F_target="
            "1+(a/b)*Delta_zero-Delta_target"
        ),
        "proportional_case": (
            "Delta_zero/b=Delta_target/a preserves the ordinary unit"
        ),
        "asymmetric_case": (
            "at a source zero the normalized contamination difference "
            "equals -1, hence contains a nonzero literal matching term; "
            "this is a typed internal-tail/endpoint source edge, not yet "
            "an automatic rank-three landing"
        ),
        "sample_difference_terms": {
            monomial: str(coefficient)
            for monomial, coefficient in sorted(expected.items())
        },
    }


def audit():
    pin_dependencies()
    records = audit_pair_supports()
    ledger = {
        "pins": PINS,
        "word": "".join(map(str, Z)),
        "matching_classes": {
            name: [f"{left}{right}:{Z[left]}{Z[right]}"
                   for left, right in matching]
            for name, matching in MATCHINGS.items()
        },
        "signed_source_pairs": [list(item) for item in SIGNED_PAIRS],
        "support_strata": records,
        "rational_pair_level_guards": rational_guards(),
        "hole13_transport": {
            "pair": ["Q2", "Q5"],
            "common_cell": "q13:11",
            "literal_source_row": "G21[012211]",
            "landing": (
                "the decorated q13 chord is the typed two-C4 response "
                "bridge of the pinned silent-C6 response-lock theorem"
            ),
        },
        "hole14_guard": audit_hole14_companion(),
        "two_row_unit_contamination": audit_unit_contamination(),
        "theorem": (
            "with selected M,N nonzero, the four normalized source pairs "
            "have exactly three support-degenerate strata after the dense "
            "odd-holonomy unit is removed.  The E13 stratum has a literal "
            "q13:11 typed response chord.  The minimal four-class stratum "
            "is two disconnected flat C4s.  The remaining six-class E14 "
            "stratum is connected but response-silent until a genuine "
            "hole-14 endpoint companion is present"
        ),
        "scope": (
            "exact Laurent matching-class and literal row typing for the "
            "canonical h=3 C6 first transgression.  The two displayed "
            "rational assignments are coefficient-level guards, not full "
            "one-bad source points.  No support deletion is claimed for "
            "the response-silent E14 pair because other full-source words "
            "may use its cells"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"degenerate C6 transport ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h3 degenerate C6 pair transport guard: PASS (exact)")
    print("dense support -> odd unit; E13 pair -> typed q13 response chord")
    print("residuals: two disconnected C4s or response-silent E14 pair")
    print("proportional unit contamination persists; asymmetry is typed")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()

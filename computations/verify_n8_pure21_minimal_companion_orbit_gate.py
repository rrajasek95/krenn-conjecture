#!/usr/bin/env python3
"""Classify and exclude every two-cell companion of the pure 21 leak.

The starting packet is the repaired mixed F_02/F_01 corner from
``verify_n8_f02_ps01_mate_pure_head_migration_gate.py``.  Its remaining
selected residue is the pure word 222222, head 21, PS matching
62|75|04|13.  This checker enumerates every DQ/PS term needing the minimum
number of new source cells, normalizes it to cancel that residue, replays all
6561 rows, and verifies explicit polynomial migration/unit identities.
"""

import argparse
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


PARENT_PATH = Path(__file__).with_name(
    "verify_n8_f02_ps01_mate_pure_head_migration_gate.py"
)
SPEC = spec_from_file_location("pure21_parent", PARENT_PATH)
require(SPEC is not None and SPEC.loader is not None, "could not load parent audit")
P = module_from_spec(SPEC)
SPEC.loader.exec_module(P)
B = P.B


PURE = (2,) * 6
U21 = P.PURE_LEAK_21
APROD = B.multiply(B.A0, B.multiply(B.A1, B.A2))


def var(name):
    return B.variable(name)


def monomial(*names):
    return B.product_polynomials(var(name) for name in names)


def matching_text(edges):
    return "|".join(f"{left}{right}" for left, right in sorted(edges))


# Each addition is (table, key, normalized value).  New values are inserted
# as constants for the exhaustive normalized source replay.
CANDIDATES = (
    {
        "name": "DQ25", "kind": "direct",
        "path": ("DQ", ((0, 4), (1, 3), (2, 5))),
        "adds": (("q", (2, 5, 2, 2), 1), ("d", (2, 1), 1)),
        "witness": ("222222", "01", "DQ", "67|04|13|25", 1),
        "residual_count": 9,
    },
    {
        "name": "REV25", "kind": "new_s1",
        "path": ("PS", 5, 2, ((0, 4), (1, 3))),
        "adds": (("p", (2, 5, 2), 1), ("s", (1, 2, 2), 1)),
        "witness": ("222221", "11", "PS", "04|13|65|72", 1),
        "residual_count": 8,
    },
    {
        "name": "S0_Q45", "kind": "new_s1",
        "path": ("PS", 2, 0, ((1, 3), (4, 5))),
        "adds": (("s", (1, 0, 2), 1), ("q", (4, 5, 2, 2), 1)),
        "witness": ("210011", "11", "PS", "14|23|65|70", 1),
        "residual_count": 9,
    },
    {
        "name": "S1_Q35", "kind": "new_s1",
        "path": ("PS", 2, 1, ((0, 4), (3, 5))),
        "adds": (("s", (1, 1, 2), 1), ("q", (3, 5, 2, 2), 1)),
        "witness": ("220021", "11", "PS", "04|23|65|71", 1),
        "residual_count": 9,
    },
    {
        "name": "S3_Q15", "kind": "new_s1",
        "path": ("PS", 2, 3, ((0, 4), (1, 5))),
        "adds": (("s", (1, 3, 2), 1), ("q", (1, 5, 2, 2), 1)),
        "witness": ("111211", "11", "PS", "02|14|65|73", 1),
        "residual_count": 9,
    },
    {
        "name": "S4_Q05", "kind": "new_s1",
        "path": ("PS", 2, 4, ((0, 5), (1, 3))),
        "adds": (("s", (1, 4, 2), 1), ("q", (0, 5, 2, 2), 1)),
        "witness": ("121221", "11", "PS", "02|13|65|74", 1),
        "residual_count": 9,
    },
    {
        "name": "P0_Q24", "kind": "anchor_shift",
        "path": ("PS", 0, 5, ((1, 3), (2, 4))),
        "adds": (("p", (2, 0, 2), 1), ("q", (2, 4, 2, 2), -1)),
        "witness": ("222222", "22", "PS", "13|24|60|75", -1),
        "residual_count": 8,
    },
    {
        "name": "P1_Q23", "kind": "anchor_shift",
        "path": ("PS", 1, 5, ((0, 4), (2, 3))),
        "adds": (("p", (2, 1, 2), 1), ("q", (2, 3, 2, 2), -1)),
        "witness": ("222222", "22", "PS", "04|23|61|75", -1),
        "residual_count": 10,
    },
    {
        "name": "P3_Q12", "kind": "anchor_shift",
        "path": ("PS", 3, 5, ((0, 4), (1, 2))),
        "adds": (("p", (2, 3, 2), 1), ("q", (1, 2, 2, 2), -1)),
        "witness": ("222222", "22", "PS", "04|12|63|75", -1),
        "residual_count": 10,
    },
    {
        "name": "P4_Q02", "kind": "anchor_shift",
        "path": ("PS", 4, 5, ((0, 2), (1, 3))),
        "adds": (("p", (2, 4, 2), 1), ("q", (0, 2, 2, 2), -1)),
        "witness": ("222222", "22", "PS", "02|13|64|75", -1),
        "residual_count": 11,
    },
    {
        "name": "QQ01_34", "kind": "anchor_shift",
        "path": ("PS", 2, 5, ((0, 1), (3, 4))),
        "adds": (("q", (0, 1, 2, 2), 1), ("q", (3, 4, 2, 2), -1)),
        "witness": ("222222", "22", "PS", "01|34|62|75", -1),
        "residual_count": 10,
    },
    {
        "name": "QQ03_14", "kind": "anchor_shift",
        "path": ("PS", 2, 5, ((0, 3), (1, 4))),
        "adds": (("q", (0, 3, 2, 2), 1), ("q", (1, 4, 2, 2), -1)),
        "witness": ("222222", "22", "PS", "03|14|62|75", -1),
        "residual_count": 10,
    },
)


BASE_Q = dict(B.Q_EDGE)
BASE_P = dict(B.FIRST)
BASE_S = dict(B.SECOND)
BASE_D = dict(B.DIRECT)


def reset_tables():
    B.Q_EDGE.clear()
    B.Q_EDGE.update(BASE_Q)
    B.FIRST.clear()
    B.FIRST.update(BASE_P)
    B.SECOND.clear()
    B.SECOND.update(BASE_S)
    B.DIRECT.clear()
    B.DIRECT.update(BASE_D)


def add_normalized(candidate):
    reset_tables()
    for table, key, value in candidate["adds"]:
        target = {"q": B.Q_EDGE, "p": B.FIRST, "s": B.SECOND, "d": B.DIRECT}[table]
        target[key] = B.constant(value)


def evaluate(polynomial):
    return P.evaluate(polynomial)


def audit_minimal_classification():
    q_support = {(0, 4), (1, 3)}
    p_support = {2}
    s_support = {5}

    ps_paths = []
    for p_site in B.SITES:
        for s_site in B.SITES:
            if p_site == s_site:
                continue
            rest = tuple(site for site in B.SITES if site not in (p_site, s_site))
            for q_matching in B.matchings(rest):
                q_edges = tuple(sorted(tuple(sorted(edge)) for edge in q_matching))
                cost = int(p_site not in p_support) + int(s_site not in s_support)
                cost += sum(edge not in q_support for edge in q_edges)
                if cost:
                    ps_paths.append((cost, p_site, s_site, q_edges))
    minimum_ps = min(path[0] for path in ps_paths)
    minimal_ps = tuple(path for path in ps_paths if path[0] == minimum_ps)
    require(minimum_ps == 2, ("minimal PS cost moved", minimum_ps))
    require(len(minimal_ps) == 11, ("minimal PS orbit size moved", minimal_ps))

    dq_paths = []
    for q_matching in B.matchings(B.SITES):
        q_edges = tuple(sorted(tuple(sorted(edge)) for edge in q_matching))
        cost = 1 + sum(edge not in q_support for edge in q_edges)  # new a_21
        dq_paths.append((cost, q_edges))
    minimum_dq = min(path[0] for path in dq_paths)
    minimal_dq = tuple(path for path in dq_paths if path[0] == minimum_dq)
    require(minimum_dq == 2, ("minimal DQ cost moved", minimum_dq))
    require(minimal_dq == ((2, ((0, 4), (1, 3), (2, 5))),),
            ("minimal DQ orbit changed", minimal_dq))
    derived_paths = {
        ("DQ", minimal_dq[0][1]),
        *(("PS", p_site, s_site, q_edges)
          for _, p_site, s_site, q_edges in minimal_ps),
    }
    registered_paths = {candidate["path"] for candidate in CANDIDATES}
    require(registered_paths == derived_paths,
            ("candidate registry does not equal the derived orbit",
             registered_paths, derived_paths))
    return minimal_dq, minimal_ps


def normalized_ledger(candidate):
    add_normalized(candidate)
    rows = []
    for word in product(B.COLORS, repeat=6):
        for row, column in product(B.COLORS, repeat=2):
            value = evaluate(B.residual(row, column, word))
            if value:
                rows.append(("".join(map(str, word)), f"{row}{column}", value))
    return rows


def audit_all_normalized_orbits():
    results = []
    for candidate in CANDIDATES:
        rows = normalized_ledger(candidate)
        require(evaluate(B.residual(2, 1, PURE)) == 0,
                (candidate["name"], "pure 21 was not cancelled"))
        word, head, operation, fine, expected = candidate["witness"]
        witness_value = next(
            (value for row_word, row_head, value in rows
             if row_word == word and row_head == head),
            Q(0),
        )
        require(witness_value == expected,
                (candidate["name"], "witness moved", witness_value, rows))
        require(len(rows) == candidate["residual_count"],
                (candidate["name"], "residual count moved", len(rows), rows))
        results.append({
            "name": candidate["name"],
            "kind": candidate["kind"],
            "witness_word": word,
            "witness_head": head,
            "witness_operation": operation,
            "witness_fine": fine,
            "witness_value": int(expected),
            "residual_count": len(rows),
        })
    reset_tables()
    return results


def sole_monomial(polynomial):
    require(len(polynomial) == 1, ("not a monomial", polynomial))
    (variables, coefficient), = polynomial.items()
    require(coefficient in (Q(1), Q(-1)), ("nonunit coefficient", polynomial))
    return Counter(variables), coefficient


def polynomial_power(polynomial, exponent):
    answer = B.constant(1)
    for _ in range(exponent):
        answer = B.multiply(answer, polynomial)
    return answer


def quotient_monomial(numerator, denominator):
    top, top_coefficient = sole_monomial(numerator)
    bottom, bottom_coefficient = sole_monomial(denominator)
    require(top_coefficient == bottom_coefficient == 1, "quotient sign changed")
    difference = top - bottom
    require(not (bottom - top), ("monomial does not divide", numerator, denominator))
    names = []
    for name, multiplicity in sorted(difference.items()):
        names.extend([name] * multiplicity)
    return B.product_polynomials(var(name) for name in names)


def anchor_difference():
    return B.add(
        B.multiply(B.ANCHORS[0], B.multiply(B.A1, B.A2)),
        B.add(B.multiply(B.ANCHORS[1], B.A2), B.ANCHORS[2]),
    )


def b_class_certificate(identity):
    # identity=-Y*m.  Choose k<=2 with m dividing APROD^k, then
    # 1=N*identity+(Y+1)APROD^k-(APROD^k-1).
    rhs = B.negate(identity)
    require(all("Y" in variables for variables in rhs), ("Y missing", identity))
    without_y = {}
    for variables, coefficient in rhs.items():
        names = list(variables)
        names.remove("Y")
        without_y[tuple(names)] = coefficient
    for exponent in (1, 2):
        target = polynomial_power(APROD, exponent)
        top, _ = sole_monomial(target)
        bottom, _ = sole_monomial(without_y)
        if not (bottom - top):
            inverse = quotient_monomial(target, without_y)
            break
    else:
        raise RuntimeError(("no anchor inverse", identity))
    require(
        B.multiply(inverse, identity)
        == B.negate(B.multiply(P.Y, target)),
        ("unit inverse failed", identity),
    )
    geometric = B.constant(0)
    power = B.constant(1)
    for _ in range(exponent):
        geometric = B.add(geometric, power)
        power = B.multiply(power, APROD)
    power_minus_one = B.multiply(anchor_difference(), geometric)
    require(power_minus_one == B.subtract(target, B.constant(1)),
            "anchor power telescoping changed")
    certificate = B.subtract(
        B.add(
            B.multiply(inverse, identity),
            B.multiply(B.add(P.Y, B.constant(1)), target),
        ),
        power_minus_one,
    )
    require(certificate == B.constant(1), ("B-class certificate failed", certificate))
    return exponent


def audit_polynomial_certificates():
    certificates = []

    # A.  DQ25: R*L_01-D*C_21=-D*U_21.
    K, R = var("K25"), var("R21")
    v_dq = B.product_polynomials((R, K, B.V["f"], B.V["g"]))
    c_dq = B.add(U21, v_dq)
    leak_dq = B.product_polynomials((B.V["D"], K, B.V["f"], B.V["g"]))
    identity_dq = B.subtract(B.multiply(R, leak_dq), B.multiply(B.V["D"], c_dq))
    require(identity_dq == B.negate(B.multiply(B.V["D"], U21)),
            "DQ migration identity changed")
    # S2*identity=-D*Y*A2.  This becomes 1 at D=1,Y=-1,A2=1.
    normalized_dy = B.subtract(
        B.multiply(B.V["D"], B.add(P.Y, B.constant(1))),
        B.subtract(B.V["D"], B.constant(1)),
    )
    require(normalized_dy == B.add(B.multiply(B.V["D"], P.Y), B.constant(1)),
            "D/Y normalization identity changed")
    cert_dq = B.subtract(
        B.add(
            B.multiply(B.V["S2"], identity_dq),
            B.multiply(normalized_dy, B.A2),
        ),
        B.ANCHORS[2],
    )
    require(cert_dq == B.constant(1), ("DQ unit certificate failed", cert_dq))
    certificates.append(("DQ25", "direct-head", 1))

    # B.  Every mate introducing a new s_1 coefficient has a diagonal 11
    # witness.  The migration identity eliminates the new-cell product and
    # leaves -Y times an anchor-unit old monomial.
    X, Z = var("X5"), var("Z2")
    v = B.product_polynomials((X, Z, B.V["f"], B.V["g"]))
    c = B.add(U21, v)
    w = B.product_polynomials((B.V["P1"], Z, B.V["f"], B.V["g"]))
    identity = B.subtract(B.multiply(X, w), B.multiply(B.V["P1"], c))
    require(identity == B.negate(B.multiply(B.V["P1"], U21)),
            "reverse-orientation identity changed")
    certificates.append(("REV25", "diagonal-11", b_class_certificate(identity)))

    s_cases = (
        ("S0_Q45", "Z0", "K45", "g", ("a", "e")),
        ("S1_Q35", "Z1", "K35", "f", ("a", "f")),
        ("S3_Q15", "Z3", "K15", "f", ("c", "e")),
        ("S4_Q05", "Z4", "K05", "g", ("c", "g")),
    )
    for name, z_name, k_name, old_edge, witness_edges in s_cases:
        z, k = var(z_name), var(k_name)
        v = B.product_polynomials((B.V["P2"], z, k, B.V[old_edge]))
        c = B.add(U21, v)
        witness = B.product_polynomials(
            (B.V["P1"], z) + tuple(B.V[edge] for edge in witness_edges)
        )
        identity = B.subtract(
            B.multiply(B.product_polynomials((B.V["P2"], k, B.V[old_edge])), witness),
            B.multiply(
                B.product_polynomials((B.V["P1"],) + tuple(B.V[e] for e in witness_edges)),
                c,
            ),
        )
        expected = B.negate(B.multiply(
            B.product_polynomials((B.V["P1"],) + tuple(B.V[e] for e in witness_edges)),
            U21,
        ))
        require(identity == expected, (name, "diagonal migration identity changed"))
        certificates.append((name, "diagonal-11", b_class_certificate(identity)))

    # C.  New p_2/q-only companions appear proportionally in heads 21 and
    # 22.  If C21=0, the complete 22 response is zero rather than the target
    # one.  The displayed identity is itself a degree-one unit certificate.
    anchor_cases = (
        ("P0_Q24", monomial("XP0", "Y", "g", "KP24"),
                     monomial("XP0", "S2", "g", "KP24")),
        ("P1_Q23", monomial("XP1", "Y", "f", "KP23"),
                     monomial("XP1", "S2", "f", "KP23")),
        ("P3_Q12", monomial("XP3", "Y", "f", "KP12"),
                     monomial("XP3", "S2", "f", "KP12")),
        ("P4_Q02", monomial("XP4", "Y", "g", "KP02"),
                     monomial("XP4", "S2", "g", "KP02")),
        ("QQ01_34", monomial("P2", "Y", "K01", "K34"),
                       monomial("P2", "S2", "K01", "K34")),
        ("QQ03_14", monomial("P2", "Y", "K03", "K14"),
                       monomial("P2", "S2", "K03", "K14")),
    )
    for name, v21, v22 in anchor_cases:
        c21 = B.add(U21, v21)
        c22 = B.subtract(B.add(B.A2, v22), B.constant(1))
        proportionality = B.subtract(
            B.multiply(P.Y, B.add(c22, B.constant(1))),
            B.multiply(B.V["S2"], c21),
        )
        require(proportionality == {}, (name, "21/22 proportionality changed"))
        certificate = B.add(
            B.add(P.Y, B.constant(1)),
            B.subtract(B.multiply(P.Y, c22), B.multiply(B.V["S2"], c21)),
        )
        require(certificate == B.constant(1), (name, "anchor unit certificate failed"))
        certificates.append((name, "anchor-22", 1))

    require(len(certificates) == 12, "certificate orbit is incomplete")
    return certificates


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("all", "classification", "source", "certificates"),
        default="all",
    )
    args = parser.parse_args()

    classification = source = certificates = None
    if args.mode in ("all", "classification"):
        classification = audit_minimal_classification()
    if args.mode in ("all", "source"):
        source = audit_all_normalized_orbits()
    if args.mode in ("all", "certificates"):
        certificates = audit_polynomial_certificates()

    kind_counts = Counter(candidate["kind"] for candidate in CANDIDATES)
    report = {
        "mode": args.mode,
        "selected_word": "222222",
        "selected_head": "21",
        "selected_operation": "PS",
        "selected_fine": "04|13|62|75",
        "minimal_new_cells": 2,
        "minimal_dq_mates": None if classification is None else len(classification[0]),
        "minimal_ps_mates": None if classification is None else len(classification[1]),
        "orbit_size": len(CANDIDATES),
        "mechanisms": dict(sorted(kind_counts.items())),
        "source_orbits_checked": None if source is None else len(source),
        "certificates_checked": None if certificates is None else len(certificates),
        "next_open_scope": "companions with at least three new source cells",
    }
    digest = sha256(
        json.dumps(report, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    print("n=8 pure-21 minimal companion orbit: PASS")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

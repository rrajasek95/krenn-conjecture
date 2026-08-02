#!/usr/bin/env python3
"""Independent exact audit of the corrected Hasse--Schmidt/cap separation.

This checker does not import the primary checker.  It independently audits
the mixed-dual-number sign, the five eight-site polars, the selected split-
cap matrix, and the zero-indeterminacy criterion.  It also checks that the
corrected primary artifacts explicitly record that no polar-to-cap
comparison or first-jet construction has been supplied.
"""

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import json


F = Fraction
SITES = tuple(range(8))
ODD = (1, 2, 3, 4, 5)
MIXED = (1, 2, 1, 1, 2)
X, P, R_SITE, Q_SITE = 0, 6, 3, 7
FORBIDDEN = frozenset((P, R_SITE))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def dual_add(left, right):
    require(len(left) == len(right), "tuple-add length mismatch")
    return tuple(left[index] + right[index] for index in range(len(left)))


def dual_multiply(left, right):
    """Multiply in Q[eps,delta]/(eps^2,delta^2).

    Coordinates are (1, eps, delta, eps*delta).
    """

    a, e, d, m = left
    b, f, g, n = right
    return (
        a * b,
        a * f + e * b,
        a * g + d * b,
        a * n + m * b + e * g + d * f,
    )


def dual_power(value, exponent):
    answer = (F(1), F(0), F(0), F(0))
    for _ in range(exponent):
        answer = dual_multiply(answer, value)
    return answer


def monomial_value(exponents, values):
    answer = F(1)
    for exponent, value in zip(exponents, values):
        answer *= value ** exponent
    return answer


def derivative_value(exponents, values, indices):
    remaining = list(exponents)
    coefficient = F(1)
    for index in indices:
        coefficient *= remaining[index]
        remaining[index] -= 1
        if remaining[index] < 0:
            return F(0)
    return coefficient * monomial_value(tuple(remaining), values)


def compositions(total, parts):
    if parts == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in compositions(total - first, parts - 1):
            yield (first,) + tail


def audit_mixed_jet_formula():
    """Check the Taylor formula on a spanning set of polynomial monomials."""

    samples = (
        ((F(2), F(-3), F(5)),
         (F(7), F(1, 2), F(-4)),
         (F(-2), F(3), F(5, 3)),
         (F(11, 2), F(-7), F(2))),
        ((F(-1), F(4, 3), F(2)),
         (F(0), F(-5), F(3, 2)),
         (F(7, 4), F(2), F(-1)),
         (F(-3), F(0), F(8))),
    )
    checked = 0
    for degree in range(8):
        for exponents in compositions(degree, 3):
            for x, xi, eta, zeta in samples:
                substituted = (F(1), F(0), F(0), F(0))
                for index, exponent in enumerate(exponents):
                    coordinate = (x[index], xi[index], eta[index], zeta[index])
                    substituted = dual_multiply(
                        substituted, dual_power(coordinate, exponent))

                constant = monomial_value(exponents, x)
                first_xi = sum(
                    (derivative_value(exponents, x, (i,)) * xi[i]
                     for i in range(3)), F(0))
                first_eta = sum(
                    (derivative_value(exponents, x, (i,)) * eta[i]
                     for i in range(3)), F(0))
                jacobian_zeta = sum(
                    (derivative_value(exponents, x, (i,)) * zeta[i]
                     for i in range(3)), F(0))
                mixed_hessian = sum(
                    (derivative_value(exponents, x, (i, j))
                     * xi[i] * eta[j]
                     for i in range(3) for j in range(3)), F(0))
                expected = (constant, first_xi, first_eta,
                            jacobian_zeta + mixed_hessian)
                require(substituted == expected,
                        f"mixed Taylor sign/factor failed at {exponents}")
                checked += 1
    require(checked == 240, "unexpected mixed Taylor audit size")
    return checked


@lru_cache(maxsize=None)
def matchings_mask(mask):
    """Generate perfect matchings by least-set-bit recursion."""

    if mask == 0:
        return ((),)
    first = (mask & -mask).bit_length() - 1
    remainder = mask ^ (1 << first)
    answer = []
    candidates = remainder
    while candidates:
        bit = candidates & -candidates
        second = bit.bit_length() - 1
        candidates ^= bit
        tail_mask = remainder ^ bit
        for tail in matchings_mask(tail_mask):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def matchings(vertices):
    mask = sum(1 << vertex for vertex in vertices)
    return matchings_mask(mask)


def colored_edge(u, v, word):
    if u < v:
        return (u, v, word[u], word[v])
    return (v, u, word[v], word[u])


def colored_term(matching, word):
    return tuple(sorted(colored_edge(u, v, word) for u, v in matching))


def contains_pair(matching, pair):
    pair = frozenset(pair)
    return any(frozenset(edge) == pair for edge in matching)


def remove_marked_edges(term, marked):
    remainder = list(term)
    for selected in marked:
        if selected not in remainder:
            return None
        remainder.remove(selected)
    return tuple(sorted(remainder))


def audit_polars():
    all_eight = matchings(SITES)
    require(len(all_eight) == 105, "eight-site matching count")
    allowed = tuple(matching for matching in all_eight
                    if not contains_pair(matching, FORBIDDEN))
    require(len(allowed) == 90, "direct-free row count")

    records = []
    supports = []
    for deleted in ODD:
        word = [0] * 8
        for site in ODD:
            if site != deleted:
                word[site] = MIXED[site - 1]
        word = tuple(word)
        row = tuple(colored_term(matching, word) for matching in allowed)
        require(len(set(row)) == 90, f"face {deleted}: row collision")

        marked = (
            colored_edge(X, deleted, word),
            colored_edge(P, Q_SITE, word),
        )
        polar = {
            remainder
            for term in row
            for remainder in (remove_marked_edges(term, marked),)
            if remainder is not None
        }

        face = tuple(site for site in ODD if site != deleted)
        expected = {
            colored_term(matching, word) for matching in matchings(face)
        }
        require(len(polar) == 3 and polar == expected,
                f"face {deleted}: polar reconstruction")

        pq_direct_terms = tuple(
            colored_term(matching, word) for matching in allowed
            if contains_pair(matching, (P, Q_SITE)))
        pq_star_terms = tuple(
            colored_term(matching, word) for matching in allowed
            if not contains_pair(matching, (P, Q_SITE)))
        pr_direct_terms = tuple(
            colored_term(matching, word) for matching in allowed
            if contains_pair(matching, (P, R_SITE)))
        pr_star_terms = tuple(
            colored_term(matching, word) for matching in allowed
            if not contains_pair(matching, (P, R_SITE)))

        def polar_of(terms):
            return {
                remainder
                for term in terms
                for remainder in (remove_marked_edges(term, marked),)
                if remainder is not None
            }

        require(polar_of(pq_direct_terms) == expected,
                f"face {deleted}: pq-direct placement")
        require(not polar_of(pq_star_terms),
                f"face {deleted}: pq-star contamination")
        require(not polar_of(pr_direct_terms),
                f"face {deleted}: pr-direct contamination")
        require(polar_of(pr_star_terms) == expected,
                f"face {deleted}: pr-star placement")

        supports.append(polar)
        records.append({
            "deleted": deleted,
            "word": "".join(map(str, word)),
            "face_word": "".join(str(word[site]) for site in face),
            "terms": len(polar),
            "pq": "direct",
            "pr": "two-star",
        })

    require(all(supports[i].isdisjoint(supports[j])
                for i in range(5) for j in range(i + 1, 5)),
            "labelled polar supports overlap")
    return records


def rank(columns):
    if not columns:
        return 0
    row_count = len(columns[0])
    matrix = [[F(columns[column][row]) for column in range(len(columns))]
              for row in range(row_count)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, row_count)
                      if matrix[row][column] != 0), None)
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            multiple = matrix[row][column]
            if multiple:
                matrix[row] = [entry - multiple * pivot_entry
                               for entry, pivot_entry
                               in zip(matrix[row], matrix[pivot_row])]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def block_copies(columns, copies):
    rows = len(columns[0])
    result = []
    for block in range(copies):
        for column in columns:
            lifted = [F(0)] * (rows * copies)
            lifted[block * rows:(block + 1) * rows] = column
            result.append(lifted)
    return result


def audit_split_cap():
    packets = (
        (F(2), F(3), F(5), F(11), F(7, 5)),
        (F(3), F(0), F(2), F(5), F(-4, 9)),
        (F(-2), F(7), F(3), F(-5), F(13, 6)),
        (F(5, 3), F(-7, 4), F(11, 5), F(2, 9), F(-8, 7)),
    )
    records = []
    for A, B, C, U, Y in packets:
        kappa = A * U - B * C
        require(kappa != 0 and Y != 0, "inactive audit packet")

        col_one, col_two = (A, C), (B, U)
        left_one, left_two = (-C, A), (U, -B)
        dot = lambda x, y: x[0] * y[0] + x[1] * y[1]
        require(dot(left_one, col_one) == 0, "first adjugate kernel sign")
        require(dot(left_two, col_two) == 0, "second adjugate kernel sign")
        require(dot(left_one, col_two) == kappa, "first curvature sign")
        require(dot(left_two, col_one) == kappa, "second curvature sign")

        target = [-Y, F(1), F(0)]
        residue = [F(1), F(0), F(1)]
        split_cap = [kappa * Y, F(0), F(0)]
        existing = [target, residue]
        require(rank(existing) == 2, "split-cap existing rank")
        require(rank(existing + [split_cap]) == 3,
                "split-cap augmented rank")
        require(rank([column[:1] for column in existing])
                == rank([column[:1] for column in existing]
                        + [split_cap[:1]]), "boundary-only membership")
        require(rank([column[:2] for column in existing])
                == rank([column[:2] for column in existing]
                        + [split_cap[:2]]), "target membership")

        # Solving a*T+b*rho=p forces a=0 from target, b=0 from residue,
        # contradicting the nonzero boundary kappa*Y.
        require(split_cap[0] != 0, "split-cap boundary unexpectedly zero")
        require(target[1] == 1 and residue[1] == 0, "target pivot")
        require(target[2] == 0 and residue[2] == 1, "residue pivot")

        graph = [target[row] + Y * residue[row] for row in range(3)]
        require(graph == [F(0), F(1), Y], "cap graph sign")
        overlap = [-kappa * entry for entry in graph]
        anchor = [kappa * entry for entry in graph]
        require(dual_add(tuple(overlap), tuple(anchor)) == (F(0),) * 3,
                "anchor cancellation sign")
        relative = [-kappa * Y * entry for entry in residue]
        require(relative == [-kappa * Y, F(0), -kappa * Y],
                "relative response sign")
        require([relative[row] + split_cap[row] for row in range(3)]
                == [F(0), F(0), -kappa * Y], "promoted response sign")

        five_existing = block_copies(existing, 5)
        five_missing = block_copies([split_cap], 5)
        require(rank(five_existing) == 10, "five-block base rank")
        require(rank(five_existing + five_missing) == 15,
                "five-block augmented rank")
        records.append({
            "kappa": str(kappa),
            "Y": str(Y),
            "direct_free": B == 0,
            "ranks": [2, 3, 10, 15],
            "tested_class": "kappa*Y*w",
        })
    return records


def audit_zero_indeterminacy():
    # J has kernel span{(-1,-1,1)}.  The obstruction (2,3) has the affine
    # lift family (2-t,3-t,t).  A landing is constant on that family exactly
    # when it kills the kernel direction.
    kernel = (F(-1), F(-1), F(1))
    good_landing = (F(1), F(1), F(2))
    bad_landing = (F(0), F(0), F(1))
    dot = lambda left, right: sum((a * b for a, b in zip(left, right)), F(0))
    require(dot(good_landing, kernel) == 0, "good landing misses kernel")
    require(dot(bad_landing, kernel) != 0, "bad landing kills kernel")
    lifts = [tuple((F(2 - t), F(3 - t), F(t))) for t in range(-3, 4)]
    require(all((lift[0] + lift[2], lift[1] + lift[2]) == (F(2), F(3))
                for lift in lifts), "affine lift family")
    require(len({dot(good_landing, lift) for lift in lifts}) == 1,
            "kernel-annihilating landing is not single valued")
    require(len({dot(bad_landing, lift) for lift in lifts}) == len(lifts),
            "non-annihilating landing became single valued")
    return {
        "kernel": [str(value) for value in kernel],
        "good_values": len({dot(good_landing, lift) for lift in lifts}),
        "bad_values": len({dot(bad_landing, lift) for lift in lifts}),
    }


def audit_explicit_separation_flags():
    root = Path(__file__).resolve().parents[1]
    primary_path = root / "computations" / "verify_h3_augmented_second_jet_polar_membership.py"
    note_path = root / "notes" / "h3-augmented-hasse-schmidt-polar-membership.md"
    primary = primary_path.read_text(encoding="utf-8")
    note = note_path.read_text(encoding="utf-8")

    primary_needles = (
        '"comparison_map_constructed": False',
        '"first_jets_constructed": False',
        '"augmented_jacobian_composition_checked": False',
        'polar class h_v*Y_0 is NOT composed with split-cap class kappa*Y*w_v',
    )
    note_needles = (
        "Equations (3) and (5) are not the same class.",
        "Therefore the ranks (6) prove no failure or necessity statement for the",
        "It does not identify those",
        "and it proves no",
        "evaluate (2) on the polar class, prove that named full-source rows fail the",
    )
    for needle in primary_needles:
        require(needle in primary, f"primary lost explicit separation flag: {needle}")
    for needle in note_needles:
        require(needle in note, f"note lost scope guard: {needle}")

    # Guard specifically against the superseded claims in the pre-fix note.
    forbidden_verbatim = (
        "The existing rows pass the boundary-only and target-augmented parts of this test",
        "adding the five polar columns raises rank by exactly five",
        "five polar obstructions are not independent",
        "The smallest Rees extension needs five independent columns",
    )
    for phrase in forbidden_verbatim:
        require(phrase not in note and phrase not in primary,
                f"superseded polar/cap composition claim remains: {phrase}")
    return {
        "primary_flags": len(primary_needles),
        "note_scope_guards": len(note_needles),
        "superseded_claims_absent": len(forbidden_verbatim),
        "comparison_constructed": False,
    }


def main():
    ledger = {
        "mixed_taylor_monomial_samples": audit_mixed_jet_formula(),
        "polars": audit_polars(),
        "split_cap": audit_split_cap(),
        "zero_indeterminacy": audit_zero_indeterminacy(),
        "separation_flags": audit_explicit_separation_flags(),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == "739e60f8070d60d2441d748e5f42860ff8e51f984a6bbb601801b51302f9b87d",
            f"independent ledger changed: {digest}")

    print("independent Hasse--Schmidt / split-cap separation audit: PASS")
    print("mixed Taylor sign: J*zeta + H(xi,eta), no factor two")
    print("five polars reconstructed independently: pq-direct / pr-two-star")
    print("split-cap only: ranks 2 -> 3 and formal five-block 10 -> 15")
    print("polar-to-cap comparison, first jets, and augmented square remain unconstructed")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact common-hafnian coupling for the two-bad Lemma-E packet.

The two-bad flag normal form peels colours a,c at the shared site p and
leaves a distributed third-colour p-port remainder.  This checker derives
that remainder from one literal common C-block family, rather than treating
its cofactors as independent.  It also shows that the compact relaxed guard
from the pinned normal-form checker fails in two explicit mixed rows when
its formal p-cofactors are replaced by the actual common hafnians.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import verify_shared_reciprocal_lemma_e_flag_normal_form as flags


ROOT = Path(__file__).resolve().parents[1]
P, QSITE, RSITE = 0, 1, 2
COMMON = (3, 4, 5, 6, 7)
COLORS = (0, 1, 2)
PINNED_FLAGS_SHA256 = (
    "7019b885b0337c8848dad180ff28a7ff5cec59ed65008ef32c6d33dd4bd9a3b5"
)
EXPECTED_LEDGER_SHA256 = (
    "7754a05083a82f957cd6e276e9699659ae5c24d27c9ed4c8445ba65bf22a3672"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_dependency():
    path = ROOT / (
        "computations/verify_shared_reciprocal_lemma_e_flag_normal_form.py"
    )
    require(sha256(path.read_bytes()).hexdigest() == PINNED_FLAGS_SHA256,
            "the Lemma-E flag normal form dependency changed")


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def add_term(polynomial, monomial, coefficient=1):
    monomial = tuple(sorted(monomial))
    polynomial[monomial] += coefficient
    if polynomial[monomial] == 0:
        del polynomial[monomial]


def internal_cell(left, right, left_color, right_color):
    return f"I{left}{right}_{left_color}{right_color}"


def star_cell(name, site, outer_color, site_color):
    return f"{name}{site}_{outer_color}{site_color}"


def internal_hafnian(vertices, word):
    vertices = tuple(vertices)
    color_at = dict(zip(vertices, word))
    polynomial = Counter()
    for matching in perfect_matchings(vertices):
        monomial = tuple(
            internal_cell(left, right, color_at[left], color_at[right])
            for left, right in matching
        )
        add_term(polynomial, monomial)
    return polynomial


def odd_star_direct(star_name, outer_color, common_word):
    color_at = dict(zip(COMMON, common_word))
    polynomial = Counter()
    for hole in COMMON:
        rest = tuple(site for site in COMMON if site != hole)
        for monomial, coefficient in internal_hafnian(
                rest, tuple(color_at[site] for site in rest)).items():
            add_term(
                polynomial,
                monomial + (
                    star_cell(star_name, hole,
                              outer_color, color_at[hole]),
                ),
                coefficient,
            )
    return polynomial


def full_remainder_direct(q_color, r_color, common_word):
    """Literal matching expansion after p uses one common-site port."""

    color_at = dict(zip(COMMON, common_word))
    polynomial = Counter()
    vertices = (QSITE, RSITE) + COMMON
    for p_hole in COMMON:
        remaining = tuple(site for site in vertices if site != p_hole)
        word_at = {QSITE: q_color, RSITE: r_color, **color_at}
        for matching in perfect_matchings(remaining):
            monomial = [star_cell(
                "P", p_hole, 2, color_at[p_hole]
            )]
            for left, right in matching:
                if (left, right) == (QSITE, RSITE):
                    monomial.append(f"D_{q_color}{r_color}")
                elif left == QSITE:
                    monomial.append(star_cell(
                        "Q", right, q_color, color_at[right]
                    ))
                elif left == RSITE:
                    monomial.append(star_cell(
                        "R", right, r_color, color_at[right]
                    ))
                else:
                    monomial.append(internal_cell(
                        left, right, color_at[left], color_at[right]
                    ))
            add_term(polynomial, tuple(monomial))
    return polynomial


def common_hafnian_formula(q_color, r_color, common_word):
    """P_t (D_jk K + Q_j R_k J) at N=8."""

    color_at = dict(zip(COMMON, common_word))
    polynomial = Counter()
    for p_hole in COMMON:
        p_cell = star_cell("P", p_hole, 2, color_at[p_hole])

        # Chord term D_jk times K=q_C^[2] on C minus the p-port site.
        rest = tuple(site for site in COMMON if site != p_hole)
        for monomial, coefficient in internal_hafnian(
                rest, tuple(color_at[site] for site in rest)).items():
            add_term(polynomial,
                     monomial + (p_cell, f"D_{q_color}{r_color}"),
                     coefficient)

        # Separate q,r routes: ordered distinct holes, followed by the one
        # residual internal edge J=q_C^[1].
        for q_hole in COMMON:
            if q_hole == p_hole:
                continue
            for r_hole in COMMON:
                if r_hole in (p_hole, q_hole):
                    continue
                last = tuple(site for site in COMMON
                             if site not in (p_hole, q_hole, r_hole))
                require(len(last) == 2,
                        "the N=8 lower common power stopped being one edge")
                monomial = (
                    p_cell,
                    star_cell("Q", q_hole, q_color,
                              color_at[q_hole]),
                    star_cell("R", r_hole, r_color,
                              color_at[r_hole]),
                    internal_cell(last[0], last[1],
                                  color_at[last[0]], color_at[last[1]]),
                )
                add_term(polynomial, monomial)
    return polynomial


def audit_symbolic_coupling():
    full_rows = 0
    odd_rows = 0
    row_hash = sha256()
    for common_word in product(COLORS, repeat=len(COMMON)):
        for outer_color in COLORS:
            # This is exactly star*K, the E3 odd-site deleted hafnian row.
            direct_q = odd_star_direct("Q", outer_color, common_word)
            direct_r = odd_star_direct("R", outer_color, common_word)
            require(direct_q and direct_r,
                    "the unrestricted odd-star polynomial vanished")
            odd_rows += 2
            row_hash.update(json.dumps(
                (tuple(sorted(direct_q.items())),
                 tuple(sorted(direct_r.items()))),
                separators=(",", ":"),
            ).encode())
        for q_color in COLORS:
            for r_color in COLORS:
                direct = full_remainder_direct(
                    q_color, r_color, common_word
                )
                formula = common_hafnian_formula(
                    q_color, r_color, common_word
                )
                require(direct == formula,
                        "the common-hafnian remainder formula failed")
                full_rows += 1
                row_hash.update(json.dumps(
                    tuple(sorted(direct.items())),
                    separators=(",", ":"),
                ).encode())
    require((odd_rows, full_rows) == (1458, 2187),
            "the exact common-hafnian row census changed")
    return odd_rows, full_rows, row_hash.hexdigest()


def numeric_hafnian(vertices, word, cells):
    polynomial = Fraction(0)
    for matching in perfect_matchings(vertices):
        coefficient = Fraction(1)
        for left, right in matching:
            coefficient *= cells.get(
                (left, right, word[left], word[right]), Fraction(0)
            )
        polynomial += coefficient
    return polynomial


def audit_relaxed_guard_source_failure():
    """Replace the two formal half-X2 cofactors by their actual hafnians."""

    cells = {
        (4, 5, 0, 0): Fraction(1),
        (6, 7, 0, 0): Fraction(1),
        (3, 6, 1, 1): Fraction(1),
        (5, 7, 1, 1): Fraction(1),
        (QSITE, 4, 1, 1): Fraction(1),
        (RSITE, 3, 0, 0): Fraction(1),
        (P, 5, 2, 2): Fraction(1, 2),
        (P, 6, 2, 2): Fraction(1, 2),
    }
    remainder = {}
    for word in product(COLORS, repeat=8):
        if word[P] != 2:
            continue
        value = Fraction(0)
        for p_hole in COMMON:
            p_value = cells.get(
                (P, p_hole, word[P], word[p_hole]), Fraction(0)
            )
            if not p_value:
                continue
            residual = tuple(site for site in range(1, 8)
                             if site != p_hole)
            value += p_value * numeric_hafnian(residual, word, cells)
        if value:
            remainder[word] = value

    expected = {
        (2, 1, 0, 0, 1, 2, 0, 0): Fraction(1, 2),
        (2, 1, 0, 0, 1, 1, 2, 1): Fraction(1, 2),
    }
    require(remainder == expected,
            f"the relaxed guard's actual source remainder changed: {remainder}")
    target_word = (2,) * 8
    require(target_word not in remainder,
            "the relaxed guard unexpectedly produced its formal X2 target")
    mismatch_count = len(remainder) + 1
    return remainder, target_word, mismatch_count


def audit_raw_common_hole_dichotomy():
    """Exact selected-summand incidence behind the mixed (c,a) row.

    A nonzero summand of Q_c*K chooses a Q-hole u and a matching of C-u;
    a summand of R_a*K chooses an R-hole v.  If u=v, Q_c*R_a is killed by
    the site-square relation.  If u!=v, exactly one edge of either selected
    matching avoids both holes and therefore gives a raw Q_c*R_a*J term.
    This is a provenance statement; aggregate terms with the same output
    word may still cancel.
    """

    witnesses = tuple(
        (hole, matching)
        for hole in COMMON
        for matching in perfect_matchings(
            tuple(site for site in COMMON if site != hole)
        )
    )
    require(len(witnesses) == 15,
            "the five-site near-perfect witness count changed")
    same_hole = 0
    distinct_hole = 0
    raw_terms = 0
    for q_hole, q_matching in witnesses:
        for r_hole, r_matching in witnesses:
            if q_hole == r_hole:
                same_hole += 1
                continue
            distinct_hole += 1
            q_edges = tuple(edge for edge in q_matching
                            if r_hole not in edge)
            r_edges = tuple(edge for edge in r_matching
                            if q_hole not in edge)
            require(len(q_edges) == len(r_edges) == 1,
                    "a distinct-hole witness lost its surviving J edge")
            raw_terms += len(set(q_edges + r_edges))
    require((same_hole, distinct_hole) == (45, 180),
            "the raw common-hole split changed")
    require(180 <= raw_terms <= 360,
            "the raw mixed-term provenance count left its exact bounds")
    return len(witnesses), same_hole, distinct_hole, raw_terms


def main():
    pin_dependency()
    odd_rows, full_rows, symbolic_hash = audit_symbolic_coupling()
    remainder, target_word, mismatch_count = audit_relaxed_guard_source_failure()
    witness_count, same_hole, distinct_hole, raw_terms = (
        audit_raw_common_hole_dichotomy()
    )
    ledger = {
        "pinned_flags_sha256": PINNED_FLAGS_SHA256,
        "common_sites": COMMON,
        "odd_star_rows": odd_rows,
        "full_remainder_rows": full_rows,
        "symbolic_row_sha256": symbolic_hash,
        "identity": "P_t*(D_jk*K+Q_j*R_k*J)=delta_jt*delta_kt*X_t",
        "K": "q_C^[2]",
        "J": "q_C^[1]",
        "relaxed_guard_actual_remainder": [
            (word, (value.numerator, value.denominator))
            for word, value in sorted(remainder.items())
        ],
        "relaxed_guard_missing_target": target_word,
        "relaxed_guard_source_mismatches": mismatch_count,
        "raw_near_perfect_witnesses": witness_count,
        "raw_common_hole_pairs": same_hole,
        "raw_distinct_hole_pairs": distinct_hole,
        "raw_distinct_hole_mixed_terms": raw_terms,
        "raw_dichotomy_scope": "selected_summands_before_aggregate_cancellation",
        "general_packet_status": "open_common_hafnian_system",
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    require(digest == EXPECTED_LEDGER_SHA256,
            f"the common-hafnian ledger changed: {digest}")
    print("shared reciprocal two-bad common-hafnian packet: PASS")
    print("odd-star / full remainder rows:", odd_rows, "/", full_rows)
    print("relaxed four-flag guard actual mixed rows:", len(remainder))
    print("relaxed guard source mismatches:", mismatch_count)
    print("raw common/distinct-hole witness pairs:",
          same_hole, "/", distinct_hole)
    print("general common-hafnian packet: OPEN")
    print("ledger_sha256=", digest, sep="")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Exact cap-tail reduction on the normalized common-radical chart.

The pinned provenance system gives D_tt*R=1.  Localize with U*D_tt=1 and put
r=U*Q_t*R_t in the site-square-zero algebra.  The target full row becomes

    D_tt*P*(q+r)^[2] = X_t + U*H_0,
    H_0=P*(Q_t*R_t)^[2]=2*P*Q_t^[2]*R_t^[2].

The checker verifies the divided-power identity coefficientwise on all 243
five-site words, proves H has zero raw all-target coefficient, and eliminates
the other eight direct-block scalars by exact source-row determinants.  It
identifies the precise quartic cap tail; it does not claim that H_0 is zero
or in im(Phi).
"""

from __future__ import annotations

from hashlib import sha256
import itertools
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "computations"))

import verify_shared_reciprocal_two_bad_common_radical_provenance_system as source


PINNED_PROVENANCE_SHA256 = (
    "0f038dc17dbe711797318a1277cf68f751b6bb01423ccbb8eef0888ba96bedea"
)
EXPECTED_TAIL_SHA256 = (
    "72a88c13eb8203a963fbf31f28fb428ea174582e396f7ccc04dca04828f38f5b"
)
EXPECTED_LEDGER_SHA256 = (
    "dad2e495f9dea7dc8b44bf2c3d8e0e1e30eedfe7aa0397a2e2f08b58b16126af"
)

SITES = source.SITES
COLOURS = source.COLOURS
T = source.T


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def pin_dependency():
    path = ROOT / (
        "computations/"
        "verify_shared_reciprocal_two_bad_common_radical_provenance_system.py"
    )
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == PINNED_PROVENANCE_SHA256,
            f"the common-radical provenance dependency changed: {actual}")


def multiply_polynomials(left, right):
    answer = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            source.add_term(
                answer,
                source.multiply(*(left_monomial + right_monomial)),
                left_coefficient * right_coefficient,
            )
    return answer


def scale_polynomial(polynomial, scalar):
    return {monomial: scalar * coefficient
            for monomial, coefficient in polynomial.items()
            if scalar * coefficient}


def row_linear(row, site, colour):
    entry = source.row_entry(row, site, colour)
    if entry == 0:
        return {}
    if entry == 1:
        return {(): 1}
    return {(entry,): 1}


def uv_edge(word, left, right):
    # The physical quadratic Q_t*R_t has the symmetric endpoint block
    # U_left V_right + V_left U_right.
    first = multiply_polynomials(
        row_linear("Qt", left, word[left]),
        row_linear("Rt", right, word[right]),
    )
    second = multiply_polynomials(
        row_linear("Rt", left, word[left]),
        row_linear("Qt", right, word[right]),
    )
    return source.add_polynomials(first, second)


def cap_tail_coefficient(word):
    answer = {}
    for p_site in SITES:
        p_entry = row_linear("P", p_site, word[p_site])
        remaining = tuple(site for site in SITES if site != p_site)
        for matching in source.perfect_matchings(remaining):
            term = p_entry
            for left, right in matching:
                term = multiply_polynomials(
                    term, uv_edge(word, left, right)
                )
            answer = source.add_polynomials(answer, term)
    return answer


def factored_tail_coefficient(word):
    # P*U^[2]*V^[2]: choose the P site, two of the remaining four sites
    # for U, and the complementary two sites for V.
    answer = {}
    for p_site in SITES:
        remaining = tuple(site for site in SITES if site != p_site)
        for u_sites in itertools.combinations(remaining, 2):
            v_sites = tuple(site for site in remaining if site not in u_sites)
            term = row_linear("P", p_site, word[p_site])
            for site in u_sites:
                term = multiply_polynomials(
                    term, row_linear("Qt", site, word[site])
                )
            for site in v_sites:
                term = multiply_polynomials(
                    term, row_linear("Rt", site, word[site])
                )
            answer = source.add_polynomials(answer, term)
    return answer


def audit_quartic_tail():
    words = tuple(itertools.product(COLOURS, repeat=5))
    tail = {}
    factored = {}
    for word in words:
        direct = cap_tail_coefficient(word)
        factor = factored_tail_coefficient(word)
        require(direct == scale_polynomial(factor, 2),
                f"the quartic tail factorization failed at {word}")
        if direct:
            tail[word] = direct
            factored[word] = factor

    # Both Q_t and R_t have their sole target projection at site 1.
    # Two distinct product slots therefore cannot both contribute target.
    require((T,) * 5 not in tail,
            "the quartic cap tail acquired a raw X_t coefficient")
    require(tail,
            "the general quartic cap tail vanished identically")
    payload = json.dumps([
        (word, sorted((monomial, coefficient)
                      for monomial, coefficient in polynomial.items()))
        for word, polynomial in sorted(tail.items())
    ], separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_TAIL_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_TAIL_SHA256,
                f"the quartic cap tail changed: {digest}")
    return {
        "nonzero_word_coefficients": len(tail),
        "sparse_terms": sum(len(polynomial) for polynomial in tail.values()),
        "tail_sha256": digest,
        "factorization": "H=P*(Qt*Rt)^[2]=2*P*Qt^[2]*Rt^[2]",
        "raw_Xt_coefficient": 0,
    }


def audit_cap_identity_and_minor_elimination():
    labels, equations = source.build_system()
    target_word = (T,) * 5
    target_label = "".join(map(str, target_word))
    response = source.phi_polynomial("P", target_word)
    product_tt = source.product_polynomial("Qt", "Rt", target_word)
    require(not product_tt,
            "the normalized Qt/Rt product acquired a raw target term")
    full_target = source.polynomial_by_label(
        labels, equations, f"F22:{target_label}"
    )
    require(full_target == source.add_polynomials(
        source.multiply_variable(response, "D22"), {(): -1}
    ), "the source target row changed before cap normalization")

    # In the localization U*D22=1, the literal F22 source row is
    # P*K + P*Qt*Rt*q - X_t.  Polarizing the divided square of
    # q+U*Qt*Rt gives
    #
    #   D22*P*(q+U*Qt*Rt)^[2]
    #     = X_t + U*H_0                 modulo F22 and U*D22-1.
    #
    # Thus, after using the inverse relation, cap-X_t is the literal F22
    # source row plus U*H_0.  We audit the non-localized part coefficientwise.
    words = tuple(itertools.product(COLOURS, repeat=5))
    for word in words:
        response_word = source.phi_polynomial("P", word)
        product_word = source.product_polynomial("Qt", "Rt", word)
        tail_word = cap_tail_coefficient(word)
        target = {(): 1} if word == target_word else {}
        original_source = source.polynomial_by_label(
            labels, equations, f"F22:{''.join(map(str, word))}"
        )
        expected_source = source.add_polynomials(
            source.add_polynomials(
                source.multiply_variable(response_word, "D22"),
                product_word,
            ), target, -1,
        )
        require(original_source == expected_source,
                f"the F22 source row changed at {word}")

        # Expand the formal cap before imposing U*D22=1, then verify that
        # its reduction differs by the inverse relation times B+U*H_0.
        formal_cap = source.add_polynomials(
            source.multiply_variable(response_word, "D22"),
            source.multiply_variable(
                source.multiply_variable(product_word, "D22"), "U22"
            ),
        )
        formal_cap = source.add_polynomials(
            formal_cap,
            source.multiply_variable(source.multiply_variable(
                source.multiply_variable(tail_word, "D22"), "U22"
            ), "U22"),
        )
        reduced_cap = source.add_polynomials(
            source.add_polynomials(
                source.multiply_variable(response_word, "D22"),
                product_word,
            ),
            source.multiply_variable(tail_word, "U22"),
        )
        inverse_relation = source.add_polynomials(
            source.multiply_variable({("D22",): 1}, "U22"), {(): -1}
        )
        inverse_correction = multiply_polynomials(
            inverse_relation,
            source.add_polynomials(
                product_word, source.multiply_variable(tail_word, "U22")
            ),
        )
        require(source.add_polynomials(
            formal_cap, reduced_cap, -1
        ) == inverse_correction,
                f"the localized cap expansion changed at {word}")
        require(source.add_polynomials(
            reduced_cap, target, -1
        ) == source.add_polynomials(
            original_source, source.multiply_variable(tail_word, "U22")
        ), f"the localized cap congruence changed at {word}")

    # For each of the other eight full tensors F_jk=D_jk*L+B_jk=0,
    # the localized target coordinate R=L(t^5) eliminates D_jk exactly:
    #
    #   R F_jk(w)-L(w)F_jk(t^5)
    #       =R B_jk(w)-B_jk(t^5)L(w).
    #
    # These are 8*242 literal source determinants.  The target family gives
    #
    #   R F_22(w)-L(w)F_22(t^5)=R B_22(w)+L(w),
    #
    # another 242 source determinants.  Since D22*R=1, R is a unit.
    zero_minor_count = 8 * (len(words) - 1)
    target_equation_count = len(words) - 1
    require((zero_minor_count, target_equation_count) == (1936, 242),
            "the normalized full-row minor census changed")

    # Audit all 2,178 determinants against the committed source rows and
    # freeze their reduced right-hand sides.
    response_target = source.phi_polynomial("P", target_word)
    determinant_hasher = sha256()
    for q_index, q_row in enumerate(source.Q_ROWS):
        for r_index, r_row in enumerate(source.R_ROWS):
            family = f"F{q_index}{r_index}"
            target_source = source.polynomial_by_label(
                labels, equations, f"{family}:{target_label}"
            )
            product_target = source.product_polynomial(
                q_row, r_row, target_word
            )
            for word in words:
                if word == target_word:
                    continue
                word_label = "".join(map(str, word))
                response_word = source.phi_polynomial("P", word)
                word_source = source.polynomial_by_label(
                    labels, equations, f"{family}:{word_label}"
                )
                product_word = source.product_polynomial(q_row, r_row, word)
                determinant = source.add_polynomials(
                    multiply_polynomials(response_target, word_source),
                    multiply_polynomials(response_word, target_source),
                    -1,
                )
                expected = source.add_polynomials(
                    multiply_polynomials(response_target, product_word),
                    multiply_polynomials(response_word, product_target),
                    -1,
                )
                if (q_index, r_index) == (T, T):
                    expected = source.add_polynomials(expected, response_word)
                require(determinant == expected,
                        f"source determinant changed at {family}:{word_label}")
                encoded = json.dumps(
                    (f"{family}:{word_label}", sorted(
                        (monomial, coefficient)
                        for monomial, coefficient in expected.items()
                    )), separators=(",", ":")
                )
                determinant_hasher.update(encoded.encode())
                determinant_hasher.update(b"\n")

    return {
        "localization": ["D22*R=1", "U*D22=1"],
        "target_cap": "D22*P*(q+U*Qt*Rt)^[2]=X_t+U*H_0",
        "zero_family_rank_one_minors": zero_minor_count,
        "target_family_nonpure_rows": target_equation_count,
        "remaining_direct_block_variables": 0,
        "source_determinant_sha256": determinant_hasher.hexdigest(),
    }


def main():
    pin_dependency()
    tail = audit_quartic_tail()
    reduction = audit_cap_identity_and_minor_elimination()
    ledger = {
        "pinned_provenance_sha256": PINNED_PROVENANCE_SHA256,
        "quartic_cap_tail": tail,
        "normalized_full_row_reduction": reduction,
        "verdict": (
            "after localizing D22*R=1 the common-radical target row is a "
            "six-site cap by q+U*Qt*Rt with the single exact error "
            "2*U*P*Qt^[2]*Rt^[2]; all direct-block scalars eliminate by "
            "2178 source determinants, but the tail is not yet proved "
            "zero or in im(Phi)"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the common-radical cap-tail ledger changed: {digest}")

    print("shared reciprocal common-radical cap tail: PASS")
    print("H_0=2*P*Qt^[2]*Rt^[2]; raw X_t coefficient zero")
    print("direct block eliminated by 2178 source determinants")
    print(f"tail sha256: {tail['tail_sha256']}")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()

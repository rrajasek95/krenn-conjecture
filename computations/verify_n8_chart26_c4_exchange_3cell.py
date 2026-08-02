#!/usr/bin/env python3
"""Exact C4 base-matching exchange and its tetrahedral 3-cell.

For a perfect matching M and a colour word c, let m_M(c) be the matching
monomial and H_c the full eight-site hafnian coefficient.  The pair

    P^M_cd = m_M(c) H_d - m_M(d) H_c

is the un-divided source transport.  For two matchings M,N, the three-row
matrix with columns (m_M(c),m_N(c),H_c)^T supplies the missing coherences:
its 2-minors give the M transports, N transports, and matching-exchange
minors; its 3-minors are base-exchange Bianchi cells; and the signed four-
column Laplace relation is a literal tetrahedral 3-cell.

This checker uses the chart-26 colour square c=1,2,10,11 and the alternating
C4 exchange

    M=(02)(13)(45)(67),  N=(02)(13)(47)(56).

All calculations are in the full aggregate polynomial ring, before chart
support coordinates are set to one.  Polynomials are sparse integer maps.
"""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIRST_PATH = HERE / "verify_n8_chart26_first_homogeneous_spair.py"
SPEC = importlib.util.spec_from_file_location("n8_c4_first", FIRST_PATH)
FIRST = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(FIRST)
D5 = FIRST.D5

EXPECTED_LEDGER_SHA256 = (
    "64b1f89a760ae8268e0ab4fe9712cb9b289a3b540f9c0a370a3554f754ade287"
)

M = ((0, 2), (1, 3), (4, 5), (6, 7))
N = ((0, 2), (1, 3), (4, 7), (5, 6))
STATES = (1, 2, 10, 11)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def add_value(polynomial, monomial, coefficient):
    value = polynomial.get(monomial, 0) + coefficient
    if value:
        polynomial[monomial] = value
    else:
        polynomial.pop(monomial, None)


def add_scaled(target, source, scalar=1, multiplier=b""):
    for monomial, coefficient in source.items():
        add_value(
            target,
            bytes(sorted(multiplier + monomial)),
            scalar * coefficient,
        )


def matching_monomial(matching, code):
    word = D5.decode_word(code)
    variables = []
    for left, right in matching:
        variables.append(D5.COORDINATE_ID[
            (left, right, word[left], word[right])
        ])
    return bytes(sorted(variables))


def hafnian(code, omit=()):
    omitted = set(omit)
    polynomial = Counter()
    word = D5.decode_word(code)
    for matching, term in zip(D5.MATCHINGS, D5.iter_word_terms(code)):
        edges = tuple(sorted(
            tuple(sorted(edge)) for edge in matching
        ))
        if edges in omitted:
            continue
        polynomial[bytes(sorted(term))] += 1
    # Distinct matchings can collide only after a specialization, not here.
    require(all(value == 1 for value in polynomial.values()),
            "full aggregate hafnian terms collided")
    require(word == D5.decode_word(code), "word decoder changed")
    return dict(polynomial)


def pair_minor(row, h, first, second):
    answer = {}
    add_scaled(answer, h[second], 1, row[first])
    add_scaled(answer, h[first], -1, row[second])
    return answer


def scalar_minor(first_row, second_row, first, second):
    answer = {}
    add_value(
        answer,
        bytes(sorted(first_row[first] + second_row[second])),
        1,
    )
    add_value(
        answer,
        bytes(sorted(first_row[second] + second_row[first])),
        -1,
    )
    return answer


def triple_minor(a, b, h, first, second, third):
    """det([b;a;H]) on the three selected state columns."""
    p_m = {
        pair: pair_minor(a, h, *pair)
        for pair in ((second, third), (first, third), (first, second))
    }
    answer = {}
    add_scaled(answer, p_m[(second, third)], 1, b[first])
    add_scaled(answer, p_m[(first, third)], -1, b[second])
    add_scaled(answer, p_m[(first, second)], 1, b[third])
    return answer


def common_monomial(polynomials):
    monomials = [monomial for polynomial in polynomials for monomial in polynomial]
    require(monomials, "common monomial requested for empty support")
    common = Counter(monomials[0])
    for monomial in monomials[1:]:
        common &= Counter(monomial)
    return bytes(sorted(common.elements()))


def quotient(monomial, divisor):
    answer = list(monomial)
    for variable in divisor:
        require(variable in answer, "monomial quotient is not exact")
        answer.remove(variable)
    return bytes(answer)


def matching_key(matching):
    return tuple(sorted(tuple(sorted(edge)) for edge in matching))


def audit():
    require(set(M) & set(N) == {(0, 2), (1, 3)},
            "the common matching core changed")
    symmetric_difference = tuple(sorted(set(M) ^ set(N)))
    require(symmetric_difference
            == ((4, 5), (4, 7), (5, 6), (6, 7)),
            "M symmetric-difference N is not the frozen alternating C4")

    a = {code: matching_monomial(M, code) for code in STATES}
    b = {code: matching_monomial(N, code) for code in STATES}
    h = {code: hafnian(code) for code in STATES}
    h_without_bases = {
        code: hafnian(code, omit=(matching_key(M), matching_key(N)))
        for code in STATES
    }
    require(all(len(h[code]) == 105 for code in STATES),
            "eight-site hafnian term census changed")
    require(all(len(h_without_bases[code]) == 103 for code in STATES),
            "removing the two matching rows changed the cofactor census")

    pair_records = []
    p_m = {}
    p_n = {}
    deltas = {}
    for left_index, first in enumerate(STATES):
        for second in STATES[left_index + 1:]:
            key = (first, second)
            p_m[key] = pair_minor(a, h, first, second)
            p_n[key] = pair_minor(b, h, first, second)
            deltas[key] = scalar_minor(a, b, first, second)

            # Endpoint Pluecker exchange:
            # b_i P^M_ij - a_i P^N_ij = Delta^MN_ij H_i,
            # and the identical formula at endpoint j.
            for endpoint in (first, second):
                identity = {}
                add_scaled(identity, p_m[key], 1, b[endpoint])
                add_scaled(identity, p_n[key], -1, a[endpoint])
                for delta_monomial, delta_coefficient in deltas[key].items():
                    add_scaled(
                        identity,
                        h[endpoint],
                        -delta_coefficient,
                        delta_monomial,
                    )
                require(not identity,
                        "an endpoint C4 exchange identity failed")

            gcd_m = common_monomial((p_m[key],))
            gcd_n = common_monomial((p_n[key],))
            pair_records.append({
                "states": list(key),
                "M_transport_terms": len(p_m[key]),
                "N_transport_terms": len(p_n[key]),
                "exchange_minor_terms": len(deltas[key]),
                "M_transport_gcd_degree": len(gcd_m),
                "N_transport_gcd_degree": len(gcd_n),
                "M_primitive_degree": sorted(set(
                    len(quotient(term, gcd_m)) for term in p_m[key]
                )),
                "N_primitive_degree": sorted(set(
                    len(quotient(term, gcd_n)) for term in p_n[key]
                )),
            })

    triple_records = []
    triples = []
    for omitted in range(4):
        triple = tuple(
            state for index, state in enumerate(STATES) if index != omitted
        )
        triples.append(triple)
        first, second, third = triple
        c = triple_minor(a, b, h, first, second, third)

        # The opposite matching-row contraction has the opposite sign.
        opposite = {}
        for scalar, state, pair in (
            (1, first, (second, third)),
            (-1, second, (first, third)),
            (1, third, (first, second)),
        ):
            add_scaled(opposite, p_n[pair], scalar, a[state])
        comparison = dict(c)
        add_scaled(comparison, opposite, 1)
        require(not comparison,
                "the two matching contractions are not opposite")

        # Expansion along the H row uses the C4 exchange minors.
        delta_expansion = {}
        for scalar, state, pair in (
            (1, first, (second, third)),
            (-1, second, (first, third)),
            (1, third, (first, second)),
        ):
            for delta_monomial, delta_coefficient in deltas[pair].items():
                add_scaled(
                    delta_expansion,
                    h[state],
                    scalar * delta_coefficient,
                    delta_monomial,
                )
        comparison = dict(c)
        add_scaled(comparison, delta_expansion, 1)
        require(not comparison,
                "the matching-exchange Bianchi expansion changed sign")

        # Contributions H=m_M and H=m_N vanish separately.  Therefore the
        # curvature is supported away from both input base matchings.
        c_without_bases = triple_minor(
            a, b, h_without_bases, first, second, third
        )
        require(c == c_without_bases,
                "a base matching survived its own exchange determinant")
        triples[-1] = (triple, c)
        triple_records.append({
            "states": list(triple),
            "terms": len(c),
            "degree_histogram": dict(sorted(Counter(map(len, c)).items())),
            "coefficient_histogram": dict(sorted(Counter(c.values()).items())),
        })

    c_by_omitted = {
        omitted: triples[omitted][1] for omitted in range(4)
    }
    # Signed Laplace relation for each matching row.  These are the literal
    # tetrahedral 3-cell boundaries beyond the pairwise Bianchi identities.
    for row_name, row in (("M", a), ("N", b)):
        tetrahedron = {}
        for omitted, state in enumerate(STATES):
            add_scaled(
                tetrahedron,
                c_by_omitted[omitted],
                1 if omitted % 2 == 0 else -1,
                row[state],
            )
        require(not tetrahedron,
                f"the {row_name}-row tetrahedral 3-cell failed")

    ledger = {
        "states": list(STATES),
        "state_words": {
            str(code): list(D5.decode_word(code)) for code in STATES
        },
        "matching_M": [list(edge) for edge in M],
        "matching_N": [list(edge) for edge in N],
        "alternating_C4": [list(edge) for edge in symmetric_difference],
        "hafnian_terms_per_state": 105,
        "hafnian_terms_after_removing_M_N": 103,
        "pair_exchange_identities": 12,
        "pair_records": pair_records,
        "triple_exchange_identities": 4,
        "triple_records": triple_records,
        "tetrahedral_row_syzygies": 2,
        "conclusion": (
            "the alternating-C4 matching exchange has exact endpoint, "
            "Bianchi, and tetrahedral source coherences"
        ),
        "scope_guard": (
            "this closes one C4 exchange 3-cell; it does not prove global "
            "exactness after gluing every matching row or diagonalizing labels"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return ledger, digest


def main():
    ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "frozen C4 exchange 3-cell ledger changed")
    print(
        "n=8 chart26 C4 exchange 3-cell: PASS; "
        "endpoint=12, Bianchi=4, tetrahedra=2"
    )
    print(json.dumps(ledger, sort_keys=True))
    print("sha256:", digest)


if __name__ == "__main__":
    main()

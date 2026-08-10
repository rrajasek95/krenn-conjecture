#!/usr/bin/env python3
"""Exact source-relative audit of the h=3 twenty-cut terminal class.

The calculation keeps literal endpoint-labelled q cells and endpoint-star
cells.  It proves the polynomial identity recorded in
notes/h3-three-set-source-relative-terminal-class.md; in particular it does
not assume that a physical binary cut has the canonical response two-jet.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations


W = tuple(range(6))
EDGES = tuple(combinations(W, 2))
THREE_SETS = tuple(combinations(W, 3))


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def edge(left, right):
    return (left, right) if left < right else (right, left)


@lru_cache(maxsize=None)
def matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], start=1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(rest):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def clean(polynomial):
    return Counter(
        {
            monomial: coefficient
            for monomial, coefficient in polynomial.items()
            if coefficient
        }
    )


def constant(value):
    return Counter({(): Fraction(value)}) if value else Counter()


def variable(name):
    return Counter({(name,): Fraction(1)})


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return clean(answer)


def scale(polynomial, scalar):
    scalar = Fraction(scalar)
    return clean(
        Counter(
            {
                monomial: scalar * coefficient
                for monomial, coefficient in polynomial.items()
            }
        )
    )


def subtract(left, right):
    return add(left, scale(right, -1))


def multiply(*polynomials):
    answer = constant(1)
    for polynomial in polynomials:
        product = Counter()
        for left_monomial, left_coefficient in answer.items():
            for right_monomial, right_coefficient in polynomial.items():
                product[tuple(sorted(left_monomial + right_monomial))] += (
                    left_coefficient * right_coefficient
                )
        answer = clean(product)
    return answer


def polynomial_sum(polynomials):
    return add(*tuple(polynomials))


def q_cell(left, right, left_label, right_label):
    """Literal endpoint-ordered internal cell on the unordered edge."""

    if left > right:
        return q_cell(right, left, right_label, left_label)
    return variable(f"q{left}{right}_{left_label}{right_label}")


def p_star(site, label):
    return variable(f"p{site}_{label}")


def s_star(site, label):
    return variable(f"s{site}_{label}")


ALPHA = variable("alpha")


def response_edge(left, right, labels):
    return add(
        multiply(p_star(left, labels[left]), s_star(right, labels[right])),
        multiply(p_star(right, labels[right]), s_star(left, labels[left])),
    )


def word_quadratic(labels):
    return {
        selected: q_cell(*selected, labels[selected[0]], labels[selected[1]])
        for selected in EDGES
    }


def word_response(labels):
    return {selected: response_edge(*selected, labels) for selected in EDGES}


def hafnian(entries):
    return polynomial_sum(
        multiply(*(entries[edge(*selected)] for selected in matching))
        for matching in matchings(W)
    )


def one_response_coefficient(response, quadratic):
    answer = Counter()
    for matching in matchings(W):
        for marked in range(3):
            factors = [
                response[edge(*selected)] if position == marked else quadratic[edge(*selected)]
                for position, selected in enumerate(matching)
            ]
            answer.update(multiply(*factors))
    return clean(answer)


PURE_LABELS = (0,) * len(W)
Q = word_quadratic(PURE_LABELS)
R = word_response(PURE_LABELS)


def response_layer(number):
    answer = Counter()
    for matching in matchings(W):
        for chosen in combinations(range(3), number):
            chosen = frozenset(chosen)
            answer.update(
                multiply(
                    *(
                        R[edge(*selected)] if position in chosen else Q[edge(*selected)]
                        for position, selected in enumerate(matching)
                    )
                )
            )
    return clean(answer)


Q2 = response_layer(2)
Q3 = response_layer(3)
H2 = add(multiply(ALPHA, Q2), scale(Q3, 3))
CHI = add(multiply(ALPHA, Q2), Q3)


def theta(marked, second, first, leading):
    marked = tuple(sorted(marked))
    outside = tuple(site for site in W if site not in marked)
    answer = Counter()
    for inside_pair in combinations(marked, 2):
        remaining_inside = next(site for site in marked if site not in inside_pair)
        for outside_endpoint in outside:
            remaining_outside = tuple(
                site for site in outside if site != outside_endpoint
            )
            answer.update(
                multiply(
                    second[edge(*inside_pair)],
                    first[edge(remaining_inside, outside_endpoint)],
                    leading[edge(*remaining_outside)],
                )
            )
    # The three-crossing part is the 3 by 3 permanent.
    for assigned in permutations(outside):
        answer.update(
            multiply(
                *(
                    first[edge(left, right)]
                    for left, right in zip(marked, assigned)
                )
            )
        )
    return clean(answer)


CANONICAL_SECOND = {
    selected: multiply(scale(ALPHA, 2), R[selected]) for selected in EDGES
}


def target(endpoint_left, endpoint_right, word):
    """GHZ target of the literal full row F_{ij}(word)."""

    return int(
        endpoint_left == endpoint_right
        and all(label == endpoint_left for label in word)
    )


def audit():
    cut_sum = Counter()
    physical_row_sum = Counter()
    landing_error_sum = Counter()
    companion_sum = Counter()

    for marked in THREE_SETS:
        marked_set = frozenset(marked)
        word = tuple(int(site in marked_set) for site in W)
        physical_q = word_quadratic(word)
        physical_r = word_response(word)

        physical_middle = hafnian(physical_q)
        # This independent matching formula must agree with the literal
        # three-set connection-plus-permanent expansion.
        physical_theta = theta(marked, physical_q, physical_q, physical_q)
        require(
            physical_middle == physical_theta,
            ("literal cut formula", marked),
        )

        canonical = theta(marked, CANONICAL_SECOND, R, Q)
        companion = one_response_coefficient(physical_r, physical_q)
        physical_row = add(multiply(ALPHA, physical_middle), companion)

        cut_sum.update(canonical)
        landing_error_sum.update(subtract(physical_middle, canonical))
        companion_sum.update(companion)
        physical_row_sum.update(physical_row)

        # The selected row uses two distinct exposed endpoint labels a,b.
        # Every 3+3 word is mixed, so its GHZ target is literally zero.
        require(target(0, 1, word) == 0, ("off-diagonal target", marked))
        # The same is true even for either diagonal row: the word is not
        # constant.  This checks that no diagonal augmentation is hidden in
        # the twenty middle rows themselves.
        require(target(0, 0, word) == 0, ("diagonal-0 cut target", marked))
        require(target(1, 1, word) == 0, ("diagonal-1 cut target", marked))

    cut_sum = clean(cut_sum)
    physical_row_sum = clean(physical_row_sum)
    landing_error_sum = clean(landing_error_sum)
    companion_sum = clean(companion_sum)

    require(
        cut_sum == scale(CHI, 8),
        "canonical twenty-cut marking identity changed",
    )

    connecting_class = add(
        companion_sum,
        multiply(ALPHA, landing_error_sum),
    )

    # K - 16 alpha Q3 = sum_S F_ab(w_S) - 8 alpha H2.
    left = subtract(connecting_class, scale(multiply(ALPHA, Q3), 16))
    right = subtract(physical_row_sum, scale(multiply(ALPHA, H2), 8))
    require(left == right, "source-relative terminal identity changed")

    # Equivalently, before H2, K=-8 alpha chi modulo the twenty rows.
    require(
        physical_row_sum
        == add(connecting_class, scale(multiply(ALPHA, CHI), 8)),
        "pre-H2 relative identity changed",
    )

    # Pure diagonal rows carry target one.  Any Bianchi transport using
    # them must use the normalized equations F_ii(i^6)-1, not F_ii=0.
    require(target(0, 0, (0,) * 6) == 1, "colour-0 anchor target changed")
    require(target(1, 1, (1,) * 6) == 1, "colour-1 anchor target changed")
    require(target(2, 2, (2,) * 6) == 1, "colour-2 anchor target changed")

    ledger_lines = []
    for name, polynomial in (
        ("cut_sum", cut_sum),
        ("landing_error", landing_error_sum),
        ("companion_sum", companion_sum),
        ("connecting_class", connecting_class),
        ("physical_row_sum", physical_row_sum),
    ):
        ledger_lines.append(f"{name}:{len(polynomial)}")
        for monomial, coefficient in sorted(polynomial.items()):
            ledger_lines.append(
                f"{name}|{'*'.join(monomial) or '1'}|"
                f"{coefficient.numerator}/{coefficient.denominator}"
            )
    digest = sha256("\n".join(ledger_lines).encode()).hexdigest()
    expected = "22f2418741c6dbeae3dc55f0637cab6fef5392843012da75228b49f347919527"
    require(digest == expected, ("ledger digest", digest))

    return {
        "cuts": len(THREE_SETS),
        "cut_terms": len(cut_sum),
        "landing_terms": len(landing_error_sum),
        "companion_terms": len(companion_sum),
        "class_terms": len(connecting_class),
        "row_terms": len(physical_row_sum),
        "digest": digest,
    }


def main():
    ledger = audit()
    print(
        "h=3 three-set source-relative terminal class: PASS; "
        f"cuts={ledger['cuts']}; cut/landing/companion/class/rows="
        f"{ledger['cut_terms']}/{ledger['landing_terms']}/"
        f"{ledger['companion_terms']}/{ledger['class_terms']}/"
        f"{ledger['row_terms']}"
    )
    print(f"ledger_sha256={ledger['digest']}")
    print("relative identity: K-16*alpha*Q3=sum(F_ab(w_S))-8*alpha*H2")
    print("target audit: all twenty 3+3 rows are zero-target; pure anchors require -1")


if __name__ == "__main__":
    main()

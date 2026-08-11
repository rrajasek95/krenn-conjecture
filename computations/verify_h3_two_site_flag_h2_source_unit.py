#!/usr/bin/env python3
"""Verify the parametric two-site-flag Hamming-two source unit.

The calculation is deliberately dependency-free.  Polynomials are sparse
integer dictionaries whose monomials are sorted tuples of variable names.
"""

from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json


SITES = tuple(range(6))
MATCHING = ((0, 1), (2, 3), (4, 5))
MATCHING_SET = set(MATCHING)

WORD_A = (0, 0, 1, 1, 1, 1)
WORD_B = (0, 0, 0, 0, 1, 1)
WORD_C = (0, 0, 1, 1, 0, 0)
WORD_ZERO = (0,) * 6


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, 0) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def scale(coefficient, polynomial):
    if not coefficient:
        return {}
    return {
        monomial: coefficient * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def multiply(left, right):
    answer = {}
    for first, first_value in left.items():
        for second, second_value in right.items():
            monomial = tuple(sorted(first + second))
            answer[monomial] = answer.get(monomial, 0) + first_value * second_value
            if not answer[monomial]:
                del answer[monomial]
    return answer


def constant(value):
    return {} if not value else {(): value}


def variable(name):
    return {(name,): 1}


@lru_cache(maxsize=None)
def matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position, partner in enumerate(vertices[1:], 1):
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in matchings(rest):
            answer.append(((first, partner),) + matching)
    return tuple(answer)


def q_entry(x, y, first_color, second_color, mutation=None):
    if x > y:
        x, y, first_color, second_color = y, x, second_color, first_color
    key = (x, y, first_color, second_color)
    if mutation is not None and key == mutation:
        return variable("q_mut")
    if first_color == second_color:
        return constant(int((x, y) in MATCHING_SET))
    return variable(f"q{x}{y}_{first_color}{second_color}")


def hafnian(word, vertices=SITES, mutation=None):
    answer = {}
    for matching in matchings(tuple(vertices)):
        term = constant(1)
        for x, y in matching:
            term = multiply(term, q_entry(x, y, word[x], word[y], mutation))
        answer = add(answer, term)
    return answer


# The two-site triangular flag, restricted to colors 0 and 1.  The unused
# parameters are retained so the verifier reconstructs the literal rows
# rather than starting from their already-simplified forms.
P = {
    (0, 0): variable("A"),
    (1, 0): variable("B"),
    (1, 1): variable("C"),
}
S0 = {(0, 1): variable("D")}
S1 = {
    (0, 0): variable("E"),
    (0, 1): variable("F"),
    (1, 1): variable("G"),
}


def response(first, second, word, mutation=None):
    answer = {}
    for x, y in combinations(SITES, 2):
        coefficient = add(
            multiply(first.get((x, word[x]), {}), second.get((y, word[y]), {})),
            multiply(first.get((y, word[y]), {}), second.get((x, word[x]), {})),
        )
        if not coefficient:
            continue
        complement = tuple(site for site in SITES if site not in (x, y))
        answer = add(answer, multiply(coefficient, hafnian(word, complement, mutation)))
    return answer


def source_row(direct, second, word, mutation=None):
    return add(
        multiply(variable(direct), hafnian(word, mutation=mutation)),
        response(P, second, word, mutation),
    )


def certificate(mutation=None, star_mutation=False):
    second_one = dict(S1)
    if star_mutation:
        second_one[(2, 0)] = variable("s_mut")

    f00_a = source_row("d00", S0, WORD_A, mutation)
    f01_b = source_row("d01", second_one, WORD_B, mutation)
    f01_c = source_row("d01", second_one, WORD_C, mutation)
    f01_zero = source_row("d01", second_one, WORD_ZERO, mutation)
    k_b = hafnian(WORD_B, vertices=(2, 3, 4, 5), mutation=mutation)
    k_c = hafnian(WORD_C, vertices=(2, 3, 4, 5), mutation=mutation)

    total = add(
        multiply(variable("d01"), f00_a),
        scale(-1, multiply(variable("d00"), f01_b)),
        scale(-1, multiply(variable("d00"), f01_c)),
        multiply(multiply(variable("d00"), add(k_b, k_c)), f01_zero),
    )
    target = multiply(variable("d00"), variable("d01"))
    return {
        "f00_a": f00_a,
        "f01_b": f01_b,
        "f01_c": f01_c,
        "f01_zero": f01_zero,
        "k_b": k_b,
        "k_c": k_c,
        "total": total,
        "target": target,
    }


def main():
    data = certificate()
    require(data["total"] == data["target"], ("source unit moved", data["total"]))

    matching_identity = add(
        hafnian(WORD_A),
        scale(-1, hafnian(WORD_B)),
        scale(-1, hafnian(WORD_C)),
        data["k_b"],
        data["k_c"],
    )
    require(matching_identity == constant(1), ("matching identity moved", matching_identity))

    # The known chi=-12 specialization has d00=d01=1 and B*E=-1, so its
    # pure crossed row vanishes and the four-row identity becomes the frozen
    # three-row unit.  This substitution is evaluated directly.
    specialization = {"d00": 1, "d01": 1, "B": 1, "E": -1}

    def evaluate(polynomial):
        answer = {}
        for monomial, coefficient in polynomial.items():
            remaining = []
            value = coefficient
            for name in monomial:
                if name in specialization:
                    value *= specialization[name]
                else:
                    remaining.append(name)
            if value:
                key = tuple(remaining)
                answer[key] = answer.get(key, 0) + value
                if not answer[key]:
                    del answer[key]
        return answer

    require(evaluate(data["f01_zero"]) == {}, "pure crossed row did not vanish")
    three_row = add(
        evaluate(data["f00_a"]),
        scale(-1, evaluate(data["f01_b"])),
        scale(-1, evaluate(data["f01_c"])),
    )
    require(three_row == constant(1), ("three-row specialization moved", three_row))

    # Both the common pure matching and the triangular star flag are
    # load-bearing.  A forbidden diagonal cell or an outside star component
    # must destroy the polynomial identity.
    diagonal_mutation = certificate(mutation=(2, 4, 1, 1))
    require(diagonal_mutation["total"] != diagonal_mutation["target"],
            "forbidden diagonal mutation was not detected")
    star_mutation = certificate(star_mutation=True)
    require(star_mutation["total"] != star_mutation["target"],
            "outside-star mutation was not detected")

    ledger = {
        "arbitrary_ordered_cross_q_variables": 30,
        "binary_diagonal_support": [f"{x}{y}" for x, y in MATCHING],
        "certificate_rows": [
            "F00(001111)",
            "F01(000011)",
            "F01(001100)",
            "F01(000000)",
        ],
        "certificate_multipliers": [
            "d01", "-d00", "-d00", "d00*(K_B+K_C)"
        ],
        "certificate_target": "d00*d01",
        "matching_identity_terms": len(matching_identity),
        "row_term_counts": {
            key: len(data[key])
            for key in ("f00_a", "f01_b", "f01_c", "f01_zero", "k_b", "k_c")
        },
        "three_row_specialization": 1,
        "mutations_detected": ["24:11", "S1(2,0)"],
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    expected = "3a7d50571c60218c267b97e0464b6f32c8ad059f317aa77d6af8ced96322e45a"
    require(digest == expected, ("ledger changed", digest, ledger))
    print("h=3 two-site-flag Hamming-two source unit: PASS")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

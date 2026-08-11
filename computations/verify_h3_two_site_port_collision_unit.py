#!/usr/bin/env python3
"""Verify the unrestricted-q two-site port collision identities.

The four source rows are reconstructed from the endpoint-coloured matching
formula.  Internal binary q-cells are independent variables; in particular,
no diagonal matching support is fixed.
"""

from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json


SITES = tuple(range(6))
ZERO = (0, 0, 0, 0, 0, 0)
PORT_WORDS = {
    "00": ZERO,
    "01": (0, 1, 0, 0, 0, 0),
    "10": (1, 0, 0, 0, 0, 0),
    "11": (1, 1, 0, 0, 0, 0),
}


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


def q_entry(x, y, first_colour, second_colour):
    if x > y:
        x, y, first_colour, second_colour = (
            y,
            x,
            second_colour,
            first_colour,
        )
    return variable(f"q{x}{y}_{first_colour}{second_colour}")


def hafnian(word, vertices=SITES):
    answer = {}
    for matching in matchings(tuple(vertices)):
        term = constant(1)
        for x, y in matching:
            term = multiply(term, q_entry(x, y, word[x], word[y]))
        answer = add(answer, term)
    return answer


def generic_quadratic_entry(prefix, x, y, first_colour, second_colour):
    if x > y:
        x, y, first_colour, second_colour = (
            y,
            x,
            second_colour,
            first_colour,
        )
    return variable(f"{prefix}{x}{y}_{first_colour}{second_colour}")


def quadratic_hafnian(entry, word):
    answer = {}
    for matching in matchings(SITES):
        term = constant(1)
        for x, y in matching:
            term = multiply(term, entry(x, y, word[x], word[y]))
        answer = add(answer, term)
    return answer


def divided_square_times(entry, other, word):
    """Coefficient of entry^[2] * other on full six-site support."""
    answer = {}
    for matching in matchings(SITES):
        for other_position in range(3):
            term = constant(1)
            for position, (x, y) in enumerate(matching):
                chosen = other if position == other_position else entry
                term = multiply(term, chosen(x, y, word[x], word[y]))
            answer = add(answer, term)
    return answer


def three_distinct_quadratics(first, second, third, word):
    """Coefficient of first * second * third on full six-site support."""
    answer = {}
    assignments = (
        (first, second, third),
        (first, third, second),
        (second, first, third),
        (second, third, first),
        (third, first, second),
        (third, second, first),
    )
    for matching in matchings(SITES):
        for chosen_entries in assignments:
            term = constant(1)
            for chosen, (x, y) in zip(chosen_entries, matching):
                term = multiply(term, chosen(x, y, word[x], word[y]))
            answer = add(answer, term)
    return answer


def one_times_divided_square(first, second, word):
    """Coefficient of first * second^[2] on full six-site support."""
    answer = {}
    for matching in matchings(SITES):
        for first_position in range(3):
            term = constant(1)
            for position, (x, y) in enumerate(matching):
                chosen = first if position == first_position else second
                term = multiply(term, chosen(x, y, word[x], word[y]))
            answer = add(answer, term)
    return answer


# The same triangular port as in the preceding Hamming-two theorem.  Only
# colours zero and one are relevant to the four displayed output words.
P0 = {
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


def response(first, second, word):
    answer = {}
    for x, y in combinations(SITES, 2):
        coefficient = add(
            multiply(first.get((x, word[x]), {}), second.get((y, word[y]), {})),
            multiply(first.get((y, word[y]), {}), second.get((x, word[x]), {})),
        )
        if not coefficient:
            continue
        complement = tuple(site for site in SITES if site not in (x, y))
        answer = add(answer, multiply(coefficient, hafnian(word, complement)))
    return answer


def source_row(direct, second, word, target=False):
    answer = add(
        multiply(variable(direct), hafnian(word)),
        response(P0, second, word),
    )
    if target:
        answer = add(answer, constant(-1))
    return answer


def polynomial_variables(polynomial):
    return {
        name
        for monomial in polynomial
        for name in monomial
    }


def main():
    d00 = variable("d00")
    d01 = variable("d01")
    be = multiply(variable("B"), variable("E"))
    j_port = add(
        multiply(variable("A"), variable("G")),
        multiply(variable("C"), variable("E")),
    )
    l_port = add(
        multiply(d01, variable("D")),
        scale(-1, multiply(d00, variable("F"))),
    )

    q_complement = hafnian(ZERO, vertices=(2, 3, 4, 5))
    expected_responses = {
        "00": ({}, multiply(be, q_complement)),
        "01": ({}, multiply(j_port, q_complement)),
        "10": (
            multiply(multiply(variable("B"), variable("D")), q_complement),
            multiply(multiply(variable("B"), variable("F")), q_complement),
        ),
        "11": (
            multiply(multiply(variable("C"), variable("D")), q_complement),
            multiply(multiply(variable("C"), variable("F")), q_complement),
        ),
    }

    rows = {}
    differences = {}
    for label, word in PORT_WORDS.items():
        row00 = source_row("d00", S0, word, target=(label == "00"))
        row01 = source_row("d01", S1, word)
        require(
            response(P0, S0, word) == expected_responses[label][0],
            ("00 response factorization moved", label),
        )
        require(
            response(P0, S1, word) == expected_responses[label][1],
            ("01 response factorization moved", label),
        )
        rows[("00", label)] = row00
        rows[("01", label)] = row01
        differences[label] = add(
            multiply(d01, row00),
            scale(-1, multiply(d00, row01)),
        )

    u = {
        "00": scale(-1, multiply(d00, be)),
        "01": scale(-1, multiply(d00, j_port)),
        "10": multiply(variable("B"), l_port),
        "11": multiply(variable("C"), l_port),
    }
    expected_differences = {
        "00": add(scale(-1, d01), multiply(u["00"], q_complement)),
        "01": multiply(u["01"], q_complement),
        "10": multiply(u["10"], q_complement),
        "11": multiply(u["11"], q_complement),
    }
    require(
        differences == expected_differences,
        ("port difference factorization moved", differences),
    )

    # The aligned conclusion is a tensor statement, not only the 0000
    # coefficient checked above.  Reconstruct all 64 binary output words.
    # After J=L=0, only port word 00 survives, and its coefficient is the
    # arbitrary four-site divided-square tensor plus the one pure target.
    aligned_word_ledger = {}
    for word in product(range(2), repeat=6):
        port = f"{word[0]}{word[1]}"
        row00 = source_row("d00", S0, word, target=(word == ZERO))
        row01 = source_row("d01", S1, word)
        difference = add(
            multiply(d01, row00),
            scale(-1, multiply(d00, row01)),
        )
        complement_word = (0, 0) + word[2:]
        q_coefficient = hafnian(complement_word, vertices=(2, 3, 4, 5))
        expected = multiply(u[port], q_coefficient)
        if word == ZERO:
            expected = add(expected, scale(-1, d01))
        require(
            difference == expected,
            ("all-word port factorization moved", word, difference),
        )
        aligned_word_ledger["".join(map(str, word))] = {
            "port": port,
            "terms": len(difference),
        }

    # For any nonzero port word, the two direct terms cancel first.  Both
    # response differences then contain the same arbitrary four-site
    # cofactor, so their 2x2 determinant is an ordinary source constant.
    for label in ("01", "10", "11"):
        identity = add(
            multiply(u[label], differences["00"]),
            scale(-1, multiply(u["00"], differences[label])),
        )
        expected = scale(-1, multiply(d01, u[label]))
        require(identity == expected, ("port collision identity moved", label, identity))

    # In the 01 channel both 00-response coefficients vanish.  Cancelling
    # their common d00 factor gives the sharper four-row unit used in the
    # proof note.
    sharp_identity = add(
        scale(-1, multiply(multiply(d01, j_port), rows[("00", "00")])),
        multiply(multiply(d00, j_port), rows[("01", "00")]),
        multiply(multiply(d01, be), rows[("00", "01")]),
        scale(-1, multiply(multiply(d00, be), rows[("01", "01")])),
    )
    sharp_target = multiply(d01, j_port)
    require(sharp_identity == sharp_target, ("sharp port unit moved", sharp_identity))

    # On the aligned boundary the cap
    #
    #        K0 = d01 E_00 - d00 E_01
    #
    # has zero direct scalar and response r0=p0(d01*s0-d00*s1).
    # Equations J=L=0 make r0 the single literal edge
    # -d00*B*E e0@0 e0@1.  It is therefore square-zero.  Along the
    # identity direction K(z)=K0+zI, write tau=s(I) and b=r(I).  The h=3
    # clean error has the universal double-root factorization
    #
    # E(z)=z^2*r0*(tau*b*q+b^[2])+z^3*(tau*b^[2]*q+b^[3]).
    #
    # Verify this coefficientwise for every binary output word, leaving q
    # and b completely generic.
    z = variable("z")
    tau = variable("tau")
    r0_scalar = scale(-1, multiply(d00, be))

    def r0_entry(x, y, first_colour, second_colour):
        if x > y:
            x, y, first_colour, second_colour = (
                y,
                x,
                second_colour,
                first_colour,
            )
        if (x, y, first_colour, second_colour) == (0, 1, 0, 0):
            return r0_scalar
        return {}

    def b_entry(x, y, first_colour, second_colour):
        return generic_quadratic_entry(
            "b", x, y, first_colour, second_colour
        )

    def r_line_entry(x, y, first_colour, second_colour):
        return add(
            r0_entry(x, y, first_colour, second_colour),
            multiply(z, b_entry(x, y, first_colour, second_colour)),
        )

    double_root_term_counts = {}
    for word in product(range(2), repeat=6):
        r2q = divided_square_times(r_line_entry, q_entry, word)
        r3 = quadratic_hafnian(r_line_entry, word)
        clean_error = add(multiply(multiply(z, tau), r2q), r3)

        r0_b_q = three_distinct_quadratics(r0_entry, b_entry, q_entry, word)
        r0_b2 = one_times_divided_square(r0_entry, b_entry, word)
        b2_q = divided_square_times(b_entry, q_entry, word)
        b3 = quadratic_hafnian(b_entry, word)
        quadratic_coefficient = add(
            multiply(tau, r0_b_q),
            r0_b2,
        )
        cubic_coefficient = add(multiply(tau, b2_q), b3)
        expected_clean_error = add(
            multiply(multiply(z, z), quadratic_coefficient),
            multiply(multiply(multiply(z, z), z), cubic_coefficient),
        )
        require(
            clean_error == expected_clean_error,
            ("aligned cap double-root factorization moved", word),
        )
        double_root_term_counts["".join(map(str, word))] = len(clean_error)

    # A literal one-edge quadratic has zero divided square.  This is the
    # source-algebra reason K0 is a clean (but inactive) cap.
    square_zero_slices = 0
    for vertices in combinations(SITES, 4):
        for local_word in product(range(2), repeat=4):
            # Two copies of r0 would both have to use the same physical
            # edge.  No four-site matching can contain that edge twice.
            word = [0] * 6
            for site, colour in zip(vertices, local_word):
                word[site] = colour
            r0_square = {}
            for matching in matchings(vertices):
                term = constant(1)
                for x, y in matching:
                    term = multiply(
                        term, r0_entry(x, y, word[x], word[y])
                    )
                r0_square = add(r0_square, term)
            require(
                not r0_square,
                ("single-edge cap ceased to be square-zero", vertices, local_word),
            )
            square_zero_slices += 1

    # No internal q-cell is normalized: all 60 endpoint-ordered binary cells
    # exist in the universal coefficient ring.  The four selected words use
    # only the cells compatible with their output colours, as they should.
    q_universe = {
        f"q{x}{y}_{first}{second}"
        for x, y in combinations(SITES, 2)
        for first, second in product(range(2), repeat=2)
    }
    used_variables = set().union(
        *(polynomial_variables(row) for row in rows.values())
    )
    used_q_variables = {
        name for name in used_variables if name.startswith("q")
    }
    require(len(q_universe) == 60, "binary q universe moved")
    require(used_q_variables, "literal rows lost their internal q variables")
    require(used_q_variables <= q_universe, "unknown q variable appeared")

    ledger = {
        "internal_q_specializations": 0,
        "endpoint_ordered_binary_q_universe": len(q_universe),
        "q_variables_used_by_selected_words": len(used_q_variables),
        "port_words": list(PORT_WORDS),
        "universal_collision_channels": ["01", "10", "11"],
        "port_obstructions": {
            "J": "A*G+C*E",
            "L": "d01*D-d00*F",
            "U01": "-d00*J",
            "U10": "B*L",
            "U11": "C*L",
        },
        "sharp_unit_rows": [
            "F00(000000)",
            "F01(000000)",
            "F00(010000)",
            "F01(010000)",
        ],
        "sharp_unit_target": "d01*(A*G+C*E)",
        "aligned_boundary": {
            "conditions": ["J=0", "L=0"],
            "binary_words_checked": len(aligned_word_ledger),
            "only_live_port": "00",
            "tensor_consequence": "q_A^[2]=-d01/(d00*B*E)*Y0^A",
            "cap": "K0=d01*E00-d00*E01",
            "direct_scalar": 0,
            "target_coefficients": ["d01", 0, 0],
            "response": "r0=-d00*B*E*e0@0*e0@1",
            "response_square": 0,
            "response_square_slices_checked": square_zero_slices,
            "cleanliness": "inactive clean cap",
            "identity_line_error": (
                "z^2*r0*(tau*b*q+b^[2])"
                "+z^3*(tau*b^[2]*q+b^[3])"
            ),
            "identity_line_binary_words_checked": len(double_root_term_counts),
        },
        "row_term_counts": {
            f"F{first}_{word}": len(row)
            for (first, word), row in sorted(rows.items())
        },
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    expected_digest = "0ab1a01f6e54c9d4125759c943682f0a16eb99cad8c3a5d372689d91e75fc556"
    require(digest == expected_digest, ("ledger changed", digest, ledger))
    print("h=3 unrestricted-q two-site port collision unit: PASS")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

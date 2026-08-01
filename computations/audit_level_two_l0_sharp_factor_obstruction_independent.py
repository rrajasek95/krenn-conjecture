#!/usr/bin/env python3
"""Independent exact audit of the sharp L0 factor obstruction.

Research evidence only.  Krenn's conjecture remains open.

The rank-sharp six-site packet M from
verify_level_two_three_invertible_l0_obstruction.py has rank(dPsi_M)=55 and
contains literal tangent columns e_(0^6), e_(1^6).  This checker proves the
strictly stronger fact that no arbitrary binary endpoint blocks

    U^0, U^1, V^0, V^1 and W_(s,t)

can realize all four eight-site L0 target slices.  In fact the 00, 11, and
01 slices alone are inconsistent; the 10 slice is not used.

The proof has two independently audited parts.

1. Exact rank 55 and five independent universal gauge kernels identify
   ker(dPsi_M) with the trace-zero vertex gauges.  Absorbing W into the six
   vertex scalars turns each slice into the block equations

     U^s_r (V^t_u)^T + V^t_r (U^s_u)^T
       = E^(s,t)_(ru) + (lambda^(s,t)_r+lambda^(s,t)_u) M_ru.

2. On the K4 induced by residual vertices {0,1,4,5}, 38 of the 72 scalar
   equations have an explicit rational Nullstellensatz certificate

                              sum c_k f_k = 1.

   The certificate has 124 coefficient monomials, coefficient degree at
   most two, and at most eight terms in one multiplier.  It is verified here
   with a tiny standard-library sparse-polynomial implementation rather than
   a computer-algebra dependency.

All checks use exact Fraction/integer arithmetic, raise explicitly, and
remain live under python -O and python -I -S.
"""

from fractions import Fraction as Q
from itertools import combinations, product


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


SITES = tuple(range(6))
COLOURS = (0, 1)
EDGES = tuple(combinations(SITES, 2))
CELLS = tuple((u, v, a, b) for u, v in EDGES
              for a, b in product(COLOURS, repeat=2))
WORDS = tuple(product(COLOURS, repeat=6))


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    head = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        partner = vertices[position]
        rest = vertices[1:position] + vertices[position + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((head, partner),) + tail)
    return tuple(answer)


MATCHINGS = {
    vertices: perfect_matchings(vertices)
    for size in (0, 2, 4, 6)
    for vertices in combinations(SITES, size)
}


def outer(left, right, scale=1):
    return tuple(
        tuple(scale * left[a] * right[b] for b in COLOURS)
        for a in COLOURS
    )


SITE_VECTORS = {site: (site + 1, site + 2) for site in SITES}
E_ZERO = ((1, 0), (0, 0))
E_ONE = ((0, 0), (0, 1))
BLOCKS = {
    (0, 1): outer(SITE_VECTORS[0], SITE_VECTORS[1]),
    (0, 2): E_ONE,
    (0, 3): outer(SITE_VECTORS[0], (1, 0)),
    (0, 4): ((5, 6), (11, 8)),
    (0, 5): ((6, 7), (13, 9)),
    (1, 2): outer(SITE_VECTORS[1], (1, 0), -1),
    (1, 3): E_ONE,
    (1, 4): ((6, 8), (12, 11)),
    (1, 5): ((7, 9), (14, 12)),
    (2, 3): E_ZERO,
    (2, 4): outer(SITE_VECTORS[2], SITE_VECTORS[4]),
    (2, 5): outer(SITE_VECTORS[2], SITE_VECTORS[5]),
    (3, 4): outer(SITE_VECTORS[3], SITE_VECTORS[4], -1),
    (3, 5): outer(SITE_VECTORS[3], SITE_VECTORS[5]),
    (4, 5): E_ZERO,
}
M = {
    (u, v, a, b): BLOCKS[u, v][a][b]
    for u, v in EDGES
    for a, b in product(COLOURS, repeat=2)
}


def hafnian(packet, vertices, word):
    vertices = tuple(sorted(vertices))
    total = 0
    for matching in MATCHINGS[vertices]:
        term = 1
        for u, v in matching:
            term *= packet[u, v, word[u], word[v]]
        total += term
    return total


def cofactor(packet, word, u, v):
    remaining = tuple(site for site in SITES if site not in (u, v))
    return hafnian(packet, remaining, word)


def differential_matrix(packet):
    return [
        [
            cofactor(packet, word, u, v)
            if (word[u], word[v]) == (a, b) else 0
            for u, v, a, b in CELLS
        ]
        for word in WORDS
    ]


def apply_matrix(matrix, vector):
    return [
        sum(entry * coefficient for entry, coefficient in zip(row, vector))
        for row in matrix
    ]


def rational_rank(matrix):
    rows = [[Q(value) for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next((slot for slot in range(rank, len(rows))
                      if rows[slot][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for slot in range(len(rows)):
            if slot == rank or not rows[slot][column]:
                continue
            multiple = rows[slot][column]
            rows[slot] = [left - multiple * right
                          for left, right in zip(rows[slot], rows[rank])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def modular_rank(matrix, prime):
    rows = [[value % prime for value in row] for row in matrix]
    rank = 0
    width = len(rows[0]) if rows else 0
    for column in range(width):
        pivot = next((slot for slot in range(rank, len(rows))
                      if rows[slot][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inverse = pow(rows[rank][column], -1, prime)
        rows[rank] = [(value * inverse) % prime for value in rows[rank]]
        for slot in range(len(rows)):
            if slot == rank or not rows[slot][column]:
                continue
            multiple = rows[slot][column]
            rows[slot] = [
                (left - multiple * right) % prime
                for left, right in zip(rows[slot], rows[rank])
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def ranks_over_three_fields(matrix):
    return (
        rational_rank(matrix),
        modular_rank(matrix, 101),
        modular_rank(matrix, 1_000_003),
    )


def audit_rank_kernel_and_targets():
    derivative = differential_matrix(M)
    mixed = [
        row for row, word in zip(derivative, WORDS)
        if word not in ((0,) * 6, (1,) * 6)
    ]
    require(ranks_over_three_fields(derivative) == (55, 55, 55),
            "the sharp packet no longer has differential rank 55")
    require(ranks_over_three_fields(mixed) == (53, 53, 53),
            "the sharp packet no longer has mixed rank 53")

    pure_zero = [int(word == (0,) * 6) for word in WORDS]
    pure_one = [int(word == (1,) * 6) for word in WORDS]
    zero_column = CELLS.index((0, 1, 0, 0))
    one_column = CELLS.index((4, 5, 1, 1))
    require([row[zero_column] for row in derivative] == pure_zero,
            "cell (01,00) is no longer the literal e_(0^6) preimage")
    require([row[one_column] for row in derivative] == pure_one,
            "cell (45,11) is no longer the literal e_(1^6) preimage")

    gauges = []
    for basis in range(5):
        mu = [0] * 6
        mu[basis] = 1
        mu[5] = -1
        tangent = [
            (mu[u] + mu[v]) * M[u, v, a, b]
            for u, v, a, b in CELLS
        ]
        require(not any(apply_matrix(derivative, tangent)),
                ("a universal gauge direction left the kernel", basis))
        gauges.append(tangent)
    require(rational_rank(gauges) == 5,
            "the five trace-zero gauge directions are dependent")
    # Rank 55 gives nullity 5, so the five gauges are the entire kernel.

    slope = [hafnian(M, SITES, word) for word in WORDS]
    radial = [M[cell] for cell in CELLS]
    require(
        apply_matrix(derivative, radial) == [3 * value for value in slope],
        "Euler's identity D(M)=3 Psi(M) failed",
    )
    mu = (1, -2, 3, -4, 5, -3)
    require(sum(mu) == 0, "the direct-absorption gauge is not trace zero")
    for direct in (-7, 5):
        lam = tuple(Q(value) - Q(direct, 6) for value in mu)
        require(sum(lam) == -direct,
                "the endpoint direct cell was not recovered from lambda")
        require(all(
            lam[r] + lam[u]
            == Q(mu[r] + mu[u]) - Q(direct, 3)
            for r, u in EDGES
        ), "the endpoint direct cell was not absorbed edgewise")
    return derivative


# Sparse polynomials are dictionaries monomial -> exact rational coefficient.
# A monomial is a sorted tuple of variable names; repetition is retained.
ZERO = {}
ONE = {(): Q(1)}


def polynomial_term(coefficient, *variables):
    coefficient = Q(coefficient)
    return {} if not coefficient else {tuple(sorted(variables)): coefficient}


def polynomial_add(*polynomials):
    answer = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            answer[monomial] = answer.get(monomial, Q(0)) + coefficient
            if not answer[monomial]:
                del answer[monomial]
    return answer


def polynomial_scale(polynomial, coefficient):
    coefficient = Q(coefficient)
    return {
        monomial: coefficient * value
        for monomial, value in polynomial.items()
        if coefficient * value
    }


def polynomial_multiply(left, right):
    answer = {}
    for left_monomial, left_value in left.items():
        for right_monomial, right_value in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            answer[monomial] = (
                answer.get(monomial, Q(0)) + left_value * right_value
            )
            if not answer[monomial]:
                del answer[monomial]
    return answer


def parse_multiplier(text):
    """Parse the small Singular-style coefficient grammar used below."""

    normalized = text.replace(" ", "").replace("-", "+-")
    answer = {}
    for raw_term in normalized.split("+"):
        if not raw_term:
            continue
        sign = 1
        if raw_term.startswith("-"):
            sign = -1
            raw_term = raw_term[1:]
        factors = raw_term.split("*")
        coefficient = Q(sign)
        variables = []
        for factor in factors:
            if "/" in factor:
                numerator, denominator = factor.split("/")
                require(numerator.isdigit() and denominator.isdigit(),
                        ("invalid rational factor", factor))
                coefficient *= Q(int(numerator), int(denominator))
            elif factor.isdigit():
                coefficient *= int(factor)
            else:
                require(
                    factor
                    and factor[0] in "uv"
                    and factor[1:].isdigit(),
                    ("invalid certificate variable", factor),
                )
                variables.append(factor)
        answer = polynomial_add(
            answer, polynomial_term(coefficient, *variables)
        )
    return answer


# The kth multiplier below multiplies the kth scalar equation in the order
# SLICES x LOCAL_EDGES x (i,j), with every tuple lexicographic.  This is an
# exact lift of 1 from the ideal; omitted equation indices have multiplier 0.
CERTIFICATE_TEXT = {
    1: "-1",
    2: "8/11",
    3: "1/2",
    4: "-4/11",
    29: "-9/16*u051*v010+9/22*u051*v011",
    30: "-2/3*u050*v010-u051*v010+16/33*u050*v011+8/11*u051*v011",
    31: "7/16*u051*v010-7/22*u051*v011",
    32: "1/2*u050*v010+1/2*u051*v010-4/11*u050*v011-4/11*u051*v011",
    33: "-2/3*u041*v010+16/33*u041*v011",
    34: "-9/16*u040*v010-u041*v010+9/22*u040*v011+8/11*u041*v011",
    35: "1/2*u041*v010-4/11*u041*v011",
    36: "7/16*u040*v010+1/2*u041*v010-7/22*u040*v011-4/11*u041*v011",
    38: "-3/35*u050*v000-u051*v000+3/70*u050*v001+1/2*u051*v001",
    40: "24/385*u050*v000+8/11*u051*v000-12/385*u050*v001-4/11*u051*v001",
    41: "-3/35*u041*v000+3/70*u041*v001",
    42: "-u041*v000+1/2*u041*v001",
    43: "24/385*u041*v000-12/385*u041*v001",
    44: "8/11*u041*v000-4/11*u041*v001",
    46: "-9/16*u000*v010+7/16*u001*v010+9/22*u000*v011-7/22*u001*v011",
    47: "-3/35*u010*v000+24/385*u011*v000+3/70*u010*v001-12/385*u011*v001-2/3*u000*v010+1/2*u001*v010+16/33*u000*v011-4/11*u001*v011",
    48: "-u010*v000+8/11*u011*v000+1/2*u010*v001-4/11*u011*v001-u000*v010+1/2*u001*v010+8/11*u000*v011-4/11*u001*v011",
    53: "9/16*u151*v010-9/22*u151*v011",
    54: "2/3*u150*v010+u151*v010-16/33*u150*v011-8/11*u151*v011",
    55: "-7/16*u151*v010+7/22*u151*v011",
    56: "-1/2*u150*v010-1/2*u151*v010+4/11*u150*v011+4/11*u151*v011",
    57: "2/3*u141*v010-16/33*u141*v011",
    58: "9/16*u140*v010+u141*v010-9/22*u140*v011-8/11*u141*v011",
    59: "-1/2*u141*v010+4/11*u141*v011",
    60: "-7/16*u140*v010-1/2*u141*v010+7/22*u140*v011+4/11*u141*v011",
    62: "3/35*u150*v000+u151*v000-3/70*u150*v001-1/2*u151*v001",
    64: "-24/385*u150*v000-8/11*u151*v000+12/385*u150*v001+4/11*u151*v001",
    65: "3/35*u141*v000-3/70*u141*v001",
    66: "u141*v000-1/2*u141*v001",
    67: "-24/385*u141*v000+12/385*u141*v001",
    68: "-8/11*u141*v000+4/11*u141*v001",
    70: "9/16*u100*v010-7/16*u101*v010-9/22*u100*v011+7/22*u101*v011",
    71: "3/35*u110*v000-24/385*u111*v000-3/70*u110*v001+12/385*u111*v001+2/3*u100*v010-1/2*u101*v010-16/33*u100*v011+4/11*u101*v011",
    72: "u110*v000-8/11*u111*v000-1/2*u110*v001+4/11*u111*v001+u100*v010-1/2*u101*v010-8/11*u100*v011+4/11*u101*v011",
}


LOCAL_SITES = (0, 1, 4, 5)
LOCAL_EDGES = tuple(combinations(LOCAL_SITES, 2))
SLICES = ((0, 0), (1, 1), (0, 1))


def quotient_equation(label):
    s, t, r, u, i, j = label
    answer = polynomial_add(
        polynomial_term(1, f"u{s}{r}{i}", f"v{t}{u}{j}"),
        polynomial_term(1, f"v{t}{r}{i}", f"u{s}{u}{j}"),
    )
    target = (
        (s, t) == (0, 0) and (r, u, i, j) == (0, 1, 0, 0)
    ) or (
        (s, t) == (1, 1) and (r, u, i, j) == (4, 5, 1, 1)
    )
    if target:
        answer = polynomial_add(answer, polynomial_term(-1))
    entry = BLOCKS[r, u][i][j]
    if entry:
        answer = polynomial_add(
            answer,
            polynomial_term(-entry, f"l{s}{t}{r}"),
            polynomial_term(-entry, f"l{s}{t}{u}"),
        )
    return answer


EQUATION_LABELS = tuple(
    (s, t, r, u, i, j)
    for s, t in SLICES
    for r, u in LOCAL_EDGES
    for i, j in product(COLOURS, repeat=2)
)


EXPECTED_SELECTED_LABELS = (
    (0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 1),
    (0, 0, 0, 1, 1, 0), (0, 0, 0, 1, 1, 1),
    (1, 1, 0, 4, 0, 0), (1, 1, 0, 4, 0, 1),
    (1, 1, 0, 4, 1, 0), (1, 1, 0, 4, 1, 1),
    (1, 1, 0, 5, 0, 0), (1, 1, 0, 5, 0, 1),
    (1, 1, 0, 5, 1, 0), (1, 1, 0, 5, 1, 1),
    (1, 1, 1, 4, 0, 1), (1, 1, 1, 4, 1, 1),
    (1, 1, 1, 5, 0, 0), (1, 1, 1, 5, 0, 1),
    (1, 1, 1, 5, 1, 0), (1, 1, 1, 5, 1, 1),
    (1, 1, 4, 5, 0, 1), (1, 1, 4, 5, 1, 0),
    (1, 1, 4, 5, 1, 1),
    (0, 1, 0, 4, 0, 0), (0, 1, 0, 4, 0, 1),
    (0, 1, 0, 4, 1, 0), (0, 1, 0, 4, 1, 1),
    (0, 1, 0, 5, 0, 0), (0, 1, 0, 5, 0, 1),
    (0, 1, 0, 5, 1, 0), (0, 1, 0, 5, 1, 1),
    (0, 1, 1, 4, 0, 1), (0, 1, 1, 4, 1, 1),
    (0, 1, 1, 5, 0, 0), (0, 1, 1, 5, 0, 1),
    (0, 1, 1, 5, 1, 0), (0, 1, 1, 5, 1, 1),
    (0, 1, 4, 5, 0, 1), (0, 1, 4, 5, 1, 0),
    (0, 1, 4, 5, 1, 1),
)


def audit_nullstellensatz_certificate():
    require(len(EQUATION_LABELS) == 72,
            "the three-slice local equation count changed")
    selected_labels = tuple(
        EQUATION_LABELS[index - 1] for index in CERTIFICATE_TEXT
    )
    require(selected_labels == EXPECTED_SELECTED_LABELS,
            ("certificate equation orientations changed", selected_labels))
    require(
        set((r, u) for _, _, r, u, _, _ in selected_labels)
        <= set(LOCAL_EDGES),
        "the certificate left the local K4",
    )
    require(set((s, t) for s, t, _, _, _, _ in selected_labels)
            == set(SLICES),
            "the certificate slice set changed")

    multipliers = {
        index: parse_multiplier(text)
        for index, text in CERTIFICATE_TEXT.items()
    }
    term_count = sum(len(polynomial) for polynomial in multipliers.values())
    maximum_degree = max(
        len(monomial)
        for polynomial in multipliers.values()
        for monomial in polynomial
    )
    maximum_terms = max(len(polynomial) for polynomial in multipliers.values())
    require(
        (len(multipliers), term_count, maximum_degree, maximum_terms)
        == (38, 124, 2, 8),
        "the sparse certificate statistics changed",
    )

    identity = {}
    for index, multiplier in multipliers.items():
        equation = quotient_equation(EQUATION_LABELS[index - 1])
        identity = polynomial_add(
            identity, polynomial_multiply(multiplier, equation)
        )
    require(identity == ONE,
            ("the exact Nullstellensatz identity failed", identity))
    return len(multipliers), term_count, maximum_degree, maximum_terms


def main():
    audit_rank_kernel_and_targets()
    count, terms, degree, largest = audit_nullstellensatz_certificate()
    print("sharp L0 factor obstruction independent audit: PASS")
    print("  differential ranks       : D=55, D_mixed=53")
    print("  kernel                    : five gauges, hence exact")
    print("  slices used               : 00, 11, 01 (10 unused)")
    print("  local residual graph      : K4 on {0,1,4,5}")
    print("  certificate equations     : %d/72" % count)
    print("  coefficient terms/degree  : %d / %d" % (terms, degree))
    print("  largest multiplier        : %d terms" % largest)
    print("  exact identity            : sum(c_k f_k) = 1")
    print("  conclusion                : no binary endpoint completion")


if __name__ == "__main__":
    main()

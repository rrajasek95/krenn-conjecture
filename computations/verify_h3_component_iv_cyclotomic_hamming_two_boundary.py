#!/usr/bin/env python3
"""First literal Hamming-two row on the cyclotomic Component-IV slice.

At the word 112112 (distance two from the pure-1 anchor), the normalized
cyclotomic q_m slice plus the only x-bearing cells visible in that word gives

    direct = sum_v r_v h_v = 0,
    response = P_m^T K_zeta(r) S_m.

The response is a genuine nonzero coupling, but it has an exact two-plane
kernel even with a localized cross-word carrier.  Thus the completed static
anchor/crossed packet plus this first Hamming-two row has no unit and does
not perform the needed endpoint-word change.  The first new complete-word
grade is the Hamming-three word 012112.

This is an associated-graded/source-module counterguard, not a full source.
"""

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_DIGEST = "a62954f772ad2ae2007131c41923b7aa6bd3bd145f64a986cb37d6a4bfa0d636"
PINS = {
    "computations/verify_h3_component_iv_square_zero_slice_routing_boundary.py":
        "6d41acd033a1c5eced5968a8deb780331f2ee93e21f8b85efcba840bf3664e08",
    "computations/verify_h3_two_chart_h2_tagged_reinsertion_cokernel.py":
        "5c508a1ec64cf290c4a110e8411eb5f60add06621fe08a7632d0bbcd2cb3644d",
    "computations/verify_h3_literal_full_nine_schur_polar_no_go.py":
        "a9347a06f516fe05a4d22872de5ac8071ca2824105159e59579ee1e8aad741cc",
    "computations/verify_h3_rootless_component_iii_complete_typed_inventory.py":
        "3e2b5912f58646169547b418bb4975a27635dcd8d548a010eb4c2e265412f465",
}

SITES = tuple(range(1, 6))
MIXED = (1, 2, 1, 1, 2)
CYCLE = frozenset(tuple(sorted(edge)) for edge in
                  ((1, 2), (2, 3), (3, 4), (4, 5), (5, 1)))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


class K:
    """Q[zeta]/(zeta^2+zeta+1), represented as a+b*zeta."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        if isinstance(a, K):
            self.a, self.b = a.a, a.b
        else:
            self.a, self.b = Q(a), Q(b)

    def __add__(self, other):
        other = K(other)
        return K(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-K(other))

    def __rsub__(self, other):
        return K(other) - self

    def __mul__(self, other):
        other = K(other)
        # zeta^2=-zeta-1
        return K(self.a * other.a - self.b * other.b,
                 self.a * other.b + self.b * other.a - self.b * other.b)

    __rmul__ = __mul__

    def __truediv__(self, rational):
        return K(self.a / Q(rational), self.b / Q(rational))

    def __eq__(self, other):
        other = K(other)
        return self.a == other.a and self.b == other.b

    def __bool__(self):
        return bool(self.a or self.b)

    def text(self):
        def q(value):
            return (str(value.numerator) if value.denominator == 1
                    else f"{value.numerator}/{value.denominator}")
        return [q(self.a), q(self.b)]


ZERO = K(0)
ONE = K(1)
ZETA = K(0, 1)


def q_edge(left, right):
    return ONE if tuple(sorted((left, right))) in CYCLE else ZETA


def haf4(vertices):
    a, b, c, d = vertices
    return (q_edge(a, b) * q_edge(c, d)
            + q_edge(a, c) * q_edge(b, d)
            + q_edge(a, d) * q_edge(b, c))


def face_values():
    return tuple(haf4(tuple(site for site in SITES if site != deleted))
                 for deleted in SITES)


def cofactor_matrix(r):
    r"""K_uv=[word on {x}+D\{u,v}] q^[2], u,v in D."""
    matrix = [[ZERO for _ in SITES] for _ in SITES]
    for u_index, u in enumerate(SITES):
        for v_index, v in enumerate(SITES):
            if u >= v:
                continue
            remaining = tuple(site for site in SITES if site not in (u, v))
            value = ZERO
            for x_partner in remaining:
                internal = tuple(site for site in remaining if site != x_partner)
                value += r[x_partner - 1] * q_edge(*internal)
            matrix[u_index][v_index] = value
            matrix[v_index][u_index] = value
    return matrix


def mat_vec(matrix, vector):
    return [sum((entry * value for entry, value in zip(row, vector, strict=True)),
                ZERO)
            for row in matrix]


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), ZERO)


def response_matrix(first, cofactor, second):
    """first^T cofactor second; site rows, endpoint-label columns."""
    labels = len(first[0])
    output = [[ZERO for _ in range(labels)] for _ in range(labels)]
    for i in range(labels):
        for j in range(labels):
            left = [first[site][i] for site in range(len(SITES))]
            right = [second[site][j] for site in range(len(SITES))]
            output[i][j] = dot(left, mat_vec(cofactor, right))
    return output


def rank_over_k(matrix):
    work = [[K(value) for value in row] for row in matrix]
    answer = 0
    width = len(work[0]) if work else 0

    def inverse(value):
        # (a+bz)^-1 = ((a-b)-b z)/(a^2-a*b+b^2).
        norm = value.a * value.a - value.a * value.b + value.b * value.b
        require(norm, "attempted to invert zero")
        return K((value.a - value.b) / norm, -value.b / norm)

    for column in range(width):
        pivot = next((row for row in range(answer, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[answer], work[pivot] = work[pivot], work[answer]
        scale = inverse(work[answer][column])
        work[answer] = [scale * value for value in work[answer]]
        for row in range(len(work)):
            if row == answer or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [left - scale * right for left, right in
                         zip(work[row], work[answer], strict=True)]
        answer += 1
    return answer


def determinant_q(matrix):
    # This matrix is rational in the static audit.
    work = [[Q(value) for value in row] for row in matrix]
    answer = Q(1)
    for column in range(len(work)):
        pivot = next((row for row in range(column, len(work))
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, len(work)):
            if not work[row][column]:
                continue
            scale = work[row][column] / value
            for index in range(column, len(work)):
                work[row][index] -= scale * work[column][index]
    return answer


def hamming_distance_from_pure(word, colour):
    return sum(value != colour for value in word)


def main():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}: {actual}")

    require(ZETA * ZETA + ZETA + ONE == ZERO, "cyclotomic relation failed")
    require(ZETA * ZETA * ZETA == ONE, "zeta ceased to be a cube root")
    h = face_values()
    require(h == (ZERO,) * 5, "a cyclotomic face hafnian became nonzero")

    # The first word visible from the pure-1 anchor is Hamming two.  Its only
    # new q cells are r_v=q_(xv)^(1,m_v).  The q^[3] direct coefficient is
    # sum r_v h_v and hence zero for every r.
    word_h2 = (1,) + MIXED
    word_h3 = (0,) + MIXED
    require(hamming_distance_from_pure(word_h2, 1) == 2,
            "selected word stopped being Hamming two")
    require(hamming_distance_from_pure(word_h3, 1) == 3,
            "endpoint-changed word stopped being Hamming three")

    r = (ONE, ZERO, ZERO, ZERO, ZERO)  # localized carrier q_(x1)^(1,1)
    direct = sum((value * face for value, face in zip(r, h, strict=True)), ZERO)
    require(direct == ZERO, "Hamming-two direct term stopped vanishing")
    cofactor = cofactor_matrix(r)
    require(cofactor[1][2] == ONE, "literal H2 coupling K_23 lost its unit term")
    require(rank_over_k(cofactor) == 3, "cyclotomic H2 cofactor rank changed")

    # Exact two-plane kernel.  It is nontrivial on both conjugate zeta
    # orbits because all identities are over Q[zeta]/(zeta^2+zeta+1).
    e1 = [ONE, ZERO, ZERO, ZERO, ZERO]
    k = [ZERO, ONE, ZETA, ZETA, ONE]
    require(mat_vec(cofactor, e1) == [ZERO] * 5,
            "carrier-site kernel vector changed")
    require(mat_vec(cofactor, k) == [ZERO] * 5,
            "cyclotomic kernel vector changed")
    require(rank_over_k([e1, k]) == 2, "H2 kernel plane collapsed")

    # Put two labelled endpoint-star columns on this kernel plane.  Their
    # selected-word restrictions have rank two, yet every one of the four
    # labelled response coefficients vanishes.  A third label may be
    # completed in another word grade without changing this calculation.
    first = [[e1[site], k[site]] for site in range(5)]
    second = [[k[site], e1[site]] for site in range(5)]
    require(rank_over_k(first) == 2 and rank_over_k(second) == 2,
            "selected star restrictions lost rank two")
    response = response_matrix(first, cofactor, second)
    require(response == [[ZERO, ZERO], [ZERO, ZERO]],
            "kernel-plane Hamming-two response became nonzero")

    # The row is nevertheless a genuine coupling, not the zero polynomial:
    # P=e_2 and S=e_3 read the literal unit K_23.
    probe_p = [[ZERO] for _ in SITES]
    probe_s = [[ZERO] for _ in SITES]
    probe_p[1][0] = ONE
    probe_s[2][0] = ONE
    probe = response_matrix(probe_p, cofactor, probe_s)
    require(probe == [[ONE]], "generic H2 coupling became identically blind")

    # The completed two-anchor/direct/crossed static packet is full, but its
    # complete-word grades are separate from 112112.  It cannot remove the
    # kernel plane by a constant source-grade combination.
    static = [
        [1, 0, 1, 0],
        [0, 0, 1, 1],
        [0, 0, 1, -2],
        [0, 1, 2, 0],
    ]
    require(determinant_q(static) == -3, "static determinant changed")

    # The needed endpoint recolouring is a different complete-word grade.
    # Its x-bearing cells rho_v=q_(xv)^(0,m_v) are disjoint source variables
    # from r_v=q_(xv)^(1,m_v); H2 at 112112 cannot constrain them.
    r_labels = tuple(f"q_x{site}^(1,{MIXED[site-1]})" for site in SITES)
    rho_labels = tuple(f"q_x{site}^(0,{MIXED[site-1]})" for site in SITES)
    require(set(r_labels).isdisjoint(rho_labels),
            "H2 and endpoint-changed carriers collided")

    ledger = {
        "scope": "cyclotomic q_m plus first literal H2 cross-word cells and static packet",
        "coefficient_field": "Q[zeta]/(zeta^2+zeta+1)",
        "tests_both_geometric_zeta_orbits": True,
        "H2_word": "112112",
        "H2_distance_from_pure_1": 2,
        "direct_term": "sum_v r_v*h_v=0",
        "response_term": "P_m^T*K_zeta(r)*S_m",
        "localized_probe": "r_1=q_x1^(1,1)=1",
        "K_rank": rank_over_k(cofactor),
        "K_nonzero_probe": "K_23=1",
        "K_kernel_basis": [
            [value.text() for value in e1],
            [value.text() for value in k],
        ],
        "rank_two_star_guard_response": [[value.text() for value in row]
                                           for row in response],
        "static_det": "-3",
        "source_unit_in_bounded_module": False,
        "forced_endpoint_word_change": False,
        "first_new_word": "012112",
        "first_new_word_distance_from_pure_1": 3,
        "H2_carriers": r_labels,
        "endpoint_changed_carriers": rho_labels,
        "exact_missing_row": (
            "a source-provenant relation coupling the H2 kernel plane at 112112 "
            "to the endpoint-changed full-nine word 012112 (01211200 before "
            "deleting the two chart endpoints)"
        ),
        "not_a_full_source": True,
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":")).encode()
    digest = sha256(encoded).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST, f"ledger digest changed: {digest}")

    print("h=3 cyclotomic Component-IV Hamming-two boundary: PASS")
    print("H2 coupling: nonzero; K_zeta(r1) rank 3 with kernel dimension 2")
    print("rank-two star guard: all H2 rows zero; static determinant -3")
    print("first missing complete-word grade: 012112 (Hamming three)")
    print(f"ledger sha256: {digest}")


if __name__ == "__main__":
    main()

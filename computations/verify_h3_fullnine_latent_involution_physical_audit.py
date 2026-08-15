#!/usr/bin/env python3
"""Audit the physical full-nine => latent-involution implication at h=3.

The theorem proved in the companion note is intrinsic to the literal
site-square-zero EqSystem.  For endpoints p,q and residual six-site port
space V, put

    p_i = sum A_px(i,c) x_(x,c),  s_j = sum A_qx(j,c) x_(x,c),
    C(u,v) = u v q^[2].

Every full-nine equation is exactly

    C(p_i,s_j) = delta_ij X_i - a_ij q^[3],

so C(P,S) is contained in W=span(q^[3],X_0,X_1,X_2).  If the six stars
are independent and the scalar-zero channel matrix K is invertible, use the
ordered basis (p_0,p_1,p_2,s_0,s_1,s_2) and

    J = [[0,K],[K^T,0]],  T = diag(I_3,-I_3).

For every lambda killing W, C_lambda has zero P-by-S block and
A_lambda=J^{-1}C_lambda anticommutes with T.  The converse is the same block
calculation in characteristic not two.

The machine test uses a literal 77-cell N=8 physical guard.  On endpoints
(2,3) its two endpoint-star triples span six dimensions; all nine selected
cap lines are rootless.  The guard misses only the global pure 0^8 and 1^8
normalizations, but those residuals themselves lie in W, so the coarse
containment and every quotient anticommutator still hold.  This is a test of
the implication's algebra and conventions, not an exact GHZ example.

No B/Eq, Gamma, AugP2, or operation-labelled coordinates occur here.
"""

from __future__ import annotations

import importlib
import os
import sys
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


PINS = {
    "verify_rootless_latent_polarization_involution.py":
        "d6869f6ef83cda61ccb490232b033a40abe41e234ae234397117ebec86cd43df",
    "../notes/rootless-latent-polarization-involution.md":
        "a746db7d56ea611ce9b1a90142f52df92fe69e048c1a65f1b55f746de35a9465",
    "verify_n8_d2_kill_and_monochrome_rigidity.py":
        "6320c3bdb795df3050952e52bd9c0fb9f4d5f2cdbf9eb543cd3467179630a745",
    "verify_cap_line_cubic_activity_dichotomy.py":
        "39a0b8ee22e4eec56b1174d200e29679a3baeae1a814ec422f69b6a9725f1300",
}
EXPECTED_LEDGER_SHA256 = (
    "495af6a66a413d9bb39dfdb6d8dda0a3b8775e2677843b437c422d5fdb0afc5d"
)


def pin_sources():
    result = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            result[relative] = sha256(handle.read()).hexdigest()
        require(result[relative] == expected,
                "pinned source changed: %s (%s)" %
                (relative, result[relative]))
    return result


PINNED = pin_sources()
D = importlib.import_module("verify_n8_d2_kill_and_monochrome_rigidity")
L = importlib.import_module("verify_cap_line_cubic_activity_dichotomy")

COLORS = (0, 1, 2)
ALL_SITES = tuple(range(8))
ENDPOINTS = (2, 3)
RESIDUAL = tuple(site for site in ALL_SITES if site not in ENDPOINTS)
WORDS = tuple(product(COLORS, repeat=6))


def zero_matrix(rows, columns):
    return [[Q(0) for _ in range(columns)] for _ in range(rows)]


def identity(size):
    answer = zero_matrix(size, size)
    for index in range(size):
        answer[index][index] = Q(1)
    return answer


def transpose(matrix):
    return [list(row) for row in zip(*matrix, strict=True)]


def matmul(left, right):
    require(len(left[0]) == len(right),
            "matrix product has incompatible shapes")
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), Q(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def matrix_add(left, right):
    return [[a + b for a, b in zip(lrow, rrow, strict=True)]
            for lrow, rrow in zip(left, right, strict=True)]


def matrix_equal_zero(matrix):
    return all(not entry for row in matrix for entry in row)


def inverse(matrix):
    size = len(matrix)
    require(size and all(len(row) == size for row in matrix),
            "inverse expects a nonempty square matrix")
    work = [list(map(Q, row)) + identity(size)[index]
            for index, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        require(pivot is not None, "matrix is singular")
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [entry / scale for entry in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [entry - factor * pivot_entry
                         for entry, pivot_entry in
                         zip(work[row], work[column], strict=True)]
    return [row[size:] for row in work]


def determinant(matrix):
    work = [list(map(Q, row)) for row in matrix]
    size = len(work)
    answer = Q(1)
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        value = work[column][column]
        answer *= value
        for row in range(column + 1, size):
            factor = work[row][column] / value
            for other in range(column + 1, size):
                work[row][other] -= factor * work[column][other]
    return answer


def block_cross(pairing):
    zero = zero_matrix(3, 3)
    return ([zero[row] + list(pairing[row]) for row in range(3)]
            + [list(transpose(pairing)[row]) + zero[row] for row in range(3)])


def audit_block_equivalence(j_inverse, involution):
    """Test the cross-block/anticommutator equivalence on a basis of Sym^2."""
    checked = 0
    for left in range(6):
        for right in range(left, 6):
            form = zero_matrix(6, 6)
            form[left][right] = Q(1)
            form[right][left] = Q(1)
            cross_zero = all(not form[i][3 + j]
                             for i, j in product(COLORS, repeat=2))
            operator = matmul(j_inverse, form)
            anticommutes = matrix_equal_zero(matrix_add(
                matmul(operator, involution), matmul(involution, operator)))
            require(cross_zero == anticommutes,
                    "cross-block/anticommutator equivalence failed on (%d,%d)"
                    % (left, right))
            checked += 1
    require(checked == 21, "Sym^2 basis census changed")
    return checked


def as_chart_packet(blocks):
    local = {site: index for index, site in enumerate(RESIDUAL)}
    q, p, s, direct = {}, {}, {}, {}
    for x, y in combinations(RESIDUAL, 2):
        block = D.C.oriented(blocks, x, y)
        for a, b in product(COLORS, repeat=2):
            if block[a][b]:
                q[(local[x], local[y], a, b)] = block[a][b]
    for endpoint, output in zip(ENDPOINTS, (p, s), strict=True):
        for x in RESIDUAL:
            block = D.C.oriented(blocks, endpoint, x)
            for i, colour in product(COLORS, repeat=2):
                if block[i][colour]:
                    output[(i, local[x], colour)] = block[i][colour]
    direct_block = D.C.oriented(blocks, *ENDPOINTS)
    for i, j in product(COLORS, repeat=2):
        if direct_block[i][j]:
            direct[(i, j)] = direct_block[i][j]
    return L.Packet(q, p, s, direct)


def star_vector(packet, shore, label):
    getter = packet.pe if shore == "P" else packet.se
    return tuple(getter(label, site, colour)
                 for site in range(6) for colour in COLORS)


def q_cube(packet):
    return tuple(packet.haf(
        lambda x, y: packet.qe(x, y, word[x], word[y])) for word in WORDS)


def pair_q2(packet, left, right):
    """Literal coefficients of left*right*q^[2], including diagonal 2."""
    answer = []
    for word in WORDS:
        total = Q(0)
        for x, y in L.PAIRS:
            response = (left[3 * x + word[x]] * right[3 * y + word[y]]
                        + left[3 * y + word[y]] * right[3 * x + word[x]])
            if not response:
                continue
            rest = tuple(site for site in range(6) if site not in (x, y))
            total += response * packet.haf(
                lambda u, v: packet.qe(u, v, word[u], word[v]), rest)
        answer.append(total)
    return tuple(answer)


def target_vector(colour):
    return tuple(Q(1) if word == (colour,) * 6 else Q(0) for word in WORDS)


def vector_add(*terms):
    return tuple(sum(entries, Q(0)) for entries in zip(*terms, strict=True))


def vector_scale(scalar, vector):
    return tuple(scalar * entry for entry in vector)


def independent_vectors(vectors):
    selected = []
    for vector in vectors:
        if D.C.rank(selected + [vector]) > len(selected):
            selected.append(vector)
    return tuple(selected)


def quotient_functionals(w_basis):
    """Return lambda rows spanning W^perp, represented on 729 coordinates."""
    target_dimension = len(w_basis)
    pivot_rows = []
    for coordinate in range(len(WORDS)):
        row = tuple(vector[coordinate] for vector in w_basis)
        if D.C.rank([tuple(w[entry] for w in w_basis)
                     for entry in pivot_rows] + [row]) > len(pivot_rows):
            pivot_rows.append(coordinate)
        if len(pivot_rows) == target_dimension:
            break
    require(len(pivot_rows) == target_dimension,
            "failed to find pivot coordinates for W")
    pivot_matrix = [[vector[row] for vector in w_basis] for row in pivot_rows]
    pivot_inverse = inverse(pivot_matrix)
    pivot_set = set(pivot_rows)
    functionals = []
    for coordinate in range(len(WORDS)):
        if coordinate in pivot_set:
            continue
        # lambda(v)=v_coordinate-B_coordinate B_pivot^{-1} v_pivot.
        coefficients = matmul(
            [[vector[coordinate] for vector in w_basis]], pivot_inverse)[0]
        functional = [Q(0)] * len(WORDS)
        functional[coordinate] = Q(1)
        for coefficient, pivot in zip(coefficients, pivot_rows, strict=True):
            functional[pivot] -= coefficient
        require(all(sum((functional[k] * vector[k]
                         for k in range(len(WORDS))), Q(0)) == 0
                    for vector in w_basis),
                "constructed quotient functional does not kill W")
        functionals.append(tuple(functional))
    return tuple(pivot_rows), tuple(functionals)


def pairing(functional, vector):
    return sum((a * b for a, b in zip(functional, vector, strict=True)), Q(0))


def audit_physical_packet():
    blocks = D.build_stage_a(D.STAGE_A_BASE)
    defects = D.C.exactness_defects(blocks, ALL_SITES)
    require(defects == {(0,) * 8: (Q(0), Q(1)),
                        (1,) * 8: (Q(0), Q(1))}, defects)
    packet = as_chart_packet(blocks)

    p_vectors = tuple(star_vector(packet, "P", i) for i in COLORS)
    s_vectors = tuple(star_vector(packet, "S", j) for j in COLORS)
    latent_vectors = p_vectors + s_vectors
    star_ranks = (D.C.rank(p_vectors), D.C.rank(s_vectors),
                  D.C.rank(latent_vectors))
    require(star_ranks == (3, 3, 6),
            "the physical endpoint stars do not give a 3+3 split: %s"
            % (star_ranks,))

    q3 = q_cube(packet)
    targets = tuple(target_vector(colour) for colour in COLORS)
    w_basis = independent_vectors((q3,) + targets)
    require(len(w_basis) == 4, "W does not have the expected dimension four")

    c_vectors = [[None for _ in range(6)] for _ in range(6)]
    for left in range(6):
        for right in range(left, 6):
            value = pair_q2(packet, latent_vectors[left], latent_vectors[right])
            c_vectors[left][right] = value
            c_vectors[right][left] = value

    # This is the literal implication row by row.  The guard has diagonal
    # normalization multipliers (0,0,1), but all residuals still lie in W.
    diagonal_multipliers = []
    for i, j in product(COLORS, repeat=2):
        lhs = vector_add(c_vectors[i][3 + j],
                         vector_scale(packet.de(i, j), q3))
        if i == j:
            coefficient = lhs[WORDS.index((i,) * 6)]
            require(lhs == vector_scale(coefficient, targets[i]),
                    "a diagonal full-nine residual escaped its pure target")
            diagonal_multipliers.append(coefficient)
        else:
            require(not any(lhs),
                    "an off-diagonal full-nine row is nonzero")
    require(tuple(diagonal_multipliers) == (Q(0), Q(0), Q(1)),
            "the guard's two missing pure normalizations changed")

    pivot_rows, functionals = quotient_functionals(w_basis)
    quotient_forms = []
    cross_nonzero = 0
    for functional in functionals:
        form = [[pairing(functional, c_vectors[left][right])
                 for right in range(6)] for left in range(6)]
        require(form == transpose(form), "C_lambda is not symmetric")
        cross_nonzero += sum(form[i][3 + j] != 0
                             for i, j in product(COLORS, repeat=2))
        if any(entry for row in form for entry in row):
            quotient_forms.append(form)
    require(cross_nonzero == 0,
            "C(P,S) has a nonzero image in the quotient T/W")
    form_span_rank = D.C.rank([
        tuple(entry for row in form for entry in row)
        for form in quotient_forms])
    require(form_span_rank > 0,
            "the physical test is vacuous: C has no quotient polarization")

    direct = [[packet.de(i, j) for j in COLORS] for i in COLORS]
    alpha = direct[0][1]
    tau = sum((direct[i][i] for i in COLORS), Q(0))
    require((alpha, tau) == (Q(-34), Q(85)),
            "the selected scalar pencil changed")
    pairing_k = [[Q(34) if i == j else Q(0) for j in COLORS]
                 for i in COLORS]
    pairing_k[0][1] += Q(85)  # K_*=tau E_01-alpha I.
    require(sum((pairing_k[i][j] * direct[i][j]
                 for i, j in product(COLORS, repeat=2)), Q(0)) == 0,
            "K_* is not scalar-zero under the no-transpose contraction")
    require(determinant(pairing_k) == Q(34) ** 3,
            "the scalar-zero channel matrix is not invertible")

    j_form = block_cross(pairing_k)
    j_inverse = inverse(j_form)
    involution = [[Q(1) if row == column and row < 3 else
                   Q(-1) if row == column else Q(0)
                   for column in range(6)] for row in range(6)]
    require(matmul(involution, involution) == identity(6), "T^2 != I")
    require(sum(involution[i][i] for i in range(6)) == 0, "tr T != 0")
    require(matrix_equal_zero(matrix_add(
        matmul(transpose(involution), j_form), matmul(j_form, involution))),
        "T is not J-skew")
    symmetric_basis_checks = audit_block_equivalence(j_inverse, involution)
    anticommutator_failures = 0
    for form in quotient_forms:
        operator = matmul(j_inverse, form)
        if not matrix_equal_zero(matrix_add(matmul(operator, involution),
                                            matmul(involution, operator))):
            anticommutator_failures += 1
        # C symmetric means A is J-self-adjoint: A^T J = J A = C.
        require(matmul(transpose(operator), j_form) == form
                and matmul(j_form, operator) == form,
                "A_lambda=J^-1 C_lambda lost the form convention")
    require(anticommutator_failures == 0,
            "a literal quotient polarization failed to anticommute")

    line = L.line_verdict(packet, 0, 1)
    require(line["gcd"] == (Q(1),) and line["rank"] == 4,
            "the nontrivial physical test line is no longer rootless")
    require(line["act"] == (Q(0), Q(0), Q(0), Q(-34), Q(85)),
            "the selected activity is not z^3(-34+85z)")

    return {
        "physical_scope": "literal 77-cell site-square-zero N=8 guard",
        "eqsystem_rows_satisfied": 3 ** 8 - len(defects),
        "missing_rows": tuple(sorted(defects)),
        "endpoints": ENDPOINTS,
        "residual_sites": RESIDUAL,
        "star_ranks_P_S_total": star_ranks,
        "dim_W": len(w_basis),
        "W_pivot_words": tuple(WORDS[index] for index in pivot_rows),
        "dim_W_perp": len(functionals),
        "nonzero_quotient_forms": len(quotient_forms),
        "quotient_form_span_rank": form_span_rank,
        "cross_quotient_nonzero_entries": cross_nonzero,
        "diagonal_target_multipliers": tuple(diagonal_multipliers),
        "direct_block": tuple(tuple(row) for row in direct),
        "selected_line": {
            "colours": (0, 1), "alpha": alpha, "tau": tau,
            "activity": line["act"], "clean_coordinate_rank": line["rank"],
            "gcd": line["gcd"],
        },
        "scalar_zero_K": tuple(tuple(row) for row in pairing_k),
        "det_K": determinant(pairing_k),
        "rank_J": D.C.rank(j_form),
        "involution_trace": sum(involution[i][i] for i in range(6)),
        "symmetric_basis_equivalence_checks": symmetric_basis_checks,
        "anticommutator_failures": anticommutator_failures,
    }


def build_ledger():
    physical = audit_physical_packet()
    return {
        "theorem": (
            "literal full-nine rows imply C(P,S) subset "
            "span(q^[3],X0,X1,X2); under rank(P+S)=6 and det(K)!=0 this "
            "is equivalent in characteristic not two to the displayed "
            "J-skew involution anticommutators"
        ),
        "definitions": {
            "latent_basis": "(p_0,p_1,p_2,s_0,s_1,s_2)",
            "C": "C(u,v)=u*v*q^[2] in the literal six-site top word space",
            "J": "[[0,K],[K^T,0]]; r_K=1/2*l^T J l",
            "T": "diag(I_3,-I_3)",
            "A_lambda": "J^-1 C_lambda, with J A_lambda=C_lambda",
            "contraction": "s(K)=sum_ij K_ij a_ij (no hidden transpose)",
        },
        "extra_hypotheses": (
            "characteristic not two",
            "the scalar-zero channel matrix K is invertible",
        ),
        "physical_span_hypothesis": (
            "rank of the combined six literal endpoint stars is six is needed "
            "only to identify abstract channel L with its physical port span"
        ),
        "not_needed_for_containment": (
            "rootlessness", "scalar-zero", "activity", "invertibility of K",
        ),
        "pins": PINNED,
        "physical_test": physical,
        "scope": (
            "The involution is equivalent only to the quotient containment. "
            "It does not recover the exact diagonal coefficients, a common "
            "direct matrix, or any word/fine/operation presentation."
        ),
    }


def main():
    ledger = build_ledger()
    digest = D.content_hash(ledger)
    require(digest == EXPECTED_LEDGER_SHA256,
            "ledger digest changed: got %s" % digest)
    test = ledger["physical_test"]
    print("PASS: literal full-nine implication and latent conventions audited")
    print("physical guard star ranks P,S,total:", test["star_ranks_P_S_total"])
    print("W/Wperp dimensions: %d/%d; quotient-form span rank: %d" %
          (test["dim_W"], test["dim_W_perp"],
           test["quotient_form_span_rank"]))
    print("rootless test line: activity z^3(-34+85z), det K=%s" %
          test["det_K"])
    print("all literal quotient anticommutators vanish")
    print("sha256:", digest)


if __name__ == "__main__":
    main()

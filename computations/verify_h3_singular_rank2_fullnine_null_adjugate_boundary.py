#!/usr/bin/env python3
"""Exact null/adjugate boundary of the singular h=3 scalar-zero cap.

For the literal full-nine rows

    a_ij Q + p_i s_j F = delta_ij X_i,

let K have rank two, nonzero diagonal, and <K,a>=0.  If xi^T K=0 and
K eta=0, contraction by xi eta^T gives the source-valid one-channel row

    beta Q + p(xi)s(eta)F = sum_i xi_i eta_i X_i,
    beta=<xi eta^T,a>.

The diagonal cofactors of K record exactly which target labels survive.
This checker audits that field-independent reduction, exhausts the normalized
rank-two strata over F_5, and freezes the smallest physical common-q local
guard to the tempting determinant/permanent-triangle shortcut.

The guard is deliberately not a full EqSystem source: it satisfies all nine
rows on the three pure words and one selected mixed word, while its first
remaining defect is the literal row 00:000011.  Thus it is a counterguard to
closing the singular packet from matrix alternation plus Hessian naturality,
not a counterexample to Krenn's conjecture.
"""

from __future__ import annotations

import argparse
import importlib
import json
import os
import sys
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)


PINS = {
    "verify_h3_pure_selected_mixed_rootless_common_q_guard.py":
        "ad6534cb08b29b66217cfefc7aa241964f95ced752ea0b6e81a9775517ccf7a1",
    "../notes/2026-08-15-h3-pure-selected-mixed-rootless-common-q-guard.md":
        "c9a26002177c16e41fe3c4f50c31ace1522ad7b5abb9d1f05ebdd7c27a80a861",
    "verify_h3_common_q_hessian_realization_gate.py":
        "ff927d71b37a0988ce0ac96230950f99f983646a640229b8614d1e81494567c2",
    "../notes/2026-08-15-h3-common-q-hessian-realization-gate.md":
        "58ce518336914446902d73cb669f72ccf7d195201297553cd7defb07f890d78a",
    "verify_h3_unified_dark_annihilator_singular_cap_boundary.py":
        "8cced865640ea93bbe3b72c5a1a9bd34d50eb2eaf2647a5dbbafa165f2cfc34e",
    "../notes/h3-unified-dark-annihilator-singular-cap-boundary.md":
        "1d66839c136fbb71aef349ad96dea4b62257f1e7ea63f7a224abe3af2ed582aa",
}

EXPECTED_LEDGER_SHA256 = (
    "119b29b9dc763731d79c068adfecbca1fa6dd6e9ae5983371e091493d005a7bb"
)

G = importlib.import_module(
    "verify_h3_pure_selected_mixed_rootless_common_q_guard")
H = importlib.import_module("verify_h3_common_q_hessian_realization_gate")
A = G.A
COLORS = tuple(range(3))


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def pin_sources():
    answer = {}
    for relative, expected in sorted(PINS.items()):
        path = os.path.normpath(os.path.join(HERE, relative))
        with open(path, "rb") as handle:
            actual = sha256(handle.read()).hexdigest()
        require(actual == expected,
                "pinned source changed: %s (%s)" % (relative, actual))
        answer[relative] = actual
    return answer


PINNED = pin_sources()


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def determinant(matrix, modulus=None):
    value = (
        matrix[0][0] * (matrix[1][1] * matrix[2][2]
                        - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2]
                          - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1]
                          - matrix[1][1] * matrix[2][0])
    )
    return value if modulus is None else value % modulus


def permanent(matrix, modulus=None):
    value = sum(
        (matrix[0][perm[0]] * matrix[1][perm[1]]
         * matrix[2][perm[2]])
        for perm in permutations(COLORS)
    )
    return value if modulus is None else value % modulus


def rank(matrix, modulus=None):
    work = [list(row) for row in matrix]
    rows, columns = len(work), len(work[0])
    pivot = 0
    for column in range(columns):
        chosen = next((row for row in range(pivot, rows)
                       if ((work[row][column] % modulus) if modulus
                           else work[row][column])), None)
        if chosen is None:
            continue
        work[pivot], work[chosen] = work[chosen], work[pivot]
        lead = work[pivot][column]
        if modulus:
            inverse = pow(lead % modulus, modulus - 2, modulus)
            work[pivot] = [(entry * inverse) % modulus
                           for entry in work[pivot]]
        else:
            lead = Q(lead)
            work[pivot] = [Q(entry) / lead for entry in work[pivot]]
        for row in range(rows):
            if row == pivot:
                continue
            scalar = ((work[row][column] % modulus) if modulus
                      else work[row][column])
            if not scalar:
                continue
            if modulus:
                work[row] = [
                    (entry - scalar * base) % modulus
                    for entry, base in zip(work[row], work[pivot], strict=True)
                ]
            else:
                work[row] = [
                    Q(entry) - Q(scalar) * base
                    for entry, base in zip(work[row], work[pivot], strict=True)
                ]
        pivot += 1
        if pivot == rows:
            break
    return pivot


def adjugate(matrix):
    # adj(A)_ij is the cofactor C_ji.
    answer = []
    for i in COLORS:
        row = []
        for j in COLORS:
            source_rows = [r for r in COLORS if r != j]
            source_columns = [c for c in COLORS if c != i]
            minor = (matrix[source_rows[0]][source_columns[0]]
                     * matrix[source_rows[1]][source_columns[1]]
                     - matrix[source_rows[0]][source_columns[1]]
                     * matrix[source_rows[1]][source_columns[0]])
            row.append((-1 if (i + j) % 2 else 1) * minor)
        answer.append(row)
    return answer


def matrix_product(left, right, modulus=None):
    answer = [[sum(left[i][k] * right[k][j] for k in COLORS)
               for j in COLORS] for i in COLORS]
    if modulus:
        answer = [[entry % modulus for entry in row] for row in answer]
    return answer


def pairing(left, right):
    return sum(left[i][j] * right[i][j]
               for i, j in product(COLORS, repeat=2))


def canonical_null(matrix, modulus):
    for vector in product(range(modulus), repeat=3):
        if vector == (0, 0, 0):
            continue
        first = next(i for i, value in enumerate(vector) if value)
        if vector[first] != 1:
            continue
        if all(sum(matrix[i][j] * vector[j] for j in COLORS) % modulus == 0
               for i in COLORS):
            return vector
    raise RuntimeError("rank-two matrix has no null vector")


def normalized_rank_two_census(prime=5):
    """Exhaust all diag-one rank-two matrices over F_5.

    Left row scaling takes any matrix with nonzero fixed-label diagonal to
    this bookkeeping chart.  It preserves rank, zero/nonzero principal
    cofactors, and determinant/permanent vanishing.  No physical target GL is
    asserted.
    """
    strata = Counter()
    support_strata = Counter()
    examples = {}
    total = 0
    for offdiag in product(range(prime), repeat=6):
        a, b, c, d, e, f = offdiag
        matrix = [[1, a, b], [c, 1, d], [e, f, 1]]
        if determinant(matrix, prime):
            continue
        if rank(matrix, prime) != 2:
            continue
        total += 1
        principal = ((1 - d * f) % prime,
                     (1 - b * e) % prime,
                     (1 - a * c) % prime)
        live = sum(value != 0 for value in principal)
        per_zero = permanent(matrix, prime) == 0
        strata[(live, per_zero)] += 1
        examples.setdefault((live, per_zero), tuple(tuple(row)
                                                     for row in matrix))

        right = canonical_null(matrix, prime)
        left = canonical_null(transpose(matrix), prime)
        left_support = sum(value != 0 for value in left)
        right_support = sum(value != 0 for value in right)
        intersection = sum(left[i] != 0 and right[i] != 0 for i in COLORS)
        require(intersection == live,
                ("adjugate/null-support mismatch", matrix, principal,
                 left, right))
        require(left_support >= 2 and right_support >= 2,
                ("a null vector became coordinate despite nonzero diagonal",
                 matrix, left, right))
        support_strata[(left_support, right_support, intersection)] += 1

        adj = adjugate(matrix)
        require(not any(matrix_product(matrix, adj, prime)[i][j]
                        for i, j in product(COLORS, repeat=2)),
                "K adj(K) is nonzero")
        require(not any(matrix_product(adj, matrix, prime)[i][j]
                        for i, j in product(COLORS, repeat=2)),
                "adj(K) K is nonzero")
        require(tuple(adj[i][i] % prime for i in COLORS) == principal,
                "principal cofactor order changed")

    expected = Counter({
        (1, False): 288, (1, True): 96,
        (2, False): 1644, (2, True): 240,
        (3, False): 912, (3, True): 224,
    })
    expected_support = Counter({
        (2, 2, 1): 384,
        (2, 2, 2): 252,
        (2, 3, 2): 816,
        (3, 2, 2): 816,
        (3, 3, 3): 1136,
    })
    require(strata == expected, ("F_5 cofactor/permanent census changed", strata))
    require(support_strata == expected_support,
            ("F_5 null-support census changed", support_strata))
    require(total == 3404, ("F_5 rank-two total changed", total))
    require(not any(key[0] == 0 for key in strata),
            "a rank-two nonzero-diagonal matrix lost every principal cofactor")
    return {
        "field": "F_5",
        "normalized_rank_two_matrices": total,
        "principal_cofactor_count_x_permanent_zero": {
            "%d,%s" % (live, per_zero): count
            for (live, per_zero), count in sorted(strata.items())
        },
        "null_support_left_right_intersection": {
            "%d,%d,%d" % key: value
            for key, value in sorted(support_strata.items())
        },
        "representatives": {
            "%d,%s" % (live, per_zero): matrix
            for (live, per_zero), matrix in sorted(examples.items())
        },
    }


def contract_vectors(vectors, coefficients):
    return tuple(sum(coefficients[i] * vectors[i][coordinate]
                     for i in COLORS)
                 for coordinate in range(len(vectors[0])))


def physical_cycle_guard():
    packet = G.build_packet()
    p_vectors = tuple(A.star_vector(packet, "P", colour)
                      for colour in COLORS)
    s_vectors = tuple(A.star_vector(packet, "S", colour)
                      for colour in COLORS)
    hessian, cross, common_q = H.audit_common_q(
        packet, p_vectors, s_vectors)

    matrix = [[Q(1), Q(-1), Q(0)],
              [Q(0), Q(1), Q(-1)],
              [Q(-1), Q(0), Q(1)]]
    left = (Q(1), Q(1), Q(1))
    right = (Q(1), Q(1), Q(1))
    direct = [[packet.de(i, j) for j in COLORS] for i in COLORS]
    adj = adjugate(matrix)

    require(rank(matrix) == 2 and determinant(matrix) == 0,
            "the cycle cap is not rank two")
    require(permanent(matrix) == 0,
            "the determinant-zero cycle acquired a permanent")
    require(tuple(matrix[i][i] for i in COLORS) == (Q(1),) * 3,
            "the cycle cap lost a diagonal target")
    require(adj == [[Q(1)] * 3 for _ in COLORS],
            ("the cycle adjugate changed", adj))
    require(all(sum(left[i] * matrix[i][j] for i in COLORS) == 0
                for j in COLORS), "the displayed left null is wrong")
    require(all(sum(matrix[i][j] * right[j] for j in COLORS) == 0
                for i in COLORS), "the displayed right null is wrong")
    require(pairing(matrix, direct) == 0,
            "the cycle cap is not scalar-zero")
    beta = pairing(adj, direct)
    require(beta == -2,
            "the null rank-one cap lost its nonzero direct scalar")

    # The determinant and permanent have only the same two nonzero even
    # permutation monomials, 1 and -1.  No odd-holonomy term appears.
    permutation_terms = tuple(
        (perm, matrix[0][perm[0]] * matrix[1][perm[1]]
         * matrix[2][perm[2]],
         sum(perm[i] > perm[j] for i in COLORS for j in range(i + 1, 3)) % 2)
        for perm in permutations(COLORS)
    )
    nonzero_terms = tuple(item for item in permutation_terms if item[1])
    require(nonzero_terms == (((0, 1, 2), Q(1), 0),
                              ((1, 2, 0), Q(-1), 0)),
            ("the even-cycle cancellation changed", nonzero_terms))

    # Contraction of the nine Hessian reconstructions is exactly the
    # reconstruction for the contracted physical stars.  This is the
    # coefficientwise common-q naturality needed by the null-vector row.
    contracted_left = contract_vectors(p_vectors, left)
    contracted_right = contract_vectors(s_vectors, right)
    hessian_checks = 0
    for word_index, word in enumerate(A.WORDS):
        lhs = sum(adj[i][j] * cross[i][j][word_index]
                  for i, j in product(COLORS, repeat=2))
        rhs = H.reconstruct_coordinate(
            contracted_left, contracted_right, word, hessian)
        require(lhs == rhs,
                ("null contraction broke common-q Hessian naturality", word))
        hessian_checks += 1
    require(hessian_checks == 3 ** 6,
            "the contracted Hessian word census changed")

    # The local packet supplies the pure anchors and selected mixed zero row
    # for K.  It is not promoted to a full EqSystem source.
    local_cap_rows = tuple(
        (word, packet.cap_row(matrix, dict(enumerate(word))))
        for word in G.LOCAL_WORDS
    )
    require(tuple(value for _, value in local_cap_rows)
            == (Q(1), Q(1), Q(1), Q(0)),
            ("the singular local cap row changed", local_cap_rows))

    # Neither the singular cap nor its active rank-one adjugate is clean in
    # this exact physical packet.  This prevents silently replacing the
    # adjugate contraction by an active-clean landing.
    clean_ledgers = {}
    for name, cap, expected_count, expected_first in (
        ("singular_K", matrix, 8,
         ((0, 0, 0, 1, 0, 1), Q(-6))),
        ("active_adjugate", adj, 63,
         ((0, 0, 0, 0, 0, 1), Q(-4))),
    ):
        nonzero = tuple(
            (word, packet.E_word(cap, dict(enumerate(word))))
            for word in A.WORDS
            if packet.E_word(cap, dict(enumerate(word)))
        )
        require(len(nonzero) == expected_count and nonzero[0] == expected_first,
                ("clean-error ledger changed", name, len(nonzero), nonzero[:1]))
        clean_ledgers[name] = {
            "direct_scalar": str(packet.cap_s(cap)),
            "nonzero_clean_error_words": len(nonzero),
            "first": (nonzero[0][0], str(nonzero[0][1])),
        }

    # Recheck the first missing complete row, rather than inheriting only its
    # prose label from the local-guard dependency.
    defects = []
    for i, j in product(COLORS, repeat=2):
        for word in A.WORDS:
            value = packet.row(i, j, dict(enumerate(word)))
            target = Q(1) if i == j and word == (i,) * 6 else Q(0)
            if value != target:
                defects.append((i, j, word, value - target))
    require(len(defects) == 106 and defects[0]
            == (0, 0, (0, 0, 0, 0, 1, 1), Q(1)),
            ("the local packet's first complete-row defect changed",
             len(defects), defects[:1]))

    return {
        "matrix_K": tuple(tuple(map(str, row)) for row in matrix),
        "rank_det_per": (rank(matrix), str(determinant(matrix)),
                         str(permanent(matrix))),
        "diagonal": tuple(str(matrix[i][i]) for i in COLORS),
        "left_null": tuple(map(str, left)),
        "right_null": tuple(map(str, right)),
        "adjugate": tuple(tuple(map(str, row)) for row in adj),
        "direct": tuple(tuple(map(str, row)) for row in direct),
        "sigma_K": str(pairing(matrix, direct)),
        "beta_adjugate": str(beta),
        "nonzero_permutation_terms": tuple(
            (perm, str(value), parity) for perm, value, parity in nonzero_terms),
        "common_q": common_q,
        "contracted_hessian_checks": hessian_checks,
        "local_cap_rows": tuple((word, str(value))
                                for word, value in local_cap_rows),
        "clean_error": clean_ledgers,
        "complete_rows": {
            "satisfied": 9 * 3 ** 6 - len(defects),
            "defects": len(defects),
            "first_defect": (defects[0][0], defects[0][1], defects[0][2],
                             str(defects[0][3])),
        },
    }


def build_ledger():
    return {
        "theorem": "singular rank-two null/adjugate full-nine boundary",
        "pins": PINNED,
        "field_independent_reduction": {
            "hypotheses": (
                "rank(K)=2, every K_ii nonzero, sigma(K)=<K,a>=0, and "
                "all nine literal rows share one q"
            ),
            "null_contraction": (
                "xi^T K=0, K eta=0 implies beta q^[3]+"
                "p(xi)s(eta)q^[2]=sum_i xi_i eta_i X_i, "
                "beta=<xi eta^T,a>"
            ),
            "adjugate": (
                "adj(K)=gamma eta xi^T, so the null-contraction cap "
                "xi eta^T is gamma^{-1} adj(K)^T; its diagonal is the "
                "principal-cofactor diagonal up to one common scalar, and "
                "its nonzero count is exactly |supp(xi) intersect supp(eta)|"
            ),
            "support": (
                "both null supports have size at least two; their "
                "intersection has size 1,2,or3 and is never empty"
            ),
            "three_target_branch": (
                "if all three principal cofactors and beta are nonzero, "
                "the transposed-adjugate null contraction is a literal "
                "target-active rank-one cap, but "
                "cleanliness is an independent equation"
            ),
            "lower_target_branch": (
                "one or two nonzero principal cofactors give respectively "
                "a unary or binary one-channel null contraction"
            ),
            "hessian": (
                "contracting the nine common-q reconstruction equations "
                "commutes exactly with the null vectors; it introduces no "
                "new scalar equation beyond the contracted physical stars"
            ),
        },
        "normalized_finite_audit": normalized_rank_two_census(),
        "physical_local_counterguard": physical_cycle_guard(),
        "scope": {
            "positive": (
                "every forced singular cap routes source-validly to a "
                "one-channel unary/binary/ternary adjugate row"
            ),
            "negative": (
                "det(K)=0, nonzero diagonal anchors, and common-q Hessian "
                "naturality do not force an odd/permanent unit or a clean "
                "adjugate cap"
            ),
            "not_claimed": (
                "the displayed physical packet is exact on 36 scalar rows, "
                "not on all 6561; no full-nine source guard or Krenn "
                "counterexample is claimed"
            ),
            "first_new_obligation": (
                "the complete mixed/deleted-word row (0,0;000011), whose "
                "physical residual is +1 in the guard"
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("structural", "full", "exhaustive"),
                        default="structural")
    parser.add_argument("--dump-ledger", action="store_true")
    arguments = parser.parse_args()
    ledger = build_ledger()
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                "ledger digest changed: got %s" % digest)
    if arguments.dump_ledger:
        print(json.dumps(ledger, indent=2, sort_keys=True))
    print("PASS: singular rank-two null/adjugate boundary")
    print("F_5 normalized rank-two census: 3404 matrices; intersections 1/2/3")
    print("cycle guard: det=per=0, adj(K)=all-ones, beta=-2, dirty")
    print("first complete-row obligation: 00:000011 = +1")
    print("sha256:", digest)


if __name__ == "__main__":
    main()

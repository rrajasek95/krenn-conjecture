#!/usr/bin/env python3
"""Exact two-site contraction/deletion identities for decorated hafnians.

For arbitrary endpoint matrices A_uv and a bilinear covector C on sites
p,q, this checker verifies

    contr_C H_S(A) = s_C H_R(A) + D H_R(A)[B_C],

where R=S-{p,q}, s_C=<C,A_pq>, and B_C is the symmetrized product of the
two contracted endpoint stars.  Literal deletion from the same source is
H_R(A); consequently contraction is a nonzero scalar deletion exactly when
the derivative correction is a scalar multiple of H_R(A).

Two exact minimal counterguards show that source minimality does not force a
good pair.  The six-edge K4 realization of Delta_(4,3) has nonzero trace
correction at every pair.  The cancellation-rich nine-cell realization of
Delta_(6,2) likewise has no pair whose induced four-site source is a scalar
Delta_(4,2).  Finally, a scalar six-site example shows why replacing B_C by
Schur-complement edges is invalid: the contraction has only the first
directional derivative, while the updated hafnian creates higher B terms.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/small-tensor-findings.md":
        "d12784e3772582615e4f58ff93ead825fe0fea33cbb3cb62a6c6ee60b6ef792c",
    "notes/tensor-route.md":
        "de5be830daf11861814af84d8ea3369090dfcc9fb849a9255b9e984d470778a2",
    "notes/product-cap-monomer-reduction.md":
        "84d2d44f24b35335e9afb68665a3682363850affcf2add01ff08eca19e820fec",
    "computations/verify_product_cap_four_cumulant.py":
        "0c57532110f5b14b55c91cfeb4f09225571679225c5ae3bba75ba32f7a8bce13",
}
EXPECTED_LEDGER_SHA256 = (
    "7c989a93c97dc8d5a678629f74701dae3bfc80f468edc429120c9e5bbca090e6"
)

Matrix = dict[tuple[int, int], Q]
System = dict[tuple[int, int], Matrix]
Tensor = dict[tuple[int, ...], Q]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def edge_key(u: int, v: int) -> tuple[int, int]:
    require(u != v, "loops are forbidden")
    return (u, v) if u < v else (v, u)


def edge_entry(system: System, u: int, v: int,
               colour_u: int, colour_v: int) -> Q:
    key = edge_key(u, v)
    if u < v:
        return system.get(key, {}).get((colour_u, colour_v), Q(0))
    return system.get(key, {}).get((colour_v, colour_u), Q(0))


def matrix(system: System, u: int, v: int, colours: int) -> Matrix:
    return {
        (a, b): edge_entry(system, u, v, a, b)
        for a in range(colours) for b in range(colours)
        if edge_entry(system, u, v, a, b)
    }


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield (edge_key(first, second),) + tail


def hafnian_coefficient(system: System, vertices: tuple[int, ...],
                        word: tuple[int, ...]) -> Q:
    require(len(vertices) == len(word), "word length")
    colours_at = dict(zip(vertices, word, strict=True))
    answer = Q(0)
    for matching in perfect_matchings(vertices):
        term = Q(1)
        for u, v in matching:
            term *= edge_entry(system, u, v, colours_at[u], colours_at[v])
        answer += term
    return answer


def hafnian_tensor(system: System, vertices: tuple[int, ...],
                   colours: int) -> Tensor:
    answer = {}
    for word in product(range(colours), repeat=len(vertices)):
        value = hafnian_coefficient(system, vertices, word)
        if value:
            answer[word] = value
    return answer


def contract_tensor(top: Tensor, vertices: tuple[int, ...], p: int, q: int,
                    covector: Matrix, colours: int) -> Tensor:
    residual = tuple(v for v in vertices if v not in (p, q))
    position = {vertex: index for index, vertex in enumerate(vertices)}
    answer = {}
    for residual_word in product(range(colours), repeat=len(residual)):
        residual_at = dict(zip(residual, residual_word, strict=True))
        value = Q(0)
        for a, b in product(range(colours), repeat=2):
            word = tuple(a if vertex == p else b if vertex == q
                         else residual_at[vertex] for vertex in vertices)
            value += covector.get((a, b), Q(0)) * top.get(word, Q(0))
        if value:
            answer[residual_word] = value
    require(set(position) == set(vertices), "position audit")
    return answer


def scale_tensor(coefficient: Q, value: Tensor) -> Tensor:
    return {word: coefficient * entry for word, entry in value.items()
            if coefficient * entry}


def add_tensors(*values: Tensor) -> Tensor:
    answer = Counter()
    for value in values:
        answer.update(value)
    return {word: entry for word, entry in answer.items() if entry}


def scalar_pair(system: System, p: int, q: int,
                covector: Matrix, colours: int) -> Q:
    return sum((coefficient * edge_entry(system, p, q, a, b)
                for (a, b), coefficient in covector.items()), Q(0))


def cross_matrix(system: System, p: int, q: int, i: int, j: int,
                 covector: Matrix, colours: int) -> Matrix:
    answer = {}
    for ci, cj in product(range(colours), repeat=2):
        value = Q(0)
        for (a, b), coefficient in covector.items():
            value += coefficient * (
                edge_entry(system, p, i, a, ci)
                * edge_entry(system, q, j, b, cj)
                + edge_entry(system, q, i, b, ci)
                * edge_entry(system, p, j, a, cj)
            )
        if value:
            answer[ci, cj] = value
    return answer


def cross_system(system: System, vertices: tuple[int, ...], p: int, q: int,
                 covector: Matrix, colours: int) -> System:
    residual = tuple(v for v in vertices if v not in (p, q))
    answer = {}
    for i, j in combinations(residual, 2):
        value = cross_matrix(system, p, q, i, j, covector, colours)
        if value:
            answer[i, j] = value
    return answer


def directional_hafnian(system: System, direction: System,
                         vertices: tuple[int, ...], colours: int) -> Tensor:
    answer = {}
    position = {vertex: index for index, vertex in enumerate(vertices)}
    for word in product(range(colours), repeat=len(vertices)):
        colours_at = dict(zip(vertices, word, strict=True))
        total = Q(0)
        for matching in perfect_matchings(vertices):
            for selected in matching:
                term = edge_entry(direction, *selected,
                                  colours_at[selected[0]],
                                  colours_at[selected[1]])
                for edge in matching:
                    if edge == selected:
                        continue
                    term *= edge_entry(system, *edge,
                                       colours_at[edge[0]],
                                       colours_at[edge[1]])
                total += term
        if total:
            answer[word] = total
    require(len(position) == len(vertices), "direction position audit")
    return answer


def diagonal_tensor(order: int, colours: int,
                    coefficients: tuple[Q, ...] | None = None) -> Tensor:
    if coefficients is None:
        coefficients = (Q(1),) * colours
    require(len(coefficients) == colours, "diagonal coefficients")
    return {(colour,) * order: coefficient
            for colour, coefficient in enumerate(coefficients) if coefficient}


def proportional(left: Tensor, right: Tensor) -> tuple[bool, Q | None]:
    support = set(left) | set(right)
    if not support:
        return True, Q(0)
    pivot = next((word for word in support if right.get(word, Q(0))), None)
    if pivot is None:
        return False, None
    coefficient = left.get(pivot, Q(0)) / right[pivot]
    return (all(left.get(word, Q(0))
                == coefficient * right.get(word, Q(0)) for word in support),
            coefficient)


def verify_contraction_formula(system: System, vertices: tuple[int, ...],
                               p: int, q: int, covector: Matrix,
                               colours: int) -> dict[str, object]:
    top = hafnian_tensor(system, vertices, colours)
    residual = tuple(v for v in vertices if v not in (p, q))
    deleted = hafnian_tensor(system, residual, colours)
    contracted = contract_tensor(top, vertices, p, q, covector, colours)
    scalar = scalar_pair(system, p, q, covector, colours)
    direction = cross_system(system, vertices, p, q, covector, colours)
    derivative = directional_hafnian(system, direction, residual, colours)
    require(contracted == add_tensors(scale_tensor(scalar, deleted), derivative),
            ("two-site contraction formula failed", p, q, covector))
    deletion_projective, deletion_scalar = proportional(contracted, deleted)
    correction_projective, correction_scalar = proportional(derivative, deleted)
    require(deletion_projective == correction_projective,
            "the projective correction criterion changed")
    if deleted and deletion_projective:
        require(deletion_scalar == scalar + correction_scalar,
                "projective scalar identity")
    nonzero_scalar_deletion = bool(deleted) and deletion_projective \
        and deletion_scalar not in (None, Q(0))
    return {
        "pair": [p, q],
        "s_C": str(scalar),
        "B_nonzero_edges": len(direction),
        "deleted_support": len(deleted),
        "correction_support": len(derivative),
        "contraction_is_scalar_literal_deletion": nonzero_scalar_deletion,
        "deletion_scalar": (None if deletion_scalar is None
                            else str(deletion_scalar)),
    }


def k4_delta3_system() -> tuple[System, tuple[int, ...], int]:
    system: System = {}
    for colour, matching in enumerate((((0, 1), (2, 3)),
                                       ((0, 2), (1, 3)),
                                       ((0, 3), (1, 2)))):
        for edge in matching:
            system[edge_key(*edge)] = {(colour, colour): Q(1)}
    return system, (0, 1, 2, 3), 3


def audit_k4_minimal_counterguard() -> dict[str, object]:
    system, vertices, colours = k4_delta3_system()
    top = hafnian_tensor(system, vertices, colours)
    require(top == diagonal_tensor(4, 3), "K4 stopped realizing Delta_4,3")

    trace = {(a, a): Q(1) for a in range(colours)}
    records = []
    endpoint_basis = Counter()
    for p, q in combinations(vertices, 2):
        record = verify_contraction_formula(
            system, vertices, p, q, trace, colours
        )
        require(not record["contraction_is_scalar_literal_deletion"]
                and record["B_nonzero_edges"] == 1,
                ("K4 acquired a trace-deletion pair", record))
        residual = tuple(v for v in vertices if v not in (p, q))
        deleted = hafnian_tensor(system, residual, colours)
        require(len(deleted) == 1, "K4 deletion stopped being one pure edge")
        edge_colour = next(iter(deleted))[0]

        # Exercise every ordered endpoint colour.  Equal colour matching the
        # pq edge is the direct term; the other two equal colours are the two
        # cross matchings.  Off-diagonal endpoint contractions vanish.
        pq_entry_colour = next(iter(matrix(system, p, q, colours)))[0]
        require(edge_colour == pq_entry_colour,
                "complement and selected K4 edge colours diverged")
        for a, b in product(range(colours), repeat=2):
            covector = {(a, b): Q(1)}
            basis_record = verify_contraction_formula(
                system, vertices, p, q, covector, colours
            )
            contracted = contract_tensor(top, vertices, p, q,
                                         covector, colours)
            expected = diagonal_tensor(
                2, colours,
                tuple(Q(int(a == b == colour)) for colour in range(colours))
            )
            require(contracted == expected,
                    ("arbitrary endpoint contraction changed", p, q, a, b))
            kind = (
                "offdiagonal_zero" if a != b else
                "direct_same_colour" if a == pq_entry_colour else
                "cross_same_colour"
            )
            endpoint_basis[kind] += 1
            if kind == "direct_same_colour":
                require(basis_record["s_C"] == "1"
                        and basis_record["B_nonzero_edges"] == 0,
                        (kind, basis_record))
            elif kind == "cross_same_colour":
                require(basis_record["s_C"] == "0"
                        and basis_record["B_nonzero_edges"] == 1,
                        (kind, basis_record))
            else:
                require(basis_record["s_C"] == "0"
                        and basis_record["B_nonzero_edges"] == 0,
                        (kind, basis_record))
        records.append(record)

    # Every one of the six decorated entries is essential: deleting it
    # removes the unique monomial for its diagonal colour.
    essential = 0
    for edge, entries in tuple(system.items()):
        require(len(entries) == 1, "K4 cell count")
        smaller = {key: dict(value) for key, value in system.items()}
        del smaller[edge]
        if hafnian_tensor(smaller, vertices, colours) != top:
            essential += 1
    require(essential == 6, "K4 stopped being cell-minimal")
    return {
        "target": "Delta_(4,3)",
        "nonzero_decorated_cells": 6,
        "every_cell_essential": essential == 6,
        "trace_pairs_tested": len(records),
        "trace_pairs_giving_scalar_literal_deletion": sum(
            record["contraction_is_scalar_literal_deletion"]
            for record in records
        ),
        "trace_pair_records": records,
        "ordered_endpoint_basis_census": dict(endpoint_basis),
        "conclusion": (
            "even an inclusion-minimal exact diagonal hafnian source need "
            "not have a pair whose all-colours contraction is represented "
            "by literal deletion"
        ),
    }


def n6_delta2_cancellation_system() -> tuple[System, tuple[int, ...], int]:
    # Zero-based form of the exact example in small-tensor-findings.md.
    system: System = {
        (0, 1): {(0, 0): Q(1), (1, 0): Q(1)},
        (2, 3): {(0, 0): Q(1)},
        (4, 5): {(0, 0): Q(1)},
        (1, 3): {(0, 0): Q(1)},
        (0, 2): {(1, 0): Q(-1)},
        (0, 5): {(1, 1): Q(1)},
        (1, 2): {(1, 1): Q(1)},
        (3, 4): {(1, 1): Q(1)},
    }
    return system, tuple(range(6)), 2


def audit_n6_cancellation_counterguard() -> dict[str, object]:
    system, vertices, colours = n6_delta2_cancellation_system()
    top = hafnian_tensor(system, vertices, colours)
    require(top == diagonal_tensor(6, 2), "six-site cancellation target changed")
    trace = {(0, 0): Q(1), (1, 1): Q(1)}
    records = []
    support_census = Counter()
    endpoint_basis_census = Counter()
    dense_covector = {
        (0, 0): Q(1), (0, 1): Q(2),
        (1, 0): Q(3), (1, 1): Q(-1),
    }
    for p, q in combinations(vertices, 2):
        record = verify_contraction_formula(
            system, vertices, p, q, trace, colours
        )
        require(not record["contraction_is_scalar_literal_deletion"],
                ("six-site example acquired an inductive pair", record))
        require(record["B_nonzero_edges"] > 0,
                ("trace cross system vanished", record))
        support_census[record["deleted_support"]] += 1
        records.append(record)

        residual = tuple(v for v in vertices if v not in (p, q))
        for a, b in product(range(colours), repeat=2):
            covector = {(a, b): Q(1)}
            verify_contraction_formula(system, vertices, p, q,
                                       covector, colours)
            contracted = contract_tensor(top, vertices, p, q,
                                         covector, colours)
            expected = (diagonal_tensor(
                len(residual), colours,
                tuple(Q(int(a == b == colour))
                      for colour in range(colours))
            ))
            require(contracted == expected,
                    ("n6 ordered endpoint contraction changed", p, q, a, b))
            endpoint_basis_census[
                "diagonal_pure" if a == b else "offdiagonal_zero"
            ] += 1

        verify_contraction_formula(system, vertices, p, q,
                                   dense_covector, colours)
        require(contract_tensor(top, vertices, p, q,
                                dense_covector, colours)
                == diagonal_tensor(len(residual), colours,
                                   (Q(1), Q(-1))),
                ("dense asymmetric endpoint cap changed", p, q))

    # Every decorated matrix cell, including the two cells on edge 01, is
    # essential to the exact output tensor.
    essential = 0
    cell_count = sum(len(entries) for entries in system.values())
    for edge, entries in tuple(system.items()):
        for cell in tuple(entries):
            smaller = {key: dict(value) for key, value in system.items()}
            del smaller[edge][cell]
            if not smaller[edge]:
                del smaller[edge]
            if hafnian_tensor(smaller, vertices, colours) != top:
                essential += 1
    require(cell_count == essential == 9,
            ("six-site source minimality changed", cell_count, essential))
    return {
        "target": "Delta_(6,2)",
        "underlying_edges": len(system),
        "nonzero_decorated_cells": cell_count,
        "every_cell_essential": essential == cell_count,
        "trace_pairs_tested": len(records),
        "trace_pairs_giving_scalar_literal_deletion": sum(
            record["contraction_is_scalar_literal_deletion"]
            for record in records
        ),
        "deleted_tensor_support_census": {
            str(size): count for size, count in sorted(support_census.items())
        },
        "ordered_endpoint_basis_census": dict(endpoint_basis_census),
        "dense_asymmetric_covectors_tested": len(records),
        "dense_cap": "[[1,2],[3,-1]] -> e0^R-e1^R",
        "pair_records": records,
        "conclusion": (
            "at even order six, exact cancellation and cell-minimality still "
            "do not force a trace contraction with no projective cross-source "
            "correction; a ternary proof must use genuinely r=3 data"
        ),
    }


def audit_schur_replacement_failure() -> dict[str, object]:
    # Scalar sites p=4,q=5 and boundary 0,1,2,3.  The old boundary system is
    # zero.  p connects 0,2; q connects 1,3; pq is a unit.  Hence B is K2,2
    # on the boundary.  The exact contraction contains only H+D H[B]=0,
    # whereas replacing old edges by B creates its two perfect matchings.
    vertices = tuple(range(6))
    p, q = 4, 5
    system: System = {
        (p, q): {(0, 0): Q(1)},
        edge_key(p, 0): {(0, 0): Q(1)},
        edge_key(p, 2): {(0, 0): Q(1)},
        edge_key(q, 1): {(0, 0): Q(1)},
        edge_key(q, 3): {(0, 0): Q(1)},
    }
    covector = {(0, 0): Q(1)}
    record = verify_contraction_formula(system, vertices, p, q,
                                        covector, 1)
    residual = (0, 1, 2, 3)
    old = {edge: value for edge, value in system.items()
           if p not in edge and q not in edge}
    direction = cross_system(system, vertices, p, q, covector, 1)
    updated = {edge: dict(value) for edge, value in old.items()}
    for edge, entries in direction.items():
        target = updated.setdefault(edge, {})
        for cell, value in entries.items():
            target[cell] = target.get(cell, Q(0)) + value
    old_h = hafnian_tensor(old, residual, 1)
    first = directional_hafnian(old, direction, residual, 1)
    schur_h = hafnian_tensor(updated, residual, 1)
    require(record["s_C"] == "1" and old_h == {} and first == {}
            and schur_h == {(0, 0, 0, 0): Q(2)},
            ("Schur counterguard changed", record, old_h, first, schur_h))
    return {
        "scalar_pair_s": 1,
        "cross_edges": [list(edge) for edge in sorted(direction)],
        "literal_contraction": 0,
        "old_deleted_hafnian": 0,
        "first_directional_derivative": 0,
        "hafnian_after_edge_update_A_plus_B": 2,
        "first_missing_term": "(1/2) D^2 H[A][B,B] = 2",
        "criterion": (
            "when s is a unit, the Schur edge update A+B/s represents the "
            "contraction iff the sum of Taylor terms of order at least two "
            "vanishes in the top residual degree"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "decorated hafnian two-site contraction/deletion counterguard",
        "pins": PINS,
        "exact_identity": {
            "formula": "contr_C H_S=s_C H_R+D H_R[B_C]",
            "s_C": "<C,A_pq>",
            "pure_endpoint_formula": (
                "B^(a,b)_ij=u_i^a tensor v_j^b + "
                "v_i^b tensor u_j^a"
            ),
            "target_contraction": (
                "contr_C Delta_(S,r)=sum_a C_(a,a) e_a^(tensor R)"
            ),
            "literal_deletion": "H_R(A) from the induced same source",
            "nonzero_projective_deletion_criterion": (
                "D H_R[B_C] lies in <H_R(A)> and the resulting scalar is nonzero"
            ),
            "all_colour_trace_specialization": (
                "for C=I and H_S=Delta, this holds iff H_R(A) is a nonzero "
                "scalar multiple of the smaller Delta"
            ),
            "squarefree_Grassmann_scope": (
                "the hafnian lives in the commutative square-zero/zeon "
                "algebra.  Its cross star product is symmetric (+), not the "
                "alternating Pluecker wedge (-); ordinary Grassmann rank-one "
                "or Pfaffian Schur identities do not remove B_C"
            ),
        },
        "minimal_ternary_K4_counterguard": audit_k4_minimal_counterguard(),
        "six_site_binary_cancellation_counterguard":
            audit_n6_cancellation_counterguard(),
        "ordinary_Schur_update_counterguard": audit_schur_replacement_failure(),
        "verdict": (
            "No pair-without-cross-correction theorem follows from the "
            "decorated hafnian contraction identity plus source-cell "
            "minimality.  Exact minimal diagonal sources can have nonzero "
            "projective correction at every pair.  In the all-colour trace "
            "case, asking for a good pair is exactly asking that one induced "
            "deleted subsystem already realize the smaller diagonal target, "
            "so the contraction formula alone is an induction restatement."
        ),
        "remaining_positive_route": (
            "a ternary n>=6 proof must add a genuinely global incidence or "
            "minimal-support theorem forcing H_(S-{p,q}) proportional to "
            "Delta for some pair, or force the projective class of D H[B] "
            "to vanish.  Neither arbitrary endpoint-colour algebra, "
            "commutative-squarefree Grassmann relations, nor Schur updating "
            "supplies that theorem."
        ),
        "scope": (
            "exact arbitrary endpoint matrices and bilinear caps.  The K4 "
            "guard is ternary but below the n>=6 range; the n=6 guard is "
            "binary.  Together they refute a uniform minimality/contraction "
            "lemma, not a specifically ternary n>=6 theorem."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("freeze EXPECTED_LEDGER_SHA256=" + digest)
        return
    print("two-site decorated contraction identity: EXACT")
    print("same-source deletion criterion: PROJECTIVE CROSS CLASS ZERO")
    print("minimal ternary K4 good trace pairs: 0/6")
    print("minimal binary n6 good trace pairs: 0/15")
    print("ordinary hafnian Schur edge update: FALSE")
    print("remaining theorem must be ternary+n>=6+global incidence")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

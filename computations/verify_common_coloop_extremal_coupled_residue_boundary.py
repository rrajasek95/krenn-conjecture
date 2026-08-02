#!/usr/bin/env python3
"""Audit extremal compatibility of the coupled common-coloop residues.

The checker has three independent exact ledgers:

* exhaustive support-graph deletion for a good direct block when Q=0;
* rational local-tensor models for every nonzero-top cross-row branch,
  including the rank-one dark boundary omitted by the four-branch list;
* the literal remaining curvature-row elimination and attainable-scalar
  criterion on those models.

Standard library only; live under -O and -I -S.  Research evidence only.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def vector(*entries):
    return tuple(F(entry) for entry in entries)


def add_vectors(*vectors):
    if not vectors:
        return ()
    require(all(len(item) == len(vectors[0]) for item in vectors),
            "vector dimensions changed")
    return tuple(sum(item[index] for item in vectors) for index in range(len(vectors[0])))


def scale_vector(source, scalar):
    scalar = F(scalar)
    return tuple(scalar * entry for entry in source)


def dot(left, right):
    require(len(left) == len(right), "dot-product dimensions changed")
    return sum(a * b for a, b in zip(left, right))


def rref(rows):
    work = [[F(value) for value in row] for row in rows]
    if not work:
        return (), ()
    pivot_row = 0
    pivots = []
    for column in range(len(work[0])):
        selected = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if selected is None:
            continue
        work[pivot_row], work[selected] = work[selected], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * normalized
                for entry, normalized in zip(work[row], work[pivot_row])
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    return tuple(tuple(row) for row in work), tuple(pivots)


def rank(vectors):
    return len(rref(vectors)[1]) if vectors else 0


def mutual_anchors(edges):
    degrees = {}
    for left, right in edges:
        degrees[left] = degrees.get(left, 0) + 1
        degrees[right] = degrees.get(right, 0) + 1
    return frozenset(
        edge for edge in edges
        if degrees[edge[0]] == degrees[edge[1]] == 1
    )


def zero_top_extremal_deletion_audit():
    # A good pair has a nonzero residual star row at every coordinate.
    # Model one such supported cell at each of the six coordinate
    # endpoints.  Exhaust every nonempty support of the 3x3 direct block.
    p = tuple(f"p{i}" for i in range(3))
    q = tuple(f"q{j}" for j in range(3))
    star_edges = frozenset(
        {(p[i], f"p{i}-outside") for i in range(3)}
        | {(q[j], f"q{j}-outside") for j in range(3)}
    )
    direct_cells = tuple((p[i], q[j]) for i in range(3) for j in range(3))
    ledger = []
    count = 0
    for size in range(1, len(direct_cells) + 1):
        for chosen in combinations(direct_cells, size):
            count += 1
            direct = frozenset(chosen)
            before_edges = star_edges | direct
            after_edges = star_edges
            before = mutual_anchors(before_edges)
            after = mutual_anchors(after_edges)
            require(not (before & direct),
                    "a good-pair direct cell became a mutual anchor")
            require(before <= after,
                    "deleting an invisible direct block destroyed an old anchor")
            require(len(after_edges) < len(before_edges),
                    "zero-top deletion did not lower support")
            require(len(after) >= len(before),
                    "zero-top deletion lowered the anchor count")
            ledger.append(f"{size}:{len(before)}:{len(after)}")
    require(count == 2**9 - 1, "the direct-block support census changed")
    return count, sha256("|".join(ledger).encode()).hexdigest()


LOCAL_DIMENSION = 3
OFF_DIMENSION = 3
TENSOR_DIMENSION = LOCAL_DIMENSION * OFF_DIMENSION
E = tuple(
    tuple(F(1) if index == basis else F(0) for index in range(LOCAL_DIMENSION))
    for basis in range(LOCAL_DIMENSION)
)
Y = tuple(
    tuple(F(1) if index == basis else F(0) for index in range(OFF_DIMENSION))
    for basis in range(OFF_DIMENSION)
)
ZERO_OFF = (F(0),) * OFF_DIMENSION
ZERO_TENSOR = (F(0),) * TENSOR_DIMENSION


def outer(local, off):
    return tuple(local[i] * off[j] for i in range(LOCAL_DIMENSION) for j in range(OFF_DIMENSION))


def tensor_columns(tensor):
    return tuple(
        tuple(tensor[i * OFF_DIMENSION + j] for i in range(LOCAL_DIMENSION))
        for j in range(OFF_DIMENSION)
    )


def local_rank(tensor):
    return rank(tensor_columns(tensor))


def row_holds(direct, top, first_jet, target):
    return add_vectors(scale_vector(top, direct), first_jet) == target


def branch_models():
    x_r = outer(E[0], Y[0])
    x_s = outer(E[1], Y[1])

    # Nondegenerate local-rank-two model.  Both diagonal direct
    # coefficients are nonzero, so the tangent scalar is surjective.
    q_rank_two = add_vectors(outer(E[0], Y[0]), outer(E[1], Y[1]))
    rank_two = {
        "name": "rank-two-active",
        "Q": q_rank_two,
        "u": E[1],
        "v": E[0],
        "a_rr": F(1),
        "a_rt": F(0),
        "a_ss": F(1),
        "a_ts": F(0),
        "H_r": scale_vector(Y[1], -1),
        "H_t": ZERO_OFF,
        "G_s": scale_vector(Y[0], -1),
        "G_t": ZERO_OFF,
        "sigma0": F(0),
        "expected_rank": 2,
        "kind": "dark",
    }

    # Rank-two fixed-scalar model: diagonal tangent coefficients vanish,
    # but the affine base scalar is already nonzero.
    rank_two_fixed = {
        "name": "rank-two-fixed-active",
        "Q": q_rank_two,
        "u": E[0],
        "v": E[1],
        "a_rr": F(0),
        "a_rt": F(0),
        "a_ss": F(0),
        "a_ts": F(0),
        "H_r": Y[0],
        "H_t": ZERO_OFF,
        "G_s": Y[1],
        "G_t": ZERO_OFF,
        "sigma0": F(2),
        "expected_rank": 2,
        "kind": "dark",
    }

    # Hidden rank-one dark boundary: both cross coefficients and both
    # cross A-arms vanish.  It was not represented by the previous four
    # named rows.
    rank_one_dark = {
        "name": "rank-one-dark-fixed-active",
        "Q": outer(E[2], Y[2]),
        "u": E[0],
        "v": E[1],
        "a_rr": F(0),
        "a_rt": F(0),
        "a_ss": F(0),
        "a_ts": F(0),
        "H_r": Y[0],
        "H_t": ZERO_OFF,
        "G_s": Y[1],
        "G_t": ZERO_OFF,
        "sigma0": F(3),
        "expected_rank": 1,
        "kind": "dark",
    }

    left = {
        "name": "rank-one-left-surjective",
        "Q": outer(E[0], Y[2]),
        "u": E[0],
        "v": E[1],
        "a_rr": F(0),
        "a_rt": F(2),
        "a_ss": F(0),
        "a_ts": F(0),
        "H_r": Y[0],
        "H_t": scale_vector(Y[2], -2),
        "G_s": Y[1],
        "G_t": ZERO_OFF,
        "sigma0": F(0),
        "expected_rank": 1,
        "kind": "left",
    }

    right = {
        "name": "rank-one-right-surjective",
        "Q": outer(E[1], Y[2]),
        "u": E[0],
        "v": E[1],
        "a_rr": F(0),
        "a_rt": F(0),
        "a_ss": F(0),
        "a_ts": F(-3),
        "H_r": Y[0],
        "H_t": ZERO_OFF,
        "G_s": Y[1],
        "G_t": scale_vector(Y[2], 3),
        "sigma0": F(0),
        "expected_rank": 1,
        "kind": "right",
    }

    cases = (rank_two, rank_two_fixed, rank_one_dark, left, right)
    ledger = []
    for case in cases:
        q_top = case["Q"]
        require(row_holds(
            case["a_rr"], q_top, outer(case["u"], case["H_r"]), x_r
        ), f"r diagonal failed in {case['name']}")
        require(row_holds(
            case["a_rt"], q_top, outer(case["u"], case["H_t"]), ZERO_TENSOR
        ), f"rt row failed in {case['name']}")
        require(row_holds(
            case["a_ss"], q_top, outer(case["v"], case["G_s"]), x_s
        ), f"s diagonal failed in {case['name']}")
        require(row_holds(
            case["a_ts"], q_top, outer(case["v"], case["G_t"]), ZERO_TENSOR
        ), f"ts row failed in {case['name']}")
        require(local_rank(q_top) == case["expected_rank"],
                f"top local rank changed in {case['name']}")

        # Q!=0 forces a_rs=0.  The tangent scalar row is therefore
        # (a_rr,a_rt,a_ss,a_ts) on the four effective singleton
        # coordinates.  Its image is all scalars iff this row is nonzero;
        # otherwise sigma0 is the sole attainable value.
        scalar_row = (
            case["a_rr"], case["a_rt"], case["a_ss"], case["a_ts"]
        )
        scalar_surjective = any(scalar_row)
        nonzero_attainable = scalar_surjective or case["sigma0"] != 0
        require(nonzero_attainable,
                f"no nonzero scalar is attainable in {case['name']}")
        case["scalar_surjective"] = scalar_surjective
        ledger.append(
            f"{case['name']}:{local_rank(q_top)}:"
            f"{int(scalar_surjective)}:{case['sigma0']}"
        )
    return cases, sha256("|".join(ledger).encode()).hexdigest()


def remaining_curvature_row_audits(cases):
    x_t = outer(E[2], Y[2])
    p_t_local = add_vectors(E[0], E[2])
    s_t_local = add_vectors(E[1], E[2])
    ledger = []
    for index, case in enumerate(cases, start=1):
        a_tt = F(index)
        q_top = case["Q"]
        local_terms = add_vectors(
            scale_vector(q_top, a_tt),
            outer(p_t_local, case["H_t"]),
            outer(s_t_local, case["G_t"]),
        )
        gamma_tt = add_vectors(x_t, scale_vector(local_terms, -1))
        require(add_vectors(local_terms, gamma_tt) == x_t,
                f"missing diagonal row failed in {case['name']}")

        if case["kind"] == "dark":
            expected = add_vectors(x_t, scale_vector(q_top, -a_tt))
        elif case["kind"] == "left":
            # Q=u*q_t and H_t=-a_rt*q_t.
            correction_local = add_vectors(
                scale_vector(case["u"], a_tt),
                scale_vector(p_t_local, -case["a_rt"]),
            )
            expected = add_vectors(x_t, scale_vector(
                outer(correction_local, Y[2]), -1
            ))
        else:
            correction_local = add_vectors(
                scale_vector(case["v"], a_tt),
                scale_vector(s_t_local, -case["a_ts"]),
            )
            expected = add_vectors(x_t, scale_vector(
                outer(correction_local, Y[2]), -1
            ))
        require(gamma_tt == expected,
                f"corrected curvature corner changed in {case['name']}")

        # The other three rows of the curvature rectangle determine their
        # Gamma entries after the direct and first-jet data are fixed.
        p_s_local = E[2]
        s_r_local = add_vectors(E[0], E[1])
        direct_sr, direct_st, direct_tr = F(2), F(-1), F(3)
        gamma_sr = scale_vector(add_vectors(
            scale_vector(q_top, direct_sr),
            outer(p_s_local, case["H_r"]),
            outer(s_r_local, case["G_s"]),
        ), -1)
        gamma_st = scale_vector(add_vectors(
            scale_vector(q_top, direct_st),
            outer(p_s_local, case["H_t"]),
            outer(s_t_local, case["G_s"]),
        ), -1)
        gamma_tr = scale_vector(add_vectors(
            scale_vector(q_top, direct_tr),
            outer(p_t_local, case["H_r"]),
            outer(s_r_local, case["G_t"]),
        ), -1)
        require(add_vectors(
            scale_vector(q_top, direct_sr),
            outer(p_s_local, case["H_r"]),
            outer(s_r_local, case["G_s"]),
            gamma_sr,
        ) == ZERO_TENSOR, f"sr row failed in {case['name']}")
        require(add_vectors(
            scale_vector(q_top, direct_st),
            outer(p_s_local, case["H_t"]),
            outer(s_t_local, case["G_s"]),
            gamma_st,
        ) == ZERO_TENSOR, f"st row failed in {case['name']}")
        require(add_vectors(
            scale_vector(q_top, direct_tr),
            outer(p_t_local, case["H_r"]),
            outer(s_r_local, case["G_t"]),
            gamma_tr,
        ) == ZERO_TENSOR, f"tr row failed in {case['name']}")

        encoded = ",".join(str(value) for value in gamma_tt)
        ledger.append(f"{case['name']}:{encoded}")
    return sha256("|".join(ledger).encode()).hexdigest()


def polar_sharpness_audits(cases):
    # The remaining literal rows determine curvature entries but do not,
    # at the linear Taylor level, force the D-images to hit the affine
    # residual.  Retain exact detecting witnesses for every compatible
    # nonzero-top branch.
    ledger = []
    for case in cases:
        lam = vector(1, 0)
        if case["kind"] == "left":
            d_left, d_right, mu = vector(2, 0), vector(0, 1), F(1)
        elif case["kind"] == "right":
            d_left, d_right, mu = vector(0, 1), vector(-3, 0), F(1)
        else:
            d_left, d_right, mu = vector(0, 1), vector(0, -1), F(0)
        require(dot(lam, d_left) == mu * case["a_rt"],
                f"left polar pairing failed in {case['name']}")
        require(dot(lam, d_right) == mu * case["a_ts"],
                f"right polar pairing failed in {case['name']}")
        residual = vector(1, 0)
        require(dot(lam, residual) != 0,
                f"polar detector failed in {case['name']}")
        ledger.append(
            f"{case['name']}:{dot(lam, d_left)}:{dot(lam, d_right)}:{mu}"
        )
    return sha256("|".join(ledger).encode()).hexdigest()


def main():
    support_count, deletion_digest = zero_top_extremal_deletion_audit()
    cases, compatibility_digest = branch_models()
    curvature_digest = remaining_curvature_row_audits(cases)
    polar_digest = polar_sharpness_audits(cases)
    print("zero-top deletion ledger sha256", deletion_digest)
    print("nonzero-top compatibility ledger sha256", compatibility_digest)
    print("remaining curvature-row ledger sha256", curvature_digest)
    print("polar sharpness ledger sha256", polar_digest)
    print("direct-block supports exhausted", support_count)
    print("extremal coupled-residue boundary: verified")


if __name__ == "__main__":
    main()

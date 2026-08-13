#!/usr/bin/env python3
"""Locate the first physical-presentation obstruction to the response shear.

The augmentation-zero universal occurrence family is algebraically trivial
on the free ninety-coordinate occurrence space.  If ``1`` is the all-ones
column and ``z`` has zero sum, then

    M_z = I - 1 z^T,       M_z^{-1}=I+1 z^T,
    1^T M_z u = R-N z^T u.

This does not imply a trivialization through the physical monomial
presentation ``u_(i,j,M)=p_i s_j product_(e in M) q_e``.  On the first
two-orientation/two-matching rectangle the toric relation has differential
on the constant shear

    (p1*s0-p0*s1)*(q23*q45-q24*q35).

More generally, in the fixed-endpoint 2 by 3 Segre block the constant shear
is tangent iff the two endpoint-orientation values agree or all three
matching values agree.  An exact response-fibre point shows that neither is
forced by the aggregate response equation: the physical Jacobian has rank
12 and adjoining the constant shear raises it to 13.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
N = 90
SITES = tuple(range(6))
EDGES = tuple(combinations(SITES, 2))
PINS = {
    "computations/verify_h3_universal_response_deformation_e14_orbit_ks_gate.py":
        "39713f3683dd3d2376e5a911987ee3670ec291cf850072d6b4932e7a93745fc7",
    "notes/h3-universal-response-deformation-e14-orbit-ks-gate.md":
        "d9032c365e8fd8fb5baf320dcc5adac8832c023119fb7d4df69d02cce3d5878f",
    "computations/verify_h3_universal_response_ks_augmented_readout_extension_gate.py":
        "4493274dfbda62cec0d6823272762fb01c3a798123a1da206559e91890ba9047",
    "notes/h3-universal-response-ks-augmented-readout-extension-gate.md":
        "f201fd4c4599a27173a824d7475ade679ef2de55e7c91bc3dd9cc917ac16ee37",
}
EXPECTED_LEDGER_SHA256 = (
    "113f412026d6ae9f5907d8ed9075ca85a76bcda2b33c5c3f5288f7d2c578a2c2"
)


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    left = vertices[0]
    for index, right in enumerate(vertices[1:], start=1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted(((min(left, right), max(left, right)),) + tail))


def occurrences() -> tuple[tuple[object, ...], ...]:
    answer = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            residual = tuple(site for site in SITES
                             if site not in (p_site, s_site))
            for matching in perfect_matchings(residual):
                answer.append((p_site, s_site, matching))
    require(len(answer) == len(set(answer)) == N,
            "the occurrence inventory changed")
    return tuple(answer)


def rank(columns: tuple[tuple[Q, ...], ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    rows = [[Q(columns[column][row]) for column in range(len(columns))]
            for row in range(height)]
    answer = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(answer, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[answer], rows[pivot] = rows[pivot], rows[answer]
        value = rows[answer][column]
        rows[answer] = [entry / value for entry in rows[answer]]
        for row in range(height):
            if row == answer or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[answer], strict=True)]
        answer += 1
    return answer


def dot(left, right) -> Q:
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def free_occurrence_trivialization_audit() -> dict[str, object]:
    # A symbolic rank-one calculation can be checked on arbitrary exact
    # centered z and u.  M acts by M u=u-1(z^T u).
    z = tuple(Q(index - Q(N - 1, 2)) for index in range(N))
    require(sum(z, Q(0)) == 0, "the test parameter stopped being centered")
    u = tuple(Q((index % 7) - 3) for index in range(N))
    scalar = dot(z, u)
    transformed = tuple(value - scalar for value in u)
    inverse = tuple(value + dot(z, transformed) for value in transformed)
    require(inverse == u
            and sum(transformed, Q(0))
                == sum(u, Q(0)) - N * dot(z, u),
            "the centered rank-one shear identity changed")

    # Matrix determinant lemma: det(I-1*z^T)=1-z^T*1=1.  The inverse is
    # I+1*z^T because (1*z^T)^2=1*(z^T*1)*z^T=0.
    return {
        "free_occurrence_family": "R_z=R-N*z^T*u on z^T*1=0",
        "trivializing_matrix": "M_z=I-1*z^T",
        "determinant": 1,
        "inverse": "I+1*z^T",
        "permutation_equivariant": True,
        "selected_one_parameter_relation": (
            "z=s(e_f-1/N); R_z=(1+s)R-sNf, formally equivalent to "
            "R-s'Nf with s'=s/(1+s)"
        ),
    }


def exponent(occurrence: tuple[object, ...]) -> tuple[int, ...]:
    p_site, s_site, matching = occurrence
    answer = [0] * (12 + len(EDGES))
    answer[p_site] = 1
    answer[6 + s_site] = 1
    for selected in matching:
        answer[12 + EDGES.index(selected)] = 1
    return tuple(answer)


def first_toric_rectangle_audit() -> dict[str, object]:
    values = occurrences()
    lookup = {value: index for index, value in enumerate(values)}
    x = ((2, 3), (4, 5))
    y = ((2, 4), (3, 5))
    corners = (
        (0, 1, x),  # A*x
        (0, 1, y),  # A*y
        (1, 0, x),  # B*x
        (1, 0, y),  # B*y
    )
    indices = tuple(lookup[corner] for corner in corners)
    exponents = tuple(exponent(corner) for corner in corners)
    require(tuple(left + right for left, right in
                  zip(exponents[1], exponents[2], strict=True))
            == tuple(left + right for left, right in
                     zip(exponents[0], exponents[3], strict=True)),
            "the first toric rectangle stopped being a binomial")

    # F=u_Ay*u_Bx-u_Ax*u_By.  On the all-ones occurrence tangent,
    # dF=Bx+Ay-By-Ax=(B-A)(x-y).
    A, B, x_value, y_value = map(Q, (1, -1, 1, 2))
    corner_values = (A * x_value, A * y_value,
                     B * x_value, B * y_value)
    derivative = (corner_values[2] + corner_values[1]
                  - corner_values[3] - corner_values[0])
    require(corner_values[1] * corner_values[2]
                == corner_values[0] * corner_values[3]
            and derivative == (B - A) * (x_value - y_value) == 2,
            "the toric-shear differential changed")
    return {
        "corner_order": [str(corner) for corner in corners],
        "occurrence_indices": list(indices),
        "toric_binomial": "u_Ay*u_Bx-u_Ax*u_By",
        "physical_factorization": (
            "u_Am=A*x_m, u_Bm=B*x_m; "
            "A=p0*s1, B=p1*s0"
        ),
        "constant_shear_differential": (
            "(B-A)(x-y)=(p1*s0-p0*s1)"
            "*(q23*q45-q24*q35)"
        ),
        "sample_nonzero_value": str(derivative),
    }


def fixed_endpoint_segre_tangent_audit() -> dict[str, object]:
    # The three 2x2-minor differentials on the constant 2x3 tangent are
    # (B-A)(x_j-x_k).  Over a field, all vanish iff A=B or x0=x1=x2.
    tests = []
    for A, B, xs in (
        (Q(1), Q(1), (Q(1), Q(2), Q(4))),
        (Q(1), Q(3), (Q(2), Q(2), Q(2))),
        (Q(1), Q(3), (Q(1), Q(2), Q(4))),
        (Q(0), Q(0), (Q(1), Q(2), Q(4))),
        (Q(1), Q(3), (Q(0), Q(0), Q(0))),
    ):
        derivatives = tuple((B - A) * (xs[left] - xs[right])
                            for left, right in combinations(range(3), 2))
        expected = A == B or len(set(xs)) == 1
        require((not any(derivatives)) == expected,
                ("the fixed-endpoint Segre fork changed", A, B, xs))
        tests.append({
            "A": str(A), "B": str(B),
            "matching_values": list(map(str, xs)),
            "minor_derivatives": list(map(str, derivatives)),
            "constant_shear_tangent": expected,
        })
    return {
        "block": "two endpoint orientations by three residual matchings",
        "minor_differentials": "(B-A)(x_j-x_k), j<k",
        "exact_tangent_iff": "A=B or x0=x1=x2",
        "endpoint_dark_arm": "A=B",
        "matching_dark_arm": "x0=x1=x2",
        "tests": tests,
    }


def response_fibre_jacobian_guard() -> dict[str, object]:
    values = occurrences()
    # Exact sparse response point.  Only p0,p1,s0,s1 are nonzero; every q
    # edge is 1 except q24=2.  The two endpoint orientations cancel in the
    # complete response, while the selected occurrence remains 1.
    p = tuple(map(Q, (1, 1, 0, 0, 0, 0)))
    s = tuple(map(Q, (-1, 1, 0, 0, 0, 0)))
    q = {edge: Q(2 if edge == (2, 4) else 1) for edge in EDGES}

    def occurrence_value(item):
        p_site, s_site, matching = item
        return p[p_site] * s[s_site] * q[matching[0]] * q[matching[1]]

    response = sum((occurrence_value(item) for item in values), Q(0))
    marked = (0, 1, ((2, 3), (4, 5)))
    marked_value = occurrence_value(marked)
    require(response == 0 and marked_value == 1,
            "the exact response-fibre guard changed")

    columns = []
    for kind in ("p", "s"):
        for variable in SITES:
            column = []
            for p_site, s_site, matching in values:
                q_product = q[matching[0]] * q[matching[1]]
                if kind == "p":
                    column.append(Q(p_site == variable) * s[s_site]
                                  * q_product)
                else:
                    column.append(p[p_site] * Q(s_site == variable)
                                  * q_product)
            columns.append(tuple(column))
    for edge in EDGES:
        column = []
        for p_site, s_site, matching in values:
            if edge not in matching:
                column.append(Q(0))
                continue
            other = matching[1] if matching[0] == edge else matching[0]
            column.append(p[p_site] * s[s_site] * q[other])
        columns.append(tuple(column))

    constant_shear = (Q(1),) * N
    jacobian_rank = rank(tuple(columns))
    augmented_rank = rank(tuple(columns) + (constant_shear,))
    require((jacobian_rank, augmented_rank) == (12, 13),
            "the response-fibre shear rank guard changed")
    return {
        "response_value": str(response),
        "marked_occurrence_value": str(marked_value),
        "physical_variable_count": len(columns),
        "monomial_map_jacobian_rank": jacobian_rank,
        "rank_after_constant_occurrence_shear": augmented_rank,
        "constant_shear_lifts_to_p_s_q_tangent": False,
        "scope": (
            "exact point of the selected complete response hypersurface, "
            "not asserted to satisfy every GHZ source equation"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))
    ledger = {
        "theorem": "universal occurrence shear / physical toric lift gate",
        "pins": PINS,
        "free_occurrence_trivialization": free_occurrence_trivialization_audit(),
        "first_toric_rectangle": first_toric_rectangle_audit(),
        "fixed_endpoint_Segre_tangent": fixed_endpoint_segre_tangent_audit(),
        "response_fibre_Jacobian_guard": response_fibre_jacobian_guard(),
        "verdict": (
            "The universal centered occurrence deformation is canonically "
            "trivial on the free ninety-coordinate presentation, but that "
            "rank-one shear does not generally lift through the physical "
            "p,s,q monomial map.  Its first obstruction is the mixed "
            "endpoint-by-matching toric conormal.  On a fixed endpoint pair "
            "the shear is tangent exactly in the endpoint-dark arm A=B or "
            "the matching-dark arm x0=x1=x2."
        ),
        "shortest_positive_theorem": (
            "Construct a physical PP/Hasse lift of the centered shear which "
            "carries every toric-minor differential as a proper face, or "
            "route a first nonzero mixed endpoint-by-matching conormal into "
            "the already typed determinant/fan/terminal alternatives."
        ),
        "scope": (
            "Exact h=3 occurrence presentation over characteristic zero. "
            "The free-family trivialization, toric relation, Segre tangent "
            "fork, and response-hypersurface rank guard are unconditional. "
            "No full-GHZ source point, physical terminal promotion, or "
            "AugP2/E14 word-grade lift is claimed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("free occurrence shear: ALGEBRAICALLY TRIVIAL")
    print("physical p,s,q lift: BLOCKED BY TORIC 2x2 MINOR")
    print("fixed-endpoint tangent iff: A=B OR x0=x1=x2")
    print("exact response-fibre Jacobian ranks: 12 -> 13")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

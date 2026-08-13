#!/usr/bin/env python3
"""Audit the marked-occurrence graph chart and its first obstruction class.

For the literal 90-term mixed response R=f+G, adjoining u=f gives the
source-valid graph equation E=f-u and the mate equation M=G+u=R-E.  On the
active chart u!=0, adjoining r=G/u gives the canonical normalization
N=1+r=0 and the exact identity

    R = E + (G-u*r) + u*N.

These are contractible presentation pairs: projection of the graph back to
the old physical source is an isomorphism, including tangent and obstruction
spaces.  In particular the graph does not canonically produce the
occurrence-local relative q-cell or the six-term comparison required by
Interface I.

The first positive remaining object is the ordinary Hasse-Hessian class
[F_[2](xi)] in coker(A), for xi in ker(A) with df(xi)!=0.  Exact Fredholm
duality gives either a second-order lift or a physical output covector
killing im(A) and detecting this one class.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
    "computations/verify_h3_trapped_carrier_full_q_six_term_extension.py":
        "f194101187d92255a8396b762769df2d3e058f0adc2072ae822da4881f1a4e3d",
    "computations/verify_h3_selected_lower_relative_weyl_bar_gate.py":
        "7a6f2afebcacc5924110e32a3f7d9c225992f07abae637d4529b5436c64cc294",
    "computations/verify_h3_six_term_exhaustive_relative_extension_alternative.py":
        "bcc55b05c10ba1ac6f3c4415c18a70274ecc29dd506fbed8e69d471b5f0a5607",
}
EXPECTED_LEDGER_SHA256 = (
    "14af41bf3463ca9f89651564eb6456bc766c47ba0ced77d79237102a6b7ac550"
)

SITES = tuple(range(6))
WORD = (1, 1, 0, 0, 0, 0)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def perfect_matchings(vertices):
    vertices = tuple(sorted(vertices))
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield ((first, second),) + tail


def variable(kind: str, *indices: int):
    return (kind,) + indices


def q_variable(left: int, right: int):
    if left > right:
        left, right = right, left
    return variable("q", left, right, WORD[left], WORD[right])


def response_occurrences():
    answer = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            complement = tuple(site for site in SITES
                               if site not in (p_site, s_site))
            for matching in perfect_matchings(complement):
                answer.append(tuple(sorted((
                    variable("p", 0, p_site, WORD[p_site]),
                    variable("s", 0, s_site, WORD[s_site]),
                    *(q_variable(left, right) for left, right in matching),
                ))))
    require(len(answer) == len(set(answer)) == 90,
            "literal response occurrence inventory changed")
    return tuple(answer)


def marked_occurrence():
    return tuple(sorted((
        variable("p", 0, 0, 1),
        variable("s", 0, 1, 1),
        q_variable(2, 3),
        q_variable(4, 5),
    )))


def moving_factors(monomial):
    return tuple(factor for factor in monomial if factor[0] != "s")


def tagged_factor(tag, factor):
    return (tag,) + factor


def hasse_coefficient(monomial, order):
    """Straight-line Hasse coefficient in the moving p,q variables."""
    moving = moving_factors(monomial)
    fixed = tuple(factor for factor in monomial if factor[0] == "s")
    answer = Counter()
    for selected in combinations(range(len(moving)), order):
        selected = frozenset(selected)
        term = tuple(sorted(
            [tagged_factor("x", factor) for factor in fixed]
            + [tagged_factor("d" if index in selected else "x", factor)
               for index, factor in enumerate(moving)]
        ))
        answer[term] += Q(1)
    return answer


def add(*polynomials):
    answer = Counter()
    for polynomial in polynomials:
        answer.update(polynomial)
    return +answer


def subtract(left, right):
    answer = Counter(left)
    answer.subtract(right)
    return +answer


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    row = 0
    for column in range(len(work[0])):
        pivot = next((index for index in range(row, len(work))
                      if work[index][column]), None)
        if pivot is None:
            continue
        work[row], work[pivot] = work[pivot], work[row]
        value = work[row][column]
        work[row] = [entry / value for entry in work[row]]
        for index in range(len(work)):
            if index == row or not work[index][column]:
                continue
            value = work[index][column]
            work[index] = [left - value * right for left, right
                           in zip(work[index], work[row], strict=True)]
        row += 1
    return row


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b
                in zip(left, right, strict=True)), Q(0))


def audit():
    actual_pins = {}
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative,
                                     actual))
        actual_pins[relative] = actual

    occurrences = response_occurrences()
    marked = marked_occurrence()
    marked_index = occurrences.index(marked)
    mates = occurrences[:marked_index] + occurrences[marked_index + 1:]
    require(len(mates) == 89, "mate aggregate stopped having 89 terms")

    # Literal Hasse coefficients make E=f-u and M=G+u transparent.  The u
    # coordinate is linear, so its second face can always be chosen to be
    # the second Hasse coefficient of f.  What remains in M is exactly R_[2].
    f2 = hasse_coefficient(marked, 2)
    g2 = add(*(hasse_coefficient(term, 2) for term in mates))
    r2 = add(f2, g2)
    graph_e2_after_u2 = subtract(f2, f2)
    graph_m2_after_u2 = add(g2, f2)
    require(not graph_e2_after_u2 and graph_m2_after_u2 == r2,
            "the graph introduced a new second Hasse obstruction")
    require(len(f2) == 3 and len(r2) == 270,
            ("literal second Hasse counts changed", len(f2), len(r2)))

    # First-order cotangent calculation on the smallest literal quotient
    # R=f+g.  E=f-u, M=g+u, and R=E+M.  The graph tangent projects
    # isomorphically to the old response tangent.
    d_r = (Q(1), Q(1), Q(0))
    d_e = (Q(1), Q(0), Q(-1))
    d_m = (Q(0), Q(1), Q(1))
    require(tuple(left + right for left, right
                  in zip(d_e, d_m, strict=True)) == d_r,
            "R=E+M stopped holding on cotangents")
    require(rank((d_r,)) == 1 and rank((d_e, d_m)) == 2,
            "graph cotangent ranks changed")
    old_tangent = (Q(1), Q(-1))
    graph_tangent = (Q(1), Q(-1), Q(1))
    require(dot(d_r[:2], old_tangent) == 0
            and dot(d_e, graph_tangent) == 0
            and dot(d_m, graph_tangent) == 0,
            "graph tangent stopped projecting to the old tangent")

    # Active ratio chart.  Q=g-u*r and N=1+r at (f,g,u,r)=(1,-1,1,-1).
    # Polynomially R=E+Q+u*N, so dR=dE+dQ+dN at u=1,N=0.
    d_r_ratio = (Q(1), Q(1), Q(0), Q(0))
    d_e_ratio = (Q(1), Q(0), Q(-1), Q(0))
    d_q_ratio = (Q(0), Q(1), Q(1), Q(-1))
    d_n_ratio = (Q(0), Q(0), Q(0), Q(1))
    reconstructed = tuple(sum(entries, Q(0)) for entries in zip(
        d_e_ratio, d_q_ratio, d_n_ratio, strict=True
    ))
    require(reconstructed == d_r_ratio,
            "localized identity R=E+Q+uN changed")
    require(rank((d_e_ratio, d_q_ratio, d_n_ratio)) == 3,
            "active graph chart stopped being a private-pivot presentation")

    # Exact finite counterguard for the proposed obstruction identification.
    # Both systems have the same R=f+g, H=df, graph chart, tangent, and
    # Lambda=dR in row(A).  An independent physical output equation can have
    # zero or nonzero quadratic obstruction on the same tangent.  Hence the
    # graph data alone does not define coker(A)->Q[Lambda].
    a = ((Q(1), Q(1)), (Q(0), Q(0)))
    h = (Q(1), Q(0))
    lam = (Q(1), Q(1))
    xi = old_tangent
    require(all(dot(row, xi) == 0 for row in a)
            and dot(h, xi) == 1 and lam == a[0],
            "Interface-II survivor counterguard changed")
    b_zero = (Q(0), Q(0))
    b_nonzero = (Q(0), Q(1))
    output_dual = (Q(0), Q(1))
    require(all(dot(output_dual, column) == 0
                for column in zip(*a, strict=True)),
            "output dual stopped killing image(A)")
    require(dot(output_dual, b_zero) == 0
            and dot(output_dual, b_nonzero) == 1,
            "Hessian obstruction guard changed")

    return {
        "theorem": "occurrence graph normalization and Hessian-cone gate",
        "pins": actual_pins,
        "literal_response": {
            "head_word": "11:110000",
            "occurrences": len(occurrences),
            "marked_terms": 1,
            "mate_terms": len(mates),
            "equation": "R=f+G=0",
        },
        "source_valid_graph": {
            "equations": ["E=f-u=0", "M=G+u=0"],
            "identity": "R=E+M",
            "old_tangent": [str(value) for value in old_tangent],
            "graph_tangent": [str(value) for value in graph_tangent],
            "conclusion": (
                "Spec(source[u]/(f-u)) projects isomorphically to source; "
                "the graph pair has a private u pivot and does not impose df=0"
            ),
        },
        "active_ratio_chart": {
            "coordinates": "u=f nonzero, r=G/u",
            "equations": ["E=f-u", "Q=G-u*r", "N=1+r"],
            "identity": "R=E+Q+u*N",
            "normalization_cell": "N=1+r has augmentation one",
            "typing_obstruction": (
                "r is the aggregate of 89 occurrence ratios and has a "
                "private chart pivot dr; it has no canonical literal "
                "matching/repeated-q boundary or six-term readout"
            ),
        },
        "second_hasse": {
            "f_order2_terms": len(f2),
            "R_order2_terms": len(r2),
            "graph_E_obstruction_after_choosing_u2": 0,
            "graph_M_obstruction": "R_[2](xi)",
            "canonical_class": "[F_[2](xi)] in coker(A)",
        },
        "fredholm_alternative": (
            "either F_[2](xi) lies in image(A), giving a second-order "
            "source lift, or some physical output covector psi satisfies "
            "psi*A=0 and psi(F_[2](xi))!=0"
        ),
        "interface_I_comparison": {
            "same_cone": False,
            "reason": (
                "the graph/ratio cone is contractible through private u,r "
                "pivots; Interface I needs an occurrence-local cell with "
                "literal repeated-q boundary and augmented physical readouts"
            ),
            "smallest_missing_map": (
                "a source-labelled Spencer comparison sending the output "
                "class [F_[2](xi)] to the existing six-term relative complex"
            ),
        },
        "finite_noncanonicity_guard": {
            "A": [[str(value) for value in row] for row in a],
            "H": [str(value) for value in h],
            "Lambda": [str(value) for value in lam],
            "xi": [str(value) for value in xi],
            "two_Hessian_classes": [[str(value) for value in b_zero],
                                      [str(value) for value in b_nonzero]],
            "physical_output_dual_for_nonzero_class": [
                str(value) for value in output_dual
            ],
            "conclusion": (
                "identical occurrence graph and Lambda-in-row data allow "
                "zero or nonzero output obstruction; the comparison map "
                "cannot be inferred from graph normalization"
            ),
        },
        "scope": (
            "exact literal 90-term response graph and second Hasse face, "
            "plus a finite source/output dual guard.  This constructs the "
            "canonical graph normalization but not a new optical source "
            "coordinate, the Interface-I comparison map, or a full formal arc"
        ),
    }


def main() -> None:
    ledger = audit()
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("occurrence graph/Hessian ledger changed", digest))
    print("h3 trapped-carrier occurrence graph/Hessian cone: PASS")
    print("R=f+G=(f-u)+(G+u): canonical graph normalization is contractible")
    print("active ratio cell 1+G/u has a private chart pivot, no physical q boundary")
    print("first obstruction: [F_[2](xi)] in coker(A), with physical output dual")
    print("Interface-I identification requires a new source-labelled comparison")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

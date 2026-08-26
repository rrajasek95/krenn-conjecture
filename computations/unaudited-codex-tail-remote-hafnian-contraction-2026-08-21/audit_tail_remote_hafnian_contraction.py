#!/usr/bin/env python3
"""Exact Hafnian contraction audit for the D611-open remote tail chart."""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import argparse
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = HERE / "results_tail_remote_hafnian_contraction.json"
TAIL_RESULT = (HERE.parent /
    "unaudited-codex-tail-polar-source-lift-2026-08-21" /
    "results_tail_polar_source_lift.json")
V = tuple(range(8))
EDGES = tuple(combinations(V, 2))
SELECTED = tuple((a, tail) for tail in (6, 7) for a in range(6))
SELECTED_SET = frozenset(SELECTED)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


@lru_cache(None)
def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def edge(u, v):
    return tuple(sorted((u, v)))


def variable_label(u, v, i, j):
    if u < v:
        return f"a_{u}{v}_{i}{j}"
    return f"a_{v}{u}_{j}{i}"


def hafnian_terms(vertices):
    return perfect_matchings(tuple(sorted(vertices)))


def source_amplitude(word, cell_value):
    value = sp.Integer(0)
    for matching in perfect_matchings(V):
        term = sp.Integer(1)
        for u, v in matching:
            term *= cell_value(u, v, word[u], word[v])
        value += term
    return sp.cancel(value)


def normalized_zero(expr, lam):
    """Test zero on 105*lam^4=1, allowing Laurent powers of lam."""
    expr = sp.cancel(expr)
    numerator, _ = sp.fraction(expr)
    polynomial = sp.Poly(sp.expand(numerator * lam**8), lam)
    modulus = sp.Poly(105 * lam**4 - 1, lam)
    return polynomial.rem(modulus).is_zero


def normalized_remainder(expr, lam):
    expr = sp.cancel(expr)
    numerator, denominator = sp.fraction(expr)
    polynomial = sp.Poly(sp.expand(numerator * lam**8), lam)
    modulus = sp.Poly(105 * lam**4 - 1, lam)
    remainder = polynomial.rem(modulus).as_expr()
    return str(sp.factor(remainder / (lam**8 * denominator)))


def logical_hash(payload):
    return sha256(json.dumps(payload, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def main(write_results=False):
    global sp
    try:
        import sympy as sp
    except ImportError:
        sites = sorted((ROOT / ".venv/lib").glob("python*/site-packages"))
        require(bool(sites), "sympy unavailable")
        sys.path.append(str(sites[-1]))
        import sympy as sp
    matchings8 = perfect_matchings(V)
    require(len(matchings8) == 105, "K8 matching count changed")

    # Termwise Euler audits.  A monomial of H has four g-edges.  The first
    # polar has one x-edge and three g-edges; the ordered second polar has
    # one x-edge, one y-edge, and two g-edges.
    h_terms = matchings8
    first_polar_terms = []
    for e in EDGES:
        residual = tuple(v for v in V if v not in e)
        for matching in perfect_matchings(residual):
            first_polar_terms.append((e, matching))
    second_polar_terms = []
    for e in EDGES:
        residual_e = tuple(v for v in V if v not in e)
        for f in combinations(residual_e, 2):
            residual = tuple(v for v in residual_e if v not in f)
            for matching in perfect_matchings(residual):
                second_polar_terms.append((e, edge(*f), matching))
    require(len(h_terms) == 105 and len(first_polar_terms) == 420 and
            len(second_polar_terms) == 1260,
            "Hafnian polar term census changed")
    require(all(len(matching) == 4 for matching in h_terms),
            "pure Euler degree changed")
    require(all(len(matching) == 3 for _, matching in first_polar_terms),
            "first-polar g-degree changed")
    require(all(len(matching) == 2 for _, _, matching in second_polar_terms),
            "second-polar g-degree changed")

    selected_incidence = Counter(
        sum(e in SELECTED_SET for e in matching) for matching in matchings8
    )
    require(selected_incidence == Counter({2: 90, 0: 15}),
            "selected-edge Euler boundary census changed")

    # Literal twelve 611 equations and dependency audit.
    rows_611 = []
    q_dependency_union = set()
    for a, tail in SELECTED:
        word = [2] * 8
        word[a] = 0
        word[tail] = 1
        word = tuple(word)
        linear = []
        quadratic = []
        for matching in matchings8:
            cross = [(u, v) for u, v in matching if word[u] != word[v]]
            term_labels = tuple(sorted(
                variable_label(u, v, word[u], word[v]) for u, v in matching
            ))
            if len(cross) == 1:
                linear.append((matching, term_labels))
            else:
                require(len(cross) == 2, "611 term degree is not one or two")
                quadratic.append((matching, term_labels, tuple(
                    variable_label(u, v, word[u], word[v]) for u, v in cross
                )))
        require(len(linear) == 15 and len(quadratic) == 90,
                "literal 611 split changed")
        selected_variable = variable_label(a, tail, 0, 1)
        require(all(selected_variable in labels for _, labels in linear),
                "611 linear terms lost selected variable")
        quadratic_cross_variables = {
            variable for _, _, variables in quadratic for variable in variables
        }
        require(all(not variable.endswith("_01")
                    for variable in quadratic_cross_variables),
                "611 quadratic side unexpectedly uses the selected 01 channel")
        q_dependency_union.update(quadratic_cross_variables)
        rows_611.append({
            "source_label": "F_" + "".join(map(str, word)),
            "selected_variable": selected_variable,
            "cofactor": f"h2_{a}{tail}",
            "linear_terms": len(linear),
            "quadratic_terms": len(quadratic),
            "quadratic_cross_channels": ["02", "12"],
            "quadratic_cross_variable_count": len(quadratic_cross_variables),
        })
    selected_variables = {variable_label(a, tail, 0, 1)
                          for a, tail in SELECTED}
    require(not (selected_variables & q_dependency_union),
            "quadratic RHS intersects selected variables")

    # Canonical 332 remainder: after the three selected 01 tail cells are
    # eliminated by their 611 equations, six literal degree-one boundary
    # cells remain.  Thus 332 does not contract to a scalar in T_selected.
    canonical_332 = tuple(map(int, "00011212"))
    degree_one_terms = []
    for matching in matchings8:
        cross = [(u, v) for u, v in matching
                 if canonical_332[u] != canonical_332[v]]
        if len(cross) != 1:
            continue
        u, v = cross[0]
        cross_label = variable_label(
            u, v, canonical_332[u], canonical_332[v])
        diagonal = [
            f"g{canonical_332[x]}_{x}{y}" for x, y in matching
            if canonical_332[x] == canonical_332[y]
        ]
        degree_one_terms.append({
            "cross_variable": cross_label,
            "diagonal_coefficient": "*".join(sorted(diagonal)),
            "selected": cross_label in selected_variables,
            "matching": [list(e) for e in matching],
        })
    require(len(degree_one_terms) == 9 and
            Counter(term["selected"] for term in degree_one_terms)
            == Counter({False: 6, True: 3}),
            "canonical 332 selected/boundary split changed")
    boundary_variables = sorted(term["cross_variable"]
                                for term in degree_one_terms
                                if not term["selected"])
    require(boundary_variables == [
        "a_03_01", "a_04_01", "a_13_01",
        "a_14_01", "a_23_01", "a_24_01",
    ], "canonical 332 boundary variables changed")

    # Exact D611-open point over Q(lambda), subsequently restricted by
    # 105*lambda^4=1.  It satisfies pure H=1, the twelve 611 equations, and
    # the eight selected 71 rows, while remaining nonzero.  It deliberately
    # need not satisfy 332; the failures show where those rows first add new
    # information.
    lam = sp.Symbol("lambda", nonzero=True)
    s = -sp.Rational(1, 5) / lam
    exceptional_cells = {
        (0, 1, 0, 2): sp.Integer(1),
        (6, 7, 1, 2): sp.Integer(1),
        (0, 6, 0, 1): s,
        (0, 1, 0, 1): -s,
        (6, 7, 1, 0): -s,
    }

    def point_cell(u, v, i, j):
        if u > v:
            u, v, i, j = v, u, j, i
        if i == j:
            return lam
        return exceptional_cells.get((u, v, i, j), sp.Integer(0))

    tail = json.loads(TAIL_RESULT.read_text())
    ledger_by_profile = {}
    for record in tail["row_ledger"]:
        ledger_by_profile.setdefault(record["profile"], []).append(
            record["source_label"])
    require(Counter(map(len, ledger_by_profile.values())) ==
            Counter({8: 1, 12: 1, 360: 1}),
            "tail row profile ledger changed")

    pure_values = {
        f"F_{colour * 8}": source_amplitude((int(colour),) * 8, point_cell)
        for colour in "012"
    }
    require(all(value == 105 * lam**4 for value in pure_values.values()),
            "pure point values changed")

    row_values = {}
    for profile in ("6+1+1", "7+1", "3+3+2"):
        for label in ledger_by_profile[profile]:
            word = tuple(map(int, label[2:]))
            row_values[label] = source_amplitude(word, point_cell)
    require(all(row_values[label] == 0
                for label in ledger_by_profile["6+1+1"]),
            "counterexample stopped satisfying twelve 611 rows")
    require(all(row_values[label] == 0
                for label in ledger_by_profile["7+1"]),
            "counterexample stopped satisfying eight 71 rows")

    nonzero_332 = [
        label for label in ledger_by_profile["3+3+2"]
        if not normalized_zero(row_values[label], lam)
    ]
    zero_332 = [label for label in ledger_by_profile["3+3+2"]
                if normalized_zero(row_values[label], lam)]
    require(nonzero_332, "332 rows ceased to detect the remote point")
    canonical_value = row_values["F_00011212"]
    require(not normalized_zero(canonical_value, lam),
            "canonical 332 detector vanished after pure normalization")

    # The Q_06 dependency counterexample stays inside D611 and pure H=1.
    # With all diagonal cells lambda, h2_06=15*lambda^3 and the two external
    # cells a_01_02=a_67_12=1 give Q_06=3*lambda^2.  Hence y0=-1/(5lambda).
    require(s * (15 * lam**3) + 3 * lam**2 == 0,
            "canonical fixed-coordinate identity changed")

    result = {
        "status": "PASS exact D611 Hafnian contraction obstruction audit",
        "hafnian_euler_polar_identities": {
            "pure": "sum_e g_e*h_e = 4*H",
            "first_polar": (
                "P1(X;g)=sum_e X_e*h_e; "
                "sum_g g*d_g P1=3*P1 and sum_X X*d_X P1=P1"
            ),
            "ordered_second_polar": (
                "P2(X,Y;g)=sum_(e disjoint f) X_e*Y_f*h_ef; "
                "sum_g g*d_g P2=2*P2, sum_X X*d_X P2=P2, "
                "sum_Y Y*d_Y P2=P2"
            ),
            "term_census": {
                "H": len(h_terms), "P1": len(first_polar_terms),
                "P2_ordered": len(second_polar_terms),
            },
            "six_site_cofactor_euler": (
                "for every edge e, sum_(f disjoint e) g_f*h_ef=3*h_e"
            ),
        },
        "D611_partial_fixed_coordinate_system": {
            "selected_edges": [f"{u}{v}" for u, v in SELECTED],
            "selected_variables": sorted(selected_variables),
            "rows": rows_611,
            "literal_formula": (
                "h2_uv*T01_uv + sum_(b,c distinct off u,v) "
                "A_ub[0,2]*A_vc[1,2]*Haf4(G2 without u,v,b,c)=0"
            ),
            "localized_solution": "T01_uv=-Q_uv/h2_uv for the twelve selected uv",
            "quadratic_dependency_channels": ["02", "12"],
            "quadratic_dependency_variable_count": len(q_dependency_union),
            "is_closed_self_map_on_12_variables": False,
            "scope_verdict": (
                "D611 inversion gives twelve coordinate functions of 156 "
                "unselected cross-colour cells.  Calling this T=B(T,T) is "
                "valid only if T denotes the full 168-cell ambient vector, "
                "in which case twelve equations do not define a fixed-point map."
            ),
        },
        "truncated_Euler_boundary": {
            "selected_matching_incidence_histogram": {
                str(k): v for k, v in sorted(selected_incidence.items())
            },
            "identity": (
                "sum_(e in E*) g_e*h_e = 4H - "
                "sum_(e notin E*) g_e*h_e, E*={a6,a7:0<=a<6}"
            ),
            "non_scalar_guard": (
                "The left side has coefficient 0 on the 15 matchings using "
                "edge 67 and coefficient 2 on the other 90 matchings, so it "
                "is not c*H for any scalar c."
            ),
        },
        "exact_boundary_valued_71_contraction": {
            "identity": (
                "For residual a and colours i,j,k, the literal 71 row is "
                "sum_v A_av[i,j]*h^j_av=0. After D611 substitution in the "
                "two tail terms: sum_(t=6,7) (h^j_at/h^k_at)*Q^k_at = "
                "sum_(b<6,b!=a) h^j_ab*A_ab[i,j]."
            ),
            "verdict": (
                "This is a six-vector boundary identity, not a zero scalar "
                "invariant; its right side contains residual cross cells."
            ),
        },
        "canonical_332_remainder": {
            "source_label": "F_00011212",
            "degree_one_terms": degree_one_terms,
            "selected_linear_terms_eliminated": 3,
            "surviving_boundary_linear_terms": 6,
            "surviving_boundary_variables": boundary_variables,
            "conclusion": (
                "Even after subtracting the three audited 611 multiples, "
                "the 332 row has six independent degree-one boundary terms. "
                "Thus the 360 rows do not collapse source-symbolically to an "
                "invariant in the twelve selected coordinates."
            ),
        },
        "exact_nonzero_partial_remote_point": {
            "field": "Q(lambda)/(105*lambda^4-1)",
            "diagonal_cells": "A_uv[c,c]=lambda for every edge and colour",
            "nonzero_cross_cells": {
                variable_label(u, v, i, j): str(value)
                for (u, v, i, j), value in exceptional_cells.items()
            },
            "pure_values_before_normalization": {
                label: str(value) for label, value in pure_values.items()
            },
            "pure_H_equals_1_after_relation": True,
            "D611_factors": "all h2_at=15*lambda^3, hence nonzero",
            "twelve_611_rows_zero": True,
            "eight_selected_71_rows_zero": True,
            "selected_tail_nonzero": "a_06_01=-1/(5*lambda)",
            "332_zero_count": len(zero_332),
            "332_nonzero_count": len(nonzero_332),
            "first_nonzero_332_labels": nonzero_332[:20],
            "canonical_332_value": str(canonical_value),
            "canonical_332_normalized_remainder": normalized_remainder(
                canonical_value, lam),
            "meaning": (
                "Pure H=1 plus D611 plus the 611/71 equations admits a "
                "nonzero partial remote point.  The 332 packet detects it, "
                "so any closure must use its full boundary-valued equations, "
                "not a scalar Euler contraction."
            ),
        },
        "remaining_exact_target": (
            "Substitute T01_at=-Q^2_at/h2_at into the 360 literal 332 rows "
            "and the eight 71 rows, clear only products of the audited h2_at, "
            "and work in the 156 unselected cross-cell variables.  No frozen "
            "Euler identity reduces this boundary system to support6 or cap activity."
        ),
        "scope_guard": (
            "The point is a counterexample to a contraction from pure+611+71, "
            "not to X5: it intentionally fails displayed 332 rows.  No claim "
            "is made that the 332 packet has a remote solution."
        ),
    }
    result["logical_sha256"] = logical_hash(result)
    if write_results:
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result["status"],
        "closed_self_map": False,
        "332_zero": len(zero_332),
        "332_nonzero": len(nonzero_332),
        "canonical_332": str(canonical_value),
        "logical_sha256": result["logical_sha256"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    args = parser.parse_args()
    main(args.write_results)

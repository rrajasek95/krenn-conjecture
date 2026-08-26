#!/usr/bin/env python3
"""Exact structural reverse interface for the k5 face 0:31:30.

This rebuilds the literal normalized source chart from the frozen recursive
face machinery, profiles every surviving raw row, and searches only
fraction-free eliminations of a variable occurring linearly in a short row
against one literal cofactor row.  It performs no ideal or emptiness solve.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
COMP = HERE.parent
BUILDER_PATH = (COMP /
    "unaudited-codex-branch0-offdiag-support-strata-2026-08-21" /
    "build_recursive_face_charts.py")
ROUTING_PATH = (COMP /
    "unaudited-codex-k56-boundary-routing-2026-08-21" /
    "results_k56_recursive_boundary_routing.json")
OUT_PREFIX = HERE / "results_face03130_reverse_interface"
STATE = (0, 31, 30)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_sha(path):
    return sha256(path.read_bytes()).hexdigest()


def logical_sha(payload):
    body = dict(payload)
    body.pop("logical_sha256", None)
    return sha256(json.dumps(body, sort_keys=True,
                             separators=(",", ":")).encode()).hexdigest()


def primitive_monomial_split(poly, variables, sp):
    """Return content, monomial gcd, and primitive remainder exactly."""
    value = sp.Poly(poly, *variables, domain=sp.QQ)
    require(not value.is_zero, "cannot split the zero polynomial")
    terms = value.terms()
    monomial = tuple(min(exponent[i] for exponent, _ in terms)
                     for i in range(len(variables)))
    monomial_expr = sp.prod(var ** exponent
                            for var, exponent in zip(variables, monomial))
    coefficients = [coefficient for _, coefficient in terms]
    denominator_lcm = sp.ilcm(*[int(c.q) for c in coefficients])
    integer_coefficients = [int(c * denominator_lcm)
                            for c in coefficients]
    numerator_gcd = abs(sp.igcd(*integer_coefficients))
    content = Fraction(numerator_gcd, denominator_lcm)
    if value.LC() < 0:
        content = -content
    content_q = sp.Rational(content.numerator, content.denominator)
    primitive = sp.Add(*(
        (coefficient / content_q) * sp.prod(
            variable ** (exponent[i] - monomial[i])
            for i, variable in enumerate(variables))
        for exponent, coefficient in terms))
    primitive = sp.Poly(primitive, *variables, domain=sp.QQ).as_expr()
    return content, monomial, primitive


def encode_poly(poly, variables, sp):
    value = sp.Poly(poly, *variables, domain=sp.QQ)
    return [{"exponents": list(exponent),
             "coefficient": [int(coefficient.p), int(coefficient.q)]}
            for exponent, coefficient in value.terms()]


def poly_profile(poly, variables, sp):
    value = sp.Poly(poly, *variables, domain=sp.QQ)
    return {
        "term_count": len(value.terms()),
        "total_degree": value.total_degree(),
        "variable_degrees": {
            str(variable): value.degree(variable)
            for variable in variables if value.degree(variable) > 0
        },
        "linear_variables": [str(variable) for variable in variables
                             if value.degree(variable) == 1],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("standard", "mutation"),
                        default="standard")
    args = parser.parse_args()

    try:
        import sympy as sp
    except ImportError:
        candidate = HERE.parents[1] / ".venv" / "lib"
        sites = sorted(candidate.glob("python*/site-packages"))
        require(bool(sites), "sympy unavailable and venv site-packages absent")
        sys.path.append(str(sites[-1]))
        import sympy as sp

    BUILD = load("face03130_literal_builder", BUILDER_PATH)
    routing = json.loads(ROUTING_PATH.read_text())
    first = routing["starts"]["k5"]["first_boundary_targets"]
    require("0:31:30" in first, "0:31:30 left the frozen first boundary")
    routed = next(row for row in routing["starts"]["k5"]["records"]
                  if row["key"] == "0:31:30")
    require(routed["selected_term_mask"] == 31 and
            routed["both_live_edge_mask"] == 30 and
            routed["support_shape"] == "four_cycle",
            "frozen routing meaning for 0:31:30 changed")

    record = BUILD.build_state(STATE)
    require(record["key"] == "0:31:30" and
            record["selected_offdiagonal_edges"] == [0, 1, 2, 3, 4] and
            record["selected_diagonal_edges"] == [5] and
            record["both_live_edges"] == [1, 2, 3, 4],
            "literal chart masks changed")
    require(record["gauge_b_edges"] == [0, 1, 2] and
            record["gauge_d_edge"] == 1,
            "lossless canonical gauge changed")
    require(record["nonzero_gauged_source_row_count"] == 16,
            "surviving literal row count changed")

    names = record["variable_names"]
    all_variables = sp.symbols(" ".join(names))
    variable_by_name = dict(zip(names, all_variables))
    gauged_names = {f"b{edge}" for edge in record["gauge_b_edges"]}
    gauged_names.add(f"d{record['gauge_d_edge']}")

    def decode(terms):
        answer = sp.Integer(0)
        for term in terms:
            coefficient = sp.Rational(*term["coefficient"])
            monomial = sp.prod(variable ** exponent for variable, exponent
                               in zip(all_variables, term["exponents"]))
            answer += coefficient * monomial
        return sp.expand(answer)

    decoded = []
    for row in record["rows"]:
        poly = decode(row["terms"])
        decoded.append((row, poly))
    active_names = sorted({str(symbol) for _, poly in decoded
                           for symbol in poly.free_symbols})
    require(not (gauged_names & set(active_names)),
            "a gauged variable survived a literal row")
    variables = tuple(variable_by_name[name] for name in active_names)
    require(len(variables) == 12,
            f"expected twelve normalized variables, got {active_names}")

    profiles = []
    for row, poly in decoded:
        profile = poly_profile(poly, variables, sp)
        profiles.append({"raw_index": row["raw_index"],
                         "label": row["label"], **profile,
                         "polynomial": str(poly),
                         "terms": encode_poly(poly, variables, sp)})

    shortest = min(profiles, key=lambda item:
                   (item["term_count"], item["total_degree"],
                    item["raw_index"]))
    require(shortest["linear_variables"],
            "shortest literal row has no linear variable")

    # Search every short-row/cofactor pair with a common linear variable.
    # Ranking first minimizes the resulting primitive numerator, then the
    # input packet.  No division is made: A*g-C*f is the stored identity.
    candidates = []
    profile_by_index = {row["raw_index"]: row for row in profiles}
    poly_by_index = {row["raw_index"]: poly for row, poly in decoded}
    pivot_pool = sorted(profiles, key=lambda item:
                        (item["term_count"], item["total_degree"],
                         item["raw_index"]))[:8]
    cofactors = [row for row in profiles if row["raw_index"] >= 10]
    for pivot in pivot_pool:
        f = poly_by_index[pivot["raw_index"]]
        for cofactor in cofactors:
            if cofactor["raw_index"] == pivot["raw_index"]:
                continue
            g = poly_by_index[cofactor["raw_index"]]
            common = sorted(set(pivot["linear_variables"]) &
                            set(cofactor["linear_variables"]))
            for name in common:
                x = variable_by_name[name]
                pf = sp.Poly(f, x)
                pg = sp.Poly(g, x)
                require(pf.degree() == pg.degree() == 1,
                        "linear-variable profile mismatch")
                A, B = pf.nth(1), pf.nth(0)
                C, D = pg.nth(1), pg.nth(0)
                resultant = sp.expand(A * D - C * B)
                if not resultant:
                    continue
                content, monomial, primitive = primitive_monomial_split(
                    resultant, variables, sp)
                primitive_profile = poly_profile(primitive, variables, sp)
                candidates.append({
                    "pivot_raw_index": pivot["raw_index"],
                    "pivot_label": pivot["label"],
                    "cofactor_raw_index": cofactor["raw_index"],
                    "cofactor_label": cofactor["label"],
                    "eliminated_variable": name,
                    "pivot_coefficient": str(A),
                    "pivot_residual": str(B),
                    "cofactor_coefficient": str(C),
                    "cofactor_residual": str(D),
                    "identity": "A*cofactor-C*pivot=resultant",
                    "content": [content.numerator, content.denominator],
                    "monomial_exponents": list(monomial),
                    "primitive_profile": primitive_profile,
                    "primitive": str(primitive),
                    "primitive_terms": encode_poly(primitive, variables, sp),
                    "packet_term_count": (pivot["term_count"] +
                                          cofactor["term_count"]),
                })
    require(candidates, "no fraction-free short-row/cofactor packet found")
    candidates.sort(key=lambda item:
                    (item["primitive_profile"]["term_count"],
                     item["primitive_profile"]["total_degree"],
                     item["packet_term_count"],
                     item["pivot_raw_index"], item["cofactor_raw_index"],
                     item["eliminated_variable"]))
    best = candidates[0]
    shortest_candidates = [item for item in candidates
                           if item["pivot_raw_index"] ==
                           shortest["raw_index"]]
    require(shortest_candidates,
            "shortest row has no literal-cofactor elimination packet")
    best_shortest = shortest_candidates[0]

    def attach_factorization(candidate):
        primitive = sp.Poly(candidate["primitive"], *variables,
                            domain=sp.QQ).as_expr()
        factorization = sp.factor_list(primitive, *variables)
        candidate["factorization_coefficient"] = str(factorization[0])
        candidate["factors"] = []
        for factor, multiplicity in factorization[1]:
            candidate["factors"].append({
                "multiplicity": multiplicity,
                **poly_profile(factor, variables, sp),
                "polynomial": str(factor),
                "terms": encode_poly(factor, variables, sp),
            })

    attach_factorization(best)
    if best_shortest is not best:
        attach_factorization(best_shortest)

    shortest_poly = poly_by_index[shortest["raw_index"]]
    shortest_solve_options = []
    for name in shortest["linear_variables"]:
        x = variable_by_name[name]
        px = sp.Poly(shortest_poly, x)
        coefficient, residual = px.nth(1), px.nth(0)
        shortest_solve_options.append({
            "variable": name,
            "coefficient": str(coefficient),
            "coefficient_profile": poly_profile(coefficient, variables, sp),
            "residual": str(residual),
            "residual_profile": poly_profile(residual, variables, sp),
        })
    shortest_solve_options.sort(key=lambda item:
                                (item["coefficient_profile"]["term_count"],
                                 item["coefficient_profile"]["total_degree"],
                                 item["residual_profile"]["term_count"],
                                 item["variable"]))

    # Literal replay of the selected identity.
    f = poly_by_index[best["pivot_raw_index"]]
    g = poly_by_index[best["cofactor_raw_index"]]
    x = variable_by_name[best["eliminated_variable"]]
    pf, pg = sp.Poly(f, x), sp.Poly(g, x)
    A, B, C, D = pf.nth(1), pf.nth(0), pg.nth(1), pg.nth(0)
    replay = sp.expand(A * g - C * f - (A * D - C * B))
    require(replay == 0, "fraction-free literal identity failed")

    if args.mode == "mutation":
        # Must fire if a single endpoint-ordered source coefficient changes.
        mutated = sp.expand(A * (g + 1) - C * f - (A * D - C * B))
        require(mutated != 0, "source mutation failed to fire")

    result = {
        "status": "PASS exact structural reverse interface; no ideal solve",
        "mode": args.mode,
        "state": "0:31:30",
        "routing": routed,
        "edge_order": ["01", "02", "03", "12", "13", "23"],
        "chart": {
            "selected_offdiagonal_edges": [0, 1, 2, 3, 4],
            "selected_diagonal_edges": [5],
            "both_live_edges": [1, 2, 3, 4],
            "gauge_b_edges": record["gauge_b_edges"],
            "gauge_d_edge": record["gauge_d_edge"],
            "active_variables": active_names,
            "raw_source_row_count": record["raw_source_row_count"],
            "nonzero_gauged_source_row_count": len(profiles),
            "source_substitution": (
                "T_e=1,D_e=1: [[a,b],[-(1+a*d)/b,d]]; "
                "T_e=1,D_e=0: [[a,b],[-1/b,0]]; "
                "T_e=0: [[a,b],[0,-1/a]]"),
        },
        "source_profiles": profiles,
        "shortest_row": shortest,
        "shortest_row_solve_options": shortest_solve_options,
        "candidate_count": len(candidates),
        "best_fraction_free_packet": best,
        "best_shortest_row_cofactor_packet": best_shortest,
        "top_fraction_free_packets": [
            {key: value for key, value in candidate.items()
             if key not in ("primitive_terms",)}
            for candidate in candidates[:12]],
        "localizers_from_parent_chart": record["localizers"],
        "source_hashes": {
            "literal_builder": file_sha(BUILDER_PATH),
            "routing_ledger": file_sha(ROUTING_PATH),
        },
        "scope_guard": (
            "The selected identity is a necessary fraction-free consequence "
            "of two literal source rows. It neither divides by its pivot "
            "coefficient nor proves the face empty. The pivot-open and "
            "pivot-zero branches must be treated separately, and any result "
            "using the remaining-c localizer covers only the interior, not "
            "the routed descendants."),
    }
    result["logical_sha256"] = logical_sha(result)
    suffix = "mutation" if args.mode == "mutation" else "standard"
    out = OUT_PREFIX.with_name(OUT_PREFIX.name + "_" + suffix + ".json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("face 0:31:30 structural reverse interface: PASS")
    print("shortest:", shortest["raw_index"], shortest["label"],
          shortest["term_count"], shortest["linear_variables"])
    print("best packet:", best["pivot_raw_index"],
          best["cofactor_raw_index"], best["eliminated_variable"],
          best["primitive_profile"])
    print("best shortest-row packet:",
          best_shortest["pivot_raw_index"],
          best_shortest["cofactor_raw_index"],
          best_shortest["eliminated_variable"],
          best_shortest["primitive_profile"])
    print("shortest solve first:", shortest_solve_options[0])
    print("factors:", [(row["term_count"], row["total_degree"],
                        row["multiplicity"]) for row in best["factors"]])
    print("logical sha256:", result["logical_sha256"])


if __name__ == "__main__":
    main()

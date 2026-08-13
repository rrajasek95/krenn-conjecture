#!/usr/bin/env python3
"""Exact global minimum-support census for the h=3 axis-pure branch.

The Boolean formula contains every one of the 69 axis coordinates and every
one of the 3645 matching monomials.  It imposes:

* each monomial variable iff all its coordinate variables are occupied;
* at least one monomial in each of the three target fibres;
* never exactly one monomial in an off-target fibre;
* every occupied coordinate lies in a live matching monomial;
* the pure-zero target matching is fixed to 01|23|45.

The fourth condition is the minimum-occupied-support reduction: deleting an
occupied coordinate which occurs in no active coefficient changes none of
the equations.  The formula has exactly six cell-support models.  Direct
rechecking shows all six have support 27 and are the F0+K2,2+K2,4 stratum.
After blocking the six cell assignments the formula is UNSAT.  The six
support-27 coefficient systems are excluded by the pinned polynomial
certificate, so the entire minimum-support axis-pure branch is empty.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = "computations/verify_h3_axis_pure_cancellation_support_lower_bound.py"
PINS = {
    BASE_PATH:
        "c7c501de4c4646b98e5525d616012bbced15957dcaaa836ebe38341c56385397",
    "notes/h3-axis-pure-cancellation-support-lower-bound.md":
        "b81542ec64eb0667c7c70109d15a0e92932d8e1ffeb124c87992a0abe96a41cc",
    "computations/verify_h3_axis_pure_singleton_mate_closure_coloop_gate.py":
        "5e79bd4cf1cdc090e75da25518044ff85e1f993f1d074049eed4f327e22f01e9",
    "notes/h3-axis-pure-singleton-mate-closure-coloop-gate.md":
        "d9d0486e7424db3720a91ea9421f837393dd2102f24f118f655b477704d6421c",
    "computations/verify_h3_axis_pure_support27_coefficient_inconsistency.py":
        "5069cc76a5fbfbba115177ab1895c180346b15d4826ca5b419ca7753aabedb65",
    "notes/h3-axis-pure-support27-coefficient-inconsistency.md":
        "98710742a10bc584eff02936dc3b49bdd407fbf122aa08331a936334c007c37e",
}
EXPECTED_LEDGER_SHA256 = "89c67e45a7ba5e05cba4dfbef988957d14ffd996bc8b3a53739c9dff9692d3b9"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load_base():
    specification = importlib.util.spec_from_file_location(
        "axis_pure_global_census_base", ROOT / BASE_PATH)
    require(specification is not None and specification.loader is not None,
            "cannot import base checker")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def solver_api():
    try:
        from pysat.solvers import Solver  # type: ignore
    except ImportError as error:
        # ``python -I -S`` intentionally omits virtual-environment site
        # initialization.  Add only this repository's pinned local venv path;
        # this preserves isolated/no-user-site testing without changing the
        # solver backend or frozen ledger.
        candidates = sorted((ROOT / ".venv" / "lib").glob(
            "python*/site-packages"))
        require(len(candidates) == 1,
                ("python-sat unavailable and local venv path ambiguous",
                 candidates, error))
        sys.path.insert(0, str(candidates[0]))
        from pysat.solvers import Solver  # type: ignore
    return Solver


def build_formula(base):
    coordinates = tuple(sorted(base.ALL_COORDINATES, key=base.coordinate_key))
    coordinate_index = {coordinate: index
                        for index, coordinate in enumerate(coordinates)}
    cell_vars = tuple(range(1, len(coordinates) + 1))

    terms_by_fibre = base.all_matching_terms()
    terms = []
    term_ids_by_fibre = {}
    term_ids_by_coordinate = [[] for _ in coordinates]
    next_variable = len(coordinates) + 1
    for fibre in sorted(terms_by_fibre, key=base.fibre_label):
        ids = []
        for term in terms_by_fibre[fibre]:
            coordinate_ids = tuple(sorted(coordinate_index[value]
                                          for value in term))
            variable = next_variable
            next_variable += 1
            term_id = len(terms)
            terms.append((variable, coordinate_ids))
            ids.append(term_id)
            for coordinate_id in coordinate_ids:
                term_ids_by_coordinate[coordinate_id].append(term_id)
        term_ids_by_fibre[fibre] = tuple(ids)

    clauses = []
    # m <-> AND cells: m=>cell for every factor, AND cells=>m.
    for variable, coordinate_ids in terms:
        for coordinate_id in coordinate_ids:
            clauses.append((-variable, cell_vars[coordinate_id]))
        clauses.append(tuple(-cell_vars[index] for index in coordinate_ids)
                       + (variable,))

    target_fibres = 0
    off_target_fibres = 0
    no_singleton_clauses = 0
    for fibre, term_ids in term_ids_by_fibre.items():
        variables = tuple(terms[index][0] for index in term_ids)
        if base.is_target_fibre(fibre):
            clauses.append(variables)
            target_fibres += 1
            continue
        off_target_fibres += 1
        # count != 1: if one term is live, at least one other is live.
        for position, variable in enumerate(variables):
            others = variables[:position] + variables[position + 1:]
            clauses.append((-variable,) + others)
            no_singleton_clauses += 1

    # Minimum-support condition: every selected coordinate participates in
    # an active monomial.  Otherwise it can be deleted without changing a
    # coefficient or the target.
    for coordinate_id, term_ids in enumerate(term_ids_by_coordinate):
        require(term_ids, "an axis coordinate appears in no matching term")
        clauses.append((-cell_vars[coordinate_id],)
                       + tuple(terms[index][0] for index in term_ids))

    # Normalize the pure-zero target matching by site symmetry.
    for physical_edge in base.F0:
        clauses.append((cell_vars[coordinate_index[("q", 0, physical_edge)]],))

    require(len(coordinates) == 69 and len(terms) == 3645
            and len(term_ids_by_fibre) == 849
            and target_fibres == 3 and off_target_fibres == 846,
            "the global formula dimensions changed")
    return {
        "coordinates": coordinates,
        "coordinate_index": coordinate_index,
        "cell_vars": cell_vars,
        "terms": tuple(terms),
        "term_ids_by_fibre": term_ids_by_fibre,
        "term_ids_by_coordinate": tuple(map(tuple, term_ids_by_coordinate)),
        "clauses": tuple(clauses),
        "top_variable": next_variable - 1,
        "target_fibres": target_fibres,
        "off_target_fibres": off_target_fibres,
        "no_singleton_clauses": no_singleton_clauses,
    }


def direct_recheck(base, formula, selected_indices) -> dict[str, object]:
    selected = frozenset(selected_indices)
    support = frozenset(formula["coordinates"][index] for index in selected)
    live_terms = set()
    target_counts = []
    off_target_counts = []
    for fibre, term_ids in formula["term_ids_by_fibre"].items():
        count = 0
        for term_id in term_ids:
            _variable, coordinate_ids = formula["terms"][term_id]
            if set(coordinate_ids) <= selected:
                count += 1
                live_terms.add(term_id)
        if base.is_target_fibre(fibre):
            require(count >= 1, ("target missing", base.fibre_label(fibre)))
            target_counts.append(count)
        else:
            require(count != 1,
                    ("off-target singleton", base.fibre_label(fibre)))
            if count:
                off_target_counts.append(count)

    require(all(any(term_id in live_terms for term_id in
                    formula["term_ids_by_coordinate"][coordinate_id])
                for coordinate_id in selected),
            "a selected coordinate is unused")

    q_edges = {
        colour: frozenset(coordinate[2] for coordinate in support
                          if coordinate[0] == "q" and coordinate[1] == colour)
        for colour in range(3)
    }
    endpoint_shores = {
        f"{shore}{colour}": tuple(sorted(coordinate[2]
            for coordinate in support if coordinate[:2] == (shore, colour)))
        for shore in ("p", "s") for colour in (1, 2)
    }
    graph_degrees = {}
    for colour, edges in q_edges.items():
        degree = Counter()
        for left, right in edges:
            degree[left] += 1
            degree[right] += 1
        graph_degrees[str(colour)] = sorted(degree.values())
    require(len(support) == 27
            and sorted(map(len, (q_edges[1], q_edges[2]))) == [4, 8]
            and sorted((graph_degrees["1"], graph_degrees["2"])) == [
                [2, 2, 2, 2], [2, 2, 2, 2, 4, 4]
            ]
            and endpoint_shores["p1"] == endpoint_shores["s1"]
            and endpoint_shores["p2"] == endpoint_shores["s2"]
            and sorted(map(len, endpoint_shores.values())) == [2, 2, 4, 4],
            "a global model left the support-27 structural type")
    return {
        "support_size": len(support),
        "support": list(base.support_key(support)),
        "target_term_counts": sorted(target_counts),
        "active_off_target_fibres": len(off_target_counts),
        "off_target_term_count_histogram": dict(sorted(Counter(
            off_target_counts).items())),
        "q_support_sizes": {str(colour): len(edges)
                            for colour, edges in q_edges.items()},
        "q_degree_profiles": graph_degrees,
        "endpoint_shores": {name: list(sites)
                            for name, sites in endpoint_shores.items()},
    }


def enumerate_models(base, formula, solver_name):
    Solver = solver_api()
    models = []
    clauses = list(formula["clauses"])
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        while solver.solve():
            raw_model = set(solver.get_model() or ())
            selected = tuple(index for index, variable in enumerate(
                formula["cell_vars"]) if variable in raw_model)
            record = direct_recheck(base, formula, selected)
            models.append((selected, record))
            # Projection block: auxiliary term variables are functions of the
            # cells, but block on cells explicitly to make the census robust.
            selected_set = set(selected)
            blocking = [(-variable if index in selected_set else variable)
                        for index, variable in enumerate(formula["cell_vars"])]
            solver.add_clause(blocking)
        final_unsat = True
    require(len(models) == 6 and len({selected for selected, _ in models}) == 6
            and {record["support_size"] for _selected, record in models} == {27},
            ("the global model census changed", len(models),
             Counter(record["support_size"] for _selected, record in models)))
    canonical = tuple(sorted(
        (record for _selected, record in models),
        key=lambda record: tuple(record["support"])
    ))
    return canonical, final_unsat


def formula_digest(formula) -> str:
    payload = {
        "top_variable": formula["top_variable"],
        "clauses": formula["clauses"],
    }
    return sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    base = load_base()
    formula = build_formula(base)
    glucose_models, glucose_unsat = enumerate_models(base, formula, "g4")
    cadical_models, cadical_unsat = enumerate_models(base, formula, "cadical195")
    require(glucose_models == cadical_models
            and glucose_unsat and cadical_unsat,
            "independent solver censuses differ")

    ledger = {
        "theorem": "h3 axis-pure global minimum-support census and emptiness",
        "pins": PINS,
        "formula": {
            "cell_variables": len(formula["cell_vars"]),
            "term_variables": len(formula["terms"]),
            "top_variable": formula["top_variable"],
            "clauses": len(formula["clauses"]),
            "target_fibres": formula["target_fibres"],
            "off_target_fibres": formula["off_target_fibres"],
            "no_singleton_clauses": formula["no_singleton_clauses"],
            "mandatory_F0": [list(edge) for edge in sorted(base.F0)],
            "minimum_support_clause": (
                "every occupied coordinate occurs in at least one live monomial"
            ),
            "sha256": formula_digest(formula),
        },
        "global_census": {
            "projected_cell_models": len(glucose_models),
            "model_support_sizes": [record["support_size"]
                                    for record in glucose_models],
            "models": glucose_models,
            "after_six_cell_blocks": "UNSAT",
            "solvers": ["glucose4", "cadical195"],
            "independent_censuses_agree": True,
            "each_model_directly_rechecked": True,
            "models_above_support27": 0,
        },
        "coefficient_consequence": {
            "all_six_support_models": "F0 + bright K2,2 + bright K2,4",
            "pinned_support27_certificate": (
                "three K2,4 permanent equations force 2*unit=0; independently "
                "q01*f_target-E1*f_q=-q01*X1"
            ),
            "all_six_coefficient_systems_inconsistent": True,
            "minimum_support_axis_pure_exact_source_exists": False,
            "any_axis_pure_exact_source_exists": False,
            "logic": (
                "if an exact source exists, the finite coordinate universe "
                "contains a minimum-occupied-support exact source.  Every "
                "coordinate in it occurs in a live monomial, since an unused "
                "coordinate can be set to zero without changing any equation "
                "or target.  Its support satisfies this formula, whose only "
                "six candidates are coefficient-inconsistent"
            ),
        },
        "verdict": (
            "There is no h=3 axis-pure exact source.  The global Boolean "
            "minimum-support formula has exactly six F0-normalized models, all "
            "at support 27 and all of the already excluded K2,2/K2,4 type; "
            "blocking them makes the unrestricted formula UNSAT.  Thus no "
            "larger inclusion-minimal stratum exists and arbitrary-coloop "
            "normalization is unnecessary for the axis-pure branch."
        ),
        "scope": (
            "canonical h=3 axis-purified five-tensor equations over a "
            "characteristic-zero field; this does not address the unpurified "
            "source branch"
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    census = ledger["global_census"]
    print("axis-pure global minimum-support models:",
          census["projected_cell_models"])
    print("model support sizes:", census["model_support_sizes"])
    print("after six projected cell blocks: UNSAT (g4 + cadical195)")
    print("support-27 coefficient certificate excludes every model")
    print("h=3 axis-pure exact source branch: EMPTY")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

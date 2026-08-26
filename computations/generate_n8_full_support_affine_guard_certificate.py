#!/usr/bin/env python3
"""Generate the RUP certificate exhausting the support-28 occurrence guards.

The semantic theorem checker reconstructs the base CNF and the full orbit;
this script is only the proof-producing side and therefore depends on PySAT.
"""

from __future__ import annotations

import argparse
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def load_search():
    path = HERE / "search_n8_global_occurrence_cnf.py"
    spec = spec_from_file_location("n8_global_occurrence_cnf", path)
    require(spec is not None and spec.loader is not None, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = load_search()


REPRESENTATIVE = {
    (0, 1): (1, 2),
    (0, 2): (0, 1, 2),
    (0, 3): (0, 1),
    (0, 4): (2,),
    (0, 5): (0, 2),
    (0, 6): (0,),
    (0, 7): (1,),
    (1, 2): (0,),
    (1, 3): (0, 2),
    (1, 4): (1,),
    (1, 5): (0, 1),
    (1, 6): (0, 1, 2),
    (1, 7): (2,),
    (2, 3): (2,),
    (2, 4): (0, 1),
    (2, 5): (1,),
    (2, 6): (1, 2),
    (2, 7): (0, 2),
    (3, 4): (0, 1, 2),
    (3, 5): (1, 2),
    (3, 6): (1,),
    (3, 7): (0,),
    (4, 5): (0,),
    (4, 6): (0, 2),
    (4, 7): (1, 2),
    (5, 6): (2,),
    (5, 7): (0, 1, 2),
    (6, 7): (0, 1),
}

REPRESENTATIVE_FULL = {
    (0, 1): (0, 1, 2), (0, 2): (2,), (0, 3): (0, 1),
    (0, 4): (0, 2), (0, 5): (1, 2), (0, 6): (1,), (0, 7): (0,),
    (1, 2): (0, 1), (1, 3): (2,), (1, 4): (1,), (1, 5): (0,),
    (1, 6): (0, 2), (1, 7): (1, 2), (2, 3): (0, 1, 2),
    (2, 4): (0,), (2, 5): (1,), (2, 6): (1, 2), (2, 7): (0, 2),
    (3, 4): (1, 2), (3, 5): (0, 2), (3, 6): (0,), (3, 7): (1,),
    (4, 5): (0, 1), (4, 6): (0, 1, 2), (4, 7): (2,),
    (5, 6): (2,), (5, 7): (0, 1, 2), (6, 7): (0, 1),
}


def orbit(target_support):
    representative = (REPRESENTATIVE if target_support == (1, 2)
                      else REPRESENTATIVE_FULL)
    colour_group = (
        ((0, 1, 2), (0, 2, 1))
        if target_support == (1, 2)
        else tuple(permutations(range(3)))
    )
    answers = set()
    for swap_endpoints in (False, True):
        for tail in permutations(range(2, 8)):
            vertex = {
                0: 1 if swap_endpoints else 0,
                1: 0 if swap_endpoints else 1,
            }
            vertex.update({2 + index: value
                           for index, value in enumerate(tail)})
            for colour_tuple in colour_group:
                colour = dict(enumerate(colour_tuple))
                transformed = {}
                for edge, support in representative.items():
                    new_edge = tuple(sorted((vertex[edge[0]], vertex[edge[1]])))
                    transformed[new_edge] = tuple(sorted(
                        colour[item] for item in support
                    ))
                answers.add(tuple(
                    transformed[edge] for edge in C.EDGES
                ))
    require(len(answers) == 720, len(answers))
    return tuple(sorted(answers))


def build_exhaustion_cnf(target_support):
    cnf, y, *_rest = C.build_instance(28, target_support, None, 4)
    for support_tuple in orbit(target_support):
        clause = []
        for edge, support in zip(C.EDGES, support_tuple, strict=True):
            for colour in C.COLORS:
                variable = y[edge, colour]
                clause.append(-variable if colour in support else variable)
        cnf.add(*clause)
    return cnf


def main():
    from pysat.solvers import Solver

    parser = argparse.ArgumentParser()
    parser.add_argument("--target-support", choices=("12", "012"),
                        default="12")
    parser.add_argument(
        "--prefix",
        default="computations/certificates/"
                "n8_full_support_affine_guard_exhaustion",
    )
    arguments = parser.parse_args()
    target_support = tuple(map(int, arguments.target_support))
    prefix = Path(arguments.prefix)
    cnf_path = prefix.with_suffix(".cnf")
    proof_path = prefix.with_suffix(".drup")
    cnf = build_exhaustion_cnf(target_support)
    cnf_path.write_text(cnf.dimacs(), encoding="ascii")
    with Solver(name="glucose42", bootstrap_with=cnf.clauses,
                with_proof=True) as solver:
        require(not solver.solve(), "orbit-excluded CNF is SAT")
        proof = solver.get_proof() or []
    additions = [line for line in proof if not line.startswith("d ")]
    require(additions and additions[-1].strip() == "0",
            "proof does not end in the empty clause")
    proof_path.write_text("\n".join(additions) + "\n", encoding="ascii")
    print("variables", len(cnf.names), "clauses", len(cnf.clauses))
    print("orbit", len(orbit(target_support)),
          "proof_additions", len(additions))
    print("cnf", cnf_path)
    print("proof", proof_path)


if __name__ == "__main__":
    main()

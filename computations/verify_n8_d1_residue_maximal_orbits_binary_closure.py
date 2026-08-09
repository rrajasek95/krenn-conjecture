#!/usr/bin/env python3
"""Close five maximal D1 residue orbits by exact binary K4 certificates."""

from __future__ import annotations

import ast
import hashlib
import importlib
import itertools
import os
import sys
from collections import Counter
from time import monotonic

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


SOURCES = {
    "maximal": (
        "verify_n8_d1_residue_maximal_orbits.py",
        "e5b01be3c4ccf6af927c87ba08fed6b1f0aeb7fa05b4cc2bcbcac93a3bcbfa8e",
    ),
    "profiles": (
        "verify_n8_d1_tripod_projection_profile_classification.py",
        "d02a156d61e4ffaa518be3d8e57490310788f89cd99fcbc907437b0ea02b5fa7",
    ),
    "orbit4": (
        "verify_n8_d1_residue_orbit4_family_and_lift.py",
        "ccf37cd1d35584c9d064200e2614dcacacf6c99ec3a0af327a92ca25ac1eb652",
    ),
}
for label, (filename, digest) in SOURCES.items():
    with open(os.path.join(HERE, filename), "rb") as handle:
        require(hashlib.sha256(handle.read()).hexdigest() == digest,
                "the pinned %s source changed" % label)

R = importlib.import_module("verify_n8_d1_residue_maximal_orbits")
P = importlib.import_module(
    "verify_n8_d1_tripod_projection_profile_classification"
)
O4 = importlib.import_module("verify_n8_d1_residue_orbit4_family_and_lift")
C, D, V = R.C, R.D, R.V

EXPECTED_LEDGER_SHA256 = (
    "a8762b8bf42e9fb35631a21d4fb8b301f1d317e35d8ff955658e270f68ea9971"
)

# Coefficients returned by Singular's lift command were copied once, but the
# checker below reconstructs and verifies each identity without invoking
# Singular.  Entry j multiplies the j-th nonzero binary fibre generator in
# lexicographic word order on {0,2}^4.
CERTIFICATES = {
    1: {
        "monomial": "x4602*x5600*x6720",
        "coefficients": (
            "x4622*x5622*x6722", "-x4622*x5622*x6720",
            "x4620*x5622*x6722",
            "-x4622*x5622*x6700-x4620*x5622*x6720", "0",
            "-x4622*x5600*x6722", "x4622*x5600*x6720",
            "-x4602*x5622*x6722", "x4602*x5622*x6720",
            "-x4600*x5622*x6722",
            "x4602*x5622*x6700+x4600*x5622*x6720", "0",
            "x4602*x5600*x6722", "-x4602*x5600*x6720",
        ),
    },
    2: {
        "monomial": "x4602*x5600*x6720",
        "coefficients": (
            "x4622*x5622*x6722", "-x4622*x5622*x6720",
            "x4622*x5622*x6702", "-x4622*x5622*x6700", "0", "0",
            "-x4622*x5600*x6722", "x4622*x5600*x6720",
            "-x4602*x5622*x6722", "x4602*x5622*x6720",
            "-x4602*x5622*x6702-x4600*x5622*x6722",
            "x4602*x5622*x6700+x4600*x5622*x6720", "0", "0",
            "x4602*x5600*x6722", "-x4602*x5600*x6720",
        ),
    },
    3: {
        "monomial": "x4602*x5600*x6720",
        "coefficients": (
            "x4622*x5622*x6722", "-x4622*x5622*x6720",
            "x4622*x5622*x6702+x4620*x5622*x6722",
            "-x4622*x5622*x6700-x4620*x5622*x6720", "0", "0",
            "-x4622*x5600*x6722", "x4622*x5600*x6720",
            "-x4602*x5622*x6722", "x4602*x5622*x6720",
            "-x4602*x5622*x6702-x4600*x5622*x6722",
            "x4602*x5622*x6700+x4600*x5622*x6720", "0", "0",
            "x4602*x5600*x6722", "-x4602*x5600*x6720",
        ),
    },
    5: {
        "monomial": "x4702*x5702*x6700",
        "coefficients": (
            "0", "x4722*x5720*x6722", "0", "0",
            "-x4722*x5702*x6722", "0", "x4722*x5702*x6700", "0",
            "-x4702*x5720*x6722", "0", "x4702*x5702*x6722",
            "-x4702*x5702*x6700",
        ),
    },
    6: {
        "monomial": "x4702*x5700*x6702",
        "coefficients": (
            "x4722*x5722*x6722", "0", "-x4722*x5722*x6702",
            "-x4722*x5722*x6700", "0", "-x4722*x5700*x6722", "0",
            "x4722*x5700*x6702", "-x4702*x5722*x6722",
            "-x4700*x5722*x6722",
            "x4702*x5722*x6700+x4700*x5722*x6702", "0",
            "x4702*x5700*x6722", "-x4702*x5700*x6702",
        ),
    },
}


def product(polynomials):
    out = D.p_const(1)
    for polynomial in polynomials:
        out = D.p_mul(out, polynomial)
    return out


def parse_polynomial(source):
    """Parse the tiny +,-,* integer polynomial grammar used above."""
    tree = ast.parse(source, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return D.p_const(node.value)
        if isinstance(node, ast.Name):
            return D.p_var(node.id)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return D.p_sub(D.p_const(0), visit(node.operand))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            return D.p_add(visit(node.left), visit(node.right))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Sub):
            return D.p_sub(visit(node.left), visit(node.right))
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
            return D.p_mul(visit(node.left), visit(node.right))
        raise RuntimeError("unsupported certificate syntax: %s" % ast.dump(node))

    return visit(tree)


def variable_name(cell):
    return "x%d%d%d%d" % cell


def binary_system(orbit_index):
    holes = set(R.EXPECTED_HOLES[orbit_index - 1])
    active = frozenset(
        V.cell(u, v, left, right)
        for u, v in itertools.combinations(V.RESIDUE, 2)
        for left, right in itertools.product((0, 2), repeat=2)
        if V.cell(u, v, left, right) not in holes
    )
    variables = {cell: D.p_var(variable_name(cell)) for cell in active}
    generators = []
    words = []
    for colours in itertools.product((0, 2), repeat=4):
        word = dict(zip(V.RESIDUE, colours))
        terms = []
        for matching in V.MATCHINGS[V.RESIDUE]:
            cells = tuple(V.cell(u, v, word[u], word[v])
                          for u, v in matching)
            if all(cell in active for cell in cells):
                terms.append(product(variables[cell] for cell in cells))
        polynomial = D.p_const(0)
        for term in terms:
            polynomial = D.p_add(polynomial, term)
        if colours == (2, 2, 2, 2):
            polynomial = D.p_sub(polynomial, D.p_const(1))
        if polynomial:
            words.append(colours)
            generators.append(polynomial)
    return active, tuple(words), tuple(generators)


def support_profile_audit(orbit_index):
    support = set(V.cell(u, v, left, right)
                  for u, v in itertools.combinations(V.RESIDUE, 2)
                  for left, right in itertools.product(V.COLORS, repeat=2))
    support -= set(R.EXPECTED_HOLES[orbit_index - 1])
    row_checks = []
    for center in V.RESIDUE:
        for neighbour in V.RESIDUE:
            if center == neighbour:
                continue
            rows = []
            for source in (0, 1):
                rows.append(tuple(colour for colour in V.COLORS
                                  if V.cell(center, neighbour, source, colour)
                                  in support))
            require(rows[0] == rows[1] and rows[0],
                    "orbit %d lost equal non-target row supports" % orbit_index)
            require(any(colour != 2 for colour in rows[0]),
                    "orbit %d acquired a target-only projected row" % orbit_index)
            row_checks.append([center, neighbour, list(rows[0])])
    return row_checks


def certificate_audit(orbit_index):
    active, words, generators = binary_system(orbit_index)
    data = CERTIFICATES[orbit_index]
    coefficients = tuple(parse_polynomial(source)
                         for source in data["coefficients"])
    require(len(coefficients) == len(generators),
            "orbit %d lift length changed" % orbit_index)
    left = D.p_const(0)
    for coefficient, generator in zip(coefficients, generators):
        left = D.p_add(left, D.p_mul(coefficient, generator))
    monomial = parse_polynomial(data["monomial"])
    require(left == monomial,
            "orbit %d monomial identity failed" % orbit_index)
    factors = tuple(data["monomial"].split("*"))
    active_names = {variable_name(cell) for cell in active}
    require(set(factors) <= active_names,
            "orbit %d certificate monomial is not localized" % orbit_index)
    return {
        "orbit": orbit_index,
        "residue_support_size": 54 - len(R.EXPECTED_HOLES[orbit_index - 1]),
        "binary_active_cells": len(active),
        "binary_nonzero_generators": len(generators),
        "binary_generator_words": [list(word) for word in words],
        "lift_nonzero_coefficients": sum(bool(poly) for poly in coefficients),
        "localized_monomial": data["monomial"],
        "localized_monomial_degree": len(factors),
        "identity_sha256": D.content_hash({
            "generators": generators,
            "coefficients": coefficients,
            "monomial": monomial,
        }),
    }


def build_ledger():
    rows = []
    for orbit_index in (1, 2, 3, 5, 6):
        profile_rows = support_profile_audit(orbit_index)
        certificate = certificate_audit(orbit_index)
        certificate["equal_nontarget_row_checks"] = len(profile_rows)
        certificate["dimension_two_branch"] = {
            "possible_profiles": ["111", "112", "122", "222"],
            "rank_one_image_lines_target_aligned": 0,
            "verdict": (
                "UNSAT by eeae4b3: 222 has no pure companion; each of "
                "111/112/122 requires target alignment of at least one "
                "rank-one projected line"
            ),
        }
        certificate["dimension_at_most_one_branch"] = {
            "actual_dimension": 1,
            "reduction": (
                "the two non-target tripod rows are proportional at each "
                "vertex; equal row supports and localized entries make the "
                "four ratios units and reduce all residue fibres to the "
                "binary {non-target,target} K4 system"
            ),
            "verdict": "UNSAT by the checked ordinary monomial identity",
        }
        rows.append(certificate)

    require([row["binary_nonzero_generators"] for row in rows]
            == [14, 16, 16, 12, 14],
            "the binary generator-count signature changed")
    require(Counter(row["localized_monomial_degree"] for row in rows)
            == {3: 5}, "a binary certificate stopped being cubic")

    return {
        "scope": "five non-O4 maximal D1 residue support orbits",
        "pinned_sources": SOURCES,
        "profile_theorem": {
            "dimK2": (
                "all zero profiles are impossible for nonzero opposite "
                "blocks; 222 is impossible; 122/112/111 require the "
                "target-line alignments classified by eeae4b3"
            ),
            "dimK1": (
                "directed target-line support makes non-target rows share "
                "a unit proportionality ratio, giving a binary K4 quotient"
            ),
        },
        "closed_orbits": rows,
        "orbit4": {
            "residue_support_size": 34,
            "status": "residue feasible (checked 14-parameter family)",
            "full_coupling_status": (
                "all but the four boundary omissions x02_20,x02_21," 
                "x13_20,x13_21 are closed by the checked pure-fibre lift"
            ),
            "boundary_omissions": ["x02_20", "x02_21", "x13_20", "x13_21"],
        },
        "conclusion": (
            "O1,O2,O3,O5,O6 are residue-empty over every field after "
            "localizing their named support cells; O4 is the sole maximal "
            "residue orbit needing external six-/eight-site coupling"
        ),
    }


def main():
    started = monotonic()
    ledger = build_ledger()
    digest = D.content_hash(ledger)
    if EXPECTED_LEDGER_SHA256 == "TO_BE_FROZEN":
        print("ledger sha256: %s" % digest)
    else:
        require(digest == EXPECTED_LEDGER_SHA256,
                "the maximal-orbit binary-closure ledger changed")
        print("ledger sha256 (frozen): %s" % digest)
    print("closed maximal residue orbits: 1,2,3,5,6")
    print("binary generator counts: 14,16,16,12,14")
    print("O4 status: residue-feasible; four boundary omissions remain")
    print("elapsed: %.3fs" % (monotonic() - started))


if __name__ == "__main__":
    main()

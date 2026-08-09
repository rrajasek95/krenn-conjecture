#!/usr/bin/env python3
"""Certify the literal single-site affinity behind the P5 Rees chart.

The generic-L bend z46 is a four-cell ambient tangent direction, but every
cell in its support is incident to site 7.  The eleven newest transverse P5
directions are supported entirely on cells incident to site 0.  Since a
perfect matching uses exactly one edge at each site, every universal matching
coefficient is affine in each complete direction block before any normal or
strict-transform graph solution is substituted.
"""

from hashlib import sha256
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_module(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


LOCAL = load_module(
    "n8_local_standard_basis_for_p5_rees_affinity",
    "analyze_n8_counterexample_local_standard_basis.py",
)
P5 = load_module(
    "n8_p5_degree6_for_rees_affinity",
    "verify_n8_p5_degree6_compatibility_kills_h0.py",
)

EXPECTED_LEDGER_SHA256 = (
    "c6e15e7b207f8bddca79fc4df50ce1d62b10f86b814a9cdaa5751f27a91780f0"
)


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def encoded_direction(reducer, parameter):
    vector = reducer.data["tangent_basis"][parameter]
    return [
        [coordinate, list(LOCAL.FACTOR.AMBIENT_COORDINATES[coordinate]),
         coefficient.numerator, coefficient.denominator]
        for coordinate, coefficient in sorted(vector.items())
    ]


def audit():
    reducer = LOCAL.LocalReducer()
    r_parameter = 46
    normal_parameters = P5.P5_NORMAL_VARIABLES
    r_support = set(reducer.data["tangent_basis"][r_parameter])
    normal_supports = {
        parameter: set(reducer.data["tangent_basis"][parameter])
        for parameter in normal_parameters
    }
    normal_support = set().union(*normal_supports.values())

    expected_r = {
        155: -1, 158: -1, 191: 1, 194: 1,
    }
    require(reducer.data["tangent_basis"][r_parameter] == expected_r,
            "z46 ambient support changed")
    require(len(normal_support) == 17,
            "P5 normal tangent support size changed")
    require(not r_support & normal_support,
            "bend and transverse supports began to overlap")

    r_cells = [LOCAL.FACTOR.AMBIENT_COORDINATES[index]
               for index in sorted(r_support)]
    normal_cells = [LOCAL.FACTOR.AMBIENT_COORDINATES[index]
                    for index in sorted(normal_support)]
    r_cell_set = set(r_cells)
    normal_cell_set = set(normal_cells)
    require(all(7 in cell[:2] for cell in r_cells),
            "a z46 cell left the site-7 star")
    require(all(0 in cell[:2] for cell in normal_cells),
            "a P5 transverse cell left the site-0 star")

    # Audit the actual universal matching-term constructor, not only the
    # graph-theoretic slogan.  A monomial can contain at most one cell from
    # either star.  Terms meeting both stars use the edge 0--7 in neither
    # block, as required for two distinct matching edges.
    counts = {
        "words": 0,
        "matching_terms": 0,
        "r_terms": 0,
        "normal_terms": 0,
        "bilinear_block_terms": 0,
    }
    maximum_r_degree = 0
    maximum_normal_block_degree = 0
    full = LOCAL.SOURCE.FULL
    for word in itertools.product(full.COLOURS, repeat=8):
        counts["words"] += 1
        for term in full.word_terms(word):
            counts["matching_terms"] += 1
            r_degree = len(r_cell_set.intersection(term))
            normal_degree = len(normal_cell_set.intersection(term))
            maximum_r_degree = max(maximum_r_degree, r_degree)
            maximum_normal_block_degree = max(
                maximum_normal_block_degree, normal_degree
            )
            require(r_degree <= 1,
                    "a matching term acquired a quadratic z46 contribution")
            require(normal_degree <= 1,
                    "a matching term uses two P5 transverse cells")
            counts["r_terms"] += bool(r_degree)
            counts["normal_terms"] += bool(normal_degree)
            counts["bilinear_block_terms"] += bool(r_degree and normal_degree)

    require(counts["words"] == 3 ** 8, "universal word count changed")
    require(counts["matching_terms"] == 3 ** 8 * 105,
            "universal matching-term count changed")
    require(maximum_r_degree == maximum_normal_block_degree == 1,
            "affine blocks were not both witnessed: "
            f"{maximum_r_degree}, {maximum_normal_block_degree}, {counts}")
    require(counts["bilinear_block_terms"],
            "the two affine blocks never occur together")

    ledger = {
        "ambient_variables": len(LOCAL.FACTOR.AMBIENT_COORDINATES),
        "tangent_variables": len(reducer.data["tangent_basis"]),
        "bend": {
            "parameter": r_parameter,
            "free_ambient_column": reducer.free_columns[r_parameter],
            "site": 7,
            "direction": encoded_direction(reducer, r_parameter),
        },
        "transverse": {
            "parameters": list(normal_parameters),
            "sites": [0],
            "ambient_support_size": len(normal_support),
            "directions": {
                str(parameter): encoded_direction(reducer, parameter)
                for parameter in normal_parameters
            },
        },
        "universal_audit": counts,
        "maximum_bend_degree": maximum_r_degree,
        "maximum_transverse_block_degree": maximum_normal_block_degree,
        "source_consequence": (
            "every universal hafnian coefficient is affine in z46 and "
            "collectively affine in the eleven retained P5 transverse "
            "variables; bend-transverse bilinear terms may occur"
        ),
        "scope_guard": (
            "literal source multiaffinity before substituting the solved "
            "ambient-normal or transverse strict-transform graphs"
        ),
    }
    encoded = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(encoded.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                "P5 Rees chart affinity ledger changed")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    audit()

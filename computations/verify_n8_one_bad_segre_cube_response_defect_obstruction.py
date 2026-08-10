#!/usr/bin/env python3
"""Exclude the Segre--K4 pure-additive chart by the diagonal responses.

For h=3 the response rows are

    p_i s_j q^[2] = delta_ij X_i,  i,j in {1,2}.

Every cell of the 14-cell Segre--K4 quadratic has a zero-colour endpoint,
as does every added pure-0 cell.  More generally, if every q-cell has a
zero-colour endpoint, no monomial in q^[2] can colour four residual sites
all 1 or all 2.  Hence both diagonal response coefficients vanish for
arbitrary endpoint stars and arbitrary coefficients.

The checker retains the literal hole and matching labels.  It also audits
the sharp escape condition: any nonzero pure-c response coefficient needs
two disjoint cc cells of q.  Thus the two diagonal anchors force at least
two disjoint 11 cells and two disjoint 22 cells; they cannot normalize a
Segre completion into the pure-additive chart.
"""

from __future__ import annotations

from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEPENDENCY = (
    "computations/verify_n8_one_bad_segre_cube_k4_closure_counterguard.py"
)
DEPENDENCY_SHA256 = (
    "44e2ca27001ef82ed77f73d5c956963b13507f98b4c9a1fd7b6f71b6434e700b"
)
EXPECTED_DIGEST = "bf525c6c3aaa9ddee63cb9d0f2a5caa5371df170dc368fe2c5784f1a32eb1943"
SITES = tuple(range(6))
COLOURS = tuple(range(3))
EDGES = tuple(itertools.combinations(SITES, 2))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load_dependency():
    path = ROOT / DEPENDENCY
    actual = sha256(path.read_bytes()).hexdigest()
    require(actual == DEPENDENCY_SHA256,
            f"dependency changed: {DEPENDENCY}: {actual}")
    spec = spec_from_file_location("segre_k4", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_pinned_support(module):
    base_support, base_weights, _rows, exported = module.audit_plucker_square()
    cross_cells = {
        ((2, 5), (0, 1)): 1,
        ((2, 5), (2, 0)): -1,
        ((3, 4), (0, 2)): 1,
        ((3, 4), (1, 0)): -1,
    }
    completion = module.audit_cross_completion(
        base_support, base_weights, exported
    )
    require(completion["full_top_tensor"] == 0,
            "the pinned Segre--K4 quadratic stopped being top-null")
    support = frozenset(set(base_support) | set(cross_cells))
    require(len(support) == 14,
            "the pinned Segre--K4 support changed")
    require(all(0 in colours for _edge, colours in support),
            "a pinned K4 cell lost its zero-colour endpoint")
    return support


def residual_matchings(holes):
    residual = tuple(site for site in SITES if site not in holes)
    return tuple(tuple(sorted(matching))
                 for matching in perfect_matchings(residual))


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


def diagonal_source_terms(colour):
    """Literal monomials contributing to [p*s*q^[2]]_(colour^6)."""
    terms = []
    for p_site in SITES:
        for s_site in SITES:
            if p_site == s_site:
                continue
            holes = frozenset((p_site, s_site))
            for matching in residual_matchings(holes):
                q_cells = tuple((edge, (colour, colour)) for edge in matching)
                terms.append({
                    "p_site": p_site,
                    "s_site": s_site,
                    "q_cells": q_cells,
                })
    return tuple(terms)


def audit_response_obstruction(module):
    pinned = build_pinned_support(module)
    pure_cells = frozenset((edge, (0, 0)) for edge in EDGES)
    pinned_plus_pure = pinned | pure_cells
    one_zero_endpoint_universe = frozenset(
        (edge, colours)
        for edge in EDGES
        for colours in itertools.product(COLOURS, repeat=2)
        if 0 in colours
    )
    require(pinned_plus_pure <= one_zero_endpoint_universe,
            "the pure-additive chart left the one-zero-endpoint universe")
    require(len(one_zero_endpoint_universe) == 75,
            "the one-zero-endpoint cell universe changed")

    response_ledgers = {}
    required_cells = set()
    for colour in (1, 2):
        terms = diagonal_source_terms(colour)
        require(len(terms) == 90,
                "the ordered-hole diagonal response term count changed")
        require(all(len(term["q_cells"]) == 2 for term in terms),
                "a diagonal response carrier stopped using two q cells")
        require(all(set(term["q_cells"]).isdisjoint(
                    one_zero_endpoint_universe) for term in terms),
                "a pure diagonal carrier entered the one-zero universe")
        require(all(not (set(term["q_cells"]) <= pinned_plus_pure)
                    for term in terms),
                "the pure-additive chart acquired a diagonal response term")
        required_cells.update(cell for term in terms for cell in term["q_cells"])
        response_ledgers[str(colour)] = {
            "target_word": str(colour) * 6,
            "ordered_hole_pairs": 30,
            "residual_two_matchings_per_hole_pair": 3,
            "literal_source_monomials": len(terms),
            "coefficient_on_one_zero_endpoint_universe": 0,
            "escape": f"two disjoint {colour}{colour} q-cells",
        }

    require(len(required_cells) == 30,
            "the union of pure-1/pure-2 q-cell escapes changed")
    require(all(colours in ((1, 1), (2, 2))
                for _edge, colours in required_cells),
            "a diagonal escape cell stopped being pure nonzero-colour")

    return {
        "pinned_K4_cells": len(pinned),
        "arbitrary_pure_zero_cells": len(pure_cells),
        "larger_one_zero_endpoint_universe_cells": len(
            one_zero_endpoint_universe
        ),
        "response_diagonal_ledgers": response_ledgers,
        "first_failed_response_row": "p1*s1*q^[2]=X1",
        "second_failed_response_row": "p2*s2*q^[2]=X2",
        "cross_zero_rows": ["p1*s2*q^[2]=0", "p2*s1*q^[2]=0"],
        "minimum_escape_support": (
            "a nonzero X1 response needs two disjoint 11 cells and a "
            "nonzero X2 response needs two disjoint 22 cells"
        ),
        "verdict": (
            "the four responses do not normalize a Segre completion into "
            "the pure-additive chart: both diagonal target coefficients "
            "vanish identically there, so the responses force genuinely "
            "two-nonzero-endpoint mixed cells"
        ),
    }


def main():
    module = load_dependency()
    ledger = {
        "dependency": {"path": DEPENDENCY, "sha256": DEPENDENCY_SHA256},
        "response_defect_obstruction": audit_response_obstruction(module),
        "scope": (
            "h=3 literal source coefficients with arbitrary endpoint-star "
            "linear forms; the theorem excludes the entire q-cell support "
            "class having a zero-colour endpoint, but it does not classify "
            "completions after 11/22 cells are added"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_FILLED":
        require(digest == EXPECTED_DIGEST,
                f"response-defect ledger changed: {digest}")
    print("N=8 Segre-K4 response defect obstruction: PASS")
    print("p1*s1 target X1 on pure-additive chart: identically zero")
    print("p2*s2 target X2 on pure-additive chart: identically zero")
    print("minimum escape: two disjoint 11 cells and two disjoint 22 cells")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

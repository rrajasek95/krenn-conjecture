#!/usr/bin/env python3
"""Audit three proposed reductions of the all-h comparison to h=3.

This checker proves finite algebraic shadows of three exact guards.

1. A disjoint identity-coloured spectator pair does not preserve the GHZ
   target: Delta_8 tensor I has nine word sectors rather than Delta_10's
   three, and no single two-site block can repair this factorization.
2. Parameter-trivial spectators cannot naturally promote the h=3 rootless
   terminal readout.  Direct sl2 intertwiner equations give
   Hom(Sym^5, Sym^(2h-1))=0 for h>3 (and likewise
   Hom(Sym^h, Sym^3)=0 for a bare local degree reduction).
3. Canonical two-site cap elimination does not commute with the pair
   hafnian before active cleanliness.  An exact square-free example has
   capped top coefficient 1 and effective-pair hafnian 2.

The general representation statements and cap identity are proved in the
paired note.  The bounded loops here are executable audits, not finite-h
substitutes for those proofs.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "notes/h3-reduced-eq-integral-rho-comparison-master-gate.md":
        "3fa8fdc6bcd17145bc1e40c608259b2312ee52f1482520fbe9e0f5a3cd1e7a76",
    "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py":
        "813419c756e7f21c09d63d3ec10f44c787e9580ca08c87809b7c4c550b908b4f",
    "notes/uniform_adjacent_cycle_filtered_prolongation.md":
        "90926cce63f1dec2a6fe62900afa0c29bea454d642c5b68b9791c5f87904f8bc",
    "computations/verify_uniform_adjacent_cycle_filtered_prolongation.py":
        "2b2555fac43a5914469a857b3a6bf19aa715ab6576220dc1dfd66dd808cad86e",
    "notes/clean-pair-cap-exact-descent-target.md":
        "90f49ac4fde9b793409d9081977e7a7135ebd76c1b5df5d699387d142c2b9b75",
    "computations/verify_clean_pair_cap_exact_descent_target.py":
        "263e8cc2fad4143803e0ce88d248c44a085a271b2d1569de86410c4448a47659",
    "notes/full-27-colon-cycle-macaulay-transfer-gap.md":
        "b1bfb66a7078cbee813aaf1b2d9a4fca5094329bcfcfb76827a75388a1e0dbdf",
    "computations/verify_full_27_colon_cycle_guard.py":
        "3beaaee3cae98ef342f98ad9ffbbd5e26f83721b91d7efb2d36130065a637567",
    "notes/odd-covariant-filtered-hankel-naturality-obstruction.md":
        "2ce57e3a1b30366831333ffcbf7ff7a0210c0b9db40ce60c9c8d6318ed9010f9",
    "computations/verify_odd_covariant_filtered_hankel_naturality_obstruction.py":
        "14727acc7d03240ef74c058a9a13a919db6dfeb81af07be4087a7a0c2e1bd50b",
}
EXPECTED_LEDGER_SHA256 = "eb09bb5f826383e53b85d9309254ba04806244da1b74407a598be1491dfe04bf"


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    a = [list(map(Fraction, row)) for row in matrix]
    rows = len(a)
    cols = len(a[0])
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if a[row][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        scale = a[rank][col]
        a[rank] = [entry / scale for entry in a[rank]]
        for row in range(rows):
            if row == rank or not a[row][col]:
                continue
            multiple = a[row][col]
            a[row] = [
                entry - multiple * pivot_entry
                for entry, pivot_entry in zip(a[row], a[rank], strict=True)
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def sym_power_sl2(degree: int) -> tuple[list[list[Fraction]], ...]:
    """Matrices H,E,F on x^(degree-i)y^i, with columns as inputs."""
    size = degree + 1
    h_mat = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    e_mat = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    f_mat = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        h_mat[i][i] = degree - 2 * i
        if i:
            e_mat[i - 1][i] = i
        if i < degree:
            f_mat[i + 1][i] = degree - i
    return h_mat, e_mat, f_mat


def intertwiner_dimension(domain_degree: int, codomain_degree: int) -> int:
    """Solve A X_domain = X_codomain A for the three sl2 generators."""
    domain_size = domain_degree + 1
    codomain_size = codomain_degree + 1
    variables = domain_size * codomain_size

    def variable(row: int, col: int) -> int:
        return row * domain_size + col

    equations: list[list[Fraction]] = []
    domain_actions = sym_power_sl2(domain_degree)
    codomain_actions = sym_power_sl2(codomain_degree)
    for x_domain, x_codomain in zip(
            domain_actions, codomain_actions, strict=True):
        for row in range(codomain_size):
            for col in range(domain_size):
                equation = [Fraction(0) for _ in range(variables)]
                # (A X_domain)_(row,col)
                for middle in range(domain_size):
                    equation[variable(row, middle)] += x_domain[middle][col]
                # -(X_codomain A)_(row,col)
                for middle in range(codomain_size):
                    equation[variable(middle, col)] -= x_codomain[row][middle]
                equations.append(equation)
    return variables - matrix_rank(equations)


def naturality_audit() -> dict[str, object]:
    rootless_dimensions = {}
    local_degree_dimensions = {}
    for h in range(3, 9):
        rootless_dimensions[h] = intertwiner_dimension(5, 2 * h - 1)
        local_degree_dimensions[h] = intertwiner_dimension(h, 3)
    require(rootless_dimensions[3] == 1
            and all(rootless_dimensions[h] == 0 for h in range(4, 9)),
            ("rootless sl2 Hom dimensions changed", rootless_dimensions))
    require(local_degree_dimensions[3] == 1
            and all(local_degree_dimensions[h] == 0 for h in range(4, 9)),
            ("local-degree sl2 Hom dimensions changed",
             local_degree_dimensions))
    return {
        "Hom_SL2_Sym5_to_Sym2hminus1": rootless_dimensions,
        "Hom_SL2_Symh_to_Sym3": local_degree_dimensions,
        "general_reason": (
            "a nonzero map between irreducible binary symmetric powers "
            "must preserve the unique highest weight, hence their degrees"
        ),
        "smallest_missing_rootless_input": (
            "a source-derived clean-line covariant of order 2h-6 together "
            "with the full common-Hankel compatibility, or directly Tr_h"
        ),
    }


def ghz_words(site_count: int) -> set[tuple[int, ...]]:
    return {tuple([colour] * site_count) for colour in range(3)}


def spectator_target_audit() -> dict[str, object]:
    counts = {}
    for h in range(3, 9):
        spectator_pairs = h - 3
        suspended = set()
        for core_colour in range(3):
            for pair_colours in product(range(3), repeat=spectator_pairs):
                word = [core_colour] * 8
                for colour in pair_colours:
                    word.extend([colour, colour])
                suspended.add(tuple(word))
        target = ghz_words(2 * h + 2)
        counts[h] = {
            "suspended_word_count": len(suspended),
            "ghz_word_count": len(target),
            "off_target_word_count": len(suspended - target),
        }
        require(len(suspended) == 3 ** (h - 2), ("spectator count", h))
        require(len(target) == 3, ("GHZ count", h))
        if h == 3:
            require(suspended == target, "h=3 target changed")
        else:
            require(suspended != target and suspended - target,
                    ("spectator product unexpectedly preserved GHZ", h))

    # A single disjoint two-site block B cannot solve Delta_8 tensor B =
    # Delta_10.  For each B_ij, different core colours demand inconsistent
    # values whenever i=j.
    demanded_values: dict[tuple[int, int], set[int]] = {
        (i, j): set() for i in range(3) for j in range(3)
    }
    for core_colour in range(3):
        for i in range(3):
            for j in range(3):
                desired = int(i == j == core_colour)
                demanded_values[(i, j)].add(desired)
    conflicts = {
        str(index): sorted(values)
        for index, values in demanded_values.items()
        if len(values) > 1
    }
    require(conflicts == {
        "(0, 0)": [0, 1],
        "(1, 1)": [0, 1],
        "(2, 2)": [0, 1],
    }, ("disjoint spectator block obstruction changed", conflicts))
    return {
        "word_counts": counts,
        "single_disjoint_pair_block_conflicts": conflicts,
        "static_fixed_word_tensoring_is_chain_valid": True,
        "static_tensoring_preserves_full_GHZ_target": False,
    }


Edge = tuple[int, int]


def normalized_edge(edge: Edge) -> Edge:
    a, b = edge
    require(a != b, ("loop", edge))
    return (a, b) if a < b else (b, a)


def hafnian(vertices: tuple[int, ...],
            edges: dict[Edge, Fraction]) -> Fraction:
    if not vertices:
        return Fraction(1)
    first = vertices[0]
    total = Fraction(0)
    for position in range(1, len(vertices)):
        second = vertices[position]
        weight = edges.get(normalized_edge((first, second)), Fraction(0))
        if not weight:
            continue
        remaining = vertices[1:position] + vertices[position + 1:]
        total += weight * hafnian(remaining, edges)
    return total


def cap_base_change_audit() -> dict[str, object]:
    vertices = tuple(range(8))
    x = {
        (0, 1): Fraction(1),
        (2, 3): Fraction(1),
        (4, 5): Fraction(1),
        (6, 7): Fraction(1),
    }
    r = {
        (0, 2): Fraction(1),
        (1, 3): Fraction(1),
    }
    s = Fraction(1)

    # [(s+r)exp(x)]_U: either the direct cap scalar s is used, or one
    # response edge r is used and x matches the remaining six sites.
    capped_top = s * hafnian(vertices, x)
    response_top = Fraction(0)
    for edge, weight in r.items():
        remaining = tuple(vertex for vertex in vertices if vertex not in edge)
        response_top += weight * hafnian(remaining, x)
    capped_top += response_top

    y = dict(x)
    for edge, weight in r.items():
        y[edge] = y.get(edge, Fraction(0)) + weight / s
    effective_pair_top = s * hafnian(vertices, y)
    clean_error = effective_pair_top - capped_top

    require(hafnian(vertices, x) == 1, "x matching changed")
    require(response_top == 0, "response top changed")
    require(capped_top == 1, ("capped top changed", capped_top))
    require(effective_pair_top == 2,
            ("effective-pair top changed", effective_pair_top))
    require(clean_error == 1, ("clean error changed", clean_error))
    return {
        "capped_top": int(capped_top),
        "canonical_effective_pair_top": int(effective_pair_top),
        "higher_cap_error": int(clean_error),
        "first_failed_square": (
            "two-site cap/evaluation followed by canonical pair reduction "
            "does not equal pair reduction followed by the h=3 comparison"
        ),
        "missing_condition": (
            "E_pq(K)=0 with s*kappa_0*kappa_1*kappa_2 nonzero, exactly the "
            "active-clean hypothesis consumed by SP-DESCENT"
        ),
    }


def source_scope_guards() -> dict[str, object]:
    master = (ROOT / (
        "notes/h3-reduced-eq-integral-rho-comparison-master-gate.md"
    )).read_text()
    master_checker = (ROOT / (
        "computations/verify_h3_reduced_eq_integral_rho_comparison_master_gate.py"
    )).read_text()
    uniform = (ROOT / (
        "notes/uniform_adjacent_cycle_filtered_prolongation.md"
    )).read_text()
    descent = (ROOT / (
        "notes/clean-pair-cap-exact-descent-target.md"
    )).read_text()
    full27 = (ROOT / (
        "notes/full-27-colon-cycle-macaulay-transfer-gap.md"
    )).read_text()
    require("At h=3" in master_checker
            and "one rho-equivariant k[beta]-linear comparison" in master,
            "master lost literal h=3 scope")
    require(r"site suspension of the hypothetical \(h=3\) row does not prove"
            in uniform
            and r"\rho_{2h-6}\in\operatorname {Sym}^{2h-6}U" in uniform,
            "uniform suspension guard changed")
    require("necessary and sufficient for the canonical" in descent
            and "The higher-cumulant error (4) is essential" in descent,
            "clean cap/base-change criterion changed")
    require("The construction suspends uniformly to every" in full27
            and "Establishing its source compatibility is the remaining"
            in full27,
            "full-27 static suspension scope changed")
    return {
        "literal_master": "h=3 only",
        "static_suspension": "proved for a fixed-word colon cycle",
        "arbitrary_source_naturality": False,
        "common_Hankel_transfer_Tr_h": False,
        "local_restriction_without_active_cleanliness": False,
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    ledger = {
        "theorem": "pointed h3 spectator uniformization no-go",
        "pins": PINS,
        "source_scope": source_scope_guards(),
        "spectator_target": spectator_target_audit(),
        "sl2_naturality": naturality_audit(),
        "local_cap_base_change": cap_base_change_audit(),
        "sharp_verdict": (
            "The h=3 pointed comparison does not functorially imply "
            "PAComp(h) through parameter-trivial spectator matching, bare "
            "divided powers, or canonical local eight-site restriction. "
            "A positive uniformization needs new order-dependent physical "
            "source data: at minimum a source-derived clean-line covariant/"
            "common-Hankel transfer, plus an all-branch chain comparison; "
            "using local pair elimination instead assumes active cleanliness "
            "and is therefore circular."
        ),
        "not_ruled_out": [
            "a nonlinear source-dependent covariant carrying order 2h-6",
            "a direct all-h pointed comparison constructed before evaluation",
            "a local restriction theorem that independently proves each "
            "required clean cap rather than assuming it",
        ],
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("uniformization ledger changed", digest))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    print("h3 -> all-h spectator uniformization: NO")
    print("fixed-word divided-power suspension: STATIC ONLY")
    print("parameter-natural rootless prolongation: Hom_SL2 = 0")
    print("local eight-site restriction: CIRCULAR THROUGH ACTIVE CLEANNESS")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

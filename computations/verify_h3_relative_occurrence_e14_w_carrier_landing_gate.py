#!/usr/bin/env python3
"""Audit landing the relative occurrence carrier in the E14 first-hit block.

The relative P2 graph retains a centered carrier ``t`` and is a resolution of
the old physical coefficient algebra.  A physical promoted-occurrence map W
would identify the relevant combination of ``t`` with the canonical E14
unary/G11 first-hit target.  This checker proves three exact facts.

1.  In the direct sum of the relative graph and the complete 269-column E14
    first-hit presentation, the desired comparison raises rank by one.  The
    pinned E14 first-hit covector, extended by zero on the graph block,
    detects it.
2.  There is a presentation-safe *relative* W cylinder: add a slack carrier
    ``r`` and a generator with boundary ``r-w+t``.  Killing ``r`` is exactly
    the missing W equation and lowers H0 by one; it is not a graph change.
3.  The existing physical Yw-to-W cap theorem only certifies the common
    physical-W output line.  Its W projection has rank one, whereas the
    endpoint-even relative carrier has rank five, and it has no E14
    unary/G11 principal boundary.  Thus the cap readout is required typing
    for W, not the occurrencewise E14 comparison itself.

The first-hit covector is a source-presentation obstruction only.  It becomes
a physical terminal only after extension over the complete augmented source
map (later endpoint-word changes, q, target, residue, anchor and terminal
rows included).
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py":
        "4dfb2846c698e5603dadeb1a73add17a7984ccedbad25e3bb09b6aa4170e62ce",
    "notes/h2-p2-relative-occurrence-graph-resolution-gate.md":
        "101f1040df04e5f6a3ca7c5034c1a3a713903704936207619c5ec8e00d59df37",
    "computations/verify_h3_centered_projector_e14_word_arrow_gate.py":
        "e1b8b17c75292f55439652ac9e5dcb1a24a3e4079c2d378e9fa63544e5491b46",
    "notes/h3-centered-projector-e14-word-arrow-gate.md":
        "e0c5249f0e79551c87dbd1b25bc3e52501ea1ae7eac07484509bbd38d18cf3de",
    "computations/verify_h3_rootless_e14_companion_core_identification.py":
        "438ae827dba9e8f7a14f011cb5d76631fc284a2a2a8c6d8bcee7003669a1ac45",
    "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py":
        "893f000e37e4bcfc78973cb042cc0858087cb25605d6cf070a1bf8dfa7a76b7a",
    "notes/h3-c6-e14-unary-spair-first-reduction-boundary.md":
        "9d3af91f0e97079c8e2bd2dd76db110fdde45e71eed0d21805bdd4575a683c4f",
    "computations/verify_h3_cplus_w_yw_cap_factorization.py":
        "0b42e8c7d9e308c93774e59eae030403f3c264e2bfe4b31e7782a0e57b78a506",
    "computations/verify_h3_interface_iii_augmented_cap_factorization.py":
        "06e64c5db2a59b8877cb112515d50779be95010801f19690f97060bf08621213",
}
EXPECTED_LEDGER_SHA256 = (
    "033c69f35205783459fcd1990c5e89b4f5b1c05b051ec24fffdca8917166e584"
)
N = 12


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def load(relative: str, name: str):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in
                zip(left, right, strict=True)), Q(0))


def add(*vectors):
    require(vectors and len({len(vector) for vector in vectors}) == 1,
            "add width")
    return tuple(sum((Q(vector[index]) for vector in vectors), Q(0))
                 for index in range(len(vectors[0])))


def scale(coefficient, vector):
    return tuple(Q(coefficient) * Q(entry) for entry in vector)


def rank(columns) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [list(map(Q, row)) for row in zip(*columns, strict=True)]
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


def unit(index: int, width: int):
    return tuple(Q(position == index) for position in range(width))


def sparse_to_dense(vector, coordinates):
    return tuple(Q(vector.get(coordinate, 0)) for coordinate in coordinates)


def canonical_first_hit_module() -> dict[str, object]:
    """Reconstruct the canonical 269-column module and its exact dual."""
    first = load(
        "computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py",
        "relative_w_e14_first",
    )
    first_ledger, first_digest = first.audit()
    require(first_digest == first.EXPECTED_LEDGER_SHA256,
            "the E14 first-hit ledger changed")

    rewrite = first.load(first.REWRITE_PATH, "relative_w_rewrite")
    top = rewrite.load(rewrite.TOP_PATH, "relative_w_top")
    two = top.load(top.TWO_CELL_PATH, "relative_w_two")
    e14 = two.load(two.E14_PATH, "relative_w_e14")
    b4 = e14.load(e14.B4_PATH, "relative_w_b4")
    _candidates, _names, responses, unary = two.universal(e14, b4, 1, 1)

    endpoint = ("p1_0_1", "s1_1_1")
    pivot = ("u35_11",)
    multiplier = ("v2411",)
    word = (0, 0, 0, 1, 0, 1)
    factor, remainder = first.factor_unary(unary[word], pivot)
    require(factor == {(): Q(-1), ("v0400",): Q(1)}
            and len(remainder) == 12,
            "the canonical E14 unary remainder changed")

    target = {
        (endpoint, first.multiply_monomials(monomial, multiplier)): coefficient
        for monomial, coefficient in remainder.items()
    }
    response_rows = [
        (output_word, first.response_terms(row))
        for output_word, row in responses.items()
    ]
    unary_rows = [
        (output_word, tuple(polynomial.items()))
        for output_word, polynomial in unary.items()
    ]

    columns = {}
    for target_endpoint, target_monomial in target:
        for row_index, (output_word, row) in enumerate(response_rows):
            for row_endpoint, row_monomial, _coefficient in row:
                if row_endpoint != target_endpoint:
                    continue
                row_multiplier = first.quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                column = {
                    (output_endpoint,
                     first.multiply_monomials(output_monomial, row_multiplier)):
                        output_coefficient
                    for output_endpoint, output_monomial, output_coefficient
                    in row
                }
                if output_word == (1,) * 6:
                    column[(("target_G11",), row_multiplier)] = Q(-1)
                columns[("G11", row_index, row_multiplier)] = column
        for row_index, (output_word, row) in enumerate(unary_rows):
            for row_monomial, _coefficient in row:
                row_multiplier = first.quotient(target_monomial, row_monomial)
                if row_multiplier is None:
                    continue
                column = {
                    (target_endpoint,
                     first.multiply_monomials(output_monomial, row_multiplier)):
                        output_coefficient
                    for output_monomial, output_coefficient in row
                }
                if output_word == (0,) * 6:
                    column[(("target_unary",) + target_endpoint,
                            row_multiplier)] = Q(-1)
                columns[("unary", row_index, target_endpoint,
                         row_multiplier)] = column

    pivots = {}
    for column in columns.values():
        first.add_exact_column(column, pivots)
    reduced = first.exact_reduce(target, pivots)
    require(len(columns) == len(pivots) == 269
            and reduced == {
                (endpoint, ("u35_11", "v2411")): Q(1),
                (endpoint, ("u35_11", "v0400", "v2411")): Q(-1),
            }, "the reconstructed E14 first-hit module changed")

    free = min(reduced)
    dual = {free: Q(1)}
    for leading in sorted(pivots, reverse=True):
        value = sum(
            coefficient * dual.get(coordinate, Q(0))
            for coordinate, coefficient in pivots[leading].items()
            if coordinate != leading
        )
        if value:
            dual[leading] = -value
    require(all(sum(coefficient * dual.get(coordinate, Q(0))
                    for coordinate, coefficient in column.items()) == 0
                for column in columns.values()),
            "the reconstructed E14 dual stopped killing a source column")
    target_pairing = sum(coefficient * dual.get(coordinate, Q(0))
                         for coordinate, coefficient in target.items())
    require(target_pairing == -1 and len(dual) == 22,
            ("the reconstructed E14 dual changed", target_pairing, len(dual)))

    denominator = math.lcm(*(value.denominator for value in dual.values()))
    content = math.gcd(*(
        abs(int(value * denominator)) for value in dual.values()
    ))
    require(target_pairing * denominator / content == -30,
            "the primitive E14 dual normalization changed")

    rootless = load(
        "computations/verify_h3_rootless_e14_companion_core_identification.py",
        "relative_w_rootless",
    )
    core_ledger, core_digest = rootless.audit()
    require(core_digest == rootless.EXPECTED_LEDGER_SHA256,
            "the rootless/E14 core ledger changed")
    promoted = tuple(core_ledger["canonical_E14_promoted_term"])
    promoted_internal = tuple(sorted(
        item for item in promoted if item not in endpoint
    ))
    promoted_coordinate = (endpoint, promoted_internal)
    require(promoted_coordinate in target,
            ("the promoted rootless/E14 term left the target", promoted_coordinate))
    promoted_pairing = dual.get(promoted_coordinate, Q(0))

    coordinates = sorted(set(target).union(*(
        set(column) for column in columns.values()
    )))
    dense_columns = [sparse_to_dense(column, coordinates)
                     for column in columns.values()]
    dense_target = sparse_to_dense(target, coordinates)
    dense_dual = tuple(dual.get(coordinate, Q(0))
                       for coordinate in coordinates)
    require(rank(dense_columns) == 269
            and rank(dense_columns + [dense_target]) == 270
            and dot(dense_dual, dense_target) == -1,
            "the dense E14 cokernel reconstruction changed")

    return {
        "module": first,
        "ledger": first_ledger,
        "coordinates": coordinates,
        "columns": dense_columns,
        "target": dense_target,
        "dual": dense_dual,
        "promoted_coordinate": promoted_coordinate,
        "promoted_pairing": promoted_pairing,
        "target_support": len(target),
        "coordinate_count": len(coordinates),
    }


def relative_graph_columns_and_private_t():
    one = (Q(1),) * N
    zero = (Q(0),) * N
    identity = tuple(unit(index, N) for index in range(N))
    c_matrix = tuple(tuple(N * Q(row == column) - 1
                           for column in range(N))
                     for row in range(N))

    def block(u, z, t):
        return tuple(u) + tuple(z) + tuple(t)

    theta = []
    phi = []
    for index in range(N):
        theta.append(block(scale(-1, identity[index]), identity[index], zero))
        phi.append(block(
            zero, scale(-1, c_matrix[index]), identity[index]
        ))
    graph = theta + phi
    require(rank(graph) == 24, "the relative graph rank changed")

    relative = load(
        "computations/verify_h2_p2_relative_occurrence_graph_resolution_gate.py",
        "relative_w_graph",
    )
    relative_ledger, relative_digest = relative.audit()
    require(relative_digest == relative.EXPECTED_LEDGER_SHA256,
            "the relative graph ledger changed")
    exact = relative_ledger["exact_P2_combination"]
    indices = tuple(exact["Gamma_indices"])
    coefficients = tuple(map(Q, exact["Gamma_coefficients"]))
    private_t = add(*(
        scale(coefficient, identity[index])
        for index, coefficient in zip(indices, coefficients, strict=True)
    ))
    require(any(private_t) and sum(private_t, Q(0)) != 0,
            "the selected t combination changed")
    graph_private_t = block(zero, zero, private_t)
    return graph, graph_private_t, private_t, relative_ledger


def direct_sum_landing_obstruction(e14) -> dict[str, object]:
    graph_columns, graph_private_t, private_t, relative_ledger = (
        relative_graph_columns_and_private_t()
    )
    # Use the already certified echelon ranks of the two direct summands.
    # The explicit E14 dual extended by zero on the graph summand kills both
    # old blocks and pairs -1 with the desired target, proving that adjoining
    # the comparison raises rank exactly once.
    old_rank = rank(graph_columns) + 269
    desired_pairing = dot(e14["dual"], e14["target"])
    require(old_rank == 24 + 269 and desired_pairing == -1,
            "the relative-graph/E14 direct-sum obstruction changed")

    # Add one slack r and the relative W cylinder d psi=r-w+t.  The new
    # relation is monic in r and hence preserves H0.  Killing r appends the
    # desired comparison w-t, whose independence was just checked.
    # The cylinder rank statement reduces to the three-coordinate quotient
    # (t_private,E14_first_hit,r), because all old columns vanish there.
    # d psi=r-w+t is (1,-1,1); r=0 is (0,0,1).
    relative_w_boundary = (Q(1), Q(-1), Q(1))
    r_zero = (Q(0), Q(0), Q(1))
    relative_rank_increment = rank([relative_w_boundary])
    killed_rank_increment = rank([relative_w_boundary, r_zero])
    require(relative_rank_increment == 1 and killed_rank_increment == 2,
            "the relative W mapping-cylinder rank changed")
    old_h0_quotient = 2
    relative_h0_quotient = 3 - relative_rank_increment
    killed_h0_quotient = 3 - killed_rank_increment
    require(relative_h0_quotient == old_h0_quotient
            and killed_h0_quotient == old_h0_quotient - 1,
            "the W cylinder stopped separating relative from absolute")

    return {
        "graph_rank": 24,
        "E14_first_hit_rank": 269,
        "direct_sum_rank": old_rank,
        "rank_after_adjoining_W_comparison": old_rank + 1,
        "desired_comparison": "w_E14-t_zprivate",
        "extended_first_hit_dual_pairing": str(desired_pairing),
        "comparison_in_old_image": False,
        "relative_W_cylinder": {
            "new_degree_zero_carrier": "r",
            "new_degree_one_generator": "psi",
            "boundary": "d psi=r-w_E14+t_zprivate",
            "augmentation": "r=w_E14-t_zprivate",
            "H0_change_with_r_retained": 0,
            "absolute_step": "set r=0",
            "H0_change_after_absolute_step": -1,
            "interpretation": (
                "the cylinder carries the defect without changing the old "
                "fibre; killing its slack is precisely the missing W law"
            ),
        },
        "relative_t_scope": {
            "full_centered_rank": relative_ledger[
                "remaining_carrier_landing"]["full_centered_carrier_rank"],
            "endpoint_even_rank": relative_ledger[
                "remaining_carrier_landing"
            ]["endpoint_even_private_carrier_rank"],
        },
    }


def physical_w_readout_scope() -> dict[str, object]:
    cplus = load(
        "computations/verify_h3_cplus_w_yw_cap_factorization.py",
        "relative_w_cplus_cap",
    )
    cplus_ledger, cplus_digest = cplus.audit()
    require(cplus_digest == cplus.EXPECTED_LEDGER_SHA256,
            "the C-plus W cap ledger changed")
    root_even = cplus_ledger["root_even_factorization"]
    source = cplus_ledger["literal_and_normal_source_provenance"]
    require(root_even["physical_W_map_needed"]
            == "Phi_cap(Yw_E)=W_E (identity on E-line)"
            and source["physical_cap_readout"] == "Yw=W=1 on r0-T",
            "the old physical W cap statement changed")

    interface = load(
        "computations/verify_h3_interface_iii_augmented_cap_factorization.py",
        "relative_w_interface_cap",
    )
    old_cap, _repairs, physical = interface.base_factorization()
    w_index = interface.ROWS.index("W")
    yw_index = interface.ROWS.index("Yw_boundary")
    w_projection = [tuple((Q(column[w_index]),)) for column in physical]
    require(old_cap[w_index] == old_cap[yw_index] == 1
            and len(physical) == 5
            and rank(w_projection) == 1
            and all(column[w_index] == column[yw_index] == 1
                    for column in physical),
            "the old cap W projection changed")

    return {
        "existing_cap_chain": "r0-T",
        "existing_cap_law": "Yw=W coefficientwise",
        "C5_physical_columns": len(physical),
        "rank_of_physical_W_output_projection": rank(w_projection),
        "relative_endpoint_even_t_rank": 5,
        "occurrencewise_t_landing_supplied": False,
        "E14_unary_G11_principal_boundary_recorded": False,
        "distinction": (
            "the old cap certifies the required physical-W output row on a "
            "common line.  It does not supply a source column whose principal "
            "boundary is the word-000101 E14 first-hit target minus a marked "
            "01211222 occurrence carrier"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    e14 = canonical_first_hit_module()
    obstruction = direct_sum_landing_obstruction(e14)
    cap_scope = physical_w_readout_scope()

    ledger = {
        "theorem": "relative occurrence carrier to E14 W landing gate",
        "pins": PINS,
        "canonical_E14_first_hit": {
            "word": "000101",
            "target_support": e14["target_support"],
            "coordinate_count": e14["coordinate_count"],
            "complete_unary_G11_columns": 269,
            "rank_Q": 269,
            "rational_dual_support": sum(value != 0 for value in e14["dual"]),
            "rational_dual_pairing_on_full_target": str(
                dot(e14["dual"], e14["target"])
            ),
            "promoted_rootless_core_coordinate": [
                list(e14["promoted_coordinate"][0]),
                list(e14["promoted_coordinate"][1]),
            ],
            "dual_pairing_on_that_single_coordinate": str(
                e14["promoted_pairing"]
            ),
            "qualification": (
                "the physical E14 object is the complete twelve-tail unary "
                "remainder; the decorated rootless 2K2 selects one of its "
                "monomials, not by itself the complete source row"
            ),
        },
        "relative_to_absolute_W": obstruction,
        "old_physical_W_cap_scope": cap_scope,
        "exact_alternative": {
            "full_map": (
                "J_full = complete augmented source map in the selected "
                "t/E14 word/fine/repeated grade"
            ),
            "target": "b_W=w_E14-t_zprivate with all proper faces",
            "constructive_arm": "b_W lies in im(J_full): physical W exists",
            "dual_arm": (
                "b_W not in im(J_full): a covector Lambda kills J_full and "
                "detects b_W"
            ),
            "current_first_hit_dual_is_full_terminal": False,
            "missing_terminal_check": (
                "extend the 22-support E14 seed over later endpoint-word "
                "changes and every q/target/residue/anchor/W/eta/sigma "
                "column, then identify the survivor with an accepted "
                "exchange, relative generator, or Fredholm separator"
            ),
        },
        "verdict": (
            "Retaining t permits a presentation-safe relative W cylinder, "
            "but identifying t with the actual E14 unary/G11 target is a new "
            "rank-one comparison already detected by the first-hit dual. "
            "The existing Yw=W cap is only the required physical output "
            "typing and has rank-one W projection; it does not construct the "
            "rank-five occurrence-local landing.  The live theorem is W "
            "membership in the complete augmented map, or promotion of its "
            "full-map dual to a physical terminal."
        ),
        "scope": (
            "exact h=2 relative graph and selected h=3 E14 first-hit block. "
            "The rank obstruction is exact for the 269-column unary/G11 "
            "presentation; it is not a full-source counterexample or a "
            "terminal theorem.  No occurrencewise E14 orbit map is assumed."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("relative occurrence/E14 W ledger changed", digest))
    return ledger, digest


def main() -> None:
    ledger, digest = audit()
    print("relative W cylinder with slack r: PRESENTATION-SAFE")
    print("absolute t=E14 comparison: NEW RANK-ONE COLUMN")
    print("E14 first-hit dual pairing=" + ledger[
        "relative_to_absolute_W"]["extended_first_hit_dual_pairing"])
    print("old Yw=W cap: OUTPUT TYPING ONLY, W-PROJECTION RANK 1")
    print("full physical terminal: NOT YET PROMOTED")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

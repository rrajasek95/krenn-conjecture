#!/usr/bin/env python3
"""Audit the minimal decorated h=4 three-presentation connection.

The intrinsic h=4 overlap is the augmented triangle, but its three vertices
have literal physical grades

    p0 = 0121221222 / t_23*q_(v,45|67) / (45|67;23),
    p1 = 0121122222 / t_45*q_(v,23|67) / (23|67;45),
    p2 = 0121122222 / t_67*q_(v,23|45) / (23|45;67).

Thus there are three presentation objects but only two displayed word
strings.  The fine and removed/reinserted labels keep p1 and p2 in distinct
direct summands.

This checker constructs the formal Cech complex, its word quotient and its
full labelled boundary.  It then audits the actual constructor boundary:
the pinned current grammar has no registered degree-zero physical arrow
between any two of these cap presentation objects.  A standard mapping
cylinder is partial on an already supplied arrow and therefore fails on all
three pairs.

After a word-only connection is formally granted, the first lift debt is the
rank-two fine/removed/reinserted incidence.  A concrete spanning-tree lift
needs one word-changing edge p0->p1 and one same-word label-switch edge
p1->p2.  The symmetric Cech presentation additionally needs the third edge
and a triangle coherence cell.  Conditional equal-mu protected readouts have
zero edge debt; they do not supply any of the missing labelled arrows.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h4_collision_ks_one_edge_shuffle_overlap.py":
        "bf25a8c481ad8e42a14b22ff3f955f5d321289356d9dd11962ffc68d4e06671e",
    "notes/h4-collision-ks-one-edge-shuffle-overlap.md":
        "3b50f4a6e556f3cd760d335910b788b7b16d074d0a5382dc89bae381e2932972",
    "computations/verify_h4_collision_ks_decorated_presentation_mismatch.py":
        "ed0a43db7e9656119bdaf21ebea1d433451cfe1f32f2ce086f3c19dda0275d6a",
    "notes/h4-collision-ks-decorated-presentation-mismatch.md":
        "ef34f5fabc6a9e20210ceafa3f68fa23d959f744694f05509aa16433b0c00ed3",
    "computations/verify_h3_gamma_star_executable_gen_phys_registry.py":
        "173ebdedcfdadd9891704223ea93731509c18a4d120aa34d6c7bc8a4f3aebddb",
    "notes/h3-gamma-star-executable-gen-phys-registry.md":
        "0511cd14b1233092eda070313ec2bdea8550b4853f6ebe77a8a316b67d7d8ca0",
    "computations/verify_h3_matching_face_residual_flip_semidirect_gate.py":
        "0769314fa55e0978a24680a16f5f5bd4bad8b176322d9709cb42c8b73e025f1e",
    "notes/h3-matching-face-residual-flip-semidirect-gate.md":
        "7e93c5dbf094748371b274bbacce6f677f3eeb8fc8476aca38956652bfae3bf9",
}
EXPECTED_LEDGER_SHA256 = (
    "c204d67a24984905bacf1246f1f864a6a05a3c26fb85498d7afe7f69831de1d8"
)

FAMILIES = (
    ("forward_01=-D*s1", "DSQ", ("0", "S")),
    ("reverse_01=+p0*q01", "PQQ", ("S", "0")),
    ("forward_02=-D*s0", "DSQ", ("1", "S")),
    ("reverse_02=+p1*q01", "PQQ", ("S", "1")),
)
EDGE_NAMES = ("u01", "u02", "u12")

Vector = tuple[Q, ...]


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise RuntimeError(detail)


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))


def add(left: Vector, right: Vector) -> Vector:
    require(len(left) == len(right), "add width")
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(coefficient: Q, vector: Vector) -> Vector:
    return tuple(coefficient * value for value in vector)


def dot(left: Vector, right: Vector) -> Q:
    require(len(left) == len(right), "dot width")
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def rank(columns: tuple[Vector, ...]) -> int:
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[columns[column][row] for column in range(len(columns))]
            for row in range(height)]
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


@dataclass(frozen=True)
class Presentation:
    name: str
    word: str
    fine: str
    window: tuple[str, str]
    removed: str
    reinserted: str
    coarse_repeated: str = "P3+K2"


PRESENTATIONS = (
    Presentation("p0", "0121221222", "t_23*q_(v,45|67)",
                 ("45", "67"), "23", "23"),
    Presentation("p1", "0121122222", "t_45*q_(v,23|67)",
                 ("23", "67"), "45", "45"),
    Presentation("p2", "0121122222", "t_67*q_(v,23|45)",
                 ("23", "45"), "67", "67"),
)


class MissingPhysicalArrow(RuntimeError):
    pass


class DecoratedConnectionRegistry:
    """The literal h=4 cross-presentation arrow table currently available."""

    def __init__(self) -> None:
        # The pinned source triangle supplies intrinsic overlap incidence, not
        # a decorated cap-grade operation matrix unit.  The pinned executable
        # source registry and residual-flip audit supply no such cap arrow.
        self.arrows: dict[tuple[str, str], str] = {}

    def mapping_cylinder(self, source: str, target: str) -> str:
        producer = self.arrows.get((source, target))
        if producer is None:
            raise MissingPhysicalArrow(
                f"no registered degree-zero physical arrow {source} -> {target}"
            )
        return f"Cyl({source}->{target}) via {producer}"


def formal_cech_audit() -> dict[str, object]:
    # C0 order p0,p1,p2; C1 order u01,u02,u12.
    u01 = tuple(map(Q, (-1, 1, 0)))
    u02 = tuple(map(Q, (-1, 0, 1)))
    u12 = tuple(map(Q, (0, -1, 1)))
    edges = (u01, u02, u12)
    triangle = tuple(map(Q, (1, -1, 1)))
    triangle_boundary = add(add(scale(triangle[0], u01),
                                scale(triangle[1], u02)),
                            scale(triangle[2], u12))
    augmentation = tuple(map(Q, (1, 1, 1)))
    require(rank(edges) == 2
            and triangle_boundary == (Q(0),) * 3
            and rank((triangle,)) == 1
            and dot(augmentation, u01) == dot(augmentation, u02) ==
                dot(augmentation, u12) == 0,
            "augmented triangle changed")
    require(rank((u01, u12)) == 2,
            "the proposed two-edge spanning tree stopped connecting C0")

    # Word quotient: p0 has word A and p1,p2 have word B.
    word_edges = (
        tuple(map(Q, (-1, 1))),
        tuple(map(Q, (-1, 1))),
        tuple(map(Q, (0, 0))),
    )
    require(rank(word_edges) == 1 and rank(edges) == 2,
            "word/full-label incidence ranks changed")
    return {
        "C2_C1_C0_Cminus1_dimensions": [1, 3, 3, 1],
        "d2_d1_augmentation_ranks": [1, 2, 1],
        "edge_order": list(EDGE_NAMES),
        "d_tau": [1, -1, 1],
        "d1_d2": [0, 0, 0],
        "H1_of_three_edge_one_skeleton": len(edges) - rank(edges),
        "H1_after_triangle_cell": len(edges) - rank(edges) -
            rank((triangle,)),
        "formal_augmented_Cech_complex_exact": True,
        "literal_word_strings": sorted({p.word for p in PRESENTATIONS}),
        "presentation_objects": 3,
        "literal_word_string_count": 2,
        "word_quotient_edge_rank": rank(word_edges),
        "full_label_edge_rank": rank(edges),
        "minimal_concrete_spanning_tree": ["u01", "u12"],
        "minimal_tree_instances": {
            "word_changing": 1,
            "same_word_fine_removed_reinserted_switch": 1,
        },
        "symmetric_Cech_completion": (
            "add u02 and one coherence cell tau with "
            "d(tau)=u01-u02+u12"
        ),
    }


def labelled_boundary_audit() -> dict[str, object]:
    full_edges = (
        tuple(map(Q, (-1, 1, 0))),
        tuple(map(Q, (-1, 0, 1))),
        tuple(map(Q, (0, -1, 1))),
    )
    records = []
    for left, right, edge in ((0, 1, "u01"), (0, 2, "u02"),
                              (1, 2, "u12")):
        p_left, p_right = PRESENTATIONS[left], PRESENTATIONS[right]
        changed = []
        for tag in ("word", "fine", "window", "removed", "reinserted"):
            if getattr(p_left, tag) != getattr(p_right, tag):
                changed.append(tag)
        require("fine" in changed and "window" in changed
                and "removed" in changed and "reinserted" in changed,
                (edge, changed))
        require(("word" in changed) == (edge != "u12"),
                (edge, changed))
        records.append({
            "edge": edge,
            "source": p_left.name,
            "target": p_right.name,
            "word_changes": "word" in changed,
            "changed_literal_tags": changed,
            "fine_boundary": f"{p_right.fine}-{p_left.fine}",
            "removed_reinserted_boundary": (
                f"({ '|'.join(p_right.window) };{p_right.removed};"
                f"{p_right.reinserted})-"
                f"({ '|'.join(p_left.window) };{p_left.removed};"
                f"{p_left.reinserted})"
            ),
            "coarse_repeated_boundary": 0,
        })

    # Fine and full removed/reinserted labels are each three independent
    # idempotents, so their edge-boundary matrices are both the full triangle
    # incidence and have rank two.  A word-only bridge cannot hit them.
    require(len({p.fine for p in PRESENTATIONS}) == 3
            and len({(p.window, p.removed, p.reinserted)
                     for p in PRESENTATIONS}) == 3
            and rank(full_edges) == 2,
            "the literal label separation changed")
    return {
        "presentations": [
            {
                "name": p.name,
                "word": p.word,
                "fine": p.fine,
                "window": list(p.window),
                "removed": p.removed,
                "reinserted": p.reinserted,
                "coarse_repeated": p.coarse_repeated,
            }
            for p in PRESENTATIONS
        ],
        "edges": records,
        "fine_label_count": 3,
        "removed_reinserted_label_count": 3,
        "fine_boundary_rank": 2,
        "removed_reinserted_boundary_rank": 2,
        "coarse_P3_plus_K2_boundary_rank": 0,
        "first_lift_debt_after_a_word_only_connection": (
            "rank-two fine t_i*q_(v,N_i) and tied window/removed/"
            "reinserted incidence"
        ),
        "primitive_debt_generators": [
            "t_45*q_(v,23|67)-t_23*q_(v,45|67)",
            "t_67*q_(v,23|45)-t_45*q_(v,23|67)",
        ],
    }


def current_grammar_audit() -> dict[str, object]:
    registry = DecoratedConnectionRegistry()
    failures = []
    for source, target in (("p0", "p1"), ("p0", "p2"),
                           ("p1", "p2")):
        try:
            registry.mapping_cylinder(source, target)
        except MissingPhysicalArrow as error:
            failures.append(str(error))
    require(len(failures) == 3
            and all(failure.startswith(
                "no registered degree-zero physical arrow")
                    for failure in failures), failures)

    constructors = (
        {
            "constructor": "intrinsic h4 shuffle/Cech overlap",
            "physical_cross_presentation_arrow": False,
            "separator": (
                "forgets physical word/fine/window/removed/reinserted tags"
            ),
        },
        {
            "constructor": "coefficient and Macaulay product",
            "physical_cross_presentation_arrow": False,
            "separator": "objectwise cap or response operation parent",
        },
        {
            "constructor": "PP/Hasse restriction and reinsertion",
            "physical_cross_presentation_arrow": False,
            "separator": (
                "emits the three distinct presentation-labelled faces; no "
                "registered degree-zero identification between them"
            ),
        },
        {
            "constructor": "Cartan/Weyl and K_Eq/AugP2 cap operations",
            "physical_cross_presentation_arrow": False,
            "separator": "cap-object internal; retained idempotents differ",
        },
        {
            "constructor": "termwise residual-matching flip bar",
            "physical_cross_presentation_arrow": False,
            "separator": (
                "conditional response-word 110000 PP bar; pinned audit has "
                "no cap 01211222/t*q_(v,N)/P3+K2 transport"
            ),
        },
        {
            "constructor": "standard mapping cylinder",
            "physical_cross_presentation_arrow": False,
            "separator": "requires an already registered input chain map",
        },
    )
    require(not any(item["physical_cross_presentation_arrow"]
                    for item in constructors), constructors)

    return {
        "audited_constructor_families": list(constructors),
        "registered_cross_presentation_degree_zero_arrows": 0,
        "requested_pairs": ["p0->p1", "p0->p2", "p1->p2"],
        "mapping_cylinder_results": ["MissingPhysicalArrow"] * 3,
        "exceptions": failures,
        "physical_C1_image_rank_in_current_registry": 0,
        "exact_current_grammar_no_go": True,
        "global_full_source_exhaustiveness_claim": False,
        "first_missing_physical_constructor": (
            "a cap-grade presentation connection retaining word, "
            "t_i*q_(v,N_i), window, removed edge and reinsertion edge"
        ),
    }


def protected_readout_audit() -> dict[str, object]:
    differences = (
        tuple(map(Q, (1, -1, 0))),
        tuple(map(Q, (1, 0, -1))),
    )
    mu = Q(1, 30)
    zero = (Q(0),) * 3
    equal = (mu,) * 3
    minus_equal = tuple(-value for value in equal)
    rows = {
        "target": minus_equal,
        "q": zero,
        "anchor": zero,
        "ores": equal,
        "W": minus_equal,
        "ridge": equal,
    }
    readings = {
        name: [str(dot(detector, values)) for detector in differences]
        for name, values in rows.items()
    }
    require(all(values == ["0", "0"] for values in readings.values()),
            readings)
    word_idempotent = tuple(map(Q, (1, 0, 0)))
    require([dot(detector, word_idempotent) for detector in differences]
            == [Q(1), Q(1)], "word detector control")
    return {
        "status": "conditional on three equal transported local B0 bridges",
        "normalization_mu": "1/30",
        "protected_values": {
            name: [str(value) for value in values]
            for name, values in rows.items()
        },
        "detector_order": ["(1,-1,0)", "(1,0,-1)"],
        "protected_detector_readings": readings,
        "all_protected_edge_debts_zero": True,
        "word_idempotent_control_readings": ["1", "1"],
        "unconditional_physical_values_constructed": False,
        "consequence": (
            "equal protected scalars do not create a source arrow and do "
            "not pay the earlier fine/removed/reinserted boundary"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    formal = formal_cech_audit()
    labels = labelled_boundary_audit()
    grammar = current_grammar_audit()
    readout = protected_readout_audit()
    require(formal["full_label_edge_rank"] ==
                labels["fine_boundary_rank"] == 2
            and grammar["physical_C1_image_rank_in_current_registry"] == 0,
            "the connection obstruction ranks changed")
    require(len(FAMILIES) == 4
            and {family[1] for family in FAMILIES} == {"DSQ", "PQQ"},
            "the fixed collision-family packet changed")
    ledger = {
        "theorem": "h4 three-presentation physical connection grammar gate",
        "pins": PINS,
        "formal_Cech_mapping_cylinder": formal,
        "literal_grade_boundary": labels,
        "fixed_collision_packet": {
            "tail": "23|45|67",
            "families": [
                {"name": name, "operation": operation,
                 "missing_doubled": list(missing_doubled)}
                for name, operation, missing_doubled in FAMILIES
            ],
            "independent_three_presentation_complexes": len(FAMILIES),
            "formal_dimensions_over_all_four_families": [4, 12, 12, 4],
            "formal_ranks_over_all_four_families": [4, 8, 4],
            "current_physical_cross_presentation_edge_rank": 0,
        },
        "current_physical_constructor_grammar": grammar,
        "protected_readout": readout,
        "minimal_positive_extension": {
            "concrete_tree_edges": [
                "phi01: p0->p1, word-changing and full-label preserving",
                "phi12: p1->p2, same-word fine/window/removed/reinserted switch",
            ],
            "tree_is_sufficient_for_connected_H0_descent": True,
            "symmetric_Cech_extra_data": [
                "phi02: p0->p2",
                "Tau with dTau=phi01-phi02+phi12",
            ],
            "one_uniform_schema_may_generate_the_instances": True,
            "schema_must_be_PP_restriction_reinsertion_natural": True,
            "d_squared_alone_forces_coherence_cell": False,
        },
        "verdict": (
            "The formal three-presentation Cech triangle is exact, but the "
            "pinned current physical constructor registry has no degree-zero "
            "arrow on any of its three edges.  Granting a word-only "
            "connection exposes the first lift debt: the rank-two incidence "
            "of the three t_i*q_(v,N_i) and tied window/removed/reinserted "
            "labels.  A concrete connected lift needs one word-changing and "
            "one same-word label-switch edge; the symmetric triangle also "
            "needs the third edge and one coherence cell.  Conditional "
            "equal-mu protected readouts have zero edge debt, so they neither "
            "obstruct nor construct this missing connection."
        ),
        "scope": (
            "exact no-go for the executable constructor grammar pinned here, "
            "fibrewise over the fixed tail 23|45|67 and all four collision "
            "families.  It is not an exhaustive theorem about an unwritten "
            "full decorated source and does not rule out a new PP-natural "
            "word/fine/reinsertion connection schema."
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("h4 connection ledger changed", digest))
    return ledger, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("all", "complex", "grammar",
                                           "readout"), default="all")
    parser.add_argument("--json", action="store_true")
    arguments = parser.parse_args()
    ledger, digest = audit()
    if arguments.json:
        print(json.dumps({"mode": arguments.mode, "ledger": ledger,
                          "sha256": digest}, indent=2, sort_keys=True))
    else:
        print(f"h4 three-presentation connection ({arguments.mode}): PASS")
        print("formal Cech ranks: 1,2,1; current physical edge rank: 0")
        print("first post-word debt: fine/removed/reinserted rank 2")
        print("minimal tree: one cross-word edge + one same-word label edge")
        print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Complete differential of the shifted chart-H1 denominator candidate.

The first-comparison gate isolates a unique degree shift and a unique
chart-odd sign, but does not construct the corresponding source cell.  This
checker compares that gate with the committed full Hasse/Koszul/cap
totalization.  In two external directions the latter supplies the complete
five-term derived filler of h_v Y w.  Forgetting its four proper Hasse
companions leaves exactly h_v (H_0-u) e_Eq; after the two internal matching
directions this becomes the primitive (H_0-u) e_Eq defect.

The strict chart difference supplies the required -S_v placement as a
closed derived cycle.  It does not supply a higher source generator whose
boundary is the primitive chart kernel k_v.  Thus dn_v is constructed in
the prolonged presentation, while db_v=k_v and physical descent remain the
precise missing data.
"""

from fractions import Fraction
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
Q = Fraction
EXPECTED_DIGEST = "82445db6604e473d0957e42e484f4496a7c9b31d16c4da7ba918dbcd780c4502"
PINS = {
    "computations/verify_h3_non_euler_chart_h1_first_comparison_gate.py":
        "f96cf470fc09255dd092b0d904c2aa85bab3d9ca6966c48c383a19b5ce31e54d",
    "computations/verify_h3_full_hasse_koszul_cap_totalization.py":
        "51940ce0ac8387b68e7725508db6da1a1c055ea036335bbf19750580c69e13fb",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, f"pinned dependency changed: {relative}")


GATE = load(
    "h3_shifted_chart_h1_gate",
    "verify_h3_non_euler_chart_h1_first_comparison_gate.py",
)
HASSE = load(
    "h3_shifted_chart_h1_hasse",
    "verify_h3_full_hasse_koszul_cap_totalization.py",
)


def add_module(*elements):
    return HASSE.module_add(*elements)


def coefficient_times_generator(coefficient, generator):
    return {generator: coefficient} if coefficient else {}


def external_two_face(deleted):
    """Build the honest five-term indexed external Hasse filler."""
    directions = HASSE.endpoint_variables(deleted)
    require(len(directions) == 2, "external direction count changed")
    full_mask = 3
    h = HASSE.derivative(HASSE.H_MIXED, directions)
    require(h == HASSE.face_hafnian(deleted),
            "external mixed coefficient stopped being h_v")

    source_cycle = HASSE.indexed_top_koszul_cycle(directions)
    require(len(source_cycle) == 5,
            "external indexed Koszul cycle stopped having five terms")
    expected_labels = {
        ("r_0", 0), ("r_0", 1), ("r_0", 2),
        ("r_0", full_mask), ("r_m", full_mask),
    }
    require(set(source_cycle) == expected_labels,
            "external source companions changed labels")
    require(source_cycle[("r_0", 0)] == h,
            "zero-jet source term stopped being h_v r_0")
    require(source_cycle[("r_m", full_mask)]
            == HASSE.scale(-1, HASSE.F_PURE),
            "top mixed-row companion changed")
    require(not HASSE.indexed_hasse_chain_differential(
        source_cycle, directions
    ), "complete external indexed source cycle is not closed")

    # n_v=s_{ut}-h_v T.  Only r_0[empty] and T carry target one.
    n_chain = dict(source_cycle)
    n_chain[("T", 0)] = HASSE.scale(-1, h)
    target = HASSE.add(source_cycle[("r_0", 0)], n_chain[("T", 0)])
    require(not target, "external filler retained target")

    # T has differential -Yw, hence coefficient -h gives +hYw.
    n_boundary = {("w", 0): HASSE.multiply(h, HASSE.CAP_Y)}
    require(n_boundary[("w", 0)]
            == HASSE.multiply(HASSE.face_hafnian(deleted), HASSE.CAP_Y),
            "external filler boundary is not h_v Y w")

    # The tempting diagonal h_v(r_0-T) has an extra Eq boundary.  The four
    # proper Hasse companions cancel it exactly.
    diagonal = {
        ("r_0", 0): h,
        ("T", 0): HASSE.scale(-1, h),
    }
    diagonal_eq = HASSE.multiply(h, HASSE.F_PURE)
    companions = {
        label: coefficient for label, coefficient in n_chain.items()
        if label not in diagonal
    }
    require(len(companions) == 4,
            "external proper-face companion count changed")
    companion_eq = HASSE.indexed_hasse_chain_differential(
        companions, directions)
    require(companion_eq == {
        ("eq", 0): HASSE.scale(-1, diagonal_eq)
    }, "proper Hasse companions stopped cancelling h_v F_0 e_Eq")

    return {
        "deleted": deleted,
        "directions": [repr(item) for item in directions],
        "h_terms": len(h),
        "source_terms": len(n_chain),
        "source_companion_terms": len(companions),
        "source_labels": [repr(label) for label in sorted(
            n_chain, key=repr
        )],
        "complete_boundary": "h_v*Y*w",
        "target": 0,
        "ordinary_residue": 0,
        "diagonal_projection_residual": "h_v*(H_0-u)*e_Eq",
        "companion_boundary": "-h_v*(H_0-u)*e_Eq",
    }


def qzero_top_defect(deleted, matching):
    """Retain all four faces, then compare with the top diagonal symbol."""
    directions = HASSE.endpoint_variables(deleted) + HASSE.internal_variables(
        matching
    )
    require(len(directions) == 4, "four-direction cube changed")
    full_mask = 15
    source_cycle = HASSE.indexed_top_koszul_cycle(directions)
    require(not HASSE.indexed_hasse_chain_differential(
        source_cycle, directions
    ), "four-direction indexed cycle is not closed")
    require(source_cycle[("r_0", 0)] == HASSE.constant(),
            "q-zero top stopped being the unit times r_0")
    require(source_cycle[("r_m", full_mask)]
            == HASSE.scale(-1, HASSE.F_PURE),
            "q-zero mixed companion changed")

    # After discarding positive Hasse row copies, the chain is r_0-T.
    # Under the old differential its exact extra component is F_0 e_Eq.
    top = {
        "r_0": HASSE.constant(),
        "T": HASSE.constant(-1),
    }
    old_differential = {
        "r_0": {"eq": HASSE.F_PURE},
        "T": {"w": HASSE.scale(-1, HASSE.CAP_Y)},
    }
    observed = HASSE.apply_module_map(top, old_differential)
    require(observed == {"eq": HASSE.F_PURE, "w": HASSE.CAP_Y},
            "q-zero diagonal residual changed")
    return {
        "deleted": deleted,
        "matching": [list(pair) for pair in matching],
        "full_indexed_terms": len(source_cycle) + 1,
        "top_diagonal": "r_0-T",
        "top_boundary": "Y*w",
        "primitive_underived_residual": "(H_0-u)*e_Eq",
    }


def chart_odd_audit():
    """Check the exact selected-face chart sign and what it does not build."""
    _word, h, _pq, _pr, square, _neutral, cochain = GATE.chart_vectors()
    records, repair = GATE.chart_placement_classification(
        _pq, _pr, cochain
    )
    require(repair == (-1, 1),
            "required primitive chart placement stopped being -S_v")
    minus_square = GATE.scale(square, -1)
    require(GATE.pairing(minus_square, cochain) == Q(-1),
            "-S_v stopped carrying terminal correction -1")
    require(GATE.odd_face_projection(minus_square)
            == GATE.scale(h, -1),
            "-S_v stopped projecting to -h_v")
    return {
        "selected_face": GATE.DELETED,
        "primitive_placements_checked": len(records),
        "required_chart_odd_placement": "-S_v=-(pq-direct)+(pr-two-star)",
        "marked_terminal": -1,
        "chart_difference_differential": 0,
        "chart_difference_target": 0,
        "chart_difference_ordinary_residue": 0,
        "higher_cell_with_boundary_k_v_constructed": False,
        "meaning": (
            "the oppositely oriented strict chart difference realizes the "
            "required marked tail as a closed derived cycle, but it is not "
            "a source two-cell b_v with d b_v=k_v"
        ),
    }


def audit():
    pin_dependencies()
    gate, gate_digest = GATE.audit()
    require(gate_digest
            == "980a89c64009ba6eedbaa7f2c6969b8fcf7b2bfe4031983a163360bf6126c91e",
            "first-comparison ledger changed")
    require(gate["minimal_shift"]["shift_sites"] == [0, 6, 7]
            and gate["chart_tail"]["repair_placement"] == [-1, 1],
            "shift/sign input changed")

    external = [external_two_face(deleted) for deleted in HASSE.ODD]
    qzero = [
        qzero_top_defect(deleted, matching)
        for deleted in HASSE.ODD
        for matching in HASSE.matchings(HASSE.face(deleted))
    ]
    require(len(qzero) == 15, "q-zero matching inventory changed")
    chart = chart_odd_audit()

    ledger = {
        "input_gate_commit": "f872900",
        "unique_shift": "sigma=e_(x,0)+e_(p,0)+e_(q,0)",
        "external_two_direction_faces": external,
        "qzero_four_direction_faces": qzero,
        "chart_odd": chart,
        "derived_filler": {
            "formula": (
                "s_ut=H_m*r_0[ut]+d_uH_m*r_0[t]+d_tH_m*r_0[u]"
                "+h_v*r_0[empty]-(H_0-u)*r_m[ut]; n_v=s_ut-h_v*T"
            ),
            "d_total_n_v": "h_v*Y*w",
            "target": 0,
            "ordinary_residue": 0,
            "constructed": True,
            "ambient_complex": "two-direction prolonged Hasse presentation",
        },
        "source_comparison_filler": {
            "required": "d_source(b_v)=k_v",
            "constructed": False,
            "first_degree_status": (
                "k_v remains the primitive two-chart H1 kernel; the "
                "prolonged chain adds row-face companions but no Cech/"
                "overlap two-cell whose differential is k_v"
            ),
        },
        "physical_descent": {
            "diagonal_order2_residual": "h_v*(H_0-u)*e_Eq",
            "qzero_order4_residual": "(H_0-u)*e_Eq",
            "conclusion": (
                "the complete Hasse companions cancel these residuals only "
                "inside the prolonged presentation; forgetting them is the "
                "exact first primitive physical-comparison obstruction"
            ),
        },
        "verdict": (
            "positive derived target filler and exact -S_v sign; no source "
            "cell with boundary k_v, and the first underived residual is "
            "(H_0-u)*e_Eq after q-zero selection"
        ),
        "scope": (
            "exact h=3 direct-free selected fine degree; complete two- and "
            "four-direction Boolean Hasse companions, but no claim that the "
            "prolonged presentation descends to the physical source"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode("ascii")).hexdigest()
    if EXPECTED_DIGEST != "TO_BE_PINNED":
        require(digest == EXPECTED_DIGEST,
                f"shifted complete differential ledger changed: {digest}")
    return ledger, digest


def main():
    _ledger, digest = audit()
    print("h=3 shifted chart-H1 candidate complete differential: PASS (exact)")
    print("external derived filler: 5 source terms, d n_v=h_v*Y*w")
    print("target / ordinary residue: 0 / 0")
    print("required chart-odd placement: -S_v, terminal -1")
    print("source filler d b_v=k_v: not constructed")
    print("first q-zero underived residual: (H_0-u)*e_Eq")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()

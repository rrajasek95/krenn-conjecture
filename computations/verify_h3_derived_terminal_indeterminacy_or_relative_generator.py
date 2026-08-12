#!/usr/bin/env python3
"""Derived terminal extension and its zero-indeterminacy-or-generator split.

The f872900 source syzygy has marked value one.  The 91041f7 indexed
Hasse/Koszul filler supplies the degree-one correction, so the total-cone
cochain extends with correction value -1.  Its strict pq/pr difference is,
however, a target/ordinary-residue/boundary-zero cycle z whose marked value
is one.  Thus alternative fillers n+c*z have every rational correction
value: the derived extension is not zero-indeterminate on this primitive
H1 summand.

The final linear-algebra audit records the useful physical dichotomy.  For
an augmented physical correction map J and a physically typed terminal
functional q, either q kills ker J (so the promoted value is independent of
the correction), or a normalized element of ker J is itself the required
relative generator.  This statement is conditional on q carrying the
physical anchor/fine-grade typing; the derived chart readout alone does not
supply that comparison.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
EXPECTED_LEDGER_SHA256 = "dde75a89477549d7e04f3a26231bacbe5e48dbea653dc9e0dca2155bb9e06073"
PINS = {
    "computations/verify_h3_non_euler_chart_h1_first_comparison_gate.py":
        "f96cf470fc09255dd092b0d904c2aa85bab3d9ca6966c48c383a19b5ce31e54d",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
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


GATE = load(
    "h3_derived_terminal_gate",
    "verify_h3_non_euler_chart_h1_first_comparison_gate.py",
)
SHIFT = load(
    "h3_derived_terminal_shift",
    "verify_h3_shifted_denominator_chart_filler_augmented_commutator.py",
)
TOTAL = load(
    "h3_derived_terminal_total",
    "verify_h3_full_hasse_koszul_cap_totalization.py",
)


def rank(rows):
    work = [list(map(Q, row)) for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right
                         for left, right in zip(work[row], work[pivot_row])]
        pivot_row += 1
    return pivot_row


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right)), Q(0))


def matvec(matrix, vector):
    return [dot(row, vector) for row in matrix]


def kernel_basis(matrix, width):
    """Exact nullspace basis over Q, with no external dependency."""
    work = [list(map(Q, row)) for row in matrix]
    pivot_columns = []
    pivot_row = 0
    for column in range(width):
        pivot = next((row for row in range(pivot_row, len(work))
                      if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        value = work[pivot_row][column]
        work[pivot_row] = [entry / value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            value = work[row][column]
            work[row] = [left - value * right
                         for left, right in zip(work[row], work[pivot_row])]
        pivot_columns.append(column)
        pivot_row += 1
    free_columns = [column for column in range(width)
                    if column not in pivot_columns]
    basis = []
    for free in free_columns:
        vector = [Q(0)] * width
        vector[free] = Q(1)
        for row, pivot in enumerate(pivot_columns):
            vector[pivot] = -work[row][free]
        basis.append(vector)
    require(all(not any(matvec(matrix, vector)) for vector in basis),
            "nullspace construction failed")
    return basis


def physical_dichotomy_mutation_guard():
    """Exhaust small binary J,q packets for the kernel dichotomy."""
    records = {"zero_indeterminate": 0, "relative_generator": 0}
    packets = 0
    for height in range(4):
        for width in range(1, 5):
            for matrix_mask in range(1 << (height * width)):
                matrix = [
                    [Q((matrix_mask >> (row * width + column)) & 1)
                     for column in range(width)]
                    for row in range(height)
                ]
                kernel = kernel_basis(matrix, width)
                for q_mask in range(1 << width):
                    terminal = [Q((q_mask >> column) & 1)
                                for column in range(width)]
                    values = [dot(terminal, vector) for vector in kernel]
                    witness = next((
                        (vector, value) for vector, value in zip(kernel, values)
                        if value
                    ), None)
                    packets += 1
                    if witness is None:
                        # q kills ker J iff q is in the row space of J.
                        require(rank(matrix) == rank(matrix + [terminal]),
                                "zero-indeterminate q left row(J)")
                        records["zero_indeterminate"] += 1
                    else:
                        vector, value = witness
                        normalized = [-entry / value for entry in vector]
                        require(not any(matvec(matrix, normalized)),
                                "normalized relative generator left ker J")
                        require(dot(terminal, normalized) == -1,
                                "relative generator lost anchor normalization")
                        records["relative_generator"] += 1
    require(sum(records.values()) == packets,
            "physical dichotomy packet count changed")
    return packets, records


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")

    gate, gate_digest = GATE.audit()
    shift, shift_digest = SHIFT.audit()
    require(gate_digest
            == "980a89c64009ba6eedbaa7f2c6969b8fcf7b2bfe4031983a163360bf6126c91e",
            "f872900 ledger changed")
    require(shift_digest
            == "bdcc6a2734c3bd31f060d56fd88f8f5344f39e43aed03f70f18cfa65eef74b92",
            "91041f7 ledger changed")

    # The total-cone cochain equation on the new source cell is simply
    # marked(k_v)+correction(n_v)=0.  Since marked(k_v)=1, the minimal
    # extension assigns -1 to the chosen filler.
    source_value = Q(gate["input_chart_h1"]["marked_readout"])
    correction_value = Q(-1)
    require(source_value + correction_value == 0,
            "derived total-cone cochain did not close")

    # Reconstruct the complete strict chart cycle in the indexed target.
    deleted = 1
    matching = TOTAL.matchings(TOTAL.face(deleted))[0]
    internal = TOTAL.internal_variables(matching)
    marked_u, marked_t = TOTAL.endpoint_variables(deleted)
    eps_u, eps_t, eps_e, eps_f = tuple(
        ("eps", name) for name in ("u", "t", "e", "f")
    )
    directions = {
        marked_u: eps_u,
        marked_t: eps_t,
        internal[0]: eps_e,
        internal[1]: eps_f,
    }
    tau_hm = TOTAL.translate(TOTAL.H_MIXED, directions)
    tau_f0 = TOTAL.translate(TOTAL.F_PURE, directions)
    chart_cycle = {
        "r_0_pq": tau_hm,
        "r_m_pq": TOTAL.scale(-1, tau_f0),
        "r_0_pr": TOTAL.scale(-1, tau_hm),
        "r_m_pr": tau_f0,
    }
    chart_differential = {
        "r_0_pq": {"eq": tau_f0},
        "r_m_pq": {"eq": tau_hm},
        "r_0_pr": {"eq": tau_f0},
        "r_m_pr": {"eq": tau_hm},
    }
    chart_target = {
        "r_0_pq": {"target": TOTAL.constant()},
        "r_m_pq": {},
        "r_0_pr": {"target": TOTAL.constant()},
        "r_m_pr": {},
    }
    require(not TOTAL.apply_module_map(chart_cycle, chart_differential),
            "strict chart difference is not closed")
    require(not TOTAL.apply_module_map(chart_cycle, chart_target),
            "strict chart difference retained target")
    # There are no T/rho generators in the difference, hence its physical
    # cap boundary and ordinary residue vanish identically.
    chart_w = Q(0)
    chart_ores = Q(0)

    external = TOTAL.external_face(tau_hm, (eps_u, eps_t))
    external_order_zero = TOTAL.hasse_coefficient(
        external, (), (eps_e, eps_f)
    )
    require(external_order_zero == TOTAL.face_hafnian(deleted),
            "strict chart cycle lost its h_v external face")
    _word, _h, _pq, _pr, square, _neutral, cochain = GATE.chart_vectors()
    chart_readout = GATE.pairing(square, cochain)
    require(chart_readout == 1,
            "strict target correction cycle lost marked value one")

    # Every n+c*z is another filler.  On the certified primitive chart H1
    # summand the correction values are -1+c, hence all of Q.  This proves
    # non-zero-indeterminacy without claiming that this line exhausts every
    # target H1 class in a larger resolution.
    samples = (Q(-3, 2), Q(0), Q(1), Q(7, 3))
    ambiguity_values = [correction_value + value * chart_readout
                        for value in samples]
    require(ambiguity_values == [Q(-5, 2), Q(-1), Q(0), Q(4, 3)],
            "affine filler indeterminacy changed")

    packets, dichotomy = physical_dichotomy_mutation_guard()
    ledger = {
        "derived_total_cone": {
            "source_syzygy": "d b_v=k_v",
            "target_filler": "d n_v=h_vYw",
            "marked_source_value": 1,
            "minimal_correction_value_on_n_v": -1,
            "cochain_equation": "1+(-1)=0",
        },
        "certified_target_h1_summand": {
            "generator": "z_v=N_v^pq-N_v^pr",
            "source_boundary": 0,
            "w": int(chart_w),
            "target": 0,
            "ordinary_residue": int(chart_ores),
            "marked_value": [chart_readout.numerator,
                             chart_readout.denominator],
            "indeterminacy": "q(<z_v>)=Q; n_v+c*z_v changes value by c",
            "scope": "primitive chart-difference summand, not full H1 census",
        },
        "physical_zero_indeterminacy_or_generator": {
            "hypothesis": (
                "J includes physical source boundary,w,target,ores in one "
                "fixed fine grade and q is the physically typed anchor readout"
            ),
            "branch_1": "q(ker J)=0: promoted value is well-defined",
            "branch_2": (
                "q(z)!=0: -z/q(z) has signature "
                "(ainc,w,tgt,ores)=(-1,0,0,0)"
            ),
            "binary_mutation_guard_packets": packets,
            "binary_mutation_guard_branches": dichotomy,
        },
        "consequence": (
            "the derived cochain exists, but the current chart readout is "
            "not zero-indeterminate; after a physical typed comparison the "
            "same failure is a positive relative generator, so no separate "
            "zero-indeterminacy theorem is required"
        ),
        "remaining_gate": (
            "construct the physical comparison/readout preserving fine "
            "grade and identifying chart marked value with physical anchor "
            "incidence; the derived chart value alone is not that typing"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"derived terminal ledger changed: {digest}")
    return ledger, digest


def main():
    ledger, digest = audit()
    print("h3 derived terminal indeterminacy/generator audit: PASS")
    print("cone cochain extension: correction(n_v)=-1")
    print("primitive target H1: marked(z_v)=1, w=tgt=ores=0")
    print("physical split: zero indeterminacy OR relative anchor generator")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()

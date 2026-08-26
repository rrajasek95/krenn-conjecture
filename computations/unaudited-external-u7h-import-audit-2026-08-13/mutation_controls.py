"""Mutation controls for the U7H audit checkers.

UNAUDITED EXTERNAL IMPORT AUDIT.

A verification script that cannot fail proves nothing.  Each mutant below
breaks one primitive that a checker depends on; the control asserts that the
checker DETECTS it (raises / reports a violated assertion).  A mutant that
survives is reported as a hole in the checker.

Run:  python3 mutation_controls.py
"""

from __future__ import annotations

import random
import traceback
from typing import Callable, Dict, List

import u7h_core
import transfer_six_vertex as T
import verify_u7h_theorem as V


def _instances(n: int, count: int, seed: int) -> List[Dict]:
    rng = random.Random(seed)
    out = []
    while len(out) < count:
        w = V.build_cancelling(rng, n, bool(len(out) % 2))
        if w is not None:
            out.append(w)
    return out


CORPUS6 = _instances(6, 60, 4242)


def run_theorem_checks() -> None:
    """Run the theorem checker over a fixed corpus; raises on any violation.

    Includes ORACLE controls with known answers, so that a primitive which is
    silently broken on true instances (where the mutated predicate happens to
    agree with the truth) is still detected.
    """
    # --- oracle controls, independent of the corpus
    assert len(V.perfect_matchings((0, 1, 2, 3))) == 3
    assert len(V.perfect_matchings((0, 1, 2, 3, 4, 5))) == 15
    assert V.perfect_matchings(()) == [()]
    assert not V.is_connected((0, 1, 2, 3), {(0, 1), (2, 3)})
    assert V.is_connected((0, 1, 2, 3), {(0, 1), (1, 2), (2, 3)})
    # P4 is connected but edge (1,2) lies in no perfect matching
    assert not V.is_matching_covered((0, 1, 2, 3), {(0, 1), (1, 2), (2, 3)})
    assert V.is_matching_covered((0, 1, 2, 3), {(0, 1), (1, 2), (2, 3), (0, 3)})
    # the external repo's own sharpness model: C6 with an inactive chord 02
    chord = {
        (0, 1): u7h_core.GQ(1), (1, 2): u7h_core.GQ(1), (2, 3): u7h_core.GQ(1),
        (3, 4): u7h_core.GQ(1), (4, 5): u7h_core.GQ(1), (0, 5): u7h_core.GQ(-1),
        (0, 2): u7h_core.GQ(7),
    }
    six = (0, 1, 2, 3, 4, 5)
    assert not V.hafnian(six, chord)
    assert V.allowed_edge_graph(six, chord) == set(chord) - {(0, 2)}
    assert V.support_graph(six, chord) == set(chord)
    assert V.active_cofactor_graph(six, chord) == set(chord) - {(0, 2)}
    assert V.least_cancellation(six, chord) == six
    # a disconnected non-minimal cancellation: least R must be a PROPER subset
    split = {
        (0, 1): u7h_core.GQ(2), (0, 2): u7h_core.GQ(3), (1, 3): u7h_core.GQ(-2),
        (2, 3): u7h_core.GQ(3), (4, 5): u7h_core.GQ(5),
    }
    assert not V.hafnian(six, split)
    assert V.least_cancellation(six, split) == (0, 1, 2, 3)
    assert not V.is_connected(six, V.allowed_edge_graph(six, split))

    tags = {
        k: 0
        for k in (
            "instances", "T0", "T1", "T2", "T3", "T4a", "T4b",
            "inactive_support_edge_present", "ambient_allowed_graph_disconnected",
        )
    }
    for w in CORPUS6:
        V.check_instance(6, w, tags)
    # the corpus must actually exercise the branches, else "PASS" is vacuous
    assert tags["T1"] > 0 and tags["T2"] > 0 and tags["T3"] > 0
    assert tags["T4a"] > 0 and tags["T4b"] > 0
    assert tags["inactive_support_edge_present"] > 0


def run_transfer_witness() -> None:
    """Run the transfer witness assertions; raises if the witness stops
    demonstrating the failure of the naive import."""
    w = T.test_witness()
    assert w["cell_minimal"] is True
    assert w["connected_on_V"] is False
    assert w["matching_covered_on_V"] is False
    assert w["connected_on_R"] is True
    assert w["matching_covered_on_R"] is True
    assert w["allowed_eq_active_on_R"] is True

    # --- negative controls: a configuration that must be REJECTED
    cells, chi = T.build_redundant_witness()
    minimal, deletable = T.is_cell_minimal(cells, chi)
    assert minimal is False, "non-minimal configuration accepted as cell-minimal"
    assert (0, 2, chi[0], chi[2]) in deletable
    fw = T.fibre_weights(cells, chi, T.N)
    allow = T.allowed_edge_graph(T.VERTS, fw)
    assert (0, 2) in set(fw), "redundant chord missing from the fibre support"
    assert (0, 2) not in allow, "an edge in no perfect matching reported as allowed"
    assert allow == set(fw) - {(0, 2)}


# ------------------------------------------------------------------ mutants


def mut_allowed_is_support(mod) -> None:
    mod.allowed_edge_graph = lambda verts, w: u7h_core.support_graph(verts, w)


def mut_active_is_support(mod) -> None:
    mod.active_cofactor_graph = lambda verts, w: u7h_core.support_graph(verts, w)


def mut_no_minimalisation(mod) -> None:
    mod.all_least_cancellations = lambda verts, w: [tuple(sorted(verts))]
    mod.least_cancellation = lambda verts, w: tuple(sorted(verts))


def mut_hafnian_drops_term(mod) -> None:
    def bad(vertices, w):
        ms = u7h_core.supported_matchings(vertices, w)
        acc = u7h_core.ZERO
        for m in ms[:-1] if len(ms) > 1 else ms:
            acc = acc + u7h_core.matching_weight(m, w)
        return acc
    mod.hafnian = bad


def mut_supported_ignores_zero(mod) -> None:
    mod.supported_matchings = lambda vertices, w: u7h_core.perfect_matchings(vertices)


def mut_connected_always_true(mod) -> None:
    mod.is_connected = lambda verts, edges: True


def mut_matching_covered_always_true(mod) -> None:
    mod.is_matching_covered = lambda verts, edges: True


def mut_pm_drops_one(mod) -> None:
    real = u7h_core.perfect_matchings

    def bad(vertices):
        ms = real(vertices)
        return ms[:-1] if len(ms) > 2 else ms
    mod.perfect_matchings = bad


def mut_alternating_no_op(mod) -> None:
    mod.alternating_cycle_witness = lambda verts, edges, ref: {}


def mut_degrees_off_by_one(mod) -> None:
    real = u7h_core.degrees
    mod.degrees = lambda verts, edges: {k: v + 1 for k, v in real(verts, edges).items()}


def mut_cell_minimal_always_true(mod) -> None:
    mod.is_cell_minimal = lambda cells, chi: (True, [])


def mut_fibre_weights_drops_edge(mod) -> None:
    real = u7h_core.fibre_weights

    def bad(cells, chi, n):
        w = real(cells, chi, n)
        if len(w) > 1:
            w.pop(sorted(w)[-1])
        return w
    mod.fibre_weights = bad


MUTANTS = [
    ("allowed_edge_graph := support_graph", V, mut_allowed_is_support, run_theorem_checks),
    ("active_cofactor_graph := support_graph", V, mut_active_is_support, run_theorem_checks),
    ("least_cancellation := whole vertex set", V, mut_no_minimalisation, run_theorem_checks),
    ("hafnian drops its last term", V, mut_hafnian_drops_term, run_theorem_checks),
    ("supported_matchings ignores zero weights", V, mut_supported_ignores_zero, run_theorem_checks),
    ("is_connected := True", V, mut_connected_always_true, run_theorem_checks),
    ("perfect_matchings drops one matching", V, mut_pm_drops_one, run_theorem_checks),
    ("alternating_cycle_witness := no-op", V, mut_alternating_no_op, run_theorem_checks),
    ("degrees shifted by +1", V, mut_degrees_off_by_one, run_theorem_checks),
    ("is_connected := True (transfer)", T, mut_connected_always_true, run_transfer_witness),
    ("is_matching_covered := True (transfer)", T, mut_matching_covered_always_true, run_transfer_witness),
    ("is_cell_minimal := True (transfer)", T, mut_cell_minimal_always_true, run_transfer_witness),
    ("fibre_weights drops an edge (transfer)", T, mut_fibre_weights_drops_edge, run_transfer_witness),
    ("allowed_edge_graph := support_graph (transfer)", T, mut_allowed_is_support, run_transfer_witness),
]


def main() -> None:
    print("baseline (unmutated) ...", end=" ")
    run_theorem_checks()
    run_transfer_witness()
    print("PASS")

    survivors = []
    print(f"\n{len(MUTANTS)} mutants:")
    for name, mod, apply_mut, harness in MUTANTS:
        saved = {k: getattr(mod, k) for k in dir(mod) if not k.startswith("__")}
        try:
            apply_mut(mod)
            try:
                harness()
                caught = False
                detail = "harness still passed"
            except Exception as exc:  # noqa: BLE001 - detection is the point
                caught = True
                detail = f"{type(exc).__name__}: {str(exc)[:70]}"
        finally:
            for k, v in saved.items():
                setattr(mod, k, v)
        status = "KILLED " if caught else "SURVIVED"
        print(f"  [{status}] {name:48s} {detail}")
        if not caught:
            survivors.append(name)

    # sanity: after restoring everything the baseline must still pass
    run_theorem_checks()
    run_transfer_witness()

    print()
    if survivors:
        print(f"MUTATION CONTROL INCOMPLETE: {len(survivors)} survivor(s): {survivors}")
        raise SystemExit(1)
    print(f"MUTATION CONTROL: all {len(MUTANTS)} mutants killed; baseline restored and passing")


if __name__ == "__main__":
    main()

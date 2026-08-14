#!/usr/bin/env python3
"""Audit the logarithmic shifted-ridge shortcut on the active-fan packet.

The exact Cartan restriction has 39 endpoint orbits.  Twenty-seven have a
nonconstant remote tail T; before collection their product differentials
contain 30 labelled faces Omega*d(q_e^11).  The committed ridge connection
has one-forms d(q_xv^01), and even its strongest two-root closure stays on
the 01 coefficient block.  It therefore has zero projection to the 30
remote-tail directions.

On a chosen nonzero occurrence f, T divides f and is a unit on D(f).  In
the localized Kahler module

    -T^-1 d(T Omega) = gamma - Omega*dlog(T),

and eta/sigma kill dlog(T) because every remote tail cell has colour 11
away from their weighted sites.  This is an exact formal localized lift.
It does not itself isolate the occurrence in the physical source complex,
and homogeneous localization preserves the unequal 67/01 site degrees.
Thus the remaining physical input is an occurrence-labelled shifted-grade
section, not another root-connection identity.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_active_fan_omit_coloop_cartan_termwise_protected_gate.py":
        "7d43fabe62fb5b3707821c3b969096c8d353198d7eced32862f1d8a29ba5b630",
    "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py":
        "aea73ce5ff6ce183245d209393ed60192066d38eab7d4d203caa0c82cc5b16d6",
    "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py":
        "42bf68eeb963d568d1c8d9156d4176bec31a114b6fe804744833364fe3633475",
    "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py":
        "674a7503db43b8ad53d6f4ea9d7fe095f0f26629d92e4b0dd291f14bde82fa3a",
    "computations/verify_k8_squarefree_occurrence_euler_cube_fixed_fibre_gate.py":
        "d294e65098f5f3b67de8b67a8c53a6388b8d097e0d81bc0a820ea5c93ac0b504",
    "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py":
        "5b41444ef5f4844bc1bd87a6a4e81e60a631f3549eed21c160efdcb428582ea4",
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
}
EXPECTED_LEDGER_SHA256 = (
    "907cd25b4fb2c92ef2b2954da0e9c79f57bc35d5996bc837112a07ae89bcee95"
)

ROOT_SITES = (0, 1)
ENDPOINT_SITES = (6, 7)
ACTION_SITES = frozenset(ROOT_SITES + ENDPOINT_SITES)
COLOOP_EDGE = ROOT_SITES
ENDPOINT_EDGE = ENDPOINT_SITES
REMOTE_SITES = (2, 3, 4, 5)


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


def edge(left: int, right: int) -> tuple[int, int]:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index, second in enumerate(vertices[1:], 1):
        rest = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(rest):
            yield tuple(sorted((edge(first, second),) + tail))


def swap_endpoint_site(site: int) -> int:
    if site == 6:
        return 7
    if site == 7:
        return 6
    return site


def endpoint_swap(matching):
    return tuple(sorted(edge(swap_endpoint_site(left),
                             swap_endpoint_site(right))
                        for left, right in matching))


def rank(columns) -> int:
    columns = tuple(tuple(map(Q, column)) for column in columns)
    if not columns:
        return 0
    height = len(columns[0])
    require(all(len(column) == height for column in columns), "rank height")
    rows = [[columns[column][row] for column in range(len(columns))]
            for row in range(height)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(pivot_row, height)
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        value = rows[pivot_row][column]
        rows[pivot_row] = [entry / value for entry in rows[pivot_row]]
        for row in range(height):
            if row == pivot_row or not rows[row][column]:
                continue
            value = rows[row][column]
            rows[row] = [left - value * right for left, right in
                         zip(rows[row], rows[pivot_row], strict=True)]
        pivot_row += 1
    return pivot_row


def unit(index: int, size: int):
    return tuple(Q(int(position == index)) for position in range(size))


def dot(left, right):
    return sum((Q(a) * Q(b) for a, b in zip(left, right, strict=True)), Q(0))


def active_orbits():
    sector = tuple(matching for matching in
                   perfect_matchings(tuple(range(8)))
                   if COLOOP_EDGE not in matching
                   and ENDPOINT_EDGE not in matching)
    require(len(sector) == 78, len(sector))
    visited = set()
    records = []
    for matching in sector:
        if matching in visited:
            continue
        mate = endpoint_swap(matching)
        require(mate in sector and mate != matching,
                ("bad endpoint orbit", matching, mate))
        visited.update((matching, mate))
        representative = min(matching, mate)
        tail = tuple(pair for pair in representative
                     if set(pair).isdisjoint(ACTION_SITES))
        require(tail == tuple(pair for pair in max(matching, mate)
                              if set(pair).isdisjoint(ACTION_SITES)),
                ("remote tail changed", matching, mate))
        records.append((representative, max(matching, mate), tail))
    require(len(records) == 39 and len(visited) == 78,
            (len(records), len(visited)))
    return tuple(sorted(records))


def debt_inventory_audit() -> tuple[dict[str, object], tuple, tuple]:
    records = active_orbits()
    atoms = []
    aggregates = []
    tail_histogram = Counter()
    edge_histogram = Counter()
    for representative, mate, tail in records:
        tail_histogram[len(tail)] += 1
        local_atoms = []
        for differentiated in tail:
            # Keep the occurrence parent, differentiated cell, fine colour,
            # and operation parent.  Equal physical edges in distinct
            # occurrences are deliberately different atoms.
            atom = (
                representative,
                differentiated + (1, 1),
                "Omega*dlog(q_tail^11)",
                "tail-Leibniz/Hasse",
            )
            atoms.append(atom)
            local_atoms.append(atom)
            edge_histogram[differentiated] += 1
        if local_atoms:
            aggregates.append((representative, mate, tail,
                               tuple(local_atoms)))
    require(tail_histogram == Counter({0: 12, 1: 24, 2: 3})
            and len(atoms) == 30 and len(set(atoms)) == 30
            and len(aggregates) == 27
            and edge_histogram == Counter({
                (2, 3): 5, (2, 4): 5, (2, 5): 5,
                (3, 4): 5, (3, 5): 5, (4, 5): 5,
            }), (tail_histogram, len(atoms), len(aggregates), edge_histogram))

    lookup = {atom: index for index, atom in enumerate(atoms)}
    aggregate_vectors = []
    for _representative, _mate, _tail, local_atoms in aggregates:
        vector = [Q(0)] * len(atoms)
        for atom in local_atoms:
            vector[lookup[atom]] = Q(1)
        aggregate_vectors.append(tuple(vector))
    require(rank(aggregate_vectors) == 27,
            "the occurrence-labelled debt aggregates lost independence")

    return ({
        "endpoint_orbits": len(records),
        "remote_tail_histogram": dict(sorted(tail_histogram.items())),
        "labelled_Omega_dT_atoms": len(atoms),
        "fixed_product_rule_aggregate_debts": len(aggregates),
        "aggregate_debt_rank": rank(aggregate_vectors),
        "differentiated_remote_edge_histogram": {
            str(pair): count for pair, count in sorted(edge_histogram.items())
        },
        "atom_labels_retained": [
            "endpoint-orbit parent", "differentiated physical edge",
            "colour 11", "Omega potential", "tail-Leibniz/Hasse parent",
        ],
    }, tuple(atoms), tuple(aggregate_vectors))


def connection_projection_audit(atoms, aggregates) -> dict[str, object]:
    connection_module = load(
        "computations/verify_h3_e14_cap_graph_two_parameter_flat_transport_gate.py",
        "log_kahler_committed_connection",
    )
    connection = connection_module.shifted_kahler_connection_audit()
    require(connection["nonzero_connection_one_faces"] == 4
            and connection["connection_one_face"]
                == "-d(q_xv^01) when root site i=v"
            and connection["eta_sigma_kill_connection_face"] is True
            and connection["physical_shifted_connection_face_constructed"]
                is False,
            "the committed shifted-Kahler connection changed")

    # Literal committed E14 one-faces d(q_0v^01), v=2,3,4,5.  Grant also
    # the strongest two-root closure on the coloop coefficient block:
    # d(q_01^10), d(q_01^01), and d(q_01^11).  None is a differential of
    # a remote colour-11 edge among 2,3,4,5.
    committed = tuple((0, site, 0, 1) for site in REMOTE_SITES)
    two_root_closure = (
        (0, 1, 1, 0), (0, 1, 0, 1), (0, 1, 1, 1),
    )
    debt_cells = {atom[1] for atom in atoms}
    require(debt_cells == {
        (2, 3, 1, 1), (2, 4, 1, 1), (2, 5, 1, 1),
        (3, 4, 1, 1), (3, 5, 1, 1), (4, 5, 1, 1),
    }, debt_cells)
    require(not debt_cells.intersection(committed)
            and not debt_cells.intersection(two_root_closure),
            "a ridge-root connection became a remote-tail differential")

    connection_columns = tuple((Q(0),) * len(atoms)
                               for _cell in committed + two_root_closure)
    require(rank(connection_columns) == 0
            and rank(connection_columns + aggregates) == 27,
            "the exact debt/connection quotient rank changed")

    first_atom = atoms[0]
    first_dual = unit(0, len(atoms))
    require(all(dot(first_dual, column) == 0
                for column in connection_columns)
            and dot(first_dual, unit(0, len(atoms))) == 1,
            "the first tail-debt detector changed")
    return {
        "committed_connection_one_forms": [
            f"d(q_{left}{right}^{a}{b})"
            for left, right, a, b in committed
        ],
        "strongest_local_two_root_closure": [
            f"d(q_{left}{right}^{a}{b})"
            for left, right, a, b in two_root_closure
        ],
        "projection_rank_on_30_tail_atoms": 0,
        "rank_after_27_required_aggregate_debts": 27,
        "reason": (
            "Kahler one-forms retain their coefficient-cell labels: the "
            "root connection differentiates a cell incident with 0/1, "
            "whereas every debt differentiates a colour-11 edge in {2,3,4,5}"
        ),
        "committed_gamma_connection_supplies_Omega_dT": False,
    }


def cell_weight(cell, site_weights):
    left, right, left_colour, right_colour = cell
    return (site_weights.get((left, left_colour), 0)
            + site_weights.get((right, right_colour), 0))


def selected_logarithmic_localization_audit(atoms) -> dict[str, object]:
    records = active_orbits()
    selected = next(record for record in records if len(record[2]) == 1)
    representative, mate, tail = selected
    require(representative
            == ((0, 2), (1, 6), (3, 4), (5, 7))
            and mate == ((0, 2), (1, 7), (3, 4), (5, 6))
            and tail == ((3, 4),), selected)

    # The occurrence monomial is T*R.  In A_f, T^{-1}=R/f.  This is an
    # exact localization identity and uses no analytic logarithm.
    remaining = tuple(pair for pair in representative if pair not in tail)
    require(tuple(sorted(tail + remaining)) == representative,
            "the selected occurrence stopped factoring as T*R")

    decorated_tail = (3, 4, 1, 1)
    eta_weights = {
        auxiliary: {
            (6, 0): 1,
            (auxiliary, 0): -1,
        }
        for auxiliary in range(1, 6)
    }
    sigma_weights = {(6, 2): 1, (0, 2): -1}
    require(all(cell_weight(decorated_tail, weights) == 0
                for weights in eta_weights.values())
            and cell_weight(decorated_tail, sigma_weights) == 0,
            "the selected dlog tail acquired eta/sigma weight")

    # Homogeneous localization extends the Z^8 grading to a group grading.
    # Dividing both halves by the same T subtracts the same tail degree, so
    # their 67/01 difference survives.
    degree_67 = (0, 0, 0, 0, 0, 0, 1, 1)
    degree_01 = (1, 1, 0, 0, 0, 0, 0, 0)
    tail_degree = (0, 0, 0, 1, 1, 0, 0, 0)
    multiplied_67 = tuple(a + b for a, b in
                          zip(degree_67, tail_degree, strict=True))
    multiplied_01 = tuple(a + b for a, b in
                          zip(degree_01, tail_degree, strict=True))
    localized_67 = tuple(a - b for a, b in
                         zip(multiplied_67, tail_degree, strict=True))
    localized_01 = tuple(a - b for a, b in
                         zip(multiplied_01, tail_degree, strict=True))
    require(localized_67 == degree_67 and localized_01 == degree_01
            and localized_67 != localized_01,
            "localization collapsed the shifted ridge grades")

    selected_atom = next(atom for atom in atoms
                         if atom[0] == representative
                         and atom[1] == decorated_tail)
    return {
        "selected_plus_occurrence": [list(pair) for pair in representative],
        "selected_minus_occurrence": [list(pair) for pair in mate],
        "remote_tail_T": "q_34^11",
        "factorization": "f=T*R",
        "unit_on_D_f": "T^(-1)=R/f",
        "localized_identity": (
            "-T^(-1)d(T Omega)=gamma-Omega*dlog(T)"
        ),
        "root_and_endpoint_actions_fix_T": True,
        "eta_z_on_dlogT_for_z_1_to_5": [0, 0, 0, 0, 0],
        "sigma_on_dlogT": 0,
        "logarithmic_correction_terminal_dark": True,
        "first_irreducible_typed_face": {
            "atom": repr(selected_atom),
            "human_label": "Omega*dlog(q_34^11)",
            "operation_parent": "tail-Leibniz/Hasse",
            "not_connection_parent": "ridge root Lie derivative",
            "67_half_degree_after_localization": list(localized_67),
            "01_half_degree_after_localization": list(localized_01),
        },
        "formal_localized_PP_Kahler_lift_exists": True,
        "homogeneous_localization_makes_physical_shifted_section": False,
    }


def source_selection_and_terminal_gate() -> dict[str, object]:
    hasse_module = load(
        "computations/verify_h3_hasse_coproduct_cosimplicial_totalization.py",
        "log_kahler_hasse_product",
    )
    leibniz_packets = hasse_module.bounded_hasse_leibniz_audit()
    require(leibniz_packets > 0,
            "the Hasse product-rule source theorem changed")
    euler = load(
        "computations/verify_k8_squarefree_occurrence_euler_cube_fixed_fibre_gate.py",
        "log_kahler_euler_selection",
    ).audit()
    require(euler["verdict"]["order_four_Euler_cube_is_physical_P_f"] is False
            and euler["fixed_fibre_descent"]["first_nonphysical_face_terms"] == 15,
            "the occurrence Euler source gate changed")
    centered_module = load(
        "computations/verify_h3_centered_occurrence_same_grade_physical_gate.py",
        "log_kahler_centered_selection",
    )
    centered, centered_digest = centered_module.audit()
    require(centered_digest == centered_module.EXPECTED_LEDGER_SHA256
            and centered["complete_operation_image"]
                ["physical_orbit_sums_individually_constructed"] is False,
            "the centered occurrence gate changed")
    ridge = load(
        "computations/verify_h3_residual_q_terminal_ridge_kahler_identification.py",
        "log_kahler_ridge_grade",
    ).audit()
    require(ridge["physical_repeated_grade_lift_constructed"] is False,
            "a physical shifted ridge appeared")
    return {
        "support_level_choice_of_nonzero_occurrence": True,
        "choice_defines_source_operation_projector": False,
        "Euler_selector_status": (
            "relative KS carrier; first physical-source defect is the "
            "15-term singleton normal H_e"
        ),
        "same_grade_centered_occurrence_cell_constructed": False,
        "Hasse_Leibniz_supplies_formal_PP_product_faces": True,
        "Hasse_Leibniz_supplies_physical_augmented_columns": False,
        "bounded_divided_power_Leibniz_packets_replayed": leibniz_packets,
        "conditional_order": [
            "grant an occurrence-labelled source cell selecting the chosen endpoint orbit",
            "base-change it to D(f), where T is a unit and the log ridge is terminal-dark",
            "grant the physical shifted 67/01 grade section",
            "then apply the physical q correction-or-relative-generator alternative",
        ],
        "first_dependency_for_one_occurrence_shortcut": (
            "physical occurrence selection, not the algebraic inversion of T"
        ),
        "next_dependency_after_selection": (
            "comparison from the localized PP/Kahler class to the literal "
            "shifted repeated-grade correction module"
        ),
    }


def filler_or_terminal_test(atoms, aggregates) -> dict[str, object]:
    # Existing committed connection columns have zero debt projection.
    existing = tuple((Q(0),) * len(atoms) for _ in range(7))
    selected_debt = aggregates[0]
    # The sorted inventory starts with a one-edge tail, so this is a unit.
    require(sum(selected_debt) == 1 and rank(existing) == 0
            and rank(existing + (selected_debt,)) == 1,
            "the first filler rank test changed")
    selected_index = next(index for index, value in enumerate(selected_debt)
                          if value)
    detector = unit(selected_index, len(atoms))
    require(all(dot(detector, column) == 0 for column in existing)
            and dot(detector, selected_debt) == 1,
            "the normalized debt detector changed")
    return {
        "selected_debt_rank_before_then_after": [0, 1],
        "full_required_aggregate_rank": rank(aggregates),
        "filler_test": (
            "for a selected occurrence f with debt vector g_f, a physical "
            "same-grade filler exists exactly when g_f lies in the projected "
            "column span of the occurrence-labelled correction map"
        ),
        "current_selected_detector": (
            "coefficient extraction on Omega*dlog(q_34^11); it kills every "
            "committed gamma/root-connection column and reads 1 on g_f"
        ),
        "terminal_test": (
            "if g_f is not in the physical projected span, extend this dual "
            "through the complete boundary/W/target/residue rows.  Once its "
            "q/anchor value is physically typed, the accepted dichotomy "
            "makes it either a descended separator or a normalized relative generator"
        ),
        "terminal_promotion_currently_unconditional": False,
        "why_not": (
            "the same occurrence/PP-to-physical comparison is needed to "
            "define the q/anchor value on this operation-tagged debt"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                ("pinned dependency changed", relative, actual, expected))

    inventory, atoms, aggregates = debt_inventory_audit()
    ledger = {
        "theorem": (
            "h3 active-fan logarithmic Kahler occurrence-localization gate"
        ),
        "pins": PINS,
        "debt_inventory": inventory,
        "committed_connection_projection":
            connection_projection_audit(atoms, aggregates),
        "selected_logarithmic_localization":
            selected_logarithmic_localization_audit(atoms),
        "source_selection_and_grade_gate": source_selection_and_terminal_gate(),
        "filler_or_terminal": filler_or_terminal_test(atoms, aggregates),
        "verdict": (
            "The committed gamma/root connection does not supply any of the "
            "30 Omega*dT tail faces after labels are retained.  On one "
            "chosen D(f), logarithmic normalization is nevertheless exact "
            "and eta/sigma dark.  Its use as the protected Phi is blocked "
            "first by the absent physical occurrence selector and, after "
            "granting that selector, by the absent localized PP-to-physical "
            "shifted-grade section.  Localization alone changes neither "
            "operation parent nor the unequal 67/01 site degrees."
        ),
        "scope": (
            "exact h=3 01-coloop/67-response packet, all 39 endpoint orbits, "
            "30 labelled tail differentials and the one-occurrence D(f) "
            "shortcut; not a full GHZ counterexample or an all-h theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("gamma/root connection projection to 30 Omega*dT faces: RANK 0")
    print("one-occurrence logarithmic ridge on D(f): FORMAL AND ETA/SIGMA DARK")
    print("first physical dependency: OCCURRENCE-LABELLED SOURCE SELECTION")
    print("next dependency: LOCALIZED PP-TO-SHIFTED-GRADE COMPARISON")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
r"""Aggregate-Tor shortcut on the normalized rootless C5 chart.

The five clean collision edges span the saturated sum-zero lattice in the
five face coordinates.  Consequently the rootless construction does not
need the denominator transgression tau to be onto: one homogeneous image
vector whose coordinate sum is a unit can be transported to any face basis
vector.  If the entire image is sum-zero, the sum covector survives only in
the reduced face quotient; endpoint bars force an additional Omega (or an
inadmissible ordinary-residue) dual component before it can be physical.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "51381f29700602ccd05daede6f5ec1c6285ad508046b6daf36f5e45663579a67"
PINS = {
    "computations/verify_h3_component_iv_reduced_companion_tor_gate.py":
        "5bf7e0960b413c4e5d587b3c8f46d51493010bb73413682d7705bb28070d0935",
    "notes/h3-component-iv-reduced-companion-tor-gate.md":
        "6c33ba432918f845fe9658b4637dfa811745e339f79ed82c33d8ab3340f139ba",
    "computations/verify_h3_rootless_ridge_eq_tail_attachment_composition_gate.py":
        "b1d1a62d229d9ebb3d20abbc7359503af08506fec882f629ee95a886c58490a8",
    "notes/h3-rootless-ridge-eq-tail-attachment-composition-gate.md":
        "b3fb916c2e64c9214108f49191363b986cd5890c330015b0baaf7fa0d9a683c2",
    "computations/verify_h3_rootless_normalized_c5_base_column_source_separator.py":
        "635b3e667613049817f04440401d31237db259ab7cf9948989e0da2674efb022",
    "notes/h3-rootless-normalized-c5-base-column-source-separator.md":
        "7b283f93c9bacddb94fa2f19c550b5b39217291c8c98c7603ff1ba3b42c85e43",
    "computations/verify_h3_rootless_augmented_pentagon_fredholm_alternative.py":
        "0b0831391416f85302b5f2d89da0672e07dca4c73fc5f3893ad992abd48c1d2b",
    "notes/h3-rootless-augmented-pentagon-fredholm-alternative.md":
        "4febecdfa01b6697970af0d518721058842afe784ac59f267b8ebc847a43cecb",
    "computations/verify_h3_denominator_tor_transgression_fitting_gate.py":
        "33cd6ac3de85f83ee16189601930938d73f35f2fef5db20253380801bdd78459",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def load_transgression_module():
    path = ROOT / "computations/verify_h3_denominator_tor_transgression_fitting_gate.py"
    spec = importlib.util.spec_from_file_location("aggregate_tor_dependency", path)
    require(spec is not None and spec.loader is not None,
            "cannot load the Tor transgression dependency")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def pin_dependencies() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def incidence_columns():
    columns = []
    for index in range(5):
        column = [0] * 5
        column[index] = -1
        column[(index + 1) % 5] = 1
        columns.append(tuple(column))
    return tuple(columns)


def add(*vectors):
    return tuple(sum(vector[index] for vector in vectors)
                 for index in range(5))


def scale(value, vector):
    return tuple(value * entry for entry in vector)


def transport_coefficients(z):
    """Return c with sum c_i(-e_i+e_(i+1)) = z, for sum z=0."""
    require(sum(z) == 0, "collision transport needs zero aggregate")
    prefix = Q(0)
    coefficients = []
    for index in range(4):
        prefix += Q(z[index])
        coefficients.append(-prefix)
    coefficients.append(Q(0))
    return tuple(coefficients)


def collision_transport(z):
    coefficients = transport_coefficients(z)
    result = (Q(0),) * 5
    for coefficient, column in zip(
            coefficients, incidence_columns(), strict=True):
        result = add(result, scale(coefficient, column))
    require(result == tuple(map(Q, z)),
            ("explicit C5 collision transport failed", z, result))
    return coefficients


def one_aggregate_vector_theorem():
    samples = (
        (Q(1), Q(0), Q(0), Q(0), Q(0)),
        (Q(2), Q(-3), Q(5), Q(7), Q(1)),
        (Q(1, 2), Q(2, 3), Q(-5, 7), Q(4, 5), Q(9, 11)),
    )
    records = []
    for y in samples:
        aggregate = sum(y)
        require(aggregate != 0, "sample aggregate became zero")
        normalized = scale(Q(1) / aggregate, y)
        for target in range(5):
            basis = tuple(Q(int(index == target)) for index in range(5))
            defect = add(basis, scale(Q(-1), normalized))
            coefficients = collision_transport(defect)
            reconstructed = add(
                normalized,
                *[scale(coefficient, column) for coefficient, column in zip(
                    coefficients, incidence_columns(), strict=True)],
            )
            require(reconstructed == basis,
                    "aggregate Tor vector did not transport to a face basis")
        records.append({
            "image_vector": [str(value) for value in y],
            "aggregate": str(aggregate),
            "normalizes_after_localizing_aggregate": True,
            "all_five_face_basis_vectors_reconstructed": True,
        })
    return records


def frozen_packet_audit():
    transgression = load_transgression_module()
    records = {}
    for name in ("direct_free", "tilted"):
        packet = transgression.packet_audit(name)
        rows = tuple(tuple(Q(entry) for entry in row)
                     for row in packet["transgression_rows"])
        aggregates = tuple(sum(row) for row in rows)
        active = tuple(index for index, value in enumerate(aggregates) if value)
        require(active, f"{name}: rank-deficient Tor image lost aggregate hit")
        witness = rows[active[0]]
        require(sum(witness) != 0,
                f"{name}: aggregate witness became zero")
        normalized = scale(Q(1) / sum(witness), witness)
        basis0 = (Q(1), Q(0), Q(0), Q(0), Q(0))
        collision_transport(add(basis0, scale(Q(-1), normalized)))
        records[name] = {
            "is_full_source_point": False,
            "transgression_rank": packet["transgression_rank"],
            "aggregate_nonzero_row_indices": list(active),
            "first_aggregate_witness": [str(value) for value in witness],
            "one_face_augmentation_after_collision_transport": True,
        }
    require(records["direct_free"]["transgression_rank"] == 4
            and records["tilted"]["transgression_rank"] == 3,
            "frozen packet Tor ranks changed")
    return records


def dual_extension_gate():
    # Coordinates are (Omega aggregate, face aggregate, ordinary residue).
    # Every endpoint bar is (-Omega,+face,+ores).  A face-only epsilon is
    # therefore not a cocycle.  Write an extension as (a,1,b).  Killing the
    # endpoint bar gives -a+1+b=0.  The physical pure-residue column forces
    # b=0, hence a=1.  Thus an Omega dual is forced.  Transporting it to the
    # rootless ridge then requires the still-unconstructed Omega->r map.
    endpoint_bar = (Q(-1), Q(1), Q(1))
    pure_residue = (Q(0), Q(0), Q(1))

    def pair(left, right):
        return sum(a * b for a, b in zip(left, right, strict=True))

    face_only = (Q(0), Q(1), Q(0))
    require(pair(face_only, endpoint_bar) == 1,
            "face aggregate unexpectedly killed the endpoint bar")
    illegal_residue_extension = (Q(0), Q(1), Q(-1))
    require(pair(illegal_residue_extension, endpoint_bar) == 0
            and pair(illegal_residue_extension, pure_residue) == -1,
            "ordinary-residue obstruction changed")
    physical_zero_residue_extension = (Q(1), Q(1), Q(0))
    require(pair(physical_zero_residue_extension, endpoint_bar) == 0
            and pair(physical_zero_residue_extension, pure_residue) == 0,
            "Omega extension stopped killing the typed bars")
    return {
        "coordinate_order": ["endpoint_Omega_aggregate",
                             "face_aggregate", "ordinary_residue"],
        "face_only_epsilon_on_endpoint_bar": "1 (not a cocycle)",
        "residue_correction": (
            "kills the endpoint bar but reads -1 on the physical pure-ores column"
        ),
        "unique_zero_ores_extension_on_this_block": ["1", "1", "0"],
        "remaining_physical_input": (
            "a multidegree-preserving Omega-to-rootless-ridge comparison; "
            "additional endpoint-word-change/correction rows must also be killed"
        ),
        "terminal_annihilator_constructed": False,
    }


def main() -> None:
    pin_dependencies()
    incidence = incidence_columns()
    require(all(sum(column) == 0 for column in incidence),
            "a C5 collision edge changed aggregate")
    # The explicit prefix solver proves integrally that im D=ker epsilon;
    # exercise all primitive zero-sum vectors in a bounded cube as a replay.
    primitive_checks = 0
    for a in range(-2, 3):
        for b in range(-2, 3):
            for c in range(-2, 3):
                for d in range(-2, 3):
                    z = (a, b, c, d, -a - b - c - d)
                    collision_transport(z)
                    primitive_checks += 1
    require(primitive_checks == 625, "zero-sum lattice replay changed")

    ledger = {
        "theorem": "one aggregate Tor vector suffices modulo C5 collisions",
        "collision_lattice": {
            "columns": [list(column) for column in incidence],
            "rank": 4,
            "image": "ker(epsilon: Z^5 -> Z), saturated",
            "bounded_integral_replay": primitive_checks,
        },
        "aggregate_unit_theorem": {
            "hypothesis": (
                "one homogeneous y in im(tau) has epsilon(y) a unit in the "
                "localized full-source ring"
            ),
            "conclusion": (
                "after normalizing y and adding clean collision-edge paths, "
                "every face basis vector e_v is a source-provenant reduced augmentation"
            ),
            "fine_grade_guard": (
                "y and the collision paths must be homogenized in one repeated-site "
                "degree; setting selected C5 factors numerically to one does not erase degree"
            ),
            "sample_replays": one_aggregate_vector_theorem(),
        },
        "frozen_rank_deficient_packets": frozen_packet_audit(),
        "aggregate_zero_branch": {
            "reduced_face_quotient": (
                "if epsilon(im tau)=0, epsilon survives on S^5/(im tau+im D)"
            ),
            "physical_extension_gate": dual_extension_gate(),
        },
        "scope": (
            "exact normalized-C5 collision/Tor reduction. It weakens onto(tau) "
            "to one unit aggregate hit for the rootless base-column purpose; it "
            "does not construct the Omega/ridge comparison or promote a reduced "
            "face covector to the full terminal quotient"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FILLED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"aggregate Tor shortcut ledger changed: {digest}")
    print("h3 rootless C5 aggregate-Tor shortcut: PASS")
    print("collision image = saturated ker epsilon (rank 4)")
    print("one unit aggregate Tor vector => all five face augmentations")
    print("rank-4/rank-3 frozen packets both hit the aggregate")
    print("aggregate-zero face dual: not yet a physical terminal annihilator")
    print("ledger SHA-256:", digest)


if __name__ == "__main__":
    main()

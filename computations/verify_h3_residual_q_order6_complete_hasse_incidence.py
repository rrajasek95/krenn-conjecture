#!/usr/bin/env python3
"""Audit the complete unsigned Hasse incidence tower of the order-six lift.

The order-six source-shadow theorem retained only its two-direction faces.
Here the same exact 188-term solution is expanded on every positional subset
of its six derivative directions.  If L_k denotes the resulting k-face
counter, the unsigned down-incidence satisfies

    down(L_(k+1)) = (6-k) L_k.

In particular down(L_3)=4 L_2.  Since L_2 is the nonzero residual -delta,
the higher faces cannot and should not vanish.  They are the forced coherent
Hasse lift of the pair shadow.  Physical repeated-grade typing and Spencer
signs remain separate requirements.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_residual_q_order6_missing_face_probe.py":
        "5f0e6ad385547aed67f1d954da57c71929d336552bb98d07c68d271889b982ab",
    "notes/h3-residual-q-order6-missing-face-source-shadow-lift.md":
        "e24324f495b7c9402b6d7fa43e6e30997c437987d35236335e1d88cd2142d9b1",
}
EXPECTED_LEDGER_SHA256 = "6e30806247614d5e622c79d1b904ab6ebe115c64b4cfce7d77c8ff4011c9f2ef"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name):
    specification = importlib.util.spec_from_file_location(name, ROOT / relative)
    require(specification is not None and specification.loader is not None,
            f"cannot load dependency: {relative}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def exact_solution_terms():
    order6 = load(
        "computations/verify_h3_residual_q_order6_missing_face_probe.py",
        "complete_hasse_order6",
    )
    repair = load(
        "computations/verify_h3_residual_q_order5_generator_repair.py",
        "complete_hasse_repair",
    )
    commutator = load(
        "computations/verify_h3_residual_q_covariance_curvature_commutator.py",
        "complete_hasse_commutator",
    )
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "complete_hasse_base",
    )
    system = repair.build_system(base, commutator)
    derivatives = order6.build_exact_sixth_derivatives(system)
    missing = frozenset(((0, 7, 1, 1), (2, 4, 1, 1)))
    metadata = set()
    for _product, directions in derivatives:
        if not missing.issubset(directions):
            continue
        for coefficient in order6.eligible_coefficients(
                repair, commutator, directions):
            metadata.add((coefficient, directions))

    columns = []
    for coefficient, directions in sorted(metadata, key=repr):
        column = Counter()
        for product in range(3):
            for remainder, value in derivatives.get((product, directions), {}).items():
                column[(product, tuple(sorted(remainder + coefficient)))] += value
        shadow = {row: value for row, value in column.items() if value}
        for left, right in combinations(range(6), 2):
            pair = tuple(sorted((directions[left], directions[right])))
            shadow[(3, pair)] = shadow.get((3, pair), 0) + 1
        columns.append(((coefficient, directions), shadow))

    basis = repair.select_modular_basis(columns)
    target = {(3, pair): int(value)
              for pair, value in commutator.expected_second_shadow().items()}
    solution, picked = repair.exact_solution(columns, basis, target)
    terms = [(weight, picked[index][0], picked[index][1])
             for index, weight in solution.items()]
    require(len(terms) == 188, "the exact order-six solution changed")
    return terms, commutator.expected_second_shadow()


def face_layers(terms):
    layers = {}
    for size in range(7):
        layer = Counter()
        for weight, _coefficient, directions in terms:
            for positions in combinations(range(6), size):
                face = tuple(sorted(directions[index] for index in positions))
                layer[face] += weight
        layers[size] = Counter({face: value for face, value in layer.items()
                                if value})
    return layers


def down_incidence(layer):
    answer = Counter()
    for face, coefficient in layer.items():
        for position in range(len(face)):
            subface = face[:position] + face[position + 1:]
            answer[subface] += coefficient
    return Counter({face: value for face, value in answer.items() if value})


def digest_layer(layer):
    return sha256(json.dumps(
        sorted((repr(face), str(value)) for face, value in layer.items()),
        separators=(",", ":"),
    ).encode()).hexdigest()


def audit():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected, ("pinned dependency changed", relative, actual))
    terms, expected_pair = exact_solution_terms()
    layers = face_layers(terms)

    require(not layers[0] and not layers[1],
            "empty/singleton Hasse incidence stopped cancelling")
    require(layers[2] == Counter(expected_pair),
            "the pair layer stopped being exact minus-delta")

    coherence = []
    for size in range(0, 6):
        left = down_incidence(layers[size + 1])
        right = Counter({face: (6 - size) * value
                         for face, value in layers[size].items()})
        require(left == right,
                ("unsigned Hasse incidence identity changed", size))
        coherence.append({
            "from_layer": size + 1,
            "to_layer": size,
            "factor": 6 - size,
            "identity": f"down(L_{size + 1})={(6 - size)}*L_{size}",
        })

    require(layers[2] and layers[3]
            and down_incidence(layers[3]) == Counter({
                face: 4 * value for face, value in layers[2].items()
            }), "the forced triple lift disappeared")

    return {
        "solution_terms": len(terms),
        "layer_nonzero_counts": {str(size): len(layer)
                                 for size, layer in layers.items()},
        "layer_l1": {str(size): str(sum(abs(value) for value in layer.values()))
                     for size, layer in layers.items()},
        "layer_total_coefficients": {
            str(size): str(sum(layer.values())) for size, layer in layers.items()
        },
        "layer_digests": {str(size): digest_layer(layer)
                          for size, layer in layers.items()},
        "coherence": coherence,
        "pair_layer": "exact sixteen-coordinate minus-delta",
        "triple_layer_nonzero": True,
        "zero_triple_with_nonzero_pair_possible_in_characteristic_zero": False,
        "reason": "down(L_3)=4*L_2",
        "interpretation": (
            "the higher faces are not contaminants to cancel; they are the "
            "forced coherent unsigned Hasse lift of the residual pair face"
        ),
        "physical_repeated_grade_totalization_proved": False,
    }


def main():
    ledger = {
        "theorem": "complete unsigned Hasse incidence of order-six residual lift",
        "audit": audit(),
        "scope": (
            "exact positional-subset incidence tower of the pinned 188-term "
            "operator solution.  This does not assign physical repeated-"
            "grade labels, alternating Spencer signs, or augmented readouts"
        ),
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"complete Hasse incidence ledger changed: {digest}")
    print("h3 residual-q order-six complete Hasse incidence: PASS")
    print("empty/singleton layers: zero")
    print("pair layer: exact minus-delta")
    print("higher layers: forced coherent lift; down(L3)=4*L2")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()

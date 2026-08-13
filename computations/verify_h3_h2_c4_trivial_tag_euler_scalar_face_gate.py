#!/usr/bin/env python3
"""Audit the Euler/product-rule lift of the unique C4 direction-tag line.

For the representative residual sites 2345, put

    H = q23*q45 + q24*q35 + q25*q34.

The three second-Hasse directions (D,q01), (p0,s1), (p1,s0) all send the
complete response polynomial to H.  Hence c=(2,-1,-1) is an exact apolar
relation.  It is not a source-algebra boundary.  The obvious logarithmic
Euler lift has zero face

    L01 = (2*D*q01 - p0*s1 - p1*s0)*H,

a nonzero nine-occurrence polynomial.  Its target augmentation is zero, but
it is an occurrence-centered scalar face.  A literal response-row point has
R=0 and L01=3, proving that response homogeneity does not kill the face.

Thus the C4 invariant is a face of the pointed occurrence comparison, not a
free Euler consequence.  Once this same word/fine/direction-grade face is
placed physically, the pinned augmented theorem gives the exact
filler-or-terminal alternative.
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
    "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py":
        "b03c096eb5bc4e6307cafa966f3d66d8c087e78bb8793c8448eec33f51e7e76a",
    "notes/h3-active-coloop-redistribution-second-hasse-face-classification.md":
        "985737011ea321c70096a89ea2a719db207c304d947ff4899133b39e14c46276",
    "computations/verify_h3_h2_direction_tag_maschke_c4_coinvariant_gate.py":
        "bee87b90c32720583f50d1c65dc2280dd337a46d197932d8c22aab802362d9ff",
    "notes/h3-h2-direction-tag-maschke-c4-coinvariant-gate.md":
        "f61147619b6758924c700fd3a4d99a1edb398ed9abc23f417fdf745209055d29",
    "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py":
        "ecb8725715747c3270fb069545309283d1890fbac6e66dfb6ed2f53b609e0030",
    "notes/h3-generic-symmetric-c4-placement-terminal-gate.md":
        "dcf0ef4adf500b4bee46ca301b12241e95ed1343a509a4fe4110d5dd3a906e92",
    "computations/verify_h3_trapped_carrier_occurrence_euler_source_gate.py":
        "f4139b38728165240d1b033852aba2189e8f1a721d90d2f997755be0a077e6d0",
    "notes/h3-trapped-carrier-occurrence-euler-source-gate.md":
        "92e185a39ccd8a934a7162d3018014a1651534789d8944686eb463453914f239",
    "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py":
        "8a9bfe47c934658d1b10ad42f283d6a017c27125bcb98615882e4bacd975f1eb",
    "notes/h3-o2-augmented-terminal-cap-cartan-extension-gate.md":
        "e9c0cf3c76cbe4c8061574d2b977bf1189a1fa299ef17ae1d2e463c08a313429",
}
EXPECTED_LEDGER_SHA256 = (
    "3b125fe7cd25b5a8f89cbae0c98a83228b851b8f05ea8e0b6291e378d0de1c78"
)


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


def polynomial_add(*terms):
    answer = Counter()
    for coefficient, polynomial in terms:
        for monomial, value in polynomial.items():
            answer[monomial] += Q(coefficient) * Q(value)
    return Counter({monomial: value for monomial, value in answer.items()
                    if value})


def hasse_face(polynomial, directions):
    directions = frozenset(directions)
    answer = Counter()
    for monomial, coefficient in polynomial.items():
        if directions.issubset(monomial):
            complement = tuple(variable for variable in monomial
                               if variable not in directions)
            answer[complement] += coefficient
    return Counter({monomial: value for monomial, value in answer.items()
                    if value})


def evaluate(polynomial, values):
    answer = Q(0)
    for monomial, coefficient in polynomial.items():
        value = Q(coefficient)
        for variable in monomial:
            value *= Q(values.get(variable, 0))
        answer += value
    return answer


def selected_euler_product(polynomial, selected):
    """Apply the product of logarithmic coordinate Euler projectors."""
    selected = frozenset(selected)
    return Counter({monomial: coefficient for monomial, coefficient
                    in polynomial.items() if selected.issubset(monomial)})


def literal_product_rule_audit(classification) -> dict[str, object]:
    _target, response_terms = classification.source_monomials()
    response = Counter({monomial: Q(1) for monomial in response_terms})
    q = classification.q
    p = classification.p
    s = classification.s
    direct = classification.D

    tails = (
        tuple(sorted((q(2, 3), q(4, 5)))),
        tuple(sorted((q(2, 4), q(3, 5)))),
        tuple(sorted((q(2, 5), q(3, 4)))),
    )
    direction_pairs = (
        frozenset((direct, q(0, 1))),
        frozenset((p(0), s(1))),
        frozenset((p(1), s(0))),
    )
    weights = (Q(2), Q(-1), Q(-1))
    response_faces = tuple(hasse_face(response, pair)
                           for pair in direction_pairs)
    expected_hafnian = Counter({tail: Q(1) for tail in tails})
    require(all(face == expected_hafnian for face in response_faces),
            response_faces)
    apolar_sum = polynomial_add(*zip(weights, response_faces, strict=True))
    require(not apolar_sum, apolar_sum)

    projectors = tuple(selected_euler_product(response, pair)
                       for pair in direction_pairs)
    require(all(len(projector) == 3 for projector in projectors),
            tuple(map(len, projectors)))
    scalar_face = polynomial_add(*zip(weights, projectors, strict=True))
    require(len(scalar_face) == 9 and sum(scalar_face.values(), Q(0)) == 0,
            scalar_face)
    require(tuple(sorted(Counter(scalar_face.values()).items()))
            == ((Q(-1), 6), (Q(2), 3)),
            Counter(scalar_face.values()))

    scalar_hasse_faces = tuple(hasse_face(scalar_face, pair)
                               for pair in direction_pairs)
    require(scalar_hasse_faces == tuple(
        Counter({tail: weight for tail in tails}) for weight in weights
    ), scalar_hasse_faces)

    # Monomials form a basis of the polynomial ring, so this support proves
    # L01 is not a polynomial identity.  It is also not proportional to the
    # local response aggregate, whose nine coefficients are all one.
    local_response = polynomial_add(*((Q(1), value) for value in projectors))
    require(len(local_response) == 9
            and scalar_face != local_response
            and len({scalar_face[monomial] / local_response[monomial]
                     for monomial in local_response}) == 2,
            "the scalar face became a response-row multiple")

    # A literal response-row quotient point: only one direct occurrence and
    # its p0,s1 mate survive.  The mixed target response is zero but L01=3.
    values = {
        direct: Q(1),
        q(0, 1): Q(1), q(2, 3): Q(1), q(4, 5): Q(1),
        p(0): Q(1), s(1): Q(-1),
    }
    response_value = evaluate(response, values)
    scalar_value = evaluate(scalar_face, values)
    require(response_value == 0 and scalar_value == 3,
            (response_value, scalar_value))

    # Every monomial covers all six sites once, so site Euler fields are
    # scalar on the response.  A type Euler with weights (a,b,c,d) on
    # (D,P,S,Q) preserves response homogeneity iff a+d=b+c.  Its induced
    # weights on DQ and on both PS orientations are then identical.
    homogeneous_weight_basis = (
        (Q(1), Q(1), Q(0), Q(0)),
        (Q(1), Q(0), Q(1), Q(0)),
        (Q(-1), Q(0), Q(0), Q(1)),
    )
    induced = []
    for a, b, c, d in homogeneous_weight_basis:
        require(a + d == b + c, (a, b, c, d))
        triple = (a + d, b + c, b + c)
        require(len(set(triple)) == 1
                and sum(weight * entry
                        for weight, entry in zip(weights, triple, strict=True))
                    == 0,
                triple)
        induced.append([str(value) for value in triple])

    # The nine-term scalar has occurrence augmentation zero.  In the full
    # 105-occurrence response coordinate module it lies in the centered
    # image, with C_105 v=105v.  This is a P_f-type scalar face, not zero.
    occurrence_vector = tuple(scalar_face.get(monomial, Q(0))
                              for monomial in response_terms)
    require(sum(occurrence_vector, Q(0)) == 0
            and sum(value != 0 for value in occurrence_vector) == 9,
            occurrence_vector)
    centered_image = tuple(
        Q(105) * value - sum(occurrence_vector, Q(0))
        for value in occurrence_vector
    )
    require(centered_image == tuple(Q(105) * value
                                    for value in occurrence_vector),
            "the centered occurrence identity changed")
    primitive_dual = tuple(value / Q(18) for value in occurrence_vector)
    require(sum(left * right for left, right
                in zip(primitive_dual, occurrence_vector, strict=True)) == 1,
            "the local scalar dual normalization changed")

    return {
        "representative_direction_pairs": [
            [repr(value) for value in sorted(pair)]
            for pair in direction_pairs
        ],
        "common_second_Hasse_face": [repr(tail) for tail in tails],
        "direction_tag_coefficients": [str(value) for value in weights],
        "apolar_H2_combination": 0,
        "literal_log_Euler_lift": (
            "2 E_D E_q01(R) - E_p0 E_s1(R) - E_p1 E_s0(R)"
        ),
        "scalar_zero_face": (
            "(2 D q01-p0 s1-p1 s0)"
            "(q23 q45+q24 q35+q25 q34)"
        ),
        "scalar_face_occurrences": len(scalar_face),
        "scalar_face_coefficient_profile": {"2": 3, "-1": 6},
        "target_augmentation": str(sum(scalar_face.values(), Q(0))),
        "response_row_countermodel": {
            "nonzero_variables": {repr(key): str(value)
                                  for key, value in values.items()},
            "response_value": str(response_value),
            "scalar_face_value": str(scalar_value),
            "scope": "literal complete-response row; not all GHZ equations",
        },
        "homogeneous_type_Euler_basis_induced_pair_weights": induced,
        "homogeneous_Euler_generates_C4_tag": False,
        "raw_log_Euler_preserves_response_ideal": False,
        "full_response_occurrences": len(response_terms),
        "centered_occurrence_identity": "C_105 L01=105 L01",
        "primitive_scalar_dual": "L01/18 in the 105 occurrence coordinates",
        "interpretation": (
            "the C4 tag is an exact H2 annihilator, but its first integrated "
            "proper face is a nonzero target-zero centered occurrence scalar"
        ),
    }


def distinguish_lower_c4_and_terminal() -> dict[str, object]:
    generic = load(
        "computations/verify_h3_generic_symmetric_c4_placement_terminal_gate.py",
        "h2_c4_symmetric_tail",
    )
    generic_ledger, generic_digest = generic.audit()
    require(generic_digest == generic.EXPECTED_LEDGER_SHA256,
            "the symmetric lower-C4 ledger changed")

    terminal = load(
        "computations/verify_h3_o2_augmented_terminal_cap_cartan_extension_gate.py",
        "h2_c4_tag_terminal",
    )
    terminal_ledger, terminal_digest = terminal.audit()
    require(terminal_digest == terminal.EXPECTED_LEDGER_SHA256,
            "the augmented terminal ledger changed")
    fork = terminal_ledger["post_placement_dichotomy"]
    require(fork["third_branch"] is False,
            "the filler-or-terminal fork acquired a third branch")
    return {
        "tensor_factor_distinction": {
            "current_direction_factor": "2 e_DQ-e_PS01-e_PS10",
            "lower_tail_factor": "q23q45+q24q35+q25q34",
            "integrated_scalar": "direction factor tensor lower-tail factor",
            "generic_lower_C4_placement_already_constructed": False,
            "generic_lower_C4_ledger": generic_digest,
        },
        "same_grade_requirement": (
            "the centered scalar must retain the original response word, fine "
            "grade and H2 direction-pair object before terminal promotion"
        ),
        "post_placement_alternative": fork["exact_alternative"],
        "third_branch": fork["third_branch"],
        "terminal_extension_rows": "q/ainc/target/W/ores/ridge",
        "consequence": (
            "if the centered occurrence scalar has no protected-zero filler "
            "in the exhaustive same-grade physical map, its primitive dual "
            "extends by 4373ae6 to an accepted augmented terminal"
        ),
    }


def audit() -> tuple[dict[str, object], str]:
    pin_dependencies()
    classification = load(
        "computations/verify_h3_active_coloop_redistribution_second_hasse_face_classification.py",
        "h2_c4_tag_classification",
    )
    ledger = {
        "theorem": "h3 C4 trivial direction-tag Euler/scalar-face gate",
        "pins": PINS,
        "literal_product_rule": literal_product_rule_audit(classification),
        "lower_tail_and_terminal_scope": distinguish_lower_c4_and_terminal(),
        "shortest_positive_theorem": (
            "construct the pointed occurrence comparison on the displayed "
            "nine-term target-zero scalar L01, retaining its word/fine/H2 "
            "direction tags.  Its second-Hasse face is the sole C4 tag "
            "coinvariant.  Failure of a protected filler then promotes to "
            "the existing augmented terminal; Euler homogeneity alone does "
            "not supply the comparison."
        ),
        "frontier_effect": (
            "the C4 survivor is not a new coefficient identity: it is the "
            "second-Hasse face of the same pointed occurrence/AugP2 type.  "
            "Its local scalar placement remains open and is distinct from "
            "the downstream P2 word-0102 private landing."
        ),
        "scope": (
            "exact uncoloured canonical h=3 response algebra and conditional "
            "augmented promotion.  The response-row countermodel is not a "
            "complete GHZ source, and no physical pointed placement is "
            "constructed here."
        ),
    }
    digest = sha256(json.dumps(ledger, sort_keys=True,
                               separators=(",", ":")).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest, EXPECTED_LEDGER_SHA256))
    return ledger, digest


def main() -> None:
    _ledger, digest = audit()
    require(EXPECTED_LEDGER_SHA256 != "TO_BE_FROZEN",
            ("freeze EXPECTED_LEDGER_SHA256", digest))
    print("C4 tag 2DQ-PS-PS: EXACT SECOND-HASSE ANNIHILATOR")
    print("Euler/source boundary: NO; scalar face L01 is nonzero")
    print("L01 occurrence support 9; target augmentation 0")
    print("response-row countermodel: R=0, L01=3")
    print("after same-grade placement: FILLER OR AUGMENTED TERMINAL")
    print("ledger_sha256=" + digest)


if __name__ == "__main__":
    main()

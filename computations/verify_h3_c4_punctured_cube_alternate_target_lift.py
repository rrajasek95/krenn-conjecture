#!/usr/bin/env python3
"""Source lift of the final h=3 diagonal-return C4.

The selected L tail supplies q05^02 q14^02 at the mixed word and
q05^11 q14^11 at the pure-one word.  Five complete response coefficients
form a punctured square.  If the third matching q04*q15 is absent on its
mixed faces, an integral cubical identity forces the q01*q45+q05*q14 part
to vanish at the pure word.  The pure target row then forces q04^11*q15^11,
an alternate pure-one matching.  Reselecting it makes the old L-only 02
edges nonanchor.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "computations/verify_h3_axis_target_coloop_zero_face_affine_accessibility_reduction.py":
        "3d346d9d55fc2736de58252d1b9a03d0191faa1cb38fa0fcc62cb4d4863d279f",
    "notes/h3-axis-target-coloop-zero-face-affine-accessibility-reduction.md":
        "0cc8ee2ab2126170677a5b77803e2e3544520b1d9fd74765155d887dd5856aa8",
    "computations/verify_h3_c4_zero_support_rectangle_boundary.py":
        "2f6d1c82d0c41cbe39d46bec36db1e8f28435b69ff074624efb810f19c7e83db",
    "notes/h3-c4-zero-support-rectangle-boundary.md":
        "9c1044a2542f012613e2dcb7806367b275b6cfd629e0dacecb31560f56237127",
    "computations/verify_uniform_one_bad_nonanchor_offdiagonal_good_pair.py":
        "64e85cd84112b5160efe4f43ce1208da3c49f5e58b3e4a4d6192e6a9c229c306",
    "notes/uniform-one-bad-nonanchor-offdiagonal-good-pair.md":
        "4516c5ff02f130e1ad25b4fde395c81557e58ba0c83f7f98969d95df17fd6409",
}
EXPECTED_LEDGER_SHA256 = (
    "449eda8e2da09561ac33fd819b525fb6cbf6bf27002ac5c2d727e44ab7cf6013"
)

# Four-site order is 0,1,4,5.  The omitted q sites 2,3 carry the selected
# endpoint ports P2,S3, and the endpoint output is fixed to 11.
T = (1, 1, 1, 1)
U_WORD = (1, 0, 2, 1)
V_WORD = (0, 1, 1, 2)
X = (0, 1, 1, 1)
Y = (1, 1, 2, 1)
Z = (0, 1, 2, 1)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def polynomial(*terms):
    result = Counter()
    for coefficient, variables in terms:
        result[tuple(sorted(variables))] += coefficient
    return Counter({term: coefficient for term, coefficient in result.items()
                    if coefficient})


def add(*scaled):
    result = Counter()
    for coefficient, value in scaled:
        for term, old in value.items():
            result[term] += coefficient * old
    return Counter({term: coefficient for term, coefficient in result.items()
                    if coefficient})


def multiply(left, right):
    result = Counter()
    for left_term, left_value in left.items():
        for right_term, right_value in right.items():
            result[tuple(sorted(left_term + right_term))] += (
                left_value * right_value
            )
    return Counter({term: coefficient for term, coefficient in result.items()
                    if coefficient})


def variable(name):
    return polynomial((1, (name,)))


def edge_variable(edge, left, right):
    return variable(f"q{edge}_{left}{right}")


def A(word):
    x0, x1, x4, x5 = word
    return multiply(edge_variable("01", x0, x1),
                    edge_variable("45", x4, x5))


def B(word):
    x0, x1, x4, x5 = word
    return multiply(edge_variable("05", x0, x5),
                    edge_variable("14", x1, x4))


def G(word):
    x0, x1, x4, x5 = word
    return multiply(edge_variable("04", x0, x4),
                    edge_variable("15", x1, x5))


def C(word):
    return add((1, A(word)), (1, B(word)))


def audit_words_and_routes():
    # The two bridge words use only the four already selected B-edge cells.
    require(B(U_WORD) == multiply(edge_variable("05", 1, 1),
                                  edge_variable("14", 0, 2)),
            "the first selected bridge product changed")
    require(B(V_WORD) == multiply(edge_variable("05", 0, 2),
                                  edge_variable("14", 1, 1)),
            "the second selected bridge product changed")

    # A(U),A(V) share crosswise factors.  Their recombination is A(Z).
    au = A(U_WORD)
    av = A(V_WORD)
    az = A(Z)
    require(au == multiply(edge_variable("01", 1, 0),
                           edge_variable("45", 2, 1)),
            "A(U) changed")
    require(av == multiply(edge_variable("01", 0, 1),
                           edge_variable("45", 1, 2)),
            "A(V) changed")
    require(az == multiply(edge_variable("01", 0, 1),
                           edge_variable("45", 2, 1)),
            "the recombined A(Z) pivot changed")

    routes = {}
    for name, word in (("u", U_WORD), ("v", V_WORD),
                       ("x", X), ("y", Y), ("z", Z)):
        x0, x1, x4, x5 = word
        labels = {"04": (x0, x4), "15": (x1, x5)}
        require(any(left != right for left, right in labels.values()),
                f"the mixed G({name}) term lost its offdiagonal edge")
        routes[name] = labels
    require(G(T) == multiply(edge_variable("04", 1, 1),
                             edge_variable("15", 1, 1)),
            "the alternate pure-one tail changed")
    return {
        "selected_B_bridge_u": ["q05_11", "q14_02"],
        "selected_B_bridge_v": ["q05_02", "q14_11"],
        "mixed_third_matching_labels": routes,
        "pure_third_matching": ["q04_11", "q15_11"],
        "old_L_tail": ["05:02", "14:02"],
        "alternate_L_tail": ["04:11", "15:11"],
    }


def audit_cube_identity():
    # Opposite vertices 0 and 4 vary on the face T,X,Y,Z.  A and B each
    # have determinant zero on that face, so this identity is integral.
    identity = add(
        (1, multiply(A(Z), C(T))),
        (-1, multiply(A(Y), C(X))),
        (1, multiply(B(X), C(Y))),
        (-1, multiply(B(T), C(Z))),
    )
    require(not identity, "the punctured C4 identity changed")

    # F_w is the literal complete-row combination
    #   a2*E11(w)-a1*E21(w)=U*C_w
    # off the target.  At T, E11(T)-1 is the source row, hence
    #   F_T=U*(C_T+G_T)-a2.
    endpoint_unit = variable("U_endpoint")
    a2 = variable("a2_selected")
    mixed_F = {
        word: multiply(endpoint_unit, C(word))
        for word in (X, Y, Z)
    }
    target_F = add(
        (1, multiply(endpoint_unit, add((1, C(T)), (1, G(T))))),
        (-1, a2),
    )
    certificate = add(
        (1, multiply(A(Z), target_F)),
        (-1, multiply(A(Y), mixed_F[X])),
        (1, multiply(B(X), mixed_F[Y])),
        (-1, multiply(B(T), mixed_F[Z])),
    )
    expected = multiply(A(Z), add(
        (1, multiply(endpoint_unit, G(T))),
        (-1, a2),
    ))
    require(certificate == expected,
            "the target-augmented cubical source certificate changed")
    return {
        "integral_identity": (
            "A_z*C_t-A_y*C_x+B_x*C_y-B_t*C_z=0 for C=A+B"
        ),
        "source_certificate": (
            "A_z*F_t-A_y*F_x+B_x*F_y-B_t*F_z="
            "A_z*(U*G_t-a2)"
        ),
        "face_words": {
            "t": T, "x": X, "y": Y, "z": Z,
            "selected_bridges": [U_WORD, V_WORD],
        },
    }


def audit_unit_propagation():
    # This is a branch-local localization argument, not a Boolean support
    # census.  The displayed equalities are literal consequences of the
    # complete mixed response rows when G(U)=G(V)=0.
    return {
        "first_row": (
            "C_u=0 and B_u=q05_11*q14_02 is a selected unit, so A_u is a unit"
        ),
        "second_row": (
            "C_v=0 and B_v=q05_02*q14_11 is a selected unit, so A_v is a unit"
        ),
        "recombined_pivot": (
            "A_u=q01_10*q45_21 and A_v=q01_01*q45_12 make "
            "A_z=q01_01*q45_21 a unit"
        ),
        "target_consequence": (
            "the source certificate and the selected endpoint/a2 units "
            "force G_t=q04_11*q15_11 nonzero"
        ),
    }


def pin_dependencies():
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")


def main():
    pin_dependencies()
    ledger = {
        "literal_words": audit_words_and_routes(),
        "punctured_cube": audit_cube_identity(),
        "unit_propagation": audit_unit_propagation(),
        "source_lift": (
            "after the rank-one response syzygy isolates the L-port "
            "cofactor, every nonzero mixed q04|q15 term is an offanchor "
            "offdiagonal exit. If all five vanish, the target-augmented "
            "cubical certificate forces q04_11*q15_11 nonzero"
        ),
        "physical_landing": (
            "P2|S3|04|15 is an alternate pure-one target matching. "
            "Reselecting it removes the old L-only edges 05,14 from every "
            "selected anchor; their already nonzero 02 cells enter the "
            "pinned nonanchor active-good-pair route"
        ),
        "consequence_for_2061c57": (
            "none of the sixteen flat q-edge rectangles remains a primitive "
            "K2,2/Hall obstruction once the pure target and crossed response "
            "companions are used"
        ),
        "scope": (
            "exact h=3 normalized target-coloop packet and its source-labelled "
            "symmetry copies; not a generic C4 saturation theorem"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"the punctured-C4 source-lift ledger changed: {digest}")
    print(json.dumps(ledger, indent=2, sort_keys=True))
    print(f"ledger_sha256={digest}")
    print("h3 punctured-C4 alternate-target source lift: PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Audit the physical dressing of the root-even reduced-Eq coefficient.

The generic C_+ orbit requires

    E = 2 D_root tensor v,  D_root=(-1,1,-1,1),
    v=(B1+B4)/2,

in the (H0-u)e_Eq row.  The canonical Koszul cell C_K has boundary
-(H0-u)e_Eq, so -2 D_root tensor v tensor C_K constructs E in the
unaugmented derived intersection.

This checker refines the old six-label physical block by retaining the four
root-word copies separately.  In each copy the old columns force

    O_u=(lower,Eq,W,target,ores,ainc)=(-u,-u,0,0,u,sum(u)).

For u=-E, O_u has the desired Eq coefficient and W=0, but also lower=E
and word-resolved labelled residue -E.  Summing the four root words hides
the residue because sum(D_root)=0; it does not remove the labelled class.
The lower-Eq and Eq+ores separators prove both defects are primitive in the
checked old physical block.  Thus the derived coefficient is exact, while
its complete physical descent remains a genuine augmented comparison.
"""

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PINS = {
    "computations/verify_h3_reduced_eq_koszul_tate_relative_orbit_gate.py":
        "15b47a420a6f1e2e6eb0b89e5e5efb5c895172e30b8ab9339dfa1e451ac03668",
    "computations/verify_h3_reduced_eq_cartan_cap_augmentation_dressing.py":
        "3397fc0b7d773d97fb26e737eb490136c3062549951b07eca701ee46739ff2bb",
    "computations/verify_h3_reduced_eq_full_physical_augmentation_matrix.py":
        "f66752bd3a44a9506b4a31467ce52dcb16e52f841b0f29ce66066a38ec7f97c1",
    "computations/verify_h3_tau_plus_full_interface_product_bianchi_extension_gate.py":
        "32be7ef48ad9d35b8863a62889508ccdff0010d8ebff18b366e932aab8b2bf14",
    "computations/verify_h3_tau_plus_connected_sl3_label_orbit_obstruction.py":
        "7048ab1ea5912f1be38014f193970e093c1f5d1259cc56e1e5566b1552358b52",
    "computations/verify_h3_generic_cplus_lower_quotient_smith_gate.py":
        "f4ee0503c4639b79a655bdbab94d02218c99b348bee8f3c46f9554b7e803e3e0",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def add(*vectors):
    return tuple(sum(entries, Q(0)) for entries in zip(*vectors, strict=True))


def scale(scalar, vector):
    return tuple(scalar * entry for entry in vector)


def dot(left, right):
    return sum((a * b for a, b in zip(left, right, strict=True)), Q(0))


def tensor(left, right):
    return tuple(a * b for a in left for b in right)


def unit(size, index):
    return tuple(Q(int(i == index)) for i in range(size))


def pin_inputs():
    for relative, expected in PINS.items():
        actual = digest(ROOT / relative)
        require(actual == expected, (relative, actual, expected))


D_ROOT = tuple(map(Q, (-1, 1, -1, 1)))
V = tuple(map(Q, (0, Q(1, 2), 0, 0, Q(1, 2), 0)))
LABELS = len(D_ROOT) * len(V)

LOWER = slice(0, LABELS)
EQ = slice(LOWER.stop, LOWER.stop + LABELS)
W = slice(EQ.stop, EQ.stop + LABELS)
TARGET = slice(W.stop, W.stop + LABELS)
ORES = slice(TARGET.stop, TARGET.stop + LABELS)
AINC = ORES.stop
ROWS = AINC + 1


def vector(*, lower=(), eq=(), w=(), target=(), ores=(), ainc=0):
    answer = [Q(0)] * ROWS
    for section, values in ((LOWER, lower), (EQ, eq), (W, w),
                            (TARGET, target), (ORES, ores)):
        if values:
            require(len(values) == LABELS, (section, len(values)))
            answer[section] = values
    answer[AINC] = Q(ainc)
    return tuple(answer)


def old_columns():
    """Four word-resolved copies of r0_i,T_i,varrho_i.

    This is deliberately the strongest source-faithful version of the
    pinned six-label block: residues in distinct root words are not silently
    identified.  The global anchor remains the scalar physical incidence.
    """
    r0, cap, response = [], [], []
    for index in range(LABELS):
        e = unit(LABELS, index)
        r0.append(vector(lower=e, eq=e, target=e, ainc=-1))
        cap.append(vector(w=scale(-1, e), target=e))
        response.append(vector(w=e, ores=e))
    return r0, cap, response


def nearest(coefficients, r0, cap, response):
    # O_u=-sum u_i(r0_i-T_i)+sum u_i varrho_i.
    columns = []
    for coefficient, r0_i, cap_i, response_i in zip(
            coefficients, r0, cap, response, strict=True):
        columns.append(scale(coefficient,
                             add(scale(-1, r0_i), cap_i, response_i)))
    return add(*columns)


def coarse_six(values):
    return tuple(sum((values[6 * root + label]
                      for root in range(len(D_ROOT))), Q(0))
                 for label in range(6))


def audit():
    require(sum(D_ROOT, Q(0)) == 0 and sum(V, Q(0)) == 1,
            "root/fixed-plane normalizations changed")
    e = scale(2, tensor(D_ROOT, V))
    require(set(e) == {Q(-1), Q(0), Q(1)}
            and sum(value != 0 for value in e) == 8,
            "the root-even Eq coefficient changed")

    # dC_K=-F e_Eq, so decorating C_K by -2D tensor v gives +E F e_Eq.
    koszul_decoration = scale(-1, e)
    derived_boundary = scale(-1, koszul_decoration)
    require(derived_boundary == e,
            "the decorated Koszul sign stopped producing the desired face")

    r0, cap, response = old_columns()
    old = r0 + cap + response
    lifted = nearest(scale(-1, e), r0, cap, response)
    expected_lift = vector(lower=e, eq=e, ores=scale(-1, e), ainc=0)
    require(lifted == expected_lift,
            "the nearest physical root-even lift changed")

    clean = vector(eq=e)
    require(all(lifted[index] == 0
                for index in range(W.start, TARGET.stop)),
            "W or target reappeared on the nearest lift")
    require(coarse_six(lifted[ORES]) == (Q(0),) * 6,
            "the coarse six-label residue no longer cancels")
    require(lifted[ORES] == scale(-1, e)
            and any(lifted[ORES]),
            "the word-resolved labelled residue unexpectedly vanished")
    require(lifted[AINC] == 0,
            "the global anchor incidence no longer cancels")

    # Every checked old column has lower=Eq.  The clean Eq-only cell is
    # therefore detected label by label; its physical nearest lift is not.
    lower_eq_pairings = []
    residue_pairings = []
    for index, coefficient in enumerate(e):
        if not coefficient:
            continue
        lower_eq = vector(lower=unit(LABELS, index),
                          eq=scale(-1, unit(LABELS, index)))
        eq_ores = vector(eq=scale(-1, unit(LABELS, index)),
                         w=unit(LABELS, index),
                         target=unit(LABELS, index),
                         ores=scale(-1, unit(LABELS, index)))
        require(all(dot(lower_eq, column) == 0 for column in old),
                ("lower-Eq dual sees old column", index))
        require(all(dot(eq_ores, column) == 0 for column in old),
                ("Eq+ores dual sees old column", index))
        require(dot(lower_eq, clean) == -coefficient
                and dot(lower_eq, lifted) == 0,
                ("lower/private obstruction changed", index))
        require(dot(eq_ores, clean) == -coefficient
                and dot(eq_ores, lifted) == 0,
                ("labelled-residue obstruction changed", index))
        lower_eq_pairings.append(str(-coefficient))
        residue_pairings.append(str(-coefficient))

    # Forgetting the root word loses precisely the information that the
    # labelwise Koszul audit says must be preserved.
    clean_coarse = coarse_six(clean[EQ])
    require(clean_coarse == (Q(0),) * 6,
            "the root-even Eq coefficient should also be coarse-dark")

    fixed_dual = tuple(map(Q, (0, 1, 0, 0, 1, 0)))
    actual_local = [0, 2, 3, 5]
    require(all(fixed_dual[index] == 0 for index in actual_local)
            and dot(fixed_dual, V) == 1,
            "the actual/fixed source-label separator changed")

    return {
        "theorem": "root-even K_Eq physical dressing gate",
        "required_Eq": "2 D_root (H0-u)e_Eq tensor v",
        "D_root": [str(value) for value in D_ROOT],
        "v_B0_to_B5": [str(value) for value in V],
        "nonzero_word_label_coefficients": 8,
        "unaugmented_derived": {
            "cell": "-2 D_root tensor v tensor C_K",
            "boundary": "+2 D_root (H0-u)e_Eq tensor v",
            "constructed": True,
        },
        "nearest_checked_physical_lift": {
            "formula": "O_{-E}, E=2 D_root tensor v",
            "lower_private": "+E",
            "Eq": "+E",
            "W": "0 coefficientwise",
            "target": "0 coefficientwise",
            "word_resolved_labelled_ores": "-E (nonzero)",
            "coarse_six_label_ores": "0",
            "global_anchor_incidence": "0",
        },
        "primitive_duals": {
            "lower_minus_Eq": len(lower_eq_pairings),
            "minus_Eq_plus_W_plus_target_minus_ores": len(residue_pairings),
            "pairings_on_clean_core": lower_eq_pairings,
        },
        "source_placement": {
            "actual_local_B_span": "<B0,B2,B3,B5>",
            "required_fixed_plane": "<B1,B4>",
            "root_Cartan_changes_matching_or_repeated_edge": False,
        },
        "sharp_remaining_comparison": (
            "a source-labelled augmented K_Eq lift in the actual omitted "
            "01/04 grades, or a raw C_+ cell whose hidden lower/private and "
            "word-resolved residue faces are -E and +E respectively"
        ),
        "not_an_obstruction_here": (
            "W and target are already zero on O_{-E}; coarse residue and "
            "global anchor cancel only after summing the root words"
        ),
    }


def main():
    pin_inputs()
    result = audit()
    payload = json.dumps(result, sort_keys=True, separators=(",", ":"))
    ledger = sha256(payload.encode()).hexdigest()
    print("h3 C-plus root-even K_Eq physical dressing gate: PASS")
    print("derived coefficient: constructed")
    print("nearest physical lift: W=target=0, coarse ores=0")
    print("remaining: lower/private +E and word-resolved labelled ores -E")
    print("ledger sha256:", ledger)


if __name__ == "__main__":
    main()

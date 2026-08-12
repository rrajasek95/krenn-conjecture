#!/usr/bin/env python3
"""Target-normalized abcde lift and the 0373033 generator dichotomy.

The wrong-typed pure unary abcde column can be completed by the old target
cap, split residue, and pure ordinary-residue column to a clean lower lift

    x=(lower=1, ainc=-1, W=tgt=ores=0).

Let J0 retain lower boundary, W, target, and ordinary residue, and let q be
physical anchor incidence.  Corrections of x form x+ker(J0).  Over a
characteristic-zero field, U=(1,0,0,0,0) exists iff q is nonzero on
ker(J0); in that case 0373033 already turns the ambiguity into a primitive
relative anchor generator.  Conversely U-x is itself such an ambiguity.

More strongly, if the formal cyclic comparison package A is physically
realized with (lower=5,ainc=W=tgt=ores=0), then A-5*x is a kernel element
of anchor value 5, so a relative generator follows immediately.  Thus a
physical A makes explicit construction of U unnecessary.  Without A, the
zero-indeterminate branch is only a separator on the lower-lift fibre; it
does not define the rootless polar/Fredholm map.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_LEDGER_SHA256 = "dbe3f110b5d7667d68f17cb5ea422efa6d9e45b8bf13062bc6ffc4bd36524c64"
PINS = {
    "computations/verify_h3_derived_terminal_indeterminacy_or_relative_generator.py":
        "9327b57598a5264c11e5c3085e1afceaec8fd72c408f5fc1f1eaa2490a13a8b1",
    "computations/verify_h3_rootless_abcde_unary_relative_augmentation_obstruction.py":
        "95115a771379bb09511b1d2f5f6758834af8bf7ed19734e8beadd4f5122919a5",
    "computations/verify_h3_rootless_clean_separator_repeated_inventory_gate.py":
        "af9a69ad996bd4390ff3fe9139e357a3bb765292ec969350a948612d9b824fa7",
    "computations/verify_h3_rootless_abcde_relative_matching_cell_obstruction.py":
        "39a4c24a23f8c315f6a90a9768aff6cc3061c51528b0a66594e22f8182f717af",
}

ROWS = ("lower_abcde", "ainc", "W", "target", "ores")


def require(condition: bool, message: object) -> None:
    if not condition:
        raise RuntimeError(message)


def add(*values):
    return tuple(sum(value[index] for value in values)
                 for index in range(len(ROWS)))


def scale(coefficient, value):
    coefficient = Q(coefficient)
    return tuple(coefficient * Q(entry) for entry in value)


def target_normalized_lift():
    records = []
    for y in (Q(1), Q(2), Q(-3), Q(5)):
        unary = (Q(1), Q(-1), Q(0), Q(1), Q(0))
        target_cap = (Q(0), Q(0), -y, Q(1), Q(0))
        split_residue = (Q(0), Q(0), Q(1), Q(0), Q(1))
        pure_ores = (Q(0), Q(0), Q(0), Q(0), Q(1))
        # x=R-T-Y*rho+Y*d.
        x = add(unary, scale(-1, target_cap),
                scale(-y, split_residue), scale(y, pure_ores))
        require(x == (Q(1), Q(-1), Q(0), Q(0), Q(0)),
                ("target-normalized lower lift changed", y, x))
        records.append({
            "Y": str(y),
            "formula": "x=R-T-Y*rho+Y*d_ores",
            "x": [str(entry) for entry in x],
        })
    return records


def generator_dichotomy():
    x = (Q(1), Q(-1), Q(0), Q(0), Q(0))
    U = (Q(1), Q(0), Q(0), Q(0), Q(0))
    U_minus_x = add(U, scale(-1, x))
    require(U_minus_x == (Q(0), Q(1), Q(0), Q(0), Q(0)),
            "U-x stopped being a pure anchor kernel element")
    normalized_from_U = scale(-1, U_minus_x)
    require(normalized_from_U == (Q(0), Q(-1), Q(0), Q(0), Q(0)),
            "U stopped producing the primitive relative generator")

    # If k lies in ker J0 and q(k)!=0, 0373033 normalizes -k/q(k).
    # Conversely choose k/q(k) so its anchor value is +1; x+k/q(k)=U.
    sample_kernel_values = (Q(-3), Q(-1), Q(1), Q(5, 2))
    samples = []
    for value in sample_kernel_values:
        k = (Q(0), value, Q(0), Q(0), Q(0))
        generator = scale(Q(-1, 1) / value, k)
        adjusted = add(x, scale(Q(1, 1) / value, k))
        require(generator == (Q(0), Q(-1), Q(0), Q(0), Q(0)),
                "037 normalization changed")
        require(adjusted == U,
                "nonzero anchor ambiguity stopped producing U")
        samples.append({
            "q(k)": str(value),
            "normalized_generator": [str(entry) for entry in generator],
            "adjusted_lift": [str(entry) for entry in adjusted],
        })

    # Conditional physical cyclic package.  Its lower boundary is five and
    # all four physical readouts vanish.  A-5x is therefore already the
    # kernel witness needed by 0373033.
    A = (Q(5), Q(0), Q(0), Q(0), Q(0))
    z = add(A, scale(-5, x))
    require(z == (Q(0), Q(5), Q(0), Q(0), Q(0)),
            "A-5x stopped being the conditional kernel witness")
    generator_from_A = scale(Q(-1, 5), z)
    require(generator_from_A
            == (Q(0), Q(-1), Q(0), Q(0), Q(0)),
            "physical A stopped forcing the relative generator")
    U_from_A = scale(Q(1, 5), A)
    require(U_from_A == U,
            "physical A/5 stopped having the desired U signature")

    return {
        "clean_lower_lift_x": [str(entry) for entry in x],
        "desired_U": [str(entry) for entry in U],
        "U_minus_x": [str(entry) for entry in U_minus_x],
        "U_exists_iff_anchor_indeterminacy_nonzero": True,
        "nonzero_indeterminacy_samples": samples,
        "conditional_physical_cyclic_A": [str(entry) for entry in A],
        "A_minus_5x": [str(entry) for entry in z],
        "normalized_generator_from_A": [
            str(entry) for entry in generator_from_A
        ],
        "U_signature_from_A_over_5": [str(entry) for entry in U_from_A],
        "consequence": (
            "once A is a physically typed correction chain, 0373033 lands "
            "immediately in its relative-generator branch; equivalently "
            "A/5 already has the U signature"
        ),
    }


def main() -> None:
    for relative, expected in PINS.items():
        actual = sha256((ROOT / relative).read_bytes()).hexdigest()
        require(actual == expected,
                f"pinned dependency changed: {relative}: {actual}")
    ledger = {
        "theorem": "abcde target normalization and generator dichotomy",
        "row_order": list(ROWS),
        "target_normalization": target_normalized_lift(),
        "dichotomy": generator_dichotomy(),
        "typing": {
            "J0_rows": ["lower_abcde", "W", "target", "ores"],
            "q_row": "physical pure-anchor incidence",
            "same_fine_grade_required": True,
            "cap_residue_multiplier": (
                "the unary, T, rho, and pure-ores columns are multiplied "
                "into the same abcde source grade"
            ),
            "formal_chart_anchor_is_physical_q": False,
        },
        "zero_indeterminate_branch": (
            "q kills ker J0, so every clean lower lift has anchor -1 and U "
            "does not exist.  This is only a separator on the lower-lift "
            "fibre; without a physical comparison A/P it is not the "
            "rootless Macaulay annihilator and Fredholm is not yet invocable"
        ),
        "verdict": (
            "the old cap block removes target/W/ores from the unary abcde "
            "column but leaves anchor -1.  The 0373033 alternative neither "
            "constructs the missing physical comparison nor requires U: "
            "nonzero ambiguity gives the relative generator, while any "
            "physical cyclic comparison A forces that ambiguity via A-5x"
        ),
        "scope": (
            "exact coarse augmented readouts in one common abcde grade; the "
            "physical existence of the cyclic comparison chain A remains "
            "the load-bearing source-typing hypothesis"
        ),
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                ("ledger digest changed", digest))
    print("h3 rootless abcde target-normalization dichotomy: PASS")
    print("clean lower lift: (1,-1,0,0,0)")
    print("U iff nonzero anchor indeterminacy; then 037 gives generator")
    print("physical cyclic A => generator through A-5x")
    print("zero-indeterminate fibre alone invokes Fredholm: NO")
    print("ledger sha256:", digest)


if __name__ == "__main__":
    main()

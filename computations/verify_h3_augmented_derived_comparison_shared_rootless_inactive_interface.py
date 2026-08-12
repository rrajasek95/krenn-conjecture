#!/usr/bin/env python3
"""Audit the shared derived comparison interface for Components III and IV.

This is a conditional theorem-interface checker.  It composes four already
certified facts without claiming the missing derived-to-physical comparison:

* the chart syzygy k_v has marked boundary h_v Yw;
* the indexed Hasse/Koszul chain n_v realizes d n_v = h_v Yw with zero
  target and ordinary residue and terminal correction -1;
* a primitive target/residue-zero anchor face closes the localized rootless
  pentagon; and
* a physical cap column (0,1,0,0) is exactly the missing Component-IV
  direction.

On D(h_v), the same n_v is the normalized candidate for the inactive cap
lift after scaling by kappa/h_v.  It becomes either physical cell only if
one augmented comparison also identifies the chart correction with
primitive anchor incidence and derived Yw with the physical cap line.
"""

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QQ = Fraction
PINS = {
    "computations/verify_h3_non_euler_chart_h1_first_comparison_gate.py":
        "f96cf470fc09255dd092b0d904c2aa85bab3d9ca6966c48c383a19b5ce31e54d",
    "computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py":
        "7d9e49f34da84772f6e0863a9bfe56cb9a90e0cfd3fceb76da59175ffea36c50",
    "computations/verify_h3_rootless_five_cycle_positive_interface.py":
        "fd359b3ff2abbb01d9508996c754a27b70890b2cd621926fc30b92057b337851",
    "computations/verify_h3_component_iv_cyclotomic_rees_lift_physical_separator.py":
        "12f7edba228a034523c61f10fc7633c7c736516dd3890ab3a89fce376eaa49bb",
    "notes/h3-non-euler-chart-h1-first-comparison-gate.md":
        "3e9c6fe01318005628c0ab9a28d840bf2f05958bcad9608887cff82cb769e852",
    "notes/h3-shifted-denominator-chart-filler-augmented-commutator.md":
        "1d89c1e592fdc723bb58b1b75e2ba846b812401efad33c8cd88d4265dc0a7743",
    "notes/h3-rootless-five-cycle-positive-interface.md":
        "0d9ae0107a8e62d9765a8bc7b3d9b8c1b733bea2344c3e5c48b6ce61baf33a4c",
    "notes/h3-component-iv-cyclotomic-rees-lift-physical-separator.md":
        "6e5f7b0daa37c19fbdba024f76cf5456e97931caa2c602211a5b02ac65b853e4",
}
EXPECTED_LEDGER_SHA256 = "9b768fe6858072b95a7710d8e8feeb82411500801cfeb7245ae92b570359d98e"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def file_sha256(relative):
    return sha256((ROOT / relative).read_bytes()).hexdigest()


def add(left, right):
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, QQ(0)) + QQ(value)
        if not out[key]:
            del out[key]
    return out


def scale(scalar, vector):
    scalar = QQ(scalar)
    return {key: scalar * QQ(value) for key, value in vector.items()
            if scalar * QQ(value)}


def boundary(chain):
    """Universal rank-one interface differential.

    Coefficients live in Q(h,kappa); h and kappa are symbolic basis tags in
    the ledger below.  For the exact arithmetic audit we normalize h=2 and
    kappa=3, a harmless localization test.
    """
    h = QQ(2)
    result = {}
    for name, coefficient in chain.items():
        if name == "b":
            image = {"k": QQ(1)}
        elif name == "n":
            image = {"hYw": h}
        else:
            raise RuntimeError(f"unknown generator {name}")
        result = add(result, scale(coefficient, image))
    return result


def audit():
    for relative, expected in PINS.items():
        require(file_sha256(relative) == expected,
                f"pinned dependency changed: {relative}")

    # The relative rootless correction is (b,-n): its two boundary
    # components are the chart syzygy k and the cancelling marked face -hYw.
    relative = {"b": QQ(1), "n": QQ(-1)}
    relative_boundary = boundary(relative)
    require(relative_boundary == {"k": QQ(1), "hYw": QQ(-2)},
            "rootless relative correction changed")

    # On h != 0, n/h is the invisible unit-cap lift.  Multiplication by
    # kappa gives precisely kappa Yw, with target and ores identically zero.
    h = QQ(2)
    kappa = QQ(3)
    inactive = {"n": kappa / h}
    require(boundary(inactive) == {"hYw": kappa},
            "localized inactive cap lift changed")

    # The physical relative module's primitive separator reads one on the
    # cap direction, so this direction cannot be manufactured by base change
    # among the old physical columns.  It must be supplied by the comparison.
    old_columns = {
        "old_1": (1, -1, 0, 0),
        "old_2": (0, 1, -1, 0),
        "old_3": (0, 0, 1, 1),
    }
    lam = (1, 1, 1, -1)
    require(all(sum(a * b for a, b in zip(lam, column)) == 0
                for column in old_columns.values()),
            "old physical columns left the primitive separator kernel")
    cap = (0, 1, 0, 0)
    require(sum(a * b for a, b in zip(lam, cap)) == 1,
            "physical cap direction lost primitive separator value one")

    ledger = {
        "derived_source_cell": "d b_v = k_v",
        "derived_target_filler": {
            "differential": "d n_v = h_v Yw",
            "target": 0,
            "ordinary_residue": 0,
            "chart_terminal_correction": -1,
        },
        "rootless_use": (
            "(b_v,-n_v) extends the marked chart map; it becomes the "
            "primitive rootless anchor correction only if the physical "
            "comparison identifies -S_v with pentagon anchor incidence"
        ),
        "inactive_face_open_use": (
            "on D(h_v), (kappa/h_v)n_v has derived boundary kappa Yw; "
            "it becomes the physical cap lift only if the comparison "
            "identifies this Yw with physical W"
        ),
        "physical_separator": {
            "lambda": "E+W+T-O",
            "old_columns_value": 0,
            "new_cap_value": 1,
        },
        "single_missing_datum": (
            "an augmented derived-to-physical comparison preserving source "
            "boundary, target, ordinary residue, chart grade, and terminal "
            "readout, and proving both -S_v -> primitive anchor incidence "
            "and derived Yw -> physical W; the underived diagonal projection "
            "is sufficient but not necessary"
        ),
        "remaining_separate_loci": (
            "the simultaneous face-zero locus V(h_1,...,h_5), and the later "
            "rootless/inactive horizontal identification beyond the first "
            "kappa Yw cap boundary"
        ),
        "scope": (
            "conditional interface theorem only: no physical comparison, "
            "chart cover by D(h_v), or full conjecture is claimed"
        ),
        "pins": PINS,
    }
    digest = sha256(json.dumps(
        ledger, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if EXPECTED_LEDGER_SHA256 != "TO_BE_PINNED":
        require(digest == EXPECTED_LEDGER_SHA256,
                f"shared interface ledger changed: {digest}")
    return ledger, digest


def main():
    _, digest = audit()
    print("h3 shared derived comparison interface: PASS")
    print("one filler is the candidate for both physical promotions")
    print(f"ledger_sha256={digest}")


if __name__ == "__main__":
    main()

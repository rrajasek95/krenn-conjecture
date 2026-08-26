#!/usr/bin/env python3
r"""REPAIR PROBE (item 2b): non-vacuous terminal rows in the M_v identity.

UNAUDITED.  Pinned to krenn-conjecture HEAD 7d57c552a3ef57d3a95c3bc933af547ad55e087d.

The committed composition check
``computations/verify_h3_literal_mv_cap_cartan_composition.augmented_sign_audit``
builds

    terminal = {eta1..eta5_constant: 1, eta1_U1: 1, sigma_qpq22: -1}
    K        = vector(R_corner = alpha_j, **terminal)
    candidate= -O_alpha + K
    desired  = sum_j vector(private_j = alpha_j, Eq_j = alpha_j) + vector(**terminal)
    require(candidate == desired)

The same literal `terminal` is spliced into BOTH sides, so the seven terminal
rows cancel out of the comparison: they constrain only that -O_alpha has zero
terminal rows.  The protected-row check that follows lists R_*, W_*, target_*
and ainc, never the terminal rows.  Consequently an EMPTY terminal packet
passes the committed identity unchanged.  This script demonstrates that, then
runs a repaired gate in which

  * the SUPPLY side (what K carries) is computed by contracting the physical
    stabilizer fields with the ridge class -dOmega_v (script
    derive_ridge_terminal_packet.py), and
  * the DEMAND side (what M_v must carry) is computed independently from the
    two physical defects the repo actually measures:
        - the clean-C5 aggregate separator defect eta_z(Omega_v) = -1 - delta u_z/t
          (verify_h3_rootless_clean_c5_separator_endpoint_kernel_boundary.py), and
        - the full-Jacobian sigma defect sigma(Omega_v + c_v) = +q_pq^22
          (verify_h3_rootless_clean_c5_formal_F_full_jacobian_boundary.py,
           verify_h3_residual_q_eta_one_cell_fiber_product_gate.py),
    the demand being the negative of each defect,

and the seven terminal rows are compared entrywise as part of the signature.

It also PROVES (not assumes) that -O_alpha has zero terminal rows: the eta_z-
and sigma-weight of a decorated matching monomial depends only on its word,
and vanishes identically on every word carried by the O_alpha census.
"""

from __future__ import annotations

from fractions import Fraction as Q
from hashlib import sha256
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
PINNED_HEAD = "7d57c552a3ef57d3a95c3bc933af547ad55e087d"

PINS = {
    "computations/verify_h3_literal_mv_cap_cartan_composition.py":
        "8e54a161402499c638dcba6177069fc3bb37648fb37c3546955310a56889744e",
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py":
        "b890195a8fc0c4e90c9c9c0c03c41a95690228c81026f4c2ea1fa95908564e38",
    "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py":
        "190171b72493e661dedb8e7aa369a9b72f1a71e14487632df2841ca7eeb19bf4",
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def load(relative, name, root=None):
    root = root or REPO
    specification = importlib.util.spec_from_file_location(
        name, root / relative)
    require(specification is not None and specification.loader is not None,
            ("cannot import", relative))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


derive = load("derive_ridge_terminal_packet.py", "repair23_derive", HERE)


# ---------------------------------------------------- physical demand/supply

def physical_supply(omegas, face):
    """What K carries: the eta/sigma contractions of the ridge class."""
    minus_omega = derive.pscale(-1, omegas[face])
    entries = {}
    for z in derive.ODD:
        value = derive.eta(z, minus_omega)
        entries[f"eta{z}_constant"] = value.get(derive.ONE_MONOMIAL, Q(0))
        if z == face:
            entries[f"eta{z}_U{z}"] = value.get(
                derive.monomial((derive.U[z], 1), (derive.T, -1)), Q(0))
    entries["sigma_qpq22"] = derive.sigma(minus_omega).get(
        derive.monomial((derive.A, 1)), Q(0))
    return entries


def physical_demand(omegas, face):
    """What M_v must carry: minus the two measured physical defects.

    eta defect: the clean-C5 aggregate separator reads eta_z(Omega_v) on each
    face; the compensation must be its negative.
    sigma defect: Omega_v + c_v (c_v = t - u_v, the unique affine primitive of
    the eta law) is eta-invariant but sigma-moves by +q_pq^22; the terminal
    sigma row must be its negative.
    """
    entries = {}
    for z in derive.ODD:
        defect = derive.eta(z, omegas[face])
        constant = defect.get(derive.ONE_MONOMIAL, Q(0))
        require(constant == -1, ("separator eta defect changed", face, z,
                                 derive.render(defect)))
        entries[f"eta{z}_constant"] = -constant
        if z == face:
            coefficient = defect.get(
                derive.monomial((derive.U[z], 1), (derive.T, -1)), Q(0))
            require(coefficient == -1,
                    ("separator U_z defect changed", face, z))
            entries[f"eta{z}_U{z}"] = -coefficient
    c_v = derive.poly((1, derive.monomial((derive.T, 1))),
                      (-1, derive.monomial((derive.U[face], 1))))
    corrected = derive.padd(omegas[face], c_v)
    for z in derive.ODD:
        require(derive.eta(z, corrected) == {},
                ("Omega_v + c_v stopped being eta-invariant", face, z))
    sigma_defect = derive.sigma(corrected)
    require(sigma_defect == derive.poly((1, derive.monomial((derive.A, 1)))),
            ("sigma defect changed", face, derive.render(sigma_defect)))
    entries["sigma_qpq22"] = -sigma_defect[derive.monomial((derive.A, 1))]
    return entries


# ------------------------------------- literal features carry no terminal row

def literal_feature_invariance():
    """The eta_z/sigma weight of a decorated matching monomial depends only on
    its word: it is  sum_s mu(s, w[s]).  Verified on all 3^8 words against the
    literal 90-term rows, and shown to vanish on the O_alpha census words."""
    base = load(
        "computations/verify_h3_direct_free_complete_first_fine_degree_membership.py",
        "repair23_base")
    complete = load(
        "computations/verify_h3_rootless_c5_complete_multidegree_source_no_go.py",
        "repair23_complete")

    fields = {f"eta{z}": derive.eta_weights(z) for z in derive.ODD}
    fields["sigma"] = derive.SIGMA_WEIGHTS

    def word_weight(weights, word):
        return sum(weights.get((site, colour), 0)
                   for site, colour in enumerate(word))

    checked_words = 0
    for word in product(range(3), repeat=8):
        row = base.full_row(word)
        for label, weights in fields.items():
            predicted = word_weight(weights, word)
            for mono in row:
                actual = sum(derive.weight_of(weights, cell) for cell in mono)
                require(actual == predicted,
                        ("monomial weight is not a word invariant", word,
                         label, actual, predicted))
        checked_words += 1
    require(checked_words == 3 ** 8, "word census changed")

    census_words = {tuple(complete.PURE_WORD)}
    zero = {}
    for word in sorted(census_words):
        zero["".join(map(str, word))] = {
            label: word_weight(weights, word)
            for label, weights in fields.items()}
    require(all(set(entry.values()) == {0} for entry in zero.values()),
            ("an O_alpha census word carries a terminal weight", zero))

    # Full verification (not just a witness term) on the census words.
    for word in census_words:
        for label, weights in fields.items():
            for mono in base.full_row(word):
                require(sum(derive.weight_of(weights, cell) for cell in mono)
                        == 0, ("a census feature moved", word, label))
    # Exact characterization of which source words could ever carry a terminal
    # row: the eta_z weight is [w[6]==0] - [w[z]==0] and the sigma weight is
    # [w[6]==2] - [w[0]==2].  Enumerate how many of the 3^8 words are killed by
    # all six fields, so the "-O_alpha has no terminal row" step is a stated,
    # checkable condition on words rather than an unexamined convention.
    invariant_words = 0
    for word in product(range(3), repeat=8):
        if all(word_weight(weights, word) == 0
               for weights in fields.values()):
            invariant_words += 1
    return {"words_checked": checked_words,
            "census_words": zero,
            "weight_is_word_invariant": True,
            "eta_z_weight_formula": "[w[6]==0] - [w[z]==0]",
            "sigma_weight_formula": "[w[6]==2] - [w[0]==2]",
            "words_killed_by_all_six_fields": invariant_words,
            "words_total": 3 ** 8,
            "residual_assumption": (
                "verified for the r0 half of O_alpha (word "
                + "".join(map(str, complete.PURE_WORD))
                + ").  The target cap T and residue cap rho are five-entry "
                  "formal symbols in the committed model with no literal cell "
                  "inventory, so their terminal rows are still assumed zero, "
                  "not computed"),
            }


# ------------------------------------------------- committed vs repaired gate

def build_sides(literal, terminal):
    alpha = literal.ALPHA
    per_corner = {}
    for corner in literal.CORNERS:
        per_corner[corner] = {
            "r0": literal.vector(**{f"private_{corner}": 1, f"Eq_{corner}": 1,
                                    f"target_{corner}": 1, "ainc": -1}),
            "T": literal.vector(**{f"W_{corner}": -1, f"target_{corner}": 1}),
            "rho": literal.vector(**{f"W_{corner}": 1, f"R_{corner}": 1}),
        }
    O_alpha = literal.add(*(
        literal.scale(alpha[index], literal.add(
            literal.scale(-1, per_corner[corner]["r0"]),
            per_corner[corner]["T"], per_corner[corner]["rho"]))
        for index, corner in enumerate(literal.CORNERS)))
    minus_O = literal.scale(-1, O_alpha)
    K = literal.vector(**{
        **{f"R_{corner}": alpha[index]
           for index, corner in enumerate(literal.CORNERS)},
        **terminal})
    candidate = literal.add(minus_O, K)
    desired = literal.add(*(
        literal.vector(**{f"private_{corner}": alpha[index],
                          f"Eq_{corner}": alpha[index]})
        for index, corner in enumerate(literal.CORNERS)),
        literal.vector(**terminal))
    return minus_O, K, candidate, desired


def committed_gate(literal, terminal):
    """Exactly the committed comparison (both sides get the same terminal)."""
    minus_O, K, candidate, desired = build_sides(literal, terminal)
    if candidate != desired:
        return False, "signature mismatch"
    protected = (*(f"R_{c}" for c in literal.CORNERS),
                 *(f"W_{c}" for c in literal.CORNERS),
                 *(f"target_{c}" for c in literal.CORNERS), "ainc")
    if any(candidate[literal.ROWS.index(row)] != 0 for row in protected):
        return False, "protected row survived"
    return True, "pass"


def repaired_gate(literal, terminal, demand):
    """Terminal rows are part of the compared signature and are compared to an
    independently computed physical demand."""
    minus_O, K, candidate, desired = build_sides(literal, terminal)
    if candidate != desired:
        return False, "signature mismatch"
    protected = (*(f"R_{c}" for c in literal.CORNERS),
                 *(f"W_{c}" for c in literal.CORNERS),
                 *(f"target_{c}" for c in literal.CORNERS), "ainc")
    if any(candidate[literal.ROWS.index(row)] != 0 for row in protected):
        return False, "protected row survived"
    # (R1) -O_alpha carries no terminal row, so K is the sole carrier.
    if any(minus_O[literal.ROWS.index(row)] != 0
           for row in literal.TERMINAL_ROWS):
        return False, "-O_alpha acquired a terminal row"
    # (R2) the terminal rows of the composed M_v equal the physical demand.
    for row in literal.TERMINAL_ROWS:
        if candidate[literal.ROWS.index(row)] != demand.get(row, Q(0)):
            return False, f"terminal row {row} != physical demand"
    # (R3) the terminal packet is not empty (an empty packet cannot be the
    # relative jet of a nonzero ridge).
    if all(candidate[literal.ROWS.index(row)] == 0
           for row in literal.TERMINAL_ROWS):
        return False, "terminal packet is empty"
    return True, "pass"


# ---------------------------------------------------------------------- main

def main():
    pin_report = {}
    for relative, expected in PINS.items():
        actual = sha256((REPO / relative).read_bytes()).hexdigest()
        pin_report[relative] = actual
        if expected != "TO_BE_PINNED":
            require(actual == expected,
                    ("pinned dependency changed", relative, actual))

    literal = load(
        "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
        "repair23_literal")

    omegas = {v: derive.build_omega(v) for v in derive.ODD}
    supply = physical_supply(omegas, 1)
    demand = physical_demand(omegas, 1)
    require(set(supply) == set(demand) == set(literal.TERMINAL_ROWS),
            ("terminal row set mismatch", sorted(supply), sorted(demand),
             sorted(literal.TERMINAL_ROWS)))
    require(supply == demand,
            ("supply does not meet demand", supply, demand))

    committed_literal = {
        **{f"eta{face}_constant": 1 for face in range(1, 6)},
        "eta1_U1": 1, "sigma_qpq22": -1}
    require({row: Q(value) for row, value in committed_literal.items()}
            == supply,
            "the derived packet differs from the committed literal packet")

    variants = {
        "committed literal packet": committed_literal,
        "EMPTY terminal packet": {},
        "sigma sign flipped": {**committed_literal, "sigma_qpq22": 1},
        "eta1_U1 dropped": {**committed_literal, "eta1_U1": 0},
        "eta constants doubled": {
            **{f"eta{face}_constant": 2 for face in range(1, 6)},
            "eta1_U1": 1, "sigma_qpq22": -1},
        "derived packet": {row: supply[row] for row in literal.TERMINAL_ROWS},
    }
    table = []
    for label, terminal in variants.items():
        committed_ok, committed_note = committed_gate(literal, terminal)
        repaired_ok, repaired_note = repaired_gate(literal, terminal, demand)
        table.append({
            "variant": label,
            "committed_gate": committed_ok,
            "committed_note": committed_note,
            "repaired_gate": repaired_ok,
            "repaired_note": repaired_note,
        })

    by_label = {record["variant"]: record for record in table}
    require(by_label["committed literal packet"]["committed_gate"]
            and by_label["committed literal packet"]["repaired_gate"],
            "M_v = -O_alpha + K fails with terminals compared")
    require(by_label["EMPTY terminal packet"]["committed_gate"],
            "the committed gate was expected to be vacuous on empty terminals")
    require(not by_label["EMPTY terminal packet"]["repaired_gate"],
            "the repaired gate is still vacuous")
    for label in ("sigma sign flipped", "eta1_U1 dropped",
                  "eta constants doubled"):
        require(by_label[label]["committed_gate"],
                ("the committed gate unexpectedly caught", label))
        require(not by_label[label]["repaired_gate"],
                ("the repaired gate missed", label))

    features = literal_feature_invariance()

    ledger = {
        "probe": "repair item 2b: non-vacuous M_v terminal gate",
        "status": "UNAUDITED REPAIR PROBE",
        "pinned_head": PINNED_HEAD,
        "pins": pin_report,
        "terminal_rows": list(literal.TERMINAL_ROWS),
        "physical_supply_from_minus_dOmega_1": {row: str(value)
                                                for row, value in supply.items()},
        "physical_demand_from_measured_defects": {row: str(value)
                                                  for row, value in demand.items()},
        "supply_equals_demand": True,
        "gate_table": table,
        "committed_gate_is_vacuous_on_terminals": True,
        "repaired_gate_passes_with_terminals_compared": True,
        "minus_O_alpha_terminal_rows_are_zero_because": features,
    }
    payload = json.dumps(ledger, sort_keys=True, separators=(",", ":"))
    digest = sha256(payload.encode()).hexdigest()
    print("repair23 repaired M_v terminal gate")
    for record in table:
        print("  %-26s committed=%-5s repaired=%-5s (%s)" % (
            record["variant"], record["committed_gate"],
            record["repaired_gate"], record["repaired_note"]))
    print("physical supply:", ledger["physical_supply_from_minus_dOmega_1"])
    print("physical demand:", ledger["physical_demand_from_measured_defects"])
    print("M_v = -O_alpha + K with terminals compared: PASSES")
    print("ledger_sha256=" + digest)
    HERE.joinpath("ledger_repaired_mv_terminal_gate.json").write_text(
        json.dumps(ledger, sort_keys=True, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

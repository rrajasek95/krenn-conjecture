#!/usr/bin/env python3
"""RISK PROBE C/D: M_v target-zero, and the beta=0 trace collision.

D: "the two diagonal jet targets have rank two while M_v is target-zero".
   Rank two is checked in probe_a_jstar.py from the real matrix constructor.
   Here we check the M_v half INSIDE the module that actually builds M_v:
   computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py
   (function augmented_private_pivot_no_go; `mapping_cone` is M_v).

C: the beta=0 trace collision.  We run the smallest exact instance that the
   committed constructors permit.
"""

from __future__ import annotations

import importlib.util
import sys
from fractions import Fraction as Q
from pathlib import Path

SNAP = Path(__file__).resolve().parent / "snapshot"


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, SNAP / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CONE = load(
    "computations/verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py",
    "probe_cone",
)
DIAG = load(
    "computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py",
    "probe_diag3",
)

FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("  FAIL:", msg)


print("=" * 74)
print("D2. IS M_v LITERALLY TARGET-ZERO IN ITS OWN COMMITTED MODULE?")
print("=" * 74)

# Rebuild the mapping cone exactly as the committed checker does.
CORNERS = CONE.CORNERS
ALPHA = CONE.ALPHA
ROWS = CONE.ROWS
print("  corners:", CORNERS)
print("  ALPHA  :", ALPHA)

literal_c = {
    corner: CONE.vector(**{f"private_{corner}": -1, f"Eq_{corner}": -1})
    for corner in CORNERS
}
terminal_packet = {
    **{f"eta{face}_constant": 1 for face in range(1, 6)},
    "eta1_U1": 1,
    "sigma_qpq22": -1,
}
mapping_cone = CONE.add(
    *(CONE.scale(-ALPHA[i], literal_c[c]) for i, c in enumerate(CORNERS)),
    CONE.vector(**terminal_packet),
)
target_rows = [f"target_{c}" for c in CORNERS]
target_values = tuple(mapping_cone[ROWS.index(r)] for r in target_rows)
print("  M_v (=mapping_cone) target coordinates:",
      tuple(str(v) for v in target_values))
check(all(v == 0 for v in target_values), "M_v is NOT target-zero")
print("  M_v target-zero:", all(v == 0 for v in target_values))

# mutation control: inject a target and confirm the readout notices
mutated = CONE.add(mapping_cone,
                   CONE.vector(**{f"target_{CORNERS[0]}": 1}))
mut_vals = tuple(mutated[ROWS.index(r)] for r in target_rows)
print("  mutation control (M_v + target_%s): %s"
      % (CORNERS[0], tuple(str(v) for v in mut_vals)))
check(any(v != 0 for v in mut_vals), "target readout is blind (mutation)")

print()
print("  TYPING CAVEAT: this module's `target_<corner>` coordinates are a")
print("  DIFFERENT grade from (i) the three monochromatic GHZ coordinates")
print("  carrying T(J1),T(J2), and (ii) the five-coordinate root-decorated")
print("  word space carrying (w-1)Delta.  No committed map relates them;")
print("  the sentence 'jet targets have rank two while M_v is target-zero'")
print("  therefore compares readouts in three unidentified modules.")

print()
print("=" * 74)
print("C. THE beta=0 TRACE COLLISION: SMALLEST EXACT INSTANCE")
print("=" * 74)


def mat_add(*terms):
    return [[sum(s * m[i][j] for s, m in terms) for j in range(3)]
            for i in range(3)]


# The committed beta=0 sample block from check_cap_jet_representatives.
block = [[Q(4), Q(2), Q(5)], [Q(7), Q(9), Q(-6)], [Q(13), Q(17), Q(-9)]]
a, h = 0, 3
alpha, tau, beta, k0, k1, k2 = DIAG.diagonal_data(block, a)
print(f"  committed beta=0 block, a={a}: alpha={alpha}, tau={tau}, "
      f"beta={beta}")
check(beta == 0, "the committed collision sample stopped having beta=0")
j1 = k1
j2 = mat_add((-beta, k0), (h - 1, k2))
print("  T(J1) =", tuple(str(v) for v in DIAG.diag(j1)))
print("  T(J2) =", tuple(str(v) for v in DIAG.diag(j2)))
check(j2 == mat_add((h - 1, j1)), "collision rows failed to collapse")
print("  J2 == (h-1)*J1 :", j2 == mat_add((h - 1, j1)))
print("  selected-colour coordinate a is BLIND: T(J1)[a] =",
      DIAG.diag(j1)[a], ", T(J2)[a] =", DIAG.diag(j2)[a])
check(DIAG.diag(j1)[a] == DIAG.diag(j2)[a] == 0,
      "collision rows stopped being blind at the selected colour")

print()
print("  J_* at beta=0:")
jstar = mat_add((beta - 2 * alpha, j1), (beta + alpha, j2))
print("    T(J_*) =", tuple(str(v) for v in DIAG.diag(jstar)),
      " = -3*alpha*beta*Delta =", -3 * alpha * beta)
check(DIAG.diag(jstar) == (Q(0),) * 3, "J_* target nonzero at beta=0")
print("    => J_* DEGENERATES TO TARGET ZERO at beta=0.  The b63c76c")
print("       construction supplies NOTHING on the collision stratum, and")
print("       its 'localization at alpha*beta' is exactly the step that")
print("       excises this stratum.  Consistent with the note's own caveat.")

print()
print("  Committed principal-part orders at beta=0 (polynomial_v_coefficients):")
for hh in (3, 4, 5):
    sel = DIAG.polynomial_v_coefficients(hh, Q(2), Q(0), True)
    com = DIAG.polynomial_v_coefficients(hh, Q(2), Q(0), False)
    vs, vc = DIAG.valuation(sel), DIAG.valuation(com)
    print(f"    h={hh}: selected target first order = {vs} (want {hh}), "
          f"complementary = {vc} (want {hh-1})")
    check(vs == hh and vc == hh - 1, f"collision orders changed at h={hh}")

print()
print("  What the order-h unary target jet must be (committed data):")
print("    verify_h3_phi_diagonal_rees_extension_gate.audit_diagonal_target_gate")
print("    encodes it as the HARDCODED vector unary_target = (h,0,0) and")
print("    checks only rank((collision_J1, unary_target)) == 2.")
h = 3
alpha = Q(2)
collision_j1 = (h * Q(0), -h * alpha, -h * alpha)
collision_j2 = (-h * Q(0), -h * (h - 1) * alpha, -h * (h - 1) * alpha)
unary_target = (Q(h), Q(0), Q(0))


def rank(rows):
    work = [list(map(Q, r)) for r in rows]
    pr = 0
    for col in range(len(work[0])):
        piv = next((r for r in range(pr, len(work)) if work[r][col]), None)
        if piv is None:
            continue
        work[pr], work[piv] = work[piv], work[pr]
        v = work[pr][col]
        work[pr] = [e / v for e in work[pr]]
        for r in range(len(work)):
            if r != pr and work[r][col]:
                v = work[r][col]
                work[r] = [x - v * y for x, y in zip(work[r], work[pr])]
        pr += 1
    return pr


print("    rank(collision_J1, collision_J2) =",
      rank((collision_j1, collision_j2)), "(want 1)")
print("    rank(collision_J1, unary_target) =",
      rank((collision_j1, unary_target)), "(want 2)")
check(rank((collision_j1, collision_j2)) == 1
      and rank((collision_j1, unary_target)) == 2,
      "the committed collision rank split changed")
print("    ANY vector with a nonzero selected-colour coordinate would pass")
print("    this test.  Mutation control:")
for cand, label in (((Q(1), Q(0), Q(0)), "(1,0,0)"),
                    ((Q(-7), Q(3), Q(3)), "(-7,3,3)"),
                    ((Q(0), Q(1), Q(0)), "(0,1,0) -- no selected colour")):
    r = rank((collision_j1, cand))
    print(f"      candidate {label:24s} -> rank {r}")
print("    FINDING: the guard is rank((collision_J1, X)) == 2, i.e. mere")
print("    NON-PROPORTIONALITY to collision_J1.  The colour-blind vector")
print("    (0,1,0) -- which carries NO selected-colour coordinate -- passes")
print("    it.  So the committed test does not actually certify 'carrying")
print("    the selected colour'; it certifies only independence.")
check(rank((collision_j1, (Q(0), Q(1), Q(0)))) == 2,
      "the non-proportionality reading of the guard changed")
print("    => the committed artifact is an EXISTENCE REQUIREMENT stated as a")
print("       rank condition, not a construction: no checker builds an")
print("       order-h unary target/anchor cell from source data.")

print()
print("=" * 74)
print("FAILURES:", len(FAIL))
for f in FAIL:
    print("  -", f)
print("=" * 74)
sys.exit(1 if FAIL else 0)

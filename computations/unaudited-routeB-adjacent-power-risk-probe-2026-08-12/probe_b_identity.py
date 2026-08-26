#!/usr/bin/env python3
"""RISK PROBE B: the live generic obstruction, tested under BOTH readings.

b63c76c asserts:
  "hT(J_*) = -9 alpha beta Delta.  After the physical two-root orbit and
   localization at alpha beta, this gives exactly the required rho-even
   upper target -2(w-1)Delta.  The remaining generic obstruction is only
   the lower face: the explicit even Cartan remainder (1+rho)H_w d(P(J_*))
   must equal the desired adjacent response face modulo the literal Rees
   boundary module."

READING 1 (naive):  lambda * hT(J_*)  ==  -2(w-1)Delta  as vectors.
READING 2 (charitable, and evidently the intended one):
   the "two-root orbit" is application of the Cartan operator, so via
   dH_w + H_w d = w-1 one gets, modulo im(d),
        (1+rho) H_w d(X)  ==  (1+rho)(w-1) X  ==  2(w-1) X
   for rho-even X, and X = normalized class of P(J_*) = -Delta after
   localizing at alpha*beta.  Then the answer is -2(w-1)Delta.

This probe evaluates both exactly, and isolates precisely which
identifications carry the weight.  Exact Fractions.  No repo writes.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

SNAP = Path(__file__).resolve().parent / "snapshot"


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, SNAP / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


SIG = load(
    "computations/verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py",
    "probe_sig",
)
DIAG = load(
    "computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py",
    "probe_diag2",
)
PRISM = load("computations/verify_h3_sl2_weyl_cartan_prism.py", "probe_prism")

FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("  FAIL:", msg)


N = SIG.N
COLOURS = SIG.COLOURS
MONO = tuple((c,) * N for c in COLOURS)

delta = Counter({word: Q(1) for word in MONO})
w_delta = SIG.transform(delta, SIG.weyl_word)
defect = SIG.add_counters((1, w_delta), (-1, delta))          # (w-1)Delta
rho_defect = SIG.transform(defect, SIG.rho_word)
mixed = tuple(sorted(word for word in defect if len(set(word)) > 1))
COORDS = MONO + mixed


def vec(counter):
    return tuple(Q(counter.get(word, 0)) for word in COORDS)


def show(v):
    return "(" + ", ".join(str(x) for x in v) + ")"


print("=" * 74)
print("B0. THE COMMON WORD-TARGET MODULE (committed signless checker)")
print("=" * 74)
print("  coordinates :", ["".join(map(str, w)) for w in COORDS])
print("  Delta       :", show(vec(delta)), " (= 000000+111111+222222)")
print("  w*Delta     :", show(vec(w_delta)))
print("  (w-1)Delta  :", show(vec(defect)))
check(rho_defect == defect, "(w-1)Delta is not rho-even")
required = tuple(-2 * x for x in vec(defect))
print("  REQUIRED upper target of C_plus: -2(w-1)Delta =", show(required))
print("  (notes/h3-signless-cartan-adjacent-power-shared-cell-gate.md L152)")

# ------------------------------------------------------------------ J_* side
def mat_add(*terms):
    return [[sum(s * m[i][j] for s, m in terms) for j in range(3)]
            for i in range(3)]


block = [[Q(2), Q(3), Q(-1)], [Q(5), Q(7), Q(11)], [Q(13), Q(17), Q(19)]]
a, h = 0, 3
alpha, tau, beta, k0, k1, k2 = DIAG.diagonal_data(block, a)
j1, j2 = k1, mat_add((-beta, k0), (h - 1, k2))
jstar = mat_add((beta - 2 * alpha, j1), (beta + alpha, j2))
t = DIAG.diag(jstar)
ht = tuple(h * x for x in t)
print()
print(f"  committed sample block, a=0, h=3: alpha={alpha}, beta={beta}")
print("  hT(J_*) =", tuple(str(x) for x in ht), "= -9*alpha*beta*Delta,",
      f"-9ab = {-9*alpha*beta}")
check(ht == tuple(-9 * alpha * beta for _ in range(3)),
      "hT(J_*) is not -9ab*Delta")

print()
print("=" * 74)
print("B1. READING 1 (naive vector equality) -- FAILS")
print("=" * 74)
ht_word = tuple(list(ht) + [Q(0), Q(0)])
print("  hT(J_*) embedded in the word module:", show(ht_word))
lams = {Q(required[i], x) for i, x in enumerate(ht_word) if x}
solvable = any(tuple(l * x for x in ht_word) == required for l in lams)
print("  scalars forced coordinate-by-coordinate:",
      sorted(str(l) for l in lams))
print("  exists lambda with lambda*hT(J_*) == -2(w-1)Delta ?", solvable)
check(not solvable, "unexpected: naive reading succeeds")
best = tuple(Q(2) * x for x in vec(delta))
resid = tuple(x - y for x, y in zip(best, required))
print("  best-case defect (normalize to 2*Delta):", show(resid),
      "= 2*w*Delta:", resid == tuple(2 * x for x in vec(w_delta)))
print("  -> under Reading 1 the mixed words 020020, 202202 are never")
print("     reached by ANY c1*J1+c2*J2, for any alpha,beta,h,a.")

print()
print("=" * 74)
print("B2. READING 2 (Cartan reduction) -- ARITHMETICALLY CONSISTENT")
print("=" * 74)
print("  Step 1: verify the Cartan homotopy identity where H_w is an ACTUAL")
print("          operator -- the sl2 Weyl prism toy (the only such model).")
# The prism checker itself verifies dH_w + H_w d = w-1; rerun its audit.
try:
    PRISM.audit()
    prism_ok = True
except Exception as exc:                                  # pragma: no cover
    prism_ok = False
    print("   prism checker raised:", exc)
check(prism_ok, "the sl2 Weyl Cartan prism checker failed")
print("          => dH_w + H_w*d = w-1 holds (2-variable de Rham forms).")

print()
print("  Step 2: formal consequence, assuming rho is a chain automorphism")
print("          commuting with w (committed: 'the two operations commute'):")
print("            (1+rho)H_w d(X) = (1+rho)(w-1)X - d((1+rho)H_w X)")
print("          so MODULO im(d), and for rho-even X:")
print("            (1+rho)H_w d(X) == 2(w-1)X")
print()
print("  Step 3: normalize the J_* class.  Localizing at alpha*beta makes")
print("          1/(9*alpha*beta) a unit, and")
lam = Q(1, 9 * alpha * beta)
normalized = tuple(lam * x for x in ht)
print(f"            ({lam}) * hT(J_*) =", show(normalized), "= -Delta")
check(normalized == tuple(Q(-1) for _ in range(3)),
      "the localization does not normalize hT(J_*) to -Delta")
print("  Step 4: therefore 2(w-1)*(-Delta) =", end=" ")
step4 = tuple(-2 * x for x in vec(defect))
print(show(step4))
check(step4 == required, "the Cartan reduction does not land on -2(w-1)Delta")
print("          == the required upper target -2(w-1)Delta :",
      step4 == required)
print()
print("  VERDICT B2: under Reading 2 the ARITHMETIC IS EXACT AND CORRECT.")

print()
print("=" * 74)
print("B3. WHAT READING 2 SILENTLY ASSUMES  (this is the real risk)")
print("=" * 74)
print("  (i) An identification iota carrying the normalized P(J_*) class")
print("      into the module on which w and rho act, with T(J_*) going to")
print("      a MULTIPLE OF Delta as an element (not merely as a readout).")
print()
print("      This is NOT the tautological embedding.  Committed theorem")
print("      (verify_h3_signless_cartan_adjacent_power_shared_cell_gate.py")
print("      L227-232):")
print("         rank(pure_rows + (J1,J2))        == 3")
print("         rank(pure_rows + (w-1)Delta)     == 4")
r_pure_j = 3
pure_rows = tuple(tuple(Q(int(c == r)) for c in range(5)) for r in range(3))


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


j1v = tuple(list(DIAG.diag(j1)) + [Q(0), Q(0)])
j2v = tuple(list(DIAG.diag(j2)) + [Q(0), Q(0)])
print("      recomputed here:  rank(pure + J1,J2) =",
      rank(pure_rows + (j1v, j2v)),
      "  rank(pure + (w-1)Delta) =", rank(pure_rows + (vec(defect),)))
check(rank(pure_rows + (j1v, j2v)) == 3
      and rank(pure_rows + (vec(defect),)) == 4,
      "the committed rank 3 / rank 4 split changed")
print("      i.e. the diagonal side is confined to the monochromatic span,")
print("      while (w-1)Delta is not.  So iota must be a genuinely NEW")
print("      root-decorated source-labelled map.  The same committed note")
print("      states this exact map is the missing datum:")
print('        "There is a source-labelled, Hasse/Rees-linear two-root')
print('         comparison which identifies the chosen diagonal upper face')
print('         hT(J) with the root-decorated face 2(w-1)Delta" -- and')
print('        "it is not a consequence of the committed inventories."')
print()
print("  (ii) 'modulo the literal Rees boundary module' must be at least as")
print("       coarse as im(d): the discrepancy term d((1+rho)H_w P(J_*))")
print("       has to lie in it.  N_lit is PROSE-ONLY (no span constructor);")
print("       the only committed model is the 3-basis COUNTERGUARD")
print("       M=<b,z,r>, N_lit=<b>, which exists to show Phi+anchor does")
print("       NOT imply Rees membership.  So this quotient is unverified.")
print()
print("  (iii) rho-evenness of the normalized class.  On the monochromatic")
print("        span rho=(1 4) acts trivially (it permutes sites, and every")
print("        monochromatic word is site-symmetric), so 'rho-even' is")
print("        VACUOUS on the diagonal side and carries no information:")
for wd in MONO:
    check(SIG.rho_word(wd) == wd, f"rho moved the monochromatic word {wd}")
print("        rho fixes each of 000000, 111111, 222222 :",
      all(SIG.rho_word(wd) == wd for wd in MONO))
print("        The (1+rho) factor of 2 therefore comes from the WORD side,")
print("        not from anything J_* supplies.")

print()
print("=" * 74)
print("B4. THE LOWER FACE IS NOT COMPUTABLE FROM COMMITTED CONSTRUCTORS")
print("=" * 74)
print("  Constituents of  (1+rho)H_w d(P(J_*)) == adjacent response face")
print("                   mod literal Rees boundary:")
print("   H_w        EXECUTABLE only on 2-variable de Rham forms")
print("              (verify_h3_sl2_weyl_cartan_prism.py:109,162).  Never")
print("              applied to a six-site word, a collision label, or J_*.")
print("   (1+rho)H_w NOT CONSTRUCTED.  Only occurrence in code is the")
print("              integer pair (1,1) in a formal 2-dim span")
print("              (signless gate audit_parity_gate, L186-201).")
print("   rho,w,u    EXECUTABLE on the 15-label x word basis")
print("              (verify_h3_cut_swap_odd_prism_kdu_typing_gate.py).")
print("   P(-)       PROSE.  Only its 3-vector shadow P(J)q^[h-1]=h*T(J)")
print("              is computed; no function maps a source row into a")
print("              module carrying a boundary.")
print("   d          EXECUTABLE only in the 8-site two-row Eq model")
print("              (verify_h3_full_hasse_koszul_cap_totalization.py:296).")
print("   N_lit      NO span constructor anywhere.")
print("   response   'the chosen p*t_c*B face' is a ledger type string.")
print("              face")
print()
print("  These are FOUR mutually unidentified bases (2-var de Rham forms;")
print("  6-site words x 15 collision labels; 3x3 cap matrices; 8-site")
print("  90-monomial Eq module).  The composite is not evaluable.")
print("  The repo's own checkers already certify the needed identification")
print("  as absent:  'equality_Kd_u012_equals_M_v_well_typed': False.")

print()
print("=" * 74)
print("B5. DOES THE (H_0-u)e_Eq CONORMAL DEFECT ABSORB ANYTHING HERE?")
print("=" * 74)
print("  (H_0-u)e_Eq IS fully executable")
print("  (verify_h3_full_hasse_koszul_cap_totalization.py:475-482: the")
print("   diagonal projection of the fourth-Hasse chain is {'eq': H_0-u,")
print("   'w': CAP_Y}, i.e. the wanted Yw PLUS the defect (H_0-u)*eq).")
print("  But it lives in the 8-site Eq module, on the e_Eq coordinate.")
print("  The Reading-1 defect 2*w*Delta lives on the mixed WORD coordinates")
print("  020020, 202202.  No committed map relates the two, so the")
print("  absorption question is NOT COMPUTABLE, not merely unproved.")
print()
print("  One committed fact IS relevant and is mildly favourable:")
print("  notes/h3-descent-defect-row-space-invisibility.md proves no chain")
print("  of TARGET-ZERO rows has e_0-boundary (H_0-u)e_0, and states")
print("  explicitly: 'Without target-zero on the rho_i, a row with target")
print("  t != 0 admits a = -b*t != 0 and the argument fails.'  A")
print("  TARGET-BEARING adjacent-power cell therefore escapes that no-go.")
print("  It is not excluded -- but nothing constructs it, and J_* is not")
print("  it (J_* is a diagonal cap combination, not a source cell).")

print()
print("=" * 74)
print("FAILURES:", len(FAIL))
for f in FAIL:
    print("  -", f)
print("=" * 74)
sys.exit(1 if FAIL else 0)

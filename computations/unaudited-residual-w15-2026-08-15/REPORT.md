# W15 — residual family (R) at N=8 — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 9b9bcf5. All verdicts exact (Fraction / exact sparse
polynomials / Singular over Q); NO floats in this directory. Agent's
write was policy-blocked; this transcribes its delivered report.

## HEADLINE: THE m=24 INSTANCE OF (R) IS DEAD [PROVED-HERE]
Seven-word hand certificate (6 mixed + 1 constant), verified twice
independently: hand-derived polynomial cofactor identities expanded
exactly over Z, and Singular Groebner reduction over Q with
leave-one-out minimality (6/6: dropping any word destroys it).
Mechanism = W10's prediction: THE MIXED SYSTEM FORCES A PURE
COEFFICIENT TO VANISH.

## Mechanism W15-A (Phi-forcing; uniform in N; needs NO cut)
Matchings of full blocks are supported on EVERY word, so
H_w = Phi(x,y) + extras with Phi = the Gamma-matching sum. A word is
EFFECTIVELY CLEAN when its fibre lies entirely in F(Gamma). Kill
routes: k=0 (a CONSTANT word effectively clean => H = Phi = 0 forced
by clean mixed equations, contradiction); k=1 (mixed word with ONE
extra => an occupied-cell monomial = 0); k=2 (two extras => a
binomial relation — thickness immunity destroyed, lattice re-enters).
This is the first tool that ignores Gamma's 2-connectivity entirely.

## The m=24 kill
Gamma = K4{0,1,2,3} u C4{4,5,6,7} u {07,14}; Sigma = 120. All 2,152
clean words verified to have the binomial shape; 0^8 IS effectively
clean (its lone extra single cell lies in no supported matching by
crossing parity). Certificate words w1..w6 = 10000200, 10001200,
12000200, 12001200, 00001200, 12000000; multiplier
A07[1][0]^4 A23[0][0]^3 A56[2][0]^3 A14[2][1]^2 (all occupied cells)
times H_{0^8} lies in ideal(H_w1..H_w6) over Z. Readable chain:
w1 w4 = w2 w3 forces a 2x2 minor of A14 to vanish; w4+w5 then w6
assemble A14[2][1] H_{0^8} = (cells)(minor) = 0.
Structure derived en route (independently reproving W12 §3.3 and
more): rank A45 = A56 = A67 = A07 = A14 = 1; P_L, P_R nowhere zero;
Phi = 0 IDENTICALLY on the clean stratum — W12's honest blocker is
BYPASSED (its residual identity constrains only the L-side; the
contradiction lives at the constant word).

## Controls
Independent engine (no W8/W12 code) reproduces W8's audits exactly on
all nine instances (full 6,558-word histograms) + W12-C's predicate;
252/252 template mutations detected; certificate minimality 6/6;
NON-VACUITY (decisive): an exact-rational point with all 108
full-block cells nonzero satisfies all 2,152 clean mixed equations —
the kill is not vacuous; 99/108 witness perturbations break a clean
equation, the 9 exceptions exactly A23's cells (predicted degeneracy);
positive calibration reproduces W12's m=20/21 kills by a different
route. TOOLING: Singular 4.4 reserves e1/mult/I; leading unary + is a
parse error.

## m = 25..28 — UNDECIDED, blocker sharp
At m >= 25 the added cross blocks give 0^8 a supported completion, so
NO constant is effectively clean (k=0 closed). k=1 words available:
1406/1438/719 at m=25/26/27; m=28 has extras always EVEN (k=2 = the
binomial route is designated there). At m=25 the clean layer yields
only a dichotomy (rank A56 = A67 = 1) OR (Psi = Omega = 0 => rank
A45 = A47 = 1), not a collapse; Rabinowitsch on the targets did not
terminate in budget. ODD TIGHT CUTS: m=24 finding reproduced verbatim
({0,2,3},{1,2,3},{4,5,6},{5,6,7}); m=25 only {0,2,3},{5,6,7};
m=26,27,28: NONE — route three lives at m <= 25 only.
DEFINITIONAL HANDOFF: W15's slice-cleanliness support proxy is NOT
S1's invariant; the rank-one witness search must use W5's slice_core
predicate/closed form.

## Not done / soft spots
(R) NOT ENUMERATED (largest open item: SAT for admissible thick
templates with Gamma spanning 2-connected; the |Gamma|=8 => C_8
case); the kill is instance-specific (sub-templates unchecked);
hypotheses minimal (only cells-nonzero + mixed-vanish + one constant
nonzero — inherits W8's template recording, mitigated by the exact
audit match); decide_pow/decide_sat are sufficient-only (negatives
inconclusive); the compressed model is lossy at m <= 23. No
escalation anywhere.

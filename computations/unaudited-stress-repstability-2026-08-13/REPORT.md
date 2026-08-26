# UNAUDITED STRESS TEST — representation stability for uniformity-in-h (2026-08-13)

Pinned HEAD 6426204 (HEAD moved to 6fa8d05 mid-run; diff empty on all
files under test). Fully independent rebuild (no repo imports); exact
arithmetic; floats only propose eigenvalues, each verified over Q.
Scripts + JSON in this directory. UNAUDITED.

## Verdict: SUPPORTED at the coefficient layer — with three sharp limits

T1 REPRODUCED (and extended): A_h eigenvalue h^2-3h+1 on [2h-2,2] by
three independent methods, h=3..7 (note: A_h alone stops separating
eigenspaces at h=6; the (3,1^{h-3}) relation is the needed second
separator). B_h five-sector spectrum verified h=2..5 (committed checkers
stop at 4); pointed cyclic module rank 5; P_h(4h)=8h(h+1)(2h+1).

T2 STABILITY-CONFIRMED: transfer residuals land in FIXED padded shape
lists ([2h]+[2h-2,2] one-step; +[2h-4,4],[2h-4,2,2] two-step), all
multiplicity one, at every computed h; ALL structural constants exactly
polynomial in h, fitted on 3 orders and verified OUT OF SAMPLE to h=12
(composite = 56h^3(2h-1), verified h=3..12; full fibre-constant table in
agent transcript). Caveat: the shape list is fixed PER COMPOSED STEP —
each transfer composition adds exactly one level.

T3 functoriality: pi A_{h+1} iota = A_h EXACTLY (correction lands outside
im iota); eigenvalue shift polynomial (2h-2); BUT iota does NOT preserve
level (iota(E1) leaks into level 2 — the finite shadow of the repo's own
spectator-uniformization no-go), and the intertwining test is generic
(holds for a deliberately broken operator too) — weak evidence by itself.

T4: all substantive mutations fire; two honest non-fires documented.

## Three limits (the accurate statement of what stability buys)

1. Uniform in h, NOT in iteration count: k-fold composites need k
   projector factors; arguments composing ~h transfers get no free ride.
2. Spectator suspension raises the residual level by one — functoriality
   along it does NOT transport the [2h-2,2] statement. Uniformity must be
   proved per-step-count, not induced.
3. Everything verified is coefficient-level graph commutation; the
   physical Cartan/Hasse lift (nonzero Leibniz cross terms at chain
   level, per the pinned Reynolds audit) is untouched — the open work is
   the physical lift, same as every other lane.

## Net for the uniformity clause

The one-step transfer's uniformity in h is well-supported and looks
provable (closed-form quadratic eigenvalues on every padded family).
"Rep stability, so one h suffices" would overclaim. Accurate: coefficient
data is polynomial and shape-stable in h; the open work is the physical
lift; spectator suspension leaks one level per application.

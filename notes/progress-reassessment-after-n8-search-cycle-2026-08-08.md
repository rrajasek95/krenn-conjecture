# Progress reassessment after the N=8 parallel search cycle

Date: 2026-08-08.

This note updates `progress-reassessment-2026-08-08.md` and
`n8-parallel-attack-cycle-2026-08-08.md`.  It is a research-allocation
assessment, not a proof of the conjecture.  No exact counterexample and no
complete N=8 impossibility theorem is known.

## Executive verdict

The useful part of the terminal-Bianchi branch was the N=8 saturation
localization, not the terminal-Bianchi comparison mechanism itself.  The D2
orientation/equivariance qualifications have now been audited exactly, and
the residual D1 support search has progressed from a six-cell frontier to a
certified lower bound of ten off-Sigma cells.  The old comparison-complex
lane remains retired unless a new physical source operation evades its
recorded locks.

The N=8 search has become substantially sharper, but it has not become a
near-proof.  It has eliminated every sparse D1 support through nine cells,
advanced the P5 local membership calculation by two filtered orders, and
reduced the first ten-cell D1 layer to a finite checked-proof frontier.  The
remaining D1 strata are denser, the P5 calculation is still finite-order,
and a complete N=8 theorem would still need an all-order mechanism.

The evidence from this cycle leans toward the conjecture rather than toward
a counterexample: every certified sparse D1 layer is empty, and the
corrected P5 calculation kills rather than exposes the next pure classes.
That is directional evidence only; it is not a probability estimate.

## Claude handoff: retained and retired

Retained:

- the live-split/good-crossing reduction to D1 and D2;
- the exact D2/Sigma artifacts, followed by the independent all-orientation
  audit in `dffdb86`;
- the D1 out-of-Sigma support model as the bounded exact-search domain;
- the negative terminal-Bianchi artifacts as supersession guards against
  reopening the same Schur, reset, and prolonged-derivation mechanisms.

Retired:

- terminal Bianchi as the primary positive proof allocation;
- the old four-day N=10 layer-four scratch search, whose log had not changed
  since August 4 after layers one through three merely returned SAT
  fifteen-cell supports;
- uncommitted attack-map conclusions which cite absent scratch and therefore
  are not reproducible from either checkout.

The stalled scratch process was stopped without deleting its log or changing
the terminal-Bianchi worktree.  All retained commits are ancestors of the
current main branch.

## Exact N=8 status

### D2

All 384 endpoint orientations are enumerated.  The 288 impossible
orientations fail E1/saturation; the two viable 48-family orbits have no
survivor; all 343 Signature-Lemma profiles compose to certificates.  The
hand Signature Lemma and upstream census reduction remain stated hand inputs.

### D1

The exact support-shadow closures are:

- `f5c43d3`: no six-cell support;
- `48f4bc0`: no seven-cell support;
- `575a053`: no eight-cell support;
- `cc8712a`: no nine-cell support.

Thus D1 requires at least ten nonzero aggregate cells outside Sigma.  At
ten cells, `6eb7099` compresses 1,196,640,200 raw additions to 271 symbolic
branches and freezes the first exact CNF.  Commits `77af00d` and `6b93c1a`
give independently checked deletion-free RUP certificates for five complete
support-base families.  Subsequent complete-shadow certificates close the
entire `4+4+2` family (`e310a0b`), all 58 `3+4+3` branches (`282fee5`), and
all 54 `4+3+3` branches (`de10254`).  In the final 131 `3+3+4` branches,
13,992 of 13,994 complete supports root-unit-refute against an 86-palette
basis.  The other two are the same semantic 77-cell support.  Its localized
coefficient ideal is empty by a three-binomials saturation certificate
(`d102341`).  The full ten-cell closure is `bf09216`; D1 now requires at
least eleven off-Sigma cells.  Native UNSAT alone is not promoted without a
checked proof trace.

### P5 formal-local branch

Commit `4de5dfd` kills the first eight-term H0 escape.  Commit `ad18a3b`
freezes the next mixed tails.  The original interpretation in `665f92d` was
withdrawn by `667f9f0`: a cache indexed by bare object identity returned
stale polynomials under CPython 3.13 identity reuse.

With identity-safe caches, Python 3.13 and 3.14 agree exactly:

- H1 at original degree seven cancels identically;
- H0 at original degree eight factors as
  `z16^2*z41*(z9*z25-z11*z46)` times a 28-term polynomial;
- consequently H0 vanishes on all three currently liftable components.

The next identity-safe calculation (`c75c9e3`) streams all 39 mixed tails
through degree eight.  The `z16` and `z41` components lift symbolically; one
generic-open rational point of the L component lifts after two exact free
bends.  Component-local pure reduction (`afa3da4`) then gives

- `H1_8 = 2*z4*z16^2*z41^2*(z44+z45)*L`, so H1 vanishes on all three
  components;
- a 424-term H0 degree-nine form which vanishes symbolically on `z16` and
  `z41` and at the certified twice-bent L point.

The dense generic L calculation is subsequently closed at this order by
`3e657f4`: two exact bend relations define a nonunit localized graph, all
mixed compatibility remainders reduce to zero, and the symbolic H0
degree-eight and degree-nine L remainders also reduce to zero.  No pure
survivor is certified.  This remains finite-order rather than an all-orders
standard-basis calculation.

## Uniform N to N+2 route

The forced-pair contraction is exact, and one arbitrary cross edge is
controlled.  Two cross edges falsify a universal one-controller linear
reconstruction, which led to a source-graded and then a swap-symmetrized
permanent analysis.

The resulting exact frontier is:

- the symmetrized linear grade has a nine-dimensional kernel (`807dbf1`);
- its nonlinear intersection with the rank-one permanent image is only the
  origin (`40283c0`);
- nonzero permanent-zero cross blocks cannot rescue a complete cut in the
  fixed anchored model (`3482802`);
- every fixed-old source with at most three nonzero cross coordinates fails
  cut two, including 231,336 two-class systems (`e6f183d`, with cleanup in
  `6b93c1a`);
- every four-cross support fails cut two after the complete stabilizer,
  quotient, torus-saturation and minor audit (`3699af6`).

At five cross cells, `0dfbf28` closes all 74,072,880 star orbits and the
natural old-node `2x3` biclique family.  Source-faithful affine/torus/minor
audits in `fcd911d`, `111c34c`, and `e7bfa13` close another 1,250,088
grade-three-through-six supports, leaving 10,364,088 `2+3` supports in the
fixed-old frontier.  The universal quadratic span already absorbs the
residual, so a source-independent linear quotient cannot finish this lane.
Simultaneous changes to the old source and arbitrary N-stability also remain
open.

## How close this is

An exact N=8 source would immediately disprove the conjecture after a full
6,561-coordinate reconstruction.  Conversely, closing D1 at ten cells or
advancing P5 one more order would still not prove N=8 emptiness, and a full
N=8 no-go would still not prove all even orders.

It is therefore misleading to attach one completion percentage.  The honest
assessment is:

- close to several decisive bounded subcomputations;
- materially closer to a complete, auditable N=8 search than at the start of
  the cycle;
- not yet close to a proof or disproof of the full conjecture.

The three highest-value parallel jobs are now:

1. begin the eleven-cell D1 normal-form/support-shadow layer and test whether
   the ten-cell palette/certificate basis transfers;
2. continue the identity-safe P5 recursion beyond generic-L H0 degree nine;
3. continue source-faithful affine/torus/minor batches on the remaining
   five-cross `2+3` supports before considering simultaneous old-source
   changes.

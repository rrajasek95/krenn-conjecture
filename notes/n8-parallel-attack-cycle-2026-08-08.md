# N=8 parallel attack cycle — 2026-08-08

This note records the execution cycle following
[`progress-reassessment-2026-08-08.md`](progress-reassessment-2026-08-08.md).
It changes the research allocation, not the conjecture status.  No exact
counterexample and no complete N=8 impossibility theorem is known.

## Outcome

The N=8 program is no longer one broad search.  It has two concrete exact
algebra targets, one discovery-only numerical campaign, and one uniform lane
which has reached a principled enumeration stop.

| lane | exact outcome | next target |
|---|---|---|
| D2 census geometry | all 384 endpoint orientations audited; 288 are E1/saturation-dead, the two viable 48-family orbits have 0 survivors, and all 343 Signature-Lemma profiles compose to certificates | audit maintenance only; the hand Signature Lemma and upstream census remain stated dependencies |
| D1 outside \(\Sigma\) | every source needs at least six off-\(\Sigma\) cells; at six cells, 5,184 signatures reduce to one 48-element orbit | solve the frozen 95-variable, 616-generator ideal localized at 12 cells; then classify supports with at least seven cells |
| exceptional mixed torus | \(H_1\) is locked through \(\mathfrak m^7\); the first eight-term \(H_0\) class survives only on Ferrers branch P5 | compute the degree-six P5 compatibility ideal with 45 bend parameters and reduce the \(H_0\) class on its components |
| unrestricted numerical search | compact entry bounds, norm bias, and pure/mixed/boundary diagnostics are now explicit; four cap-2 generic starts stopped at loss \(1/2\), while border starts used the imposed boundary | candidate discovery only; accept nothing without exact reconstruction and a 6,561-word audit |
| four-cut uniform backstop | no arbitrary-weight absent one-cell repair; 25,857 torus-finite two-cell pairs exhausted with no fourth cut | stop coefficient grids: 1,873 two-cell families retain continuous moduli, so require a symbolic four-cylinder identity |

## What changed about Claude's path

Claude's D2 mechanism was worth retaining.  Its former family-orientation and
equivariance qualifications are now closed by an independent exact audit.
D2 is therefore a completed N=8 lane conditional on the explicitly retained
hand inputs, not the main search direction.

The residual D1 direction was also worth retaining, but not in its broad
scratch parameterization.  A committed-input-only support cover now supplies
the first reproducible exact search input: one minimal support orbit, with a
frozen generator digest.  Missing historical scratch is no longer a blocker.

## Closeness

An exact point in either residual algebraic search still ends the conjecture
by disproof after exact reconstruction.  A proof that the frozen D1 ideal is
empty closes only the minimal six-cell D1 layer; supports with at least seven
cells remain.  Killing P5 at degree six excludes the only branch on which the
current local \(H_0\) class survives, but does not by itself prove global N=8
emptiness.  Even a complete N=8 theorem would still need a new mechanism for
N at least 10.

Thus the project is substantially closer to a decisive *N=8 experiment* but
not yet close to an all-order proof.  The two immediate exact jobs are:

1. modular/sparse elimination of the 95-variable D1 minimal-orbit ideal,
   removing linear variables and preserving the 12-cell localization;
2. streamed construction of the P5 degree-six compatibility ideal, followed
   by saturation against the eight-term \(H_0\) factorization.

## Reproducible artifacts

- [`D2 full-family audit`](n8-d2-full-family-orientation-audit.md)
- [`D1 minimal off-Sigma cover`](n8-d1-minimal-off-sigma-support-cover.md)
- [`streamed local next order`](n8-counterexample-streamed-next-order.md)
- [`P5 strict-transform prefix`](n8-p5-strict-transform-prefix.md)
- [`bounded full-search protocol`](n8-bounded-full-search-protocol.md)
- [`arbitrary-weight one-cell four-cut elimination`](n8-four-cut-arbitrary-weight-one-cell-elimination.md)
- [`two-cell four-cut orbit feasibility`](n8-four-cut-two-cell-orbit-feasibility.md)

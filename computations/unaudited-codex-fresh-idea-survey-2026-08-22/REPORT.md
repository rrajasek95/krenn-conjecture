# Fresh idea survey after the minimum-norm reduction

Status date: 2026-08-22.  This is a planning and scope document, not a
certificate and not a proof of the conjecture.

## The new organizing fact

If the exact eight-site fibre is nonempty, its squared source norm has an
attained minimum.  Exact clean-pair descent together with the certified
six-site obstruction says that every point of that fibre has no active clean
cap.  Thus there is no separate finite-boundary or escape-to-infinity branch
for the minimum-norm problem.  A useful new idea must couple the full mixed
GHZ equations to source-relative data at an attained no-cap point.

## Ideas tested in the present survey

1. **Alternating three-copy invariant plus minimum norm — retired.**
   The exact four-site GHZ minimum is already strict by a factor six in the
   sharp determinant/Hadamard inequality.  Phased six-site and Laurent
   eight-site controls are strict as well.  Fibre minimization therefore does
   not force equality in the global invariant bound.  See
   `unaudited-codex-alternating-invariant-norm-2026-08-22`.

2. **Rainbow matching triples with local rank multiplicity — retired as a
   standalone invariant.**  All 31 `S8 x S3` matching-triple geometries admit
   rank-respecting diagonal witnesses.  Nineteen already have a fourth
   physical perfect matching.  The remaining twelve have no one-cell
   completion, and every one of their 868 two-cell completion interfaces
   retains a literal mixed singleton.  This is a real first-shell theorem,
   but completion beyond that shell needs a structural exchange invariant.
   See `unaudited-codex-three-copy-31-rank-audit-2026-08-22` and its pending
   `unaudited-codex-three-copy-exchange-complex-2026-08-22`.

3. **Hermitianizing the six-site certificate — positive chartwise, retired as
   a direct global inequality.**  Free-rectangle determinant identities and odd
   Laurent-gain contradictions admit exact modulus-square/SOS forms.  Abstract
   global commonization always exists because six-site emptiness implies a
   rational Nullstellensatz certificate `1 = sum Q_w F_w`.  The actual question
   is whether an entirely new certificate compiles to a degree/growth bound
   that couples to minimum-norm stationarity.  The stored chart identities do
   not: an exact one-term support mutation makes a free-rectangle identity
   assert `0=1` while its old localizer remains a unit.  Moreover the cap
   pullback becomes singular near the activity divisor.  See
   `unaudited-codex-n6-cap-positive-pullback-2026-08-22`.

4. **Gain-graph local systems for the final m7 primitive — active.**
   Support feasibility repeatedly survives, but every coefficient replay so
   far contains an inconsistent gain cycle in `Z<3> x Z/6`.  Lazy exact
   circuit CEGAR is the only bounded complete formulation that has parsed;
   the monolithic gain encoding is sound but timed out at 479 MB.  This is a
   coefficient mechanism, not support counting.

## Recently retired generic shortcuts

The following have exact hostile controls and should not be reopened without
a new source-labelled hypothesis: tensor scaling/capacity, geometric
Brascamp--Lieb, bare ED/conormality, first-Jacobian carrier rank addition,
tail associated-graded rank, star-dual Cech/Koszul overlap, one-site CP or
Kruskal uniqueness, Hermitian least-star trace/SOS, five-sector matching-Gram
SDP, PEPS/Holant injectivity, top-tensor invariants, and ordinary
stress/rigidity matroids.

## Highest-value genuinely distinct next mechanisms

1. **Coefficient-valued exchange complex on the twelve sharp matching
   geometries.**  Uniform integer duals certify the quadratic gaps, but the
   support-only all-shell statement is false: the dense source `B=I+J` on all
   28 edges is rank-respecting and has 105 supported terms in every output
   word.  A continuation must put Laurent/gain coefficients on the exchange
   complex; no support-only cocycle, Farkas dual, or submodular potential can
   suffice.

2. **Degree-controlled global six-site Nullstellensatz inequality.**
   Compile the 19 rank/support strata and Laurent transfers into a homogeneous
   certificate with explicit localizer powers.  After normalizing projective
   cap variables, test whether its quantitative lower bound can be paired
   with exact block-normal equations.  Merely invoking abstract existence is
   insufficient.

3. **Matching-complex/local-system theorem behind gain CEGAR.**
   Prove that every support satisfying the `1222-k4` valuation clauses has a
   nontrivial gain cycle, replacing unbounded model-by-model circuit learning.
   The five-then-thousands of learned circuits show the right algebraic object
   but not yet a finite basis theorem.

4. **Two-site or matching-compatible secant circuits.**
   One-site CP uniqueness is too weak because the three GHZ colours can route
   through different neighbours.  A viable secant theorem must use circuits
   stable under perfect-matching deletion/exchange and force a shared physical
   edge, tight cut, or clean selector.  Arbitrary Segre-circuit classification
   would be excessive.

5. **Full-fibre singular normal cone.**
   Regular KKT is automatic at full Jacobian rank and Fritz--John multipliers
   have a huge vacuous kernel.  The remaining differential approach must use
   the local ideal/normal cone of the exact GHZ fibre, not carrier Hessians or
   an associated-graded tail matrix.

## Stopping rule

Promote an idea only if it yields a source-faithful identity, a finite exact
cover, or a hostile witness satisfying all hypotheses.  A rank count,
support-only SAT model, top-output invariant, or chart-local identity without
its transition/commonization data is not progress toward the global theorem.

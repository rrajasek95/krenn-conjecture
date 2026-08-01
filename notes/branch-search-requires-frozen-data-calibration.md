# The branch search needs frozen data to start at all

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  This is a guard about a
**method**, not about a packet.

## 1. Outcome

Most infeasibility statements in the h=3 star-sector artifacts are produced by
one decision procedure: propagate equations that reduce to a single repeated
variable, then split single-monomial equations into their factors.  It has
been doing a lot of work — 486, 2636 and 533 closed nodes in
[the trade note](h3-star-sector-anchor-terminal-class-trade.md), 695 in
[the monochromatic note](monochromatic-internal-quadratic-structure-and-eight-cycle-guard.md),
15 in
[the transport note](h3-star-sector-transport-collapse-general-peel-degenerate.md),
with 18 and 85 more in its complementary-guard checker
— so it is worth knowing where it has traction.

Two exceptions, so the claim is not overstated.  The colour-1 result of
[the witness note](h3-star-sector-pure-word-anchor-witness-and-colour-asymmetry.md)
is an explicit ideal-membership certificate, and C1/C2 of
[the cross-colour note](h3-cross-colour-repair-internal-edge-localization.md)
are formal identities; neither uses this search.  That note's own \(106\)-node
search is also a **strictly stronger** procedure — it adds Gaussian elimination
of linear rows, division by known-nonzero factors, and nonzero propagation —
so it is not measured here.

It has none at all without frozen coefficients.

| system | equations | unknowns | one-term equations | search |
|---|---|---|---|---|
| h=3, guard's colour-2 slice frozen | 2248 | 111 | **346** | collapse cascades; closes outright |
| h=3, nothing frozen, monochromatic | 6561 | 162 | **0** | 1 node, 1 open leaf |
| h=2, nothing frozen, monochromatic | 729 | 99 | **0** | 1 node, 1 open leaf |
| h=2, nothing frozen, general | 729 | 135 | **0** | 1 node, 1 open leaf |

The reason is immediate once measured: with nothing frozen **every generator
has at least two terms**, and a one-term equation is the procedure's only
entry point.  The frozen slice is not a convenience that speeds the search up;
it is the entire engine.

## 2. Why the h=2 row is the one that matters

At six vertices the answer is already known.
[`six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md)
proves that no six-vertex three-colour GHZ realization exists over arbitrary
complex matrices, so the h=2 system in the table is **infeasible**, and the
procedure still sees nothing whatever.

So on this benchmark the procedure is strictly weaker than a theorem the
project already has: it fails to decide a system the theorem decides.  The
converse does not hold — with a frozen slice it closes eight-vertex systems the
six-site theorem does not address — so the two are **not** comparable in
general.  What is fair to conclude is narrower and still useful: any
expectation that this procedure might settle eight vertices by itself was
misplaced, and this is the cheap experiment that says so.

One caveat on the benchmark itself.  The six-site obstruction is proved **in
this repository**, as the certified dependency `SP-K6`, and this project's
proof of it is unpublished.  The statement does have independent external
corroboration: a Lean 4 development reports a machine-checked proof of it over
the official `formal-conjectures` definitions, matching hypothesis for
hypothesis on a reading of those definitions — see
[the external certificate note](external-six-site-lean-certificate.md), which
records that development's trust boundary and its gated publication status.
Neither proof is audited here.  The calibration rests on the statement and
inherits whatever doubt remains attached to it.

## 3. Consequences

1. **The committed h=3 infeasibility results *that this search produces* are
   scope-limited to their frozen slice as a matter of method, not merely of
   wording.**  "Scope-limited" rather than "conditional": a theorem about a
   restricted system is unconditionally true of that system.  The notes do say
   this; the point here is that it could not have been otherwise.  Removing
   the frozen slice does not weaken those results a little, it removes the
   tool completely.
2. **A general attack needs different machinery.**  Linear algebra on a
   bounded-degree multiplier ansatz, an equivariant or multigraded method, or
   something else — but not this.
3. **Do not point this procedure at the unfrozen system again.**  It returns
   one node and one open leaf in well under a second, and an open leaf is not
   evidence of anything.

## 4. What structure is available instead

The rows do carry exploitable structure, just not the kind the branch search
consumes.  Give the four variable classes weights \(w_d,w_p,w_s,w_q\).  A
matching either uses the direct edge and \(h\) internal edges, or one star at
each endpoint and \(h-1\) internal edges, so every row's **left-hand side** is
homogeneous exactly when \(w_d+w_q=w_p+w_s\).  That is not enough.  The three
generators whose GHZ target is nonzero also carry a constant of grade \(0\), so
they are homogeneous only if the common grade is itself zero.  The generators
are homogeneous exactly when

\[
 \boxed{w_d+w_q=w_p+w_s\quad\text{and}\quad w_d+h\,w_q=0.}
\]

Two independent linear conditions on four weights, so the family is
**two-parameter**, not three.  The committed weight grading
\((w_q,w_p,w_s,w_d)=(-1,1,1,3)\) of
[the weight note](terminal-class-weight-invisibility-and-fourhole-grade-ladder.md)
is one member, and its common grade is zero — which is exactly what that note
records when it says every tensor coefficient has weight *zero*, not merely
equal weights.

Verified by sweep on the unfrozen h=3 **monochromatic** system: a grading
meeting both conditions leaves zero inhomogeneous generators; one meeting only
the first leaves exactly the three target-bearing generators; and one violating
the first leaves exactly \(1647\), the \(9\times183\) rows over the \(183\)
all-even words, which are the only rows carrying both term shapes at once.

Each **fully conforming** grading splits any multiplier linear system into
independent weight blocks, which is the obvious lever for a certificate search;
a grading meeting only the first condition does not, since an ideal with an
inhomogeneous generator has no such decomposition.  Whether the blocks are
small enough to be useful is **not** established here.

A finer localization of where the traction comes from: freezing the internal
quadratic alone gives \(0\) one-term equations, and so does freezing either
star alone, but freezing **both stars** gives \(336\).  The endpoint stars are
the engine, not the internal quadratic.

## 5. What this does not say

It says nothing about whether any of these systems is feasible.  It is a
statement about a tool, and specifically about that tool's entry condition.
Nor does it re-prove the six-site obstruction: that theorem is cited, not
reconstructed here, and it is what turns the h=2 row from an open question
into a calibration.

## 6. Audit

The dependency-free checker
[`verify_branch_search_frozen_data_calibration.py`](../computations/verify_branch_search_frozen_data_calibration.py)
builds all four systems from one parameterized model, asserts every equation
and unknown count, asserts that the frozen system has \(346\) one-term
equations while each unfrozen one has none and no generator with fewer than
two terms, and runs the procedure on each unfrozen system to confirm it halts
at one node with one open leaf.  It also checks directly that the frozen slice
is the source of the one-term equations, by building the same h=3 system with
and without it.

It also runs the search on the frozen system to confirm it closes outright,
sweeps the grading conditions in all three regimes, and measures the
partial-freezing census.

Standard library only, exact `Fraction` arithmetic, about thirteen seconds,
passing normal, `-O` and `-I -S`, deterministic across hash seeds.

The frozen slice is the colour-2 slice of
[the seven-row guard](h3-diagonal-segre-second-transgression-seven-row-guard.md).

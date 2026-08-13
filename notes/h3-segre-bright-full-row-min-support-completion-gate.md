# Full rows eliminate the smallest bright completion, not the axis-pure cancellation branch

## Result

Adding the genuine unary and pure-target equations sharpens the local
Segre-bright guard of `55054a0`, but it does not yet force every bright
packet into a known unit/fan/coloop.

The local block is

\[
  \begin{pmatrix}1&0&-1\\0&0&0\end{pmatrix}.
\]

Its two orientation sums are zero and its three linearized Segre minors are
`(1,2,1)`.  The pure diagonal target coefficient is one.  Since
`q^[3]=X0` has zero coefficient at the pure-`1` residual word, no direct
multiple of the unary row repairs this mismatch.  A full source must add
response occurrences of total value exactly one outside the displayed
block.

Crucially, the target equation fixes only the sum channel.  In the abstract
complete-row coefficient quotient, adding the symmetric correction
`(1/3,1/3,1/3)` changes the first orientation to
`(4/3,1/3,-2/3)`, whose sum is one, while preserving all three matching
differences `(1,2,1)`.  Hence the cylinder curvature

\[
                 t k=(A-B)(x_i-x_j)
\]

remains nonzero after imposing the unary and pure diagonal rows.  This is a
complete-row **coefficient quotient**, not a physical source lift of the
symmetric correction.  Constructing or obstructing that lift is precisely
the incidence/Tate-placement problem.

Checker:

```text
computations/verify_h3_segre_bright_full_row_min_support_completion_gate.py
```

Frozen ledger digest:

```text
cc9eaf836b0530140d88da803584c85080e83308dc396829c5982f8476d01aa8
```

## The exact smallest-support theorem

In the axis-purified direct-free chart, a monomial realization of the three
pure targets has the sharp decorated-coordinate lower bound

```text
q^[3]=X0:       3 q:00 cells,
G11=X1:         2 q:11 cells + p1 + s1,
G22=X2:         2 q:22 cells + p2 + s2.
```

Thus equality means `11` decorated source coordinates.  It is specified by
one six-site perfect matching for colour zero and a perfect matching plus a
distinguished endpoint edge for each of colours one and two.

The checker exhausts all

\[
             15\,(15\cdot3)^2=30,375
\]

labelled supports.  Exactly `3,960` give the unary target without another
decorated unary matching.  Exactly `360` also give both diagonal pure
targets with one monomial each.  Testing both orientations of each bright
endpoint edge gives `1,440` cases.  Every case has the literal profile

```text
G12: exactly one non-target matching monomial,
G21: exactly one non-target matching monomial.
```

The three target equations make all eleven support weights nonzero.  The
crossed terms are single monomials, so neither can cancel over a field.
Therefore

\[
\boxed{\text{no 11-coordinate axis-pure full source exists}.}
\]

This is stronger than a unit-weight search: the coefficients are arbitrary
nonzero scalars.

## What maximum-anchor/minimum-support does and does not add

The lexicographic maximum-anchor/minimum-support normalization is a choice
among exact sources; it is not another coefficient equation.  The theorem
above says that the naive lower-bound stratum is empty.  It does **not** say
that an exact minimum-support source, if one exists, must still have eleven
coordinates.

Consequently the complete local alternative is now:

1. An added offdiagonal decorated cell invokes the target-augmented
   private-site identity.  It produces a nonzero determinant/cofactor fan,
   which enters the committed four-good-or-literal-coloop landing.
2. If every added cell remains axis-purified, a full source must have more
   than eleven coordinates and use genuine multi-term cancellations.  The
   local bright guard is not yet excluded on this larger stratum.

The second arm is exactly the remaining axis-purified multisite
concentration theorem: prove that a minimum exact source with multiple
monomials in a pure target row admits a support-lowering switch, or else
produces an existing unit, coloop, or active carrier.

## Sharp status

The stronger full rows therefore remove the smallest clean/coloop-looking
completion, rather than proving that brightness itself vanishes.  No full
source-compatible bright guard is constructed.  The only unresolved
completion type is larger, axis-purified, and cancellation-dependent; any
offdiagonal completion is already routed.

Scope is the canonical `h=3` six-residual-site one-bad equations over a
field.  This does not prove emptiness of the full ternary GHZ source locus.

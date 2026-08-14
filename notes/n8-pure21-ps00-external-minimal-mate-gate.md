# The unique minimum external PS mate migrates to a torus unit

## Outcome

There is exactly one minimum-cost external mate of the nonlinear octagon's
first PS face.  It costs one new source cell:

\[
                  X=p_0(\text{site }4,\text{ physical colour }2). \tag{1}
\]

In the row (000022;00), it creates

\[
 X S_0 H a,\qquad \mathrm{PS},\qquad64\mid71\mid05\mid23, \tag{2}
\]

which can cancel the old term

\[
 P_0S_0a q_{45},\qquad \mathrm{PS},\qquad60\mid71\mid23\mid45. \tag{3}
\]

But the same (X) has the private complete-response migration

\[
 \boxed{X S_0c q_{35},\qquad(101222;00),\quad
        \mathrm{PS},\quad64\mid71\mid02\mid35.}          \tag{4}
\]

The two rows satisfy an exact polynomial unit certificate on the active
torus.  Consequently the unique minimum mate cannot close, and there is no
minimum-cost recurrent circuit.

## Exact minimum-cost census

The census uses the full presentation-safe source tables after adjoining the
twelve octagon cells.  In particular it retains the inherited mixed edge
(H=q_{05}^{0,2}); omitting (H) incorrectly raises the minimum cost.

For the word (000022) and head (00), enumerate every direct DQ matching and
every ordered PS endpoint pair with its remaining matching.  Count every
source-table entry absent from the current support.  The distribution is

\[
\begin{array}{c|rrrrr}
&0&1&2&3&4\\ \hline
\mathrm{PS}&1&1&13&33&42\\
\mathrm{DQ}&0&0&2&5&8.
\end{array}                                               \tag{5}
\]

The cost-zero PS path is (3).  The sole positive cost-one path has

\[
 p\text{-site}=4,\quad s\text{-site}=1,\quad
 q\text{-matching}=05\mid23,                             \tag{6}
\]

and its only missing entry is (X).  Thus (2) is not a chosen representative
of a larger minimum orbit; it is the entire minimum orbit.  All DQ mates and
all other PS mates cost at least two new cells.

## Forced migration and full replay

On the rational point from the preceding audit, (q_{45}=-2) and all inherited
factors in (2)--(3) equal one.  Cancellation therefore forces (X=2).
The checker inserts this value and replays all 6561 rows.  The new cell has
exactly nine incremental row effects:

```text
000022:00 +2   020022:01 +2   101222:00 +2
121122:01 +2   121222:01 +2   121222:02 +2
200022:00 +2   220022:01 +2   220022:02 +2
```

The first increment cancels (3).  The row (101222;00) was empty before
(X) was adjoined and becomes the single monomial (4), with value (+2).
The complete packet still has 34 nonzero full residual rows.  Thus the external mate does
not merely move debt among already occupied rows: it creates a genuinely
private operation-labelled face.

## Polynomial certificate

Write the two relevant full rows as

\[
\begin{aligned}
R_0&=S_0a(P_0q_{45}+XH),\\
R_1&=XS_0c q_{35}.
\end{aligned}                                             \tag{7}
\]

Direct multiplication gives

\[
 \boxed{c q_{35}R_0-aH R_1
       =P_0S_0a c q_{35}q_{45}.}                         \tag{8}
\]

Every factor on the right is inherited-normalized or belongs to the active
octagon torus.  The right side is therefore a unit in the relevant Laurent
ring, proving that (R_0=R_1=0) has no point there.  Notice that (8) does not
invert the new coefficient (X); the conclusion follows even before deciding
whether a proposed mate chart should explicitly localize at (X).

The next larger fibre begins at cost two: two DQ and thirteen PS paths.
Those paths are irrelevant to minimum-cost closure because the unique
cost-one mate is already excluded, but they are the exact place to look if a
future construction permits a simultaneous nonminimal packet rather than a
minimal support descent.

## Verification

Run

```text
python computations/verify_n8_pure21_ps00_external_minimal_mate_gate.py
python computations/verify_n8_pure21_ps00_external_minimal_mate_gate.py --mode classification
python computations/verify_n8_pure21_ps00_external_minimal_mate_gate.py --mode typed
python computations/verify_n8_pure21_ps00_external_minimal_mate_gate.py --mode replay
python computations/verify_n8_pure21_ps00_external_minimal_mate_gate.py --mode unit
```

The dependency-free checker derives the full 105-path cost census, proves
uniqueness of (1), retains every word/head/fine/operation label in (2)--(4),
replays all rows at the normalized mate value, and verifies (8) symbolically.

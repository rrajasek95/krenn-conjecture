# The first nonlinear dual defect closes on a lower PS unit row

## Outcome

The rational all-nonzero torus point from the first-octagon audit does cancel
the complete row containing the first Fredholm defect.  The single term

\[
 D c g q_{45},\qquad (121222;01),\quad
 67\mid02\mid13\mid45                                  \tag{1}
\]

has two same-word/head DQ companions.  At the rational point the three
matching values are (-2,+1,+1), so their complete-row sum is zero.

It does not survive the exhaustive source map.  Replaying all (3^6\cdot9)
word/head rows gives exactly 24 nonzero changes.  The lexicographically first
is the unique proper face

\[
 \boxed{P_0S_0a q_{45},\qquad (000022;00),\quad
        \mathrm{PS},\quad60\mid71\mid23\mid45.}          \tag{2}
\]

This row evaluates to (-2).  Under the inherited normalization and the
active-(q_{45}) localization it is a unit, so the current twelve-cell torus
fibre is empty in the full residual scheme.  No additional polynomial dual
is needed for this fibre.

## Restoring the complete defect row

With all twelve octagon cells symbolic, the full change at (121222;01) is

\[
 \Delta F_{121222;01}
  =Dc\bigl(gq_{45}+q_{14}q_{35}+q_{15}q_{34}\bigr).     \tag{3}
\]

All three terms are operation-DQ and retain the following fine matchings:

\[
\begin{array}{c|c|c}
\text{monomial}&\text{fine matching}&\text{rational value}\\ \hline
Dc gq_{45}&67\mid02\mid13\mid45&-2\\
Dc q_{14}q_{35}&67\mid02\mid14\mid35&1\\
Dc q_{15}q_{34}&67\mid02\mid15\mid34&1.
\end{array}                                               \tag{4}
\]

Thus the first singled-out monomial was not independently forced: its two
minimal matching companions cancel it in the literal complete row.  This is
why the localized ideal witness in the parent audit killed all eleven old
Fredholm rows.

## Exhaustive migration

The checker then evaluates every full symbolic row change at the rational
torus point.  Exactly 24 of the 6561 rows are nonzero.  Their normalized
word/head/value ledger is

```text
000022:00 -2   002222:20  1   012212:21  1
020000:01  1   020022:01 -4   022122:21  1
101221:10  1   111211:11  1   111212:01  1
111212:02 -1   121121:11  1   202200:20 -1
202222:20  4   210011:11  1   210012:01  1
210012:02 -1   212112:21  1   212212:21  3
212212:22 -1   220000:01  1   220000:02 -1
222100:21  1   222200:21  1   222222:21  2
```

The first entry has no second term anywhere in the current source support.
It uses the inherited head-(00) response endpoints (P_0) at site 0 and
(S_0) at site 1, the inherited colour-zero edge (a=q_{23}), and the new
active colour-two edge (q_{45}).  Its word is therefore exactly (000022),
and its formal matching is (60\mid71\mid23\mid45).  This is a PS migration,
not another DQ cofactor relation.

## Laurent unit certificate

Put

\[
 E=(P_0-1)S_0a+(S_0-1)a+(a-1)=P_0S_0a-1.              \tag{5}
\]

For the residual (R=P_0S_0a q_{45}) there is the exact identity

\[
 R=q_{45}(1+E).                                         \tag{6}
\]

After localizing at the active cell (q_{45}), this becomes

\[
 \boxed{1=q_{45}^{-1}R-E.}                              \tag{7}
\]

Hence (R) together with the inherited normalization equations generates the
unit ideal on this torus chart.  The obstruction is stronger than the
earlier finite sign census and applies to arbitrary nonzero complex values
of the twelve new cells.

The exact remaining boundary is also clear: a completion may try to add new
source cells outside the twelve-cell octagon support to create a mate for
(2).  Classifying those external PS/DQ mates and their next migrations is a
strictly larger fibre; the present theorem closes the simultaneous octagon
fibre itself.

## Verification

Run

```text
python computations/verify_n8_pure21_first_nonlinear_defect_complete_row_gate.py
python computations/verify_n8_pure21_first_nonlinear_defect_complete_row_gate.py --mode complete-row
python computations/verify_n8_pure21_first_nonlinear_defect_complete_row_gate.py --mode replay
python computations/verify_n8_pure21_first_nonlinear_defect_complete_row_gate.py --mode unit
```

The dependency-free checker restores the three DQ matchings, replays all
6561 rows at the rational point, pins the full 24-row ledger, verifies the
unique typed PS face (2), and checks the polynomial/Laurent identity (7).

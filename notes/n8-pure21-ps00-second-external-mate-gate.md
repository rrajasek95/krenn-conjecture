# The second external minimum orbit has two terminal branches

## Outcome

The private face

\[
 X S_0c q_{35},\qquad(101222;00),\quad
 64\mid71\mid02\mid35                                  \tag{1}
\]

has exactly two positive minimum-cost mates.  Each costs one new source cell:

\[
 X_3=p_0(3;2),\qquad X_5=p_0(5;2).                     \tag{2}
\]

They do not form a recurrent circuit, individually or simultaneously.  The
complete minimum orbit has two private migrations,

\[
\begin{aligned}
R_3&=X_3S_0bc, &&(101200;00),&&64\text{ replaced by }63,\\
R_5&=X_5S_1ce, &&(111112;01),&&65\mid73\mid02\mid14,
\end{aligned}                                           \tag{3}
\]

and the target plus these two rows generate a torus unit by an explicit
polynomial identity.

This step also disproves the simplest proposed global potential: the two
migrations lie on opposite lexicographic sides of the target, at the same
external cost.  A (cost, word/head lex) ordering cannot orient both branches.
The observed tail-edge filtration remains a useful local heuristic, not yet
a global theorem.

## Minimum-cost classification

Retain the twelve nonlinear-octagon cells and
(X=p_0(4;2)).  For word (101222), the current source support contains the
matching (02\mid35), with (c=q_{02}^{1,1}) and active
(q_{35}^{2,2}).  Exhaustive DQ/PS enumeration gives

\[
\begin{array}{c|rrrrr}
&0&1&2&3&4\\ \hline
\mathrm{PS}&1&2&15&38&34\\
\mathrm{DQ}&0&0&3&6&6.
\end{array}                                              \tag{4}
\]

The two cost-one PS paths are exactly

\[
\begin{array}{c|c|c|c}
\text{new cell}&p\text{-site}&s\text{-site}&q\text{-matching}\\ \hline
X_3&3&1&02\mid45\\
X_5&5&1&02\mid34.
\end{array}                                              \tag{5}
\]

Thus the full target row on the simultaneous minimum fibre is

\[
 R_0=S_0c(Xq_{35}+X_3q_{45}+X_5q_{34}).                 \tag{6}
\]

Its three PS fine matchings are respectively

\[
64\mid71\mid02\mid35,\quad
63\mid71\mid02\mid45,\quad
65\mid71\mid02\mid34.                                  \tag{7}
\]

## Individual normalized migrations

At the rational parent point, (X=2), (q_{35}=q_{34}=1), and
(q_{45}=-2).  Hence the individual normalized mates are

\[
                  X_3=1,\qquad X_5=-2.                 \tag{8}
\]

Adjoining (X_3) has seven incremental rows; adjoining (X_5) has six.  In
each case the target (R_0) becomes zero, but the corresponding row in (3)
is new and nonzero.  Both final source packets have 32 nonzero full residual
rows.  The exact incremental ledgers are pinned by the checker.

The first migration is

\[
 X_3S_0bc,qquad(101200;00),\quad
 \mathrm{PS},\quad63\mid71\mid02\mid45,                 \tag{9}
\]

where (b=q_{45}^{0,0}) is the inherited pure colour-zero edge.  The second is

\[
 X_5S_1ce,qquad(111112;01),\quad
 \mathrm{PS},\quad65\mid73\mid02\mid14,                \tag{10}
\]

and uses only inherited colour-one response data.  Neither terminal row
contains another term in the current simultaneous support.

## Aggregate polynomial certificate

Equations (3) and (6) obey

\[
\boxed{
 S_1ebR_0-S_1eq_{45}R_3-S_0bq_{34}R_5
   =XS_0S_1bceq_{35}.}                                  \tag{11}
\]

Every factor on the right is inherited-normalized or active on the parent
torus.  Hence the right side is a unit in the Laurent ring.  This excludes
not only each individual mate but any aggregate choice of (X_3,X_5) that
cancels (R_0).  In particular there is no hidden two-mate recurrent circuit.

## Boundary of a well-founded potential

All three external mate steps found so far have cost one, so cost alone is
constant.  Lexicographically,

\[
              (101200;00)<(101222;00)<(111112;01).       \tag{12}
\]

Thus neither increasing nor decreasing word/head lex order follows both
minimum branches.  The exact counterexample (12) rules out a global
(cost,lex) proof without an additional filtration.

Along the *private migration* chain, the active octagon tail edge has moved

\[
                  q_{45}\longrightarrow q_{35}
                  \longrightarrow\text{inherited-only}. \tag{13}
\]

This gives a local finite potential: the left endpoint of the active new
tail edge decreases and then exits the octagon support.  Equation (11), not
an unproved extrapolation of (13), is the actual terminal certificate.  A
global invariant would need to show the same tail decrease for every higher-
cost simultaneous mate packet; the present census does not claim that.

## Verification

Run

```text
python computations/verify_n8_pure21_ps00_second_external_mate_gate.py
python computations/verify_n8_pure21_ps00_second_external_mate_gate.py --mode classification
python computations/verify_n8_pure21_ps00_second_external_mate_gate.py --mode typed
python computations/verify_n8_pure21_ps00_second_external_mate_gate.py --mode replay
python computations/verify_n8_pure21_ps00_second_external_mate_gate.py --mode unit
python computations/verify_n8_pure21_ps00_second_external_mate_gate.py --mode potential
```

The checker derives the complete 105-path cost census, identifies both
minimum mates, preserves all word/head/operation/fine labels, replays both
normalized branches over all 6561 rows, verifies (11) symbolically, and pins
the lexicographic counterexample (12).

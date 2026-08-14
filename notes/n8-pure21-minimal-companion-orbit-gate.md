# All twelve minimal pure-(21) companions are unit-excluded

## Outcome

Continue from the repaired mixed (F_{02}/F_{01}) corner.  Its first
remaining migrated residue is

\[
 U_{21}=P_2Yfg
\]

at word (222222), head (21), operation PS, fine matching
(62\mid75\mid04\mid13).  In the normalized packet (U_{21}=-1).

Every new DQ or PS term which can cancel (U_{21}) needs at least two new
source cells.  There are exactly twelve minimal terms:

\[
                    1\ \mathrm{DQ}+11\ \mathrm{PS}.
\]

They split into three exact migration mechanisms.

1. The unique DQ mate creates a nonzero pure direct term under head (01).
2. Five PS mates introduce a new (s_1) coefficient; the existing (p_1)
   reuses it in a mixed diagonal (11) row, hence in the contracted apolar
   equation.
3. Six PS mates use only new (p_2/q) data; the same term occurs
   proportionally in head (22) and cancels the unit target anchor.

Each of the twelve has an explicit polynomial Nullstellensatz certificate.
Thus every two-cell completion is excluded.  The exact remaining scope is
the orbit of companions requiring at least three new source cells; no claim
is made about that larger fibre.

## Minimal-orbit classification

On the pure colour-two slice the old source supports are

\[
 P_2:\{2\},\qquad S_1:\{5\},\qquad Q_2:\{04,13\}.      \tag{1}
\]

A PS term chooses distinct endpoint sites (x,y) and a matching of the four
remaining sites.  Count one new cell for each of (P_{2,x}), (S_{1,y}),
and the two (Q_2)-edges absent from (1).  Apart from the old cost-zero
term, the minimum is two.  The eleven cost-two choices are:

\[
\begin{array}{c|c}
\text{type}&\text{new cells}\\ \hline
\text{reverse }25&P_{2,5},S_{1,2}\\
\text{new }S_1+Q&S_{1,0}+45,\ S_{1,1}+35,\ S_{1,3}+15,\ S_{1,4}+05\\
\text{new }P_2+Q&P_{2,0}+24,\ P_{2,1}+23,\ P_{2,3}+12,\ P_{2,4}+02\\
\text{new cofactor}&01+34,\ 03+14.
\end{array}                                               \tag{2}
\]

A DQ term additionally needs the previously absent direct head (a_{21}).
Among the fifteen internal perfect matchings, the unique cost-two choice is

\[
                     a_{21}+q_{25}(2,2),
 \qquad 67\mid25\mid04\mid13.                            \tag{3}
\]

The checker derives (2)--(3) by matching enumeration; they are not a hand
declared completeness assumption.

## The twelve first migrations

Normalize the two new cells in each row so that its new term equals
(-U_{21}=1).  Exact all-word replay gives:

\[
\begin{array}{c|c|c|c|c|r}
\text{mate}&\text{mechanism}&\text{word}&\text{head}&\text{fine witness}&\text{value}\\ \hline
DQ25&\text{direct}&222222&01&67|04|13|25&1\\
REV25&\text{new }s_1&222221&11&04|13|65|72&1\\
S0+45&\text{new }s_1&210011&11&14|23|65|70&1\\
S1+35&\text{new }s_1&220021&11&04|23|65|71&1\\
S3+15&\text{new }s_1&111211&11&02|14|65|73&1\\
S4+05&\text{new }s_1&121221&11&02|13|65|74&1\\
P0+24&22\text{ anchor}&222222&22&13|24|60|75&-1\\
P1+23&22\text{ anchor}&222222&22&04|23|61|75&-1\\
P3+12&22\text{ anchor}&222222&22&04|12|63|75&-1\\
P4+02&22\text{ anchor}&222222&22&02|13|64|75&-1\\
01+34&22\text{ anchor}&222222&22&01|34|62|75&-1\\
03+14&22\text{ anchor}&222222&22&03|14|62|75&-1.
\end{array}                                               \tag{4}
\]

Every row in (4) retains word, head, operation (DQ only in the first row,
PS otherwise), and fine matching.  In every specialization the selected
pure (21) row is exactly zero before the witness is read.

## Polynomial certificates

Write

\[
 A=A_0A_1A_2,qquad A_i=1,qquad D=H=1,qquad Y=-1.      \tag{5}
\]

All identities below hold before imposing (5).

### DQ mate

Let (K=q_{25}(2,2)), (R=a_{21}),

\[
 C_{21}=U_{21}+RKfg,qquad L_{01}=DKfg.
\]

Then

\[
                         RL_{01}-DC_{21}=-DU_{21}.       \tag{6}
\]

Multiplication by (S_2), followed by

\[
 D(Y+1)-(D-1)=DY+1,
\]

gives the explicit unit certificate

\[
\boxed{
1=S_2(RL_{01}-DC_{21})
 +[D(Y+1)-(D-1)]A_2-(A_2-1).}                           \tag{7}
\]

Thus the DQ repair necessarily migrates to direct head (01).

### Five new-(s_1) mates

For the reverse orientation, with new cells (X=P_{2,5}),
(Z=S_{1,2}), put

\[
 C_{21}=U_{21}+XZfg,qquad W_{11}=P_1Zfg.
\]

Then

\[
                         XW_{11}-P_1C_{21}=-P_1U_{21}.  \tag{8}
\]

For each of the other four rows, write its new cells as (Z,K), its old
colour-two edge as (E), and the two old (q)-edges in the diagonal
witness as (J).  Then

\[
 C_{21}=U_{21}+P_2ZKE,qquad W_{11}=P_1ZJ,
\]

and

\[
             (P_2KE)W_{11}-(P_1J)C_{21}=-(P_1J)U_{21}. \tag{9}
\]

The right sides of (8)--(9) are (-Y) times monomials in the anchor
variables.  Choose (k\le2) and the monomial (N) such that

\[
 N\cdot(\text{right side})=-YA^k.
\]

This gives the literal uniform certificate

\[
\boxed{
1=N\cdot(\text{migration identity})+(Y+1)A^k-(A^k-1),} \tag{10}
\]

where

\[
 A^k-1=(A-1)(1+A+\cdots+A^{k-1})
\]

and

\[
 A-1=(A_0-1)A_1A_2+(A_1-1)A_2+(A_2-1).               \tag{11}
\]

Equations (10)--(11) are an ordinary polynomial certificate, not shorthand
for localization.  The checker constructs and verifies (N) in every one
of the five cases.

### Six anchor-shift mates

Let (V_{21}) be any of the six new (21) terms and let (V_{22}) be the
term obtained by replacing the same (s_1) coefficient (Y) by the anchor
coefficient (S_2).  Put

\[
 C_{21}=U_{21}+V_{21},qquad
 C_{22}=A_2+V_{22}-1.
\]

Literal shared-star proportionality gives

\[
                    Y(C_{22}+1)-S_2C_{21}=0.            \tag{12}
\]

Hence the degree-one unit certificate is

\[
\boxed{1=(Y+1)-S_2C_{21}+YC_{22}.}                     \tag{13}
\]

If the new term cancels head (21), it also cancels the complete response
in head (22), leaving the target residual (-1).

## Exact remaining scope

The minimal companion orbit is exhausted and unit-excluded.  A surviving
completion must introduce at least three new source cells in one term, or
several individually nonminimal terms whose aggregate cancels the witnesses
in (4).  Such a completion can couple distinct fine matchings, so the
single-term identities above do not classify it.

The next honest object is therefore a multi-companion recurrence: determine
whether sums of cost-three paths can cancel the direct-head, diagonal-(11),
and anchor-(22) witnesses simultaneously.  This note proves no active-cap
or support-lowering theorem for that larger orbit.

## Verification

Run

```text
python computations/verify_n8_pure21_minimal_companion_orbit_gate.py
python computations/verify_n8_pure21_minimal_companion_orbit_gate.py --mode classification
python computations/verify_n8_pure21_minimal_companion_orbit_gate.py --mode source
python computations/verify_n8_pure21_minimal_companion_orbit_gate.py --mode certificates
```

The dependency-free checker derives all twelve minimal paths, replays all
6561 rows for every normalized companion, checks the typed witnesses, and
verifies (7), every instance of (10), and every instance of (13).

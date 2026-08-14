# The unique same-fine (PS_{01}) mate migrates to pure head (21)

## Outcome

The cross-head relation left by the first (F_{02}(010012)) DQ companion
has a unique smallest solution on the same fine matching.  It adds the
single endpoint coefficient

\[
                         s_{1,5}(2)=Y.
\]

At the normalized value (Y=-1), this (PS_{01}) mate repairs the migrated
mixed head (01), while the preceding DQ companion keeps head (02) exact.
It also satisfies the required relation

\[
                         a_{02}M_{01}-a_{01}M_{02}=0.
\]

But the coefficient (Y) is shared source data.  The existing (p_2) star
immediately reuses it on the pure word (222222), in head (21), on the
same fine matching as the nonzero (22) anchor.  That pure off-diagonal row
has value (-1).  An exact polynomial Nullstellensatz identity proves that
the repaired mixed head, the pure (21) row, and the three anchors cannot
all vanish on the normalized chart.

Thus the smallest (PS_{01}) completion is closed by a unit, not by an
active-clean conclusion.  The remaining completion would have to add a new
pure-(21) DQ/PS companion; this note makes no claim about that larger
support fibre.

## Unique same-fine mate

Retain the mixed residual word

\[
                             \omega=010012
\]

and the full matching (60\mid75\mid14\mid23).  Head (01) fixes the
first endpoint star to (p_0) and the second to (s_1).  The matching fixes
their residual sites to (0,5), and the word fixes their physical colours
to (0,2).  The (p_{0,0}(0)=P_0) coefficient already exists.  Therefore
the only new same-fine endpoint coefficient is

\[
                             s_{1,5}(2)=Y.              \tag{1}
\]

No support or basis choice is hidden in this classification: changing the
site changes the fine matching, and changing the physical colour changes
the word.

Use the earlier notation

\[
\begin{aligned}
 M_{02}&=P_0S_2ae,& a_{02}&=T,\\
 M_{01}&=P_0Yae,& a_{01}&=D,\\
 F&=Hae.
\end{aligned}
\]

Then the two mixed rows are

\[
 C_{02}=TF+M_{02},\qquad C_{01}=DF+M_{01}.              \tag{2}
\]

Their exact elimination identity is

\[
 T C_{01}-D C_{02}=T M_{01}-D M_{02}.                  \tag{3}
\]

At

\[
 D=H=1,\qquad T=Y=-1,
\]

and with every old cell normalized to one, both sides of (3) vanish and

\[
                             C_{02}=C_{01}=0.            \tag{4}
\]

So this is a genuine source-labelled solution of the previously missing
cross-head relation, not another formal scalar mate.

## Full typed migration

The repaired mixed corner and its pure reuse are

\[
\begin{array}{c|c|c|c|r}
\text{word}&\text{head}&\text{operation}&\text{fine matching}&\text{value}\\ \hline
010012&02&PS&60\mid75\mid14\mid23& 1\\
010012&02&DQ&67\mid05\mid14\mid23&-1\\
010012&01&DQ&67\mid05\mid14\mid23& 1\\
010012&01&PS&60\mid75\mid14\mid23&-1\\ \hline
222222&21&PS&62\mid75\mid04\mid13&-1\\
222222&22&PS&62\mid75\mid04\mid13& 1.
\end{array}                                               \tag{5}
\]

The last row is the existing colour-two target anchor.  The new (21)
row differs from it only in the endpoint-head label (1) versus (2): the
word, operation, and fine matching are identical.  This is literal shared
second-star naturality.

## Pure-head unit certificate

Put

\[
 U_{21}=P_2Yfg,qquad A_2=P_2S_2fg,qquad G=P_0S_2ae.
\]

Because (G U_{21}=A_2M_{01}), equation (2) gives

\[
                    A_2C_{01}-G U_{21}=A_2DHae.         \tag{6}
\]

Let

\[
 A_0=P_0S_0ab,qquad A_1=P_1S_1ce,qquad
 N=(P_0S_0b)(P_1S_1c).
\]

Multiplying (6) by (N) gives (DHA_0A_1A_2).  Hence the following is an
identity in the ordinary polynomial ring:

\[
\boxed{\begin{aligned}
1={}&N(A_2C_{01}-GU_{21})
 -(H-1)DA_0A_1A_2\\
 &-(D-1)A_0A_1A_2
 -(A_0-1)A_1A_2-(A_1-1)A_2-(A_2-1).
\end{aligned}}                                             \tag{7}
\]

Thus

\[
 (H-1,D-1,A_0-1,A_1-1,A_2-1,C_{01},U_{21})=(1).        \tag{8}
\]

The unit is detected before any Hall, radical, or support argument.  It is
the direct algebraic expression of the shared pure anchor in (5).

## Exhaustive normalized ledger

After adjoining (Y=-1), an exact replay of all
(3^6\cdot9=6561) rows has only five residuals:

\[
\begin{array}{c|c|r}
\text{word}&\text{head}&\text{value}\\ \hline
012112&21&1\\
121200&01&1\\
121200&02&-1\\
200021&10&1\\
222222&21&-1.
\end{array}                                               \tag{9}
\]

Both rows at (010012) are now exact.  The contracted packet is unchanged:

\[
 r^{[3]}=0,
 \qquad rq^{[2]}=-\Delta_{6,3}.                         \tag{10}
\]

Indeed the new (s_1) coefficient lives at the same decorated port as
(p_1), so their diagonal product is killed by the site-square-zero rule.
The obstruction in (9) is visible only before contracting the nine heads.

## Exact next boundary

On the present support, the pure colour-two internal slice contains only
(04\) and (13), so its hafnian is zero.  The full pure (21) equation is
therefore exactly (U_{21}=0), contradicted by (7).

A larger completion has two possible kinds of escape:

1. add a pure (q_{25}(2,2)) edge and a direct (a_{21}) head, creating a
   DQ mate on (67\mid25\mid04\mid13); or
2. add a second (PS_{21}) matching with different endpoint sites and
   internal cofactor.

The first escape will make the new pure hafnian visible under every existing
direct head, including (01); the second leaves the same shared-star
naturality problem on a different fine matching.  Neither is excluded by
this note.  The exact next task is therefore the pure-(21) companion orbit,
not the already solved mixed cross-head relation.

## Verification

Run

```text
python computations/verify_n8_f02_ps01_mate_pure_head_migration_gate.py
python computations/verify_n8_f02_ps01_mate_pure_head_migration_gate.py --mode classification
python computations/verify_n8_f02_ps01_mate_pure_head_migration_gate.py --mode typed
python computations/verify_n8_f02_ps01_mate_pure_head_migration_gate.py --mode relation
python computations/verify_n8_f02_ps01_mate_pure_head_migration_gate.py --mode source
python computations/verify_n8_f02_ps01_mate_pure_head_migration_gate.py --mode apolar
python computations/verify_n8_f02_ps01_mate_pure_head_migration_gate.py --mode unit
```

The checker classifies the same-fine mate, retains all word/head/operation/
fine labels, replays every normalized row, verifies the contracted packet,
and checks (3) and (7) as exact polynomial identities.

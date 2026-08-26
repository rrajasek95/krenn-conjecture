# The minimal total carrier is equivalent to the unresolved balanced filler

Status: **NO CONSTRUCTION FROM THE PINNED SOURCE CHAINS.**

Parent manifest:
`f443971c89f61ecd255e5e23840936b52f41e3aea10a29ef1c544239223bcdc4`.
Scope: the canonical source-labelled `h=3` chart only.  Nothing below is a
uniform-`h` statement or a PAComp promotion.

## 1. The proposed shortcut is exactly the old open arrow

Put

\[
 A=Dq_{01}H,\qquad B=p_0s_1H,\qquad C=p_1s_0H,
 \qquad H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.
\]

The genuine, source-provenant endpoint-choice graphs are

\[
 d\Gamma_B=t_B+A-B,\qquad d\Gamma_C=t_C+A-C.       \tag{1}
\]

Thus, with `T=t_B+t_C` and `L01=2A-B-C`, one has

\[
              d(\Gamma_B+\Gamma_C)=T+L_{01}.        \tag{2}
\]

There is an exact two-way reduction:

\[
\begin{array}{rcl}
 dE_T=T&\Longrightarrow&
 \Lambda_{01}=\Gamma_B+\Gamma_C-E_T,
 \quad d\Lambda_{01}=L_{01},\\[2mm]
 d\Lambda_{01}=L_{01}&\Longrightarrow&
 E_T=\Gamma_B+\Gamma_C-\Lambda_{01},
 \quad dE_T=T.
\end{array}                                         \tag{3}
\]

Consequently an `E_T` construction cannot bypass the balanced `L01`
filler.  It is the same missing arrow, written in the retained-carrier
basis.

This is already detected before taking proper faces.  The endpoint-chart
plane has rank two, while adjoining `L01` raises it to three:

```text
rank(B,C)=2,     rank(B,C,L01)=3.
```

In the source-faithful fixed-window packet the corresponding statement is

```text
old packet                                      rank 46
+ DQ <-> PS01 switch family                     rank 47
+ DQ <-> PS10 switch family                     rank 48.
```

The four formal mates make a `K2,2` of rank three, with one-dimensional
alternating quotient `(1,1,-1,-1)`.  Both switch types are needed.  The
current fixed-window constructor contains neither operation-changing edge.

## 2. The 36 proper faces do not totalize absolutely

Differentiate the nine terms of `L01`.  Each of the three charts has three
residual matchings.  Differentiating the two factors in each matching gives
six tail faces per chart; differentiating the two outer direction factors
gives six direction faces per chart.  Hence

```text
tail faces       3 charts x 3 tails x 2 factors = 18
direction faces  3 charts x 3 tails x 2 factors = 18
total                                                36
chart coefficients                                  2,-1,-1.
```

The available endpoint response deformation does not supply the selected
six-term `db01` carrier (nor its reversed mate), and the direct capped
`U_C4[D,Q01;2345]` reinsertion is likewise not an absolute source column.
So the literal construction already stops on the tail half.

To test whether granting those tail faces would suffice, use the strongest
presentation-safe relative `C4` totalization.  In one block write

\[
 dx=x',\quad dy=y',\quad dU=H-r,
 \qquad K=-d(xy)U=-(x'y+xy')U.                       \tag{4}
\]

Then

\[
\begin{aligned}
 d(-x'yU)&=x'y(H-r)+x'y'U,\\
 d(-xy'U)&=xy'(H-r)-x'y'U,
\end{aligned}
\]

so the two mixed reinsertion faces cancel term by term and

\[
                        dK=d(xy)(H-r).               \tag{5}
\]

This is a genuine positive calculation.  It cancels the selected `H`
direction faces without a sign or support error.  But, in the pinned
switch--Weyl orientation, it exports the closed retained face

\[
\begin{aligned}
R_{\rm ret}={}&-2((dD)q_{01}+D(dq_{01}))r_{DQ}\\
&+((dp_0)s_1+p_0(ds_1))r_{PS01}\\
&+((dp_1)s_0+p_1(ds_0))r_{PS10}.                     \tag{6}
\end{aligned}
\]

Here `dr_j=0`, so (6) is not a bookkeeping artefact.  Setting `r_j=0`
would make the cap absolute by changing the old `H0`; it is not an allowed
presentation-preserving cancellation.

## 3. Smallest independent face quotient

The retained obstruction persists after all complete companion occurrences
are restored.  In coordinates `(C,z00,z01,z10,z11)`, the four complete rows
are

\[
\begin{aligned}
F_{A0}&=C+z_{00}+z_{01},&F_{A1}&=C+z_{10}+z_{11},\\
F_{B0}&=C+z_{00}+z_{10},&F_{B1}&=C+z_{01}+z_{11}.
\end{aligned}                                       \tag{7}
\]

They have rank three, with the sole centered relation

\[
F_{A0}+F_{A1}-F_{B0}-F_{B1}=0.
\]

Adjoining the selected core `C` raises the rank to four.  The exact dual

\[
             \eta=(1,-\tfrac12,-\tfrac12,-\tfrac12,-\tfrac12)     \tag{8}
\]

kills all four rows and reads `1` on `C`.  Therefore the smallest surviving
face quotient is one-dimensional.  Scalar localization cannot remove it.

With the signs of (6), the exact next generator would be a source-labelled,
fixed-window, covariant cell `Pi_r,01` satisfying

\[
\begin{aligned}
d\Pi_{r,01}={}&+2((dD)q_{01}+D(dq_{01}))r_{DQ}\\
&-((dp_0)s_1+p_0(ds_1))r_{PS01}\\
&-((dp_1)s_0+p_1(ds_0))r_{PS10}=-R_{\rm ret}.        \tag{9}
\end{aligned}
\]

No such column occurs in the pinned source registry.  One may equivalently
postulate a single *total* `Lambda_01` whose leading boundary is `L01` and
whose lower components contain the tail corrections, the three relative
reinsertion squares, and (9).  Equation (3) would then define `E_T`.
Calling this package a single total generator does not make its absent
physical components consequences of the existing square/cube identities.

For downstream `X23`, all four operation mates still leave the separate
66-term neither-`a`-nor-`b` cap--Eq complement for each of the literal
`AB` and `AC` roots.  That debt is not part of the standalone equation
`dE_T=T` and cannot cancel across root labels.

## 4. H0, restriction, reinsertion and covariance guards

In coordinates `(A,B,C,tB,tC)`, the complete response and the two relative
graphs have rank three, hence quotient dimension two.  Adding one total
boundary `T` raises the rank to four and leaves quotient dimension one;
adding `tB,tC` separately raises it to five and kills the quotient.  Thus a
single `E_T` kills exactly the balanced carrier class.  It is an absolute
attachment, not a presentation-safe rewrite.

Likewise, `dU=H-r` replaces two coordinates by one monic relation and keeps
one local `H0` class.  The absolute specialization `dU=H` kills it.  The
reinsertion calculation (4)--(5) is exact but cannot justify that
specialization.

For restriction to one endpoint object there are only two known folds:

- canonical transport maps `B` or `C` back to `A`, giving zero switch
  boundary and preserving the old two-dimensional chart `H0`;
- raw forgetting gives `B-A` and `C-A`, but the response plus these two
  rows has rank three in three coordinates and kills that `H0`.

Therefore restriction does not construct either missing switch.

At coefficient level, both total mate involutions `tau_a,tau_b` send the
alternating `K2,2` charge to its negative.  The cut involution
`(2 5)(3 4)` permutes the three residual matchings and fixes their sum.
Any new total `Lambda_01`/`Pi_r,01` must consequently be tau-anti-equivariant
and cut-sigma covariant.  These are necessary character checks only.
Physical tau/sigma and AB/AC naturality remain untypable until the new cell
exists; assigning them now would assume the conclusion.

## Exact stopping point

There is no source-valid construction of `E_T` in the pinned chain
inventory.  The earliest obstruction is the one-dimensional balanced chart
quotient, requiring both operation-switch families.  Under their strongest
formal grant and the exact relative-`C4` reinsertion, the first surviving
proper-face obstruction is again one-dimensional, represented by (6) and
detected by (8).  The exact next physical datum is (9), or one total
`Lambda_01` packaging it together with the preceding source-labelled face
corrections.  No PAComp, `Q23`, uniform-`h`, or terminal claim is promoted.


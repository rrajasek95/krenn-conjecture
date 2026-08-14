# The four-site response gives a tied `B=Eq` lift, not an absolute `U_C4`

## Exact outcome

The physical h=2 response and normalized target equations do not construct
an absolute same-grade

```text
U_C4[D,Q01;2345].
```

Their private/lower and reduced-Eq incidence matrices are identical.  This
equality is preserved by every literal first-PP restriction and reinsertion.
In the balanced operation quotient, the only relevant functional is

\[
             \Psi=\delta\cdot(B-\operatorname {Eq}),
 \qquad \delta=(1,1,-1,-1).                           \tag{1}
\]

Consequently every four-site response construction has (Psi=0), even if
its target, physical (q), anchor, (W), residue, and ridge faces are
perfectly repaired.  The desired balanced private face has

\[
                    (B,\operatorname {Eq})=(\delta,0) \tag{2}
\]

and is detected by (1).

The negative statement is complemented by a positive local terminal
theorem.  Keep all three matching occurrences, all four literal operation
corners, all 18 direction-factor flags, all 24 tail PP flags, and every
named augmentation row.  Grant a projection-complete local supermap,
including every individual reinsertion and the entire external augmentation
space.  Its rank is

\[
                         126\quad\hbox{in dimension }127.             \tag{3}
\]

Its unique left kernel is the literal restriction/reinsertion extension of
(1).  On raw matching occurrences its normalized value is

\[
 \boxed{
 \Psi_{\rm loc}={1\over12}
   \sum_{c,m}\delta_c
       \bigl(B_{c,m}^{*}-\operatorname {Eq}_{c,m}^{*}\bigr).}         \tag{4}
\]

Thus the four-site response/target branch has a genuinely exhaustive
**local** terminal.  It is not yet the global Gate-II terminal: one new h=3
same-word/fine/repeated cross-profile column could break (1).  Formula (1)
gives the necessary and sufficient first projection of such a column.

Exact checker:
[`verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py`](../computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py).

## 1. Literal operation and matching coordinates

The four balanced corners are ordered as

```text
0  DQ[a|b]
1  DQ[b|a]
2  PS[P0,S1]
3  PS[P1,S0].
```

The two direct corners form the positive shore of (delta), and the two
endpoint-pair corners form its negative shore.  On the fixed residual
window (2345), the three matching occurrences are

\[
              23\mid45,qquad24\mid35,qquad25\mid34.                 \tag{5}
\]

For every corner (c) and matching (m), retain two distinct coordinates

\[
                   B_{c,m},\qquad \operatorname {Eq}_{c,m}.          \tag{6}
\]

The raw balanced private output is

\[
             U_B=\sum_{c,m}\delta_c B_{c,m}.                         \tag{7}
\]

The integral version of (4), without the factor (1/12), evaluates to

\[
 \Psi(U_B)
   =\sum_{c,m}\delta_c^2
   =3(1+1+1+1)=12.                                     \tag{8}
\]

After first averaging each three-matching fibre, (1) is the primitive
eight-coordinate detector from `f753b5d`; it reads four on the balanced
corner vector.  The factors (12) and (4) are the raw-occurrence and
corner-normalized versions of the same functional.

## 2. The complete top projection

The checker grants the following top rows.

1. In both (B) and Eq, both matching differences in every corner.  These
   16 rows grant the complete augmentation-zero matching plane separately
   in the two blocks.
2. Four physical h=2 response/cap rows.  In the (B+operatorname {Eq})
   projection their corner value is

   \[
          \left(\sum_mB_{c,m},\sum_m\operatorname {Eq}_{c,m}\right), \tag{9}
   \]

   with equal coefficients.
3. The four signless balanced-square companions.  Each has private support
   on one direct and one PS corner and has zero Eq component.

The signless companions are annihilated by (1), since their two corner
values have opposite (delta)-sign.  The response rows are annihilated
because of the diagonal equality in (9).  Matching differences are
annihilated because (4) is constant on the three matching occurrences.

These 24 displayed top columns have rank 23 in the 24-dimensional raw
(B+operatorname {Eq}) occurrence space.  Their unique primitive left
kernel is the integral numerator of (4).  The exact controls are

\[
\begin{array}{c|c|c}
\text{added packet}&\Psi\text{ value}&\text{top rank}\\ \hline
(B,\operatorname {Eq})=(\delta,0)&12&24\\
(B,\operatorname {Eq})=(0,\delta)&-12&24\\
(B,\operatorname {Eq})=(\delta,\delta)&0&23.
\end{array}                                             \tag{10}
\]

The last row is the load-bearing counterguard.  A fully decorated physical
column with tied private and Eq packets does not fill the balanced class.

## 3. What the normalized h=2 response actually supplies

There are (3^4=81) four-site words: three pure target words and 78 mixed
target-zero words.  The parent head is

```text
11:110000,
```

so the residual (2345) word is pure (0000).  Its physical normalized
h=2 equation is

\[
 H_{0000}-1=0,
 \qquad
 H_{0000}=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.       \tag{11}
\]

The constant (-1) in (11) belongs to the target block.  It has zero
projection on (B-operatorname {Eq}).  More importantly, lifting the
three matching incidences into the physical cap/reduced-Eq interface gives
the same vector in both blocks:

\[
                         (B,\operatorname {Eq})=(H,H). \tag{12}
\]

For the balanced DQ/PS combination, (12) becomes

\[
                         (B,\operatorname {Eq})=(\delta H,\delta H), \tag{13}
\]

which is the tied negative control in (10).

The conclusion is unchanged on a mixed word.  Its normalized target is
zero, but its response incidence is still tied as in (12).  Moreover, an
h=2 Hasse[0] row cannot simply be renamed as an
`Hasse[2](D,Q01)` or transported PS generator: the direction-pair component
of the repeated source grade is a direct-sum label.  Even granting the
strongest tagged form (13) does not fill because of (1).

Thus the normalized target is not the obstruction by itself.  The sharper
obstruction is the equality of private and reduced-Eq projections.

## 4. All first PP and reinsertion faces

The literal direction-factor order is

```text
(dD)q01, D(dq01), (dp0)s1, p0(ds1), (dp1)s0, p1(ds0).
```

The first two retain the two ordered direct-DQ corners; the next two retain
`PS[P0,S1]`; the last two retain `PS[P1,S0]`.  With the three residual
matchings this gives 18 flags.  The primitive direction profile is

\[
                         (2,2,-1,-1,-1,-1).            \tag{14}
\]

Deleting either of the two residual edges in each matching and corner gives

\[
                     4\cdot3\cdot2=24                 \tag{15}
\]

tail PP flags.

The checker retains separate (B) and Eq coordinates for all 42 flags and
grants every individual reinsertion comparison back to its literal top
corner and matching.  Formula (4) extends by assigning the same
(delta_c/12) and (-delta_c/12) values to a flag and its reinserted top
occurrence.  It therefore kills every reinsertion column separately.

On a private-only direction packet, the integral dual has value

\[
 3\bigl(2+2+(-1)(-1)+(-1)(-1)+(-1)(-1)+(-1)(-1)\bigr)
 =24.                                                   \tag{16}
\]

It also has value 24 on the private-only tail packet.  When the physical
response product rule supplies the identical Eq packet, both values become
zero:

\[
 \Psi(dB-d\operatorname {Eq})=0.                       \tag{17}
\]

Hence PP and reinsertion do not introduce a hidden route around (1).  They
propagate the same tied law to every lower face.

## 5. Target, `q`, anchor, `W`, residue, and ridge

The local checker grants the entire 19-dimensional external augmentation
space:

```text
target[4], W[4], ordinary residue[4],
M, ainc, physical q, P_f, ridge, eta, sigma.
```

This is stronger than checking only the named columns.  It also checks the
literal combinations

\[
\begin{aligned}
 T_j&=-W_j+\operatorname {target}_j,\\
 \rho_j&=W_j+\operatorname {ores}_j,\\
 K&=\sum_j\alpha_j\operatorname {ores}_j
       +\operatorname {ridge}+\eta-\sigma,\\
 q&=M-\operatorname {ainc},
 \qquad \alpha=(-1,1,1,-1).
\end{aligned}                                           \tag{18}
\]

The local terminal (4) is zero on all these rows.  Thus no choice of target,
Eq-external normalization, physical (q), anchor, (W), ordinary residue,
ridge, eta, or sigma can alter its value.  Only the reduced-Eq occurrence
block in (6) matters, and it enters with the opposite coefficient from the
private block.

This sharpens the older cap-extension calculation.  There is no need here
to solve for compensating target, (W), residue, or ridge coefficients:
the private-minus-Eq detector makes every such row invisible.

## 6. Why the local terminal is exhaustive

The complete local output has

```text
24  top B/Eq matching occurrences
36  direction-factor B/Eq flags
48  tail-PP B/Eq flags
19  external augmentation coordinates
---
127 total coordinates.
```

The supermap grants

- the projection-complete 24 top columns of Section 2;
- all 84 individual direction/tail reinsertion comparisons; and
- a basis of all 19 external augmentation rows.

Its rank is 126.  The numerator of (4) kills every column, so it spans the
entire cokernel.  Adding either the private-only or Eq-only balanced packet
raises the rank to 127; adding any tied balanced packet does not.

This is an exhaustion theorem, not an absence-from-inventory argument.  The
supermap is stronger than the literal local source map:

- matching differences are granted separately in (B) and Eq;
- every lower flag is granted its own reinsertion comparison; and
- every outside augmentation row is freely granted.

Any physical four-site response/target/PP map generated by the listed
operations factors through this supermap and is therefore annihilated by
(4).

## 7. Exact local/global boundary

The four-site conclusion is now a true dichotomy:

```text
h=2 response/target/PP closure
    -> always delta.(B-Eq)=0
    -> cannot construct absolute U_C4
    -> Psi_loc is the unique exhaustive local terminal.
```

This does not finish the global Gate-II branch.  A new h=3 column may leave
the local operation fan.  Its first exact test is

\[
             \boxed{\delta\cdot(B-\operatorname {Eq})\ne0.}         \tag{19}
\]

An oriented DQ-to-PS shore difference can satisfy (19); it is not a
tag-preserving action bar or a four-site h=2 response row.  A physical
positive construction must provide precisely such a source-labelled
relative-C4 restriction/insertion column, then repair that same column's
word-`0102`, physical (q), anchor, (W), and labelled-ridge faces.

Conversely, if the exhaustive global same-word/fine/repeated map is proved
to preserve (19) with equality zero, (4) extends from the genuine local
terminal to the accepted global augmented terminal without any additional
target/residue/ridge correction.

## Reproduction

Run

```text
python3 computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py
python3 -O computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py
python3 -OO computations/verify_h3_uc4_four_site_response_private_eq_local_terminal_gate.py
```

The checker freezes all coordinate counts, ranks, PP values, target-word
census, augmented zero signature, and the ledger digest.

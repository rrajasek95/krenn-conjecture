# The punctured C4 forces an alternate pure target matching

## Result

The sixteen zero-support rectangles left by `2061c57` do not survive the
complete unary/four-response packet.  In the normalized final target-coloop
chart, either a mixed coefficient already exposes the off-anchor matching
`04|15`, or the pure-one coefficient forces

```text
P2:11 | S3:11 | 04:11 | 15:11
```

as an alternate pure-one target matching.  Reselecting it makes the old
`L`-only cells `05:02,14:02` nonanchor, so the pinned nonanchor theorem gives
the active four-good exit.

The proof is one integral Hamming-face identity, not a support census and
not an invocation of strict endpoint Hall.

Checker:
`computations/verify_h3_c4_punctured_cube_alternate_target_lift.py`.

## 1. Literal cofactor block

Fix the selected endpoint holes `P2,S3` and write four-site words in the
order `0,1,4,5`.  The three q-matchings of the complete cofactor are

\[
 A(w)=q_{01}^{w_0w_1}q_{45}^{w_4w_5},\quad
 B(w)=q_{05}^{w_0w_5}q_{14}^{w_1w_4},\quad
 G(w)=q_{04}^{w_0w_4}q_{15}^{w_1w_5}.                 \tag{1}
\]

The selected diagonal return and pure-one target tail give four units

```text
q05:02, q14:02, q05:11, q14:11.
```

The rank-one response syzygy already proved in the zero-face reduction is,
for every q word,

\[
 a_2E_{11}(w)-a_1E_{21}(w)=U\,(A(w)+B(w)+G(w)),       \tag{2}
\]

where `U=a2*p1*s1` is a selected endpoint unit.  Away from the pure-one
word the two complete rows on the left have zero target.  At the pure-one
word `t=(1,1,1,1)`, their source-row combination is instead

\[
 F_t=U(A_t+B_t+G_t)-a_2.                              \tag{3}
\]

Thus (2)--(3) are literal polynomial combinations of the four response
rows; no cofactor has been declared independently.

## 2. The selected bridges make the cubical pivot a unit

Use

```text
u=(1,0,2,1),       B_u=q05:11*q14:02,
v=(0,1,1,2),       B_v=q05:02*q14:11.
```

Both products are selected units.  On either mixed word, a nonzero `G`
term contains an off-diagonal cell on the physical edge `04` or `15`; those
edges are outside the selected anchor union and the branch is already
routed.  Otherwise the complete zero rows give `A_u=-B_u` and
`A_v=-B_v`, so both `A_u,A_v` are units.  Explicitly,

```text
A_u=q01:10*q45:21,      A_v=q01:01*q45:12.
```

Hence their crosswise recombination

```text
A_z=q01:01*q45:21,      z=(0,1,2,1),
```

is a unit as well.  This is the only localization introduced by the proof,
and it is forced from the already selected cells by complete source rows.

## 3. Integral punctured-face certificate

Let

```text
t=(1,1,1,1),  x=(0,1,1,1),
y=(1,1,2,1),  z=(0,1,2,1).
```

For `C=A+B`, the two matching products have zero determinant on the
opposite-site `0|4` face.  Direct expansion gives the integral identity

\[
 A_zC_t-A_yC_x+B_xC_y-B_tC_z=0.                      \tag{4}
\]

If a mixed `G_x,G_y,G_z` is nonzero, it again contains an off-anchor
off-diagonal cell and routes.  Otherwise substitute the literal source-row
combinations (2)--(3) into (4).  The target-augmented certificate is

\[
 A_zF_t-A_yF_x+B_xF_y-B_tF_z
       =A_z\bigl(UG_t-a_2\bigr).                      \tag{5}
\]

All left-hand terms are complete response rows.  Since `A_z,U,a2` are
units on the surviving branch, (5) forces

\[
                 G_t=q_{04}^{11}q_{15}^{11}\ne0.      \tag{6}
\]

Equation (6) is not merely support information: together with the selected
endpoint factors it is a literal alternate monomial in the pure-one target
coefficient.

## 4. Physical landing

Reselect the pure-one target witness from

```text
L = P2 | S3 | 05 | 14
```

to

```text
L' = P2 | S3 | 04 | 15.
```

The old edges `05,14` were `L`-only relative to the selected pure-anchor
web.  They are absent from `L'`, so their already nonzero decorations
`05:02,14:02` are now offanchor.  The pinned nonanchor theorem supplies the
active distinct-head good-pair route.  If any `G` term entered earlier, its
off-anchor off-diagonal factor supplied the same route directly.

Consequently the residual sixteen q-edge `C4=K2,2` supports do not need an
endpoint-hole Hall lift or a new complete-column kernel.  The complete
target and crossed rows turn them into alternate-target reselection.

## Scope

This is an exact `h=3` theorem for the normalized target-coloop packet and
its source-labelled site/colour symmetries.  It uses the selected `L`-only
tail, `P2:21=0` zero-face response block, and the already routed status of
off-anchor `04|15` terms.  It is not a generic primitive-saturation theorem
for arbitrary flat C4 complexes.

Run

```text
python3 computations/verify_h3_c4_punctured_cube_alternate_target_lift.py
python3 -O computations/verify_h3_c4_punctured_cube_alternate_target_lift.py
python3 -I -S computations/verify_h3_c4_punctured_cube_alternate_target_lift.py
```

Frozen ledger SHA-256:

```text
449eda8e2da09561ac33fd819b525fb6cbf6bf27002ac5c2d727e44ab7cf6013
```

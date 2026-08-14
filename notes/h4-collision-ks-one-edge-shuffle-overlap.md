# The `h=4` collision/KS source prolongation has a canonical overlap triangle

## Result

The first one-edge prolongation does not create a new obstruction in the
coefficient/Koszul--principal-parts source resolution.  For every intrinsic
six-site tail matching and each of the four collision families, its three
presentations as

```text
(two-edge h3 window) * (one omitted edge)
```

map, with the exterior shuffle sign, to one `h=4` carrier.  The three
presentation boundaries agree exactly.  Each consists of the two tail
restrictions already present in its `h=3` window and the one new spectator
Leibniz face.  Thus the new face is not discarded: cycling through the
three windows gives all three intrinsic restrictions.

The presentation overlap is the augmented oriented triangle.  It is exact
integrally and has a canonical `S3`-equivariant contraction over the theorem
field `Q`.  Consequently there is no stable source-Hasse covector at this
first overlap.  What remains conditional is physical descent: every
word/fine/repeated and protected output row must take equal values on the
three window presentations.

Exact checker:
[`verify_h4_collision_ks_one_edge_shuffle_overlap.py`](../computations/verify_h4_collision_ks_one_edge_shuffle_overlap.py).

## 1. The one-edge structure map and its signs

Fix a globally oriented tail

\[
                         T=e_0e_1e_2
\]

and a collision/KS carrier `x_f` of parity `p`, where `f` is one of

```text
forward_01=-D*s1,  reverse_01=+p0*q01,
forward_02=-D*s0,  reverse_02=+p1*q01.
```

For `i=0,1,2`, put `W_i=T\setminus e_i`.  The raw tensor presentation
orders `W_i` before `e_i`.  Its shuffle sign is

\[
                \epsilon_i=(-1)^{2-i},
\]

so the intrinsic structure map is

\[
 \mu_i\bigl((x_fW_i)\mathbin\otimes e_i\bigr)
      =\epsilon_i(x_fW_i)e_i=x_fT.                    \tag{1}
\]

The complete product differential, not static multiplication, is

\[
 d\bigl((x_fW_i)\otimes e_i\bigr)
 =d(x_fW_i)\otimes e_i+(-1)^{p+2}x_fW_i\otimes de_i. \tag{2}
\]

After applying (1), the last term of (2) is the new face and has coefficient

\[
                         (-1)^{p+i}x_fW_i.             \tag{3}
\]

The two terms from `dW_i`, after their own shuffle signs, are the other two
members of the same alternating boundary.  Hence for every `i`,

\[
 d\,\mu_i(x_fW_i\otimes e_i)
 = (d_{\rm loc}x_f)T
   +\sum_{j=0}^2(-1)^{p+j}x_f(T\setminus e_j).         \tag{4}
\]

Equation (4) is independent of the chosen window.  The checker verifies it
for all four families and both carrier parities.  In particular the signs of
the new faces are `(+,-,+)` for even carriers and `(-,+,-)` for odd ones.

This is the required one-edge source structure map.  It applies to both
sides of a collision-to-Kodaira--Spencer comparison because it only uses
the dg-module Leibniz law.  If the `h=3` comparison is relabeling-covariant,
applying (1) to that comparison makes its `h=4` differential commute by
(4).

## 2. The twelve-face census

There are two related counts which should not be conflated.

First fix the old four tail sites and one new edge.  The old sites have
three matchings.  For four collision families, the literal one-edge packet
therefore has

\[
                         4\cdot3=12                    \tag{5}
\]

new `(de_i)*x_f` faces.  These are exactly the twelve faces isolated in the
preceding spectator-naturality audit.

Second consider the intrinsic full six-site source.  It has fifteen tail
matchings and hence sixty four-family collision cells.  Every such cell has
three window presentations, so the full redundant cover has 180 tops and
180 presentation-labelled new faces.  The fixed packet (5) is an exact
subset of this intrinsic census; it is not being declared an exhaustive
fixed-partition suspension.

Fibrewise over one intrinsic tail, the four families times its three window
presentations again give twelve new faces.  In each family these are the
three distinct restrictions in (4).  This is the local block used by the
overlap calculation below.

## 3. The three-window overlap is the augmented triangle

For one family let `q_i` denote the three shuffle-normalized presentations.
With oriented overlap edges `u_01,u_02,u_12` and triangle `tau`, take

\[
\begin{aligned}
 d u_{01}&=q_1-q_0, & d u_{02}&=q_2-q_0,
 &d u_{12}&=q_2-q_1,\\
 d\tau&=u_{01}-u_{02}+u_{12},
 &\varepsilon(q_i)&=1.                               \tag{6}
\end{aligned}
\]

This augmented complex has dimensions and ranks

```text
C2 -> C1 -> C0 -> intrinsic cell
 1      3      3          1

ranks: 1, 2, 1.
```

It is therefore exact.  Four collision families give dimensions
`4 -> 12 -> 12 -> 4` and ranks `4,8,4`, still with zero homology.

There is a choice-free rational contraction.  If `B` is the oriented
vertex-edge incidence matrix and `z=(1,-1,1)` is the triangle boundary,
then

\[
 s(1)={q_0+q_1+q_2\over3},\qquad
 h_0={1\over3}B^{\mathsf T},\qquad
 h_1(a)={z\cdot a\over3}\tau.                        \tag{7}
\]

The identities

\[
 Bh_0+s\varepsilon=1,
 \qquad h_0B+(d\tau)h_1=1,
 \qquad h_1(d\tau)=1                                  \tag{8}
\]

hold exactly.  The checker verifies equivariance of (6)--(8) under all six
permutations of the tail edges.  Thus (7) is the canonical shuffle/overlap
homotopy over `Q`.

The integral augmented triangle is still exact, and a based integral
contraction exists after choosing one window.  There is no integral
`S3`-equivariant contraction: an invariant section must be
`a(q0+q1+q2)`, whose augmentation is `3a`.  The denominator three is
therefore structural, not a sign error.

## 4. Exact physical-descent counterguard

The positive result is source-level.  For any additional physical row `r`,
write its values on the three presentations as

\[
                           a=(a_0,a_1,a_2).
\]

That row descends through (6) if and only if

\[
                         a_0=a_1=a_2.                 \tag{9}
\]

Equivalently its canonical mismatch is

\[
                   a-{a_0+a_1+a_2\over3}(1,1,1),      \tag{10}
\]

and the two primitive tests `(1,-1,0)` and `(1,0,-1)` detect every failure.
For the intrinsic Hasse boundary (4), (10) is zero, so there is no source
covector.  Equations (9)--(10) are the exact next test for the physical
word, fine, repeated, target, `q`, anchor, ordinary residue, `W`, and ridge
rows.  The present audit does not assign those values and hence does not
silently assume their stability.

## Scope

This is an intrinsic `h=4` source-resolution theorem.  It uses actual
six-site matchings and their restrictions; it never tensors an eight-site
GHZ target with an independently coloured spectator pair.  Therefore it is
independent of the spectator-suspension no-go.

It conditionally prolongs a relabeling-covariant physical `h=3`
collision/KS comparison, but it does not construct the still-missing `h=3`
comparison, prove its cross-word/fine placement, or prove that any protected
physical readout satisfies (9).  The exact remaining uniform obligation is
now only that augmented naturality check; the one-edge Leibniz and overlap
sign problem itself is closed.

Run normally, optimized, and isolated/no-site.  The checker freezes all
dependency hashes, both carrier parities, the fixed and global censuses, the
triangle ranks and contraction, all six permutation actions, and its ledger
digest.

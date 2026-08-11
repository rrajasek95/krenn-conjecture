# E3 always forces a unary/direct third base on the physical one-bad packet

> **Physical supersession of `fe43040`.**  The original version of this
> note left an E3-flat rational five-vector as a possible multiplicative
> boundary.  That vector omitted the mandatory zero of every response base
> on the literal unary word `0^8`.  The flat packet is not physically
> realizable in the normalized one-bad source.  The corrected theorem below
> closes all seven single-`C6/C8` records at E3.  The old abstract example is
> retained only to guard against repeating the unlabelled-vector mistake.

## Result

Continue with one of the seven single-`C6/C8` residuals from `d67b32b`.
Let `M,N` be the coloop and outside full matching bases, let

\[
 a_c=\mu_M(c),\qquad b_c=\mu_N(c),
\]

on the five exact source words, and let `h` be their target-value vector.
The nonzero E2 minor makes `a,b` independent.  The matching-exchange E3
coefficients are exactly

\[
 C^{MN}_{cde}=
 \det\begin{pmatrix}
 a_c&a_d&a_e\\ b_c&b_d&b_e\\ h_c&h_d&h_e
 \end{pmatrix}.                                         \tag{1}
\]

At the level of arbitrary evaluation vectors, precisely one of the following
occurs.

1. Some determinant (1) is nonzero.  In the literal perfect-matching
   expansion, the contributions of `M` and `N` cancel separately, so a
   third physical matching base `K!=M,N` has nonzero coefficient.
2. Every determinant vanishes.  Since `a,b` are independent,

   \[
                           h\in\langle a,b\rangle.       \tag{2}
   \]

   This is the apparent two-base five-word holonomy left after E2.

The second alternative disappears after the five words are given their
literal source labels.

## The five literal eight-site words

Write the augmented sites in the order

```text
0,1,2,3,4,5,P,S.
```

Choose the selected diagonal colour `t=2`, the other bright colour `1`, and
let `rho` be the six-letter residual word of the nonzero outside coefficient.
The five rows represented by `h=(1,0,0,1,1)` are

```text
t^8                  target 1
rho_0...rho_5,1,2    target 0   (selected mixed word d)
rho_0...rho_5,2,1    target 0   (opposite crossed word e)
0^8                  target 1   (unary/direct row)
1^8                  target 1   (other diagonal row).
```

For the literal displayed representative `rho=012012`, these are

```text
22222222, 01201212, 01201221, 00000000, 11111111.
```

Only the three columns `(t^8,d,0^8)` are needed for the corrected argument,
so no normalization of `rho` is being asserted.

## The mandatory physical zero

Both `M` and `N` are response bases.  They avoid the direct edge `P-S`, and
the normalized one-bad packet has no endpoint-colour-zero star cells:

```text
p_0=s_0=0;   the only endpoint-colour-zero cell is P-S:00.
```

Consequently

\[
                 \mu_M(0^8)=\mu_N(0^8)=0.              \tag{3}
\]

The checker verifies (3) edge by edge for all seven physical single-cycle
records: one `C6` and six `C8`s.  Now coloopness gives `b_t=0`, while the
selected outside coefficient gives `a_t b_d!=0`.  Hence

\[
\det\begin{pmatrix}
a_t&a_d&0\\
0&b_d&0\\
1&0&1
\end{pmatrix}
=a_t b_d\ne0.                                           \tag{4}
\]

Thus E3 cannot be flat.  Expanding the last row of (4) as the sum over
literal matching bases, the `M` and `N` terms cancel and some third base `K`
has `mu_K(0^8)!=0`.  An eight-site matching has nonzero `0^8` evaluation in
this normalized packet exactly when it contains `P-S:00`.  Therefore `K` is
a unary/direct-anchor base.

Checker:
`computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py`.

## What a third base buys

The edge union of two perfect matchings whose symmetric difference is one
even cycle supports exactly those two perfect matchings.  This remains true
for both physical topologies here:

```text
C6 plus one common edge: exactly M,N
C8:                       exactly M,N.
```

Hence every E3-selected `K` uses at least one physical edge outside
`M union N`.  If that edge lies outside the union of the three chosen pure
target matchings, the nonanchor theorem gives the good active route.  If it
does not, its source label is carried by the third selected target anchor;
the packet has entered the anchor-contained strict-Hall/base-exchange web,
rather than remaining a two-base affine coloop.

This conclusion is source-valid: E3 is the determinant of actual matching
monomials and coefficient rows, and its `M,N` terms cancel before any common
factor is divided out.

## Why the old flat vector was misleading

Use the exact five-row target vector

\[
                         h=(1,0,0,1,1).
\]

The checker still freezes

\[
 a=(1,1,2,3,4),\qquad b=(0,-1,-2,-2,-3),qquad h=a+b. \tag{3}

The target entry of `b` is zero, an outside entry is nonzero, and the E2
minor on the first two words is `-1`.  Nevertheless every E3 determinant
vanishes.  Thus E2 activity plus all five exact target values does not force
a third base without using multiplicative common-`q` realizability.

This remains an exact identity among five *unlabelled* vectors, but it has
nonzero fourth coordinates for `a` and `b`.  Under the literal ordering
above that coordinate is `0^8`, contradicting (3).  It is therefore not a
multiplicative common-`q` boundary and requires no toric-binomial or
realizability analysis.

## E4 remains only coherence

E4 is the row-Laplace identity among the four E3 minors.  The checker audits
all four-state subsets and both matching rows.  On (2), every E3 minor is
already zero, so both E4 tetrahedral boundaries vanish identically.  E4
provides coherence for a nonzero third-base carrier; it supplies no new
equation on the flat two-base plane.

## Scope

This closes the E3-flat multiplicative-realizability question on all seven
single-cycle records and selects a third unary/direct base.  It does not by
itself route that third base to a clean cap, source unit, or a particular
downstream anchor exchange.  The rational vectors above are now explicitly
retracted as a physical possibility.

Run

```text
python3 computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py
python3 -O computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py
python3 -I -S computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py
```

Frozen ledger SHA-256:

```text
4c8c63563892c8adb454098ea3508552e5afcb3c13d49e15058bdca38271eaaa
```

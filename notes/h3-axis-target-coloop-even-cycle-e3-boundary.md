# E3 forces a third physical base or leaves a two-base word plane

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

Therefore precisely one of the following occurs.

1. Some determinant (1) is nonzero.  In the literal perfect-matching
   expansion, the contributions of `M` and `N` cancel separately, so a
   third physical matching base `K!=M,N` has nonzero coefficient.
2. Every determinant vanishes.  Since `a,b` are independent,

   \[
                           h\in\langle a,b\rangle.       \tag{2}
   \]

   This is the exact two-base five-word holonomy left after E2.

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

## The E3-flat boundary is real at the row level

Use the exact five-row target vector

\[
                         h=(1,0,0,1,1).
\]

The checker freezes

\[
 a=(1,1,2,3,4),\qquad b=(0,-1,-2,-2,-3),qquad h=a+b. \tag{3}

The target entry of `b` is zero, an outside entry is nonzero, and the E2
minor on the first two words is `-1`.  Nevertheless every E3 determinant
vanishes.  Thus E2 activity plus all five exact target values does not force
a third base without using multiplicative common-`q` realizability.

This is an exact rational evaluation boundary, not a declared physical
source.  The next theorem must prove that two literal matching monomials on
a single `C6/C8` cannot realize (2) inside the same common quadratic and
endpoint-star packet, or route such a realization directly to an affine
target-line modification.

## Why E4 does not help on its own

E4 is the row-Laplace identity among the four E3 minors.  The checker audits
all four-state subsets and both matching rows.  On (2), every E3 minor is
already zero, so both E4 tetrahedral boundaries vanish identically.  E4
provides coherence for a nonzero third-base carrier; it supplies no new
equation on the flat two-base plane.

## Scope

This advances every E3-curved single-cycle packet to a third physical edge
and isolates the remaining multiplicative obstruction.  It does not claim
that the rational vectors (3) arise from a full one-bad source, nor that an
anchor-contained third base is already clean.  No abstract higher face can
replace the missing common-`q` factorization test on (2).

Run

```text
python3 computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py
python3 -O computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py
python3 -I -S computations/verify_h3_axis_target_coloop_even_cycle_e3_boundary.py
```

Frozen ledger SHA-256:

```text
e96a469ff1e52b4bbe9fd60ec934552d131541c0e16dd2f279438e782a6b37de
```

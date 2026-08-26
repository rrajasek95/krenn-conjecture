# Singular slices of the hafnian identity are site-down redundant

Status: **UNAUDITED exact negative theorem and literal two-jet counterguard**.

## Identity and two-site normal Hessian

Put

```text
B_A(x)_ij = x_i^T A_ij x_j,
P_A(x) = Haf(B_A(x)),
G(x) = sum_c product_i x_(i,c).
```

The normalized `X5` equation is the polynomial identity `P_A=G` in the 24
site-colour variables.  On the coordinate subspace `x_6=x_7=0`, both sides
have multiplicity two.  Exact partition of the 105 physical perfect
matchings gives the leading normal form

```text
sum_ab y_(6,a)y_(7,b)
  [ A_67[a,b] q_R^[3] + l_(6,a) l_(7,b) q_R^[2] ].
```

There are 15 matchings of direct-pair-plus-three-residual type and 90 of
double-crossing-plus-two-residual type.  The target leading form is

```text
sum_c (product_(i in R) x_(i,c)) y_(6,c)y_(7,c).
```

Thus the mixed normal-Hessian block is exactly the frozen full-nine carrier
identity.  At a generic target point its `3x3` mixed block is invertible and
the full `6x6` normal Hessian has rank six, but that rank belongs to the sum
of the direct and response terms—not to `A_67`.

## Exact no-channel counterguard

Take residual point `x_i=(1,1,1)` for `i=0,...,5` and residual scalar
matching `01|23|45`.  Its six-site hafnian and the three relevant four-site
cofactors equal one.  For an arbitrary direct matrix `C=A_67`, put three
crossing response pairs on `(0,1),(2,3),(4,5)` whose outer products are the
three rows of `I-C`.  Literal matching evaluation gives

```text
normal mixed block = C + (I-C) = I.
```

The checker replays both `C=0` and the nonsymmetric rank-three matrix

```text
1 2 3
0 1 4
5 6 0.
```

Both have the same target normal Hessian `[[0,I],[I,0]]` of rank six.
Hence even the complete order-two normal jet at a residual point forces
neither the rank of the direct edge nor a common colour channel.  A hostile
row/column endpoint mutation fails, guarding the crossed orientation.

## Three-site slice

On `x_5=x_6=x_7=0`, both sides have multiplicity three and their ordinary
Hessians vanish.  The first nonzero normal form is

```text
(A_56 l_7 + A_57 l_6 + A_67 l_5) q_W^[2]
  + l_5 l_6 l_7 q_W.
```

The exact matching partition is `45` one-internal/one-crossing/two-residual
terms plus `60` three-crossing/one-residual terms.  This is precisely the
frozen three-site contraction, not a new Hessian constraint.

## Why the global singular scheme adds no rows

Retaining every normal colour and residual word gives

```text
two sites:   3^2 * 3^6 = 3^8 = 6561,
three sites: 3^3 * 3^5 = 3^8 = 6561.
```

Concatenating the exposed and residual colour words is a bijection with the
original eight-site words.  Consequently the full polynomial normal slice
is merely a permutation of the original normalized coefficient system.  A
pointwise slice is too weak, as the counterguard shows; imposing the slice
as a polynomial identity recovers all of `X5` and assumes the unresolved
system.

The first potentially new datum must therefore couple different residual
points/slices nonlinearly—equivalently the archived response-dependent
normal reinsertion or overlap identity.  Taking another singular derivative
does not create a new source constraint.

## Replay

```bash
python3 computations/unaudited-codex-hafnian-singular-slice-2026-08-23/audit_hafnian_singular_slice.py --check-results
python3 -O computations/unaudited-codex-hafnian-singular-slice-2026-08-23/audit_hafnian_singular_slice.py --check-results
python3 -I -S computations/unaudited-codex-hafnian-singular-slice-2026-08-23/audit_hafnian_singular_slice.py --check-results
```

The hostile command must fail:

```bash
python3 computations/unaudited-codex-hafnian-singular-slice-2026-08-23/audit_hafnian_singular_slice.py --mutate-crossed-orientation
```

Frozen logical digest:
`8f0eeea7993a153819ae5891cbac841fd7e1a1ad03769e74f95af8e84c9586b6`.

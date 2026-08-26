# Equivariant differential rank and Hessian carrier audit

## Outcome

Status: **UNAUDITED exact structural PASS / direct rank route retired**.
At an exact GHZ source the 21-dimensional normalization torus gives the
complex

```text
Lie(T0) --G_A--> E^252 --J_A=dF_A--> W^6561.
```

If `s=dim ker(G_A)` is the source stabilizer, equivariance proves

```text
rank(J_A) <= 231+s,       rank(J_A)-s <= 231.
```

Thus the sharp contradiction target would be
`X5+no-cap => rank(J_A)-s>=232`.  The existing carrier response matrices do
not provide such first-Jacobian blocks.  They occur one derivative later,
as Hessian blocks after a direct rank-one subtraction.  Even there, a
carrier blocker is not a conormal/radical element, so the surviving exact
target is a source-faithful conormal lift before applying the second
fundamental form.

## 1. Exact torus complex

For the basis cocharacter `e_(i,c)-e_(7,c)`, the source tangent column is

```text
G_(uv,ab) = A_uv[ab]
  *(delta_(u,a),(i,c)+delta_(v,b),(i,c)
    -delta_(u,a),(7,c)-delta_(v,b),(7,c)).
```

Semi-invariance gives the literal identity

```text
(J_A G_A)_(w,(i,c))
  = (1_(w_i=c)-1_(w_7=c))*F_w(A).
```

At `F(A)=GHZ`, the right side is zero.  Since `rank G_A=21-s`, rank-nullity
gives the bound above.  Infinitesimal rigidity modulo T0 only yields equality
`rank J=231+s`; it is consistent and is not itself a contradiction.

## 2. Exact controls

All ranks below are exact over Q; sparse rational elimination agrees at the
two primes `1000003` and `1000033`.

| control | live cells | `s` | rows | rank | rank minus `s` | pattern matching | defects |
|---|---:|---:|---|---:|---:|---:|---:|
| W40 | 20 | 9 | X3 | 235 | 226 | 236 | 0 |
| W40 | 20 | 9 | X4 | 240 | 231 | 244 | 0 |
| W40 | 20 | 9 | full F | 242 | 233 | 248 | 3 |
| W25 | 38 | 1 | X3 | 210 | 209 | 214 | 0 |
| W25 | 38 | 1 | X4 | 239 | 238 | 246 | 78 |
| W25 | 38 | 1 | full F | 245 | 244 | 252 | 103 |

W40 exactly saturates the equivariant X4 bound `231+s=240`.  W25 is
all-blocked but has `s=1`, disproving “no-cap forces a free T0 orbit” at the
lower rung.  Its 78 X4 defects add 29 Jacobian ranks and its 25 remaining
defects add six more; those ranks cannot be used at an exact target without
the missing X5 argument.

The pattern columns already show why Hall selection is insufficient.  W40
X4 has a nonzero-entry matching of size 244, above the forbidden target 241,
yet its exact rank is only 240.  Torus/source identities cancel every such
larger determinant.  A support-only selection of nonzero cofactors cannot
prove the required minor.

The frozen support6, support8, and branch-1 positive-dimensional charts are
one-colour diagonal components/support records, not 252-coordinate
three-colour X5 points.  Their fixed-left mate units forbid the needed
assembly, so a global `dF` rank there is undefined.  The existing 310 support
records only give support stabilizer dimensions `0,1,2,3` with orbit-record
counts `187,91,26,6`.

## 3. Carrier matrices are not first-Jacobian blocks

Fix a pair `p,q`, residual six-site word `z`, and let
`Phi_(pq,z)[i,j]=F_(i,j,z)`.  Literal matching partition gives

```text
Phi = H6(z)*s_pq
    + sum_(a<b in U) H4(z without a,b)*rho_ab^(z_a,z_b),

rho_ab^(alpha,beta)[i,j]
  = A_pa[i,alpha]A_qb[j,beta]
    + A_pb[i,beta]A_qa[j,alpha].
```

The 105 matchings split as 15 using `pq` and
`15*2*3=90` avoiding it.  The checker compares all 688,905 canonical-pair
source-labelled terms.

The true first-Jacobian pair slice is instead

```text
dF_(i,j,z) / dA_pq[k,l] = delta_((i,j),(k,l))*H6(z),
```

a degree-three `H6(z) I9` block.  Each `rho` row is degree two.  Stacking
forbidden residual edges gives `90x9` for a star and `108x9` for a triangle.
The quotient `C*/W_C` is inside the nine-dimensional cap dual, not a quotient
of the 6,561-dimensional codomain of `J`; its ranks do not add across
carriers as first-Jacobian ranks.

## 4. Exact Hessian identification

Let `M` be either matching on the four residual sites outside `{a,b}`.  For
the word with colours `(i,j,alpha,beta,z)`, differentiating by the two source
cells of `M` leaves the four-site Hafnian

```text
d^2_M F_w
  = A_pq[i,j] A_ab[alpha,beta] + rho_ab^(alpha,beta)[i,j].
```

The checker replays 19,683 canonical source-labelled Hessian terms.  Hence
the carrier rows are genuine Hessian coefficients after subtracting the
direct rank-one `A_pq tensor A_ab` term.

At an exact point put

```text
V=ker J_A,   O=im G_A,   N=coker J_A.
```

Equivariance gives

```text
d^2F_A(G_X A,v) + J_A(G_X v) = X.J_A(v).
```

Thus for `v in V`, the second fundamental form

```text
II_A : Sym^2(V/O) -> N,
       ([v],[w]) |-> [d^2F_A(v,w)]
```

is well defined.

## 5. Blocker is not conormal/radical membership

A scalar form dual to `II` needs a conormal
`lambda in ker(J_A^T)`.  Carrier `K` lives only on one nine-output slice.
Neither `L_C K=0` nor `ell in rowspan(L_C)` implies `lambda J_A=0`.

Two exact controls fire:

- W25 carrier `(01, star centre 2)` has `rank L=9`, so all four activity
  forms are blockers.  For `ell_0=K00`, contraction with the true Jacobian
  column `A_01[00]` is the pure cofactor `1/2`, not zero.
- W40 active carrier `(67, star centre 5)` has `K=I3`, `L K=0`, and activity
  `s=1`; the same conormal test sees pure cofactor `1`.

There is also a universal normal-direction guard: Euler homogeneity gives

```text
J_A(A)=4F(A)=4GHZ.
```

Therefore GHZ is zero in `coker J_A`; it cannot be a nonzero normal
obstruction.  A second-order obstruction must use a genuinely mixed
conormal.

## 6. One bounded conormal-overlap test

The 28 pair slices have 252 raw coefficients, but their global word functions

```text
lambda(w)=sum_(p<q) K_pq[w_p,w_q]
```

form exactly the degree-at-most-two ANOVA grade

```text
1 + 8*(3-1) + binom(8,2)*(3-1)^2 = 129.
```

The overlap gauge therefore has dimension 123.  The checker compresses
`J^T` directly to a `252x129` rational matrix; it never constructs a dense
`6561x252` matrix.  On both controls,

```text
rank_Q(J_W40^T on pair grade)=129,
rank_Q(J_W25^T on pair grade)=129.
```

Thus neither point has any nonzero conormal assembled from pair-flattening
covectors, even before imposing blocker compatibility.

There is also a coefficient-free strict-overlap lemma.  If one global
`lambda` is separately a function only of `(w_p,w_q)` for every physical
pair, compare two disjoint pairs: varying one while holding the other proves
that `lambda` is constant.  Hence the intersection of the 28 pair-local
subspaces is one-dimensional.  The diagonal blockers `K00,K11,K22` cannot
glue by literal equality.

A pairwise conormal at a hypothetical X5 point would therefore require a
new rank drop forced by the full equations.  Otherwise the first possible
lift lives in word degree at least three.  It is not a formal consequence of
the 728 carrier overlaps.

## 7. Properness/finite-fibre pivot guard

Kempf--Ness symplectic reduction by the compact torus is homeomorphic to the
affine T0 quotient.  The frozen normalized one-hot quotient theorem already
gives a decisive control: on every properly three-edge-coloured sparse chart,
the normalized source quotient is a single point represented by the all-unit
source `A*`.  The induced quotient map is therefore finite and proper on that
chart.  Nevertheless

```text
H(A*) != GHZ,
pi_target(H(A*)) = pi_target(GHZ),
```

because GHZ is the closed target-orbit limit of `H(A*)`.  Thus finite fibre
plus properness on the bare symplectic quotient cannot promote quotient
equality to exact membership.  Any viable refinement must retain a
non-invariant mixed-normal or carrier flag separating these two outputs.

## Terminal verdict and next exact target

The first-derivative `232+s` route is not supported by carrier ranks, and the
direct Hessian-radical interpretation fails.  The smallest surviving lemma
is:

> Find an X5-forced word-degree-at-least-three mixed conormal, with literal
> source labels, on each fixed rank/membership branch; then test the dual
> second fundamental form on non-torus tangent classes.

Without this conormal lift, the 728 blocked conditions do not force a normal
GHZ direction or a rank contradiction.  Bare symplectic-quotient
properness/finite-fibre criteria are independently insufficient.

## Replay

```sh
python3 computations/unaudited-codex-x5-equivariant-differential-rank-2026-08-21/audit_x5_equivariant_differential_rank.py --write-results
python3 -O computations/unaudited-codex-x5-equivariant-differential-rank-2026-08-21/audit_x5_equivariant_differential_rank.py
python3 -I -S computations/unaudited-codex-x5-equivariant-differential-rank-2026-08-21/audit_x5_equivariant_differential_rank.py
```

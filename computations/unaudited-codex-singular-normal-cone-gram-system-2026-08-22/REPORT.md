# Singular normal cone and Hermitian Gram incidence system

Status: **UNAUDITED exact formulation and bounded identity audit**.  This
report does not claim that the resulting system is inconsistent.

## Outcome

There is a source-faithful singular minimum-norm system which avoids both
known defects of the old Fritz--John presentation:

1. it uses the actual limiting normal cone of the reduced exact fibre, rather
   than a redundant `alpha=0` output multiplier; and
2. it encodes all 728 four-way blocker clauses by nine-variable Hermitian
   Gram witnesses, without rank-minor charts or a `4^728` branch expansion.

The bounded exact result is twofold.  First, the Gram formulation is exactly
equivalent to row-space membership on the realified complex source.  Second,
the site--colour Euler identities eliminate all three pure coordinates of a
naive singular output multiplier.  That elimination does **not** repair the
old singular branch: a mixed-only output cokernel of complex dimension at
least `6558-252=6306` remains at every source.  Hence the actual reduced
normal cone, not `J_A^*lambda=0`, is load-bearing.

## 1. Logical entry from the global proof spine

Let

```text
E = direct_sum_(p<q) C^(3x3),       dim_C E=252,
W = (C^3)^(tensor 8),               dim_C W=6561,
Phi:E->W                             (degree four),
X = {A:Phi(A)=Delta_8}.
```

If `X` is nonempty, its realification is closed in `R^504`, so the squared
Hermitian norm has a global minimum `A`.  Certified clean-cap descent and the
certified arbitrary-complex six-site theorem imply that every point of `X`
has no active clean cap.  In particular, the minimum satisfies all 728
star/triangle blocked-carrier clauses.

Every full star and every site triangle is an exact affine source block.
Thus the same minimum satisfies the regularity-free least-block equations for
all eight 63-column stars and all 56 27-column triangles.  No regular KKT
assumption is used here.

Finally Fermat's rule for a closed set gives

```text
-grad(1/2 ||.||^2)(A) in N_X(A),
```

where `N_X` is the real limiting normal cone.  This remains valid at a
singular minimum.  It is the correct replacement for the tautological
`alpha=0` branch.

## 2. Exact nine-variable encoding of one blocked carrier

For one of the 728 carriers let `L_C(A)` be its literal `90x9` star or
`108x9` triangle response matrix.  Its four blocker rows are

```text
ell_C,0 = K_00,
ell_C,1 = K_11,
ell_C,2 = K_22,
ell_C,3 = <K,A_pq>.
```

The exact response criterion says that this carrier fails to give an active
cap precisely when at least one `ell_C,i` belongs to `rowspan L_C(A)`.

For every complex matrix `L` and row `ell`,

```text
ell in rowspan(L)
  <=> ell^* in im(L^*)
  <=> there exists z in C^9 with L^*L z=ell^*.             (1)
```

The second equivalence is Hermitian and rank-free.  Indeed

```text
ker(L^*L)=ker(L)
```

because `z^*L^*Lz=||Lz||^2`; taking orthogonal complements gives
`im(L^*L)=im(L^*)`.  A bilinear transpose cannot replace the adjoint here:
over `C`, isotropic row spaces can make `L^T L` lose rank.

One scalar selects the blocker.  Put

```text
p(sigma)=sigma(sigma-1)(sigma-2)(sigma-3)
d_i(sigma)=product_(j!=i) (sigma-j)/(i-j).
```

Then the complete blocked clause is exactly

```text
p(sigma_C)=0,
L_C(A)^* L_C(A) z_C
   = sum_(i=0)^3 d_i(sigma_C) ell_C,i(A)^*.               (2)
```

Over characteristic zero, `p=0` selects one of `0,1,2,3` and the four
Lagrange polynomials specialize to the corresponding standard basis vector.
Thus (2) is equivalent, in both directions, to the four-way disjunction.  It
uses ten auxiliary complex scalars per carrier: nine entries of `z_C` and
one `sigma_C`.  Across all carriers this is 6,552 Gram variables and 728
selectors.  It replaces 75,600 row-combination variables, explicit rank
localizers, or an exponential branch list.

To write (2) polynomially over the real source, set `A=x+iy`; then the
adjoint is the transpose after `x-iy`.  All coefficients remain rational
after clearing the fixed Lagrange denominators.

## 3. Exact source-sized least-block equations

Let `E_0` be one of the 64 maximal intersecting edge families and let

```text
L_E0(A): C^d -> W,       d=63 for a full star, d=27 for a triangle.
```

The unconditional minimum-norm condition

```text
A_E0 in im L_E0(A)^*
```

has the same Hermitian Gram compression:

```text
A_E0=L_E0(A)^* L_E0(A) eta_E0.                            (3)
```

It needs `8*63+56*27=2016` source-block multiplier coordinates, rather than
64 output-sized multipliers.  Equation (3) is equivalent to exact affine
block normality even when the full fibre is singular.

The 21 target-torus balance equations may be added as inexpensive direct
consequences of minimum norm.  They do not replace (3) or the normal-cone
condition.

## 4. The correct singular normal-cone branch

Let `X_R` be the **reduced real** exact fibre in `R^504`, and choose a finite
Whitney stratification

```text
X_R = disjoint_union_nu S_nu.
```

For a source `A` in a stratum `S_nu`, minimum norm implies

```text
grad(1/2||.||^2)(A) perpendicular T_A S_nu.
```

Equivalently the source/normal pair lies in the closure of the conormal
bundle of that stratum.  Define

```text
CN(X_R)=union_nu closure(T^*_(S_nu) R^504).
```

The singular normal equation is simply

```text
(A,-A) in CN(X_R),                                        (4)
```

up to the harmless sign convention for the objective gradient.

This has a standard exact algebraic presentation on a stratum chart.  If a
reduced local ideal has generators `h`, generic codimension `c`, and a chosen
live `c`-minor of `Dh`, then the conormal closure is obtained from

```text
h(A)=0,
I_(c+1)(Dh(A))=0,
I_(c+1)( [ Dh(A) ; A^T ] )=0                              (5)
```

by saturating at the live `c`-minors and the stratum localizer, and then
taking closure.  One must range over the finitely many reduced
component/Fitting strata.  Using the radical/reduced local ideal is
load-bearing: the Jacobian of a nonreduced generating presentation need not
span the geometric conormal.

Equation (5), not `alpha A=J_A^*lambda` with `alpha=0`, is the smallest
theorem-grade singular interface.  It allows the minimizing point itself to
be a rank-drop limit of smooth normal pairs.

## 5. Smallest complete necessary system

The following real polynomial/constructible system is necessary for a
hypothetical exact source.  Therefore proving it inconsistent proves
`X5 + all 728 blocked => contradiction` and closes the conjecture.

```text
(FIBRE)       Phi(A)=Delta_8.

(NORMAL)      (A,-A) lies in CN(X_R), presented stratumwise by (5).

(BLOCK-MIN)   A_E=L_E^*L_E eta_E
              for all 8 full stars and all 56 triangles.

(BALANCE)     the 21 site-colour target-torus moment equalities.

(BLOCKED-C)   p(sigma_C)=0 and
              L_C^*L_C z_C=sum_i d_i(sigma_C) ell_C,i^*
              for every one of the 728 response carriers.
```

This is smaller and safer than the old Fritz--John interface in three ways:

1. no 6,561-coordinate output multiplier is introduced;
2. no carrier rank stratum or four-way external case expansion is needed;
3. singularity is handled by the reduced conormal closure, rather than by a
   universal left-cokernel witness.

The conormal/Fitting strata are the only unresolved structural input in this
formulation.  The Gram equations are already exact globally on the
realification.

## 6. New exact Euler elimination on the naive singular branch

Although the naive branch is not the right normal cone, its redundancy can
be sharpened source-faithfully.

For a site `v` and colour `c`, let `g_(v,c)(A)` multiply precisely the source
cells incident with `v` whose endpoint colour at `v` is `c`.  Every perfect
matching monomial contains exactly one cell incident with `v`.  Hence the
literal weighted Euler identity is

```text
(J_A g_(v,c)(A))_w = 1_(w_v=c) Phi(A)_w.                  (6)
```

At an exact ternary GHZ point the right side is the single pure-word basis
vector `e_(c^8)`.  Therefore any output covector in the raw left cokernel
satisfies

```text
J_A^*lambda=0  =>
lambda_(c^8)=<lambda,J_A g_(v,c)(A)>=0,
              c=0,1,2.                                  (7)
```

Thus all three pure multiplier coordinates eliminate exactly.  This is
strictly stronger than the unweighted degree-four Euler equation, which only
controls their sum.

But (7) terminally does not rescue `alpha=0`.  With the pure coordinates set
to zero, the remaining mixed Jacobian is a `6558x252` matrix, so

```text
dim_C ker(J_mix^*) >= 6558-252 = 6306                    (8)
```

at every source.  Consequently a nonzero mixed-only `lambda` satisfying the
singular output-multiplier equations exists universally, including away from
the exact fibre.  It carries no minimum-norm information.

This is the literal counterguard against reverting from (4)--(5) to the raw
Fritz--John presentation.

## 7. Terminal scope and next exact target

The report proves a new exact low-variable encoding of all 728 blocker
clauses and the pure-multiplier elimination (7).  It does not prove the
normal-cone system empty.

The smallest legitimate next elimination is not a global Macaulay run.  It
is one reduced exact-fibre/Fitting chart:

1. choose a source-faithful chart already present in the `X5` archive;
2. compute or certify its reduced local ideal and generic codimension;
3. form the saturated conormal equations (5);
4. append the Gram equations (2)--(3), using symmetry only after literal
   carrier labels are retained; and
5. seek a unit or a literal point of the system.

A literal point would be a counterguard to the normal-cone closure on that
chart, not a counterexample to the conjecture unless it also satisfies the
full exact fibre.  A unit on one chart is only a chart closure; a global proof
still requires the finite reduced/Fitting cover.

## Replay

The checker exhausts all `105*3^8=688,905` matching monomials and all
site--colour weights in (6), verifies the selector table, and records (8).

```sh
python3 computations/unaudited-codex-singular-normal-cone-gram-system-2026-08-22/audit_singular_normal_cone_gram_system.py --write-results
python3 -O computations/unaudited-codex-singular-normal-cone-gram-system-2026-08-22/audit_singular_normal_cone_gram_system.py
python3 -I -S computations/unaudited-codex-singular-normal-cone-gram-system-2026-08-22/audit_singular_normal_cone_gram_system.py
```

The hostile `--mutate-selector` run must fail.

All three valid modes return logical SHA-256
`8b3179f4ae26094e1206841e97f8a16fd35318b4aa8d12678c0f122cc87e12c1`;
the hostile selector mutation exits nonzero.

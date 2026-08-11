# Multisite endpoint concentration has an affine gate before Hall

## Result

The passage from arbitrary multisite endpoint stars to the concentrated
ordered-hole packet has an exact two-stage criterion.  It is not implied by
minimum response support plus selected target matchings alone.

Fix the common `q` and the two right rows `s_1,s_2`.  Put

\[
 L_s(v)=(vs_1q^{[h-1]},vs_2q^{[h-1]}).
\]

The two left rows lie in affine fibres

\[
 \mathcal A_1=p_1+\ker L_s,\qquad
 \mathcal A_2=p_2+\ker L_s.                            \tag{1}
\]

Choose target-coordinate points `p_i'` in (1).  Recompute

\[
 M_{p'}(w)=(p_1'wq^{[h-1]},p_2'wq^{[h-1]})
\]

and choose target-coordinate points `s_j'` in the two right affine fibres.
If the four chosen sites are distinct, bilinearity gives exactly

\[
 p_i's_j'q^{[h-1]}=p_is_jq^{[h-1]}=\delta_{ij}X_i.     \tag{2}
\]

This is a finite joint-kernel modification, not a tangent argument.  It is
anchor-safe precisely when every coordinate deleted by the two kernel
translations is either not a protected mutual anchor or is carried through
an anchor-preserving matching switch.

The obstruction is sharp:

1. the selected diagonal-response hole families may have no disjoint pair;
2. even after disjoint holes are selected, an affine fibre in (1) may miss
   every target-coordinate line; and
3. minimum support converts that failure into a unique full-support circuit
   modulo the target, not into a deletable kernel column.

Checker:
`computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py`.

## Exact Hall normal form for selected holes

One selected summand in each diagonal response gives two physical hole
edges.  Their four ordered ports are distinct exactly when those two edges
are disjoint.  Thus aggregate selection fails Hall precisely when the two
nonempty hole-edge families are **cross-intersecting**.

There is a short complete classification.  Let `A,B` be nonempty edge
families such that every edge of `A` meets every edge of `B`.

* A matching of three edges in `A` cannot be met by the two endpoints of
  an edge in `B`, so `nu(A)<=2`.
* If `nu(A)=1`, `A` is pairwise intersecting and is contained in a star or
  a triangle.
* If `nu(A)=2`, choose disjoint edges `ab,cd` in `A`.  Every edge of `B`
  joins one endpoint of `ab` to one endpoint of `cd`; hence `B` lies in the
  four-edge `K_{2,2}` rectangle on those sites.

This is the complete Hall obstruction—star, triangle, or four-site
rectangle—not an unbounded support family.  The checker audits all `32,767`
nonempty edge families on six sites through their maximal cross-
intersectors.  Exactly `5,141` have a nonempty cross-intersector, split as

```text
star 171, triangle 20, four-site rectangle 4950.
```

For individual selected hole pairs the `15^2=225` choices split into `90`
disjoint choices and `135` Hall collisions.

## Why selected matchings do not solve the affine gate

A selected matching term only says that one coordinate column contains a
nonzero target monomial.  The same complete column may also contain mixed
debts, cancelled by other occupied sites.  It need not itself be an exact
target preimage.

The pinned physical common-square guard realizes this literally:

\[
 C_0=X_1+Y,\qquad C_1=-Y,qquad C_0+C_1=X_1.           \tag{3}

Both columns are independent, the response is exact, and the first column
contains the selected `X_1` matching.  Nevertheless neither occupied site
line maps to `X_1`; the affine fibre has no target-coordinate point.  Its
free directions are response-zero coordinates and cannot delete either
occupied component.

At minimum support this is the general linear normal form.  If the occupied
complete response columns are `C_1,...,C_k`, they are independent.  Modulo
the target line their images have rank `k-1`, and the occupied star
coefficients form the unique full-support circuit.  Hence minimum support
does not manufacture a joint-kernel deletion; the full packet must kill or
transport this circuit.

The guard (3) is genuine for one common `q^[2]` and its complete Hessian
recurrences, but it is not a full one-bad source: its unary top is zero and
the second diagonal/crossed response packet is missing.  Those rows are
exactly the still-load-bearing input.

## Interface with the active-companion theorem

If a circuit carrier produces a nonzero determinant/cofactor product on a
free selected-anchor companion, `c78fc9b` supplies the distinct-head,
four-good active landing.  The remaining circuit branch is therefore
precise:

\[
 \boxed{\text{all active carrier products are trapped in the selected
 anchor web, and a required affine fibre misses every coordinate line}.}
                                                               \tag{4}
\]

The cubic anchor-union theorem and source units close (4) after the stars
have already been concentrated.  They do not prove that an arbitrary
multisite packet reaches that concentrated affine chart.  The needed
source theorem must use the unary top and the other-colour companion rows
to force one of:

* a target-coordinate point in every sequential affine fibre;
* a free active carrier covered by `c78fc9b`; or
* an anchor-preserving relation through a star/triangle/rectangle Hall
  obstruction.

This identifies the accessibility obligation without opening another
support or cardinality layer.

## Scope and verification

Run

```text
python3 computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py
python3 -O computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py
python3 -I -S computations/verify_uniform_multisite_endpoint_affine_hall_concentration_boundary.py
```

The checker pins the physical affine guard, the minimum-support Hessian
circuit theorem, the selected-channel classification, and the cubic
anchor-union landing.  It verifies the exact sequential kernel identity,
the complete cross-intersecting Hall normal form, and the physical failure
of affine target-line hitting.

Frozen ledger SHA-256:

```text
2168b112db11f4e652d1bc70e6569b0319f455ddf61fffc8cad8cbd073810613
```

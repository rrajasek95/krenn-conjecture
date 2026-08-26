# Quotient elimination and pure-skeleton rank floor at `N=8`

Status: **UNAUDITED EXACT NECESSARY REDUCTION.  THE UNIVERSAL `N=8`
THEOREM REMAINS OPEN.**  No certified or spine file was edited.

## Headline

The 219 literal `X4` slice identities have been independently projected to
`C*/W_C` for all 728 star/triangle carriers.  This projection cannot by
itself yield a carrier-local threshold in quotient dimensions zero through
seven: the exact W40 `X4` source has blocked carriers in every one of those
dimensions.

There is, however, a useful top-quotient theorem.  If `rank(L_C)=0` and the
pair block `A_pq` is nonzero, the carrier is active.  Combining this with one
live perfect matching from each pure row gives a global support condition.
An exact `S8 x S3` orbit census then proves:

> Every source blocked on all star and triangle carriers and satisfying
> `PURE-LIVE` occupies at least **12 physical site pairs**.  Depending on the
> chosen pure-matching chart, the exact lower floor is 12, 13, 14, or 16.

This closes every support stratum with at most eleven occupied physical
pairs.  It is a necessary reduction, not an `X4` emptiness proof.

## 1. Independently reconstructed quotient interface

Fix `p,q`, write `U=[8]-{p,q}`, and identify endpoint-ordered caps with
`C=F^9`.  For a residual edge `a<b`, the raw atomic response row is rebuilt
as

```text
rho_ab^(alpha,beta)[i,j]
  = A_pa[i,alpha] A_qb[j,beta]
      + A_pb[i,beta] A_qa[j,alpha].                    (1)
```

For a carrier `C`, `W_C` is the row span of (1) on forbidden residual
edges.  A rational nullspace basis of `W_C` gives coordinates on
`C*/W_C`.  For each of the 219 residual words `z` with maximum colour
multiplicity at least four, the checker independently verifies in that
quotient

```text
[delta_z] = H6(z)[s_pq]
  + sum_(ab allowed) H4(z without a,b)[rho_ab^(z_a,z_b)].  (2)
```

It does this for every labelled carrier, without importing the compressor's
implementation or ledger.  W40 has zero projected defects.  W25-F8 has
projected defects and is retained only as the all-blocked/outside-`X4`
negative control.

## 2. No carrier-local threshold in dimensions 0--7

For W40, the blocked carrier quotient dimensions are exactly

```text
0,1,2,3,4,5,6,7.
```

Its six active star carriers have quotient dimension eight.  Therefore a
claim of the form "an `X4` carrier with quotient dimension `d` is active"
is false for every `d<=7`.  Quotient dimension eight remains unresolved in
general; W40 supplies only positive examples there.

## 3. The top-quotient live-pair lemma

Suppose `rank(L_C)=0`.  Then `W_C=0`, so the four activity forms are the
three distinct coordinate forms

```text
kappa_0=K_00, kappa_1=K_11, kappa_2=K_22
```

and `s_pq=<K,A_pq>`.  If `A_pq` is nonzero, all four are nonzero linear
forms.  Their product is nonzero in the polynomial ring `Sym(C*)` over any
field.  Thus the carrier is active.  Equivalently:

> In an all-carrier-blocked source, every star and triangle carrier on every
> live physical pair has `rank(L_C)>=1`.                         (3)

No `X4`, balance, or genericity assumption is used in this lemma.

## 4. Raw arm graph and the exact support implication

For a live pair `p,q`, form the **potential raw arm graph** `R_pq` on `U`:
put `ab` in `R_pq` when the occupied physical-pair graph contains either

```text
pa and qb,  or  pb and qa.                              (4)
```

This definition is deliberately before numerical cancellation.  If an edge
is absent from `R_pq`, both products in every row of (1) are support-zero.
Consequently, if `R_pq` lies in a star or triangle carrier, all forbidden
atomic blocks vanish and `rank(L_C)=0`.  By (3), this is impossible in an
all-blocked source.

An exhaustive check of all `2^15=32,768` graphs on six vertices verifies the
elementary classification

```text
matching_number(R)<=1
  iff R is contained in a star or in a triangle.         (5)
```

The triangle-only cases are a must-fire control against silently retaining
only stars.  Equations (3)--(5) prove:

> For every selected live pure edge `pq`, `R_pq` has two disjoint edges.
> In particular both `p` and `q` have at least two occupied physical
> neighbours outside `pq`.                               (6)

Choosing one live perfect matching, which covers all eight sites, gives the
corollary that the occupied physical-pair graph has minimum degree at least
three and hence at least 12 edges.

Cancellation does not weaken this implication: (4) is used only to prove
that forbidden rows are identically support-zero.  Nonzero potential arms
are never asserted to produce nonzero response rows.

## 5. Exhaustive pure-matching orbit floors

The checker independently enumerates all `105^3=1,157,625` ordered choices
of one perfect matching in each pure colour.  A generator BFS under adjacent
site and colour swaps gives exactly 31 `S8 x S3` orbits.

For each representative it exhausts physical-edge augmentations in
increasing cardinality until condition (6) holds for every selected edge.
The resulting exact floors are:

| minimum physical pairs | chart orbits | labelled matching triples |
|---:|---:|---:|
| 12 | 16 | 428,505 |
| 13 | 6 | 514,080 |
| 14 | 8 | 213,780 |
| 16 | 1 | 1,260 |

Each stored upper witness is rechecked.  Deleting a necessary added edge is
a must-fire mutation.  Lower bounds are exhaustive: the search begins at
the degree-deficit bound and tests every smaller admissible augmentation
cardinality before accepting a witness.

The result uses only `PURE-LIVE` and all-carrier failure.  `BAL`, `X4`, and
`NO-SINGLETON-332` have not yet been imposed on the surviving decorated
supports.

### 5.1 Exact minimum-support census

An independent second enumerator exhausts every orbitwise augmentation at
the stated minimum.  There are 679 orbit-coordinate incidences: 373 at 12
pairs, 20 at 13, 262 at 14, and 24 at 16.  They comprise 520 labelled
physical masks and exactly 20 unlabelled graph types.  The unique 16-pair
type is two `K4`s joined by a perfect matching.  These counts are only a
support census; no cell-decoration conclusion is inferred from them.

## 6. Complete forced-support carrier family on the 31 charts

For a selected pure occurrence `(c,pq)`, the other two selected matchings
give zero, one, or two forced residual response edges.  The complete family
of clean carriers containing all of that forced support is exactly:

* zero edges: all six residual stars and all twenty residual triangles;
* one edge, including two coincident responses: its two endpoint stars and
  the four triangles containing it;
* two distinct intersecting edges: their common-centre star and their
  three-vertex triangle;
* two disjoint edges: the empty family.

This definition avoids an endpoint choice in the coincident case and is
manifestly `S8 x S3`-covariant.  The checker verifies the forced edges with
multiplicity, the entire carrier family, shared-pair colours, and the
split/same-endpoint orientation under generators of `S8 x S3` on all 31
representatives (1,488 occurrence images).

Exactly four zero-based orbits have empty family at all twelve selected
occurrences:

```text
zero-based quotient orbits 25,26,27,28
legacy one-based charts    28,29,30,31.
```

The legacy mapping is independently reconstructed from the port-matching
canonicalization, rather than guessed from orbit order.  Thus every one of
the other 27 charts has at least one selected occurrence with a nonempty
complete forced-support carrier family.  This is the proved **27-chart
carrier-family theorem**.  It says a carrier is available; it does not say
that the carrier is active.

W40 is the positive calibration.  It is zero-based orbit 24 / legacy chart
25 and has occurrence histogram `disjoint:2, intersecting:8, single:2`.
Its complete families recover exactly six active star instances.  All 219
literal `X4` projections vanish on these families.  The other 510 residual
words are not `X4` rows; 42 projected defects there are retained as a shell
control.

## 7. Exact five-row template, and the smallest failed bridge

The sparse m25 calculation supplies a useful algebra template.  At a site
with exactly two effective full neighbours, a three-row mixed-`X4` packet
varying the site colour and having one isolated live singleton spike
Cramer-forces a `2 x 2` arm minor `D=0`.  A second compatible packet at a
different spike colour has the form `D*Q + U=0`, where `U` is a live Laurent
unit.  The five rows therefore contradict an open source over every
integral domain.

The smallest tempting bridge lemma is false:

> A split canonical-star occurrence does **not** imply that the compatible
> five-row packet exists.

W40 is an exact countercontrol.  It has eight split canonical-star
occurrences, but its 28 physical blocks have support-size histogram
`0:11, 1:14, 2:3`; in particular it has no full `3 x 3` block at all, so it
cannot supply the template's two effective full neighbours.  More
conceptually, the selected skeleton supplies forced pure response edges,
not isolated singleton spikes, monomial spike cofactors, or structural
vanishing of all error cofactors.

Accordingly the five-row identity is recorded only as an algebra template.
No source-global packet-entry theorem and no source-valid reselection or
descent has been proved for the 27 charts.

## 8. Calibrations and exact remaining blocker

* W40 has one live matching in each pure colour.  Its triple is zero-based
  orbit 24, whose forced floor is 14 physical pairs; W40 occupies 17 and
  satisfies (6).
* W25-F8 has pure-live counts `(2,1,1)`, giving zero-based orbits 26 and 28;
  it occupies 21 physical pairs and satisfies (6), as an all-blocked source
  must.  Its failed projected slices ensure it is not mistaken for `X4`.
* W40 provides the exact carrier-local limitation in dimensions 0--7.

The remaining coefficient-level statement is precise: for a source-valid
selected chart outside orbits 25--28, prove that at least one member of a
nonempty complete forced-support family is active.  The present data do not
couple the blocker classes of different carrier members strongly enough to
do this.  A replacement by reselection would additionally require a
source-valid pure matching and a well-founded decreasing metric; neither is
supplied by a mixed-row cancellation.  Both statements remain open.

## 9. Reproduction

```text
python3 computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/audit_quotient_skeleton.py
python3 -O computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/audit_quotient_skeleton.py
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/audit_quotient_skeleton.py

python3 computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/enumerate_floor_supports.py
python3 -O computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/enumerate_floor_supports.py
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/enumerate_floor_supports.py

python3 computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/audit_canonical_carriers.py
python3 -O computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/audit_canonical_carriers.py
PYTHONDONTWRITEBYTECODE=1 python3 -I -S computations/unaudited-codex-x4-quotient-eliminator-2026-08-20/audit_canonical_carriers.py
```

Machine-readable quotient profiles and orbit floors are in `results.json`;
minimum supports are in `floor_supports.json`; complete carrier families,
legacy mapping, covariance controls, and the W40 countercontrol are in
`canonical_carriers.json`.

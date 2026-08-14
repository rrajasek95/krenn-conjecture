# The uniform support-16 two-`RRX` closure

This note continues the 26 residual graph orbits from
[`n8-support16-clean-terminal-census.md`](n8-support16-clean-terminal-census.md).
It proves a uniform tensor/rank theorem for 22 of them and closes every
mutual-coordinate exceptional completion by literal complete mixed fibres.
The remaining four graph orbits have a different, three-matching face.

The exact checker is
[`verify_n8_support16_two_rrx_coordinate_mixed_closure.py`](../computations/verify_n8_support16_two_rrx_coordinate_mixed_closure.py).

## Outcome

Every one of the 22 minimum-seal-two residuals has the same local geometry.
At a cubic/high cap `pq`, write

```text
P=N(p)-q={h,a},       S=N(q)-p={h,b,c},
x=the live edge on the two remaining vertices.
```

There is no `RRR` matching, and the only two `RRX` matchings are

```text
x | hb | ac,          x | hc | ab.                    (1)
```

Consequently their full coefficient map is the same tensor as at support 15:

\[
 F=a_0\otimes b_1+a_1\otimes b_0.                    \tag{2}
\]

The degree-four anchor-placement theorem and tensor-rank classification leave
only the familiar two coordinate rank strata.  Under a mutual-coordinate
completion of those strata, all 22 orbits are excluded by complete mixed
rows:

```text
normalized coordinate completions             33,228
immediate anchor-only Laurent units             33,186
binomial-to-singleton contradictions                42
binomial propagation length one / two            39 / 3
```

This includes both new `(6,4^5,3^2)` orbits.  Neither has any edge deletion
isomorphic to the support-15 terminal, so their proof is genuinely new rather
than an invocation of the previous result.

Exactly four graph orbits remain outside the two-`RRX` family.  Their minimum
face has three `RRX` matchings, no `RRR`, and a degree-four--degree-four cap.

## 1. The uniform tensor theorem

The cubic endpoint has exactly three incident source anchors.  On its two
external edges write the near vectors `u_0,u_1`.  At the degree-four endpoint,
write the two private response blocks as `M_0,M_1`.  Removing the common live
`x` multiplier and fixed far-coordinate factors from (1) gives

\[
 a_i=u_i^TKM_0,\qquad b_i=u_i^TKM_1,
\]

and hence (2), with every matrix entry retained.

The exact pure-tensor classification is:

\[
 a_0\otimes b_1+a_1\otimes b_0=0
\]

only if one side vanishes, or both pairs span lines with opposite
proportionality ratios.  For a rank-one cap `K=xy^T`,

\[
 F=2(u_0\cdot x)(u_1\cdot x)
       (y^TM_0)\otimes(y^TM_1).                       \tag{3}
\]

At the degree-four endpoint, at least three of the four roles

```text
direct, shared, M0, M1
```

are anchors.  Of the five possible placements, three anchor both response
blocks and reduce (2) to the already proved scalar `2x2` permanent.  The other
two have one anchored response block `w tensor e_d` and one arbitrary block
`M`.  Formula (3) supplies an active zero whenever an external vector, `w`,
or a left kernel of `M` meets the coordinate torus.

After permuting colours, the only exceptions are

```text
u0=e0, u1=e1, w=e0,
rank(M)=3,
or rank(M)=2 with ker_left(M)=<e_direct>.
```

Writing the relevant rows of `K` as `(a,b,c)` and `(d,e,f)`, the row before
`M` is

\[
                    g=(2ad,ae+bd,af+cd),
\]

and the same saturation identity handles both exceptional ranks:

\[
 2(ae)^2=2(ae)(ae+bd)-(be)(2ad).                      \tag{4}
\]

Thus (4) is the local obstruction, and complete source rows must remove it.

## 2. Exhaustive coordinate completions

For each of the 22 graph representatives, an edge state is one of

```text
*    an arbitrary 3x3 wildcard block, with all nine cells granted;
0,1,2 a nonzero scalar mutual coordinate anchor of that colour.
```

The normalized local exceptional chart fixes

```text
pq=2, ph=0, pa=1,
one of qb,qc is *, the other has colour w in {0,1},
qh has colour 1-w.
```

Exchanging `b,c` and choosing `w` gives four local variants.  Every vertex is
required to see coordinate anchors of all three colours.  The checker
backtracks all compatible assignments exactly; there is no sampling or
finite-field substitution.

Granting every wildcard cell makes the test anti-monotone in precisely the
useful direction: a matching unique in this maximum support remains unique
after any actual wildcard specialization.

For 33,186 completions, a mixed word has a unique matching consisting only
of live anchor scalars.  Its target coefficient is

\[
                         \prod_{e\in P}t_e=0,
\]

which becomes `1=0` after Laurent localization at the nonzero anchors.

The remaining 42 completions have an equally exact two-stage certificate.
A two-term mixed row is

\[
                         A+X=0,                         \tag{5}
\]

where `A` is already a product of known nonzero cells.  Hence `X` is nonzero,
and every wildcard cell dividing `X` is nonzero.  After one such row in 39
cases, and two rows in three cases, a singleton mixed row is a product of
known nonzero cells but is required to vanish.  No determinant of the
wildcard block is divided out; the argument works identically in rank three
and exceptional rank two.

For example, one completion of the orbit-size-240 new graph uses

```text
01211012:
 t27 t36 x01(0,1) x45(1,0) + t05 t14 t27 t36 = 0,

01220202:
 t27 t35 t46 x01(0,1) = 0.
```

The second monomial of the first row is an anchor unit.  Therefore
`x01(0,1)` is nonzero, contradicting the singleton second row.  The checker
stores an exact word/cell certificate for every exceptional completion.

## 3. The two first support-16 orbits

For the two `(6,4^5,3^2)` representatives from the census:

| orbit size | coordinate completions | immediate units | propagated |
|---:|---:|---:|---:|
| 60 | 1,104 | 1,104 | 0 |
| 240 | 998 | 996 | 2 |

Deletion cannot invoke support 15 even abstractly.  The old terminal has
degree sequence `(4^6,3^2)`.  Deleting one edge from a graph with a
degree-six vertex leaves that vertex of degree at least five, so no deletion
can enter the old orbit.  The checker additionally tests all 32 literal
deletions and finds none in its full relabelling orbit.

## 4. The four seal-three residuals

The exact residual list is now:

| degrees | orbit | triangles | squares | selected cap |
|---|---:|---:|---:|---|
| `(5,4^6,3)` | 360 | 6 | 16 | `26` |
| `(4^8)` | 840 | 8 | 12 | `04` |
| `(4^8)` | 2,520 | 8 | 10 | `02` |
| `(4^8)` | 10,080 | 6 | 14 | `04` |

Their representative supports are

```text
orbit 360:
01 02 03 05 06 15 16 17 24 26 27 34 35 37 45 46

orbit 840:
04 05 06 07 12 13 16 17 23 25 27 34 37 45 46 56

orbit 2520:
02 05 06 07 13 14 16 17 23 25 27 34 37 45 46 56

orbit 10080:
04 05 06 07 13 15 16 17 23 24 26 27 35 37 45 46
```

At the selected degree-four--degree-four cap,

```text
P={h0,h1,a},       S={h0,h1,b},
```

the two shores overlap in two vertices.  The two remaining vertices carry a
common live edge `x`, and the three seals are exactly

\[
 x\bigl(r_{h_0h_1}r_{ab}
       +r_{h_0b}r_{ah_1}
       +r_{h_0a}r_{h_1b}\bigr),                       \tag{6}
\]

with labels permuted according to the representative.  Equation (6), not
the two-tensor (2), is the next coefficient object.

The shortest next attack is to classify the anchor placements at both
degree-four endpoints of (6), dispatch placements reducing to a scalar
three-matching quadratic, and run the same wildcard-complete mixed-fibre
propagation only on the surviving coordinate placements.

## Scope

The local tensor/rank theorem is arbitrary-coefficient and applies to all 22
orbits.  The global mixed-fibre exhaustion is a theorem for **mutual-coordinate
anchor completions**.  The forced incident-edge theorem alone supplies a
rank-one block with a fixed coordinate factor at the far endpoint; it does
not make every high-degree near factor coordinate.  A noncoordinate vector
in one of the marked roles of (2) already routes to the active rank-one zero,
but a directed noncoordinate anchor elsewhere in the graph is not silently
re-coordinatized here.  Landing those remaining directed anchors into a
marked face is the exact hypothesis still needed to promote this conditional
closure to an unconditional exact-source theorem.

## Reproduction

```sh
python3 computations/verify_n8_support16_two_rrx_coordinate_mixed_closure.py
python3 -O computations/verify_n8_support16_two_rrx_coordinate_mixed_closure.py
python3 -I -S computations/verify_n8_support16_two_rrx_coordinate_mixed_closure.py
```

The frozen ledger digest is
`b469342acee94774030bc1b106edefff713b8bff036efb7458eebe6547edc7d2`.

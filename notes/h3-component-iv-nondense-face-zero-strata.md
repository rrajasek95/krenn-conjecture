# Nondense `V(h)` has one regular four-site family and two singular boundaries

## Exact support theorem

Let `q_m` be the five-site decorated scalar slice from `1932822`, and let
`h_v` be its five deleted-four-site hafnians.  Classify exact supports, so
every displayed edge coefficient is nonzero.

If one four-site face has exactly one supported perfect matching, its
`h_v` is a nonzero monomial.  Excluding these leaves 172 labelled supports,
or 14 orbits under `S5`.  They split exactly as follows.

1. Nine nondense orbits are feasible.
   - Six are intersecting edge families: stars and the triangle (including
     their subfamilies).  They have matching number at most one, so every
     `h_v` vanishes termwise.
   - Three have one isolated vertex and induced support `C4`, `K4-e`, or
     `K4`.  Their sole supported four-site hafnian has respectively two,
     two, or three terms and can cancel.
2. Four nondense orbits are impossible: `K2,3`, `K2,3` plus the edge in
   its two-vertex part, `K5` minus two disjoint edges, and `K5` minus one
   edge.  In each case three of the binomial face equations form an odd
   Laurent holonomy.  Their product ratios give `1=(-1)^odd=-1`, hence a
   localized `2` unit in characteristic zero.
3. The remaining orbit is dense `K5`, whose two cyclotomic torus points are
   the stratum already classified by `1932822`.

Checker:
`computations/verify_h3_component_iv_nondense_face_zero_strata.py`.

This gives a compact structural statement: every feasible nondense exact
support is either intersecting, or is carried by four sites and contains a
`C4`.

## Which boundary strata admit the normal comparison

The five-face Jacobian `dh` distinguishes the proof-relevant pieces.

For canonical `C4` coordinates

```text
x02=a, x03=b, x12=c, x13=-bc/a,
```

and also after adjoining `x01=e` (`K4-e`), the same five-column minor is

```text
4*b^2*c^3.
```

It is a unit on the exact support torus.  Thus these strata have normal
rank five.

On isolated `K4`, write

```text
x02=a, x03=b, x12=c, x13=d, x01=e,
x23=-(ad+bc)/e.
```

The corresponding minor is

```text
4*c*((ad)^2 + adbc + (bc)^2).                         (1)
```

Away from the zero of the second factor, the normal rank is again five.
At every rank-five point, choose five dual normal directions.  Since each
`h_v` is quadratic, the divided normal matrix has the exact form
`B(tau)=I+tau R`, hence is formally invertible.  The polynomial shifted
filler and the indispensable normal Hasse face from `827e329` therefore
extend verbatim at the relative derived level.  This is the
comparison-compatible nondense family.

## First exact boundary counterguard

Equation (1) has a cyclotomic zero.  A normalized representative is

```text
x01=x02=x03=x12=1,  x13=zeta,  x23=zeta^2,
zeta^2+zeta+1=0,
```

with the fifth vertex isolated.  Its three `K4` matching products are
proportional to `zeta^2,zeta,1`, its five face hafnians vanish, and

```text
rank(dh)=4.
```

In face order `0123,0124,0134,0234,1234`, the primitive missing normal
covector is

```text
(0, 1, zeta, zeta^2, 1).                              (2)
```

It annihilates all ten edge-direction columns of `dh`.  Thus the dense
normal inverse cannot simply be specialized across this boundary.  The
minimal new lemma here is a source-provenant endpoint-word-changing row
whose normal boundary pairs nontrivially with (2), or a constructive source
route excluding this orbit.

The intersecting star/triangle strata are more singular: representative
normal ranks are `0,3,3,4,3,4` for zero, one edge, two-star, three-star,
triangle, and four-star.  Their square-zero equation is combinatorial and
the fixed-word packet of `1932822` does not route them.  They require a
separate source theorem for matching-number-at-most-one support; they are
not consequences of the cap-line inactive/rootless split.

## Scope

This is an exact classification of the internal `q_m` support tori and an
exact relative-derived normal-rank theorem.  It does not construct a full
physical source on any boundary stratum, identify derived `Yw` with the
physical cap coordinate, or prove that a singular support lands in an
inactive branch.  The primitive physical comparison obstruction pinned by
the Component-IV artifacts remains.

## Verification

```text
python3 computations/verify_h3_component_iv_nondense_face_zero_strata.py
python3 -O computations/verify_h3_component_iv_nondense_face_zero_strata.py
python3 -I -S computations/verify_h3_component_iv_nondense_face_zero_strata.py
```

Frozen ledger SHA-256:

```text
2df42d8e4a2da409eee136059408dd18d401c62a16480e18822df537fad02585
```

# The singular `V(h)` strata have literal weighted-normal escape rows

## Cyclotomic isolated `K4`

Use the normalized singular point from `9376a3f`:

```text
x01=x02=x03=x12=1,  x13=zeta,  x23=zeta^2,
zeta^2+zeta+1=0,
```

with site `4` isolated.  The first face Jacobian has rank four and primitive
left covector, in face order `0123,0124,0134,0234,1234`,

```text
lambda=(0,1,zeta,zeta^2,1).
```

There is nevertheless an exact tangent direction

```text
n01=1+zeta, n02=1, n04=1,
n14=zeta^2, n24=zeta, n34=1.                           (1)
```

For the literal five marked Schur polars,

```text
h(q0+tau*n)=tau^2*(0,-2-zeta,1+zeta,1,0),
lambda h(n)=-4-2*zeta != 0.                            (2)
```

Thus the first-order covector is not an all-order separator.  The second
Hasse coefficient of the already-certified complete endpoint-word-change
plus Schur rows pairs nontrivially with it.  Together with four independent
first-normal edge columns, (2) gives weighted degrees

```text
(1,1,1,1,2).
```

This is the requested positive source-row coefficient.  It does not by
itself supply the complete second-normal source-chain companion.

## Intersecting supports

The six intersecting exact-support orbits from `9376a3f` also have complete
weighted normal systems.  Exact degree profiles are

| support | rank `dh` | weighted normal degrees |
|---|---:|---|
| zero | 0 | `2,2,2,2,2` |
| one edge | 3 | `1,1,1,3,3` |
| two-star | 3 | `1,1,1,2,2` |
| three-star | 4 | `1,1,1,1,3` |
| triangle | 3 | `1,1,1,2,2` |
| four-star | 4 | `1,1,1,1,2` |

For example, on the four-star `x01=x02=x03=x04=1`, the tangent

```text
n12=1, n14=-1, n23=-1, n34=1
```

satisfies `dh(n)=0` and `h(n)=2 e_1234`.  It supplies the missing face in
order two.

The one-edge and three-star cases genuinely first expose their missing
directions in order three.  On the one-edge point `x01=1`, the arcs

```text
q+tau*x02+tau^2*x34,
q+tau*x12+tau^2*x34
```

have order-two terms in the existing first-normal span and order-three
terms `e_0234` and `e_1234`.  On the three-star, the second arc has the same
triangular form and supplies its sole missing face in order three.  The
checker records every arc and all lower coefficients, and verifies that the
resulting five columns are exact bases.

## Source provenance and remaining lemma

The word change `11211200 -> 01211200` is a literal 105-term covariance
identity.  The five subsequent marked Schur polars are the literal
three-matching polynomials `h_v`.  Therefore every coefficient above is a
Hasse/principal-parts coefficient of an original complete source row, not a
declared aggregate column.  All complete words remain mixed, and the two
tagged chart copies remain equal with opposite signs, so target and old
ordinary residue vanish coefficientwise.

The remaining step is chain-level.  `827e329` constructs and verifies the
complete **first** normal Hasse face.  The singular strata require the
complete second-normal companion, and the one-edge/three-star strata require
the displayed third-normal triangular companion.  After those companions,
one must still identify derived `Yw` with physical `W`.  This note does not
declare either construction or physical cap identification.

## Verification

```text
python3 computations/verify_h3_component_iv_singular_face_weighted_normal_escape.py
python3 -O computations/verify_h3_component_iv_singular_face_weighted_normal_escape.py
python3 -I -S computations/verify_h3_component_iv_singular_face_weighted_normal_escape.py
```

Frozen ledger SHA-256:

```text
29a01bfdb19f1dac157ab20ad0e876d8602d37020bc4e69f9fdd95fd1aa0ef1d
```

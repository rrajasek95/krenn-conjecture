# Four-vertex path switching leaves a decorated cofactor correction

## Outcome

On the smallest decorated Ward guard, the coefficient-complete four-vertex
hafnian expansion cleanly isolates the desired physical C4 exchange.  After
that exchange, one term remains:

```text
H_1567(0011) - rho H_1567(1111).                           (1)
```

Here `rho` is the scalar supplied by whatever determinant/rank-one exchange
is used on the four distinguished vertices.  The correction (1) changes a
colour cell on the common physical edge `15`.  Neither the physical C4 nor
the currently selected curvature minor contains that cell.  Thus path
switching identifies the missing source grade but does not eliminate it.

The literal four-cell support has 14 Laurent singleton target rows, so its
full torus saturation is the unit ideal for a much simpler reason.  That
vacuous unit must not be promoted as a common-edge transport lemma.

## Exact four-vertex expansion

Use

```text
support     = 03:11, 15:00, 15:11, 67:11
active word = 10022011
pure word   = 11111111
four sites  = {0,2,3,4}
residual    = {1,5,6,7}.
```

Classify every perfect matching by whether the four distinguished sites are
paired internally, retaining all other matchings as the mate/path sum.  On
this packet the two complete expansions are

```text
active: (02|34) H_1567(0011) = mask 10,
pure:   (03|24) H_1567(1111) = mask 13,                    (2)
```

and every other internal pairing and mate/path sum is zero.  The residual
cofactors are

```text
H_1567(0011) = (15:00)(67:11) = mask 10,
H_1567(1111) = (15:11)(67:11) = mask 12.                  (3)
```

Switching `02|34` to `03|24` can compare the four-site cell products in
(2).  It cannot replace the first line of (3) by the second.  The unmatched
correction is concretely

```text
(67:11) ((15:00) - rho (15:11)).                          (4)
```

This is the minimal decorated alternating-cycle correction: physically the
edge `15` is common to both matchings, but source-labelled incidence sees
two different parallel colour cells.

## Why the present curvature ledger does not remove it

The nonzero selected curvature packet uses

```text
(02:10)(43:10) - (04:11)(23:00) = -1.
```

The exact colour ledger on the guard is

```text
02:10=1, 43:10=0, 04:11=1, 23:00=1,
34:22=1, 24:11=1.
```

The active exchange needs `34:22`, while the curvature's opposite cell is
`43:10`; the pure exchange needs `03:11` and `24:11`.  More importantly,
none of these six entries is `15:00` or `15:11`.  Substitution of the
rank-one arms and curvature scalar therefore leaves (4) untouched.  A
successful identity needs an additional full-nine row whose source-labelled
path reaches edge `15` in both colour grades.

## Fixed-support saturation is vacuous

The complete eight-site target residual for this four-cell packet has
exactly 15 rows:

```text
14 nonzero Laurent monomial rows,
1 pure row (mask 13) - 1.
```

In particular the selected active coefficient itself is the singleton
`mask 10`.  Localizing the four support weights makes that one row a unit,
before any four-vertex exchange or common-edge comparison is used.  Hence a
computer algebra result saying that this literal fixed-support saturation is
the unit ideal would be correct but irrelevant to the desired uniform lemma.

The first nonvacuous coefficient-complete chart must admit cancellation
mates for these private rows.  The committed Hall audit already shows that
no such mate-complete active support occurs through seven additions; this
note does not enumerate the eight-addition layer.

## Scope

The correction (4) is a precise no-go for a proof using only the physical
C4 exchange plus the existing curvature scalar.  It is not a no-go for a
larger Bianchi/Ward identity that transports the residual colour word, and
the sparse packet is not an exact GHZ source.

## Reproduction

```text
python3 computations/verify_oo_c8_four_vertex_exchange_correction.py
python3 -O computations/verify_oo_c8_four_vertex_exchange_correction.py
```

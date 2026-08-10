# Every direct second repair creates another forced singleton

## Result

Continue from the eight first-mate charts in
`n8-one-bad-first-cross-mate-exchange.md`.  Each first mate creates one or
two private mixed top words.  Fix one such word.  Its displayed matching is
one of the fifteen physical perfect matchings on six sites, so there are
exactly fourteen direct second routes with the same endpoint-coloured word.

The exact source-labelled census has

```text
12 private top witnesses * 14 alternate routes = 168 charts.
```

They split as `112` charts above the first sharp orbit and `56` above the
second.  Every direct route needs either two or three genuinely new cells:

| new cells | charts |
|---:|---:|
| 2 | 72 |
| 3 | 96 |

On every chart, complete expansion of the top tensor and all four binary
response rows leaves at least one forbidden singleton coefficient.  More
strongly, every chart has a **fresh** singleton using a newly introduced
second-route cell.  Thus

\[
 \boxed{\text{none of the 168 direct second-route charts has a rational
 point on its localized coefficient torus.}}             \tag{1}
\]

The checker is
`computations/verify_n8_one_bad_second_coupled_repair_residual.py`.

## Why this is multiplication-safe

This conclusion does not identify a cell product after passing to an
abstract support shadow.  Localize at the seven sharp cells.  Their
all-`a` top anchor and two diagonal response anchors make their products
nonzero.  The old private cross equation has the form

\[
                         m_{\rm old}+m_{\rm mate}=0,      \tag{2}
\]

so both first-mate cells are nonzero.  The selected private top equation,
after the direct second route is added, has

\[
                         t_{\rm mate}+t_{\rm second}=0.  \tag{3}
\]

The first term is nonzero, hence the product of the new second-route cells
is nonzero.  Every residual singleton recorded by the checker is a literal
matching monomial in these forced-nonzero cells.  Its required mixed
coefficient equation is therefore `unit=0` in the localized scalar
coefficient ring.  No multiplication of target tensors or cancellation of
a common matching power is used.

## The smallest genuine residual

Use the first sharp orbit

```text
Ma = 01|23|45,       colour a=2
Mb = 02|14,          colour b=0, holes (3,5)
Mc = 03|15,          colour c=1, holes (2,4).
```

For the `bc` cross row, take the first mate

```text
01:01, 25:01.
```

One induced top word is `100101`.  Its old and new routes are

```text
14:00 | 03:11 | 25:01,
04:10 | 13:01 | 25:01.
```

Thus the direct second repair adds only `04:10` and `13:01`.  Equation (3)
forces their product nonzero.  But complete top expansion has the two fresh
singleton rows

```text
000122 : 45:22 | 02:00 | 13:01,
112201 : 23:22 | 15:11 | 04:10.
```

Equivalently, the localized coefficient ideal contains

\[
 z_{45}^{22}z_{02}^{00}z_{13}^{01},\qquad
 z_{23}^{22}z_{15}^{11}z_{04}^{10},                     \tag{4}
\]

while every factor is nonzero.  Either row is already the first genuine
second-route obstruction.  The same chart also retains two inherited
singletons, but (4) shows that the failure is not merely inherited from the
first step.

## Exact scope

Equation (1) closes one first mate followed by one direct alternate perfect
matching for one induced top word.  It does not exclude a simultaneous
third-route packet that repairs several residual words with shared cells,
nor a different leading support.  The next proof step, if this lane is
continued, is an exchange/holonomy statement for simultaneous repairs of
the two fresh words in (4), not a wider unconstrained support search.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_one_bad_second_coupled_repair_residual.py
.venv/bin/python -O computations/verify_n8_one_bad_second_coupled_repair_residual.py
```

Both modes freeze

```text
f992ba8a9e6ba72fe3fe6c7ddc860e5e4d4630e05028b88df177fd54d3e6d996
```

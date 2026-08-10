# First variation of the Segre--K4 diagonal-carrier unit

## Exact result

The six-row certificate for the fixed Segre--K4 quadratic is valid after
adjoining arbitrary `00`, `11`, and `22` cells on all fifteen edges.  There
are 76 remaining decorated cell coordinates.  Adjoin any one of them with
an independent coefficient and compute the exact transgression of that
certificate.

Of the 76 directions, 60 leave the certificate identically unchanged.  The
only 16 nonzero first variations are

```text
02:10  02:12  02:20
03:01  03:10  03:20
04:02  04:10  04:12  04:20
05:01  05:10  05:21
13:01  14:02  15:01
```

Every one is incident to site 0 or site 1.  Their transgression term counts
are respectively

```text
8,6,8,  3,8,8,  3,4,12,8,  3,7,12,  3,3,3.
```

The complete histogram over all missing cells is

```text
0 terms: 60 cells
3 terms:  6 cells
4 terms:  1 cell
6 terms:  1 cell
7 terms:  1 cell
8 terms:  5 cells
12 terms: 2 cells
```

The standard-library checker
`computations/verify_n8_one_bad_segre_cube_diagonal_carrier_first_variation.py`
reconstructs every physical matching and verifies that each remainder is
linear in the adjoined coordinate.

## Interpretation

This turns the vague requirement to “deform the mixed carrier” into a small
normal obstruction.  At first order, a deformation that can evade the
diagonal-carrier unit must use one of sixteen endpoint-local directions.
The four one-bad response rows should now be restricted to those directions:
either they force a literal unit/clean cap, or they exhibit the first genuine
coefficient-feasible tangent carrier.

The statement is only first-order.  Two directions that are individually
invisible can interact at second order, so the result is not a chart-cover
or an emptiness theorem by itself.

# Direct X5 attack on matching-triple orbit 23 after a unimodular T0 gauge

## Verdict

The certified pure-matching chart admits an exact nine-variable torus gauge,
but the reduction is not large enough to close the chart.  A bounded F4 run
on the resulting `244`-variable, `242`-equation incremental core completes
three degree-6 matrices, then times out with `181,573` pending pairs.  It
returns neither a unit nor a candidate point.

This is one `S8 x S3` orbit only.  No conclusion is drawn for the other 30
matching-triple orbits.

## 1. Chosen maximal-rank chart

The 31-orbit ledger gives orbit 23 the representative

```text
M0 = 01 | 23 | 45 | 67,
M1 = 02 | 13 | 46 | 57,
M2 = 03 | 12 | 47 | 56.                              (1)
```

Its twelve physical anchor pairs are distinct.  The chart localizes the
twelve diagonal source cells selected by (1), equivalently their product.
An exact character-rank census confirms that all 31 matching-triple
representatives have anchor-weight rank nine on `T0`; hence nine is maximal
and orbit 23 is a valid maximal-rank choice.

The normalization-preserving torus has cocharacter lattice

```text
N(T0) = {u in Z^24 : sum_i u_(i,c)=0 for c=0,1,2},
dim T0 = 21,
```

with basis `e_(i,c)-e_(7,c)`, `i=0,...,6`.  A diagonal anchor `x_ij[cc]`
has restricted weight

```text
delta_(i,k)+delta_(j,k)-delta_(i,7)-delta_(j,7)
```

in colour block `c`.

## 2. Exact gauge slice and invariant products

Fix the first three anchors of each matching to one:

```text
x01_00 = x23_00 = x45_00 = 1,
x02_11 = x13_11 = x46_11 = 1,
x03_22 = x12_22 = x47_22 = 1.                       (2)
```

Their `9 x 21` character matrix has rank nine.  On the cocharacter columns

```text
(0,0),(0,2),(0,4),
(1,0),(1,1),(1,4),
(2,0),(2,1),(2,5),
```

the determinant is `-1`.  Thus (2) is an **integral unimodular gauge**:
it requires no root extraction and works over every field, not merely over
an algebraic closure.

The three unfixed anchors become

```text
P0 = x67_00,
P1 = x57_11,
P2 = x56_22.                                         (3)
```

Each `Pc` is exactly the product of the four original anchors of colour `c`,
because the product of their four weights is the pure character and is
trivial on `T0`.  The localized slice therefore uses the single exact row

```text
uinv * P0 * P1 * P2 - 1 = 0.                         (4)
```

This preserves the invariant anchor products rather than setting them to
one.  Nine of the 252 source variables are eliminated:

```text
252 source variables -> 243 slice source variables
                     -> 244 variables including uinv.
```

The guaranteed anchor action has rank only nine, so a 12-dimensional `T0`
stabilizer remains.  Further gauge fixing would require additional live
cells not supplied by this pure-matching chart and would silently restrict
to a smaller open.

## 3. Literal incremental X5 core

At the deterministic `F_32003` specialization, the three pure equations are
solved linearly through (3); their values are

```text
P0 = 28087,   P1 = 14024,   P2 = 26476 mod 32003.
```

Equation (4) is then solved for `uinv`.  Starting from these four exactly
satisfied base equations, literal mixed rows are inserted by increasing
off-count into the affine Newton system `J delta = -F`.

The coefficient rank reaches `241` after 237 independent mixed rows.  The
next literal equation

```text
F_11210111 = 0                         (profile 611)  (5)
```

gives the first tangent contradiction.  The 238 mixed residuals seen have
profile census

```text
48 profile 71,
94 profile 62,
96 profile 611.
```

The resulting exact nonlinear input contains

```text
244 variables,
238 mixed X5 rows + 3 pure rows + 1 localizer = 242 equations,
664,750 bytes,
SHA256 d10b10ac2fe1a5d9862157d8ef38dd9b371958cd06a21e7a7dfafce3aab62e79.
```

The complete gauge, specialization, row-label ledger, and source hashes are
in [`results_orbit23_t0_gauge_x5.json`](results_orbit23_t0_gauge_x5.json).
As before, the tangent contradiction is a local screen at a nonsolution; it
is not nonlinear UNSAT.

## 4. The single bounded F4 gate

Command:

```bash
timeout 60s msolve -f orbit23_t0_core_p32003.ms \
  -o orbit23_t0_core_p32003.out -t 4 -v 2 -m 500
```

Completed frontier:

| degree | matrices | new basis elements | zero reductions |
|---:|---:|---:|---:|
| 5 | 3 | 1,015 | 0 |
| 6 | 3 | 1,169 | 331 |

The three completed degree-6 matrices have sizes

```text
2233 x 268816,
1994 x 234259,
2038 x 232720.
```

At the timeout, the next 500-pair degree-6 batch sees `181,573` pending
pairs.  Exact details are frozen in
[`results_orbit23_t0_core_msolve_probe.json`](results_orbit23_t0_core_msolve_probe.json).

Compared with the ungauged triangle-incidence cores, the reduction does let
F4 process substantially more of degree 6 within the cap.  It does not
materially change the terminal behavior: pair growth accelerates and no
unit, parametrization, or dimension sentinel appears.

## 5. Exact scope and next residual

Proved for orbit 23:

1. the twelve anchor characters have maximal `T0` rank nine;
2. the nine fixed anchors have a determinant-`-1` character minor;
3. the remaining three anchors are the preserved invariant products;
4. the source-faithful localized slice has 244 variables including one
   inverse;
5. the specified incremental core and F4 frontier are literal X5 data.

Not proved:

1. feasibility or infeasibility of orbit 23;
2. anything about the other 30 matching-triple charts beyond their common
   anchor-weight rank nine;
3. validity of fixing any additional source cell;
4. a global implication from the random tangent contradiction.

The bounded result says the pure anchors alone can quotient only 9 of the 21
torus dimensions.  A materially smaller direct solve needs a source theorem
forcing twelve additional live cells, or a coefficient/elimination identity
that handles the residual stabilizer without localizing them.

## 6. Replay

```bash
python3 audit_orbit23_t0_gauge_x5.py --check-results
python3 -O audit_orbit23_t0_gauge_x5.py --check-results
python3 -I -S audit_orbit23_t0_gauge_x5.py --check-results
```

Logical digest:

```text
3992167f07c0a25e708959edb03d0038eb6ca430905d4b0587492e498de55cf0
```

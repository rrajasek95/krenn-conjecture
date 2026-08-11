# Edge `03` stays zero to all orders on the same-hole normal form

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_edge03_nakayama_stability.py`

## Verdict

The active-clean pencil in `c85ff47` is not merely a first filtered
phenomenon.  In the completed local ring of the literal same-hole normal
form, allow **every** internal decorated `q` cell to vary.  The complete
`tt`, `ca`, and diagonal-`Ra` rows force

```text
q03:ab = 0   for every a,b in {0,1,2}.
```

Thus the exact stability condition identified in `c85ff47` holds to all
orders, and its active clean cap survives arbitrary higher internal-`q`
support.  The proof is a finite Nakayama contraction, not a cubic support
enumeration.

The theorem retains the displayed endpoint-star and direct normal form.
Deforming those stars or leaving the three localized unit charts is a
different branch.

## Exact source rows

Use colours `(a,c,t)=(0,1,2)`.  The `tt` row with fixed holes

```text
Pt@1, Qt@0, Rt@4
```

leaves only physical edge `23`.  Its nine literal coefficients therefore
fix the complete decorated block

```text
q23:22=1,       q23:ij=0 for (i,j)!=(2,2).
```

Put

```text
u_ab = q03:ab,
v_a  = q02:a1,
w_b  = q34:b1.
```

The following base cells are units in the completed chart:

```text
q24:11,   q34:00,   q01:00.
```

For every `a,b`, the `ca` word `(a,2,1,b,1)` gives exactly

```text
q24:11*u_ab + v_a*w_b = 0.                         (1)
```

The third matching would contain `q23:1b` and is zero by the `tt` block;
the common-hole cubic is colour-incompatible.  Hence (1) is a complete
physical row, not an initial-form truncation.

For every `a`, the `ca` word `(a,2,1,0,0)` gives

```text
q34:00*v_a + u_a0*q24:10 = 0.                       (2)
```

Again the possible `q23` term is zero.  Finally the diagonal-`Ra` word
`(0,0,0,b,1)` gives

```text
q01:00*w_b + u_0b*q14:01 + q04:01*q13:0b = 0.       (3)
```

The checker reconstructs all `9+3+3` equations directly from literal
perfect matchings and verifies every source label and sign.

## Nakayama contraction

Let `m` be the maximal ideal of cells zero at the displayed normal-form
point and put

```text
I=(u_ab),       V=(v_a),       W=(w_b).
```

The three unit-leading row families give

```text
V subset m I,
W subset m I + m^2,
I subset V W.
```

Therefore

```text
I subset (mI)(mI+m^2)
  subset m^2 I^2 + m^3 I
  subset m^3 I,
```

where the last inclusion uses `I subset m`.  Since `I` is finitely
generated in the complete local ring, Nakayama gives `I=0`.

This is the all-order statement which the first tangent audit was missing.
There is no later nonlinear `q03` repair compatible with the complete rows
on this normal-form chart.

## Consequence for the active-clean pencil

For the pencil

```text
E_tt + z(E_cc+mu I),
```

the only possible clean-error term uses the disjoint response edges `26`
and `14`, leaving complement edge `03`.  Each decoration `q03:ab` would
produce its own distinct error word `(a,2,0,b,2,0)`.  Since the ideal of
all those cells is zero, the cap error remains identically zero in the
completed branch.  The explicit point `mu=z=1` remains active.

## Scope

This is all-order in the internal quadratic, not merely through quadratic
normal degree.  It assumes the literal endpoint-star/direct normal form

```text
Pt@1:t, Qc@0:c, Ra@2:a, Qt@0:t, Rt@4:t,
Dca=1, Dtt=0, Dpr=Ecc,
```

and localization at `q24:11*q34:00*q01:00 != 0`.  Extra endpoint-star
components can change equations (1)--(3), and a branch on which one of the
three units vanishes is not covered.  Those, rather than cubic internal
support, are the precise remaining same-hole escape routes.

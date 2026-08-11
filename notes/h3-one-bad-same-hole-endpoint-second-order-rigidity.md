# Every endpoint tangent lifts to order two, but none breaks the private unit

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_endpoint_second_order_rigidity.py`

## Verdict

Restrict the exact endpoint Hasse map to the three full-Jacobian kernels from
`bb35c6a`.  Every endpoint tangent admits a second-order correction solving
all `6561` output rows through order two.  Nevertheless the private defect
Hessian is identically zero on every kernel pair, so no genuine quadratic
endpoint arc breaks the private-row unit.

For an arc `X(t)=X0+t*v+t^2*w`, the order-two full-output equation is

```text
J*w + H(v,v) = 0.
```

The exact restricted ledgers are

```text
packet                         dim K  K-pairs  nonzero H  entries  rank J/H
shared C/A                        29      435          3       67   133/133
middle A/T right                  11       66          3       49   151/151
middle A/T left+secondary         11       66          3       78   151/151
```

All but three quadratic kernel monomials have zero Hasse column.  Each of the
three surviving columns lies in `im J`; the checker constructs and replays an
explicit rational endpoint correction for every one.  Thus the second-order
compatibility locus is the whole tangent kernel rather than a smaller
quadratic subvariety.

## Private defect

Write

```text
D = ra*F_00000001 - rc*F_00000000.
```

The first derivative of `D` vanishes on the entire endpoint space by
`bb35c6a`.  On two kernel directions, all first-output terms vanish, so the
quadratic coefficient reduces exactly to

```text
H_00000001 + 2*H_00000000.
```

The checker evaluates this on all `435+66+66=567` symmetric kernel pairs.
Every value is zero.  Since `dD(w)=0` for the second-order correction as
well, no compatible endpoint jet changes `D` at order two.

The only nonzero Hasse pairs come from two distinguished outer gauge
coordinates.  For shared C/A these are direct cells `56:00,57:11`; for both
middle packets they are `57:11,67:10`.  The exact correction vectors are
included in the frozen ledger.

## Scope

This is a complete coefficient-exact order-two endpoint theorem with
internal `q` fixed.  It does not promote the nonexact carrier calibrations to
solutions, and it does not classify cubic endpoint effects or any `q`
deformation/support layer.

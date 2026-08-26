# Exact Cof(1,3) targeted certificate audit

Status: **UNAUDITED, exact characteristic-zero branch result**.  This lane
does not edit any proof spine.

## Outcome

The frozen degree-267 modular inverse of `Cof(1,3)` has been traced back to
the literal source row and converted into an exact fraction-free Cramer
obstruction

```text
G(D,D*y) = D^2 * cleared_Cof(1,3)(y).
```

The source replay includes the `D=0` boundary and uses the three labelled
packet rows `t023`, `t123`, and `Cof(0,0)`.  The reduced obstruction has
7,264 terms and degrees `(1,8,31,26)` in `(b0,b1,d1,x)`.  The independent
raw-source replay has logical SHA
`ae25cf4a808cebdf8ed64386f5de1c99b43734446fb8c05a7b8463f7218990a2`.

Eliminating `b0` exactly against

```text
Q = A*b0^2 + C,       G = g1*b0 + g0
```

gives the fraction-free necessary condition

```text
A*g0^2 + C*g1^2
 = L * (b1-d1)^2 * (x-1)^5 * (-C)^6 * (d1^2*x-1)^7,
```

where `L` is a primitive 3,152-term degree-46 polynomial.  The exact
factorization is over `Z`; its logical result SHA is
`0d8057c4c3dc8de98cbb720b2f2dad357e2732610d17d90fa00790f23f962e7d`.
Only `x-1` and `C` are removed using the already declared chart/Q live
conditions.  Neither `b1-d1` nor `d1^2*x-1` is silently treated as a unit.

## Closed h branch

On the branch `h=d1^2*x-1=0`, exact Laurent substitution factors `Q` as

```text
-(d1^2+1)*(d1^2+2*d1-1)*(b0-d1)*(b0+d1).
```

The frozen saturator makes all factors except `b0-d1` live, so `Q` forces
`b0=d1`.  After those substitutions, all fifteen determinant rows and the
Cofactor row reduce to exact polynomials of 15--70 terms in `Q[b1,d1]`.
An exact Singular lift using fourteen determinants (all except
`minor_0145`) and `Cof(1,3)` proves

```text
sum_i multiplier_i * row_i = (b1+d1)^2.
```

Since `b1+d1` is a declared live factor, this is an exact localized unit
certificate closing the entire `h=0` branch.  The certificate logical SHA
is `08826f812c4d4b1fc1d952b63036959d1dd5dd6d010a185cb495cc6e972a7cd6`;
an independent frozen-ledger replay gives
`fdecd4e514d3a89cbfb80f4e49bf1e5578ce3cad1368a67613c3f2f453ab750e`,
and negating one multiplier fires the mutation guard.

## Remaining branches and scope

This does **not** prove the full four-variable ideal is a unit.

- `G` vanishes identically after `b1=d1`, so the selected Cofactor row gives
  no information on that branch; it must be closed from `Q` and the fifteen
  determinant rows.  A sibling lane has identified two alternative Cramer
  packets whose specialized Cofactor rows remain nonzero (2,370 and 3,197
  terms); their two-prime/unit tests were still pending at this report.
- On the generic open branch `(b1-d1)*(d1^2*x-1) != 0`, the exact conditions
  are `L=0` plus the fifteen fraction-free minor determinants.  Their large
  factors have 2,588--3,985 terms and are exported for targeted modular or
  exact branch work.  A bounded 60-second first-prime solve timed out and is
  explicitly not interpreted as a negative result.
- The earlier degree-267 finite-field inverses remain valid modular evidence
  for the larger false-component quotient, but are not promoted to a
  characteristic-zero unit here.

The determinant identities `g1*f0-g0*f1` are exact and division-free.  All
fifteen were factored over `Z`; every one contains the expected
`b1-d1`, `d1^2*x-1`, `x-1`, and `C` factors (with recorded multiplicities).

## Artifacts

- `audit_cofactor13_reduced_source.py` — independent literal source/Cramer
  replay.
- `build_cofactor13_b0_resultants_flint.py` — exact `Q,G` resultant and
  factorization.
- `cofactor13_qg_resultant_large_factor.txt` — exact 3,152-term `L`.
- `build_cofactor13_b0_minor_determinants_flint.py` and
  `cofactor13_b0_minor_large_factors.jsonl` — all fifteen exact determinants.
- `export_cofactor13_h_branch.py` — exact two-variable branch reduction.
- `certificate_cofactor13_h_branch_live_power.json` — exact source lift.
- `build_cofactor13_h_branch_certificate.py` — independent replay and
  mutation check.
- `results_three_mode_replay.json` — standard, `-O`, and `-I -S` replay;
  logical SHA
  `e66de105875e7b43e7029ff6c66cbe94cec026ea250d20d912cabc0896de4f4f`.

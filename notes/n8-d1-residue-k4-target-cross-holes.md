# N=8 D1: the target-cross residue obstruction

Suppose one residue edge block is supported only on its target cross:

```text
F00=F01=F10=F11=0,
F02,F12,F20,F21 != 0,
```

with `F22` arbitrary.  If the four adjacent edge blocks are full and the
opposite block `A` has one localized off-target entry, residue purity is
impossible over every field.  Boundary cells play no role.

Write

```text
H_kl = F_kl*A + b_k tensor e_l + c_l tensor d_k.
```

The four zero non-target slices synchronize common nonzero lines `u,v`:

```text
b_k=beta_k*u,       d_k=theta*beta_k*v,
c_l=gamma_l*u,      e_l=-theta*gamma_l*v       (k,l=0,1).
```

The `k2` and `2l` zero slices, whose four `F` coefficients are localized,
make both

```text
S=u tensor e2+theta*c2 tensor v,
T=theta*b2 tensor v-u tensor d2
```

nonzero scalar multiples of `A`.

If `(u,c2)` and `(v,e2)` are both independent, comparing the two rank-two
pencils gives

```text
b2=x*u+y*c2,        d2=theta*x*v-y*e2.
```

Consequently

```text
b2 tensor e2+c2 tensor d2=x*S,
```

so the target slice `H22` is a scalar multiple of `A`.  Its localized
off-target entry prevents equality to `E22`.

If `c2` lies on `u`, then `S`, `A`, and (by `T` proportional to `S`) `b2`
have common left factor `u`; the entire target slice has that factor.  Since
`u` has full support it cannot be `E22`.  The case `e2` on `v` is the
transpose-symmetric common-right-factor argument.  These cases exhaust the
rank split.

The identities are polynomial over `Z`; only the line synchronization and
rank split pass to the fraction field of a localized integral domain.  The
argument is therefore characteristic-free and is suitable for uniform
descent after localization.

The exact checker
[`verify_n8_d1_residue_k4_target_cross_holes.py`](../computations/verify_n8_d1_residue_k4_target_cross_holes.py)
reconstructs the maximal `213`-cell (`50/54` residue) representative, checks
all `8,100` support fibres and the exact `41` localized hypotheses, and
verifies the independent and both dependent tensor identities coefficient
by coefficient.

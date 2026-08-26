# Carrier site-colour torus covariance

Status: **exact covariance PASS; unstratified no-cap locus is not closed**.

For the site-colour torus

```text
A_uv[i,j] -> lambda_(u,i) lambda_(v,j) A_uv[i,j],
```

the three pure Hafnians have characters
`product_s lambda_(s,c)`.  The pure-normalization-preserving subtorus is
therefore cut out by these three products being one and has dimension 21.

For a carrier pair `(p,q)`, response row `r=(ab:alpha,beta)`, and column
`ij`, put

```text
rho_r     = lambda_(a,alpha) lambda_(b,beta),
kappa_ij  = lambda_(p,i) lambda_(q,j).
```

Both literal response summands have character `rho_r kappa_ij`, hence

```text
L(lambda.A) = D_rho L(A) D_kappa.
```

Thus rank is invariant and kernels transform by `K -> D_kappa^-1 K`.
The three diagonal blockers `K_dd` have character `kappa_dd^-1`, while
`<K,A_pq>` is invariant.  All four blocker-membership and activity
conditions are torus invariant.

Every carrier minor is a semi-invariant.  An `L` minor on rows `R`, columns
`C` scales by `product_R rho * product_C kappa`.  An augmented diagonal
blocker minor has the additional factor `kappa_dd^-1`; an augmented direct
blocker minor has the same factor as the corresponding `L` minor.

## Closedness guard

`rank(L)<=r` is closed and torus invariant.  On `rank(L)=r`, blocker
membership is imposed by augmented `(r+1)`-minors, but the nonzero `r`-minor
condition makes the branch only locally closed.  The union over ranks is not
closed in general, even after pure normalization.

An exact source-coordinate curve proves this.  Set

```text
A_01[c,c]=A_23[c,c]=A_45[c,c]=A_67[c,c]=1  for c=0,1,2,
A_16[0,0]=1,
A_27[0,0]=t,
```

and every other cell to zero.  All three pure Hafnians equal one.  For the
star carrier `(67, centre 0)`, at `t!=0` the response rowspace is
`span(K00)`, so the memberships are `[true,false,false,false]`.  At `t=0`,
the response matrix is zero and all memberships are false.  Hence the K00
branch, and the four-blocker no-cap union, specializes out at the rank drop.

Hilbert--Mumford arguments may use the torus weights only after retaining
the rank strata or declaring a specific closure; the raw no-cap membership
union is not a closed torus-stable target.

## Replay

```sh
python3 computations/unaudited-codex-carrier-torus-covariance-2026-08-21/audit_carrier_torus_covariance.py --write-results
python3 -O computations/unaudited-codex-carrier-torus-covariance-2026-08-21/audit_carrier_torus_covariance.py --write-results
python3 -I -S computations/unaudited-codex-carrier-torus-covariance-2026-08-21/audit_carrier_torus_covariance.py --write-results
```


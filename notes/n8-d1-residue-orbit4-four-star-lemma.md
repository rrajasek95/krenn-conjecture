# O4 downsets: the z-optional four-star lemma

The maximal O4 six-site proof does not need the direct boundary edge.  Over
any field of characteristic different from 2, it needs only four
boundary-star units and the four residue units supporting the injective
tripod minor.

For one boundary pair `(u,v)` and boundary colors `(a,b)`, write `P,Q` for
the two boundary-to-residue stars.  The support-faithful antecedent is

```text
P7_0, Q7_0, P6_0, P4_0,
x46_00, x47_02, x57_02, x45_00.
```

The last four cells certify

```text
det(Phi minor)=alpha0^5*c0^2*e0^2*A45_00^2 != 0.
```

No direct cell `x_uv_ab` is assumed nonzero.

The two non-target site-7 equations are

```text
P7_l*Phi(Q)+Q7_l*Phi(P)=0, l=0,1.
```

If their 2-by-2 determinant is nonzero, injectivity gives `P=Q=0`, contrary
to `P4_0`.  Otherwise `rho=Q7_0/P7_0` is a unit, the color-1 equation gives
`Q7_1=rho*P7_1`, and injectivity gives `Q=-rho*P`.  The complete matching
tensor reduces, with arbitrary `w` (possibly zero), to

```text
w*E222+tau*Phi(P)-2*Psi(P)=0.
```

If `tau!=0`, the `P6_0` slice writes `A45` as a sum of
`P4 tensor e` and `c tensor P5`.  Substitution in

```text
E22=A45+b tensor e+c tensor d
```

is impossible after quotienting the first factor by `<c>`: it would force
the full vector `e` to be the target line.

If `tau=0`, invertibility of 2 and `P6_0` give

```text
P4 tensor e+c tensor P5=0.
```

Since `P4_0` is a unit, `P4=kappa*c`, `P5=-kappa*e` with `kappa!=0`.  The
target slice is

```text
w*E22+2*kappa^2*c tensor e=0,
```

again impossible modulo `<c>`.  This is why `w`, hence the direct boundary
edge, is optional.

There are eight injectivity charts, not just the displayed `000` chart:

```text
det(i,j,k)=(-1)^(i+j+k) alpha_k^5*c_i^2*e_j^2*A45_ij^2,
                                               i,j,k in {0,1}.
```

Either non-target coordinate at site 7 can define `rho`.  The checker hence
emits 192 clauses: 12 boundary-color transports times 8 minor charts times 2
site-7 ratio coordinates.  This prevents a downset from evading the lemma by
deleting a single residue-minor witness.

The exact checker

```text
computations/verify_n8_d1_residue_orbit4_four_star_lemma.py
```

reconstructs the raw 81-coefficient matching reduction, all eight injectivity
minors, both scalar branches, and all 192 transports over W1/W2 and their
boundary colors.  Each transport emits the eight-cell negative support clause
used by the downset CEGAR.

Reproduce with:

```bash
.venv/bin/python computations/verify_n8_d1_residue_orbit4_four_star_lemma.py
.venv/bin/python -O computations/verify_n8_d1_residue_orbit4_four_star_lemma.py
```

Frozen ledger SHA-256:
`2faf9ed3e4711e90e86b6b1a771e41a5ec59e177abc343557f36e67cb66487f9`.

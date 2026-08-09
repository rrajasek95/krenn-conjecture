# D1 O4: exact six-site closure after the four omissions

The last maximal residue orbit O4 has a genuine residue family, but its
four-boundary-omission full frontier is empty.  The proof uses only residue
purity and the `W1={0,2,4,5,6,7}` six-site equations; it is valid over every
field.

The exact checker is

```text
computations/verify_n8_d1_residue_orbit4_six_site_closure.py
```

It reconstructs the 193-cell support, checks all 8,100 support fibres, freezes
the 4,969-generator input, and verifies every tensor identity below.

## O4 residue normal form

Write `t=e2` and name the residue blocks

```text
A=A45, B=B46, C=C47, D=D56, E=E57, F=F67.
```

The checked O4 family from `07f800a`, in the gauge `F67_22=1`, is

```text
C=c tensor t,       E=e tensor t,       F=t tensor t,
B[:,0]=alpha0*c,    B[:,1]=alpha1*c,    B[:,2]=b,
D[:,0]=-alpha0*e,   D[:,1]=-alpha1*e,   D[:,2]=d,
A=t tensor t-b tensor e-c tensor d.
```

The entries `alpha0,c0,e0,A00` are units on the O4 maximal torus.  For the
tripod map

```text
Phi(X,Y,Z)=X tensor D+B tensor Y+A tensor Z,
```

the checker computes the exact 9-by-9 minor on tensor-coordinate rows

```text
0,1,2,3,6,9,18,24,26
```

and obtains

```text
det = alpha0^5*c0^2*e0^2*A00^2.
```

Thus `Phi` is injective using only named localized cells, in every
characteristic.

## Boundary reduction

Fix boundary colors `(site0,site2)=(0,0)`.  Let `P_r` and `Q_r` be the three
entries on the edges from sites 0 and 2 to residue vertex `r`, and put
`z=x02_00`.  Every entry of these vectors and `z` is localized.

Look first at residue-site-7 colors 0 and 1.  Since the three O4 blocks
incident to vertex 7 are target-column supported, the two slices are

```text
P7_l*Phi(Q)+Q7_l*Phi(P)=0,  l=0,1.
```

If the two non-target projections of `P7,Q7` are independent, injectivity of
`Phi` gives `P=Q=0`, contrary to localization.  Otherwise, for a unit `rho`
and some scalar `tau`,

```text
Q_r=-rho*P_r (r=4,5,6),
Q7=rho*P7+rho*tau*t,
z=rho*w,
```

where `w` is a unit.  Substitution in all 81 coefficients reduces the whole
six-site tensor to

```text
w*t^3 + tau*Phi(P) - 2*Psi(P) = 0,
```

with

```text
Psi(P)=P4 tensor P5 tensor t
      +P4 tensor e  tensor P6
      +c  tensor P5 tensor P6.
```

## The two scalar branches

If `tau` is nonzero, the color-0 slice at site 6 is

```text
tau*P6_0*A
 =(tau*alpha0+2*P6_0)*P4 tensor e
 +(2*P6_0-tau*alpha0)*c tensor P5.
```

Since `tau` and `P6_0` are units, `A=L(P4 tensor e)+M(c tensor P5)` for two
scalars `L,M`.  Substitute this in the residue identity

```text
t tensor t=A+b tensor e+c tensor d.
```

It writes

```text
t tensor t=u tensor e+c tensor v.
```

Quotient the first factor by the line `<c>`.  The class of `t` is nonzero
because `c0` is a unit, so equality of the remaining nonzero decomposable
tensors forces `e` parallel to `t`.  This contradicts the localized entry
`e0`.

If `tau=0`, characteristic 2 immediately leaves `w*t^3=0`.  Outside
characteristic 2, the color-0 slice gives

```text
P4 tensor e+c tensor P5=0,
```

so `P4=kappa*c` and `P5=-kappa*e`.  The target slice then becomes

```text
w*t tensor t+2*kappa^2*c tensor e=0,
```

which is again impossible after quotienting the first factor by `<c>`.

This closes both boundary-projection branches and every characteristic.

## Scope and remaining downset issue

Together with the four pure-fibre factors in `07f800a`, the exact maximal O4
full-support chart is closed: if one of

```text
x02_20, x02_21, x13_20, x13_21
```

is present, the pure lift is a unit certificate; if all four are absent, the
six-site proof above applies.

This is not yet an automatic closure of every support below O4.  The six-site
argument localizes 25 boundary/W1 cells; a smaller support can omit one of
them and enter a projection-degenerate branch.  Closing those degenerations,
or proving that they transport to the other residue atoms, is the remaining
downset-completeness task.

## Reproduction

```bash
.venv/bin/python computations/verify_n8_d1_residue_orbit4_six_site_closure.py
.venv/bin/python -O computations/verify_n8_d1_residue_orbit4_six_site_closure.py
```

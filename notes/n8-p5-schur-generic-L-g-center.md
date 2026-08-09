# P5 finite-Schur recovery of the generic-L monic G center

The source-faithful finite first-Rees equations recover the third generic-L
bend equation after the exact 207-row Schur graph.  The checker is
`computations/verify_n8_p5_schur_generic_L_g_center.py`.

## Localized coordinate

Repeated substitution of `b^-1` is kept finite by making the exact coordinate
change

```text
b = z44+z45,   z45 = b-z44,   q=b^-1.
```

Every monomial is reduced by `b*q=1` as it is formed.  This is a polynomial
change followed by localization, not a modular or truncated normal form.  In
these coordinates the 196 identity-leading normal rows and eleven transverse
rows solve exactly through graph order six.  All transverse residuals are
zero.  The 28 nonpivot compatibility families have total term counts

```text
0, 0, 10, 165, 1590, 11102
```

at graph orders one through six.

## Third-bend center

With `r3=z46^(3)`, the recovered 14-term equation is

```text
G = z0*z26*z30*z54 - z26*z30^2*z54
  + z0*z7*z46*z54 - z7*z24*z46*z54 - z7*z30*z46*z54
  - z0*z26*z52*z54 + z26*z30*z52*z54
  + z7*z46*z52*z54 + z7*z26*z54^2
  - s*z0*z52 + s*z7*z54 - t*z0 - t*z52 - r3.
```

Thus `dG/dr3=-1` is a unit.  Exact characteristic-zero Singular reduction
modulo the already certified localized ideal

```text
<L,F1,F2,b*q-1,z11*w-1,z16*p16-1,z41*p41-1>
```

leaves nonzero normal forms in rows 30 and 33, of 42 and 28 terms.  The checker
certifies the source-level congruences

```text
Q30 = -1/2*z11*z16^2*z41*(z26+b-z44)*G,
Q33 =  1/2*z11*z16^2*z41*(z44-z26)*G.
```

After adjoining `G`, all 26 nonzero order-six compatibility rows reduce to
zero and the localized ideal remains nonunit.  The frozen ledger SHA-256 is
`46d107934702ade1987b9dea48db7242eadfcfb87e1c6897dc3ee2e183dcc15e`.

This proves the source Schur center through graph order six.  Monicity of this
one `G` row is the expected Hensel pivot, but it does not by itself prove that
the same triangular recurrence controls every later bend.  A filtered
all-order lemma and full scalar or conormal membership of `H0,H1` remain open.

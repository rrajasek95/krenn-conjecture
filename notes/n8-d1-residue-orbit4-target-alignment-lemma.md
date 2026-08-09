# O4 downsets: the target-alignment lemma

The first genuine degeneration below the injective O4 four-star charts is
not a rank drop of the tripod map.  It is a target-line alignment.  In the
O4 residue family, suppose

```text
e=eta*e2,       eta != 0.
```

Then `E57` is target-supported and the non-target corner of `D56` vanishes.
The tripod map remains injective: for `i,j,k in {0,1}` the checker exhibits

```text
det(i,j,k)=(-1)^(i+j+k)*alpha_k^3*c_i^4*d_j^4.
```

Fix one six-site boundary pair and colors, and write `P,Q` for its two
boundary stars.  If the direct boundary cell is absent, the two site-7
non-target equations and tripod injectivity reduce the dependent branch to

```text
tau*Phi(P)-2*Psi(P)=0.
```

The branch `tau=0` already has the localized monomial coefficient
`-2*c_i*P5_j*P6_k`.  For `tau!=0`, put `mu=2/tau`.  Quotienting the third
factor by the target line first shows that either the non-target projections
of `P6` and `alpha` are independent, which immediately forces a localized
star coordinate to vanish, or

```text
P6_bar=kappa*alpha_bar.
```

Writing the two remaining quotient scalars as `L,N`, the exact coefficients
force `L=N`.  Away from `kappa*mu=+/-1`, the checker verifies the ordinary
polynomial identity

```text
3*kappa^2*mu*T-Q*E
 = c*(L-Z*eta)^2*(kappa*mu-1)*(kappa*mu+1).
```

Thus `L=Z*eta`; the non-target equation `E=0` then makes the chosen
localized coordinate of `P4` zero.  At `kappa*mu=1`, the other quotient
forces a localized coordinate of `d` to vanish.  At `kappa*mu=-1`, a second
checked identity is

```text
3*Tminus-Qminus*Eminus=2*c*(Z*eta+kappa*r)^2,
```

and again `Eminus=0` forces the chosen coordinate of `P4` to vanish.  This
proves emptiness in characteristic different from `2,3`.  Swapping residue
sites `4,5` gives the symmetric `c`-target branch.

The exact checker

```text
computations/verify_n8_d1_residue_orbit4_target_alignment_lemma.py
```

reconstructs the eight aligned tripod minors, the reduced tensor coefficient,
both scalar elimination identities, and 384 support-faithful clauses.  Each
clause has two positive alignment escapes, one positive direct-edge escape,
and eight negative localized witnesses; it therefore makes no downward
monotonicity assumption.

Frozen ledger SHA-256:
`1b869666b0b59178b6d3fd5b9122c5df6de25a349fae08dc44ccf7b57180ec19`.

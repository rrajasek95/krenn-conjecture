# N=8 P5 source-faithful generic-L F1 center

## Exact result

The finite first-Rees matching equations recover the known generic-L
first-bend relation after the 207-row Schur elimination.

The checker
`computations/verify_n8_p5_schur_generic_L_f1_center.py` lets the P5 base
coordinate $z_{46}$ bend as

$$
z_{46}(\tau)=z_{46}+\tau s+\tau^2t
$$

and solves the full 196 normal and eleven transverse pivot equations through
four graph orders.  Every coefficient is obtained from the original finite
source polynomials by the identity/$bI_{11}$ triangular solves.  Reduction
modulo

$$
L=z_9z_{25}-z_{11}z_{46}
$$

gives zero mixed remainders through graph order three.  At graph order four
only Q30 and Q33 remain, and they factor as

$$
Q_{30}=\frac12z_{16}^2z_{41}(z_{26}+z_{45})F_1,
$$

$$
Q_{33}=\frac12z_{16}^2z_{41}(z_{26}-z_{44})F_1,
$$

where

$$
F_1=-z_9z_{29}z_{44}+z_0z_{11}z_{46}
-z_{11}z_{24}z_{46}+z_{11}z_{26}z_{54}+s z_{11}.
$$

On the dense chart $z_{16}z_{41}z_{11}(z_{44}+z_{45})\ne0$, the equation is
monic in the first bend $s$.  It therefore supplies the next exact
Weierstrass/Schur row in the component-local quotient.

The frozen characteristic-zero ledger has SHA-256
`f26fd19f3500b1770996ec6446319120eb003d1d5d20aebe08d57bba910b0ef5`.
Its $F_1$ polynomial has SHA-256
`471760887a6532d6bc1022886f1451d742e443b7ddf991d25f8e4cf6106f92d2`.

## Scope and next step

This is a direct finite-source derivation of $F_1$, rather than a replay of
the older projected compatibility tail.  Together with the preceding $L$
checker it establishes the first two generic-L centers inside the exact
Schur quotient.

It does not yet recover the second-bend relation $F_2$, the later monic $G$
row, or H0/H1 membership.  The next graph coefficient requires the localized
$b^{-1}$ transverse solve; its compatibility numerator should recover the
known pair of second-bend relations.  After adjoining $F_2$ and $G$, scalar
or Kahler-conormal reduction of the two pure germs becomes component-local
and decisive.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_p5_schur_generic_L_f1_center.py
python3 computations/verify_n8_p5_schur_generic_L_f1_center.py
```

All arithmetic is exact over the rationals.

# N=8 P5 source-faithful Schur recovery of the L center

## Exact result

The finite first-Rees source equations, reduced by the certified 207-row
normal/transverse Schur block, recover the previously found P5 degree-six
compatibility center without importing any precomputed compatibility tail.

The checker
`computations/verify_n8_p5_schur_degree6_center.py` solves the full 207-row
formal graph coefficient by coefficient over the 45-variable P5 base.  The
new coefficients enter through the exact identity and
$bI_{11}$ Jacobian blocks, so every solve is triangular.  The first two graph
orders have no residual mixed equation.  At graph order three exactly rows
30 and 33 survive, with

$$
g_{30}=-\frac12z_{16}^2z_{41}
 (z_9z_{25}-z_{11}z_{46})(z_{26}+z_{45}),
$$

$$
g_{33}=-\frac12z_{16}^2z_{41}
 (z_9z_{25}-z_{11}z_{46})(z_{26}-z_{44}).
$$

Their difference is $-\frac12b$ times the common core.  On the
$b=z_{44}+z_{45}\ne0$ chart,

$$
\langle g_{30},g_{33}\rangle:b^\infty
=\langle z_{16}^2z_{41}L\rangle,
\qquad L=z_9z_{25}-z_{11}z_{46}.
$$

Thus the three reduced components are $z_{16}=0$, $z_{41}=0$, and $L=0$.
The dense generic-L continuation localizes $z_{16}z_{41}z_{11}b$.

The frozen characteristic-zero ledger has SHA-256
`4ffd07f0c5c58d1b13c95f5c958d9edd7ab9ee32a92eba0a604aa233cd285009`.
The two nonzero graph-order-three polynomials contain four terms each; all
39 compatibility coefficients at graph orders one and two are exactly zero.

## Significance and next center

This closes the provenance gap between the finite 253-variable Rees export
and the older filtered P5 recursion: the $L$ center is now derived directly
from the original matching polynomials through an exact all-order Schur
coordinate block.

It is still an associated-graded saturation step, not full generic-L
membership.  The next source-faithful step is to impose the $L$ blowup
$L=\tau\lambda$, continue the same triangular graph, and recover the known
first-bend and second-bend relations (the old $F_1,F_2$ center), followed by
the monic $G$ relation.  Only after that component ideal is present is the
scalar or Kahler-conormal reduction of H0/H1 decisive.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_p5_schur_degree6_center.py
python3 computations/verify_n8_p5_schur_degree6_center.py
```

All arithmetic is exact over the rationals.

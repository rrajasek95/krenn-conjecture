# N=8 P5 finite Rees-chart affinity

## Exact structural result

The two newest variable blocks in the generic-$L$ P5 chart can be retained
without losing the source's multiaffine structure:

- the free bend $z_{46}$ is supported on four ambient cells, all incident to
  site 7;
- the eleven transverse P5 directions are supported on seventeen ambient
  cells, all incident to site 0.

A perfect matching uses exactly one edge at each site.  Consequently every
universal hafnian coefficient is affine in $z_{46}$ and collectively affine
in the entire eleven-variable transverse block.  Bend--transverse bilinear
terms can occur, but no square or same-block product can occur before a
solved strict-transform graph is substituted.

The exact checker is
`computations/verify_n8_p5_rees_chart_affinity.py`.  Its frozen ledger has
SHA-256
`c6e15e7b207f8bddca79fc4df50ce1d62b10f86b814a9cdaa5751f27a91780f0`.

## Literal supports

In the 252 translated ambient coordinates, the bend direction is

$$
z_{46}=-x_{27}^{02}-x_{27}^{12}+x_{37}^{02}+x_{37}^{12}.
$$

The first eight transverse directions are individual cells on edge $04$.
The last three have three-cell supports on edges $05$ and $06$.  Every one
of those seventeen cells contains site 0.  The bend and transverse supports
are disjoint.

The checker sweeps the actual universal matching-term constructor over all
$3^8=6561$ output words and all 105 perfect matchings per word.  Among the
688,905 terms it finds:

- 43,740 terms meeting the bend support;
- 185,895 terms meeting the transverse support;
- 16,524 terms meeting both supports;
- maximum degree one in the bend and maximum collective degree one in the
  transverse block.

## Consequence for the finite exporter

The newest bend and the eleven newest transverse variables should remain
independent variables in the finite Rees chart.  Substituting the solved
$c_7$ graph would mix the bend into other ambient cells and discard this
literal triangularity.  With them retained, the twelve selected source
strict transforms have the finite shape

$$
F_i=A_i(\tau,\text{old})+
       \sum_j B_{ij}(\tau,\text{old},r)y_j,
\qquad
G=C(\tau,\text{old},y)+D(\tau,\text{old},y)r,
$$

where there are no $y_jy_k$ or $r^2$ terms.  Their initial Jacobian is the
already certified block with determinant $-b^{11}$.  Thus eliminating the
newest variables is a finite linear/rational operation after localizing the
determinant, rather than an unbounded Hensel expansion in those variables.

This does not yet eliminate the 196 ambient-normal remainders or prove that
the 27 remaining mixed germs and H0/H1 lie in the twelve-generator ideal.
It removes one possible source of infinite growth and fixes the correct
exporter architecture: retain the two single-site blocks, export the finite
$\tau$ polynomials from the original degree-four matching equations, and
only then eliminate the monic variables.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_p5_rees_chart_affinity.py
python3 computations/verify_n8_p5_rees_chart_affinity.py
```

The audit is exact and uses only rational arithmetic and literal matching
enumeration.

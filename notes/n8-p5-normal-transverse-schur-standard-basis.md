# N=8 P5 normal/transverse Schur standard basis

## Exact all-order elimination block

There is a source-faithful local standard basis for the first 207 variables
of the finite P5 Rees chart.  It is obtained with two small polynomial
coordinate changes, not by expanding the full solved normal graph:

1. shift the 196 ambient-normal variables by their quadratic offsets
   $q_p(a)$ (192 terms in total);
2. shift the eleven P5-transverse variables by the already certified first
   correction $n^{(1)}(a)$ (seven terms in six variables).

Let

$$
A=\mathbb Q[a_1,\ldots,a_{45},b^{-1}],
\qquad b=z_{44}+z_{45},
$$

and use the local order with the 196 normal variables first, the eleven
transverse variables second, and $\tau$ last.  After the two shifts every
full divided normal generator has local linear part

$$
y_p+\tau c_p(a).
$$

The 196 initial monomials are therefore the distinct variables $y_p$.
For the eleven committed obstruction pivot rows, exact full-row operations
by these normal generators remove every $y$-linear term.  Their local linear
parts are

$$
b n_j+\tau d_j(a).
$$

After multiplying by the unit $b^{-1}$, their initial monomials are the
eleven distinct variables $n_j$.  All 207 initial monomials are pairwise
coprime.  Buchberger's product criterion (valid here for these monic rows
over $A$) proves that the selected **full strict transforms**, not merely a
fixed-order truncation, form a local standard basis.

The exact checker is
`computations/verify_n8_p5_normal_transverse_schur_basis.py`.  Its frozen
characteristic-zero ledger has SHA-256
`6d793205d5f727d4aed253aa001b753a3b9faf0fdf694406c26f738fc1ec5636`.
Its optional generic-$b$ Singular export is 53,767,927 bytes with SHA-256
`ae1be4fa4fc3034a5f5695d5db37d7a3db2542445a88731ada0f1db9697727e8`.
Singular 4.4.1 parses the characteristic-zero export and certifies `std(S)`
has exactly 207 rows with endpoint leads $y_9$ and $n_{23}$.

## Sizes

The shifted source map has only 635 terms among its 252 coordinate forms,
with at most eleven terms in one coordinate.  The complete standard-basis
blocks are:

| block | rows | terms | largest row |
|---|---:|---:|---:|
| ambient normal | 196 | 822,693 | 20,754 |
| transverse pivots after exact normal row operations | 11 | 179,275 | 33,851 |

The normal family hash is
`e2da946b3ae23cfc3dbbad02c4a99a8c0dcd31aa065a151a8c555cb3c53dd0a9`;
the transverse family hash is
`09e7f567f4da55babe9dc9c9e8da5adff0b6395c2591fa4f6663ae0b1f205650`.

This eliminates 196 ambient normals and eleven P5-transverse variables by
a certified Schur/Mora block.  The unsolved quotient has 46 variables: the
45 P5 base coordinates and $\tau$.  Its remaining inputs are the 28
nonpivot mixed germs plus H0 and H1.  Before weak normal reduction, the
shifted H0 and H1 targets have 4,068 and 7,119 terms respectively.

## What remains

This result proves the etale/triangular part of the intended promotion
theorem through the first P5 transverse graph.  It does not yet prove that
the 28 remaining mixed germs or H0/H1 reduce to zero, and it does not yet
perform the $\tau$-saturation and localization along the later dense
generic-L centers.  Unit Jacobians solve variables; they do not by
themselves kill functions on the resulting base.

The next computation should use this 207-row basis as a fixed rewrite
system, weakly reduce the 28 mixed germs and H0/H1, and only then follow the
known $L/F/G$ component inside the 46-variable quotient.  Expanding another
normal correction is unnecessary: the pairwise-coprime initial theorem is
already all-order.

A potentially smaller capstone is conormal rather than scalar reduction.
After the tau-saturated generic-$L$ component ideal $K_L$ of the 28 germs is
installed, test in its Kahler module whether

$$
dH_c\in\langle dK_L\rangle.
$$

In characteristic zero this makes $H_c$ constant on the dense irreducible
component; one exact zero basepoint then forces the full germ to vanish.
The committed strict-seven identity $dH_0=U\,dG$ is the first initial layer
of exactly this proposed certificate.  Performing the differential test
before constructing $K_L$ would ask for conormal membership on every
component at once, a stronger statement not implied by the P5 evidence.

Two modular reconnaissance attempts delimit the wrong implementation:

- a double-shifted 237 MB input gave `std(N)` with 196 rows in two seconds,
  but direct H0 reduction produced no remainder after five minutes, and
  `std(N,H0)` reached about 9 GB RSS before being stopped;
- the smaller one-shift 42 MB input gave the same 196-row basis in one
  second, but a normal-only H0 reduction still produced no remainder after
  three minutes (about 1.36 GB RSS).

These runs establish no membership or nonmembership result.  In particular,
normal-only reduction is not the right target because the known
cancellations also use the eleven mixed pivot equations.  The exact
207-row block above is the smallest certified input for the next reduction.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_p5_normal_transverse_schur_basis.py
python3 computations/verify_n8_p5_normal_transverse_schur_basis.py
.venv/bin/python computations/verify_n8_p5_normal_transverse_schur_basis.py \
  --singular /tmp/n8_p5_207_schur_QQ.sing
/usr/local/bin/Singular -q /tmp/n8_p5_207_schur_QQ.sing
```

The proof checker uses exact rational arithmetic; the modular runs are
reported only as performance reconnaissance.

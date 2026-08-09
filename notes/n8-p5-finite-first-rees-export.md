# N=8 P5 finite first-Rees export

## Exact checkpoint

The first P5 strict transform can be exported directly from the original
degree-four matching equations without substituting any solved normal graph.
In 253 variables the source map is

$$
X_i=\tau T_i(a+\tau n)+\tau^2D_i(y),
$$

where $a$ consists of the 45 P5 tangent coordinates, $n$ consists of the
eleven tangent directions transverse to P5, and the 196 variables $y_p$ are
the exact ambient-normal directions dual to the echelon Jacobian rows.  The
P5 relation $z_{15}=z_{16}$ is imposed in the leading tangent term and
$z_{15}-z_{16}$ is retained among the eleven transverse variables.

The exact exporter and checker is
`computations/analyze_n8_p5_finite_rees_chart.py`.  Its complete ledger has
SHA-256
`3952965184121360b4f0137715233f51b4a9377b87f0766499c087619efdcf84`.
The generated 10,587,036-byte Singular input has SHA-256
`40eef6843e77706aba2b6b15655743f90adbbbc7350df31bed5ff685912a83db`
and parses under Singular 4.4.1.

## A finite degree bound

Every substituted ambient coordinate has only $\tau$-degrees one and two.
The 196 normal and 39 obstruction source generators have degree at most four;
the nine compact tangent-cubic combinations have degree at most five.
Consequently their substituted $\tau$-degrees are bounded by eight, eight,
and ten before strict division.  The exact valuations and resulting bounds
are:

| group | count | valuation | maximum strict $\tau$-degree |
|---|---:|---:|---:|
| ambient normal | 196 | 2 | 6 |
| obstruction | 39 | 3 | 5 |
| tangent cubic | 3 | 4 | 5 |
| tangent cubic | 6 | 5 | 5 |

The two pure residual targets
$H_c-M_c$, where $M_c$ is the already selected mixed coefficient for colour
$c$, both have valuation three and strict $\tau$-degree five.  Their strict
transforms have respectively 788 and 3,015 terms.  Since $M_c$ belongs to the
full mixed ideal, membership of $H_c-M_c$ is sufficient for membership of
$H_c$.  A nonzero remainder modulo only the selected 244-generator subideal
would not by itself be a counterexample; it would first have to be checked
against all mixed generators.

Thus the Rees input is a genuinely finite polynomial problem.  This bound
does **not** say that a truncated Hensel substitution is enough: solving the
normal graph can still produce an infinite $\tau$-series.  It says that a
finite saturated/localized ideal or standard-basis computation can decide
the full source problem without manufacturing further source jets.

## The 196-variable Schur block

For every divided normal generator the checker extracts its complete
$\tau=0$ dependence on the normal variables and verifies exactly

$$
\overline N_p=y_p+q_p(a)+\tau R_p(a,n,y,\tau).
$$

No other $y$ variable and no transverse $n$ variable occurs at $\tau=0$.
Hence the $196\times196$ $y$-Jacobian is exactly $I_{196}$ modulo $\tau$.
Over the $\tau$-adic completion, and after any of the generic-L
localizations, the formal implicit-function theorem gives a unique normal
graph.  The normal generators are a regular sequence, $\tau$ stays regular
in their quotient, and the normal block should be removed by
Schur/Hensel elimination rather than by a 253-variable brute-force
Groebner basis.  As a first check on the quotient, the $\tau=0$ normal
remainders of both exported pure targets are exactly zero.

The same elimination sends the 39 obstruction initials to only 109 terms
(at most six in any row; family SHA-256
`ae308372053f1da44815787ab1eb554e3539a28d5a9874835ae8eb5ad0ebbddb`).
They are collectively affine in the eleven transverse variables, and their
eleven committed pivot rows have exact Jacobian

$$
(z_{44}+z_{45})I_{11}.
$$

Thus the exporter source-faithfully recovers the first triangular P5 block;
on the $b=z_{44}+z_{45}\ne0$ chart these eleven variables can be eliminated
immediately after the ambient normals.

## Intended promotion theorem and remaining calculation

Let $I^{\mathrm{sat}}$ be the $\tau$-saturation of this finite ideal, completed
and localized along the dense generic-L infinitely-near component

$$
z_{16}z_{41}z_{11}(z_{44}+z_{45})\ne0.
$$

The intended all-order promotion has two finite stages:

1. eliminate the 196 normal variables using the identity Schur block;
2. in the localized strict-transform quotient, select the eleven transverse
   pivots and the monic bend equation $G$.

The committed strict-seven calculation proves that the second block has
Jacobian determinant $-(z_{44}+z_{45})^{11}$ at its initial layer.  If the
finite localized quotient promotes this to a twelve-variable
etale/triangular graph, then exact reduction of the remaining 27 mixed germs
and of the two exported pure targets is decisive.  Zero reductions prove
full completed-local membership on the dense generic-L P5 chart.  A nonzero
pure reduction locates the first all-order survivor and must then be tested
for simultaneous H0/H1 nonvanishing and algebraization.

That last saturation/localized reduction is not performed here.  In
particular, the unit Jacobians prove formal solvability of the 208 selected
variables but do not alone force the remaining mixed or pure germs to
vanish.  The smallest missing artifact is a component-local Schur reducer
for the finite exported ideal: first represent the 196 normal quotient
implicitly, then saturate/localize the resulting 57-variable system along
the already known P5/L/F/G valuation.  This avoids the ambient Mora
calculation that previously crossed the memory frontier.

## Reproduction

```sh
.venv/bin/python computations/analyze_n8_p5_finite_rees_chart.py --quiet --summary
.venv/bin/python computations/analyze_n8_p5_finite_rees_chart.py \
  --quiet --summary --singular /tmp/n8_p5_first_rees.sing
/usr/local/bin/Singular -q /tmp/n8_p5_first_rees.sing
```

The checker and export use exact rational arithmetic.

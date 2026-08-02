# Independent audit: the q-zero polynomial cube does not type its cap readout

## Outcome

The exact polynomial content of the q-zero calculation is correct and useful:

- all fifteen four-polars are the unit;
- their `pq`-direct and `pr`-two-star placements are correct;
- after reset, each internal matching sees exactly one of the fifteen odd
  denominator columns;
- the labelled rank is five and the matching-choice kernel has dimension ten;
- the four principal-parts derivatives commute, and the usual oriented
  four-cube signs square to zero; and
- the stabilizer weights first become trivial at the (q)-degree-zero
  fourth-order symbol; and
- Reynolds averaging gives the uniform duality \(L_v(h_s)=\delta_{vs}\).

The augmented readout proposed in the initial draft,

\[
             (\operatorname {boundary},\operatorname {target},
                    \operatorname {ores})=(1,0,0)       \tag{1}
\]

is not established.  The calculation constructs a polynomial
principal-parts coefficient equal to one and, in the equation-presentation
jet, a differentiated target equal to zero.  It defines neither a comparison
from that jet to the split-cap complex nor an ordinary-residue map on the
putative new cell.  During this audit the primary note and checker were
corrected: they no longer claim or output (1), and now mark the split-cap
typing as conditional.

Accordingly the corrected result is a canonical **associated polynomial
symbol**, not yet a denominator-attached cap chain.  The missing datum is
exactly the comparison/attaching map previously isolated in
[`h3-shifted-principal-parts-comparison-obstruction.md`](h3-shifted-principal-parts-comparison-obstruction.md).

## 1. Independently reconstructed polynomial identities

Keep \(D=\{1,2,3,4,5\}\), \(m=12112\), and
\(F_v=D\setminus\{v\}\).  Direct enumeration of the 90 matchings avoiding
the edge \(pr\) gives

\[
 \partial_{u_v}\partial_tH_v=h_v,
 \qquad
 \partial_N\partial_{u_v}\partial_tH_v=1              \tag{2}
\]

for every \(v\in D\) and all three
\(N\in\operatorname {PM}(F_v)\).
Every selected term contains \(pq\), so it is in the `pq`-direct sector; it
cannot contain \(pr\), so it is in the `pr`-two-star sector.

Independently rebuilding all fifteen reset columns gives

\[
 \partial_NP_m\delta(d_{s,a})=
 \begin{cases}
  1,&(s,a)=(v,m_v),\\
  0,&\text{otherwise},
 \end{cases}                                             \tag{3}
\]

before the common pure-output marker is restored.  Thus (3) really is a
complete no-leakage statement.  The fifteen choices map to five labelled
unit lines, giving rank five and kernel dimension ten.

For each of the six pairs of the four directions
\((u_v,t,N_1,N_2)\), direct differentiation in both orders gives the same
polynomial.  Separately, the cellular boundary of an abstract four-cube has
eight facets and 24 ridges, each ridge appearing twice with opposite sign.
These facts verify the ordinary principal-parts cube and its possible sign
convention.  They do not add a denominator or cap face to that cube.

The independent stabilizer calculation also agrees.  The three colour-sum
and five site-trace rows have rank seven.  Each degree-two face weight and
each degree-one edge-polar weight is nontrivial modulo those rows, while the
degree-zero weight is the colour-zero sum and hence trivial.  The five
initial face weights are independent in the quotient, and the displayed
mixed face word is the unique four-site word in each restricted character.

## 2. The uniform Reynolds lemma is genuine

For \(|D|=2r+1\), define

\[
 h_s=\sum_{M\in\operatorname {PM}(D\setminus\{s\})}q_M,
 \qquad
 L_v={1\over(2r-1)!!}
      \sum_{N\in\operatorname {PM}(D\setminus\{v\})}\partial_N. \tag{4}
\]

Then, over characteristic zero,

\[
                         L_v(h_s)=\delta_{vs}.           \tag{5}
\]

If \(s=v\), each of the \((2r-1)!!\) summands differentiates its own
matching monomial to one.  If \(s\ne v\), every matching \(N\) covers \(s\),
whereas no monomial of \(h_s\) contains an edge incident to \(s\); hence
every derivative is zero.  This proves (5) uniformly, not only in the finite
instances.  The independent checker reconstructs it through eleven odd
sites.

Equation (5) gives a canonical linear selector on the free face-polynomial
module.  It does not show that matching differences vanish in a physical
quotient, nor does it create a higher source generator.

## 3. Why the polynomial faces do not construct the attaching chain

The corrected primary note records the candidate shape

\[
       \mathsf J_{v,N}=[K_v;d_{v,m_v};u_v,t;e_1,e_2]    \tag{6}
\]

after observing that two polynomial faces agree, and now explicitly labels
it a candidate.  No chain module containing \(\mathsf J_{v,N}\), differential
on it, or comparison map from the chart principal-parts module to the odd cap
module is defined.  Equality of the two proposed faces is the compatibility
condition for attaching such a cell; it is not the attaching cell itself.

Likewise, the generic cubical sign calculation proves \(D^2=0\) for the
four commuting derivative directions.  The denominator generator is not
one of those four directions.  Choosing its sign so that one polynomial
term cancels does not verify the remaining squares of a combined
denominator/cap differential.

This distinction is now visible directly in the corrected primary checker.
Its records say

```python
"cap_boundary": "not constructed",
"ordinary_residue": "not defined",
```

and its later split-cap test still writes

```python
conditional_column = [kappa * y, Q(0), Q(0)]
```

but labels that block `Conditional typing only`.  There is no implemented
ordinary-residue map, comparison map, or augmented differential from which
that vector is obtained.  This is now a correctly scoped rank target rather
than claimed provenance.

## 4. Why the missing residue coordinate is decisive

The verified polynomial and equation-target data retain only the first two
coordinates of (1).  They cannot distinguish

\[
                  j=(1,0,0)
       \quad\text{from}\quad
                  \rho=(1,0,1).                         \tag{7}
\]

The latter is the existing ordinary-response column.  This is not merely a
formal ambiguity.  With the old split-cap columns

\[
 T=(-Y,1,0)^T,\qquad \rho=(1,0,1)^T,                   \tag{8}
\]

the two possible lifts of the same evidenced boundary/target pair behave
differently:

\[
 \begin{aligned}
 p_0&=(\kappa Y,0,0)^T,&
        \operatorname {rank}[T\ \rho\ p_0]&=3,\\
 p_1&=(\kappa Y,0,\kappa Y)^T=\kappa Y\rho,&
        \operatorname {rank}[T\ \rho\ p_1]&=2.
 \end{aligned}                                          \tag{9}
\]

Thus ordinary residue is precisely the coordinate deciding whether the
new direction exists.  It cannot be inferred from “presentation degree.”
The evaluated cap-multiplication warning in
[`site-occupancy-bockstein-partial-matching-flatness.md`](site-occupancy-bockstein-partial-matching-flatness.md)
is directly relevant: formal state/presentation splittings do not force the
evaluated cap Bockstein to vanish.

The physical target zero is narrower.  Positive differentiation of the
constant target coefficient of a mixed equation row is indeed zero inside
the equation-presentation principal-parts functor.  Transporting that zero
to the target coordinate of a split-cap column still belongs to the absent
comparison map.  No conclusion about ordinary residue follows from it.

## 5. Corrected scope and verification

What is genuinely functorial in the present enlargement is:

1. the strict two-chart polynomial principal-parts cube;
2. its sector-valued associated Rees symbol;
3. the differentiated reset-denominator support identity (3); and
4. the Reynolds selector (4).

What remains declared is:

1. a higher cell attaching the reset denominator generator to the chart
   cube;
2. a comparison taking the unit polynomial symbol to the normalized cap
   boundary \(w_v\);
3. commuting target and ordinary-residue augmentations, especially
   \(\operatorname {ores}(j_{v,N})=0\); and
4. the curvature factor converting the unit symbol to \(\kappa Y\) in that
   typed complex.

Run

```sh
.venv/bin/python computations/audit_h3_qzero_denominator_rees_four_cube_independent.py
```

The mathematical audit imports no primary implementation.  It reconstructs
the matchings, polars, sectors, reset support, derivative squares, cube signs,
stabilizer weights, ranks, and Reynolds matrices independently.  It also
checks the exact rank fork (9) and
audits the primary source text to ensure that the unsupported literal readout
has not returned, that the two missing maps remain explicit, and that the
remaining rank calculation is conditional.  Its terminal line is

```text
PASS with correction: polynomial four-cube valid, cap readout unproved
```

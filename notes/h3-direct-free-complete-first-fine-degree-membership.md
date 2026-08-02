# Complete first fine-degree membership for one direct-free face

Research obstruction and attack selection only.  This does not construct a
relative Hasse--Schmidt cell, close the unified overlap theorem, or prove
Krenn's conjecture.

## Outcome

Fix the distinguished direct-free face \(v=r=3\), so

\[
 x=0,\quad D=(1,2,3,4,5),\quad p=6,\quad q=7,
 \qquad F_3=(1,2,4,5),
\]

and use the mixed odd word \(m=12112\).  In the first squarefree fine degree

\[
 \lambda_3=e_{0,0}+e_{3,0}+e_{6,0}+e_{7,0}
 +\sum_{i\in F_3}(e_{i,0}+e_{i,m_i}),                 \tag{1}
\]

the complete strict polynomial membership problem has no solution.  Exact
sparse rational elimination gives

\[
 \operatorname{rank}C_{pq}=48,
 \qquad \operatorname{rank}[C_{pq}\ C_{pr}]=48,
 \qquad \dim\ker[C_{pq}\ C_{pr}]=48.                  \tag{2}
\]

The kernel has the explicit basis of the 48 componentwise \(pq-pr\) chart
comparisons.  Its complete common-coefficient ledger is zero; hence physical
target, the strict ordinary residue, every strict ordered landing, and every
other readout which descends from the global coefficient array vanish on the
kernel.  The desired invisible column

\[
 p_3=(h_3Y_0,\operatorname{tgt}=0,
             \operatorname{ores}=0,
             \operatorname{other}=0)                   \tag{3}
\]

raises the exact rank from \(48\) to \(49\).  Thus \(p_3\) is not in the
strict source image.

The important new point is a typing fact omitted by simply calling the old
48-column block “complete.”  All fifteen odd denominator columns were
included in the census, term by term.  Their \(\lambda_3\)-homogeneous pieces
are zero.  Therefore they add no same-degree source columns; concatenating
their raw matrices with \(C_{pq}\) would be an ill-graded membership problem.
The nonzero reset value \(h_3Y_0\) is a **degree-lowering** image, not a raw
denominator column in (1).  This precisely isolates the missing operation.

## Complete source census

The odd denominator presentation has columns

\[
 d_{s,a}\longmapsto e_a^{(s)}q^{[2]},
 \qquad s\in D,\ a\in\{0,1,2\}.                        \tag{4}
\]

The checker inspects all \(15\cdot81\cdot3=3645\) monomial terms.  A term
has one output-word slot at every odd site.  At each of the four sites met by
the matching in \(q^{[2]}\), it has a second copy of the same colour slot.
Degree (1) is squarefree in every site--colour slot, so no term of (4)
divides \(\lambda_3\).  Multiplication by a polynomial only increases fine
degree.  Consequently

\[
             (\operatorname{im}\delta)_{\lambda_3}=0.   \tag{5}
\]

This does not say that the reset defect vanishes.  The reset
\(12112\mapsto00000\) changes the output word and sends the one relevant
column to

\[
 d_{3,1}\longmapsto h_3Y_0,
 \quad h_3=q_{12}^{12}q_{45}^{12}
       +q_{14}^{11}q_{25}^{22}
       +q_{15}^{12}q_{24}^{21}.                         \tag{6}
\]

Equation (6) lies in (1) exactly because the reset replaces the duplicated
mixed output slots by zero slots.  Thus (6) is the desired column (3), not an
available source column.

For the EqSystem part, a word degree divides (1) precisely when it is zero
off \(F_3\) and chooses either \(0\) or \(m_i\) on every site of \(F_3\).
There are \(2^4=16\) words.  Its deficit is filled by a quadratic multiplier
precisely when the two multiplier edges form one of the three perfect
matchings of \(F_3\).  This gives all \(48\) columns in each chart, with no
omitted mixed row or multiplier.  Direct-freeness removes the same fifteen
global matchings from both presentations, so the two augmented column lists
are literally equal.

## Augmented rows and exact membership

The sparse matrix retains four types of output coordinate:

1. every monomial of every other full-nine boundary;
2. the whole common global-coefficient ledger, which dominates any one
   chosen strict residue/landing functional;
3. the physical target terms of the three pure-row columns; and
4. the selected cap-boundary summand containing (h_3Y_0).

The first three are common-chart rows.  One chart already has rank \(48\),
so doubling produces only the comparison kernel in (2).  The selected
summand is disjoint from all strict columns, while (3) is nonzero there;
hence the rank jump \(48\to49\).  This proves nonmembership together with
the exact kernel and readout statement, without evaluating at either of the
old rational guards.

If one formally adjoins the second-polar symbol

\[
 {\partial^2H_{01201200}\over
   \partial a_{03}^{00}\partial a_{67}^{00}}=h_3,       \tag{7}
\]

then (3) is present by definition and is unique modulo the 48 harmless chart
comparisons.  But ordinary differentiation is not source provenance.  The
mathematics still needed is exactly a relative/Rees or Hasse--Schmidt
transgression which promotes (7) to a genuine column while nullhomotoping
its lower terms.  The calculation shows that adding more strict rows in the
same degree cannot do this.

## Why this suggests the faster attack

The recurring difficulty is not discovering the scalar or the polynomial:
the correct \(h_3\), and after curvature contraction the correct
\(\kappa h_3\), are already forced.  The difficulty is changing homological
degree while retaining source provenance and simultaneous invisibility in
target and ordinary residue.  The shortest positive attack is therefore to
construct a functorial relative second-jet transgression for (7), rather
than search larger strict multiplier blocks or rely on guard
specializations.  A theorem of that type is genuinely new mathematics in
this proof architecture.

The dependency-free checker
[`verify_h3_direct_free_complete_first_fine_degree_membership.py`](../computations/verify_h3_direct_free_complete_first_fine_degree_membership.py)
performs the complete denominator census, exhaustive EqSystem source census,
and sparse exact rational rank computations.

Its frozen ledger digest is

```text
33c49461bead4c9069709b8174c6f953398dd5f7dccb2c71c45c4678e41fdbaa
```

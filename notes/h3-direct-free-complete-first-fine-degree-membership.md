# Complete first fine-degree membership for all five direct-free faces

Research obstruction and attack selection only.  This does not construct a
relative Hasse--Schmidt cell, close the unified overlap theorem, or prove
Krenn's conjecture.

## Outcome

Keep the direct-free chart fixed:

\[
 x=0,\qquad D=(1,2,3,4,5),\qquad p=6,\qquad q=7,
 \qquad r=3,\qquad A_{pr}=0,
\]

and use the mixed odd word \(m=12112\).  For every deleted face
\(v\in D\), put \(F_v=D\setminus\{v\}\) and

\[
 \lambda_v=e_{0,0}+e_{v,0}+e_{6,0}+e_{7,0}
 +\sum_{i\in F_v}(e_{i,0}+e_{i,m_i}).                  \tag{1}
\]

The complete strict polynomial membership problem has no solution in any of
the five degrees.  Exact sparse rational elimination gives, for every \(v\),

\[
 \operatorname{rank}C_{v,pq}=48,
 \qquad \operatorname{rank}[C_{v,pq}\ C_{v,pr}]=48,
 \qquad \dim\ker[C_{v,pq}\ C_{v,pr}]=48.              \tag{2}
\]

The kernel has the explicit basis of the 48 componentwise \(pq-pr\) chart
comparisons.  Its full common-coefficient ledger is zero, so physical target,
strict ordinary residue, strict ordered landing, and every other readout
descending from the global coefficient array vanish on the kernel.

This time the selected cap coordinate is not a fresh zero row.  Each of the
three pure-row multipliers in each chart has homogenized target
\(-M U_0\).  The strict same-power landing \(U_0\mapsto Y_0\) puts the same
coefficient \(-M Y_0\) in the selected cap row.  Thus six strict columns
actually hit that cap summand.  Nevertheless the target-zero desired column

\[
 p_v=(\operatorname{other}=0, h_vY_0,
      \operatorname{tgt}=0, \operatorname{ores}=0)     \tag{3}
\]

raises the exact rank from 48 to 49 for all five faces.  An explicit dual
certificate is “selected cap coefficient minus physical target
coefficient”: it vanishes on every strict column but has value one on each
of the three terms of (3).  Hence the rank jump expresses the
target--cap graph lock, not a disjoint-row tautology.

The all-face ledger is

\[
\begin{array}{c|c|c|c|c|c}
v&F_v&\#\text{ denominator terms}&
\operatorname{rank}C_{v,pq}&
\dim\ker[C_{v,pq}\ C_{v,pr}]&
\operatorname{rank}[C_{v,pq}\ C_{v,pr}\ p_v]\\ \hline
1&2345&3645&48&48&49\\
2&1345&3645&48&48&49\\
3&1245&3645&48&48&49\\
4&1235&3645&48&48&49\\
5&1234&3645&48&48&49
\end{array}                                             \tag{4}
\]

## All fifteen denominator columns

The odd denominator presentation has columns

\[
 d_{s,a}\longmapsto e_a^{(s)}q^{[2]},
 \qquad s\in D,\quad a\in\{0,1,2\}.                   \tag{5}
\]

For each \(v\), the checker inspects all
\(15\cdot81\cdot3=3645\) monomial terms.  A term has one output-word slot
at every odd site.  At each of the four sites met by the matching in
\(q^{[2]}\), it has a second copy of the same colour slot.  Degree (1) is
squarefree in every site--colour slot, so no term of (5) divides
\(\lambda_v\).  Polynomial multiplication only increases fine degree;
therefore

\[
                  (\operatorname{im}\delta)_{\lambda_v}=0
                  \qquad(v=1,\ldots,5).                 \tag{6}
\]

This does not say that the reset defect vanishes.  The reset
\(12112\mapsto00000\) hits the five columns \(d_{s,m_s}\) and sends them to
\(h_sY_0\).  These five images lie in the five distinct degrees
\(\lambda_s\).  Consequently, in the fixed degree \(\lambda_v\), exactly
one reset input remains:

\[
             d_{v,m_v}\longmapsto h_vY_0.               \tag{7}
\]

Thus all fifteen raw columns have been checked, while (7) is correctly
treated as the degree-lowering desired column rather than concatenated with
an ill-graded raw denominator matrix.

## Exhaustive EqSystem columns

A global word degree divides (1) precisely when it is zero off \(F_v\) and
chooses either \(0\) or \(m_i\) on each site of \(F_v\).  There are
\(2^4=16\) such words.  The deficit is filled by a quadratic multiplier
precisely when its two edges form one of the three perfect matchings of
\(F_v\).  Hence every face has exactly 48 columns in each chart, including
all 45 columns based on non-pure compatible words.

Direct-freeness always means deletion of the fixed block \(pr=\{6,3\}\),
not deletion of \(pv\).  It removes the same fifteen global matching terms
from both chart presentations.  Therefore the two complete augmented column
lists are equal, and the full-nine boundary alone already has the ranks and
kernel in (2).

The subgroup preserving the distinguished site \(r=3\) has the three face
orbits

\[
                         \{1,4\},\qquad\{2,5\},\qquad\{3\}. \tag{8}
\]

The computation includes representatives \(v=1,2,3\) and both partners,
without using a symmetry that changes the fixed chart.  It therefore
preserves the scope of the earlier corrected face-symmetry audit.

## The actual augmented differential and dual certificate

Let \(\ell=(w,M)\) denote one compatible word/multiplier column, let
\(C_v\ell\) be its complete full-nine polynomial boundary, and let
\(e_\ell\) be its global-coefficient ledger entry.  The strict augmented
map used by the checker is

\[
 \widehat d_v(\ell)=
 \left(
   C_v\ell,
   -{\bf1}_{w=0}M Y_0,
   -{\bf1}_{w=0}M U_0,
   e_\ell
 \right).                                               \tag{9}
\]

The coordinates are, respectively, every other full-nine boundary, selected
cap landing, physical target, and the complete common coefficient array.
The already-defined strict ordinary residue is a linear map of the final
coordinate, so retaining \(e_\ell\) is stronger than choosing a particular
formula for it.  The \(pq\) and \(pr\) copies of (9) are identical.

For a face matching monomial \(M\), define

\[
 \Phi_M(z)=[M Y_0]_{\rm cap}(z)-[M U_0]_{\rm tgt}(z).    \tag{10}
\]

Equation (9) gives \(\Phi_M\widehat d_v=0\) on all 96 strict columns.
On the desired column (3), \(\Phi_M(p_v)=1\) for each of the three
monomials \(M\) in \(h_v\).  This proves nonmembership directly.  Sparse
elimination independently records the same statement as

\[
 \operatorname{rank}\widehat d_v=48,
 \qquad
 \operatorname{rank}[\widehat d_v\ p_v]=49.            \tag{11}
\]

For zero indeterminacy, the full-nine boundary kernel is already the span of
the 48 chart comparisons.  Each comparison has zero target, zero cap
landing, and zero global-coefficient ledger.  Hence every descended strict
ordinary-residue functional vanishes there.  No guard specialization is
used anywhere in this argument.

## What mathematics is still missing

For each face the exact second polar is already known:

\[
 {\partial^2H_{c_v}\over
   \partial a_{0v}^{00}\partial a_{67}^{00}}=h_v.       \tag{12}
\]

Formally adjoining its cap column breaks the graph lock (10) and makes (3)
available, uniquely modulo the harmless comparison kernel.  Ordinary
differentiation, however, is not source provenance.  The genuinely new
mathematics is a relative/Rees or Hasse--Schmidt transgression promoting
(12) to a source-valid column while nullhomotoping its lower terms.  The
all-face result rules out the possibility that a different deletion face,
an omitted mixed row, a raw denominator multiplier, or fixed-chart symmetry
supplies that operation.

The dependency-free checker
[`verify_h3_direct_free_complete_first_fine_degree_membership.py`](../computations/verify_h3_direct_free_complete_first_fine_degree_membership.py)
supports `--face all` and the five individual face modes.  The frozen
digests are

```text
all  b8a19cac89473cd642521be9980a3d88130b31a05cb6b310631219b88a056174
1    d7418b6c20b53ec574feb679c94b99307c4d214fe05706a168b36c228d9292e7
2    ffc38f24925b1c36ef0a683597c70c5a2c575f1e46c3a31f97ca227f01c7458f
3    e1ff19a9a58059b4181202474e4eeee4eb724dbf8d05f85647954da371cdd192
4    3abff1adadbc065384bd2dca8fbf74e08a266ccbe9159c74d27c899987ef2017
5    6eb4b2d256bdabcfb27b68bb17a94e08cc223cd0765264740017bb4ada132f98
```

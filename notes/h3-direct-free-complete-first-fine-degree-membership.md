# Strict first fine-degree census for all five direct-free faces

Corrected research census and formal diagnostic only.  This note does not
reconstruct the physical cap differential or ordinary-residue formula, does
not decide the actual augmented membership of \(h_vY_0\), and does not prove
Krenn's conjecture.

## Corrected outcome

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

Three conclusions are literal.

1. All fifteen raw denominator columns were inspected term by term.  None
   has a component whose coefficient/output fine degree divides
   \(\lambda_v\), for any \(v\).
2. The complete strict EqSystem block in degree \(\lambda_v\) has 48
   columns in each chart and exact ranks

   \[
   \operatorname{rank}C_{v,pq}=48,
   \qquad \operatorname{rank}[C_{v,pq}\ C_{v,pr}]=48.  \tag{2}
   \]

3. The doubled boundary kernel is exactly the 48 componentwise
   \(pq-pr\) comparisons.  Their common global-coefficient ledger is zero,
   so any strict readout already known independently to factor through that
   ledger vanishes on the kernel.

The earlier version made two claims beyond this evidence.  They are now
withdrawn.

- The unshifted coefficient/output degree of \(h_vY_0\) has weight 9, not
  the weight-12 degree \(\lambda_v\).  Comparing it with (1) requires an
  explicit cap-module shift.
- The checker attached an equal cap coefficient to each pure target column.
  That is a useful formal graph model, but it was not reconstructed from a
  physical cap differential or ordinary-residue map.  Its rank
  \(48\to49\) is therefore conditional and is not an actual full-source
  membership theorem.

## 1. The complete raw denominator census

The odd denominator presentation has columns

\[
 d_{s,a}\longmapsto e_a^{(s)}q^{[2]},
 \qquad s\in D,\quad a\in\{0,1,2\}.                   \tag{3}
\]

For each \(v\), the checker inspects all
\(15\cdot81\cdot3=3645\) monomial terms.  A term has one output-word slot
at every odd site.  At each of the four sites met by the matching in
\(q^{[2]}\), it has a second copy of the same colour slot.  Degree (1) is
squarefree in every site--colour slot, so no term of (3) divides
\(\lambda_v\).  Multiplication by a polynomial only increases fine degree;
therefore the raw denominator presentation contributes no same-degree
column to this strict block.

This statement is independent of any cap-row shift.  It uses the literal
coefficient/output degree of each raw monomial and the componentwise
inequality with (1).

## 2. The reset degree and the missing module shift

The reset \(12112\mapsto00000\) hits the five columns \(d_{s,m_s}\) and has
formal output \(h_sY_0\).  Before assigning a degree to a cap-row basis,
its coefficient/output degree is

\[
 \bar\lambda_s=sum_{i\in D}e_{i,0}
              +\sum_{i\in F_s}e_{i,m_i},
 \qquad |\bar\lambda_s|=9.                              \tag{4}
\]

The full EqSystem degree has three additional endpoint slots.  If one
**declares** the cap-row module shift

\[
                  \sigma=e_{0,0}+e_{6,0}+e_{7,0},        \tag{5}
\]

then

\[
                         \sigma+\bar\lambda_s=\lambda_s. \tag{6}
\]

Under this explicit conditional convention, exactly the reset indexed by
\(s=v\) aligns with the fixed degree \(\lambda_v\).  Equations (5)--(6) are
a grading repair, not a construction of the shifted cap module and not
source provenance for a map sending \(d_{v,m_v}\) to \(h_vY_0\).  Without
such a declared module shift, the raw weight-9 reset image must not be called
a column in the weight-12 EqSystem block.

## 3. Exhaustive EqSystem boundary ranks

A global word degree divides (1) precisely when it is zero off \(F_v\) and
chooses either \(0\) or \(m_i\) on each site of \(F_v\).  There are
\(2^4=16\) such words.  The deficit is filled by a quadratic multiplier
precisely when its two edges form one of the three perfect matchings of
\(F_v\).  Hence every face has exactly 48 columns in each chart, including
all 45 columns based on non-pure compatible words.

Direct-freeness always means deletion of the fixed block \(pr=\{6,3\}\),
not deletion of \(pv\).  It removes the same fifteen global matching terms
from both chart presentations.  Sparse rational elimination on the literal
full-nine monomial boundaries gives (2), and hence

\[
 \ker[C_{v,pq}\ C_{v,pr}]
       =\{(a,-a):a\in\mathbb Q^{48}\}.                  \tag{7}
\]

This boundary calculation does not use either old rational guard.  The
subgroup preserving the distinguished site \(r=3\) has the three face
orbits

\[
                         \{1,4\},\qquad\{2,5\},\qquad\{3\}. \tag{8}
\]

The computation includes all three representatives and both partners, so
no symmetry changing the fixed chart is assumed.

The exact ledger is

\[
\begin{array}{c|c|c|c|c}
v&F_v&\#\text{ raw denominator terms}&
\operatorname{rank}C_{v,pq}&
\dim\ker[C_{v,pq}\ C_{v,pr}]\\ \hline
1&2345&3645&48&48\\
2&1345&3645&48&48\\
3&1245&3645&48&48\\
4&1235&3645&48&48\\
5&1234&3645&48&48
\end{array}                                             \tag{9}
\]

## 4. The formal graph-lock diagnostic

The checker retains a separate, explicitly formal model.  Let
\(\ell=(w,M)\) denote one compatible word/multiplier column, let
\(C_v\ell\) be its literal full-nine boundary, and let \(e_\ell\) record its
common coefficient.  The pure row has the literal homogenized target term
\(-MU_0\).  The diagnostic additionally **declares**, rather than derives,
an equal cap coordinate \(-MY_0\):

\[
 \widehat d^{\rm form}_v(\ell)=
 \left(
   C_v\ell,
   -{\bf1}_{w=0}M Y_0,
   -{\bf1}_{w=0}M U_0,
   e_\ell
 \right).                                               \tag{10}
\]

Inside this declared model, six columns per face hit the cap coordinate and

\[
 \Phi_M(z)=[M Y_0]_{\rm cap}(z)-[M U_0]_{\rm tgt}(z)    \tag{11}
\]

annihilates all 96 columns.  The formal target-zero vector with cap entry
\(h_vY_0\) is detected termwise by (11), and sparse elimination gives

\[
 \operatorname{rank}\widehat d^{\rm form}_v=48,
 \qquad
 \operatorname{rank}[\widehat d^{\rm form}_v\ p_v]=49. \tag{12}
\]

Equation (12) says only: **if** the physical augmented differential has the
declared common graph (10), then the target-zero cap vector is absent from
that model.  The checker does not derive the cap entry in (10), does not
reconstruct ordinary residue, and therefore does not establish (12) for the
actual augmented source complex.

The comparison kernel (7) does have zero common-coefficient ledger.  Thus an
ordinary-residue functional independently proved to descend through that
ledger has zero comparison indeterminacy.  That conditional factorization is
weaker than reconstructing its full formula here.

## 5. Correct scope and next step

For every face the exact second polar remains

\[
 {\partial^2H_{c_v}\over
   \partial a_{0v}^{00}\partial a_{67}^{00}}=h_v.       \tag{13}
\]

The present census proves that no strict one-chart syzygy was overlooked in
the first compatible EqSystem degree and that raw denominator monomials do
not enter it.  It does not prove that a physical cap landing obeys (10), and
it does not decide whether a shifted relative/Rees or Hasse--Schmidt cell can
promote (13).  Reconstructing that actual augmented differential, including
its module shifts and ordinary-residue row, is still the necessary positive
membership problem.

The dependency-free checker
[`verify_h3_direct_free_complete_first_fine_degree_membership.py`](../computations/verify_h3_direct_free_complete_first_fine_degree_membership.py)
supports `--face all` and the five individual face modes.  Its output labels
the graph calculation formal.  The corrected frozen digests are

```text
all  45d425d5e573f4040fa386ae409ea9f8861cb29f67daac8dc36a6d6445aaef61
1    a2abdc68f1e31b3c6055f222309303d8751b27d90cd173d22a8b532497af2ff3
2    d577c0d71aca09bd5ef2cdad639f2a9be06a0bbd3994a89635de7855469e250e
3    0e6f475c6f27165fae214f07ff54976957cdc8cdbcb2d3a45376ea8a6e161df1
4    0dd777f19ee9e4a7fa8f3e22faf1a13cb447822bbc20092149052d8f29ae9e59
5    bb0fa467f108e07d728879a29e9639c0b73ee11796a474e841a29c933b802d8b
```

# The five four-face defects have no strict minimal-degree full-nine lift

Research obstruction and next-row identification only.  This note does not
construct the required relative/Rees cells, prove zero indeterminacy, close
the unified overlap theorem, or prove Krenn's conjecture.

## 1. Outcome

Work universally at \(h=3\), with physical sites ordered as

\[
 x=0,\qquad D=(1,2,3,4,5),\qquad p=6,\qquad q=7,
 \qquad r=3,
\]

and impose the direct-free condition that the entire \(pr\) block is zero.
On the odd sites put

\[
                         m=12112,qquad Y_0=e_{00000}.
\]

The five failures of the universal reset are

\[
 d\tau_v=h_vY_0,qquad
 h_v=\operatorname {Haf}
       \left(q_m\big|_{D\setminus\{v\}}\right),
 \qquad v=1,\ldots,5.                                  \tag{1}
\]

There is no strict polynomial \(pq/pr\) full-nine combination whose first
nonzero fine-homogeneous component realizes any row in (1), while cancelling
all total EqSystem components and retaining the value under a strict readout
which factors through the common global coefficient.  This covers the
physical target and the already defined same-power residue and ordered
landing maps; it does not classify a new non-diagonal relative-comparison
readout.  More precisely:

1. for each \(v\), the first compatible fine multidegree contains exactly
   \(16\) global word rows and three quadratic multipliers for each row;
2. the resulting one-chart \(48\)-column boundary block has rank \(48\),
   even after setting the whole \(pr\) direct block to zero;
3. after retaining both chart presentations, the kernel is exactly the
   \(48\)-dimensional span of the tautological pairwise chart comparisons;
   and
4. the physical target, and every strict residue or ordered landing which
   factors through the common global coefficient, vanish on that kernel.

Thus none of the five abstract generators in (1) is already hidden among
the strict minimal-degree full-nine rows with a descended common-coefficient
readout.  Higher polynomial corrections enter at larger internal degree and
cannot change this degree-two initial obstruction.

The calculation also identifies the first additional row with no guesswork.
For each \(v\), let \(c_v\) be the global word which is mixed on
\(D\setminus\{v\}\) and zero on \(x,v,p,q\).  Then the exact two-edge polar

\[
 \boxed{
 \Pi_v:=
 {\partial^2 H_{c_v}\over
  \partial a_{xv}^{00}\,\partial a_{pq}^{00}}
       =h_v.}                                           \tag{2}
\]

The row \(c_v\) is mixed and hence has zero GHZ target.  In the \(pq\)
presentation, all three terms selected by (2) lie in the direct sector; in
the direct-free \(pr\) presentation, the same three terms lie in the
two-star sector.  Therefore (2) is exactly the degree-lowering symbol a
four-face comparison transgression would need.

Equation (2) is not yet a physical row.  Differentiating an equation which
vanishes at one source point is not a polynomial consequence of that
equation.  The missing new mathematics is to promote these five second
polars to source-valid relative/Rees or Hasse--Schmidt comparison cells,
with their unwanted lower components nullhomotoped.  Once that is done,
the five cells can repair the reset used by the already constructed
degree-four EqSystem Koszul cell.  The present result proves that a strict
row combination cannot replace this promotion.

## 2. The exact first fine-multidegree block

Give a labelled edge variable the fine degree

\[
                 \deg a_{ij}^{cd}=e_{i,c}+e_{j,d}.
\]

Fix \(v\) and write \(F_v=D\setminus\{v\}\).  Every site of \(F_v\) has
two relevant colour slots, zero and \(m_i\), while \(x,v,p,q\) retain only
their zero slots.  The first common fine degree is

\[
 \lambda_v=
 \sum_{i\in\{x,v,p,q\}}e_{i,0}
 +\sum_{i\in F_v}(e_{i,0}+e_{i,m_i}).                    \tag{3}
\]

A global full-nine row degree \(\mu(w)=\sum_i e_{i,w_i}\) can divide
\(\lambda_v\) only if

\[
 w_i=0\quad(i\notin F_v),
 \qquad w_i\in\{0,m_i\}\quad(i\in F_v).                \tag{4}
\]

There are exactly \(2^4=16\) such words.  For every one, the deficit
\(\lambda_v-\mu(w)\) has one slot on each of the four sites in \(F_v\).
A quadratic edge multiplier fills it exactly when its two edges are a
perfect matching of \(F_v\).  Hence there are exactly three multipliers per
word and \(48\) candidate columns.  This exhausts the multidegree; no other
full-nine word or quadratic multiplier can occur.

After \(A_{pr}=0\), every eight-site hafnian row retains \(90\) of its
\(105\) matching monomials.  Multiplication by the prescribed face matching
gives \(90\) degree-six monomial features in each column.  Exact feature
ownership gives the following certificate:

\[
\begin{array}{c|c|c|c|c}
v&\#\text{ columns}&\#\text{ features}&
 \#\text{ unique features}&\text{unique features per column}\\ \hline
1&48&3564&2880&60\\
2&48&3564&2880&60\\
3&48&3672&3072&64\\
4&48&3564&2880&60\\
5&48&3564&2880&60
\end{array}                                               \tag{5}
\]

Choosing one uniquely owned feature in every column gives \(48\) distinct
pivots.  Thus all five blocks have rank \(48\) over \(\mathbb Q\).  This is
stronger than failure of one proposed correction: there is no nonzero
one-chart syzygy anywhere in the complete first multidegree.

The three columns based on the pure global row have multipliers exactly the
three matching monomials of \(h_v\).  Their homogenized target terms are
therefore precisely \(-h_vU_0\).  Since the block is injective, those terms
cannot be corrected by the other fifteen compatible word rows.

## 3. Why adding the second chart does not repair the defect

The \(pq\) and \(pr\) full-nine equations are two partitions of the same
global matching polynomial.  The checker enumerates all \(3^8=6561\)
global words.  In every row, after direct-freeness,

\[
\begin{array}{c|cc}
\text{chart}&\text{direct matchings}&\text{two-star matchings}\\ \hline
pq&15&75\\
pr&0&90,
\end{array}                                               \tag{6}
\]

and the union in either row is the same set of \(90\) global matchings.
The three pure targets are likewise identical in the two charts.

If \(C_v\) is the injective \(48\)-column matrix from Section 2, the doubled
strict boundary matrix is

\[
                            [\,C_v\ C_v\,].               \tag{7}
\]

Its kernel is exactly

\[
                          \{(a,-a):a\in\mathbb Q^{48}\}. \tag{8}
\]

These are merely the componentwise statements that the two charts present
the same coefficient.  The physical target is part of the enumerated row
and therefore factors through \(a+b\).  The existing same-power
target--residue identity and literal ordered reconstruction likewise factor
their natural strict readouts through the common global coefficient.
Consequently those strict readouts vanish on (8).

This last sentence is a scope condition, not a classification theorem for
all possible physical readouts.  The checker explicitly models identical
linear chart readouts; it does not independently reconstruct every
ordinary-residue formula in the full relative complex.  A non-diagonal
relative comparison readout is precisely additional chain data and is not
excluded by the \(48/48\) rank calculation.

An antisymmetric readout could assign a nonzero value to (8), but it would
depend on which chart was named first.  It is not a descended physical
readout and is exactly the zero-indeterminacy failure that the construction
must avoid.  Thus the formal comparison kernel supplies no \(\tau_v\) for
any readout which descends through the common global coefficient.

## 4. The five exact polar symbols

The complete ledger is

\[
\begin{array}{c|c|c|c}
v&F_v\text{ word}&c_v&\text{polar variables}\\ \hline
1&2112&00211200&a_{01}^{00},a_{67}^{00}\\
2&1112&01011200&a_{02}^{00},a_{67}^{00}\\
3&1212&01201200&a_{03}^{00},a_{67}^{00}\\
4&1212&01210200&a_{04}^{00},a_{67}^{00}\\
5&1211&01211000&a_{05}^{00},a_{67}^{00}.
\end{array}                                               \tag{9}
\]

Indeed, a perfect matching term of \(H_{c_v}\) contains both displayed
edges exactly when it is their product with a perfect matching of \(F_v\).
There are three such face matchings, all with coefficient one.  Removing the
two displayed variables therefore leaves exactly \(h_v\), proving (2)
term by term.  The five supports are disjoint because they live on different
labelled deletion faces.

This gives a sharp formulation of the next lemma.  One must construct
source-provenant cells \(\widetilde\Pi_v\) whose associated-grade boundary is

\[
 d\widetilde\Pi_v=h_vY_0+
   (\text{higher comparison terms}),                     \tag{10}
\]

and cancel every higher term, physical target, and ordinary residue in the
complete sum.  A controlled non-flat specialization could create such cells
through the full-source kernel, but neither strict universal polynomial
rows nor the tautological chart comparison does so.

## 5. Relation to the degree-four Koszul cell

For the selected mixed row

\[
                         m_8=01211222,
\]

the previously audited first EqSystem syzygy is

\[
 K_{m_8}=H_{m_8}r_0-(H_0-u)r_{m_8}.                      \tag{11}
\]

Its lowest dehomogenized symbol is \(+r_{m_8}\), and scaling by
\(1/4=-\kappa_{\rm df}\) gives the required formal mixed-row normalization.
The obstruction to applying the reset to (11) is exactly the five-column
boundary (1).  Thus (10), if constructed with zero indeterminacy, is the
minimal missing input needed to make the Koszul symbol into a typed
source/cap chain.  The rank calculation above proves that (10) requires a
new degree-lowering comparison operation rather than a larger strict
quadratic-multiplier ansatz.

## 6. Exact verification and scope

The dependency-free checker
[`verify_h3_direct_free_literal_four_face_full_nine_no_go.py`](../computations/verify_h3_direct_free_literal_four_face_full_nine_no_go.py)

* enumerates all \(6561\) full-nine word rows in both charts;
* checks the \(15+75\) and \(0+90\) direct/two-star partitions;
* exhausts all five \(48\)-column first-multidegree blocks;
* certifies full rank by uniquely owned monomial pivots;
* checks the doubled chart kernel, the actual target, and two explicitly
  identical strict-readout models; and
* differentiates the five target-zero rows in (9), obtaining the exact
  three-term \(h_v\) in the claimed chart sectors.

The result rules out strict polynomial full-nine lifts with the required
degree-two initial.  It does not rule out relative/Rees or
Hasse--Schmidt cells, non-flat full-source Tor transgressions, localized
rational constructions, or higher operations with independently proved
source provenance.  Equation (2) identifies the required leading symbol of
such an operation; it does not assert that ordinary differentiation is
source-valid.

The frozen exact ledger digest is

```text
878a0e3ae179f2aa837f1ff190acb4a11ddca949bf8816d9e096a0cf023e39ef
```

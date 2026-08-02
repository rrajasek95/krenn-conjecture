# A terminal Hamilton skeleton is not yet the physical clean-cap readout

## 1. Outcome

The terminal path-forest proposal has two logically separate endpoint
statements.  The first is combinatorial and correct: if

\[
                         F=M\sqcup J
\]

is an alternating Hamilton path, then the join matching \(J\) leaves the
two path endpoints \(p,q\) unmatched and is a perfect matching on
\(B\setminus\{p,q\}\).  The second statement, needed for descent, is much
stronger: the coefficient of this terminal cell must be the physical cap
coefficient for \(p,q\), its direct scalar and three target diagonals must
be active, and changing the source lift must not change the clean-cap
error.

An exact chart-26 audit separates these statements.  The physical normalized
target does contain many Hamilton monomials with unique source provenance,
and one explicit such coordinate face has an active clean cap.  But:

* the 300 path terms of the first mixed-source degree-six cell have 10,173
  normalized legal terminal extensions, none of which is a physical target
  monomial; and
* on an explicit physical target Hamilton row, adding one off-path source
  coordinate leaves the terminal row and cap activity unchanged but changes
  the clean-cap error from zero to a four-term nonzero tensor.

Thus a Hamilton leading monomial is not itself the clean-cap readout.  The
terminal theorem in the proposed curvature--Bockstein dichotomy needs an
augmented, source-faithful chain map which both reaches the physical target
and kills the off-path lift ambiguity.

## 2. What the path endpoints prove formally

Let \(F\) be a spanning even-component path forest and let \(M(F)\) be its
unique odd-position matching.  At terminal rank, \(F\) is a Hamilton path,
and its even-position edges form a matching

\[
                       J(F)\text{ on }B\setminus\{p,q\}.
\tag{1}
\]

This supplies the support matching required after a putative deletion of
\(p,q\).  It does not supply a direct block on the pair \(pq\): the two
endpoints of a Hamilton path are not joined by a path edge.  Direct cap
activity is therefore independent information.

There is a useful sufficient coordinate-face lemma.  Suppose, in addition
to an active direct cap \(K\), that the only nonzero endpoint spokes are
\(A_{pa}\) and \(A_{qb}\), where \(a,b\) are the two neighbours of the path
endpoints.  Then the response in the exact cap formula is supported on one
pair:

\[
                              r=R_{ab}.
\]

In the site-square-zero algebra, \(R_{ab}^2=0\).  Hence every term in the
homogeneous cap error

\[
 {cal E}_{p,q}(K)=
 \sum_{k=2}^{h}s^{h-k}
       \left[{r^k\over k!}\exp(x)\right]_{B\setminus\{p,q\}}
\tag{2}
\]

vanishes.  This proves cleanliness on the literal sparse coordinate face.
A forest monomial, however, asserts that its selected coordinates occur; it
does not set every other endpoint spoke to zero.  Equation (2) is sensitive
to precisely those unrecorded spokes.

## 3. The physical target has unique Hamilton rows

Set the twelve chart-support coordinates to one, exactly as in the Laurent
normalization.  Each pure hafnian has 105 distinct normalized terms.  More
strongly, all

\[
                              105^3=1,157,625
\]

products of one matching from each of the three pure colours remain
distinct after normalization.  Thus every normalized monomial of
\(\bar H_0\bar H_1\bar H_2\) has coefficient one and a unique pure matching
triple.  There is no target-side provenance ambiguity in this chart.

The normalized degree distribution is

\[
\begin{array}{c|rrrrrrrrrrrr}
d&0&2&3&4&5&6&7&8&9&10&11&12\\ \hline
\#&1&36&96&612&2304&9120&25344&73584&171008&313920&345600&216000.
\end{array}
\]

Among the 25,344 degree-seven rows, exactly 5,596 have a squarefree
uncoloured Hamilton-path skeleton.  For 5,388 of them, the two endpoints
form one of the twelve chart-support pairs.  On those rows a direct diagonal
entry of \(A_{pq}\) is a normalized unit, so one can choose a cap \(K\) off
the direct-scalar hyperplane while keeping all three
\(\kappa_c=K(e_c,e_c)\) nonzero.  The remaining 208 Hamilton rows have no
support edge on their endpoint pair, so their terminal monomial alone does
not even force \(s=\langle K,A_{pq}\rangle\ne0\).

This is the positive part of the audit: physical, uniquely sourced terminal
target rows exist abundantly, and most have chart-forced direct activity.

## 4. The first mixed forest cell does not reach them

The first exact degree-six compatibility polynomial has 300 simple path
terms: 200 of type \(P_6+P_2\) and 100 of type \(P_4+P_4\).  For each term,
join either endpoint of one component to either endpoint of the other and
retain every one of the nine endpoint decorations, except that a
chart-support coordinate is a unit rather than a new normalized variable.
This gives

\[
       10,173\text{ distinct normalized degree-seven extensions}
\tag{3}
\]

and 627 additional join occurrences using a support unit.  The intersection
of (3) with the complete normalized pure target is empty.

There is also a direct label explanation.  Every one of the 300 degree-six
path terms contains a bichromatic decorated edge.  Every variable in a pure
target monomial is monochromatic at its two endpoints.  Adding one legal
join cannot remove the bichromatic variable.  Therefore the terminal
extension remains target-zero even though its uncoloured graph is a
Hamilton path.

Consequently the component-decreasing orientation does not by itself define
the required augmentation from mixed-source forest cells to the pure target.
That augmentation must be an additional chain-level operation, not the
forgetful identification of their path skeletons.

## 5. One off-path spoke changes the clean-cap readout

The target Hamilton row

```text
04237475b8cfea
```

has endpoints \((p,q)=(2,5)\) and the unique pure matching triple

```text
0075cfea   0482b8ee   23747de9.
```

Its seven normalized variables are

\[
\begin{gathered}
x_{01}^{11},\ x_{04}^{22},\ x_{17}^{22},\ x_{23}^{00},\\
x_{36}^{11},\ x_{46}^{00},\ x_{57}^{00}.
\end{gathered}
\tag{4}
\]

The direct coordinate \(x_{25}^{00}\) is in the chart support and hence is
one.  Let \(A^{(0)}\) have all twelve support coordinates and the seven
coordinates (4) equal to one, with every other coordinate zero.  The exact
cap

\[
 K=
 \begin{pmatrix}
 -1&-1&1\\
  1& 1&1\\
 -1&-1&1
 \end{pmatrix}
\tag{5}
\]

has

\[
              s=-1,\qquad(\kappa_0,\kappa_1,\kappa_2)=(-1,1,1),
\]

so \(s\kappa_0\kappa_1\kappa_2=1\).  Direct expansion of the eight-to-six
error

\[
             {\cal E}_{2,5}(K)={s r^2x\over2}+{r^3\over6}
\tag{6}
\]

gives zero on all \(3^6\) residual colour words.

Now form \(A^{(1)}\) by adding only

\[
                              x_{02}^{00}=1.              \tag{7}
\]

This is an off-support endpoint spoke, absent from (4).  It changes neither
the terminal target monomial nor the direct block \(A_{25}\), and (5) still
has the same nonzero \(s\) and \(\kappa_c\).  Nevertheless (6) now has four
nonzero coefficients, all equal to two.  In the residual-site order
\((0,1,3,4,6,7)\), their words are

```text
020220  020221  022220  022221.
```

This is an exact minimal lift-indeterminacy witness.  It does not claim that
either sparse assignment is an exact ternary source, nor that a different
cap cannot clean the perturbed assignment.  It proves the precise local
negative statement needed here: the terminal Hamilton coefficient and its
activity do not determine the physical clean-cap error.  The mixed-source
equations or a specified contracting homotopy must control (7).

## 6. Required terminal theorem

The terminal clause of the path-forest/Bockstein program must therefore
prove all of the following, with source labels retained.

1. Its transferred augmentation maps at least one terminal mixed forest
   class to a physical pure Hamilton row; uncoloured path equality is
   insufficient by Section 4.
2. The endpoint pair lies in an active direct chart, or the branch with no
   support direct edge is routed to a decreasing geometric split.
3. Every change of primitive/source lift alters the cap error by an
   augmented boundary.  Equivalently, the off-path-spoke ambiguity in
   Section 5 must vanish at an exact ternary source.
4. The resulting cap has zero error in the literal physical aggregate,
   after which the exact clean-pair descent theorem applies.

This is exactly the role of the specified homotopy in the proposed
homological-perturbation construction: it must supply a target-compatible
choice of lift, not merely prove that the path-forest complex is acyclic
before augmentation.

## 7. Verification

Run

```sh
python3 computations/verify_n8_chart26_terminal_hamilton_readout.py
```

The checker enumerates the full normalized pure target, proves uniqueness of
all pure matching triples after normalization, classifies the degree-seven
Hamilton rows and endpoint activity, compares every legal terminal extension
of the first mixed forest cell, and expands both clean-cap errors exactly over
the integers.  Its ledger digest is
`2ecee35a9284d8bcbc8955122ec3b2c7ca65a2b5002d800dbea2616db6967824`.

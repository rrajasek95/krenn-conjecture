# Independent audit of the strict four-face full-nine no-go

Audit target: commit `7723671`.  The five fine-degree rank certificates,
chart decomposition, second-polar identities, and bounded strict-readout
conclusion are sound.

This audit does not construct a relative/Rees or Hasse--Schmidt cell, prove
zero indeterminacy, compute the full source Tor transgression, close the
unified overlap theorem, or prove Krenn's conjecture.

## 1. Outcome

The independent checker reconstructs every candidate from the fine slot
degree rather than importing the primary block.  For each deleted odd site
(v), it brute-forces all (3^8) global words against the degree

\[
 \lambda_v=
 \sum_{i\in\{x,v,p,q\}}e_{i,0}
 +\sum_{i\in D\setminus\{v\}}
       (e_{i,0}+e_{i,m_i}),
 \qquad m=12112.
 \tag{A1}
\]

Exactly sixteen words divide (A1).  For each word, subtracting its row
degree leaves four labelled slots on four different sites.  Independently
pairing those slots gives exactly three quadratic edge monomials.  Thus the
first block has (16\cdot3=48) columns, with no omitted word or multiplier.

After setting every (p\)-(r) entry to zero, the independently recovered
feature ledger is

\[
\begin{array}{c|c|c|c|c}
v&\text{columns}&\text{distinct features}&
\text{uniquely owned features}&\text{unique per column}\\ \hline
1&48&3564&2880&60\\
2&48&3564&2880&60\\
3&48&3672&3072&64\\
4&48&3564&2880&60\\
5&48&3564&2880&60.
\end{array}
\tag{A2}
\]

Every column has the displayed positive number of uniquely owned monomials.
Choosing one per column gives 48 distinct pivots, so every one-chart block
is injective.  The doubled strict chart boundary is therefore
([C_v\ C_v]), of rank 48 with kernel exactly

\[
                         \{(a,-a):a\in\mathbb Q^{48}\}.
 \tag{A3}
\]

Any linear readout which descends through the common global coefficient has
the form (\rho(a)+\rho(b)=\rho(a+b)) and vanishes on (A3).  This proves the
strict minimal-degree no-go at the scope claimed in `7723671`.

The five second polars are also exact:

\[
 {\partial^2H_{c_v}\over
   \partial a_{0v}^{00}\partial a_{67}^{00}}=h_v.
 \tag{A4}
\]

Each is a target-zero global row, its three terms lie in the (pq)-direct
sector and the direct-free (pr)-two-star sector, and distinct deleted faces
have disjoint monomial support.  Equation (A4) is a correct leading symbol
for the missing relative operation, not a polynomial consequence of the
source equations.

## 2. Full reconstruction of a 48-column block

For the requested explicit independent block, take (v=3=r).  Its face is

\[
                       F_3=\{1,2,4,5\},
 \qquad m|_{F_3}=1212.
 \tag{A5}
\]

The checker does not assume the binary-word description.  It enumerates all
global ternary words (w\), forms

\[
                 \mu(w)=\sum_{i=0}^7e_{i,w_i},
 \tag{A6}
\]

and retains (w) exactly when (\mu(w)\leq\lambda_3) componentwise.  This
recovers the sixteen words which are zero off (F_3) and choose either zero
or the displayed mixed colour on each face site.

For each retained word, the checker explicitly subtracts the Counters for
(A6) from (A1).  The result is four site--colour slots.  It enumerates the
three perfect matchings of those slots and turns each into its labelled
two-edge multiplier.  For every resulting column it multiplies that
monomial by all 105 eight-site hafnian matchings and discards precisely the
15 matchings containing the forbidden edge ({p,r}=\{6,3\}).  Each column
therefore has 90 terms of coefficient one.

Across the full (v=3) block, those (48\cdot90) occurrences form 3672
distinct monomials.  Exactly 3072 occur in one column, uniformly 64 per
column.  This provides a literal 48-pivot certificate with no numerical
specialization, modular rank inference, or imported matrix.

The same reconstruction is run for the other four faces and gives (A2).
The larger unique count at (v=3) is consistent with the topology: the
deleted face omits the site (r) participating in the zeroed (p\)-(r)
block.

## 3. Exhaustion of the first fine degree

The counting argument in the primary note is complete.  A labelled edge
uses one colour slot at each of two distinct sites.  A full global row uses
one slot at every site.  Hence a row degree can divide (\lambda_v) only if
it is zero on (x,v,p,q) and uses one of the two allowed colours at every
site of (F_v).  This gives the sixteen rows.

The remaining degree has exactly one slot at each face site.  A quadratic
edge monomial fills it if and only if its two edges form a perfect matching
of (F_v).  There are exactly three.  Variables outside the face, repeated
site occupancy, and a different colour label all violate the fine degree.
Thus no additional quadratic multiplier can participate in the first
homogeneous boundary.

The three columns whose global word is `00000000` have multipliers exactly
the three monomials of (h_v).  Their homogenized target contribution is
(-h_vU_0).  Since (C_v) is injective, no combination with the fifteen
other word rows cancels its polynomial boundary in one chart.

For an arbitrary polynomial strict lift, take its first nonzero
fine-homogeneous component.  If its desired initial output is (h_vY_0),
that component lies in the block just exhausted.  Higher fine-degree terms
cannot alter it.  This justifies the primary note's passage from block
injectivity to the no-go for higher polynomial corrections with the same
degree-two initial.

## 4. Chart decomposition

There are 105 perfect matchings on eight sites.  Direct-freeness removes the
15 containing the edge (pr=\{6,3\}), leaving 90 in every labelled word
row.  Among the survivors, 15 contain (pq=\{6,7\}), while 75 do not.
No survivor contains (pr).  Hence, uniformly in all (3^8=6561) words,

\[
\begin{array}{c|cc}
 &\text{direct}&\text{two-star}\\ \hline
pq&15&75\\
pr&0&90.
\end{array}
\tag{A7}
\]

The audit assigns colour labels after this topological partition and checks
word by word that both unions are the same 90-term global hafnian row.  A
matching covers all sites, so different labelled matchings do not collide.
The two charts also have the same three pure GHZ target rows.  Thus a strict
combination retaining both complete chart presentations really has boundary
([C_v\ C_v]), and (A3) follows from injectivity of (C_v).

The sign convention is important.  A comparison vector is ((a,-a)), and
the common physical coefficient, target, or descended strict readout sees
the sum.  An antisymmetric chart-order functional could see (A3), but it
would not descend through the common global coefficient and would change
sign after swapping chart names.  It is exactly the additional relative
comparison datum which the strict calculation does not construct.

## 5. The five polar identities

Let (c_v) be zero on (x,v,p,q) and have word (m) on the other four odd
sites.  The independently reconstructed ledger is

\[
\begin{array}{c|c|c|c}
v&F_v\text{ word}&c_v&\text{differentiated edges}\\ \hline
1&2112&00211200&a_{01}^{00},a_{67}^{00}\\
2&1112&01011200&a_{02}^{00},a_{67}^{00}\\
3&1212&01201200&a_{03}^{00},a_{67}^{00}\\
4&1212&01210200&a_{04}^{00},a_{67}^{00}\\
5&1211&01211000&a_{05}^{00},a_{67}^{00}.
\end{array}
\tag{A8}
\]

Every hafnian monomial is squarefree in labelled edges.  A term survives the
two derivatives exactly when its matching contains both complementary edges
(0v) and (67).  The remaining two edges are then an arbitrary perfect
matching of (F_v), giving the three terms of (h_v), each with coefficient
one.  This proves (A4) term by term.

Because every surviving polar term contains (67=pq) before
differentiation, it belongs to the (pq)-direct sector.  Because the whole
(pr) block was removed, the same term belongs to the (pr)-two-star
sector.  The checker differentiates all four chart sectors separately and
verifies these assertions for every (v).

Ordinary differentiation is not source-valid here.  From (H_{c_v}(A)=0)
at a source point one cannot infer
(\partial_{0v}^{00}\partial_{67}^{00}H_{c_v}(A)=0).  Therefore (A4)
identifies the necessary associated-grade symbol but does not itself provide
a row in the ideal generated by the full-nine equations.

## 6. Exact readout scope

The rank theorem proves a statement about the total strict global
coefficient.  It automatically covers the physical target.  It also covers
the previously defined **strict** same-power residue and literal ordered
landing because those are linear operations on the same complete global
coefficient array: applying either operation after the chart comparison is
the same as applying it to the zero common coefficient.

The primary checker models those latter two maps by identical chart
functionals; it does not reconstruct their full formulas.  Their inclusion
in the theorem relies on their already established factorization through
the complete coefficient array, not on a new computation in `7723671`.
This is a valid use of the previous definitions, but it is the exact bound
on the conclusion.

In particular, the audit does **not** extend the no-go to:

* a non-diagonal comparison readout with independent chain provenance;
* a relative/Rees or Hasse--Schmidt cell carrying the polar (A4);
* a specialization-created full-source Tor kernel;
* a rational operation after localization; or
* a higher operation whose lower terms are separately nullhomotoped.

Within this scope, the conclusion is sound: no strict polynomial
minimal-degree full-nine combination both cancels its total EqSystem
boundary and retains (h_vY_0) under a readout descended from the common
coefficient.

The dependency-free checker
[`audit_h3_direct_free_literal_four_face_full_nine_no_go_independent.py`](../computations/audit_h3_direct_free_literal_four_face_full_nine_no_go_independent.py)
uses no primary-checker imports.  It reconstructs all five blocks, including
the full (v=3) feature matrix, audits all 6561 chart unions, verifies the
five polars by sparse exact differentiation, and freezes a separate digest.

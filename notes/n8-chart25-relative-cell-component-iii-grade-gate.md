# The chart-25 relative cell does not land in the rootless Component III attaching grade

## Outcome

The proposed chart-25 comparison is an exact representative of the **local
relative** \(4D-\tau\) class, but it is not the source-valid
\(C_{\rm rel}\) required by the rootless Component III obstruction.

Let

\[
 M_0=01^{00}\mid24^{00}\mid35^{00}\mid67^{00}.
                                                               \tag{1}
\]

Each of the four hidden rows \(A_i\) has (1) as its unique pure-zero
perfect-matching divisor.  Put \(m_i=A_i/M_0\) and

\[
                         a_i=m_i(H_0-1).                \tag{2}
\]

For every balanced incident mixed column \(e_i\) whose local trace is
\(A_i+D\), the local \(A_i\) terms cancel in \(e_i-a_i\), leaving \(D\).
Globally, however, the same difference also has:

* \(207\) nonzero monomial rows outside the five-row fibre;
* a nonzero pure target labelled by the specific multiplier \(m_i\); and
* the product-of-three-anchors site-colour degree, not the repeated selected
  response degree of \(K\).

The four \(m_i\) are distinct.  Every possible four-sum projects to \(4D\),
but retains either \(818\) or \(820\) off-fibre rows and all four target
labels.  Moreover, no choice of its balanced mixed words lies in one fixed
selected endpoint ordering.

Only after discarding the off-fibre rows and quotienting the four target
labels to one normalized target does the sum become the familiar formal
\(4D-\tau\) mapping-cylinder class.  That projection is exactly the
relative construction already classified in
[the chart-25 relative obstruction](n8-chart25-relative-4d-obstruction.md);
it is not equation (11) of
[the Component III typed audit](h3-rootless-component-iii-complete-typed-inventory.md).

## 1. The six balanced mixed columns

On the common five-row fibre, the balanced \(4+4\) binary words incident to
each \(A_i\) and \(D\) are:

\[
\begin{array}{c|l}
A_1&21212112\\
A_2&11122122,\ 21221121\\
A_3&12112212,\ 22211211\\
A_4&12121221.
\end{array}                                             \tag{3}
\]

Thus the option counts are \(1,2,2,1\), giving four possible four-sums.
This confirms that coarse \(4+4\) word count does not itself exclude the
candidate.

The selected rootless midpoint sector is finer.  With endpoint order
\((2,1)\), the six residual labels must have three \(1\)'s and three
\(2\)'s.  Of (3), only the \(A_1,A_2\) words lie in that twenty-word set.
With endpoint order \((1,2)\), only the \(A_3,A_4\) words do:

\[
\begin{array}{c|c}
\text{selected endpoint order}&\text{covered leaves}\\ \hline
(2,1)&A_1,A_2\\
(1,2)&A_3,A_4.
\end{array}                                             \tag{4}
\]

The two remaining balanced alternatives have same-colour endpoints
\((1,1)\) or \((2,2)\) and are not in either selected off-diagonal
midpoint set.  Hence every four-sum mixes at least two starting endpoint
sectors.  A global colour permutation or endpoint reversal swaps the two
rows of (4); it cannot put all four leaves in one ordering.

One individual \(e_i-a_i\) may lie over one selected midpoint word, but
normalizing it by four only changes the scalar.  It still has one word
rather than the twenty-row attaching aggregate, a nonzero target, and its
full off-fibre boundary.

## 2. Literal fine degree

Every monomial in \(e_i\) and \(a_i\) has site-colour multidegree

\[
                 (1,1,1)\quad\text{at every physical site}.    \tag{5}
\]

In particular the two selected endpoints have degree

\[
                         ((1,1,1),(1,1,1)).             \tag{6}
\]

The localized \(Q_3\) terminal has repeated degree
\(3e_a\) on the left and \(3e_b\) on the right.  Before division by the
selected direct scalar, the companion-corrected underived \(K\) row has
degree \(4e_a,4e_b\).  Neither is (6), for any labels \(a,b\).

This is a literal-grade statement.  A new selector or divisor transport
could change the effective grade, but constructing that transport is
precisely the missing physical comparison; scalar normalization of
\(e_i-a_i\) cannot do it.

## 3. Full source boundary rather than the five-row trace

Each hafnian column has \(105\) perfect-matching terms.  For every choice in
(3), the mixed column \(e_i\) and pure column \(a_i\) share exactly one
monomial row, namely \(A_i\).  Therefore, in the \(e_i-a_i\) convention,

\[
 \partial(e_i-a_i)
      =D+R_i+\tau_{m_i},                                \tag{7}
\]

where \(R_i\) has \(207\) off-fibre monomial rows.  Including \(D\), the
monomial part of (7) has \(208\) rows with coefficient histogram

\[
                         104(+1)+104(-1).               \tag{8}
\]

The target term \(\tau_{m_i}\) is the multiplier-labelled constant term of
\(-a_i\); it is nonzero.  Reversing the chain orientation reverses every
sign but removes none of these terms.

For the four possible choices in (3), the four-sum monomial boundary has:

\[
\begin{array}{c|c|c}
\text{number of choices}&\text{all monomial rows}&\text{off-fibre rows}\\
\hline
2&819&818\\
2&821&820.
\end{array}                                             \tag{9}
\]

In every case the five-row projection is exactly \(4D\).  The four pure
target multipliers are

\[
\begin{aligned}
&0d114c62bcdce0e5,\qquad 0d114d62b8dce0e6,\\
&0d114f5ebcdce0e8,\qquad 0d11505eb8dce0e9,
\end{aligned}                                          \tag{10}
\]

and are pairwise distinct source labels.

The formal local target quotient gives each label in (10) weight \(1/4\).
After that quotient their sum is one \(\tau\), and after additionally
deleting \(R=\sum R_i\), (7) becomes \(4D\pm\tau\), with the sign set by
chain orientation.  Those are exactly the two non-source operations:
target mapping-cylinder projection and off-fibre truncation.

## 4. Consequence for Component III

Equation (11) of the complete typed audit requires a source-labelled lower
face with total pure-anchor incidence \(-1\) and

\[
                     w=\operatorname{tgt}
                       =\operatorname{ores}=0,          \tag{11}
\]

in the same selected endpoint/midpoint grade as \(K\).  The chart-25
candidate supplies the desired local anchor incidence only after retaining
the nonzero target in (7).  It also fails the selected endpoint ordering,
literal fine degree, and full source boundary conditions.

Therefore neither \(4(e_i-a_i)\) nor any of the four possible four-sums is
the missing \(C_{\rm rel}\).  A positive use of chart 25 still needs a
new source-provenant comparison which simultaneously:

1. transports the product-anchor degree into one repeated selected response
   degree;
2. cancels all \(R_i\) off-fibre rows; and
3. cancels the four literal target labels without reintroducing the
   conormal/\(w\) augmentation.

That three-part comparison, not the local \(4D-\tau\) projection, is the
minimal new physical datum.

## Verification

Run

    python3 computations/verify_n8_chart25_relative_cell_component_iii_grade_gate.py
    python3 -O computations/verify_n8_chart25_relative_cell_component_iii_grade_gate.py

The checker pins the exact chart-25 fibre and Component III inventory,
recovers (1) from the coordinate table, exhausts all six balanced incident
columns and all four four-sums, compares them with both twenty-word selected
midpoint sets, and replays every literal matching term, target label, fine
degree, and off-fibre coefficient.

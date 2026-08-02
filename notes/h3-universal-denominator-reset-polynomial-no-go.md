# Universal denominator reset has no normalized polynomial correction

Research reduction only.  This note does not construct the five physical
four-face homotopies below, the invisible cross-word lift, a nonzero filtered
differential, the unified overlap theorem, or a proof of Krenn's conjecture.

## 1. Outcome

Let (D=\{1,2,3,4,5\}), let every site have colours (0,1,2), and put

\[
 \bar m=12112,\qquad Y_0=e_{00000}.
\]

Over the universal polynomial ring (R=\mathbb Q[q_{ij}^{ab}]), the odd
denominator presentation is

\[
 \delta:R^{15}\longrightarrow R^{243},\qquad
 d_{v,a}\longmapsto e_a^{(v)}q^{[2]}.
 \tag{1}
\]

The bare extraction (\epsilon_{\bar m}) meets the five columns
(d_{v,\bar m_v}) in the nonzero quadrics

\[
 \epsilon_{\bar m}\delta(d_{v,\bar m_v})=h_v,
 \qquad
 h_v=\operatorname {Haf}
 \left(q_{\bar m}|_{D\setminus\{v\}}\right).
 \tag{2}
\]

There is no polynomially corrected extraction

\[
 L=\sum_{w\in\{0,1,2\}^5}\ell_w(q)\epsilon_w,
 \qquad \ell_{12112}=1,
 \tag{3}
\]

which annihilates all fifteen columns of (1).  In fact every polynomial row
(L) satisfying (L\delta=0) has

\[
                  \ell_w(0)=0\quad\hbox{for every }w.
 \tag{4}
\]

Thus no universal denominator annihilator has a unit word coordinate.  A
rational projector may appear after localizing at internal (q)-minors, and
the sparse guard makes the five (h_v) vanish, but neither operation is the
required polynomial source construction.

There is a second, stronger obstruction at the chain level.  At the pure
output coordinate (Y_0), the degree-two initial image of the existing
fifteen target denominator rows is the five-dimensional span of the pure
four-face hafnians

\[
 g_v=\operatorname {Haf}
 \left(q_{00000}|_{D\setminus\{v\}}\right).
 \tag{5}
\]

The five (h_v) are linearly independent modulo this span.  Hence the bare
reset cannot be lifted through the same denominator presentation by a
polynomial map on relation generators.

The smallest abstract repair is exact and forced: adjoin five relative cap
generators

\[
 \boxed{\quad
 \tau_v^{\bar m\to0},\qquad
 d\tau_v^{\bar m\to0}=h_vY_0,
 \quad v=1,\ldots,5.\quad}
 \tag{6}
\]

Then send (d_{v,\bar m_v}) to (\tau_v) and the other ten denominator
generators to zero.  This gives the desired chain identity on all fifteen
columns.  Five is minimal in the associated (q)-degree-two pure-output
piece.  Adding (6) does not kill (Y_0): augmentation (q\mapsto0) kills
every old and new boundary while retaining (Y_0).

Equation (6) is an abstract presentation, not a physical construction.  The
new mathematical obligation is to realize these five initial components by
source-provenant full-nine cross-word rows, with all unwanted target,
ordinary-residue, and other EqSystem components cancelled.  Equivalently,
one may realize their five-component class as the specialization
transgression of the full source complex.  Direct-freeness alone cannot do
this.

## 2. Why the polynomial correction is impossible

For a word (w=(w_1,\ldots,w_5)), the coefficient of (e_w) in a column of
(1) is

\[
 [e_w]\delta(d_{v,a})=
 \begin{cases}
 \displaystyle
 \sum_{M\in\operatorname {Match}(D\setminus\{v\})}
       \prod_{ij\in M}q_{ij}^{w_iw_j},&w_v=a,\\[6pt]
 0,&w_v\ne a.
 \end{cases}
 \tag{7}
\]

Fix the column ((v,a)).  A monomial in (7) records a matching of the four
non-deleted sites, and its labelled edge variables record the colours at
all four sites.  Together with (w_v=a), that monomial determines (w)
uniquely.  Therefore distinct words have disjoint monomial support inside a
fixed column.

Let (c_w=\ell_w(0)).  Every entry of (1) is homogeneous of (q)-degree
two, so the degree-two part of (L\delta=0) is

\[
 \sum_{w:w_v=a}c_w[e_w]\delta(d_{v,a})=0
 \quad(v\in D, a=0,1,2).
 \tag{8}
\]

Disjoint monomial support in (8) forces every (c_w=0).  This proves (4).
The exact checker packages (8) as a sparse initial map: its 243 word columns
have rank 243.  Since (3) has (c_{12112}=1), it is impossible before any
higher-degree correction can enter.

This is stronger than checking only the five displayed defects.  It says the
universal quotient

\[
 C_q=\mathcal R_5(D)/(\mathcal R_1(D)q^{[2]})
 \tag{9}
\]

has no polynomial word-coordinate retraction with a unit leading
coefficient.  The descended reset on the sparse rational guard is a genuine
specialization phenomenon: the degree-two initial map loses the particular
five features in (2) after the guard kills them.

## 3. The five independent target defects

Writing (q_{ij}^{ab}) in site order, the five quadrics are

\[
\begin{aligned}
 h_1={}&q_{23}^{21}q_{45}^{12}+q_{24}^{21}q_{35}^{12}
                    +q_{25}^{22}q_{34}^{11},\\
 h_2={}&q_{13}^{11}q_{45}^{12}+q_{14}^{11}q_{35}^{12}
                    +q_{15}^{12}q_{34}^{11},\\
 h_3={}&q_{12}^{12}q_{45}^{12}+q_{14}^{11}q_{25}^{22}
                    +q_{15}^{12}q_{24}^{21},\\
 h_4={}&q_{12}^{12}q_{35}^{12}+q_{13}^{11}q_{25}^{22}
                    +q_{15}^{12}q_{23}^{21},\\
 h_5={}&q_{12}^{12}q_{34}^{11}+q_{13}^{11}q_{24}^{21}
                    +q_{14}^{11}q_{23}^{21}.
\end{aligned}
\tag{10}
\]

At output word (00000), only the five target columns (d_{v,0}) have a
nonzero coefficient, and those coefficients are (g_v).  Every variable in
a (g_v) has colour label (00), whereas every variable in an (h_v) has
labels in (\{1,2\}).  Moreover deleting different sites gives different
four-site supports.  Consequently

\[
 \dim_\mathbb Q\langle g_1,\ldots,g_5\rangle=5,
 \qquad
 \dim_\mathbb Q\langle g_1,\ldots,g_5,h_1,\ldots,h_5\rangle=10.
 \tag{11}
\]

Polynomial coefficients on target relation generators cannot change this
initial calculation: only their constant terms contribute in (q)-degree
two.  Thus each (h_vY_0) represents a separate missing initial relation.
This proves the lower bound of five in (6).

For completeness, corrections to the degree-zero reset on other input words
also cannot remove (10).  In the fixed source column
(d_{v,\bar m_v}), each monomial of (h_v) has unique owner (\bar m) by
the argument following (7).  Cancelling it would change the leading
coefficient of the reset at (12112).

## 4. The exact next source rows

The five required initial rows can be named by their four-site face words:

\[
\begin{array}{c|c|c}
v&D\setminus\{v\}\text{ mixed word}&\text{required row}\\ \hline
1&2112&\tau_1^{2112\to0000}\\
2&1112&\tau_2^{1112\to0000}\\
3&1212&\tau_3^{1212\to0000}\\
4&1212&\tau_4^{1212\to0000}\\
5&1211&\tau_5^{1211\to0000}.
\end{array}
\tag{12}
\]

The two (1212) entries live on different labelled deletion faces and hence
have different fine multidegrees.  A single equivariant tensor generator
could package (12), but its associated graded image must still contain five
independent labelled components.

Physically, these are not new equations (h_v=0).  They must be relative
source/cap homotopies whose pure-output initial boundary is (h_vY_0), while
their other full-nine boundary pieces cancel.  They are the five
denominator-level commutator rows needed to lift the degree-four mixed/pure
EqSystem Koszul cell through the odd quotient.  A useful typed target is

\[
 d\widetilde\tau_v
   =h_vY_0+\delta(\eta_v)+
     (\text{higher filtration/full-nine rows}),
 \tag{13}
\]

with zero physical target and ordinary residue after the complete sum.  The
terms (\delta(\eta_v)) may alter representatives but cannot remove the five
initial cokernel classes (11).

The first place to search is therefore the all-label four-face exposure of
the simultaneous (pq/pr) equations, not a larger two-row EqSystem
multiplier ansatz.  If no universal rows of type (13) exist, the remaining
route is a non-flat full-source kernel whose transgression has exactly the
five initials (10).  The ordinary cap block and the universal odd quotient
cannot manufacture them.

The distinction from direct-freeness is exact.  Setting the `pr` direct
block to zero changes endpoint data but leaves the internal universal ring
(R), (1), and every (h_v) unchanged.  The sparse direct-free guard kills
the (h_v) only because its internal (q)-support has no four-site perfect
matching at (12112).  That specialization explains the descended packet
reset, but it supplies no universal row (13).

## 5. Verification and scope

The dependency-free checker
[`verify_h3_universal_denominator_reset_polynomial_no_go.py`](../computations/verify_h3_universal_denominator_reset_polynomial_no_go.py)
enumerates all 243 words and all fifteen universal denominator columns.  It
verifies the 3645 uniquely owned degree-two monomial features, the rank-243
initial map, the five formulas (10), the ranks (5) and (10) in (11), the
literal fifteen-column chain identity after adjoining (6), and survival of
(Y_0) under (q\mapsto0).

The result rules out polynomially normalized strict extraction and a lift
through the old denominator rows.  It does not rule out the five new
source-provenant rows (13), a full-source specialization transgression,
rational constructions on smaller opens, or higher relative-Rees cells.  In
particular, (6) is a minimal algebraic specification of the missing data,
not evidence that the full-nine equations supply those data.

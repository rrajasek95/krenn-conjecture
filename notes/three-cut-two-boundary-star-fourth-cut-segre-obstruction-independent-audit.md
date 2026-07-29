# Independent audit: fixed-interior two-star Segre obstruction

## 1. Verdict and scope

The exact obstruction in
[the primary note](three-cut-two-boundary-star-fourth-cut-segre-obstruction.md)
passes an independent endpoint-ordered reconstruction over
\(\mathbb Q\).  With all \(108\) entries of the two boundary stars
variable, the line normal has

\[
                          9\cdot11\cdot9=891
\]

diagonal component triples and the plane normal has

\[
                         15\cdot13\cdot14=2730.
\]

After adjoining all six ordered off-diagonal fibres, every one of these
\(3621\) component triples has unit standard basis.  Hence neither
normal form has a complex factorized solution.

No algebraic or scope error was found.  This is a theorem only for the
nine fixed cells internal to \(S=\{0,1,2,3,4,5\}\).  It permits arbitrary
complex changes on both boundary stars and on block \(67\), but it does
not exclude a fourth cut after perturbing the interior.

## 2. Independent endpoint and cofactor expansion

For an internal edge \(i<j\), endpoint order was retained literally:
a source \(E_{cd}\) places \(c\) at \(i\) and \(d\) at \(j\).  Fresh
perfect-matching enumeration of the nine fixed cells gives

\[
 H_S=[002100]+[121200]+[111110]+[220220].                 \tag{A1}
\]

Deleting each unordered pair of sites and enumerating the four-site
matchings gives exactly

\[
\begin{array}{c|l@{\qquad}c|l@{\qquad}c|l}
01&2100&02&1110+2200&03&1010\\
04&2020&05&1211&12&2120\\
13&1100+2020&14&1110&15&2212\\
23&0000&24&0010&25&2222\\
34&0000&35&1111&45&0021+1212.
\end{array}                                                \tag{A2}
\]

Every coefficient in (A2) is one.  Inserting all nine ordered colour
pairs in the two deleted slots produces \(18\cdot9=162\) bilinear atoms.
They collide into \(126\) internal words with multiplicity distribution

\[
                    (m=1,2,3,4)=(96,25,4,1).              \tag{A3}
\]

These facts were reconstructed directly; no table or function from the
primary checker was imported.

## 3. Shared-star equations and absorption of block 67

Write

\[
 p^a_{i,c}=A_{i6}[c,a],\qquad
 q^b_{i,c}=A_{i7}[c,b],\qquad
 r_{ab}=A_{67}[a,b].                                      \tag{A4}
\]

For each boundary slice \((a,b)\), direct matching expansion separates
according to whether \(6\) is paired with \(7\):

\[
 H_{ab}=r_{ab}H_S+
 \sum_{i<j}\sum_{c,d}
 \bigl(p^a_{i,c}q^b_{j,d}+p^a_{j,d}q^b_{i,c}\bigr)
 e_c^{(i)}e_d^{(j)}\otimes H_{S\setminus\{i,j\}}.          \tag{A5}
\]

Thus both endpoint orientations are present and share the same star
variables.  No cross monomial is relaxed to an independent variable.
The first term of (A5) lies in both residual normal spaces,
\(\langle H_S\rangle\) and
\(\langle u_0,u_+\rangle\), so every one of the nine independent
parameters \(r_{ab}\) is genuinely absorbed.  It neither helps nor
obstructs the quotient equations.

After absorption, the audit generated, for every ordered \((a,b)\),

\[
 \beta(p^a,q^b)-\delta_{ab}[a^6]\in N.                    \tag{A6}
\]

All three diagonal fibres retain their coefficient-one pure targets,
and all six ordered off-diagonal fibres retain zero targets.  For
\(N=\langle H_S\rangle\), the four coefficients on the support of
\(H_S\) are equated, giving \(122+3=125\) equations per fibre.  For
\(N=\langle u_0,u_+\rangle\), the coefficient of \(u_0=[002100]\) is
free while the other three are equated, giving \(122+2=124\) equations
per fibre.  The resulting totals are respectively

\[
                          9\cdot125=1125,
 \qquad                    9\cdot124=1116.                 \tag{A7}
\]

## 4. Exact componentwise certificate

Let \(I_c(N)\) be the ideal of diagonal fibre \((c,c)\), including its
target \([c^6]\), and let \(X(N)\) be the ideal of all six ordered
off-diagonal fibres.  A newly emitted Singular program over \(\mathbb Q\),
using a different variable naming and ordering from the primary checker,
computes

\[
\begin{array}{c|ccc|c}
N&\#\min I_0&\#\min I_1&\#\min I_2&\text{triples}\\ \hline
\langle H_S\rangle&9&11&9&891\\
\langle u_0,u_+\rangle&15&13&14&2730.
\end{array}                                                \tag{A8}
\]

For every triple \((P_{0,i},P_{1,j},P_{2,k})\) of minimal components,
the audit forms

\[
                 J=P_{0,i}+P_{1,j}+P_{2,k}+X(N)            \tag{A9}
\]

and checks exactly that \(1\) reduces to zero modulo
\(\operatorname{std}(J)\).  The counts of unit/nonunit bases are

\[
\begin{array}{c|cc}
N&\text{unit}&\text{nonunit}\\ \hline
\langle H_S\rangle&891&0\\
\langle u_0,u_+\rangle&2730&0.
\end{array}                                                \tag{A10}
\]

This exhausts complex solutions: a common zero of a diagonal ideal lies
on at least one of its minimal components, so a solution of all nine
fibres would lie on one of the triples in (A9).  Every such triple is
empty after \(X(N)\) is imposed.  A rational unit certificate remains a
unit certificate after extension to \(\mathbb C\).

## 5. Consequence and executable audit

For the fixed interior, the three possible fourth cuts require precisely
the two audited normal forms: cut \(5\) requires the line, while cuts
\(0\) and \(1\) require the plane.  Equations (A8)--(A10) exclude all
three.  They also explain why the earlier formal three-atom relaxation
is insufficient: that relaxation discards the off-diagonal products
encoded in \(X(N)\).

[verify_three_cut_two_boundary_star_fourth_cut_segre_obstruction_independent_audit.py](../computations/verify_three_cut_two_boundary_star_fourth_cut_segre_obstruction_independent_audit.py)
imports none of the primary checker.  It rebuilds (A1)--(A7), emits both
exact rational component calculations, and verifies every unit
certificate in (A10).

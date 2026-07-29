# A four-site coordinate-monomial multiplier retains at most two colours

## 1. Result

Let \(D=\{0,1,2,3\}\).  At site \(i\), let the three-dimensional
space \(V_i\) have target basis

\[
                 e_0^{(i)},e_1^{(i)},e_2^{(i)},
\]

and work in the site-square-zero algebra

\[
 {\cal R}_D=\bigotimes_{i\in D}(\mathbb C\oplus V_i).
                                                               \tag{1}
\]

Let \(T=\sum_iT_i\) and \(V=\sum_iV_i'\) be arbitrary nonzero linear
forms whose local components are coordinate monomials:

\[
\begin{aligned}
 T_i&=0\quad\hbox{or}\quad \tau_i e_{a_i}^{(i)},\\
 V_i'&=0\quad\hbox{or}\quad \nu_i e_{b_i}^{(i)},
\end{aligned}
\qquad \tau_i,\nu_i\in\mathbb C^*.                         \tag{2}
\]

No support lower bound and no requirement that the used colours be
surjective are imposed.  Put

\[
             X_c=\bigotimes_{i\in D}e_c^{(i)}
             \qquad(0\le c\le2)
                                                               \tag{3}
\]

and consider multiplication by the fixed quadratic \(TV\):

\[
 \mu_{T,V}:({\cal R}_D)_2\longrightarrow({\cal R}_D)_4,
 \qquad Q\longmapsto TVQ.                                    \tag{4}
\]

**Theorem 1.1 (four-site coordinate-monomial obstruction).**
For every choice (2), including arbitrary nonzero complex local weights,

\[
 \#\{c:X_c\in\operatorname {im}\mu_{T,V}\}\le2.               \tag{5}
\]

The bound is sharp.

This gives an exact boundary theorem for the
[isotropic dressed-cap packet](uncontracted-four-cut-isotropic-dressed-cap.md).
At its smallest order \(m=4\), the divided power in the common multiplier
is \(z^{[0]}=1\), so \(F=TV\).  If all three target coefficients \(n_c\)
are nonzero, its three diagonal rows say

\[
 TV\left(x_cy_c+a_{cc}z\right)=n_cX_c.                       \tag{6}
\]

Thus all three tensors (3) would belong to the image (4), contrary to
Theorem 1.1.  Consequently no ternary four-site dressed packet has a
coordinate-monomial pair \(T,V\).  The direct block, the six off-diagonal
rows, and the rank-one form of \(x_cy_c\) are not needed for this
subcase: (4) allows an arbitrary quadratic preimage for each \(X_c\).

The result does not exclude a binary packet on the scalar-matrix-unit
boundary.  Section 5 gives its exact sharp model.

## 2. The two-row column graph

Use the \(81\) coordinate words \(w\in\{0,1,2\}^D\) as a basis of the
top degree.  Fix a two-set \(P\subset D\), a coordinate monomial \(q\)
on \(P\), and write \(D\setminus P=\{i,j\}\).  Only the \(ij\)-part of
\(TV\) can multiply \(q\) without repeating a site:

\[
 (TV)_{ij}=T_iV_j'+V_i'T_j.                              \tag{7}
\]

Under (2), the column \(\mu_{T,V}(q)\) therefore has at most two
coordinate words:

\[
 \tau_i\nu_j\,E_u+\nu_i\tau_j\,E_v.                     \tag{8}
\]

A term is omitted when its required local component is zero.  The two
words have the same coordinates on \(P\); on the complement they are

\[
 (u_i,u_j)=(a_i,b_j),\qquad
 (v_i,v_j)=(b_i,a_j).                                   \tag{9}
\]

Build a graph \(\Gamma(T,V)\) on the top coordinate words.

* A one-word column is a **pin** at that word.
* A two-word column with \(u\ne v\) is a weighted edge \(u-v\).
* If \(u=v\), the column is again a pin unless its two coefficients
  cancel.  If they cancel, the column is simply absent.

Every column of (4) appears in this construction: there are six choices
of \(P\) and nine coordinate monomials on it.

The graph is a complete description of coordinate-vector membership in
the image.  Let \(M\) be its column matrix.  The left-kernel equations
are

\[
 y_u=0\quad\hbox{at a pin},\qquad
 A_{uv}y_u+B_{uv}y_v=0\quad\hbox{on an edge}.            \tag{10}
\]

Since both edge coefficients are nonzero, an unpinned connected
component has either a one-dimensional left kernel, nonzero at every
vertex, or zero left kernel because a cycle has inconsistent gain.
It follows that

\[
 E_w\in\operatorname {im}M
 \quad\Longleftrightarrow\quad
 \begin{array}{l}
 \text{the component of \(w\) contains a nonzero pin, or}\\
 \text{one of its weighted cycles has gain different from \(1\).}
 \end{array}                                             \tag{11}
\]

Indeed, \(E_w\) is in the column space exactly when every vector in
\(\ker M^{\mathsf T}\) vanishes at \(w\).  This proves (11) without
selecting a nonzero summand from a cancelling source expression.

## 3. Arbitrary weights and Laurent gains

On a two-word edge from the first word in (9) to the second, (10) gives

\[
 y_v=-{\tau_i\nu_j\over\nu_i\tau_j}y_u
     =-{\rho_i\over\rho_j}y_u,
 \qquad \rho_k={\tau_k\over\nu_k}.                       \tag{12}
\]

Every component required in (12) is nonzero because otherwise that
column would have only one word.  Along a cycle of length \(L\), the
successive ratios telescope to a signed Laurent monomial

\[
                    (-1)^L\prod_{k=0}^3\rho_k^{\kappa_k},
 \qquad \kappa_k\in\mathbb Z.                            \tag{13}
\]

Thus the cycle can be tracked exactly by the pair

\[
              \left(L\bmod2,(\kappa_0,\kappa_1,\kappa_2,\kappa_3)\right).
                                                               \tag{14}
\]

If (14) is \((0,(0,0,0,0))\), the cycle is balanced for every choice
of weights.
If it is nonzero, the cycle may or may not become balanced after a
specialization of the \(\rho_i\).  Declaring every such cycle
inconsistent therefore gives an **upper bound** on coordinate-vector
membership, uniformly over all nonzero complex weights.

The same monotonicity handles coincident words.  Their prospective pin
has coefficient

\[
                         \tau_i\nu_j+\nu_i\tau_j.        \tag{15}
\]

It is nonzero generically but may cancel at special weights.  Such a
cancellation removes a column and can only shrink the image.  In the
weight-uniform upper audit it is therefore sound to retain every
coincident-word column as a candidate pin.

## 4. The finite pattern lemma

Encode a local component by one of four symbols: absent, colour zero,
colour one, or colour two.  Excluding the all-absent form gives

\[
                              4^4-1=255                 \tag{16}
\]

patterns for each of \(T,V\).

There is a useful reduction before any census.  If \(X_c\) belongs to
the image, its nonzero \(X_c\)-coefficient must use a colour-\(c\)
component of \(T\) and a colour-\(c\) component of \(V\).  Therefore,
if all three \(X_c\)'s belonged to the image, each pattern would use all
three colours.  On four sites there are exactly

\[
       4\cdot3!+
       \left(3^4-3\cdot2^4+3\right)=24+36=60            \tag{17}
\]

such patterns: a three-site bijection or a four-site surjection.

For all \(60^2\) pairs, apply (11) with candidate pins and the symbolic
cycle labels (14).  The exact profiles are

\[
\begin{array}{c|c}
\text{symbolically possible target set}&\text{ordered pattern pairs}\\ \hline
\varnothing&432\\
\{c\}&768\quad\text{for each }c\\
\{c,d\}&288\quad\text{for each pair }\{c,d\}\\
\{0,1,2\}&0.
\end{array}                                             \tag{18}
\]

Because numerical membership is contained in this symbolic upper
profile, the last row proves Theorem 1.1 for arbitrary weights.

As a separate guard, the checker exhausts all \(255^2=65{,}025\)
unweighted pairs, not only the reduced list (17).  It finds

\[
\begin{array}{c|c}
\text{actual unweighted target set}&\text{ordered pattern pairs}\\ \hline
\varnothing&14{,}502\\
\{c\}&13{,}749\quad\text{for each }c\\
\{c,d\}&3{,}092\quad\text{for each pair }\{c,d\}\\
\{0,1,2\}&0.
\end{array}                                             \tag{19}
\]

The agreement of the reduced unweighted profiles with (18) is an
additional check that no parity or orientation was lost in the Laurent
audit.

## 5. Binary sharpness

On the four cyclic sites put

\[
\begin{aligned}
 T&=e_0^{(0)}+e_1^{(1)},&
 V&=e_0^{(1)}+e_1^{(2)},\\
 Q_0&=e_0^{(2)}e_0^{(3)},&
 Q_1&=e_1^{(3)}e_1^{(0)}.
\end{aligned}                                           \tag{20}
\]

Square-freeness leaves exactly one assignment in each product:

\[
                         TVQ_0=X_0,\qquad TVQ_1=X_1.    \tag{21}
\]

This is the row-resolved form of the
[binary four-cycle guard](uncontracted-four-cut-isotropic-dressed-cap.md#51-a-binary-four-star-identity).
It proves that the upper bound two in (5) is exact.  In particular,
Theorem 1.1 cannot be strengthened to close the scalar-matrix-unit
binary packet.

## 6. Scope and audit

The coordinate-monomial hypothesis in (2) is essential to the proof:
it makes every column have at most two coordinate words.  A local
superposition of target axes produces larger columns, for which the
graph and gain criterion no longer applies.  The theorem is also a
four-site statement; it does not replace the higher-order divided-power
analysis.

The dependency-free checker
[verify_four_site_coordinate_monomial_dressed_packet_obstruction.py](../computations/verify_four_site_coordinate_monomial_dressed_packet_obstruction.py)
reconstructs every column from (7)--(9), checks the complete ledger
(19), performs the symbolic Laurent-gain upper audit (18), and verifies
the sharp binary profile.  It uses no polynomial solver and introduces
no random or numerical step.

# The five-face zero locus is a nonzero square-zero slice, but the existing packet cannot route it

Research boundary only.  This note sharpens the exact physical landing left
by the selected-denominator separator.  It does not construct a full source
on the landing and does not prove the unified overlap theorem.

## Exact square-zero interpretation

Fix the five-site decorated word

\[
                              m=12112
\]

and let \(q_m\) be the scalar quadratic consisting of the ten internal cells
whose endpoint decorations are prescribed by \(m\).  In the commutative
site-square-zero algebra, the coefficient of the four-site basis word
missing site \(v\) in the divided square \(q_m^{[2]}\) is exactly

\[
 h_v=\operatorname {Haf}(q_m|_{D\setminus\{v\}}).
\]

Consequently

\[
       h_1=\cdots=h_5=0\quad\Longleftrightarrow\quad q_m^{[2]}=0. \tag{1}
\]

Equation (1) is useful, but it is not an inactive-root statement.  The
square-zero quadratic can be dense and nonzero.

Normalize the five cycle edges

\[
             12,23,34,45,15
\]

to one by vertex scaling, and write \(A,B,C,D,E\) for the chords
\(13,14,24,25,35\).  Saturating by \(ABCDE\), the five equations (1) have
the exact lexicographic standard basis

\[
\begin{split}
 E^2+E+1,\quad D-E,\quad C-D,\quad B-C,\\
 A+BE+1,\quad t-E,
\end{split}                                                   \tag{2}
\]

where \(tABCDE-1\) implements saturation.  Thus on the dense torus

\[
       A=B=C=D=E=\zeta,
       \qquad \zeta^2+\zeta+1=0.                            \tag{3}
\]

There are exactly two geometric normalized points, the two primitive cube
roots.  Every one of the ten cells of \(q_m\) is nonzero.  Hence the
simultaneous face-zero stratum contains a genuinely dense, nonzero
square-zero slice; neither \(q_m=0\) nor source inactivity follows from
(1).

The checker gives a rational lift matrix proving (2) from the five face
equations and the saturation equation.  Conversely it reduces every source
equation by (2); the leading monomials
\(E^2,D,C,B,A,t\) are pairwise coprime, so the product criterion certifies
the standard basis without a runtime CAS.

## What the labelled anchors and crossed row do

The exact two-chart static block formed by two diagonal anchors, the direct
table, and the crossed zero row has determinant

\[
                                -3.                       \tag{4}
\]

It therefore closes the static label transport completely.  This is not the
missing operation.  All connection, normal, and curvature rows in that
packet preserve the decorated endpoint word.  The physical face needed by
the order-four comparison lies at

\[
 (x,v,p,q)=(0,m_v,2,2),
\]

whereas the zero-endpoint lower face needed for the clean/inactive landing
lies at

\[
 (x,v,p,q)=(0,0,0,0).                                    \tag{5}
\]

For every one of the five faces, the two words in (5) are different and
remain different under all six global colour permutations.  Fixed-label K4
curvature decomposes into 81 disjoint three-matching components, one for
each decorated four-site word, so no combination of those rows crosses
(5).  The selected curvature scalar can already be a unit
\(\kappa=AU-BF=1\); localization at \(\kappa\) does not alter this grading.

Thus the currently proved packet permits the bounded source-grade datum

\[
       \kappa\ne0,\qquad q_m\ne0,\qquad q_m^{[2]}=0,     \tag{6}
\]

without supplying either a scalar-zero clean cap or an inactive-root
landing.  The old split-cap landing also locks q-augmentation to ordinary
residue, so it cannot be silently substituted for the absent word-changing
face.

## Exact consequence and stopping rule

The proposed shortcut

\[
 V(h_1,\ldots,h_5)
       \Longrightarrow q_m=0\text{ or an already closed inactive/clean branch}
\]

does not follow from the square-zero equation, curvature localization, or
the completed anchor/crossed static block.  The cyclotomic stratum (3) is an
exact counterguard to that bounded inference.  It is **not** a full physical
source point: unexamined Hamming-two and other full-word coefficients may
still exclude it.

The remaining proof-level input is now precise.  One needs either

1. a literal full-nine/Hamming-two source identity that changes the selected
   mixed endpoint word in (5) to the zero/anchor word while preserving target
   and ordinary residue; or
2. a source theorem showing that the complete physical rootless packet
   cannot realize the cyclotomic square-zero slice (3).

Another scalar Tor membership, static selector rank, or fixed-label
curvature calculation cannot provide this landing.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_square_zero_slice_routing_boundary.py
.venv/bin/python -O computations/verify_h3_component_iv_square_zero_slice_routing_boundary.py
```

The dependency-free checker proves the saturated standard basis by exact
rational lift and reduction, verifies the cyclotomic point in
\(\mathbb Q(\zeta)\), recomputes the static determinant, and audits all five
word bridges under all target-colour permutations.  It pins the selected
membership separator, the prior face-zero routing boundary, the two-chart
Fitting calculation, and the physical curvature word-change obstruction.

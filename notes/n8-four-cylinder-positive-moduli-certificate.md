# A symbolic four-cylinder certificate for the positive-moduli N=8 strata

## Outcome

All 1,873 positive-dimensional two-cell character families left open by
[the orbit-feasibility audit](n8-four-cut-two-cell-orbit-feasibility.md)
are excluded for arbitrary nonzero complex weights.  The certificate is
symbolic and source-faithful: it uses coefficient slices of the literal
cofactor maps and high-sector residual rows, not samples of coefficients and
not an invariant of the final output tensor.

Together with the zero-dimensional orbit search, this proves the following
local statement.  Starting from the anchored sixteen-source N=8 family, no
addition at two distinct previously absent aggregate coordinates, with
arbitrary complex weights, preserves the three pure anchors and complete
active cuts \(z=2,3,4\) while acquiring a fourth complete active cut in
\(z=0,1,5\).

This remains a theorem about the anchored two-cell neighbourhood.  It does
not cover reweighting its sixteen occupied coordinates, three-cell additions,
other anchor families, or all even orders.

## 1. The coefficient-cylinder construction

For a rank-one quotient-character pair, the stabilizing diagonal torus
normalizes one nonzero weight to one; write the remaining invariant
coefficient as \(t\).  A rank-zero pair retains both coefficients \(t,s\).
Thus these parameterizations cover the full nonzero complex orbit strata,
not merely a chosen affine slice.

Fix a cut \(z\), and let \(c_k(t)\), \(1\leq k\leq15\), be its labelled
five-site insertion columns for a rank-one character family.  Let \(r_b(t)\)
be the high-sector residual row indexed by the boundary word \(b\).  A
matching uses the variable added cell at most once, so

\[
             c_k(t)=c_{k,0}+t c_{k,1},\qquad
             r_b(t)=r_{b,0}+t r_{b,1}.                    \tag{1}
\]

Define the parameter-independent coefficient cylinder

\[
 {\cal U}_z=
 \operatorname{span}_{\mathbb Q}
 \{c_{k,0},c_{k,1}:1\leq k\leq15\}.                       \tag{2}
\]

The actual insertion space at every parameter lies in \({\cal U}_z\).
Consequently complete high-sector membership forces

\[
 \bar r_{b,0}+t\bar r_{b,1}=0
 \quad\text{in}\quad
 \mathbb Q^{243}/{\cal U}_z                              \tag{3}
\]

for every boundary row.  Each nontrivial vector equation in (3) has no
solution, one rational solution, or is identically zero.  Intersecting these
conditions over the three fixed cylinders gives an exact family-wide
certificate.

The checker reconstructs (1) at \(t=0,1,2\) coefficient by coefficient before
using it.  Thus the calculation is an exact symbolic elimination of \(t\);
the three values audit multilinearity and are not a coefficient search.

## 2. Rank-one closure

The 1,858 rank-one character pairs split as follows:

| coefficient-cylinder condition on cuts \(2,3,4\) | families |
|---|---:|
| inconsistent for every \(t\) | 1,737 |
| forces \(t=0\) | 108 |
| forces \(t=1\) | 2 |
| all projected equations vanish identically | 11 |

The \(t=0\) cases lie on the already closed one-cell boundary.  The two
\(t=1\) families are

\[
\begin{aligned}
 E_{35;11}+tE_{45;01},\\
 E_{35;12}+tE_{45;02}.
\end{aligned}
\]

Literal exact reconstruction at \(t=1\) shows that cut \(z=2\) fails, so
neither is a four-cut repair.

### The nine maximal-minor certificates

Nine of the eleven coefficient-invisible families are detected by actual
cofactor-span minors.  At \(t=1\), the checker selects independent labelled
cofactor columns and a residual row outside their span.  If their generic
cofactor rank is fourteen, all \(15\times15\) cofactor minors are checked to
vanish at sixteen distinct rational parameters.  Each such minor has degree
at most fifteen, so this proves the symbolic rank ceiling fourteen.  Rank
fifteen needs no auxiliary ceiling because there are only fifteen labelled
columns.

The selected augmented determinant has degree at most sixteen.  Its exact
coefficient polynomial is reconstructed from consecutive rational values and
checked at one additional value.  Membership in the relevant cut cylinder
forces every selected determinant to vanish.  Taking their monic gcds gives

| gcd of necessary minors | families |
|---|---:|
| \(t\) | 3 |
| \(t^2\) | 1 |
| \(t^4\) | 1 |
| \(t^5\) | 2 |
| \(t^4(t+1)\) | 2 |

The first seven families, represented by the first four gcd types, force the
excluded boundary \(t=0\).  For the last two families, exact reconstruction
at the only additional root \(t=-1\) shows that cut \(z=4\) fails.  This
closes all nine without assuming that a rank computed at a generic parameter
persists at exceptional roots.

### The two flat fixed-cut families

Two families are genuinely invisible to both the coefficient-cylinder
quotient and the fixed-cut minors:

\[
 E_{23;01}+tE_{23;20},
 \qquad
 E_{67;02}+tE_{67;10}.                                  \tag{4}
\]

The fixed-cylinder coefficient projection gives no parameter equation, and
at the determinant selection point every residual row lies in the actual
fixed-cut cofactor spans.  No assertion about the fixed cuts at other
parameters is needed.  Repeating (2)--(3) separately on each possible fourth
cut \(z=0,1,5\) gives an inconsistent affine equation for every one of the
six family-cut combinations.  Hence no parameter in (4) enters even one
fourth cofactor cylinder, so neither family can contain a countermodel.

## 3. Rank-zero bilinear closure

The rank-zero stratum consists of the fifteen pairs among the six
zero-character coordinates found by the one-cell audit.  Write their weights
as \(t,s\).  Every column and residual row is bilinear:

\[
c_k(t,s)=c_{k,00}+t c_{k,10}+s c_{k,01}+ts c_{k,11},      \tag{5}
\]

and similarly for \(r_b(t,s)\).  Replace (2) by the span of all four
coefficient slices.  Projection of the residual rows then gives scalar
necessary equations of the form

\[
                       a+bt+cs+dts=0.                    \tag{6}
\]

For ten pairs there are two distinct primitive equations and for five pairs
there are three.  In every one of the fifteen families, the exact projected
equation set contains

\[
                              t=0.                        \tag{7}
\]

This contradicts the required nonzero weight immediately.  Equivalently, the
Laurent saturation by \(ts\) is the unit ideal.  The checker verifies (5) at
the additional point \((t,s)=(2,3)\) for every labelled column and residual
row before extracting (7).

## 4. What stabilizes under N to N+2

The **form** of the certificate is stable.  At any even order \(N\), a
three-site boundary leaves an odd shore \(U\) of size \(N-3\).  Its labelled
insertion map has \(3(N-3)\) columns

\[
 V_u\otimes H_{U\setminus\{u\}},
 \qquad u\in U.
\]

For \(q\) added cells, perfect matchings are multiaffine in their weights, so
the universal coefficient cylinder is always the span of at most \(2^q\)
coefficient slices of these same labelled columns.  Projecting source-built
residual rows into its quotient and coupling several cuts therefore makes
sense unchanged after adjoining two vertices.

The **numerical certificate** does not yet stabilize.  The ranks fourteen and
fifteen, the particular rows, and the minor gcds above use the N=8 anchored
support.  At \(N+2\), the number of labelled columns grows by six and no
compatible lift of this anchor has been proved to preserve the same quotient
rows or gcd factors.  A uniform theorem now needs one of:

1. a contraction from the \(N+2\) coefficient cylinders to these N=8
   quotient equations; or
2. a local row functional whose support and nonzero affine or bilinear
   coefficient are unchanged by adding a matched vertex pair.

So the construction supplies a credible N-stable language for a
four-cylinder identity, but this computation alone is not an induction in
the order.

## Reproduction

    python3 computations/verify_n8_four_cylinder_positive_moduli_certificate.py
    python3 -O computations/verify_n8_four_cylinder_positive_moduli_certificate.py
    python3 -I computations/verify_n8_four_cylinder_positive_moduli_certificate.py
    python3 -S computations/verify_n8_four_cylinder_positive_moduli_certificate.py

The checker uses only the Python standard library and exact rational sparse
row reduction.  Raising checks are used throughout, so optimized mode does
not weaken the certificate.

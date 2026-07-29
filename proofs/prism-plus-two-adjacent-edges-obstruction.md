# Prism plus two adjacent complementary pairs

Let

\[
 P=\{03,04,05,12,14,15,23,24,35\}
\]

be the triangular prism on vertices `0,...,5`.  Its complement is the cycle

\[
 01,13,34,45,25,02.
\]

This note treats two adjacent edges of that cycle.

**Theorem.**  Suppose the only possibly nonzero aggregate edge matrices are
on

\[
 P\cup\{01,13\}.                                             \tag{1}
\]

Even if all eleven allowed matrices are arbitrary asymmetric `3 by 3`
complex matrices, their six-site matching tensor cannot equal
`Delta_(6,3)`.  By relabeling, the same holds for any two adjacent edges of
the complementary six-cycle.

**Proof.**  Vertices `2,4,5` have exactly three allowed neighbors.  The
cubic-vertex lemma proved in
`proofs/prism-plus-one-edge-obstruction.md` therefore applies at these three
vertices.  It says that every edge incident to one of them is a nonzero
same-color rank-one basis edge, and that its three incident colors are
distinct.  Thus the eight matrices on

\[
 12,23,24,04,14,05,15,35                                   \tag{2}
\]

have the form `w_e E_(kappa(e),kappa(e))`, with `w_e != 0`.
Only the three matrices on the triangle `01,03,13` remain arbitrary.

Permute the colors so that properness at vertex 2 reads

\[
 \kappa(12)=0,\qquad \kappa(23)=1,\qquad \kappa(24)=2.       \tag{3}
\]

Put

\[
 b=\kappa(04),\quad e=\kappa(14),\quad
 c=\kappa(05),\quad f=\kappa(15),\quad i=\kappa(35).
\]

Properness at vertices 4 and 5 gives

\[
 \{b,e\}=\{0,1\},\qquad \{c,f,i\}=\{0,1,2\}.              \tag{4}
\]

The allowed graph has exactly the following six perfect matchings:

\[
\begin{array}{lll}
 N_{01}=\{01,24,35\},&N_{03}=\{03,15,24\},
   &N_{13}=\{05,13,24\},\\
 M_B=\{04,12,35\},&M_D=\{04,15,23\},
   &M_C=\{05,14,23\}.
\end{array}                                                   \tag{5}
\]

The first row contains the three arbitrary triangle matrices.  Crucially,
all three matchings in that row also contain the forced color-2 edge `24`.
Every coefficient they contribute therefore lies on the coordinate slice

\[
 c_2=c_4=2.                                                  \tag{6}
\]

The matching `M_B`, on the other hand, has the single nonzero basis
coefficient at

\[
 (b,0,0,i,b,i).                                              \tag{7}
\]

It is outside (6), and the other two pure matchings have color 1 rather than
0 at vertex 2, so no other term has the coloring (7).  Its coefficient is
the product of three nonzero scalars from (2).  Consequently (7) must be a
target coloring, hence constant.  This forces

\[
 b=i=0.                                                       \tag{8}
\]

Equation (4) then gives `e=1` and `{c,f}={1,2}`.  Now `M_D`
has the nonzero basis coefficient

\[
 (0,f,1,1,0,f).                                              \tag{9}
\]

This coloring is mixed, is outside (6), and cannot equal the coloring of
`M_C=(c,1,1,1,1,c)` because `c` is either 1 or 2 whereas the first
coordinate of (9) is 0.  Thus (9) is a uniquely supported nonconstant
coefficient and cannot vanish.  This contradicts the target tensor.

The complementary graph is a six-cycle, whose automorphism group is
transitive on adjacent edge pairs.  Relabeling proves the final assertion.
QED.

The argument leaves `A_01,A_03,A_13` completely arbitrary; their entries
are excluded only by the exact source-dependent slice (6), not by a
rank-one assumption.


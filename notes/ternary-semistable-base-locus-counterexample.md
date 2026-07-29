# The ternary matching base locus contains semistable points

## 1. Exact counterexample

Let (B=\{0,1,2,3,4,5\}), let every local colour space be
(V_i=\mathbb C^3), and put

\[
 A_{ij}=I_3\quad\text{for }ij\in
 \{01,02,12,34,35,45\},
 \qquad A_{ij}=0\quad\text{otherwise}.                 \tag{1}
\]

Thus the nonzero support graph is (K_3\sqcup K_3).  It has no perfect
matching: every matching leaves at least one vertex of each odd component
uncovered.  Consequently

\[
                         H_6(A)=0.                       \tag{2}
\]

Nevertheless (A) is semistable for the natural action of

\[
                         G=\prod_{i=0}^5SL(V_i).         \tag{3}
\]

Indeed, the polynomial

\[
 D(A)=\prod_{ij\in\{01,02,12,34,35,45\}}\det A_{ij}    \tag{4}
\]

is a homogeneous (G)-invariant.  Under
(A_{ij}\mapsto g_iA_{ij}g_j^{\mathsf T}), each determinant is multiplied
by ((\det g_i)(\det g_j)=1).  At (1), (D(A)=1\ne0).  The invariant
criterion for the null cone therefore makes (1) semistable.

This is already a ternary, six-site source with full-rank nonzero blocks;
it is not the one-dimensional scalar degeneration used in the earlier
nonarchimedean audit.

## 2. Consequence for reduction modulo two

A proposed nonarchimedean bridge cannot prove base-locus avoidance merely
by arranging a semistable special source.  Semistability of the source does
not imply that its matching tensor is nonzero, even for (q=3,n=6) and
even when every nonzero aggregate block is invertible.  Any successful
semistable-replacement argument must retain a nonvanishing invariant pulled
back from the *target*, or impose an additional condition excluding odd
support components; arbitrary source semistability is insufficient.

The exact audit is
[`verify_ternary_semistable_base_locus.py`](../computations/verify_ternary_semistable_base_locus.py).


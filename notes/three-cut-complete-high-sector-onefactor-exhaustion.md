# Three complete cuts: exact one-factor exhaustion at order eight

## 1. Result and scope

Let \(B=S\mathbin{\dot\cup}R\), with \(|S|=6\) and \(|R|=2\).  Take three
perfect matchings \(M_0,M_1,M_2\) of \(B\), and put the diagonal tensor
\(e_r\otimes e_r\) on every edge of \(M_r\).  The matchings may overlap;
an edge shared by several factors carries the sum of their diagonal colour
tensors.  All other aggregate edge blocks are zero.

**Proposition 1.1.**  Among the six cuts

\[
 C_z=R\cup\{z\},\qquad U_z=S\setminus\{z\},\qquad z\in S,
\]

at most two can simultaneously have both

\[
 \left.(T_{3,z})^\flat\right|_{K_{U_z}}
       =\left.\iota_{C_z}\delta_{U_z}\right|_{K_{U_z}}
 \quad\hbox{and}\quad
 \delta_{U_z}(K_{U_z})\ne0.                                \tag{1}
\]

The bound is sharp.  There are 264 normalized records attaining two when
\(M_0\) has no \(R\mid S\) crossing edge and 64 when \(M_0\) has two.
The model in
[the complete two-cut countermodel](adjacent-five-cut-complete-high-sector-countermodel.md)
is one such sharp record.

This is an exact exhaustion of the smallest shared one-factor family, not
a three-cut theorem for arbitrary aggregate edge tensors.  It therefore
supports, but does not prove, the current global target: three complete
cuts are the first overlap level not already defeated by this family.

## 2. Exact linear test

For a five-set \(U\), form the complete cofactor-insertion space

\[
 {\cal S}_U=\sum_{u\in U}V_u\otimes H_{U\setminus\{u\}},
 \qquad K_U={\cal S}_U^\perp.                               \tag{2}
\]

After flattening on \(C_z\mid U_z\), identity (1) holds on the whole of
\(K_{U_z}\) exactly when every \(U_z\)-row of

\[
                         T_{3,z}-\Delta_{B,3}                \tag{3}
\]

belongs to \({\cal S}_{U_z}\).  This is a rational column-membership test
in the 243-dimensional coordinate space on \(U_z\), with at most fifteen
cofactor-insertion columns.  Moreover

\[
 \delta_{U_z}(K_{U_z})\ne0
 \quad\Longleftrightarrow\quad
 \dim\bigl({\cal S}_{U_z}+\langle e_0^{\otimes U_z},
 e_1^{\otimes U_z},e_2^{\otimes U_z}\rangle\bigr)
       >\dim{\cal S}_{U_z}.                                  \tag{4}
\]

Thus (1) is checked without constructing a basis of the typically large
annihilator \(K_{U_z}\).

## 3. Exhaustive normalization

A perfect matching has either zero or two crossing edges across
\(R\mid S\).  The shore-preserving permutation group is transitive on
each type, so the color-zero factor may be normalized to exactly one of

\[
 \begin{aligned}
 M_0^{(0)}&=01,23,45,67,\\
 M_0^{(2)}&=06,17,23,45.
 \end{aligned}                                               \tag{5}
\]

For each representative, there are
\(\binom{105+1}{2}=5565\) unordered pairs with repetition
\(\{M_1,M_2\}\).  This includes every overlap with \(M_0\), with each
other, or both.  Swapping colors one and two preserves (1), so these two
scans exhaust the stated family up to the permitted normalization.  Exact Gaussian elimination
over \(\mathbb Q\) applies (3)--(4) on all six cuts of every record.  The
largest number of active complete cuts is two in both scans.

## 4. Exact audit

[`search_three_cut_complete_high_sector_onefactor_families.py`](../computations/search_three_cut_complete_high_sector_onefactor_families.py)
enumerates all perfect matchings recursively, including every colour choice
on shared edges, expands every four- and eight-site matching tensor,
performs every membership and defect-rank test over `fractions.Fraction`,
and prints both normalized scan counts, both maxima, and representatives attaining
equality.  Its finite-field routines are retained only for optional
reconnaissance; the exhaustive result uses the exact branch on every record.

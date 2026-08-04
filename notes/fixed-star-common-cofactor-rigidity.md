# Fixed-star rigidity when the common cofactors are diagonal

This note isolates an exact branch of the fixed-vertex equations.  The
point is that the tensors appearing at the different ports are not arbitrary
slices: they are complementary hafnians of one common edge system.  In the
branch treated here, however, entry-minimality and coefficient separation
already force the entire star to be the three expected monochromatic ports.
The only branch left open has a genuinely mixed complementary hafnian.

Let `B` have even cardinality `n >= 6`, let

\[
 H_B(A)=\sum_{M\in\operatorname {PM}(B)}\bigotimes_{uv\in M}A_{uv}
        =\Delta_{B,3}:=\sum_{c=0}^2e_c^{\otimes B},          \tag{1}
\]

and fix a vertex `p`.  Put `J=B\setminus\{p\}` and, for `j in J`, define
the complementary tensor

\[
 C_j=H_{B\setminus\{p,j\}}(A).                              \tag{2}
\]

The endpoint-`p` row of `A_{pj}` is denoted

\[
 r_{j,c}=(e_c^*\otimes\operatorname{id})A_{pj}
         =\sum_{l=0}^2 a_{j,c,l}e_l^{(j)},                  \tag{3}
\]

with the tensor factors put in this order regardless of the numerical order
of `p,j`.  Expanding (1) at the unique matching edge incident with `p` gives
the three **common-cofactor star equations**

\[
 \sum_{j\in J}r_{j,c}^{(j)}\otimes C_j=e_c^{\otimes J},
 \qquad c=0,1,2.                                            \tag{4}
\]

## 1. The local use of entry-minimality

Call a solution of (1) **entry-minimal** if it has the fewest nonzero
aggregate scalar matrix entries among all solutions of (1).  For every
nonzero incident entry form its unweighted global derivative tensor

\[
 T_{j,c,l}=e_c^{(p)}\otimes e_l^{(j)}\otimes C_j.            \tag{5}
\]

**Lemma 1 (star irredundancy).**  At an entry-minimal solution, all tensors
(5) indexed by nonzero entries `a_{j,c,l}` are linearly independent.  In
particular, `C_j` is nonzero whenever `A_{pj}` is nonzero.

**Proof.**  Every perfect matching uses exactly one edge incident with `p`.
Consequently the full tensor is linear, with no cross terms, in simultaneous
perturbations of all entries incident with `p`.  A dependence among (5)
therefore gives a perturbation supported only on currently nonzero entries
which leaves (1) unchanged for every value of its parameter.  Choose the
parameter to make one entry zero.  No zero entry becomes nonzero, contradicting
entry-minimality.  A zero tensor among (5) is already a dependence.
\(\square\)

This is the only minimality input below.

## 2. Classification of a diagonal-cofactor star

Let

\[
 D_S=\operatorname{span}\{e_0^{\otimes S},e_1^{\otimes S},
                           e_2^{\otimes S}\}.
\]

**Theorem 2 (diagonal-cofactor star rigidity).**  Suppose (1) is
entry-minimal and every active complementary tensor at `p` is diagonal:

\[
 A_{pj}\ne0\quad\Longrightarrow\quad
 C_j\in D_{B\setminus\{p,j\}}.                              \tag{6}
\]

Then `p` has exactly three active neighbours `j_0,j_1,j_2`.  There are
nonzero scalars `gamma_0,gamma_1,gamma_2` such that

\[
 C_{j_l}=\gamma_l e_l^{\otimes(B\setminus\{p,j_l\})},
 \qquad
 A_{p j_l}=\gamma_l^{-1}e_l^{(p)}\otimes e_l^{(j_l)},
 \quad l=0,1,2,                                             \tag{7}
\]

and every other `A_{pj}` is zero.

**Proof.**  Fix an active `j` and write

\[
 C_j=\sum_{r=0}^2\gamma_{j,r}
                    e_r^{\otimes(J\setminus\{j\})}.         \tag{8}
\]

Choose a nonzero incident cell `a_{j,c,l}`.  For `r != l`, inspect in the
row-`c` equation (4) the coefficient of the coloring which is `l` at `j`
and `r` at every other vertex of `J`.  The term indexed by `j` contributes

\[
                         a_{j,c,l}\gamma_{j,r}.              \tag{9}
\]

No term indexed by `k != j` contributes: its diagonal cofactor sees both
the color `l` at `j` and the color `r` at least one vertex of
`J\setminus\{j,k\}`.  That latter set is nonempty since `n >= 6`.  The
target coefficient is zero, so (9) vanishes.  Thus
`gamma_{j,r}=0` for every `r != l`.

Lemma 1 makes `C_j` nonzero, hence `gamma_{j,l} != 0`.  Repeating the same
coefficient test for any second nonzero cell in a column `l' != l`, now with
`r=l`, would give

\[
                         a_{j,c',l'}\gamma_{j,l}=0.
\]

Therefore all entries of `A_{pj}` lie in the single endpoint-`j` column
`l`, and for some nonzero `gamma_j`

\[
              A_{pj}=a_j\otimes e_l^{(j)},\qquad
              C_j=\gamma_j e_l^{\otimes(J\setminus\{j\})}. \tag{10}
\]

Write `sigma(j)=l`.  The derivative tensor (5) of a nonzero row-`c` entry
on this edge is now

\[
                 \gamma_j e_c^{(p)}\otimes e_l^{\otimes J}.
\]

For fixed `(c,l)` these tensors are proportional.  Lemma 1 therefore says
that at most one of the scalars `a_{j,c,l}` with `sigma(j)=l` is nonzero.
The coefficient of `e_l^{\otimes J}` in (4) is exactly

\[
       \sum_{j:\,\sigma(j)=l}\gamma_j a_{j,c,l}=\delta_{c,l}.
                                                                    \tag{11}
\]

Because (11) has at most one nonzero summand, all off-diagonal rows
`c != l` vanish, while for `c=l` there is exactly one summand and its value
is one.  This gives one distinct active neighbour for each `l`, and (7)
follows. \(\square\)

The proof uses the actual common cofactors only through (2)--(4); it does
not replace them by independently selectable slice tensors.

## 3. Consequence if every star is in this branch

**Corollary 3.**  An entry-minimal realization of \(\Delta_{B,3}\) cannot have
the diagonal-cofactor property (6) at every vertex.

**Proof.**  If it did, Theorem 2 would give at every vertex exactly one
incident nonzero `00` cell, one `11` cell, and one `22` cell.  The cells of
each color consequently form a perfect matching `P_0,P_1,P_2`, and the
three matchings are edge-disjoint.

For `n >= 6`, the standard three-one-factors lemma gives a fourth perfect
matching `M` in \(P_0\cup P_1\cup P_2\).  Color each vertex by the color
of its edge in `M`.  This coloring is mixed, since an all-`l` matching would
be the unique matching `P_l`.  It also has exactly one compatible matching:
at a vertex of color `l`, its unique compatible incident cell is its
`P_l`-edge.  Hence its coefficient in (1) is the nonzero product of the
cells of `M`, contradicting the zero mixed coefficient of
\(\Delta_{B,3}\).  \(\square\)

*Attribution.*  The three-one-factors lemma is **Bogdanov's observation**
(Bogdanov 2017), published as Thm 1 of Chandran-Gajjala,
arXiv:2202.05562, and in multigraph form as Thm 1.7 of
Chandran-Gajjala-Illickan, arXiv:2407.00303; see
[`references/REFERENCES.md`](../references/REFERENCES.md).  No priority is
claimed for it here.

Thus a hypothetical entry-minimal source has at least one vertex `p` and
one active neighbour `j` for which

\[
 C_j\notin D_{B\setminus\{p,j\}}.                            \tag{12}
\]

More locally, any star with more than three active neighbours must contain
such a genuinely mixed cofactor.  Controlling this mixed-cofactor branch is
the remaining fixed-star problem.  Its quotient relations, second-center
defect chase, and six-site separator criterion are developed in
[`notes/fixed-star-mixed-cofactor-chase.md`](fixed-star-mixed-cofactor-chase.md).

## 4. Why irredundancy cannot be dropped: an actual shared-edge example

The common origin of the cofactors does not by itself prevent wrong-color
cancellation.  On vertices `1,...,6`, use two colors and the following
aggregate tensors (the smaller endpoint is written first):

\[
\begin{array}{c|c}
12&(e_0+e_1)\otimes e_0\\
34,56,24&e_0\otimes e_0\\
13&-e_1\otimes e_0\\
16,23,45&e_1\otimes e_1.
\end{array}                                                   \tag{13}
\]

Its only supported perfect matchings are

\[
 12|34|56,\qquad13|24|56,\qquad16|23|45,                    \tag{14}
\]

and their sum is exactly
\(e_0^{\otimes6}+e_1^{\otimes6}\).
At `p=1`, all three active cofactors are computed from the same internal
edge system:

\[
 C_2=e_0^{\otimes4},\qquad C_3=e_0^{\otimes4},\qquad
 C_6=e_1^{\otimes4}.                                        \tag{15}
\]

The two star rows are therefore

\[
\begin{aligned}
 e_0^{(2)}\otimes C_2&=e_0^{\otimes5},\\
 e_0^{(2)}\otimes C_2-e_0^{(3)}\otimes C_3
        +e_1^{(6)}\otimes C_6&=e_1^{\otimes5}.              \tag{16}
\end{aligned}
\]

The first two terms in the second line cancel after their tensor slots are
restored.  This is a genuine hafnian source, including the shared internal
edge `56`, rather than an abstract assignment of separate slices.

There is no conflict with Theorem 2.  The derivative tensors belonging to
the `(1,0)` cells on `12` and `13` are identical, so Lemma 1 fails.  Deleting
both of those cells leaves the two monochromatic matchings and the same
binary target.  Thus entry-minimality is exactly what forbids this
cancellation in the diagonal-cofactor branch.

The audit
[`computations/verify_fixed_star_binary_cofactors.py`](../computations/verify_fixed_star_binary_cofactors.py)
checks all 64 coefficients, computes the three cofactors from the common
edge dictionary, verifies (16), and verifies the support-reducing deletion.

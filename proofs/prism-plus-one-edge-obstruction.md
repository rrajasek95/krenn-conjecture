# Exact obstruction on the prism plus one arbitrary extra pair

This note extends the arbitrary-matrix prism proposition: adjoining any one
of the six missing underlying pairs still cannot produce
`Delta_(6,3)`, even when every allowed pair carries an arbitrary asymmetric
`3 by 3` complex matrix.

## 1. Rigidity at a cubic vertex

Let every site have color space `V=C^3`, with basis `e_0,e_1,e_2`.

**Cubic-vertex lemma.**  Suppose `H_n(A)=Delta_(n,3)` for an even `n>=6`,
and a vertex `p` has only three allowed underlying neighbors
`j_0,j_1,j_2`.  Then all three
incident aggregate matrices are nonzero rank-one same-color tensors

\[
 A_{p j_s}=w_s e_{r_s}^{(p)}\otimes e_{r_s}^{(j_s)},
 \qquad w_s\in\mathbb C^\times,                              \tag{1}
\]

where `(r_0,r_1,r_2)` is a permutation of `(0,1,2)`.  In particular, the
three incident edges are active and have three distinct colors at `p`.

**Proof.**  The star expansion at `p` has at most three terms,

\[
 \Delta_{n,3}=\sum_{s=0}^2
 A_{p j_s}\otimes H_{B\setminus\{p,j_s\}}.                   \tag{2}
\]

The partition rank of the diagonal tensor is three.  Hence no term in (2)
can vanish: otherwise its partition rank would be at most two.

Let `R` be the `n-4` sites other than `p,j_0,j_1,j_2`.  Take any covector
`lambda in V_p^*` with all three coordinates
`lambda_i=lambda(e_i)` nonzero, and on the tensor product of the sites in
`R` take the multilinear covector

\[
 K_lambda=\sum_{i=0}^2\lambda_i^{-1}(e_i^*)^{\otimes R}.
\]

Contract (2) by `lambda` at `p` and by `K_lambda` on `R`.  On the three
neighbor sites the left side becomes exactly

\[
 \Delta_{3,3}=\sum_{i=0}^2 e_i\otimes e_i\otimes e_i.        \tag{3}
\]

The right side is a sum of three slice terms, whose singleton factors at
`j_s` are

\[
 L_s(\lambda)=(\lambda\otimes\operatorname{id})A_{p j_s}.
                                                                    \tag{4}
\]

The three-slice center lemma (proved in `notes/tensor-route.md`, (25a)--
(25b)) applied to (3) says that the three vectors (4) are nonzero multiples
of three distinct coordinate basis vectors.

This holds for every `lambda` in the Zariski-dense torus `(C^*)^3`.  If two
coordinate functions of the linear map `L_s` were nonzero linear forms,
their product would vanish on that torus, hence identically, which is
impossible in the polynomial ring over `C`.  Thus the image of `L_s` lies
in one fixed coordinate line and `A_{p j_s}` has matrix rank one.  These
three fixed image lines are distinct, because they are distinct for every
generic `lambda`.

Write

\[
 A_{p j_s}=a_s\otimes e_{t_s}^{(j_s)}.
\]

Equation (4) never vanishes on `(C^*)^3`.  Therefore the linear form
`lambda mapsto lambda(a_s)` has no zero on that torus.  A linear form in
three variables with at least two nonzero coefficients does have such a
zero, so `a_s` is itself a nonzero multiple of one coordinate vector.
Thus every incident matrix is a nonzero decorated rank-one basis edge.

The mode-`p` rank of the left side of (2) is three, so the three coordinate
vectors `a_s` use distinct colors.  Contract (2) at `p` by the dual vector
selecting one of them.  Exactly one term remains, while the target slice is
a nonzero multiple of `e_r^{\otimes(n-1)}`.  Its factor at `j_s` is
`e_{t_s}`; equality forces `t_s=r`.  This proves (1).  QED.

The argument permits arbitrary complex entries and uses no positivity or
termwise inference from a vanishing sum.  Rather, rank one and same endpoint
colors are consequences of the exact target equation.

## 2. The prism plus one missing pair

On vertices `0,1,2,3,4,5`, take the triangular-prism edge set

\[
 P=\{03,04,05,12,14,15,23,24,35\}.                           \tag{5}
\]

Its four perfect matchings are

\[
\begin{aligned}
 M_A&=\{03,15,24\},&M_B&=\{04,12,35\},\\
 M_D&=\{04,15,23\},&M_C&=\{05,14,23\}.                     \tag{6}
\end{aligned}
\]

Adjoin the missing pair `01`.  There is exactly one new perfect matching,

\[
 N=\{01,24,35\}.                                             \tag{7}
\]

**Theorem (one-extra-pair obstruction).**  If all matrices outside
`P union {01}` are zero, then arbitrary matrices
`A_e in C^(3 by 3)` on these ten pairs cannot satisfy

\[
 H_6(A)=\Delta_{6,3}.                                        \tag{8}
\]

The same holds after adjoining any single edge of the complement of `P`.

**Proof.**  Vertices `2,3,4,5` have degree three in the allowed underlying
graph.  Apply the cubic-vertex lemma at each one.  Every edge of `P` touches
at least one of these vertices.  Consequently there are nonzero scalars
`w_e` and colors `kappa(e)` such that

\[
 A_e=w_e E_{\kappa(e),\kappa(e)}\quad(e\in P),               \tag{9}
\]

and the three incident colors at each of `2,3,4,5` are distinct.  The added
matrix `A_01` remains completely arbitrary.

Apply a simultaneous color permutation so that

\[
 \kappa(12)=0,\qquad\kappa(23)=1,\qquad\kappa(24)=2.         \tag{10}
\]

For shortness put

\[
\begin{array}{c|ccccccccc}
e&03&04&05&12&14&15&23&24&35\\ \hline
\kappa(e)&a&b&c&0&e&f&1&2&i.
\end{array}                                                   \tag{11}
\]

Properness at vertices `3,4,5` gives

\[
 \{a,i\}=\{0,2\},\qquad \{b,e\}=\{0,1\},\qquad
 \{c,f,i\}=\{0,1,2\}.                                     \tag{12}
\]

There are two cases.

First suppose `i=0`.  Then `a=2`, `{c,f}={1,2}`, and
`{b,e}={0,1}`.  The new matching (7), regardless of the entries of `A_01`,
is supported only on colorings

\[
 (*,*,2,0,2,0),                                              \tag{13}
\]

so it has no monochromatic coefficient.  The four nonzero prism monomials
in (6) have colorings

\[
\begin{array}{c|c}
M_A&(2,f,2,2,2,f)\\
M_B&(b,0,0,0,b,0)\\
M_D&(b,f,1,1,b,f)\\
M_C&(c,e,1,1,e,c).
\end{array}                                                   \tag{14}
\]

The all-2 target coefficient can only come from `M_A`, forcing `f=2` and
hence `c=1`.  The all-0 target coefficient can only come from `M_B`, forcing
`b=0` and hence `e=1`.  Then `M_C` is the all-1 matching, while the remaining
matching `M_D` has the mixed coloring

\[
 (0,2,1,1,0,2).                                              \tag{15}
\]

Its coefficient is the product of three nonzero scalars from (9).  It cannot
be canceled by `N`, whose four fixed coordinates in (13) disagree with
(15), and the other three prism terms are supported on the three constant
colorings.  This contradicts (8).

Now suppose `i=2`.  Then `a=0`, `{c,f}={0,1}`, and again
`{b,e}={0,1}`.  Matching `N` can have a monochromatic coefficient only in
color 2.  Matching `M_A` cannot be monochromatic because it contains both
the color-0 edge `03` and the color-2 edge `24`; `M_B` cannot be
monochromatic because it contains the color-0 edge `12` and color-2 edge
`35`; and `M_C,M_D`, both containing `23`, can only be monochromatic in
color 1.  Hence no matching produces the all-0 coloring at all, contradicting
its required coefficient one in (8).

This proves the assertion for the added pair `01`.  The complement of the
prism (5) is the six-cycle

\[
 01,13,34,45,25,02,
\]

and every automorphism of this cycle is an automorphism of its complement,
the prism.  Its edges form one orbit, so relabeling proves the assertion for
any one missing pair.  QED.

## 3. Consequence for finite-versus-border analysis

The triangular-prism degeneration cannot be made finite by turning on a
single additional underlying pair, even with all nine entries of that new
matrix and all entries of the original nine matrices available.  Any exact
finite realization approaching this boundary stratum must therefore turn on
at least two complementary pairs simultaneously.

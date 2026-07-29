# One-site gluing is a one-cross projection, not an aggregate closure

## 1. Outcome

Contracting one output site of each of two aggregate matching tensors has an
exact edgewise description, but only after retaining the sector with exactly
one new cross edge.  If the contracted incident blocks are replaced by
ordinary aggregate edges, the full matching tensor also contains every
higher odd crossing sector.  Thus the ordinary aggregate model is **not**
closed under one-site contraction.

The first failure is already sharp.  Contract two canonical four-site
ternary GHZ sources by the identity covector.  At the tensor level the result
is exactly `Delta_(6,3)`.  The canonical effective edges form the triangular
prism and give instead

\[
             H_6=\Delta_{6,3}+e_{012012}.                 \tag{1}
\]

The extra word is the unique three-cross matching.  More generally, gluing
an arbitrary hypothetical exact source at a vertex `p` to the canonical
four-site gadget gives

\[
 H_{n+2}=\Delta_{n+2,3}
   +\left(L_0L_1L_2{q^{m-2}\over(m-2)!}\right)
       \otimes e_0\otimes e_1\otimes e_2,\qquad n=2m,    \tag{2}
\]

where `q` is the quadratic internal to the old source after deleting `p`
and `L_0,L_1,L_2` are its three star rows.  Consequently this proposed
amplification is exact if and only if the new nonlinear cubic collision in
parentheses vanishes.  The original star equations do not imply that
vanishing: the canonical four-site source makes it a nonzero basis tensor.

The prism also gives an exact audit against the available structural
theorems.  Its aggregate support is matching-covered, tight-cut-free, cubic,
and 3-vertex-connected.  Its cubic stars already have precisely the local
normal form forced by cubic-vertex rigidity; the fourth perfect matching is
the obstruction predicted by the global part of that theorem.  Every block
has rank one, however, so the rank-at-least-two and rank-three graphs are
empty and all source-Hessian connectivity theorems land on their exceptional
branch.  The three-shore torus-zero hypothesis also fails termwise.  Hence
gluing supplies neither a low aggregate separator nor a uniform
contradiction; it forgets a global one-use constraint and creates (1).

The exact checker is

```text
.venv/bin/python computations/verify_one_site_gluing_contamination.py
```

## 2. Arbitrary one-site contraction

Let

\[
 P=X\mathbin{\dot\cup}\{p\},\qquad
 Q=Y\mathbin{\dot\cup}\{q\},                             \tag{3}
\]

where `P,Q` have even cardinality, so `X,Y` are odd.  Let `A` and `B` be
arbitrary aggregate edge tensors on `P` and `Q`, respectively, and let

\[
                    K\in(V_p\otimes V_q)^*               \tag{4}
\]

be an arbitrary bilinear covector.  No symmetry, rank, or nonvanishing
condition is imposed.

Orient an incident block with the distinguished site first.  For `x in X`
and `y in Y`, define the effective cross block `C_xy in V_x tensor V_y` by

\[
 C_{xy}=K\mathbin{\lrcorner}
                 \bigl(A_{px}\otimes B_{qy}\bigr).       \tag{5}
\]

In coordinates, if the rows of `A_px,B_qy` belong to `p,q`, then

\[
                    C_{xy}=A_{px}^{\mathsf T}KB_{qy}.     \tag{6}
\]

Define an ordinary edge system `D` on `X disjoint-union Y` by

\[
 D_{xx'}=A_{xx'},\qquad D_{yy'}=B_{yy'},\qquad D_{xy}=C_{xy}.
                                                                    \tag{7}
\]

Write `H_D^(r)` for the sum of the perfect-matching terms of `D` which use
exactly `r` edges across `X|Y`.

**Proposition 2.1 (exact sector closure).**  One has

\[
 K\mathbin{\lrcorner}\bigl(H_P(A)\otimes H_Q(B)\bigr)
                         =H_D^{(1)}.                      \tag{8}
\]

If every cross block in (7) is multiplied by an indeterminate `t`, then

\[
 H_D(t)=\sum_{\substack{r\ge1\\r\ {m odd}}}t^rH_D^{(r)},
 \qquad
 K\mathbin{\lrcorner}\bigl(H_P(A)\otimes H_Q(B)\bigr)
                         =[t]H_D(t).                      \tag{9}
\]

In particular, the canonical effective source at `t=1` is an exact gluing
if and only if

\[
                    \sum_{r\ge3,\ r\ {m odd}}H_D^{(r)}=0. \tag{10}
\]

**Proof.**  Expand both tensors at their distinguished vertices:

\[
 H_P(A)=\sum_{x\in X}A_{px}\otimes H_{X\setminus\{x\}}(A),
 \qquad
 H_Q(B)=\sum_{y\in Y}B_{qy}\otimes H_{Y\setminus\{y\}}(B). \tag{11}
\]

Contracting the first displayed factors by `K` turns their product into
`C_xy`.  The remaining factors independently range over a perfect matching
of `X-{x}` and one of `Y-{y}`.  This is exactly the unique-cross expansion
of `D`, proving (8).

Every perfect matching crosses a cut in the parity of either shore.  Since
both shores in (3) are odd, its crossing number is positive and odd.
Multiplication of every cross block by `t` records that number, proving
(9), and evaluation at `t=1` gives (10).  `QED`

Thus contraction is closed in a *marked one-cross sector* (equivalently,
after coefficient extraction), not in the ordinary complex edge model.  A
nilpotent marker can remember that every effective edge arose from the same
single gluing event; aggregation over `C` forgets that correlation and lets
several effective edges occur in one matching.

The exception in which one original tensor has only two sites is also now
transparent: one of `X,Y` then has size one, so no sector with `r>=3`
exists.  The four-site gadget is the first possible failure.

## 3. Exact formula for the canonical four-site gadget

Let `C={0,1,2}`.  The canonical gadget has vertices

\[
                       \{q,y_0,y_1,y_2\}.                \tag{12}
\]

Put `E_ii=e_i tensor e_i` on `qy_i`, and also put `E_ii` on
`y_jy_k` when `{i,j,k}=C`.  Its three perfect matchings give

\[
                         H_4=\sum_{i=0}^2e_i^{\otimes4}. \tag{13}
\]

Now let `A` be any exact ternary source on

\[
                         \{p\}\mathbin{\dot\cup}X,
 \qquad |X|=2m-1,\qquad m\ge2.                           \tag{14}
\]

Work in the commutative square-free site algebra on `X`.  Write

\[
 q=\sum_{x<x'}A_{xx'},\qquad
 L_a=\sum_{x\in X}(e_a^*\otimes\operatorname{id})A_{px}
          \quad(0\le a\le2).                             \tag{15}
\]

The three slices at `p` of `H_(2m)(A)=Delta_(2m,3)` are exactly

\[
                  L_a{q^{m-1}\over(m-1)!}=e_a^{\otimes X}.
                                                                    \tag{16}
\]

For an arbitrary bilinear covector `K`, put

\[
 K_{ab}=K(e_a,e_b),\qquad L_b^K=\sum_{a=0}^2K_{ab}L_a.   \tag{17}
\]

Formula (5) says that every cross block ending at `y_b` is

\[
 D_{xy_b}=\left(\sum_aK_{ab}
            (e_a^*\otimes\operatorname{id})A_{px}\right)
                         \otimes e_b.                    \tag{18}
\]

In particular it has matrix rank at most one.  Because the new shore has
three vertices, only the one- and three-cross sectors exist.  Equations
(16)--(18) give the complete identity

\[
\boxed{
 H_D=\sum_{a,b=0}^2K_{ab}
          e_a^{\otimes X}\otimes e_b^{\otimes\{y_0,y_1,y_2\}}
 +\Theta_{K,p}(A)\otimes
          e_0^{(y_0)}e_1^{(y_1)}e_2^{(y_2)},}             \tag{19}
\]

where

\[
 \boxed{\quad
 \Theta_{K,p}(A)=L_0^KL_1^KL_2^K{q^{m-2}\over(m-2)!}
                  \in\bigotimes_{x\in X}V_x.\quad}      \tag{20}
\]

Indeed, a one-cross matching ending at `y_b` uses the internal edge between
the other two terminals, also of color `b`; its old-shore sum is the left
side of (16) with `L_b^K`.  This proves the first line of (19).  A
three-cross matching sends all three terminals across, so its old-shore sum
chooses the three labelled rows `L_0^K,L_1^K,L_2^K` at distinct sites and
matches the remaining sites by `q`.  Square-free multiplication and the
factor `(m-2)!` count every such matching once, proving (20).

For the identity covector, (19) is precisely (2), with

\[
                  \Theta_p(A)=L_0L_1L_2{q^{m-2}\over(m-2)!}. \tag{21}
\]

This is the exact nonlinear condition omitted by the proposed gluing
argument.  It is the `T_3=0` equation in the vertex-expansion formulation of
[`vertex-expansion-gadget-obstruction.md`](vertex-expansion-gadget-obstruction.md),
now obtained directly from arbitrary one-site contraction.

## 4. The canonical self-gluing counterexample

Take a second copy of (13), with old surviving vertices `x_0,x_1,x_2`.
Then

\[
 L_0=e_0^{(x_0)},\qquad L_1=e_1^{(x_1)},\qquad
 L_2=e_2^{(x_2)},                                        \tag{22}
\]

so, at `m=2`,

\[
                         \Theta_p(A)=e_0e_1e_2\ne0.      \tag{23}
\]

At the tensor level, contraction of the two inputs by the identity is

\[
 \left(\sum_a e_a^{\otimes X}e_a^{(p)}\right)
 \mathbin{\mathop{\lrcorner}_{p,q}}
 \left(\sum_b e_b^{(q)}e_b^{\otimes Y}\right)
                    =\sum_a e_a^{\otimes(X\sqcup Y)}.   \tag{24}
\]

The effective support, however, consists of the two triangles and the
three spokes `x_i y_i`.  Its four supported perfect matchings are

\[
\begin{aligned}
 M_i&=x_iy_i\mid x_jx_k\mid y_jy_k
                   &&(\{i,j,k\}=\{0,1,2\}),\\
 M_*&=x_0y_0\mid x_1y_1\mid x_2y_2.                     \tag{25}
\end{aligned}
\]

The first three give the three constant words and the last gives `012012`,
which proves (1) without any numerical or genericity argument.  More
generally, a diagonal contraction
`K=diag(kappa_0,kappa_1,kappa_2)` gives pure coefficients `kappa_i` and the
unique mixed coefficient `kappa_0kappa_1kappa_2`; hence no choice with all
three pure coefficients nonzero removes the contaminant.

This is a genuine failure of closure of the image class, rather than only a
failure of the canonical blocks.  The established arbitrary-matrix
six-site theorem in
[`../proofs/low-rank-graph-laurent-obstruction.md`](../proofs/low-rank-graph-laurent-obstruction.md)
says that the contracted tensor `Delta_(6,3)` in (24) has no aggregate
six-site preimage at all.

## 5. Why the structural obstructions do not amplify

The self-glued support in (25) is the triangular prism.

1. **Aggregate connectivity.**  Every edge lies in one of the four
   matchings (25), so the graph is matching-covered and bridgeless.  Deleting
   at most two vertices leaves it connected: if both deleted vertices are
   on one triangle, the surviving vertex uses its spoke to the intact
   triangle; if one is deleted on each triangle, at least one spoke joins
   the two surviving triangle edges.  Thus it is 3-vertex-connected.  For
   every three-vertex shore, one of (25) crosses three times (a two-line
   check according as the shore is `3+0` or `2+1` across the two triangles),
   so it has no nontrivial tight cut.  The low-separator and tight-cut
   reductions therefore do not apply.

2. **Cubic vertices.**  Every vertex is cubic and is incident with one
   `E_00`, one `E_11`, and one `E_22` block.  This is exactly the conclusion,
   not a violation, of cubic-vertex rigidity.  Its global fourth-matching
   argument produces `M_*`; equation (1) is the resulting forbidden mixed
   monomial.  Grafting has not built an exact source to which the theorem
   can be applied--it has built the theorem's sharp obstruction.

3. **Rank graphs and source Hessians.**  In the general construction
   (18), every new cross block and every new triangle block has rank at most
   one.  Hence the three new vertices are isolated in both the
   rank-at-least-two and rank-three graphs.  This is precisely the
   disconnected/isolated escape allowed by the all-pair source-Hessian
   theorems.  On the prism the escape is quantitative: after the fifteen
   possible pair deletions, the four-site source-Hessian map has ranks
   `35` six times, `34` three times, and `26` six times in its
   54-dimensional domain.  Its kernel therefore has dimension at least
   `19`, far beyond the at-most-three-dimensional vertex-gauge image.

4. **Three-shore contraction.**  On either triangular shore, contracting
   its vertices by full-coordinate covectors cannot annihilate even one
   internal basis edge: the contraction of `E_ii` is a product of two
   nonzero `i`-coordinates.  Thus the torus-zero hypothesis needed to leave
   a `3 by 3` vector permanent never occurs.  Sectorwise, the one-cross
   part is already `Delta_(6,3)`, while the three-cross part is the single
   mixed shore row `e_012`; this is compatible with the pure-edge
   dimension-three branch of the three-shore normal form and fails only in
   the explicit mixed coefficient (1).

The same diagnosis holds uniformly for (19): the added terminals create a
rank-one three-site appendage, and exact amplification would require the
new cubic equation `Theta_(p)=0`.  No cited support, Hessian, cubic-local, or
three-shore theorem supplies that equation.  One-site gluing therefore does
not reduce the uniform conjecture; its exact obstruction is the nonlinear
three-cross collision (20).

## 6. Exact audit

The checker first uses dense nonsymmetric integer blocks and a dense
off-diagonal integer covector to verify (6)--(9) coefficientwise, including
endpoint order.  It then enumerates all `3^4` coefficients of each canonical
input gadget, contracts their coefficient dictionaries directly, and
independently enumerates all `3^6` coefficients of the effective source.  It
verifies the split

\[
                     H_D^{(1)}=\Delta_{6,3},\qquad
                     H_D^{(3)}=e_{012012}.                \tag{26}
\]

It also enumerates all supported perfect matchings, checks matching
coverage, 3-connectivity after every deletion of fewer than three vertices,
and absence of a tight three-shore.  Finally it constructs every four-site
linear map `Z mapsto Zq` after pair deletion and computes its rank by exact
rational Gaussian elimination, yielding the Hessian census quoted above.

# Exact reduction for a central bridge between two standard `K_4` blocks

This note continues
[`two-k4-anchor-bridge-obstruction.md`](two-k4-anchor-bridge-obstruction.md)
and completes the central-edge classification.  No arbitrary aggregate
tensor on the anchor pair `L_*R_*` can synchronize the two standard
four-site equality blocks, even with arbitrary signed complex tensors and
parallel sources on all nine nonanchor bridges.

Throughout, the two standard four-site equality blocks have vertices

\[
 L_*,L_0,L_1,L_2\qquad\hbox{and}\qquad
 R_*,R_0,R_1,R_2.
\]

The arbitrary nonanchor bridge tensors are
`B_ij in V_(L_i) tensor V_(R_j)`, and now an arbitrary central tensor

\[
                         D\in V_{L_*}\otimes V_{R_*}       \tag{1}
\]

is also allowed.  Parallel sources are aggregated in `B_ij` and `D`.

## 1. The common six-site contaminant

Let `K_rs` be the four-site matching tensor of the complementary bridge
`K_(2,2)` obtained by deleting `L_r,R_s`.  Let `J_rs` insert the fixed
factors `e_r` at `L_r` and `e_s` at `R_s`.  Finally, let `P` be the full
matching tensor on the six nonanchor sites when the central edge is used.
This induced six-site source includes both nonanchor triangles inherited
from the two `K_4` blocks and all nine tensors `B_ij`.

After dividing each slice by its two nonzero anchor-edge weights, the nine
anchor-color slices of a hypothetical `Delta_(8,3)` identity say

\[
\begin{aligned}
 J_{rr}(K_{rr})&=-\delta_{rr}P,\tag{2a}\\
 J_{rs}(K_{rs})&=-\lambda_{rs}E_{rs}-\delta_{rs}P
                                      \qquad(r\ne s),\tag{2b}
\end{aligned}
\]

where every `lambda_rs` is nonzero, `delta_rs=0` exactly when the `(r,s)`
coordinate of `D` is zero, and

\[
 E_{rs}=\bigotimes_{i=0}^2e_r^{(L_i)}
        \bigotimes_{j=0}^2e_s^{(R_j)}.                    \tag{3}
\]

If `P=0`, (2) is exactly the anchor-free signature already proved
impossible.  Hence `P != 0`.  Let

\[
 \mathcal R=\{r:\exists s,\ \delta_{rs}\ne0\},\qquad
 \mathcal C=\{s:\exists r,\ \delta_{rs}\ne0\}.          \tag{4}
\]

The left sides of (2), as well as `E_rs`, lie in the subspace having factor
`e_r` at `L_r` and `e_s` at `R_s`.  Thus every active coordinate `(r,s)`
forces `P` into that subspace, and intersecting gives the exact
factorization

\[
 P=\left(\bigotimes_{r\in\mathcal R}e_r^{(L_r)}\right)
   \left(\bigotimes_{s\in\mathcal C}e_s^{(R_s)}\right)
   P_{\rm free}.                                          \tag{5}
\]

This is the basic structural reduction for every central bridge.

## 2. Every coordinate-dense central tensor is impossible

Assume that the coordinate support of `D` meets all three rows and all
three columns.  Equation (5) then makes the common contaminant a nonzero
rainbow product,

\[
 P=\rho\,
 e_0^{(L_0)}e_1^{(L_1)}e_2^{(L_2)}
 e_0^{(R_0)}e_1^{(R_1)}e_2^{(R_2)},qquad \rho\ne0.       \tag{6}
\]

Consequently each complementary square `K_rs` has extremely small
coordinate support:

* for `r != s`, it has the nonzero block-constant coordinate with all
  remaining left colors `r` and all remaining right colors `s`, and, when
  `delta_rs != 0`, also the rainbow-complement coordinate;
* for `r=s`, it is zero if `d_rr=0`, and otherwise is a nonzero multiple
  of the rainbow-complement coordinate.

There is an exact Boolean support lemma.

**Lemma 2.1.**  Under these nine square signatures and the existence of a
nonzero rainbow term in `P`, every one of the `81` scalar entries of the
nine bridge tensors `B_ij` is nonzero.

**Proof.**  For each output coordinate of each complementary square there
are two matching monomials.  At a required zero coordinate their support
bits must agree; at each required nonzero coordinate at least one bit must
be present.  Moreover a matching contributing the rainbow coefficient of
`P` cannot use either inherited nonanchor-triangle edge: its two endpoints
have distinct rainbow colors, while every such internal edge is
same-color.  Hence some bridge-only perfect matching supports the rainbow
coloring.

These are `1545` Boolean variables (including product auxiliaries) and at
most `5849` elementary CNF clauses.  The checker enumerates all `265`
nonempty coordinate supports meeting every row and column.  In every case,
adding the single cardinality condition "at most 80 bridge cells" is
UNSAT.  Equivalently all `81` cells are forced.  The checker also validates
the full-support assignment against every generated clause. `QED`

Full scalar support is itself impossible.  Fix any off-diagonal square
`K_rs`, write its remaining rows as `i,k` and columns as `j,l`, and fix the
right colors at the block-constant value `s,s`.  All denominators below are
nonzero by Lemma 2.1.  Define

\[
 R(a,c)=
 \frac{B_{ij}^{a s}B_{kl}^{c s}}
      {B_{il}^{a s}B_{kj}^{c s}}.                         \tag{7}
\]

This is a rank-one multiplicative table in `(a,c)`, so

\[
 R(r,r)R(a,c)=R(r,c)R(a,r)                                \tag{8}
\]

for all `a,c`.  Choose `a != r` and `c != r`.  At the three coordinates
`(a,c),(r,c),(a,r)`, the square output is zero: the block-constant point is
`(r,r)`, while the optional rainbow point has two distinct right colors
different from `(s,s)`.  Hence each of the three ratios is `-1`.
Equation (8) gives `R(r,r)=-1`, making the block-constant coefficient zero
as well.  This contradicts (2b).

Thus **no central tensor whose exact coordinate support meets all three
rows and all three columns can synchronize the two blocks**.  In
particular, every matrix with all nine coordinates nonzero and the full
diagonal tensor `sum_r d_r e_r tensor e_r` are excluded exactly.

## 3. Every central support of size at most three is impossible

The untouched equations `(r,s)` with `delta_rs=0` retain the zero-square and
pure off-diagonal line implications from the anchor-free proof.  Exhausting
the `512` aggregate bridge-edge supports closes every central support with
at most three cells except the following simultaneous-permutation and
transpose orbits:

\[
\begin{array}{c|c}
|\operatorname {supp}D|&\text{representatives}\ \hline
2&\{00,11\},\\
3&\{00,01,11\},\quad\{00,01,22\},\quad\{00,11,22\}.
\end{array}                                                \tag{9}
\]

The last representative meets every row and column and was closed in
Section 2.  The other three have short coordinate contradictions.

For `supp(D)={00,11}` or `{00,01,11}`, the untouched equation `K_22=0`
forces the four tensors `B_00,B_01,B_10,B_11` to be rank-one with common
endpoint lines `u_0,u_1,v_0,v_1`.  The untouched pure signatures `K_20`
and `K_21` force

\[
                         v_1=\mathbb C e_0,qquad
                         v_0=\mathbb C e_1.               \tag{10}
\]

But every matching term of the untouched `K_02` uses either the line
`v_0` at `R_0` or `v_1` at `R_1`.  Its required coefficient has color
`e_2` at both sites, so that coefficient is zero, a contradiction.

For `supp(D)={00,01,22}`, use `K_11=0` instead.  It gives common right
lines `v_0,v_2` on the square with row and column sets `{0,2}`.  The pure
signatures `K_10,K_12` force

\[
                         v_2=\mathbb C e_0,qquad
                         v_0=\mathbb C e_2.               \tag{11}
\]

Every term of `K_21` then has a wrong fixed factor at `R_0` or `R_2`, so
its required all-`e_1` right coefficient vanishes.  This is again a
contradiction.  Sparse aggregate-edge supports omitted from this paragraph
are already closed by a unique pure matching term; the checker performs
that exact preliminary audit before applying (10)--(11).

Therefore any still-possible central bridge must have at least four
nonzero coordinate entries, at least two active rows, and at least two
active columns.

## 4. The six four-cell orbits, and the `2 by 3` closure

After Sections 2--3 and the coordinate-row/column theorem of the companion
note, the first intermediate supports have four cells.  There are `54`
labeled supports in six orbits:

\[
\begin{array}{c|l}
12&\{00,01,02,11\},\\
12&\{00,01,02,12\},\\
12&\{00,01,11,12\},\\
 6&\{00,01,20,21\},\\
 6&\{00,01,21,22\},\\
 6&\{01,02,10,12\}.
\end{array}                                                \tag{12}
\]

The orbit action is simultaneous permutation of row and column labels,
together with transposition.  Five rows of (12) have two active rows and
all three active columns, up to transposition.  Treat all such supports at
once.  Let the active rows be `{p,q}`, let `t` be the missing row, and use
all three columns.  Equation (5) has the form

\[
 P=e_p^{(L_p)}e_q^{(L_q)}
   e_0^{(R_0)}e_1^{(R_1)}e_2^{(R_2)}\,w^{(L_t)},          \tag{13}
\]

for a nonzero vector `w`.

The square-support clauses of Lemma 2.1 give a stronger open-chart lemma.

**Lemma 4.1 (`2 by 3` open chart).**

1. If the `e_t` coefficient of `w` is nonzero, all `81` scalar entries of
   the bridge tensors are nonzero.
2. If `w` lies in `span(e_p,e_q)`, every bridge entry is nonzero except
   possibly an entry whose physical left site is `L_t` and whose left
   endpoint color is `e_t`.  Thus the following `72` entries are forced:

\[
                 B_{ij}^{ab}\ne0
                 \quad\text{whenever }(i,a)\ne(t,t).     \tag{14}
\]

The checker proves this simultaneously for every one of the `75` exact
central supports with two active rows and three active columns.  There are
`300` exact supports of `w` containing `e_t`; adding "at most 80 cells" is
UNSAT in every case.  For the remaining `225` active-plane supports of
`w`, adding the single clause saying that at least one of the `72` entries
in (14) vanishes is UNSAT.  Full bridge support is independently checked
to satisfy every base clause, so neither assertion is vacuous.

Now choose `r in {p,q}`, choose an active `s != r`, and let `r'` be the
other active row color.  In `K_rs`, fix both remaining right colors to
`s`.  The `P` term in (2b) has rainbow colors on the remaining right sites,
so it has zero coefficient in this slice.  The only desired nonzero point
of the resulting `2 by 2` left-color table is `(r,r)`.  All entries needed
to form the four ratios

\[
                  R(r,r),R(r,r'),R(r',r),R(r',r')        \tag{15}
\]

are nonzero by either part of Lemma 4.1.  The three nontarget coefficients
make the last three ratios `-1`; the multiplicative rectangle identity (8)
then makes `R(r,r)=-1`, canceling the required point.  This contradiction
closes all five `2 by 3` orbits in (12), all their transposes, and in fact
every central support with active-size `2 by 3` or `3 by 2`, including
supports of sizes five and six.

## 5. The nonprincipal `2 by 2` closure

The fourth row of (12) is the only nonprincipal `2 by 2` orbit.  Use the
representative

\[
 \operatorname {supp}D=\{00,01,20,21\}.                  \tag{16}
\]

Thus the active row set is `{0,2}`, the active column set is `{0,1}`, and
(5) leaves an arbitrary nonzero two-site tensor `W` at `L_1,R_2`:

\[
 P=e_0^{(L_0)}e_2^{(L_2)}e_0^{(R_0)}e_1^{(R_1)}
                         W^{(L_1,R_2)}.                  \tag{17}
\]

**Lemma 5.1 (`2 by 2` open chart).**  For every one of the `511` possible
nonempty exact coordinate supports of `W`, the following `64` bridge
entries are nonzero:

\[
 B_{ij}^{ab}\ne0
 \quad\text{if }(i,a)\ne(1,1)\ \text{and}\ (j,b)\ne(2,2).
                                                               \tag{18}
\]

The clause generator considers all `15` underlying matchings: six use
three bridges, while nine use one bridge and one inherited triangle edge
on each shore.  It retains exactly the patterns compatible with the fixed
coefficient of `P` (for (17), only the six bridge-only patterns survive).
For each exact support of `W`, appending the one clause "some entry in
(18) vanishes" is UNSAT.  The checker again verifies separately that
setting all `81` cells nonzero satisfies the base formula.

Apply the coefficient rectangle to `K_01`, fix the two right colors to
`1`, and use left colors `0,2`.  Every scalar entry in the four ratios is
covered by (18).  The common contaminant in (17) has color `e_0` at the
remaining active right site `R_0`, so it has no coefficient with both
remaining right colors equal to `1`.  Hence the same three-zero rectangle
forces the required `(0,0)` coefficient to vanish.  This closes (16).  A
full principal `2 by 2` rectangle is closed by the same argument that
proved (10): the four equations used there lie outside that rectangle.
Proper subsets have at most three cells and were already closed in
Section 3.

## 6. Exhaustion of the central edge

Every nonzero coordinate support of `D` falls into one of the following
cases:

1. one active row or one active column: the companion note's exact
   `34 by 512` line audit;
2. all three active rows and columns: Section 2;
3. at most three coordinate cells: Section 3;
4. active size `2 by 3` or `3 by 2`: Section 4;
5. active size `2 by 2`: Section 3 for proper subsets, and Section 5 plus
   the principal-square argument for the full rectangles.

These cases are exhaustive.  Together with the `P=0` reduction to the
anchor-free theorem, they prove:

> **Central-bridge theorem.**  Two standard weighted `K_4` realizations of
> ternary equality cannot be synchronized to `Delta_(8,3)` by arbitrary
> tensors on all nine nonanchor bridges and an arbitrary tensor on the
> anchor-to-anchor edge.  Endpoint colors may be asymmetric, weights may
> be arbitrary complex numbers, and parallel sources are allowed.

Run

```text
uv run python computations/verify_dense_central_bridge_reduction.py
```

to replay the support classifications, the `265+300+225+511` SAT
implications, the coefficient rectangles, and the complete support
exhaustion.

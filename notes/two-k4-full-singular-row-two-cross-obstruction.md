# Four singular blocks cannot occupy a full row

## 1. Result

Let the two shores of the two-`K_4` chart be

\[
 L=\{0,1,2,3\},\qquad R=\{0,1,2,3\},
\]

with the standard ternary one-factorization.  Write `B_ij` for the
`3 by 3` cross block from `L_i` to `R_j`.

**Theorem 1.1.**  There is no exact two-`K_4` realization of
`Delta_(8,3)` in which

\[
       \det B_{0j}=0\quad(0\leq j<4),\qquad
       \det B_{ij}\ne0\quad(1\leq i<4,\ 0\leq j<4).     \tag{1}
\]

By transposition, four singular blocks cannot occupy a full column either.
Thus the first exactly-four-singular position orbit is closed for
arbitrary ranks, not merely when its four exceptional blocks vanish.

The proof first uses the dead four-cross slabs to force two coordinate zero
rows among the four exceptional blocks.  One actual two-cross target slice
then turns those two zero rows, together with two ordinary row kernels,
into a rank contradiction.  The exact finite audit is

```text
computations/verify_two_k4_full_singular_row_two_cross_obstruction.py
```

## 2. Internal weights and zero cofactors

For an internal shore edge `uv`, let `kappa(uv)` be its factor colour and
write its nonzero left and right weights as `lambda_uv` and `rho_uv`.
The coefficient of the constant word `c^4` in either internal `K_4`
gadget is the product of the two weights in the colour-`c` factor.  Exact
four-site equality makes this product one.  In particular every
`lambda_uv` and `rho_uv` is nonzero.

Recall the eight directed-triangle dead coordinate lines.  Fix one whose
hole `h` is not zero.  All four reference blocks `B_hj` are invertible.
The four-vector syzygy from
[`two-k4-dead-slice-determinantal-boundary.md`](two-k4-dead-slice-determinantal-boundary.md)
therefore makes all four complementary `Per_3` tensors vanish.  For a
physical block column `j`, its local `Per_3` map consists of the three rows

\[
             e_{a_i}^{\mathsf T}B_{ij}\qquad(i\ne h),   \tag{2}
\]

up to common right multiplication by `B_hj^(-1)`.  Call this column a
**status** when the three displayed rows span a space of dimension at most
one.  Common right multiplication does not change that condition.

We use two elementary consequences of a zero local image of `Per_3`.

1. If all three maps have three nonzero coordinate images, at least two
   maps have rank one.
2. If one map has exactly one zero coordinate image and its other two
   images are independent, the other two maps have rank one.

The first is Lemma 3.1 of
[`two-k4-two-singular-boundary.md`](two-k4-two-singular-boundary.md);
the second is the one-defect lemma in
[`two-k4-exact-three-allzero-path-obstruction.md`](two-k4-exact-three-allzero-path-obstruction.md).
Both are field-uniform in characteristic zero and require no genericity.

## 3. Every colour is active in at most two exceptional blocks

For a colour `c`, put

\[
       A_c=\{j:e_c^{\mathsf T}B_{0j}\ne0\},\qquad m_c=|A_c|. \tag{3}
\]

**Lemma 3.1.**  Under (1), `m_c <= 2` for every `c`.

**Proof.**  There are exactly two directed-triangle lines whose hole is
not zero and whose assignment at vertex zero is `c`.  Consider either
line and suppose first that `m_c=4`.  Every one of its four local column
maps is clean.  Since all four complementary `Per_3` tensors vanish, every
three-subset contains at least two statuses.  Hence at least three of the
four columns are statuses.

If `m_c=3`, call the unique inactive column dirty.  The complementary
triple of three clean columns contains at least two statuses.  If the dirty
map is a status, this already gives three.  If it is not a status, its two
nonzero rows are independent; applying the one-defect lemma to the three
triples containing it forces all three clean columns to be statuses.
Again the line has at least three statuses.

The two lines selecting `(0,c)` therefore demand at least six statuses
when `m_c >= 3`.  At an active physical column they cannot both occur:
the two triples share the same nonzero row `e_c^T B_0j` and also select two
distinct rows of one of the invertible blocks `B_ij`.  Two statuses would
make those distinct rows proportional.  Thus an active column has capacity
one across the pair of lines.  An inactive column has the trivial capacity
two.  Total capacity is at most

\[
                       m_c+2(4-m_c)=8-m_c\leq5,         \tag{4}
\]

contradicting demand six.  Hence `m_c <= 2`. `QED`

For completeness, the shared invertible rows in the three colour cases
are, in the standard ordering of the eight lines,

\[
          c=0:(t_4,t_6),\qquad
          c=1:(t_2,t_7),\qquad
          c=2:(t_3,t_5).                                \tag{5}
\]

The checker reconstructs these pairs directly from the one-factorization
and verifies that the shared row colours are distinct.

## 4. A kernel-cleaned two-cross slice

Fix any colour `c`.  Lemma 3.1 leaves at least two physical columns outside
`A_c`; choose two of them and call their right edge `uv`.  Put

\[
 d=\kappa(uv),\qquad \{j,k\}=R\setminus\{u,v\}.         \tag{6}
\]

Thus

\[
                     e_c^{\mathsf T}B_{0u}
                    =e_c^{\mathsf T}B_{0v}=0.           \tag{7}
\]

Let `Q_d={q in C^3:q_d=0}`.  Both `Q_d` and
`ker(e_c^T B_0k)` have dimension at least two, so choose

\[
 0\ne q\in Q_d\cap\ker(e_c^{\mathsf T}B_{0k}).         \tag{8}
\]

Also put

\[
               P=\ker(e_c^{\mathsf T}B_{0j}),
               \qquad\dim P\geq2.                      \tag{9}
\]

Choose `t` with `kappa(0t)=c` and let `{r,s}` be the other two left
vertices.  Contract the eight-site coefficient as follows:

* fix `L_0,L_t` to colour `c`;
* fix `R_u,R_v` to colour `d`;
* contract `R_k` by `q` and `R_j` by an arbitrary `p in P`;
* leave `L_r,L_s` open.

The target contraction is zero because the two fixed right colours force
a constant target word to have colour `d`, whereas `q_d=0`.

On the source side, `uv` is the only surviving internal right edge.  Every
other edge incident with `u` or `v` has a colour different from `d`, while
the complementary edge `jk` is killed by `q_d=0`.  Every four-cross
matching vanishes as well: if `L_0` crosses to `u` or `v`, use (7); if it
crosses to `j` or `k`, use (8)--(9).  The two-cross term using the other
left factor edge `rs` is killed for the same reason at its `L_0` cross
edge.

Exactly two matchings remain.  Both use the internal edges `0t` and `uv`,
and cross `r,s` to `j,k` in the two possible orders.  Consequently

\[
 B_{rj}p\otimes B_{sk}q+B_{rk}q\otimes B_{sj}p=0
                         \qquad(p\in P).                \tag{10}
\]

The common factor `lambda_0t rho_uv` has been divided out.

## 5. Fixed-leg rank collapse

We finish with a coordinate-free one-line lemma.

**Lemma 5.1 (fixed-leg cancellation).**  Let `V,W` be vector spaces, let
`y in W` be nonzero, and suppose

\[
                 x_p\otimes y+z\otimes w_p=0
\]

for a fixed `z in V` and every `p` in a subspace `P`.  Then every `x_p`
lies in `span(z)`.

**Proof.**  Apply `V -> V/span(z)` to the first tensor factor.  This gives
`bar(x_p) tensor y=0`; since `y` is nonzero, `bar(x_p)=0`. `QED`

Apply the lemma to (10), with

\[
 x_p=B_{rj}p,\quad y=B_{sk}q,\quad
 z=B_{rk}q,\quad w_p=B_{sj}p.                           \tag{11}
\]

The vector `y` is nonzero because `B_sk` is invertible and `q` is nonzero.
It follows that

\[
                         B_{rj}P\subseteq\operatorname{span}(B_{rk}q).
                                                               \tag{12}
\]

But `dim P >= 2` and `B_rj` is invertible, so the left side has dimension
at least two, whereas the right side has dimension one.  This
contradiction proves Theorem 1.1.

## 6. Boundary left open

The theorem removes the full-row/full-column orbit from the
exactly-four-singular boundary.  It does not address the other nine
position orbits.  The mechanism to reuse there is precise: find a left
factor edge whose two endpoint blocks can be made invisible in one target
row, then use two complementary right kernels to erase the entire
four-cross sector while retaining a two-dimensional input plane on an
invertible block.

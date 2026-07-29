# A full block row cannot coexist with a two-defect row

## 1. Result

Work in the two-`K_4` chart with standard ternary equality tensors on the
two shores.  Write `B_ij` for the `3 by 3` cross block from left site `i`
to right site `j`.

**Theorem 1.1.**  Suppose one block row is completely invertible and a
second block row has at least two invertible blocks.  Then the full
matching-tensor equations have no solution.

In particular, the exact-six orbit

\[
 E_2=\{00,01,10,12,21,22\},                            \tag{1}
\]

the bipartite six-cycle with one empty row and one empty column in its
singular support, is impossible for arbitrary singular ranks and entries.
The same local theorem also excludes the exact-six orbit `E_1`, since its
row-degree partition is likewise `(2,2,2,0)`.

The proof is field-uniform in characteristic zero.  Its new ingredient is
a two-exception Hessian calculation.  If either exceptional component is
nonzero, the six-cell slab already erases the entire effective quadratic.
If both are literally zero, the full eight-cell erasure leaves exactly the
block on the edge joining the two regular sites.  That residual edge misses
an exceptional endpoint, which is enough for the usual three-coordinate-
lines versus two-plane contradiction.

The exact audit is
[`verify_two_k4_six_cycle_two_defect_obstruction.py`](../computations/verify_two_k4_six_cycle_two_defect_obstruction.py).

Combining this theorem with the coincident-defect incident obstruction
removes all three exact-six position orbits.  A separated one-plus-two
defect extension below also removes every exact-seven support.  Hence the
net determinantal consequence is

\[
                 \boxed{\#\{(i,j):\det B_{ij}=0\}\ge8}.               \tag{1a}
\]

## 2. The two-exception erasure lemma

Let

\[
 \mathcal R=\bigotimes_{i=0}^3(\mathbb F\oplus V_i),
 \qquad V_i^2=0,\qquad \dim V_i=3,                     \tag{2}
\]

over a field of characteristic different from two.  Let `U,W` be
three-spaces, let `K subset U` and `L subset W` be two-planes, and set

\[
 p_x=\sum_iP_ix,\qquad s_y=\sum_iS_iy.                 \tag{3}
\]

Assume every `P_i:U -> V_i` is an isomorphism.  Split the sites into two
exceptional sites `h,k` and two regular sites `r,s`, and assume

\[
 S_r,S_s\text{ are isomorphisms},\qquad
 S_h,S_k\text{ are singular}.                         \tag{4}
\]

For `q in R_2`, write `q_ij` for its block on the edge `ij`.

**Lemma 2.1 (two-exception six/eight-cell erasure).**

1. If `(S_h,S_k)!=(0,0)` and

   \[
                  q p_xs_y=0\qquad(x\in K,\ y\in W),  \tag{5}
   \]

   then `q=0`.

2. If `S_h=S_k=0` and

   \[
      q p_xs_y=0\qquad\text{whenever }x\in K
                                      \text{ or }y\in L,              \tag{6}
   \]

   then

   \[
                    q_{ij}=0\qquad(ij\ne rs).          \tag{7}
   \]

Thus a nonzero exceptional component makes the six-cell map injective;
with two zero components, the nine-dimensional arbitrary block `q_rs` is
the complete eight-cell kernel.

## 3. Square-free coefficient calculation

We record the coefficient argument because the distinction between a
singular nonzero component and a zero component is essential here.

### 3.1 A three-site fact

On three sites, let two components of a three-dimensional star be
isomorphisms and let the third be nonzero.  Multiplication from degree two
to top degree by the whole star has zero common kernel:

\[
 Q\left(A_0y+A_1y+A_2y\right)=0\quad(y\in W)
                         \quad\Longrightarrow\quad Q=0.               \tag{8}
\]

To see this, normalize the two isomorphisms.  A coefficient whose color is
outside `im A_0` first kills the two blocks incident with site zero modulo
`im A_0`.  The remaining two-site coefficients make those incident blocks
factor through `im A_0`; inserting any nonzero coefficient of `A_0` kills
them and then the opposite block.  No division other than by that chosen
nonzero coefficient and the two invertible determinants occurs.  If
`A_0=0`, in contrast, the arbitrary block on the opposite edge is exactly
the kernel.

### 3.2 One active exceptional component

First suppose `S_h!=0` and `S_k=0`.  For `x in K`, put `T_x=q p_x`.
Equation (5) says that `T_x` annihilates the star `s(W)`.  Contracting at
site `k` by an arbitrary covector reduces the three components of `T_x`
which contain `k` to (8) on the active sites `h,r,s`.  Hence those three
components vanish.  Equivalently, on each of the overlapping triples

\[
                         hkr,\qquad hks,\qquad krs,     \tag{9}
\]

we have

\[
 q_{ij}P_\ell x+q_{i\ell}P_jx+q_{j\ell}P_ix=0
                                      \qquad(x\in K).  \tag{10}
\]

Each individual equation (10) is the two-plane Koszul equation and has
one alternating generator.  On the three overlaps, their boundary signs
make its scalar equal successively to its negative.  Since `2!=0`, the
common scalar vanishes and all six blocks of `q` vanish.  The case
`S_h=0,S_k!=0` is symmetric.

### 3.3 Both exceptional components active

Suppose now `S_h,S_k` are both nonzero.  Put

\[
 H_h=\operatorname {im}S_h,\qquad H_k=\operatorname {im}S_k.          \tag{11}
\]

Project the top-degree equation for `T_xs_y` at site `k` to
`V_k/H_k`.  By (8), every component of `T_x` containing `k` has its
`k`-mode in `H_k`.  Projecting at `h` gives the analogous statement there.
Choose complements to `H_h,H_k` and expand the three overlapping Koszul
equations first in the quotient modes and then in the image modes.  The
resulting elimination has the following complete incidence table.  Here
`d_i=dim H_i`, `t=rank(S_h\oplus S_k)`, and
`epsilon_i=dim(H_i\cap P_iK)`:

\[
\begin{array}{c|c|c|c|c}
(d_h,d_k)&t&\epsilon_h&\epsilon_k&\dim\ker(5)\\ \hline
(1,1)&1,2&0,1&0,1&0\\
(1,2)&2,3&0,1&1,2&0\\
(2,1)&2,3&1,2&0,1&0\\
(2,2)&2,3&1,2&1,2&0.
\end{array}                                             \tag{12}
\]

For clarity, this is not a generic-rank table.  After bases are chosen in
the two images and their complements, the quotient equations kill every
block not incident with the corresponding exceptional site.  The image
equations leave three possible common Koszul coefficients.  Their overlap
matrix is the odd three-leg matrix

\[
 (z_{hr},z_{hs},z_{kr},z_{ks},z_{rs})
   \longmapsto
 (z_{hr}+z_{hs},\ z_{kr}+z_{ks},\
  z_{hr}-z_{kr}+z_{rs},\ z_{hs}-z_{ks}-z_{rs}),         \tag{13}
\]

together with unit pivots from the nonzero image maps.  Back-substitution
leaves a scalar equal to its negative, so it vanishes in characteristic
different from two.  The entries encoding the relative positions in
(12) occur only above these pivots.  This proves the zero kernel in every
row of (12), and hence part 1 of Lemma 2.1.

### 3.4 The double-zero branch

Let `S_h=S_k=0` and choose a basis `(u,v)` of `K`.  Condition (5) says
only that the components of `q p_x` on the triples `hkr` and `hks`
vanish.  The two overlapping triangle equations give

\[
 \ker(5)=\mathcal R_{rs}\oplus\mathbb F\Omega,         \tag{14}
\]

where `R_rs=V_r tensor V_s` is the arbitrary opposite-edge block and the
nonzero blocks of `Omega` are

\[
\begin{array}{c|ccccc}
ij&hk&hr&hs&kr&ks\\ \hline
\Omega_{ij}/(P_iu\otimes P_jv-P_iv\otimes P_ju)
  &-1&1&1&-1&-1.
\end{array}                                             \tag{15}
\]

There is no `rs` block in `Omega`.  This proves directly that the six-cell
kernel has dimension `9+1=10`.

Choose `w notin K`.  The two additional erased cells in (6) have
`x=w,y in L`.  The block in `R_rs` remains invisible, because `s_y` is
supported only at `r,s`.  On the other hand, contract the `h,k` modes of
`Omega p_ws_y` by dual covectors selecting respectively `P_hu` and
`P_kv`.  Up to a nonzero scalar the result is

\[
                 P_rw\otimes S_sy-S_ry\otimes P_sw.    \tag{16}
\]

Because `S_r,S_s` are isomorphisms and `L` is a two-plane, choose `y in L`
outside the two lines whose images are parallel to `P_rw` and `P_sw`.
Then (16) is nonzero.  Thus the last two cells kill `Omega` and leave
exactly `R_rs`, proving part 2.

## 4. The actual two-/four-cross sector

Let rows `r_0,s_0` be the completely invertible and two-defect block rows,
respectively.  Let `a,b` be the complementary left sites and put

\[
                         c=\kappa(ab)=\kappa(r_0s_0).   \tag{17}
\]

For each left row and color define its right-site star

\[
 p_{i,x}=\sum_j\operatorname {row}_x(B_{ij})^{(j)}.     \tag{18}
\]

Let

\[
 q_R=\sum_{uv}\rho_{uv}
            E_{\kappa(uv),\kappa(uv)}^{(uv)},\qquad
 q_{\rm eff}=\lambda_{ab}q_R+p_{a,c}p_{b,c},           \tag{19}
\]

where every internal edge weight is nonzero.  Fix colors `c,c` at `a,b`
and colors `x,y` at `r_0,s_0`.  Exact grouping of the matching terms gives

\[
 q_{\rm eff}p_{r_0,x}p_{s_0,y}
       =\text{the complete two-/four-cross coefficient}.             \tag{20}
\]

For `(x,y)!=(c,c)`, the left word is nonconstant and `ab` is its only
compatible internal edge.  The zero-cross and target coefficients vanish,
so the actual tensor equations give all eight erasures

\[
 q_{\rm eff}p_{r_0,x}p_{s_0,y}=0
                                  \qquad((x,y)\ne(c,c)).               \tag{21}
\]

This is precisely Lemma 2.1: the first star has four invertible component
maps, while the second has two invertible and two singular components.

## 5. Endpoint obstruction

Let the exceptional right sites be `h,k` and the regular sites `r,s`.
If either exceptional block in row `s_0` is nonzero, part 1 of Lemma 2.1
and the six cells in (21) give

\[
                              q_{\rm eff}=0.            \tag{22}
\]

If both exceptional blocks are zero, part 2 gives instead

\[
                    (q_{\rm eff})_{hi}=0\qquad(i\ne h),               \tag{23}
\]

because its only possible block is `rs`.  Either (22) or (23) contradicts
the same endpoint geometry.  At endpoint `h`, the three incident blocks of
`lambda_ab q_R` have the three nonzero, distinct coordinate lines

\[
                    \mathbb F e_{\kappa(hi)}\qquad(i\ne h),           \tag{24}
\]

which span `V_h`.  Every incident block of the product correction in
(19), however, has endpoint image in the fixed plane

\[
 \operatorname {span}\left(
   \operatorname {row}_c(B_{ah})^{\mathsf T},
   \operatorname {row}_c(B_{bh})^{\mathsf T}\right).  \tag{25}
\]

Equations (22) or (23) would place all three lines (24) in (25), an
impossibility.  This proves Theorem 1.1.

For the representative (1), row `3` is completely invertible.  Pair it
with row `0`, whose exceptional columns are `0,1`; the possible double-zero
residual is only the regular edge `23`, and endpoint `0` gives (23).
Therefore all 96 labelled supports in the `E_2` orbit are excluded.

## 6. One separated defect against two defects

The same calculation tolerates one more exceptional map on the first
star, provided it is separated from the two exceptions on the second.

**Lemma 6.1 (separated one-plus-two erasure).**  Keep the notation of
Lemma 2.1.  Let `t` be one of the two regular sites of the second star.
Allow `P_t` to be arbitrary, while every `P_i` for `i!=t` remains an
isomorphism.  Assume the two exceptional sites `h,k` of the second star
are distinct from `t`.  If

\[
 q p_xs_y=0\qquad\text{whenever }x\in K\text{ or }y\in L,             \tag{26}
\]

then the same dichotomy holds:

\[
\begin{cases}
q=0,&(S_h,S_k)\ne(0,0),\\
q\in\mathcal R_{tu},&S_h=S_k=0,
\end{cases}                                                           \tag{27}
\]

where `u` is the other regular site.

Here is the additional coefficient check.  Apply first the six-cell slab
`K times W`.  The elimination of Section 3 is unchanged until the final
three-site Koszul compatibility.  Replacing `P_t|K` by a map of rank
`0,1`, or `2` gives

\[
\begin{array}{c|c|c}
 &\text{six-cell residual}&\text{eight-cell residual}\\ \hline
(S_h,S_k)\ne(0,0)&\text{dimension at most }1&0\\
S_h=S_k=0&\mathcal R_{tu}\oplus\mathbb F\Omega'&\mathcal R_{tu}.
\end{array}                                                           \tag{28}
\]

The possible one-dimensional class in the first row occurs only when the
exceptional restriction loses the last Koszul pivot.  Since `S_t` is an
isomorphism and `t` is not `h` or `k`, one of the two cells in
`(U minus K) times L` detects its nonzero hole-`t` alternating tensor,
exactly as in (16).  The same two cells kill `Omega'` in the double-zero
row.  The block `R_tu` is invisible because the second star is supported
only at `t,u`.  This proves (27).  The elimination uses only ranks of
`P_t|K`; it therefore includes zero, rank-one, and rank-two singular
blocks with arbitrary relative bases.

## 7. Exact-seven census and obstruction

The three exact-six residual orbits from the preceding classification are
all gone.  The orbit `E_0=K_(1,3) disjoint-union K_(3,1)` contains three
singleton rows with the same exceptional column, so the coincident-defect
incident theorem excludes it.  Theorem 1.1 excludes `E_1` and `E_2`, since
both have an empty row and another row of singular degree two.  Thus every
solution has at least seven singular blocks before using Lemma 6.1.

Now enumerate seven singular positions subject to all of these erasure
consequences, on rows and columns.  A degree-zero vertex is impossible:
Theorem 1.1 would force each of the other three degrees to be at least
three, already requiring nine positions.  Two degree-one vertices are
also impossible, whether their exceptional neighbours are distinct
(separated-defect erasure) or equal (coincident-defect incident erasure).
The only positive partition of seven into four parts with at most one
singleton is therefore

\[
                              (2,2,2,1).                \tag{29}
\]

Both shores must have this degree partition.  Exact enumeration of all
`binom(16,7)=11440` supports leaves 816 labelled supports in three
`S_4 times S_4 times C_2` orbits:

\[
\begin{array}{c|c|l|l}
 &\text{orbit size}&\text{representative}&\text{graph type}\\ \hline
F_0&144&00,01,10,11,22,23,32&C_4\sqcup P_4\\
F_1& 96&00,01,10,12,21,22,33&C_6\sqcup K_2\\
F_2&576&00,01,10,12,21,23,32&P_8.
\end{array}                                                           \tag{30}
\]

All three are excluded uniformly, without orbit-by-orbit algebra.  Let
row `r_0` be the unique singleton row and let `t` be its exceptional
column.  Column `t` has degree at most two, so among the three degree-two
rows at most one can meet `t`.  Choose a degree-two row `s_0` which does
not.  Its two exceptional columns `h,k` are disjoint from `t`.  The stars
of rows `r_0,s_0` satisfy Lemma 6.1, and the actual eight sector equations
are again (21).

If either block at `s_0h,s_0k` is nonzero, the effective quadratic
vanishes.  If both are zero, it is supported only on the edge joining the
two regular columns.  In either case all three blocks incident with `h`
vanish, and (24)--(25) give the three-axis/two-plane contradiction.  Hence
all 816 supports in (30) are impossible, proving (1a).

## 8. Exact audit

Run

```text
python computations/verify_two_k4_six_cycle_two_defect_obstruction.py
```

The checker verifies:

1. all canonical rank, image-incidence, and joint-kernel cases in (12),
   plus nontrivial relative bases;
2. rank `54/54` whenever either exceptional map is nonzero, with a minimal
   active integer minor of determinant `-32`;
3. the double-zero ranks `44/54` on six cells and `45/54` on eight cells,
   the explicit Koszul bridge (15), and the exact nine-dimensional
   regular-edge kernel;
4. all `1458` coefficients of (20), using both the positive-rank and
   literal-double-zero branches on an exact `E_2` support; and
5. the 96-element `E_2` position orbit and the final endpoint-span
   obstruction;
6. all 125 rank/incidence normal forms for Lemma 6.1, including nontrivial
   relative bases; and
7. the exact-seven census `11440 -> 816`, its three orbit sizes
   `144,96,576`, and all `4374` sector coefficients for positive-rank and
   double-zero representatives of those three orbits.

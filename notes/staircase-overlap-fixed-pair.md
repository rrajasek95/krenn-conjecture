# Fixed-pair overlap of the cyclic staircase

## 1. Outcome

Fix an invertible aggregate edge `A_pq`.  A third vertex `x` for which all
three one-cross constant residues survive is put into the cyclic staircase
normal form of `five-set-contamination-normal-form.md`.  Such a site has a
simple invariant property:

\[
             A_{px}K_rA_{qx}^{T}\ne0\qquad(r=0,1,2).       \tag{1}
\]

Thus a staircase chart does not produce a triple-zero site.  It produces
the opposite extreme: none of the three colors is a zero-cross witness.

Combining (1) with the universal one-hole and two-hole identities gives a
source-global overlap restriction.  For a fixed invertible pair, every
zero-cross witness must be a constant-row degeneracy site.  There are at
least two such sites for each color and at least three different such sites
in total.  In particular, at order eight at most three of the six outside
vertices can have nondegenerate staircase charts.  If exactly three do,
then all three of the other vertices are triple-zero sites.  The only
combinatorially possible escape is a cyclic double-zero pattern, but anchor
saturation and the exact two-hole anchor-rectangle identity rule it out;
the remaining permutation alternative is excluded by the two-witness
bound unless all three anchor colors agree sitewise.

This bound genuinely uses the global annihilation identities.  The local
staircase equations alone admit arbitrarily many compatible charts sharing
one fixed invertible pair.  An explicit family is given in Section 5.  It
also shows that overlap of (32b), without compatibility of the quotient
caps or the other matching sectors, cannot by itself force a clean pair
cap or any finite support bound.

## 2. A staircase site has no zero cross color

Use the cross-product convention

\[
K_0=\begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix},\quad
K_1=\begin{pmatrix}0&0&-1\\0&0&0\\1&0&0\end{pmatrix},\quad
K_2=\begin{pmatrix}0&1&0\\-1&0&0\\0&0&0\end{pmatrix}. \tag{2}
\]

**Lemma 2.1 (staircase--witness incompatibility).**  Let `C={p,q,x}` and
assume all three one-cross constant-row residues for this shore are
nonzero.  If `A_pq` is invertible, then (1) holds.

**Proof.**  Relabel the three vertices and simultaneously permute the three
colors as in Corollary 3.2 of
`five-set-contamination-normal-form.md`.  The chart can be written

\[
\begin{aligned}
 A_{qx}/a_0&=E_{00}+b_0^{-1}(e_1u^T+ve_2^T),\\
 A_{px}/a_1&=E_{11}+b_1^{-1}(-e_0u^T+we_2^T),\\
 A_{pq}/a_2&=E_{22}+b_2^{-1}(-e_0v^T-we_1^T),             \tag{3}
\end{aligned}
\]

where every `a_i,b_i` is nonzero.  The determinant formula for the last
edge is

\[
       \det(A_{pq}/a_2)=b_2^{-2}v_0w_1.                  \tag{4}
\]

Hence invertibility gives `v_0 w_1 != 0`.  Put
`P=A_px/a_1` and `Q=A_qx/a_0`.  Directly from the two indicated rows in
(3), the same matrix entry of the three cross matrices is

\[
 \bigl((PK_0Q^T)_{10},(PK_1Q^T)_{10},(PK_2Q^T)_{10}\bigr)
       =(b_0^{-1}v_0,\ b_1^{-1}w_1,\ -1).                \tag{5}
\]

Every entry in the vector on the right is nonzero.  Restoring the factor
`a_0a_1` proves (1) in this chart.  A simultaneous color permutation only
permutes the three zero/nonzero assertions, and reversing an endpoint
orientation only transposes a cross matrix up to sign.  Thus the conclusion
is invariant under the relabeling used to obtain (3). `QED`

Notice that no invertibility of `A_px` or `A_qx` is required.  The
invertibility of the shared pair alone supplies the two nonzero transfer
coordinates in (5).

## 3. Global restriction for a fixed invertible pair

Let `B` be the even source vertex set, put

\[
 R=B\setminus\{p,q\},\qquad C_x=\{p,q,x\},\qquad
 U_x=B\setminus C_x,                                    \tag{6}
\]

and let `M_{U_x}` be the mixed three-cross row space for the shore `C_x`.
Define the constant-row degeneracy set

\[
 D_{pq}=\{x\in R:\ell_{r^{C_x}}\in M_{U_x}
                       \text{ for at least one }r\}.     \tag{7}
\]

Also define the three zero-cross witness sets

\[
 S_r(p,q)=\{x\in R:A_{px}K_rA_{qx}^T=0\}.               \tag{8}
\]

**Theorem 3.1 (all witnesses lie on the degeneracy boundary).**  In an
exact matching-tensor realization with invertible `A_pq`,

\[
             S_r(p,q)\subseteq D_{pq}\qquad(r=0,1,2).    \tag{9}
\]

Moreover

\[
 |S_r(p,q)|\ge2\quad(r=0,1,2),\qquad
 \left|S_0(p,q)\cup S_1(p,q)\cup S_2(p,q)\right|\ge3.   \tag{10}
\]

Consequently `|D_pq|>=3`.

**Proof.**  If `x` is not in `D_pq`, all three constant one-cross residues
are nonzero.  The three-shore normal form and invertibility of `A_pq` put
the triangle `C_x` in the staircase branch.  Lemma 2.1 says that `x` lies
in none of the sets (8), which proves (9).

The first three bounds in (10) are Corollary 5.2 of
`two-vertex-annihilation-identities.md`; they follow by leaving one outside
site uncontracted.  The union bound is Theorem 6.1 of that note; it follows
by leaving two sites uncontracted.  Inclusion (9) then gives
`|D_pq|>=3`. `QED`

The content of (9) is color-refined: for each target color there are at
least two third vertices which simultaneously have a zero cross matrix in
that color and have some named constant one-cross row in the mixed-row
span.  The degenerate row color need not equal the zero-cross color.

## 4. The eight-vertex finite alternative

Suppose `|B|=8`, so the fixed pair has six outside vertices.  Call
`x in R\D_pq` a nondegenerate staircase site.

**Corollary 4.1 (at most three charts on eight vertices).**  There are at
most three nondegenerate staircase sites for a fixed invertible pair.

If there is at least one such site, some vertex in `D_pq` is a zero-cross
witness for at least two colors.  If there are exactly three staircase
sites, put `D_pq={x_0,x_1,x_2}`.  Then exactly one of the following holds.

1. Some `x_i` is triple-zero:
   \[
             A_{px_i}K_rA_{qx_i}^T=0\quad(r=0,1,2).       \tag{11}
   \]
2. After relabeling the sites and colors,
   \[
   S_0=\{x_1,x_2\},\qquad
   S_1=\{x_0,x_2\},\qquad
   S_2=\{x_0,x_1\}.                                    \tag{12}
   \]
   At the site `x_r`, the two row spaces obey
   \[
      \operatorname{row}A_{px_r},\operatorname{row}A_{qx_r}
             \subset e_r^\perp,
      \qquad
      \operatorname{row}A_{px_r}+\operatorname{row}A_{qx_r}
             =e_r^\perp.                                \tag{13}
   \]

**Proof.**  Theorem 3.1 gives `|D_pq|>=3`, proving the first assertion.
There are at least six zero-cross incidences, two for each color.  If a
staircase site exists, `|D_pq|<=5`, so one site supports at least two of
these incidences.

Now suppose the complement of `D_pq` has size three.  Then `D_pq` also has
size three.  If no site is triple-zero, each site supports at most two
zero colors.  The lower bound of six incidences is therefore attained with
equality: every `S_r` has size two and every site belongs to exactly two of
them.  The unique incidence pattern is (12).  At `x_r` the missing witness
color is `r`.  The local row-space classification for exactly two witness
colors (Lemma 3.1(2) of
`general-invertible-pair-witness-incidence.md`) gives (13). `QED`

Already two staircase sites force entry into the triple-zero boundary.

**Corollary 4.1a (two charts force a triple-zero site).**  If an
eight-vertex exact realization has at least two nondegenerate staircase
sites for a fixed invertible pair `pq`, then some outside site `x` obeys

\[
                    A_{px}K_rA_{qx}^T=0
                    \qquad(r=0,1,2).                    \tag{13a}
\]

**Proof.**  It suffices to treat exactly two staircase sites; with three,
Corollary 4.3 below applies.  Thus `|D_pq|=4`.  Suppose no site is
triple-zero.  Every site of `D_pq` then belongs to at most two witness
sets.  Since each of the three sets `S_r` has size at least two,

\[
                6\le\sum_r|S_r|\le8.                   \tag{13b}
\]

In particular some color `r` has `|S_r|=2`.

Choose one forced directed `r`-anchor from `p`, at `u`, and one from `q`,
at `v`.  Both lie in `D_pq`, and `u!=v`, since equality would make that
site triple-zero.  They are both in `S_r`, so
`S_r={u,v}`.  The opposite blocks `A_qu,A_pv` are nonzero and are not
directed `r`-anchors, again because either exception would make a
triple-zero site.  Theorem 6.2 of
`two-vertex-annihilation-identities.md` therefore rules out
`J(u,v)={r}` and forces

\[
                 J(u,v)=\{r,s\}                         \tag{13c}
\]

for another color `s`.  Moreover the theorem makes the opposite blocks
directed `s`-anchors.  Hence `S_s={u,v}`, with the four blocks at `u,v`
forming the swapped anchor rectangle

\[
 \begin{array}{c|cc}
      &p&q\\ \hline
   u&r&s\\
   v&s&r.
 \end{array}                                             \tag{13d}
\]

Let `t` be the third color and let `y,z` be the other two sites of
`D_pq`.  Neither `u` nor `v` can carry a directed `t`-anchor, so the
forced `t`-anchors from `p,q` occupy `y,z`; they are distinct under the
no-triple-zero assumption.  The cross product of the distinct coordinate
row lines at `u,v` is in color `t`, so those two sites are not in `S_t`.
Consequently

\[
                         S_t=\{y,z\}.                    \tag{13e}
\]

But now `J(y,z)={t}`.  Both opposite blocks at `y,z` are nonzero and are
not `t`-anchors, so the first alternative of the same anchor-rectangle
theorem is impossible.  This contradiction proves (13a). `QED`

Thus the extremal three-chart overlap reduces the other half of the six
outside sites to either the already-studied triple-zero branch or one
explicit cyclic arrangement of the three coordinate annihilator planes.

The forced incident-edge theorem sharpens the extremal case further.

**Corollary 4.2 (anchor saturation in the three-chart case).**  Suppose
there are exactly three staircase sites, so `|D_pq|=3`.  For every
`x in D_pq` there are nonzero column vectors `a_x,b_x` and colors
`alpha(x),beta(x)` such that

\[
       A_{px}=a_xe_{\alpha(x)}^T,\qquad
       A_{qx}=b_xe_{\beta(x)}^T,                          \tag{14a}
\]

and both maps `alpha,beta:D_pq->{0,1,2}` are bijections.  Either
`alpha(x)=beta(x)` at some site, which is a triple-zero site, or, after
identifying the three sites with their `alpha` colors, `beta` is one of
the two 3-cycles.  In the latter case the two zero-cross colors at `x` are
exactly `alpha(x),beta(x)` and the missing color is the third one.

**Proof.**  A directed `r`-anchor from `p` at a site `x` has
`A_px=ae_r^T!=0`, and therefore

\[
                  A_{px}K_rA_{qx}^T=0.                  \tag{14b}
\]

Lemma 2.1 rules this out at a staircase site.  The invertible edge `pq`
cannot itself be a directed anchor.  Hence the forced incident-edge
theorem puts one directed anchor from `p`, for each of the three colors,
among the three sites of `D_pq`.  A nonzero matrix cannot be a directed
anchor of two different colors, so the three anchors occupy the three
sites bijectively.  This proves the first formula in (14a) and bijectivity
of `alpha`; the argument at `q` proves the second.

If `alpha(x)=beta(x)`, the two row spaces are the same coordinate line and
all three cross matrices vanish.  Otherwise their cross product is a
nonzero multiple of the remaining coordinate vector, so exactly the two
listed colors are zero witnesses.  If equality never occurs, the
permutation `beta o alpha^{-1}` has no fixed point.  A derangement of
three symbols is a 3-cycle. `QED`

Thus the non-triple-zero extremal branch is not merely a cyclic incidence
pattern: it consists of six saturated rank-one anchors, with the two
endpoint colorings differing by a 3-cycle.  This is a finite source-level
configuration on which a subsequent pair-cap calculation can be made
without any remaining row-space freedom.

In fact the two-hole identity rejects this last configuration.

**Corollary 4.3 (three charts force a triple-zero site).**  Under the
hypotheses of Corollary 4.2, some `x in D_pq` satisfies

\[
                   A_{px}K_rA_{qx}^T=0
                   \qquad(r=0,1,2).                     \tag{14c}
\]

**Proof.**  Suppose not.  Use the cyclic anchor description of Corollary
4.2.  Fix a color `r`, let

\[
             u=\alpha^{-1}(r),\qquad v=\beta^{-1}(r).    \tag{14d}
\]

Then `u!=v`, the block `A_pu` is a nonzero directed `r`-anchor from `p`,
and `A_qv` is a nonzero directed `r`-anchor from `q`.  The cyclic witness
pattern gives

\[
                         S_r(p,q)=\{u,v\}.               \tag{14e}
\]

The three two-element witness sets are the three different pairs in
`D_pq`, so the notation of Theorem 6.2 in
`two-vertex-annihilation-identities.md` gives `J(u,v)={r}`.  Its first
anchor-rectangle alternative says that either `A_qu=0`, or `A_pv=0`, or
both opposite blocks are directed `r`-anchors.

Anchor saturation says instead that

\[
       A_{qu}=b_ue_{\beta(u)}^T\ne0,\qquad
       A_{pv}=a_ve_{\alpha(v)}^T\ne0.                    \tag{14f}
\]

Because `beta o alpha^{-1}` is a 3-cycle,
`beta(u)!=r` and `alpha(v)!=r`.  Thus neither opposite block is an
`r`-anchor, contradicting every alternative of the two-hole theorem.
`QED`

Therefore the second branch in Corollary 4.1 is a useful intermediate
normal form but not an actual exact realization: the extremal overlap of
three nondegenerate charts already forces (14c).

The permutation structure then propagates the one triple-zero site to all
three degenerate sites.

**Corollary 4.4 (the exact three-plus-three pattern).**  If an invertible
pair on an eight-vertex exact realization has exactly three nondegenerate
staircase sites, then every site in `D_pq` is triple-zero.  Equivalently,
the six outside sites split exactly as

\[
 \begin{array}{c|c}
  3\text{ staircase sites}&
       A_{px}K_rA_{qx}^T\ne0\text{ for every }r\\
  3\text{ saturated anchor sites}&
       A_{px}K_rA_{qx}^T=0\text{ for every }r.
 \end{array}                                             \tag{14g}
\]

At the three triple-zero sites, after labeling them by color,

\[
             A_{px_r}=a_re_r^T,\qquad
             A_{qx_r}=b_re_r^T,
             \qquad a_r,b_r\ne0.                         \tag{14h}
\]

**Proof.**  By Corollary 4.3, the relative permutation
`pi=beta o alpha^{-1}` has a fixed point.  A permutation of three symbols
with a fixed point is either the identity or a transposition.  Suppose it
is a transposition and let `c` be its unique fixed color.  At the fixed
site the two anchor row lines agree, so that site is a zero witness for
color `c`.  At each of the two swapped sites the row lines are the other
two distinct coordinate lines, whose cross product is a nonzero multiple
of `e_c`; neither site is a zero witness for `c`.  Lemma 2.1 excludes the
three staircase sites as well.  Hence `|S_c(p,q)|=1`, contradicting the
two-witness bound (10).  Therefore `pi` is the identity.  Formula (14a)
then gives (14h), and all three sites are triple-zero. `QED`

## 5. Arbitrarily many local charts can share one pair

The preceding finite bound does not follow from the staircase equations
alone.  Let

\[
 v=w=(1,1,1)^T,\qquad
 A_{pq}=E_{22}-e_0v^T-we_1^T
       =\begin{pmatrix}-1&-2&-1\\0&-1&0\\0&-1&1\end{pmatrix}. \tag{15}
\]

For every label `x`, independently choose
`u_x=(1,1,t_x)^T` and set

\[
\begin{aligned}
 A_{qx}&=E_{00}+e_1u_x^T+ve_2^T,\\
 A_{px}&=E_{11}-e_0u_x^T+we_2^T.                         \tag{16}
\end{aligned}
\]

All three matrices in each triangle are invertible:

\[
             \det A_{pq}=1,\qquad
             \det A_{px}=-1,\qquad
             \det A_{qx}=1.                             \tag{17}
\]

For every `x`, with the slots in the displayed vertex order, the exact
three-slice identity is

\[
 e_0^{(p)}\otimes A_{qx}
 +e_1^{(q)}\otimes A_{px}
 +e_2^{(x)}\otimes A_{pq}
       =e_0^{\otimes C_x}+e_1^{\otimes C_x}
                         +e_2^{\otimes C_x}.             \tag{18}
\]

Indeed, the two occurrences of each of
`e_0 e_1 u_x`, `e_0 v e_2`, and `w e_1 e_2` cancel, leaving only the three
pure diagonal cells.  The construction works for arbitrarily many labels
`x`, and (5) becomes

\[
 \bigl((A_{px}K_0A_{qx}^T)_{10},
       (A_{px}K_1A_{qx}^T)_{10},
       (A_{px}K_2A_{qx}^T)_{10}\bigr)=(1,1,-1).          \tag{19}
\]

This is an exact countermodel to any proposed conclusion based only on
overlapping instances of (32b): neither a zero-cross color nor a bound on
the number of third vertices follows.  It is not asserted to extend to a
global matching-tensor realization; the one-hole identities show that it
cannot do so with every outside vertex remaining in the nondegenerate
chart branch.

## 6. Support alignment of the shared edge

There is one further local invariant, useful for organizing the finitely
many charts.  Formula (3) says that, after one simultaneous color
permutation, `A_pq` is upper triangular:

\[
 \operatorname{supp}A_{pq}
 \subseteq\{(i,i):0\le i\le2\}
       \cup\{(i,k),(i,j),(k,j)\}                         \tag{20}
\]

for a total order `i<k<j`, and all three diagonal entries are nonzero.
Conversely every invertible matrix with support of the form (19) occurs as
the shared pair in a staircase identity: take its middle diagonal entry as
`a_2`, recover the row vector `v` and column vector `w` from the five other
allowed cells (splitting the corner `(i,j)` arbitrarily), and then use
(3).

If all three off-diagonal cells in (19) are nonzero, their orientation
determines the total order uniquely.  Hence every nondegenerate third-site
chart assigns the same coordinate axis to `p`, the same middle axis to the
third vertex, and the same coordinate axis to `q`.  This alignment still
does not couple the free vectors `u_x`, as the family (15)--(18) shows.

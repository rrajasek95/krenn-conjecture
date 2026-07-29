# The corank-two relation space closes the local-full block branch

## 1. Outcome

Let `E_q` be the two-dimensional excess Hessian quotient for a deleted
pair, and assume the six off-diagonal classes have the row-column basis
property.  Their four-dimensional relation space contains substantially
more information than any one alternating relation.  On a rank-three
internal edge, its whole physical block image is at most three-dimensional.

When the three rows of one deleted star form a basis at both endpoints of
that edge, the resulting `3 by 3` block map has only two exact possibilities.

* Its relation-space image is zero.  Then the other star has rank at most
  one at both endpoints, and at the two endpoints it is supported on the
  same single colour column.
* Its relation-space image is the invertible internal-block line.  Then
  the other star is obtained from the first at both endpoints by the same
  invertible diagonal colour matrix.

There is no intermediate rank-two case.  On a connected rank-three graph,
the first alternative propagates a globally missing colour row, while the
second propagates one diagonal matrix and then one common invertible
symmetric zero-diagonal internal colour matrix.  The first contradicts the
dense-row hypothesis, and the second is killed by the simultaneous
orthogonal-colour argument of
[`cauchy-shared-matrix-diagonal-obstruction.md`](cauchy-shared-matrix-diagonal-obstruction.md).

Consequently the local-full corank-two branch is impossible without any
faithfulness assumption on the third osculating symbol.

## 2. The six directions and their four relations

Use the notation of
[`hessian-corank-two-osculating-dichotomy.md`](hessian-corank-two-osculating-dichotomy.md).
For `c != d`, put

\[
                         u_{cd}=[K_{cd}]\in E_q.
\]

Suppose `dim E_q=2` and every row and every column pair is a basis:

\[
 \{u_{cd}:d\ne c\}\text{ is a basis},\qquad
 \{u_{cd}:c\ne d\}\text{ is a basis}.                 \tag{1}
\]

Let

\[
 Z_0=\{M=(m_{cd})\in\operatorname {Mat}_3(\mathbb C):m_{cc}=0\}
\]

and define

\[
 f:Z_0\longrightarrow E_q,
 \qquad f(M)=\sum_{c\ne d}m_{cd}u_{cd},
 \qquad \mathscr D=\ker f.                             \tag{2}
\]

Then

\[
                         \dim\mathscr D=4.              \tag{3}
\]

For a fixed first index and a fixed second index, respectively, write

\[
 R_c=\operatorname {span}\{E_{cd}:d\ne c\},\qquad
 C_d=\operatorname {span}\{E_{cd}:c\ne d\}.            \tag{4}
\]

The two basis assertions in (1) say exactly

\[
                 \mathscr D\cap R_c=0,\qquad
                 \mathscr D\cap C_d=0                 \tag{5}
\]

for every `c,d`.  These avoidance statements are the essential input
which is lost if one retains only a single relation among the six classes.

At an internal pair `ij`, package the local star columns as

\[
 P_i=(p_{0,i}\ p_{1,i}\ p_{2,i}),\qquad
 S_i=(s_{0,i}\ s_{1,i}\ s_{2,i}).                     \tag{6}
\]

The physical block of the relation represented by `M` is

\[
 \mathcal L_{ij}(M)=P_iMS_j^{\mathsf T}
                         +S_iM^{\mathsf T}P_j^{\mathsf T}.             \tag{7}
\]

Indeed, the block of `p_cs_d` is
`p_(c,i)s_(d,j)^T+s_(d,i)p_(c,j)^T`.  Since a member of
`mathscr D` is a Hessian gauge after adding its scalar multiple of `q`,

\[
                 \mathcal L_{ij}(\mathscr D)
                              \subseteq\mathbb Cq_{ij}. \tag{8}
\]

Modulo the line `C q_ij`, the map (7) annihilates `mathscr D` and hence
factors through the two-space `Z_0/mathscr D`.  Therefore

\[
                         \operatorname {rank}\mathcal L_{ij}\le3.     \tag{9}
\]

This proves the asserted rank bound without a genericity assumption.

## 3. Exact local classification

We isolate the linear-algebra statement.  For a colour `c`, let

\[
 \mathcal X_c=\{N\in\operatorname {Mat}_3:
                N_{ab}=0\text{ whenever }a,b\ne c\}.   \tag{10}
\]

Every matrix in `mathcal X_c` has rank at most two, and

\[
 \mathcal X_c\cap\mathcal X_d
       =\operatorname {span}\{E_{cd},E_{dc}\}\quad(c\ne d),
 \qquad \bigcap_c\mathcal X_c=0.                       \tag{11}
\]

**Theorem 3.1 (relation-space block classification).**  Let
`mathscr D subset Z_0` be a four-plane satisfying (5).  Let `A,B` be
`3 by 3` matrices and put

\[
 T_{A,B}(M)=MB^{\mathsf T}+AM^{\mathsf T}.              \tag{12}
\]

Suppose that `H` is invertible and

\[
                         T_{A,B}(\mathscr D)\subseteq\mathbb C H.      \tag{13}
\]

Then exactly one of the following holds.

1. **Dead relation line.**  `T_(A,B)(mathscr D)=0` and
   `rank T_(A,B)<=1`.  If the rank is zero, `A=B=0`.  If the rank is one,
   there are a colour `delta` and a nonzero vector `v`, with
   `v_delta=0`, such that

   \[
                            A=v e_\delta^{\mathsf T},
              \qquad       B=-v e_\delta^{\mathsf T}.                \tag{14}
   \]

2. **Live relation line.**  `T_(A,B)(mathscr D)=C H`,
   `rank T_(A,B)=3`, and

   \[
                            A=B=\operatorname {diag}(d_0,d_1,d_2),
              \qquad       d_0d_1d_2\ne0.              \tag{15}
   \]

In the second case `C H` is a line of invertible symmetric
zero-diagonal matrices.

### Proof: the dead case

The quotient by `mathscr D` has dimension two, so (13) first gives
`rank T<=3`.  Suppose `T(mathscr D)=0`.  If `rank T=2`, then
`dim ker T=4`, hence `mathscr D=ker T`.  By (5), `T` is injective on
every `R_c`; consequently

\[
                         T(R_c)=\operatorname {im}T
                         \subseteq\mathcal X_c           \tag{16}
\]

for all three `c`.  Equation (11) would give `im T=0`, a contradiction.
Rank three is already excluded by `dim ker T=3<dim mathscr D`.  Thus
`rank T<=1`.

For completeness, the rank-one normal form is elementary.  Put

\[
 v_{cd}=T(E_{cd})=e_c(Be_d)^{\mathsf T}
                           +(Ae_d)e_c^{\mathsf T}.       \tag{17}
\]

Thus `v_cd in mathcal X_c`.  If the common nonzero image line occurs for
all three first indices, it lies in `intersection_c mathcal X_c=0`.
Hence it occurs for at most two first indices.

If it occurs for two, say zero and one, then the two outputs with first
index two vanish.  Thus the first two columns initially have only their
opposite bottom entries available.  Requiring the remaining outputs to
lie in `mathcal X_0 intersection mathcal X_1=span(E_01,E_10)` kills
those entries as well.  Only column two can survive, and its diagonal
and directed outputs say that its two matrices are opposite:

\[
                         A=v e_2^{\mathsf T},\qquad
                         B=-v e_2^{\mathsf T},\qquad v_2=0.            \tag{18}
\]

If the image line occurs for only one first index, the same entry
comparison makes the column with that first index zero and leaves two
possible opposite columns.  Their images are supported on two different
skew coordinate lines, so rank one makes one column zero.  This again
gives (18), after a permutation of the colours.
If every `v_cd` vanishes, applying (17) for the two choices `c != d` in
each fixed column gives `A=B=0`.  This proves the dead alternative.

### Proof: a live line cannot have rank two

Suppose next that `T(mathscr D)=C H`.  Rank one is impossible: the image
would be the invertible line `C H`, whereas every generator (17) has rank
at most two.  Assume for contradiction that `rank T=2`.  Put
`K=ker T`; then `dim K=4` and

\[
                  K_0=K\cap\mathscr D\quad\text{has dimension }3.    \tag{19}
\]

For each `c`, the restriction of `T` to `R_c` has rank exactly one.  It
cannot have rank zero, since then the two-plane `R_c subset K` would meet
the three-plane `K_0 subset K` nontrivially, contrary to (5).  It cannot
have rank two, since then the full image of `T` would lie in
`mathcal X_c` and could not contain the invertible matrix `H`.

Let `N_c=T(R_c)`, a nonzero line in `mathcal X_c`.  The three lines span
the two-space `im T`.  They cannot all coincide.  There are two cases.

If they are pairwise distinct, rescale generators so that

\[
 \begin{aligned}
 N_0&=\mathbb C(R_{01}+R_{02}),\\
 N_1&=\mathbb C(-R_{01}+R_{12}),\\
 N_2&=\mathbb C(-R_{02}-R_{12}),                         \tag{20}
 \end{aligned}
\]

where `R_cd` is a nonzero matrix on the two directed entries `cd,dc`.
If one `R_cd` vanished, every matrix in the pencil would miss one
unordered colour pair and would be singular.  Since the pencil contains
`H`, all three are nonzero.

Every `N_c` in (20) has zero diagonal.  Applying this to the generators
gives

\[
                         A_{cd}=-B_{cd}\qquad(c\ne d).  \tag{20a}
\]

The component of `v_cd` on the edge joining `c` to the third colour is
always alternating: it is a scalar multiple of
`E_ce-E_ec`.  Hence, if for example `R_01` were not alternating, both
`v_02` and `v_12` would have to vanish.  The two equations in column two
then force column two of both `A` and `B` to vanish.  Since `N_0,N_1` are
nonzero, `v_01` and `v_10` are nonzero.  Their diagonal-column components
are nonzero, so the corresponding components make `v_20` and `v_21`
nonzero as well.  Now `v_21` forces `R_02` to be alternating.  But the
same diagonal pair from column zero occurs on `R_01` in `v_10` and on
`R_02` in `v_20`; it then forces `R_01` to be alternating, a contradiction.
Thus all three `R_cd` are alternating, and every matrix in `im T` is a
skew `3 by 3` matrix.  Such a matrix is singular, again contradicting the
presence of `H`.

It remains that two row lines coincide.  Permuting colours, write

\[
 N_0=N_1=\mathbb C N,\qquad
 N=xE_{01}+yE_{10},\qquad (x,y)\ne(0,0).                \tag{21}
\]

First suppose that `x+y != 0`.  Entry comparison in the four conditions
`v_01,v_02,v_10,v_12 in C N` then gives

\[
 A=\begin{pmatrix}
 t_{10}x&-u&0\\-v&t_{01}y&0\\0&0&0
 \end{pmatrix},\qquad
 B=\begin{pmatrix}
 t_{10}y&u&0\\v&t_{01}x&0\\0&0&0
 \end{pmatrix},                                        \tag{22}
\]

with `v_02=v_12=0`.  The remaining two outputs are

\[
 \begin{aligned}
 v_{20}&=\begin{pmatrix}0&0&t_{10}x\\0&0&-v\\
                         t_{10}y&v&0\end{pmatrix},\\
 v_{21}&=\begin{pmatrix}0&0&-u\\0&0&t_{01}y\\
                         u&t_{01}x&0\end{pmatrix}.       \tag{23}
 \end{aligned}
\]

They span the one line `N_2`.  Direct expansion gives

\[
          \det(aN+bv_{20})=\det(aN+bv_{21})=0           \tag{24}
\]

identically in all displayed parameters.  Hence every matrix in the
two-space `span(N,N_2)` is singular.  This final contradiction excludes
this subcase.

There is one additional subcase which must be kept separate.  If
`x+y=0`, rescale so that `x=1,y=-1`; thus `N` is alternating.  The same
entry comparison now permits `v_02` and `v_12` to be nonzero.  Its full
normal form is

\[
 A=\begin{pmatrix}
 t_{10}&-u&t_{12}\\-v&-t_{01}&-t_{02}\\0&0&0
 \end{pmatrix},\qquad
 B=\begin{pmatrix}
 -t_{10}&u&-t_{12}\\v&t_{01}&t_{02}\\0&0&0
 \end{pmatrix}=-A.                                    \tag{24a}
\]

In particular

\[
                  T_{A,B}(M)=AM^{\mathsf T}-MA^{\mathsf T}
\]

is skew-symmetric for every `M`.  Its image therefore contains no
invertible `3 by 3` matrix.  This contradiction completes the exclusion
of rank two.

### Proof: classification in rank three

We now have `rank T=3`.  Its kernel has dimension three.  Since
`dim mathscr D=4` and its image is one-dimensional,

\[
                     \ker T\subset\mathscr D,\qquad
                     T(\mathscr D)=\mathbb C H.          \tag{25}
\]

Moreover `T^{-1}(C H)` has dimension four, so (25) says
`T^{-1}(C H)=mathscr D`.  It follows from (5) that `T` is injective on
all six planes `R_c,C_d`, and their images avoid `C H`.

Put `U=im T` and `U_c=T(R_c)`.  Then `U_c` is a two-plane in
`U intersection mathcal X_c`.  Since `H` is invertible,
`U intersection mathcal X_c=U_c`.  The three planes `U_c` are distinct.
Indeed, if `U_c=U_d`, it is the full two-space
`span(E_cd,E_dc)`.  Projection to the principal `cd by cd` block has rank
at least two on `U`, so its kernel `U intersection mathcal X_e`, for the
third colour `e`, has dimension at most one, contradicting
`dim U_e=2`.

Consequently

\[
 \ell_{cd}=U_c\cap U_d
       \subseteq\operatorname {span}\{E_{cd},E_{dc}\}  \tag{26}
\]

is a line for every unordered pair, and the three disjointly supported
lines span `U`.  Thus every matrix in `U` has zero diagonal.  Applying
this to (17) gives

\[
                         A_{cd}=-B_{cd}\qquad(c\ne d).  \tag{27}
\]

Suppose an off-diagonal entry `B_(ed)` is nonzero, with `c,d,e` distinct.
The corresponding component of `v_cd` makes `ell_ce` the alternating
line.  If `(A_dd,B_dd)` were nonzero, it would orient both `ell_cd` and
`ell_ed` by the same ordered pair.  After permuting colours so that
`d=2`, every matrix in `U` would have the form

\[
 \begin{pmatrix}
 0&z&xB_{22}\\-z&0&yB_{22}\\xA_{22}&yA_{22}&0
 \end{pmatrix},                                        \tag{28}
\]

whose determinant is identically zero.  This contradicts `H in U`.
Hence `A_dd=B_dd=0`.  But then the two outputs in the column plane `C_d`
are both multiples of the one alternating line `ell_ce`, contradicting
injectivity on `C_d`.  Therefore every off-diagonal entry of `B`, and by
(27) of `A`, is zero.

Write `a_d=A_dd` and `b_d=B_dd`.  On an unordered pair `cd`, the two
outputs are

\[
 b_dE_{cd}+a_dE_{dc},\qquad
 a_cE_{cd}+b_cE_{dc}.                                  \tag{29}
\]

They span the one line `ell_cd`, so

\[
                         a_ca_d=b_cb_d\qquad(c\ne d).   \tag{30}
\]

Injectivity on every column plane says `(a_d,b_d) != (0,0)`.  If one
`a_d` or `b_d` vanished, (30) and the other two nonzero pairs would give
an immediate contradiction; hence all six scalars are nonzero.  The
ratios `r_d=a_d/b_d` obey `r_cr_d=1` for all distinct `c,d`, so

\[
                         r_0=r_1=r_2=\epsilon,\qquad
                         \epsilon^2=1.                  \tag{31}
\]

For `epsilon=-1`, the whole image is skew-symmetric and contains no
invertible matrix.  Therefore `epsilon=1`, which is exactly (15).
Since `MD+DM^T` is symmetric and zero-diagonal for diagonal `D` and
`M in Z_0`, the last assertion follows.  This completes the proof of
Theorem 3.1. `QED`

## 4. Propagation on the rank-three graph

Return to (7), and suppose

\[
                         P_i\text{ is invertible for every internal }i. \tag{32}
\]

On an edge `ij` of `G_3(q)`, left-right multiplication by
`P_i^(-1),P_j^(-T)` puts (7) into (12), with

\[
                         A_i=P_i^{-1}S_i,qquad
                         A_j=P_j^{-1}S_j.               \tag{33}
\]

Theorem 3.1 applies to the transformed invertible block.

Call the edge live when its relation-space image is nonzero.  On a live
edge,

\[
                         A_i=A_j=D_{ij}                 \tag{34}
\]

for an invertible diagonal matrix.  A dead edge has both endpoint
matrices of rank at most one.  Therefore no live edge is adjacent to a
dead edge.  Connectedness of `G_3(q)` makes all its edges live or all dead.

If all are dead, Theorem 3.1 says that on each edge the two endpoint
matrices either both vanish, or both have one nonzero column with the same
colour index.  A zero endpoint propagates zero through the connected
graph.  Otherwise the unique column index propagates.  Hence either every
`S_i` is zero, or two of the three global rows `s_d` vanish identically.
Both conclusions contradict the dense-row hypothesis.

Thus all edges are live.  Equations (34) and connectedness give one global
invertible diagonal matrix

\[
                         D=\operatorname {diag}(d_0,d_1,d_2),
 \qquad                  S_i=P_iD\quad\text{for every }i.              \tag{35}
\]

Make the sitewise changes `P_i^(-1)`.  The block map is now the same on
every internal pair:

\[
                         T_D(M)=MD+DM^{\mathsf T}.       \tag{36}
\]

For a live edge, `T_D(mathscr D)` is one fixed nonzero line `C H`.
Choose `M_0 in mathscr D` with `T_D(M_0)=H`.  Relation (8) holds on every
internal pair, not merely on `G_3(q)`.  Hence

\[
                         H\in\mathbb C q'_{ij}\quad(i<j),             \tag{37}
\]

where `q'_(ij)=P_i^(-1)q_ijP_j^(-T)`.  Since `H` is invertible, every
block is nonzero and

\[
                         q'_{ij}=w_{ij}H                \tag{38}
\]

for one common invertible symmetric zero-diagonal matrix `H`.  In
particular the argument automatically upgrades the rank-three graph to
the complete graph.

## 5. Contradiction from the pair equations

After the same site changes,

\[
                         p_c=\sum_i e_c^{(i)},\qquad
                         s_d=d_dp_d.                    \tag{39}
\]

The pair equations become

\[
 d_d\mathcal H_q(p_cp_d)+a_{cd}Q=\delta_{cd}X'_c,       \tag{40}
\]

where the three `X'_c` are nonzero and linearly independent.  Let

\[
 G=\{g\in SL_3:gHg^{\mathsf T}=H\}.
\]

The simultaneous action of `G` at all internal sites fixes `q` and `Q`.
Thus

\[
 \overline\Phi:\operatorname {Sym}^2\mathbb C^3
       \longrightarrow (\text{top support})/\mathbb C Q,
 \qquad
 u\odot v\longmapsto[\mathcal H_q(p(u)p(v))]           \tag{41}
\]

is equivariant.  Since every `d_d` is nonzero, the off-diagonal equations
in (40) put all three off-diagonal coordinate directions in its kernel.
The `G`-span of those directions is all of `Sym^2 C^3`: the invariant
line `C H` is already in their span, and their trace-free intersection is
a nonzero part of the irreducible five-dimensional trace-free summand.
Therefore `bar Phi=0`.

The three diagonal equations in (40) now put all `X'_c` in the line
`C Q` (and give `X'_c=0` if `Q=0`).  This contradicts their independence.
We have proved:

**Corollary 5.1 (local-full corank two is impossible).**  Under the
connected spanning rank-three graph hypothesis and the row-column basis
property (1), the pair equations cannot hold if `P_i` is invertible at
every internal site and all three rows of the other star are nonzero.
The symmetric assertion holds with the two deleted stars interchanged.

The hypothesis (32) is not automatic from connectedness.  The singular
edge classification and
[`live-component-zero-cut-propagation.md`](live-component-zero-cut-propagation.md)
give the sharp replacement: if one live edge exists, all invertible-star
sites form a complete live component, while every rank-three boundary
vertex has both star matrices literally zero.  Thus the only obstruction
to applying this section globally is an explicit two-star-zero vertex cut.

No injectivity of `III_q`, and no projective proportionality between
`u_cd` and `u_dc`, is used.

## 6. Exact audit

[`verify_corank_two_local_block_classification.py`](../computations/verify_corank_two_local_block_classification.py)
checks over the exact symbolic field:

1. the block formula (17) and the rank-three diagonal normal form;
2. the determinant-zero identities (24) for the repeated-row-line
   rank-two case, together with the omitted alternating-line family
   (24a) and its skew-symmetric image;
3. the determinant-zero identity (28) used to eliminate off-diagonal
   endpoint entries;
4. the pair determinants (30) and their two sign solutions; and
5. the rank-one dead normal form (14).

The script certifies the coordinate calculations only; the dimension and
propagation arguments are proved above.

# The all-dead corank-two product geometry reduces to one aligned two-plane

## 1. Statement and outcome

Let

\[
 {\cal R}=\bigotimes_{i\in I}(\mathbb C\oplus V_i),
 \qquad V_i^2=0,
 \qquad {\cal R}_1=\bigoplus_iV_i .                    \tag{1}
\]

For `x,y in R_1`, write `xy` for their product in `R_2`.  Thus its
`ij` block, for `i!=j`, is

\[
                 x_i y_j^{\mathsf T}+y_i x_j^{\mathsf T}.             \tag{2}
\]

Fix six nonzero linear elements `p_0,p_1,p_2,s_0,s_1,s_2`.  Assume

1. every one of the six elements reaches at least three sites;
2. every pair among the `p_c`, and every pair among the `s_d`, is
   linearly independent;
3. the six products `p_c s_d`, `c!=d`, span a two-space `W`; and
4. in every fixed row and every fixed column the two off-diagonal
   products form a basis of `W`.

This is exactly the global product configuration obtained when every
relation edge in the corank-two relation space is dead.  The purpose of
this note is to retain the same-site terms while exploiting that deadness.

The following cases are closed here.

**Theorem 1.1 (reduction to the aligned two-plane).**  Put

\[
 P=\langle p_0,p_1,p_2\rangle,
 \qquad S=\langle s_0,s_1,s_2\rangle .                 \tag{3}
\]

If either `dim P<=2` or `dim S<=2`, then all three diagonal products
`p_c s_c` already belong to `W`.  Suppose instead that both dimensions
are three and put `k=dim(P intersection S)`.

* The cases `k=0` and `k=1` are impossible.
* If `k=3`, the span of all nine products has dimension at most four.  On
  the only chart not closed by the intrinsic alternating kernel, its
  dimension is in fact at most three.
* If `k=2`, the span of all nine products has dimension at most four
  unless the unique intrinsic alternating relation belongs to the
  four-dimensional off-diagonal relation space.

Consequently the desired assertion

\[
 \dim {\langle p_cs_c:c=0,1,2\rangle+W\over W}\le2                 \tag{4}
\]

is reduced to one exact locus: `dim P=dim S=3`, `dim(P intersection
S)=2`, and the intrinsic rank-two relation is literally zero-diagonal in
the named colour bases.  Section 8 gives its normal form.

That last locus, including every singular normalization boundary, is
excluded in
[`aligned-two-plane-boundary-closure.md`](aligned-two-plane-boundary-closure.md)
together with Propositions 9.1--9.2 of
[`all-dead-corank-two-product-reduction.md`](all-dead-corank-two-product-reduction.md).

## 2. The relation four-plane

Let

\[
 Z_0=\{M\in\operatorname {Mat}_3:M_{00}=M_{11}=M_{22}=0\}
\]

and define

\[
 T(M)=\sum_{c,d}m_{cd}p_cs_d\in{\cal R}_2,
 \qquad {\mathscr D}=\ker(T|_{Z_0}).                    \tag{5}
\]

The assumptions give

\[
 \dim\mathscr D=4,
 \qquad \mathscr D\cap R_c=\mathscr D\cap C_d=0       \tag{6}
\]

for every coordinate off-diagonal row plane `R_c` and column plane
`C_d`.  Equivalently, `D^perp` is a two-plane whose restriction to each
of those six coordinate planes is an isomorphism.

We use twice the following consequences.

**Lemma 2.1 (two-regularity).**  For every nonzero `b,a in C^3`,

\[
 \dim\mathscr D b\ge2,
 \qquad \dim\mathscr D^{\mathsf T}a\ge2.               \tag{7}
\]

**Proof.**  If `dim D b<=1`, its left annihilator has dimension at least
two.  For every annihilating row `a`, deletion of the diagonal of
`ab^T` belongs to `D^perp`.  If `b` has at least two nonzero coordinates,
this map is injective and one may choose `a` with a prescribed zero
coordinate, producing a member of `D^perp` with an empty row.  If `b` is
supported at one coordinate, all these matrices are supported in one
column, and the same row-column restriction isomorphism is contradicted.
Transpose the argument for the second assertion. `QED`

**Lemma 2.2 (no rank-one relation).**  The space `D` contains no nonzero
rank-one matrix.

**Proof.**  Write such a matrix as `xy^T`.  Its zero diagonal says
`x_cy_c=0` for all three `c`, so the supports of `x` and `y` are disjoint.
One of those two nonempty supports is a singleton.  The matrix is
therefore contained in one coordinate row plane or one coordinate column
plane, contrary to (6). `QED`

We also need an invertible relation.

**Lemma 2.3 (an invertible member).**  The space `D` contains an
invertible matrix.

**Proof.**  A four-dimensional complex space of `3 by 3` matrices which
contains no invertible matrix contains a nonzero matrix of rank at most
one.  Here is a short standard proof of the only nontrivial case.  If all
nonzero matrices had constant rank two, the universal matrix on
`P(D)=P^3` would give a constant-rank bundle map

\[
                    {\cal O}(-1)^3\longrightarrow{\cal O}^3.
\]

Its kernel and cokernel would be line bundles, say `O(k)` and `O(l)`.
The Chern identity would be

\[
             1+kH=(1-H)^3(1+lH).
\]

The `H^2` coefficient gives `l=1`, while the `H^3` coefficient is then
`2`, a contradiction on `P^3`.  Lemma 2.2 now finishes the proof. `QED`

## 3. Ordinary lifts and the intrinsic kernel

Regard `P,S:C^3 -> R_1` as the injective column maps when both star
spans have dimension three.  Before same-site terms are discarded, (5)
lifts to

\[
 \widetilde T(M)=PMS^{\mathsf T}+SM^{\mathsf T}P^{\mathsf T}
                 \in\operatorname {Sym}^2(P+S).         \tag{8}
\]

For `M in D`, (8) is block diagonal by sites:

\[
                  \widetilde T(M)\in\bigoplus_i\operatorname {Sym}^2V_i.
                                                               \tag{9}
\]

The ordinary symmetrization kernel is canonical:

\[
 \ker\widetilde T\simeq\Lambda^2(P\cap S),
 \qquad \dim\ker\widetilde T={k\choose2}.              \tag{10}
\]

Indeed, the kernel of `P tensor S -> Sym^2(P+S)` consists exactly of the
alternating tensors whose two legs lie in the intersection.

Let `K=ker T` in all of `Mat_3`.  Since `D subset K`, (10) immediately
gives

\[
 \dim K\ge4+{k\choose2}
              -\dim(\mathscr D\cap\ker\widetilde T).   \tag{11}
\]

Thus (4) already follows whenever the right side is at least five.  For
`k=2,3`, the only remaining chart has

\[
                         \ker\widetilde T\subseteq\mathscr D.        \tag{12}
\]

## 4. Rank-deficient star spans

Suppose `dim P=2`.  Pairwise independence says that, for each `d`, the
two vectors `{p_c:c!=d}` are a basis of `P`.  The corresponding column
pair of products is a basis of `W`, hence

\[
                         s_dP=W.                         \tag{13}
\]

Since `p_d in P`, this puts `p_ds_d` in `W`.  The argument with the two
stars interchanged handles `dim S=2`.  Dimension one is already excluded
by pairwise independence.

## 5. Disjoint three-planes are impossible

Assume `k=0`.  Choose the invertible `M_0 in D` supplied by Lemma 2.3.
Then \(B_0=\widetilde T(M_0)\) is a nondegenerate symmetric form on the
six-space \(U=P\oplus S\).  Because it is block diagonal by sites,

\[
                         U=\bigoplus_iU_i,
 \qquad U_i\subseteq V_i,                               \tag{14}
\]

is a `B_0`-orthogonal decomposition.  Every operator

\[
                         A_M=B_0^{-1}\widetilde T(M),
                         \qquad M\in\mathscr D,          \tag{15}
\]

preserves every `U_i`.

After harmless changes of basis on the two three-spaces, (15) is the
direct sum of the two families

\[
 C=M_0^{-1}M,
 \qquad C^{\mathsf T}.                                  \tag{16}
\]

The family in (16) is irreducible on `C^3`.  A common invariant line
would give `dim D b<=1`; a common invariant plane, after taking its
annihilator, would give `dim D^T a<=1`.  Both contradict Lemma 2.1.

The projection of any common invariant subspace of (16) to either
three-dimensional summand is again invariant.  Hence every nonzero `U_i`
has dimension at least three.  The support hypothesis supplies at least
three nonzero `U_i`, whereas their direct sum has dimension six.  This is
impossible.

## 6. A one-dimensional intersection is impossible

Assume `k=1`.  Choose bases in the two star spaces in which their common
line is represented by the first vector.  If `M=(m_ab)`, the matrix of
`widetilde T(M)` on a basis of the five-space `U=P+S` is

\[
 \begin{pmatrix}
 2m_{00}&m_{10}&m_{20}&m_{01}&m_{02}\\
 m_{10}&0&0&m_{11}&m_{12}\\
 m_{20}&0&0&m_{21}&m_{22}\\
 m_{01}&m_{11}&m_{21}&0&0\\
 m_{02}&m_{12}&m_{22}&0&0
 \end{pmatrix}.                                         \tag{17}
\]

Its determinant is

\[
                  2\det M\cdot
                    \det\begin{pmatrix}m_{11}&m_{12}\\m_{21}&m_{22}
                         \end{pmatrix}.                  \tag{18}
\]

The first factor is not identically zero on `D` by Lemma 2.3.  The
second is not identically zero either.  Otherwise the indicated `2 by 2`
compression of `D` would be a singular matrix space.  Such a subspace of
`Mat_2` has a common kernel or a common cokernel.  Lifting it would give
`dim D b<=1` or `dim D^T a<=1`, contrary to Lemma 2.1.  Over the infinite
field `C`, the product in (18) is therefore nonzero at some `M_0 in D`.

Use this nondegenerate `B_0` exactly as in (14)--(15).  The support
hypothesis again gives at least three nonzero invariant site summands.
Their dimensions add to five, so one of them is a common invariant line
`C y`.

Put `x=B_0^{-1}y`.  Pull `x` back to a pair `(a,b)` on the two abstract
three-spaces.  Invariance of `C y` says

\[
  \dim\operatorname {span}_{M\in\mathscr D}
       \bigl(P(Mb)+S(M^{\mathsf T}a)\bigr)\le1.          \tag{19}
\]

Neither `a` nor `b` is zero, by Lemma 2.1.  The kernel of
\(P\oplus S\longrightarrow U\) is the one-dimensional anti-diagonal copy
of \(P\cap S\).  Hence the map

\[
             \mathscr D\longrightarrow\mathbb C^3\oplus\mathbb C^3,
             \qquad M\longmapsto(Mb,M^{\mathsf T}a)     \tag{20}
\]

has rank at most two.  Its kernel has dimension at least two and consists
of matrices satisfying

\[
                             Mb=0,
 \qquad                       M^{\mathsf T}a=0.          \tag{21}
\]

After quotienting the right by `C b` and restricting the left to
`ker a`, (21) is a two-dimensional pencil of `2 by 2` matrices.  A binary
homogeneous determinant has a projective zero over `C`; the pencil
therefore contains a nonzero matrix of rank at most one.  This contradicts
Lemma 2.2.

## 7. Coincident three-planes

Assume `k=3`.  If the three-dimensional intrinsic kernel in (10) is not
contained in `D`, (11) gives `dim K>=5` and hence `rank T<=4`, proving
(4).

It remains to treat (12).  Write `S=PC` for an invertible transition
matrix `C`.  The ordinary kernel is

\[
            \{A C^{-\mathsf T}:A^{\mathsf T}=-A\}.      \tag{22}
\]

For every matrix in (22) to have zero diagonal, each column of
`C^{-T}` must be supported on its matching coordinate.  Thus `C` is
diagonal.  After rescaling colours, the six off-diagonal products reduce
to the three products

\[
                         p_0p_1,\quad p_0p_2,\quad p_1p_2.           \tag{23}
\]

They span `W`, and every pair is a basis.  Their unique relation therefore
has all three coefficients nonzero.  It is represented by an invertible
symmetric zero-diagonal matrix `H`, and (9) says

\[
                         P_i H P_j^{\mathsf T}=0
                         \qquad(i\ne j).                \tag{24}
\]

Let \(L_i=\operatorname {im}P_i^{\mathsf T}\subset\mathbb C^3\).
These site row spaces span \(\mathbb C^3\) and
are pairwise `H`-orthogonal.  The elementary three-dimensional
classification gives

\[
                \operatorname {rank}
                  \bigl(\operatorname {Sym}^2P\longrightarrow{\cal R}_2\bigr)
                  \le3.                                 \tag{25}
\]

For completeness: a rank-three `L_i` kills all other spaces; a rank-two
`L_i` puts every other `L_j` in its one-dimensional orthogonal and leaves
only the two cross directions plus their common line-square; if all
`L_i` are lines, nonisotropic lines occur in at most three mutually
orthogonal types, while repetitions can occur only on one isotropic line
and then there is at most one transverse type.  In each case the cross-site
quadratic coefficients have dimension at most three.  This proves the
stronger bound in the aligned `k=3` chart.

## 8. Exact form of the residual two-plane chart

Assume now `k=2` and (12).  The intrinsic kernel is a rank-two matrix

\[
                         0\ne N\in\mathscr D\cap Z_0.   \tag{26}
\]

Choose a complement `t notin P` and write

\[
                         S=PA+t v^{\mathsf T}.           \tag{27}

\]

When `A` is invertible, put `u=A^{-T}v`.  The ordinary kernel is generated
by

\[
                         N=[u]_\times A^{-T}.            \tag{28}

\]

The zero-diagonal condition has a useful exact solution.  Every column of
`A^{-T}` lies in the plane spanned by its matching coordinate vector and
`u`; hence

\[
                         A^{-T}=D+u r^{\mathsf T}        \tag{29}
\]

for a diagonal `D`.  If `D` is invertible, changing the complement `t`
and rescaling the three colours puts (27) into

\[
                         \boxed{\ s_c=p_c+v_c t\ },      \tag{30}

\]

with all `v_c` nonzero on the full-support chart.  The reverse products
satisfy

\[
 p_cs_d-p_ds_c=t(v_dp_c-v_cp_d),                        \tag{31}

\]

so their differences lie in `tH`, where

\[
                         H=\{\textstyle\sum a_cp_c:\sum v_ca_c=0\}.
                                                               \tag{32}
\]

Equations (26)--(32), together with the cases in which one diagonal entry
of `D` vanishes, are the sole residual all-dead product geometry.

## 9. Exact reconnaissance

[`search_all_dead_product_geometry.py`](../computations/search_all_dead_product_geometry.py)
checks three useful boundaries exactly.  It verifies the rational
three-site symmetric model, exhausts all full-rank four-scalar-site
models over `F_3`, and exhausts all 63,180 decompositions of type
`2+1+1` in the normalized aligned two-plane four-space over `F_3`.
There are 30 decompositions whose lifted off-diagonal five-space has a
block-diagonal intersection of dimension at least three; every one makes
one of the six named star vectors miss a summand.  The script is
reconnaissance, not a characteristic-zero proof of the residual lemma.

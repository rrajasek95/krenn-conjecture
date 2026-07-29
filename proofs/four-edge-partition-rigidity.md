# Four-edge partition rigidity on the residual rank-one chart

This note classifies the two four-edge decompositions left by the
color-sensitive deletion search on the canonical all-rank-one six-vertex
support chart.  The argument concerns the transformed matrices

\[
 B_{uv}^{(\alpha)}(a,b)
   =(\alpha_{u,a}+\alpha_{v,b})A_{uv}(a,b),                 \tag{1}
\]

not the original rank-one matrices `A_uv`.  A transformed matrix can have
rank two, but the additive multiplier in (1) makes its relevant local image
plane explicit.

## 1. A `2+2` slice-span classification

Let `X,Y,Z` be vector spaces containing independent triples
`e_0^X,e_1^X,e_2^X`, and similarly in `Y,Z`, and let

\[
 D=\sum_{r=0}^2g_r e_r^X\otimes e_r^Y\otimes e_r^Z,
 \qquad g_0g_1g_2\ne0.                                     \tag{2}
\]

Suppose

\[
 D=x_1\otimes P_1+x_2\otimes P_2
        +y_1\otimes Q_1+y_2\otimes Q_2,                    \tag{3}
\]

where `x_i in X`, `P_i in Y tensor Z`, `y_i in Y`, and
`Q_i in X tensor Z`.  Zero summands may be omitted.  Put

\[
 U=\operatorname{span}\{x_i:P_i\ne0\},\qquad
 V=\operatorname{span}\{y_i:Q_i\ne0\}.                    \tag{4}
\]

**Lemma 1.1 (`2+2` axis cover).**  Every coordinate color is covered by
one of the two center spans:

\[
 e_r^X\in U\quad\hbox{or}\quad e_r^Y\in V
 \qquad(r=0,1,2).                                          \tag{5}
\]

Consequently, if all four terms are nonzero and `dim U=dim V=2`, at least
one of `U,V` is a coordinate plane.  More generally, (5) is the complete
subspace obstruction even when a summand vanishes.

**Proof.**  Apply the quotient map

\[
 (X\longrightarrow X/U)\otimes(Y\longrightarrow Y/V)
                                      \otimes\operatorname{id}_Z
\]

to (3).  Every term on the right vanishes.  Therefore

\[
 \sum_{r=0}^2g_r\bar e_r^X\otimes\bar e_r^Y\otimes e_r^Z=0.
\]

Independence of the three `e_r^Z` and nonvanishing of the `g_r` give
`bar e_r^X tensor bar e_r^Y=0` separately for every `r`.  A pure tensor
over a field is zero only if one factor is zero, proving (5).  Since
`dim U,dim V<=2`, the pigeonhole principle puts two of the three coordinate
axes in one span; a two-dimensional space containing two coordinate axes is
their coordinate plane. `QED`

There is a complementary statement when two slices have one center and the
other two have separate centers.

**Lemma 1.2 (`2+1+1` contraction).**  Suppose

\[
 D=x_1\otimes P_1+x_2\otimes P_2+y\otimes Q+z\otimes R,    \tag{6}
\]

with the first two slices centered in `X`, the third in `Y`, and the fourth
in `Z`.  Assume `U=span{x_1,x_2}` has dimension two, and let
`0 != ell in X^*` annihilate `U`.  Set

\[
 I=\{r:\ell(e_r^X)\ne0\}.
\]

Then `|I|<=2`.  If `|I|=2`, then

\[
 y\in\operatorname{span}\{e_r^Y:r\in I\},\qquad
 z\in\operatorname{span}\{e_r^Z:r\in I\}.                 \tag{7}
\]

**Proof.**  Contract (6) in `X` by `ell`.  The first two terms vanish and
the remaining matrix in `Y tensor Z` is

\[
 \sum_r g_r\ell(e_r^X)e_r^Y\otimes e_r^Z
      =y\otimes q+p\otimes z.                              \tag{8}
\]

The left side has matrix rank `|I|`, while the right side has rank at most
two.  If `|I|=2`, both rank-one terms on the right are necessarily retained,
and their two left factors span the column space
`span{e_r^Y:r in I}`; similarly their right factors span the corresponding
row space.  This gives (7). `QED`

We will also use the three-slice center lemma from
`proofs/exceptional-triangle-obstruction.md`: a three-way diagonal tensor
with three nonzero coefficients written as one nonzero slice centered at
each of its three modes has three distinct coordinate singleton factors.

## 2. Canonical all-rank-one support chart

The residual support chart has six full-factor rank-one edges

\[
 \mathcal C=\{03,05,14,15,23,24\},                          \tag{9}
\]

and the other nine edges are the following basis cells:

\[
\begin{array}{c|ccccccccc}
uv&01&02&04&12&13&25&34&35&45\\ \hline
(\text{color at }u,\text{color at }v)
  &(2,1)&(0,0)&(0,2)&(1,1)&(1,0)&(0,2)&(2,0)&(2,2)&(1,1).
\end{array}                                                 \tag{10}
\]

On an edge in `C`, write the original matrix as

\[
 A_{uv}=a_{uv}^{(u)}\otimes a_{uv}^{(v)},                  \tag{11}
\]

where every coordinate of both factors is nonzero.  Multiplication on the
left and right by the corresponding invertible diagonal factor matrices
does not change ranks, coordinate supports, or whether an individual
line/plane is coordinate.  The diagonal matrices can differ from edge to
edge, so spans involving two edges will be handled explicitly below.  The
individual properties of `B_uv` can be read directly from its additive mask

\[
 M_{uv}(a,b)=\alpha_{u,a}+\alpha_{v,b},\qquad
 B_{uv}=\operatorname{diag}(a_{uv}^{(u)})M_{uv}
          \operatorname{diag}(a_{uv}^{(v)}).                \tag{12}
\]

## 3. The four-edge path witness

Take

\[
 S_1=\{03,05,14,15\}                                       \tag{13}
\]

and the exact stabilizer point (the generic family parameter specialized
to `t=2`)

\[
\begin{array}{c|cccccc}
v&0&1&2&3&4&5\\ \hline
\alpha_v&(0,1,0)&(-1,0,1)&(0,0,0)&(0,0,0)&(0,0,0)&(2,0,0).
\end{array}                                                 \tag{14}
\]

It obeys `sum_v alpha_(v,r)=1` for every color and kills every edge outside
`S_1` on the support (10).  Before the edge-dependent diagonal rescalings
coming from (11), its column spaces at vertices `0` and `1` are

\[
\begin{aligned}
 \operatorname{col}_0 M_{03}&=\mathbb C e_1,\\
 \operatorname{col}_0 M_{05}
   &=P_0:=\operatorname{span}\{e_1,(2,3,2)\},\\
 \operatorname{col}_1 M_{14}&=\mathbb C(-1,0,1),\\
 \operatorname{col}_1 M_{15}
   &=P_1:=\operatorname{span}\{(-1,0,1),(1,2,3)\}.          \tag{15}
\end{aligned}
\]

The plane `P_0` has normal `(1,0,-1)` and contains exactly one coordinate
axis, `C e_1`.  The plane `P_1` has normal proportional to `(-1,2,-1)` and
contains no coordinate axis.  In particular neither is a coordinate plane.
After the possibly different diagonal rescalings, denote the actual four
spaces by

\[
 L_{03}=\mathbb C e_1,\qquad P_{05},\qquad L_{14},\qquad P_{15}. \tag{16}
\]

Here `P_05` is a noncoordinate plane containing exactly `C e_1` among the
coordinate axes; `L_14` is a noncoordinate line supported on coordinates
`0,2`; and `P_15` is a noncoordinate plane containing no coordinate axis.

**Proposition 3.1.**  No tensors `C_e` on the complementary four vertices
can satisfy

\[
 \Delta_{6,3}=\sum_{e\in S_1}B_e^{(\alpha)}\otimes C_e.     \tag{17}
\]

**Proof.**  Contract vertices `3,4,5` by generic covectors, each nonzero on
all three coordinate basis vectors.  On vertices `0,1,2`, the target is a
diagonal tensor of the form (2).  The terms on `03,05` become slices
centered at vertex `0`, while those on `14,15` become slices centered at
vertex `1`.  The covectors can also be chosen so that every globally
nonzero summand of (17) remains nonzero after contraction.

Let `U,V` be the spans of the retained singleton factors at vertices `0,1`.
If all four summands are nonzero, choose the covector at vertex `5`
generically.  Then

\[
 U=P_{05},\qquad
 V=\operatorname{span}\{L_{14},x_{15}\},\qquad
 x_{15}\in P_{15},                                        \tag{18}
\]

and `x_15` can additionally be chosen with full coordinate support.  Since
`P_05` contains only the coordinate axis `C e_1`, condition (5) says `V`
must contain both `e_0` and `e_2`, hence must equal the coordinate plane
`span{e_0,e_2}`.  But the full-support vector `x_15` does not lie in that
plane, a contradiction.

The possible zero-summand degeneracies do not escape the argument.  At
least three summands must be nonzero, because `Delta_(6,3)` has partition
rank three.  If exactly one is omitted, the corresponding possibilities
for `(U,V)` are

\[
\begin{array}{c|c|c}
\text{omitted edge}&U&V\\ \hline
03&\mathbb Cx_{05}\ (x_{05}\text{ full-support})
   &\operatorname{span}\{L_{14},x_{15}\}\\
05&\mathbb C e_1&\operatorname{span}\{L_{14},x_{15}\}\\
14&P_{05}&\mathbb Cx_{15}\ (x_{15}\text{ full-support})\\
15&P_{05}&L_{14}.
\end{array}                                                 \tag{19}
\]

In the first row `U` contains no coordinate axis, so the at-most-two
dimensional `V` cannot contain all three.  In the second row (5) again
forces `V=span{e_0,e_2}`, contradicted by the full-support `x_15`.  In the
third row `U` contains only `e_1` while the line `V` contains no coordinate
axis.  The fourth row has the same property because `L_14` is
noncoordinate.  Thus (5) fails in every case, and (17) is impossible.
`QED`

The transformed ranks in this witness are `(1,2,1,2)` in the order
`03,05,14,15`, but Proposition 3.1 uses the stronger and stable local-plane
information rather than ranks alone.

## 4. The two-path witness

Now take

\[
 S_2=\{03,14,15,23\}                                       \tag{20}
\]

and

\[
\begin{array}{c|cccccc}
v&0&1&2&3&4&5\\ \hline
\alpha_v&(0,0,0)&(1,0,1)&(0,0,0)&(0,1,0)&(0,0,0)&(0,0,0).
\end{array}                                                 \tag{21}
\]

Again the color sums are one and all other supported edges are killed.  All
four masks have rank one.  On `03` and `23` the factor at vertex `3` is the
same coordinate line `C e_1`.  On `14` and `15` the factors at vertices
`4` and `5` are the original full-support factors from (11), hence are
noncoordinate lines.

**Proposition 4.1.**  No tensors `C_e` can satisfy

\[
 \Delta_{6,3}=\sum_{e\in S_2}B_e^{(\alpha)}\otimes C_e.     \tag{22}
\]

**Proof.**  Contract vertices `0,1,2` generically.  The two terms on
`03,23` become slices centered at vertex `3` with the same singleton factor
`e_1`; merge them into one slice.  The terms on `14,15` become slices
centered at vertices `4,5`, with fixed full-support singleton factors
`a_{14}^{(4)}` and `a_{15}^{(5)}`.

If all four original summands are nonzero, their merged vertex-`3` slice
cannot vanish: otherwise the contracted diagonal tensor would be a sum of
only two slices.  The three-slice center lemma therefore applies and says

\[
 e_1,\quad a_{14}^{(4)},\quad a_{15}^{(5)}
\]

are three distinct coordinate lines.  The latter two lines have full
coordinate support, a contradiction.

Degeneracies are again harmless.  If one of the `14,15` summands vanishes,
merging leaves at most two slices.  If one of `03,23` vanishes, the other
one still supplies the `e_1`-centered slice and the same three-slice-center
contradiction applies.  Fewer than three globally nonzero summands are
excluded by partition rank.  Thus (22) is impossible. `QED`

## 5. The three triangle-plus-leaf witnesses

The remaining three witnesses of degree sequence `(3,2,2,1)` have the
following exact stabilizers.  The ordered triple `(X,Y,Z)` gives the three
vertices retained after contraction.  The two edges in the fourth column
become the two `X`-centered slices; the edge in the fifth column becomes the
`Y`-centered slice, and the remaining edge becomes the `Z`-centered slice.

\[
\begin{array}{c|c|c|c|c}
S& (\alpha_0,\ldots,\alpha_5)&(X,Y,Z)&X\text{-edges}&Y\text{-edge}\\ \hline
\{01,03,05,15\}
 &(011,000,000,000,000,100)&(0,1,2)&03,05&15\\
\{05,14,15,45\}
 &(000,\bar101,000,000,000,210)&(5,4,2)&05,15&14\\
\{14,15,24,45\}
 &(000,101,000,000,010,000)&(4,5,0)&24,14&15.
\end{array}                                                  \tag{23}
\]

Here `011` means `(0,1,1)`, `bar101` means `(-1,0,1)`, and so on.  In each
row the two `X`-matrices have ranks one and two.  The rank-one local line is
respectively supported on colors `12`, supported on colors `01`, and equal
to the coordinate line `C e_1`.  A generic local vector from the rank-two
matrix has full coordinate support.  The factor of the `Y`-matrix at `Y`
is also full-support.

**Proposition 5.1.**  None of the three rows of (23) can give a four-term
decomposition of `Delta_(6,3)`.

**Proof.**  Contract the three vertices outside `(X,Y,Z)` generically.  Let
`L` be the rank-one local line at `X` and let `x` be the singleton obtained
from the rank-two matrix.  We may choose `x` with full support and outside
`L`, so `U=span{L,x}` is a plane.  It is not a coordinate plane: in the
first two rows the only coordinate plane that could contain the
two-coordinate-support line `L` does not contain `x`; in the last row no
coordinate plane containing `e_1` contains a full-support `x`.

Let `ell` annihilate `U`.  Lemma 1.2 says its coordinate support has size
at most two.  It cannot have size one, since that would make `U` a
coordinate plane.  Thus it has size two, and (7) says that the singleton
factor `y` at `Y` lies in the corresponding coordinate plane.  This
contradicts the full support of `y`.

If one of the two `X`-summands is globally zero, the three remaining slices
have one center each, and the three-slice center lemma contradicts the full
support of `y`.  If the `Y`-summand is zero, Lemma 1.1 applied to the
`X,Z` centers would have to cover three coordinate axes by a noncoordinate
plane and one line, impossible.  If the `Z`-summand is zero, the same axis
cover uses `U` and the full-support line `C y`, and again fails.  Two or
fewer summands contradict partition rank three. `QED`

## 6. The three-star-with-leaf witness

The last survivor set is

\[
 S_3=\{03,13,23,24\},\qquad
 (\alpha_0,\ldots,\alpha_5)=(000,000,001,110,000,000).       \tag{24}
\]

Retain vertices `(0,3,4)`.  The edges `13,23` become slices centered at
vertex `3`; their local factors are `e_0` and a generic full-support vector
`x_23` from a rank-two image plane.  Hence their span `U` is a
noncoordinate plane containing exactly the axis `C e_0`.  The edges
`03,24` become slices centered at vertex `4`; the `24` singleton factor at
vertex `4` is full-support.

**Proposition 6.1.**  This witness cannot decompose `Delta_(6,3)`.

**Proof.**  Lemma 1.1 says each coordinate axis lies in the vertex-`3` span
`U` or in the at-most-two-dimensional vertex-`4` span `V`.  Since `U`
contains only `C e_0`, the space `V` must contain `e_1,e_2` and hence equal
their coordinate plane.  This is impossible because `V` contains the
full-support singleton supplied by edge `24`.

If one summand vanishes, the same axis-cover argument is even sharper.
Omitting `13` leaves a full-support line at vertex `3`, so the other
two-dimensional center cannot cover all three axes.  Omitting `23` leaves
only `C e_0` there and still forces the full-support `24` factor into the
`e_1,e_2` plane.  Omitting `03` leaves a full-support line at vertex `4`,
and omitting `24` leaves only one arbitrary line there; neither can cover
the two axes missing from `U`.  Fewer summands are excluded by partition
rank. `QED`

## 7. Consequence for the residual chart

Exact rational enumeration finds no deletion leaving at most three edges
and exactly the following six deletion sets leaving four:

\[
\begin{gathered}
\{01,03,05,15\},\quad \{03,05,14,15\},\quad
\{03,13,23,24\},\\
\{03,14,15,23\},\quad \{05,14,15,45\},\quad
\{14,15,24,45\}.
\end{gathered}                                               \tag{25}
\]

Propositions 3.1, 4.1, 5.1, and 6.1 exclude all six.  Thus the canonical
`F=empty` residual support chart is impossible.

The finite support enumeration, stabilizer equations, mask ranks, and local
axis claims are independently checked over the rationals by

```sh
.venv/bin/python computations/verify_four_edge_partition_witnesses.py
```

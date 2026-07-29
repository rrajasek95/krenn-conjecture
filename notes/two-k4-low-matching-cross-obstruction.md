# Two `K_4` equality shores need a four-edge cross matching

## 1. Outcome

Let

\[
 L=\{L_*,L_0,L_1,L_2\},\qquad
 R=\{R_*,R_0,R_1,R_2\},                                \tag{1}
\]

and put the unit ternary equality realization on each shore.  Thus the
colour-`r` one-factor is

\[
 L_*L_r\mid L_iL_j,\qquad \{i,j\}=\{0,1,2\}\setminus\{r\},        \tag{2}
\]

and similarly on `R`; every displayed edge carries `E_(rr)`.  Add
arbitrary complex `3 by 3` matrices on a bipartite cross graph `G` between
the shores.

**Theorem 1.1.**  If the matching number of `G` is at most three, the
resulting eight-site matching tensor is not `Delta_(8,3)`.

The adjacent matching-number-four stratum in which `G` has a unique perfect
matching is excluded in
[`two-k4-unique-perfect-matching-cross-obstruction.md`](two-k4-unique-perfect-matching-cross-obstruction.md).

In particular this excludes the proposed six-edge two-star chart

\[
 G_\star=\{L_*R_s:s=0,1,2\}
       \mathbin\cup\{L_rR_*:r=0,1,2\}.                  \tag{3}
\]

The two-star contradiction is especially short: a mixed word has at most
one two-cross matching, so an off-diagonal correction forces a star matrix
to be supported on one matrix unit.  The two required off-diagonal colours
then force the same matrix onto two different units.

The extension to every `nu(G)<=3` has only two Hall-maximal cases.  The
degree pattern `(1,1,4,4)` has a ten-coefficient polynomial certificate.
The other case is `K_(3,4)`.  Expanding at its isolated vertex turns the
three colours into three overlapping `K_(2,4)` pure-output identities.
Each such identity has a rigid two-edge-star normal form, and two different
normal forms necessarily create a uniquely supported mixed coefficient.

No rank assumption, genericity, positivity, reality, or coordinate support
condition is imposed on a cross matrix.  Parallel sources may be aggregated
into the matrices used here.  The obstruction is over every field of
characteristic zero.

## 2. The two-cross correction equation

Write

\[
 X_r^L=\bigotimes_{u\in L}e_r^{(u)},\qquad
 X_s^R=\bigotimes_{v\in R}e_s^{(v)}.                    \tag{4}
\]

With no cross edge, the two shores contribute

\[
                         \sum_{r,s=0}^2X_r^LX_s^R.       \tag{5}
\]

A perfect matching crosses an even number of times.  If `nu(G)<=3`, four
crossings are impossible, so every matching uses zero or two cross edges.
Consequently an exact realization would require its entire two-cross
sector to equal

\[
             T_2=-\sum_{r\ne s}X_r^LX_s^R.              \tag{6}
\]

Thus the six off-diagonal block-constant coefficients are `-1`, while all
three diagonal block-constant coefficients and every mixed coefficient of
`T_2` are zero.  All arguments below concern the actual coefficient tensor
in (6), not only its physical support.

## 3. The two-star chart dies one coefficient at a time

Put

\[
                    U_s=A_{L_*R_s},\qquad
                    V_r=A_{L_rR_*}.                       \tag{7}
\]

Every two-cross matching in (3) has, for unique `r,s`, the form

\[
 L_*R_s\mid L_rR_*\mid
 L_iL_j\mid R_kR_l,                                     \tag{8}
\]

where `{i,j}=C\setminus{r}` and `{k,l}=C\setminus{s}`.
The last two edges have colours `r` and `s`.  Hence the coefficient of the
block-constant word `X_r^LX_s^R` in (8) is

\[
                         U_s(r,s)V_r(r,s).                \tag{9}
\]

No colouring is produced by two different matchings (8).  Indeed, its two
uncrossed left leaves determine `r`: they both have colour `r`.  Two
different choices of `r` would force the third leaf to have two different
colours.  The same argument determines `s` on the right.

Fix `r!=s`.  Equation (6) gives

\[
                         U_s(r,s)V_r(r,s)=-1.             \tag{10}
\]

In particular both factors are nonzero.  Replace the `(r,s)` cell used on
`U_s` in (8) by any other cell `(a,b)`.  The resulting word is mixed, its
matching is still unique, and (6) therefore says

\[
                         U_s(a,b)V_r(r,s)=0.              \tag{11}
\]

It follows that

\[
                              U_s\in\mathbb C^*E_{rs}.    \tag{12}
\]

The same variation on `V_r` gives `V_r in C^*E_(rs)`.  For a fixed `s`
there are two choices `r!=s`; (12) would put the same nonzero matrix `U_s`
on two distinct matrix-unit lines.  This is impossible.  Thus the six
off-diagonal terms and the mixed zero terms already exclude the chart;
the three diagonal equations are not needed.

## 4. Only two maximal low-matching graphs

Let `G subseteq K_(4,4)` have no four-edge matching.  Hall's theorem gives
a nonempty left set `S` with

\[
                         |N(S)|<|S|.                      \tag{13}
\]

Put `k=|S|`, enlarge `N(S)` to a set `T` of size `k-1`, and enlarge `G`
to

\[
 G(S,T)=\bigl(S\mathbin\times T\bigr)
       \mathbin\cup\bigl((L\setminus S)\mathbin\times R\bigr).   \tag{14}
\]

Setting the added cross matrices to zero recovers `G`, so it suffices to
exclude (14).  For `k=1,4`, graph (14), up to transposition, is `K_(3,4)`.
For `k=2,3`, again up to transposition, its left degrees are

\[
                              (1,1,4,4).                  \tag{15}
\]

The colour-preserving Klein-four automorphisms of the standard `K_4`
factorization are transitive on vertices.  Together with a global colour
permutation, they put the two cases into the canonical charts below.

## 5. The `(1,1,4,4)` chart: a polynomial certificate

Use local vertex order

\[
 (L_*,L_0,L_1,L_2\mid R_*,R_0,R_1,R_2)                  \tag{16}
\]

and retain the cross edges

\[
 L_*R_*,\quad L_0R_*,\quad
 \{L_1,L_2\}\mathbin\times\{R_*,R_0,R_1,R_2\}.         \tag{17}
\]

Write `x_(uv)^(ab)` for the `(a,b)` cell on a cross edge.  Define

\[
\begin{array}{llll}
 u=x_{L_*R_*}^{10},&v=x_{L_0R_*}^{10},
 &p=x_{L_1R_0}^{10},&q=x_{L_2R_0}^{10},\\[2mm]
 k_0=x_{L_2R_1}^{01},&h_0=x_{L_1R_*}^{01},
 &k_1=x_{L_1R_2}^{01},&h_1=x_{L_2R_0}^{01},\\
 k_2=x_{L_1R_1}^{01},&h_2=x_{L_2R_*}^{01},
 &k_3=x_{L_1R_0}^{01},&h_3=x_{L_2R_2}^{01}.
\end{array}                                               \tag{18}
\]

There are only two two-cross matchings at the block word
`1111|0000`, and four at `0000|1111`.  Equation (6) gives

\[
                 I:=up+vq=-1,
       \qquad    A:=\sum_{i=0}^3k_ih_i=-1.               \tag{19}
\]

The following eight mixed words each have exactly the one displayed
two-cross matching:

\[
\begin{array}{c|c@{\qquad}c|c}
1110|0111&vk_0&1220|0111&uk_0\\
2102|0221&vk_1&1101|0221&uk_1\\
2102|0111&vk_2&1101|0111&uk_2\\
2102|0100&vk_3&1101|0100&uk_3.
\end{array}                                               \tag{20}
\]

They must vanish, so

\[
                         uk_i=vk_i=0\qquad(0\le i\le3).  \tag{21}
\]

Multiplying the two required coefficients in (19) and using (21) gives

\[
 AI=(up+vq)\sum_i k_ih_i
   =\sum_i ph_i(uk_i)+\sum_i qh_i(vk_i)=0,               \tag{22}
\]

whereas (19) gives `AI=1`.  This is the promised ten-coefficient exact
contradiction.  Equivalently, a literal Nullstellensatz certificate is

\[
 1=\sum_i ph_i(uk_i)+\sum_i qh_i(vk_i)-A(I+1)+(A+1).     \tag{23}
\]

## 6. One isolated anchor forces three pure six-site identities

It remains to exclude the canonical `K_(3,4)` graph

\[
              G=\{L_0,L_1,L_2\}\mathbin\times R,        \tag{24}
\]

with `L_*` cross-isolated.  Expanding a hypothetical equality at `L_*`,
the `e_r` coordinate can only use the internal edge `L_*L_r`.  Deleting
these two vertices shows that, for every `r`, the graph on the other two
left leaves and all four right vertices has matching tensor

\[
                              e_r^{\otimes6}.             \tag{25}
\]

The edge between the two remaining left leaves is `E_(rr)`, all eight
cross matrices are arbitrary, and the right shore still carries its unit
`K_4` equality block.

Fix `r` and call the remaining left vertices `a,b`.  For each right vertex
`v`, take the `r`-th left row of its two cross matrices:

\[
 x_v=(A_{av})_{r,*}^{\mathsf T},\qquad
 y_v=(A_{bv})_{r,*}^{\mathsf T},\qquad
 Z_v=[x_v\ y_v]\in\mathbb C^{3\mathbin\times2}.         \tag{26}
\]

Let

\[
                         J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.  \tag{27}
\]

For a right edge `uv`, let `chi(uv)` be its factor colour.  The complementary
right edge has the same colour.  If `uv` supplies the two crossed endpoints,
their coefficient matrix is

\[
 M_{uv}=x_uy_v^{\mathsf T}+y_ux_v^{\mathsf T}
       =Z_uJZ_v^{\mathsf T}.                              \tag{28}
\]

A nonconstant right word satisfies at most one internal edge: two satisfied
edges sharing a vertex would demand two colours there, while two disjoint
satisfied edges are complementary, have the same factor colour, and make
the word constant.  Comparing (25) with the zero-cross contribution
`Delta_(4,3)` therefore yields scalars `lambda_uv` such that

\[
 M_{uv}=\lambda_{uv}E_{cc}\quad(c=\chi(uv)),              \tag{29}
\]

and, on the two edges `F_c` of each factor,

\[
 \sum_{uv\in F_c}\lambda_{uv}
 =\begin{cases}0,&c=r,\\-1,&c\ne r.\end{cases}          \tag{30}
\]

## 7. Classification of a pure `K_(2,4)` correction

**Lemma 7.1 (two-edge-star normal form).**  Let matrices `Z_v` obey
(29)--(30).  Write `{s,t}=C\setminus{r}`.  There is a unique right vertex
`w` of rank two.  If `u_c` denotes the neighbour of `w` on the colour-`c`
edge and `z=u_r`, then

\[
\begin{array}{c|cccc}
v&w&u_s&u_t&z\\ \hline
\operatorname {supp}(\text{either column of }Z_v)
 &\{s,t\}&\{s\}&\{t\}&\varnothing .
\end{array}                                               \tag{31}
\]

Every coordinate indicated in (31) is nonzero.

**Proof.**  If `Z_u,Z_v` both have rank two, the product in (28) has rank
two: `Z_v^T` is onto, `J` is invertible, and `Z_u` is injective.  Hence at
most one `Z_v` has rank two.

Suppose all four have rank at most one.  On a nonzero edge write
`Z_u=a_uh_u^T`.  Equation (29) forces the endpoint line `C a_u` to be the
coordinate line of that edge.  The three edges incident with `u` have
different colours, so `u` can lie on at most one nonzero-`lambda` edge.
The nonzero-`lambda` support is therefore a matching.  Two disjoint `K_4`
edges belong to the same factor, so at most one factor sum in (30) could be
nonzero, contrary to the two values `-1`.  Thus there is one rank-two
vertex `w`.

The required nonzero edges in colours `s` and `t` intersect, because
disjoint edges have the same colour.  Their intersection cannot be a
rank-one vertex, so it is `w`.  Every other vertex still has
nonzero-`lambda` degree at most one.  It follows from (30) that the only
nonzero coefficients are

\[
                      \lambda_{wu_s}=\lambda_{wu_t}=-1.  \tag{32}
\]

In particular `M_(wz)=0`; injectivity of `Z_wJ` gives `Z_z=0`.

Absorb scalars into two nonzero vectors `h_s,h_t in C^2` so that

\[
 Z_{u_s}=e_sh_s^{\mathsf T},\qquad
 Z_{u_t}=e_th_t^{\mathsf T}.                              \tag{33}
\]

Equations (28) and (32), together with `M_(u_su_t)=0`, become

\[
 Z_wJh_s=-e_s,qquad Z_wJh_t=-e_t,qquad
                         h_s^{\mathsf T}Jh_t=0.           \tag{34}
\]

The first two equations make `h_s,h_t` independent.  If
`h_s=(a,b)^T` and `h_t=(c,d)^T`, the last equation says

\[
                 ad+bc=0,\qquad ad-bc=-2bc\ne0.         \tag{35}
\]

Thus `a,b,c,d` are all nonzero.  Both columns in (33) have the stated
nonzero axial support.  Solving

\[
 Z_wJ[h_s\ h_t]=[-e_s\ -e_t]                             \tag{36}
\]

and using (35) shows that both columns of `Z_w` have nonzero `e_s` and
`e_t` coordinates and no `e_r` coordinate.  This is exactly (31). `QED`

## 8. Two normal forms cannot be mutually invisible

Denote the four-site support pattern (31), with target colour `r` and
centre `w`, by `S(r,w)`.  The following finite fact is the last input.

**Lemma 8.1 (unique mixed coefficient).**  Let `r!=t`.  If `x` has exact
sitewise support `S(r,w)` and `y` has exact sitewise support `S(t,w')`,
then their two-monomer response on the unit right `K_4` is nonzero.

More precisely, enumerate the six choices of crossed endpoint pair and its
two orientations.  The number of right words receiving exactly one
supported monomial is

\[
\begin{array}{c|c}
\text{relation between }w,w'&\text{unique words}\\ \hline
w=w'\text{, or }\chi(ww')=C\setminus\{r,t\}&9\\
\chi(ww')=r\text{ or }t&13.
\end{array}                                               \tag{37}
\]

This is a four-case enumeration: translate `w` to a fixed `K_4` vertex by
the colour-preserving Klein group, and `w'` is either that vertex or its
unique neighbour in one of the three colours.  In every case at least nine
words have a unique monomial.  Every factor in such a monomial is one of
the nonzero coordinates in (31), so its coefficient cannot vanish. `QED`

Return to the three identities (25).  Let `x_(r,i)` denote the column of
the colour-`r` normal form belonging to physical left vertex `L_i`; it is
defined whenever `i!=r`.  For distinct `r,t`, the two vectors

\[
                              x_{r,t},\qquad x_{t,r}       \tag{38}
\]

occur together after `L_*` is matched to the third leaf `L_k`.  Their left
endpoint colours are `r,t`, not the required pair `k,k`.  The internal
left edge also has colour `k`, so it contributes nothing to this mixed
coefficient.  Equation (25) therefore requires the two-monomer response
of (38) to be zero.  Lemma 8.1 says it is nonzero, a contradiction.

This excludes `K_(3,4)`.  Sections 4--5 then exclude every cross graph of
matching number at most three, completing Theorem 1.1.

## 9. Exact audit

[`verify_two_k4_low_matching_cross_obstruction.py`](../computations/verify_two_k4_low_matching_cross_obstruction.py)

* enumerates all `105` matchings and all `3^8` colourings;
* checks the two-star matching uniqueness and its forced matrix units;
* recovers the ten Ferrers coefficients and verifies certificate (23)
  symbolically;
* verifies the general symbolic normal form (33)--(36);
* audits all `48` cases of the exact-support table (37); and
* checks every one of the `2^16` physical cross graphs without a perfect
  matching is contained in one of the two Hall envelopes used above.

Running it produces

```text
Two-K4 low-matching cross obstruction: PASS
```

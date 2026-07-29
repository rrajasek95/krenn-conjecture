# Arbitrary-order pair-cut exchange is a flat reindexing

## 1. Outcome

There is a uniform closed formula for every iterated contraction of a
matching tensor.  Fix a set `S` of exposed physical sites.  The contraction
is a sum over partial matchings on `S`: a matched pair uses its direct
source cell, every unmatched exposed site uses one star into the common
complement, and the complement is finished by one divided matching power.
Every layer has coefficient one.

Consequently all mixed-contraction/Bianchi identities between complete
deleted-pair tensor systems are flat.  For two deleted pairs `P,P'` and
every `S` containing their union,

\[
 \iota_{S\setminus P}E^P=\iota_{S\setminus P'}E^{P'}.
\]

Both sides are the same `S`-site coefficient of the original top residual.
If the pairs overlap, every higher identity is obtained by further
contracting the three-site exchange; if they are disjoint, it is obtained
from the four-site exchange.  Thus no arbitrary-order compatibility made
only from complete pair slices supplies a new ideal generator.

The same formula gives the full collision Maurer--Cartan hierarchy.  Its
order-three member is genuinely stronger than the *order-two Taylor
truncation*, because a direct connection coefficient can be dormant at
order two.  This does not contradict pair-slice redundancy: a complete
pair tensor contains all complement colour coefficients, whereas the
order-two collision system retains only one Taylor grade.

## 2. Uniform exposed-set formula

Let `B` have `2m` sites and work in the commutative site-square-zero algebra

\[
 \mathcal R_B=\bigotimes_{v\in B}(\mathbb C\oplus V_v),
 \qquad V_v^2=0.
\]

Let `Q` be an arbitrary quadratic and put `H=Q^[m]=Q^m/m!`.  Fix
`S subseteq B`, put `R=B\setminus S`, and decompose `Q` as

\[
 Q=q+\sum_{u\in S}\sum_c x_{u,c}\ell_{u,c}
   +\sum_{\{u,v\}\subseteq S}\sum_{c,d}
       a_{uv}^{cd}x_{u,c}x_{v,d}.                       \tag{1}
\]

Here `q` is internal to `R`, `ell_(u,c)` is the complete colour-`c`
star from `u` into `R`, and endpoint colours in `a_(uv)^(cd)` remain
attached to their named endpoints.

For a colour word `gamma:S->{0,1,2}`, let `Match(S)` denote all partial
matchings on `S`.  If `M` is such a matching, write `V(M)` for its covered
vertices and set

\[
 a_M(\gamma)=\prod_{\{u,v\}\in M}a_{uv}^{\gamma_u\gamma_v},
 \qquad
 \ell_{S\setminus V(M)}(\gamma)
    =\prod_{u\in S\setminus V(M)}\ell_{u,\gamma_u}.
\]

Use the convention `q^[d]=0` for `d<0`.  Then

\[
 \boxed{
 \iota_{S,\gamma}H
  =\sum_{M\in\operatorname{Match}(S)}
     a_M(\gamma)\,
     \ell_{S\setminus V(M)}(\gamma)\,
     q^{[m-|S|+|M|]} .}                                 \tag{2}
\]

**Proof.**  In a perfect matching of `B`, retain the edges having both
endpoints in `S`.  They form a unique partial matching `M`.  Every remaining
site of `S` is matched to a distinct site of `R`, producing the displayed
star product.  The unused sites of `R` are paired internally.  Their number
of edges is

\[
 m-\bigl(|M|+|S|-2|M|\bigr)=m-|S|+|M|.
\]

Conversely, every term of (2) reconstructs one such perfect matching.
The reconstruction is bijective.  Since `H=Q^[m]` and the final internal
power is divided, every unordered matching occurs with coefficient one.
No support, rank, or noncancellation hypothesis is used. `QED`

For the ternary target `Delta_B=sum_c X_c^B`, the corresponding residual is

\[
 \iota_{S,\gamma}(H-\Delta_B)
 =\text{the right side of (2)}
  -\sum_{c=0}^2
    \mathbf1_{\gamma_u=c\ \text{for every }u\in S}X_c^R.          \tag{3}
\]

For nonempty `S`, at most one summand in the target term is nonzero.  The
sum notation also covers `S=emptyset`, when it gives the full target.

## 3. Pair exchange and exact redundancy

For a physical pair `P={u,v}` define its complete residual rows by

\[
 E^P_{ab}=\iota_{u,a}\iota_{v,b}(H-\Delta_B).           \tag{4}
\]

If `P,P' subseteq S`, commutativity of contractions and (3) give

\[
 \boxed{
 \iota_{S\setminus P,\gamma}E^P_{\gamma|P}
 =\iota_{S,\gamma}(H-\Delta_B)
 =\iota_{S\setminus P',\gamma}E^{P'}_{\gamma|P'}.}     \tag{5}
\]

For overlapping pairs `(r,t)` and `(r,z)`, the minimal case has three
exposed sites.  On their common complement, write the three direct cells as
`a_ij,b_ik,c_jk` and the three stars as `p_i,s_j,ell_k`.  Formula (2) is

\[
 (a_{ij}\ell_k+b_{ik}s_j+c_{jk}p_i)q^{[m-2]}
   +p_is_j\ell_kq^{[m-3]}.                              \tag{6}
\]

Both pair charts give (6), merely in a different order.  Every contraction
at one or more further sites is a contraction of this literal equality.
There is therefore no independent higher curvature.

More strongly, the scalar coordinates of (4) are indexed by
`(a,b,omega)`, where `omega` is a colour word on `B\setminus P`.  This is
a bijection with all colour words on `B`.  Hence the scalar generator list
for any one complete pair system is exactly the full coordinate list of
`H-Delta_B`; changing the pair only permutes that list.  Equation (5) is an
identity in the polynomial ring of aggregate endpoint-ordered edge cells,
not an additional equation holding only on the target fibre.

Associated structural assumptions can still add information.  For
example, two zero-star charts impose two different literal zero blocks.
That extra source information is not supplied by the exchange equations
themselves.

## 4. Uniform collision/Bianchi hierarchy

The same theorem specializes to the half-shift source

\[
 q(t)=q_0+tK+t^2W,
 \qquad K=\sum_i z_i k_i,
 \qquad W=\sum_{i<j}\eta_{ij}z_iz_j.                    \tag{7}
\]

Assume `q_0` and the `k_i` have no `z` component.  For a subset `S` of
`r` sites, extraction of `t^r z_S` gives

\[
 \boxed{
 [t^rz_S]q(t)^{[m]}
  =\sum_{M\in\operatorname{Match}(S)}
       \left(\prod_{ij\in M}\eta_{ij}\right)
       \left(\prod_{k\in S\setminus V(M)}k_k\right)
       q_0^{[m-r+|M|]}.}                                \tag{8}
\]

This also follows directly from the normalized multinomial expansion

\[
 [t^r]q(t)^{[m]}
 =\sum_{a+2b=r}{K^aW^bq_0^{m-a-b}\over
                         a!b!(m-a-b)!}.                 \tag{9}
\]

The factorials in (9) exactly cancel the orderings of the unmatched sites
and of the edges of `M`, leaving coefficient one in (8).

For the half-shift target

\[
 Y+\prod_i(x_i-tz_i/2)+\prod_i(x_i+tz_i/2),             \tag{10}
\]

the fixed-`S` equation, for `r>=1`, is

\[
 \text{right side of (8)}=
 \begin{cases}
  0,&r\text{ odd},\\
  2^{1-r}X_{B\setminus S},&r\text{ even}.
 \end{cases}                                            \tag{11}
\]

At orders two and three this gives respectively

\[
 \eta_{ij}q_0^{[m-1]}+k_ik_jq_0^{[m-2]}
     ={1\over2}X_{-ij},                                 \tag{12}
\]

and

\[
 (\eta_{ij}k_k+\eta_{ik}k_j+\eta_{jk}k_i)q_0^{[m-2]}
   +k_ik_jk_kq_0^{[m-3]}=0.                             \tag{13}
\]

Equation (13) is a concrete quotient-free lower-cofactor curvature.  It is
not determined by the order-two images in (12) when, for example,
`q_0^[m-1]` vanishes in one direct-pair sector but its product with `k_k`
does not.  The dormant-connection example in
[`collision-cofactor-bianchi.md`](collision-cofactor-bianchi.md) realizes
exactly this phenomenon.  Thus (13) adds information to a Taylor system
truncated at order two.  It is nevertheless one top coefficient of the
full transformed tensor and adds nothing to a complete pair slice.

## 5. Lower-cofactor mixed partials are universally flat

There is a second possible meaning of "mixed partial."  Let
`partial_(uv;ab)` differentiate the polynomial map `Q -> Q^[m]` with
respect to the aggregate cell `a_(uv)^(ab)`.  For cells on pairwise
vertex-disjoint physical edges `e_1,...,e_k`, one has

\[
 \partial_{e_1}\cdots\partial_{e_k}H
 =x_{e_1}\cdots x_{e_k}
    Q_{B\setminus V(e_1,\ldots,e_k)}^{[m-k]};           \tag{14}
\]

if two selected physical edges meet, the derivative is zero.  Again the
coefficient is one.  For unnormalized `Q^m`, the right side of (14) is
multiplied by `m!` when its residual power is written as a divided power.

In particular, for two disjoint cells `e,f`, with
`C_e=Q_(B\setminus V(e))^[m-1]`, the lower cofactors obey

\[
 x_e\,\partial_f C_e
 =x_ex_fQ_{B\setminus V(e,f)}^{[m-2]}
 =x_f\,\partial_e C_f.                                  \tag{15}
\]

For overlapping cells both sides are zero.  All higher commutators and
Bianchi sums obtained from (14) vanish identically.  This is a useful
integrability check if lower cofactors have been introduced as independent
relaxation variables, but it is automatic for cofactors of one actual
quadratic.

Finally, equality `H(Q)=Delta_B` at one source does **not** imply
`partial_e H(Q)=0`.  Differentiating the target equation in a source-cell
direction is valid only along a proved family of exact solutions (as in a
target-stabilizer or half-shift construction).  Without such a family, the
only universal mixed-partial statement is the zero commutator (14)--(15),
not vanishing of either cofactor.

## 6. Audit

The dependency-free checker
[`verify_arbitrary_order_pair_cut_bianchi_exactness.py`](../computations/verify_arbitrary_order_pair_cut_bianchi_exactness.py)
independently reconstructs every perfect matching from a representative of
every exposed-set cardinality through ten sites, verifies coefficient-one
multiplicity, checks the
three- and four-site layer ledgers, checks complete-pair colour-coordinate
reindexing, and audits the half-shift target factors `2^(1-r)`.

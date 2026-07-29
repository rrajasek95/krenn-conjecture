# Arbitrary common annihilators expose the all-zero-cross branch

## 1. Outcome

The cross-product contraction loses all information at precisely the sites
where its three coefficient matrices vanish.  This note repairs that loss by
allowing an arbitrary vector in the common annihilator of the two contracted
star rows.

For an invertible deleted block `A_pq`, suppose every outside site is a
zero-cross witness for all three colors:

\[
 A_{pu}K_rA_{qu}^{T}=0\qquad(u\ne p,q,\ r=0,1,2).       \tag{1}
\]

Then the arbitrary-annihilator identities imply the following exact facts.

1. For each color `r`, at least two outside vertices have the coordinate
   common row line `C e_r` for their two blocks from `p,q`.
2. At `n=8`, the six outside vertices therefore partition into three
   two-element classes `U_0,U_1,U_2`.
3. Deleting `U_r` forces the complementary four-site matching tensor,
   restricted to the four common-annihilator planes, to be a nonzero pure
   tensor `kappa_r e_r^(tensor 4)`.  A second exact equation couples
   `kappa_r` to the four star vectors at the two holes.
4. For holes in two different classes, either the corresponding projected
   four-site cofactor is zero or a definite symmetrized star matrix is zero.
5. A four-site edge network with nonzero pure matching tensor has a
   target-aligned apex.  Combining those apices with the zero mixed
   cofactors forces the graph of nonzero mixed cofactors to be connected,
   with no rank assumption on its fifteen projected edge blocks.
6. Connectivity makes the zero-star alternatives incompatible with the
   three same-class star equations.  Hence the entire `n=8`
   all-zero-cross branch (1) is impossible, including its rank-degenerate
   boundary.

These conditions reject every invertible-pair branch of the existing `K_8`
witness-incidence model and prove that no full realization can have an
invertible pair for which all six outside sites are triple-zero witnesses.
The three pure cofactors alone are still consistent: an explicit rational
six-site network below satisfies them, the no-hole and one-hole equations,
and nine of the fifteen two-hole equations.  Its six failures show exactly
why the target-apex propagation must use the complete mixed-hole system.

## 2. The common-annihilator identities

Let `B` be even, let

\[
 H_B(A)=\Delta_{B,3}=\sum_{r=0}^2 e_r^{\otimes B},       \tag{2}
\]

fix distinct `p,q`, and put `R=B\setminus\{p,q\}`.  Orient
`A_xy` with rows at `x` and columns at `y`.  For covectors `alpha,beta`
at `p,q`, define

\[
 \begin{aligned}
 g&=\alpha^TA_{pq}\beta,\\
 x_u&=A_{pu}^T\alpha,\\
 y_u&=A_{qu}^T\beta,\\
 N_u(\alpha,\beta)&=\{z\in\mathbb C^3:x_u^Tz=y_u^Tz=0\}.
 \end{aligned}                                           \tag{3}
\]

Unlike the cross product `x_u cross y_u`, the space `N_u` remembers its
full dimension when `x_u,y_u` are dependent.  Choose independently an
arbitrary `z_u in N_u(alpha,beta)` at every contracted outside site.

Write `Q_w` and `Q_wz` for the one- and two-site partial contractions of
`H_R(A)`, and write

\[
 h_S=\left\langle H_S(A),\bigotimes_{u\in S}z_u\right\rangle . \tag{4}
\]

Then direct separation of perfect matchings gives three exact identities.

**Theorem 2.1 (arbitrary common-annihilator identities).**  For every
choice in (3),

\[
 \sum_{r=0}^2\alpha_r\beta_r\prod_{u\in R}z_{u,r}
   =g\left\langle H_R(A),\bigotimes_{u\in R}z_u\right\rangle, \tag{5}
\]

and, leaving one site `w` open,

\[
 \sum_{r=0}^2\alpha_r\beta_r
       \prod_{u\in R\setminus\{w\}}z_{u,r}\ e_r
   =gQ_w.                                                  \tag{6}
\]

For distinct holes `w,z`, put `S=R\setminus\{w,z\}`.  Then

\[
 \operatorname {diag}\left(
   \alpha_r\beta_r\prod_{u\in S}z_{u,r}
 \right)_{r=0}^2
 =gQ_{wz}+h_S(x_wy_z^T+y_wx_z^T).                         \tag{7}
\]

**Proof.**  In (5), every matching avoiding `pq` matches `p` to an
outside site `u`; its contraction contains `x_u^Tz_u=0`.  The surviving
matchings use `pq`, producing the right side.

For (6), a matching avoiding `pq` still vanishes.  If `p` is matched to
the open site `w`, then `q` is matched to a contracted site and is killed;
the case with `p,q` reversed is identical.  If neither endpoint is matched
to `w`, the contracted partner of `p` already kills the term.  The
`pq`-matchings give `gQ_w`.

With two holes, an avoiding matching can survive only when `p,q` are
matched to `w,z` in one of the two possible orders.  The remaining
matching sum is the common scalar `h_S`; the two assignments give the two
outer products in (7).  Matchings using `pq` give `gQ_wz`.  Contracting the
right side of (2) gives the displayed diagonal left sides. `QED`

The incidence quadric

\[
 X_{pq}=\{(\alpha,\beta):g(\alpha,\beta)=0\}              \tag{8}
\]

is where the new freedom is most useful.  On `X_pq`, the right sides of
(5) and (6) vanish and (7) loses its cofactor term `gQ_wz`.  When
`A_pq` is invertible, `g` is an irreducible bilinear form, so `X_pq` is
irreducible and its coordinate ring is a domain.

## 3. What three zero cross matrices mean

Put `P=A_pu` and `Q=A_qu`.  With the cross-product matrices `K_r` used in
[`two-vertex-annihilation-identities.md`](two-vertex-annihilation-identities.md),

\[
 \bigl((\alpha^TP)\mathbin\times(\beta^TQ)\bigr)_r
   =\alpha^T(PK_rQ^T)\beta.                              \tag{9}
\]

Thus all three matrices `PK_rQ^T` vanish exactly when every vector in the
row space of `P` is parallel to every vector in the row space of `Q`.

**Lemma 3.1 (triple-zero classification).**  If `PK_rQ^T=0` for all
three `r`, then either

* `P=0` or `Q=0`; or
* there is a nonzero row vector `ell` and column vectors `a,b` such that
  \[
       P=a\ell^T,\qquad Q=b\ell^T.                        \tag{10}
  \]

Conversely, every pair in these alternatives has three zero cross
matrices.

**Proof.**  Suppose both row spaces are nonzero.  Fix nonzero rows
`x in row(P)` and `y in row(Q)`.  Equation (9) makes them parallel.  Every
other row in either row space is parallel to the fixed nonzero row in the
other, so both row spaces are the same line.  This is (10).  The converse
is immediate from `ell cross ell=0`; a zero block is immediate as well.
`QED`

The one-sided-zero alternatives in Lemma 3.1 are important: (1) alone
does not force a fixed common row line at every site.  The arbitrary-plane
one-hole identity removes exactly this loophole at the sites needed below.

## 4. Two fixed coordinate common-line sites per color

Call `u` a **coordinate common-line site of color `r`** when

\[
 A_{pu}=a_ue_r^T,\qquad A_{qu}=b_ue_r^T,qquad
 (a_u,b_u)\ne(0,0).                                      \tag{11}
\]

This definition permits one of the two blocks to vanish, but their total
row space must be the nonzero line `C e_r`.

**Theorem 4.1 (two coordinate common lines).**  Suppose `A_pq` is
invertible and (1) holds at every `u in R`.  If (2) holds, then for every
color `r` there are at least two distinct coordinate common-line sites of
color `r`.

**Proof.**  Work first at a point `(alpha,beta)` of the dense open subset

\[
 X^\circ=X_{pq}\cap\{\alpha_0\alpha_1\alpha_2
                    \beta_0\beta_1\beta_2\ne0\}.         \tag{12}
\]

At every outside site, (1) and (9) show that
`span(x_u,y_u)` has dimension at most one.  Fix a color `r` and an omitted
site `w`.  The `r` coefficient of (6), restricted to `X_pq`, says

\[
 \alpha_r\beta_r\prod_{u\ne w}z_{u,r}=0                 \tag{13}
\]

for every independent choice `z_u in N_u(alpha,beta)`.

If `span(x_u,y_u)` is not `C e_r`, its annihilator `N_u` contains a
vector with nonzero `r` coordinate.  This includes the case
`span(x_u,y_u)=0`.  If no `u!=w` had span `C e_r`, choose such a vector at
every contracted site; (12) would make (13) nonzero.  Hence for every
omitted `w` there is some other site with contracted row span `C e_r`.
Equivalently, at each point of `X^circ` at least two sites have this span.

For completeness, this pointwise statement globalizes without a genericity
assumption on the blocks.  Let `Y_u` be the constructible subset of
`X^circ` on which `span(x_u,y_u)=C e_r`.  The preceding paragraph gives

\[
 X^\circ=\bigcup_{u\ne v}(Y_u\cap Y_v).                  \tag{14}
\]

The variety `X^circ` is irreducible, so one pair `Y_u,Y_v` is dense.
On that dense set every non-`r` coordinate of `alpha^T A_pu`,
`beta^T A_qu`, and the analogous two rows at `v`, vanishes.  These linear
polynomials therefore vanish on all of `X_pq`.  The two projections of
`X_pq` onto the `alpha` and `beta` spaces are surjective, so all columns
outside `r` in those four blocks vanish.  Density of `Y_u,Y_v` also says
that neither pair of blocks is simultaneously zero.  Thus `u,v` satisfy
(11). `QED`

This conclusion is strictly stronger than the earlier two-zero-witness
count.  At a triple-zero site the cross-product covector is identically
zero and makes the old one-hole identity tautological; the two-plane of
arbitrary annihilators instead detects its actual row line.

## 5. The six-site equality case at `n=8`

Now let `|B|=8`, so `R` has six vertices.  A nonzero row line cannot equal
two different coordinate lines.  The three sets supplied by Theorem 4.1
are therefore disjoint.  Since each has size at least two, they exhaust
`R`:

\[
 R=U_0\sqcup U_1\sqcup U_2,\qquad |U_r|=2.               \tag{15}
\]

For `u in U_c`, write

\[
 A_{pu}=a_ue_c^T,\qquad A_{qu}=b_ue_c^T.                 \tag{16}
\]

The fixed common-annihilator plane is then

\[
 L_u=e_c^\perp.                                          \tag{17}
\]

Take `U_r={w,z}` and put `S_r=R\setminus U_r`.  Every site of `S_r` has
label different from `r`, so `e_r in L_u` there.  Define

\[
 N_r=a_wb_z^T+a_zb_w^T.                                  \tag{18}
\]

**Theorem 5.1 (three pure four-site cofactors).**  There are nonzero
constants `kappa_0,kappa_1,kappa_2` and scalars `lambda_r` such that, for
every `r`,

\[
 \left\langle H_{S_r}(A),\bigotimes_{u\in S_r}z_u\right\rangle
   =\kappa_r\prod_{u\in S_r}z_{u,r}
 \quad(z_u\in L_u),                                      \tag{19}
\]

and

\[
 E_{rr}-\kappa_rN_r=\lambda_rA_{pq}.                     \tag{20}
\]

Equivalently, the restriction of the four-site matching tensor `H_Sr` to
the four planes (17) is exactly

\[
                 \kappa_r e_r^{\otimes4}.                \tag{21}
\]

**Proof.**  Use `w,z` as the two holes in (7) and restrict to `X_pq`.
The target is

\[
 \alpha_r\beta_r\prod_{u\in S_r}z_{u,r}\ E_{rr},        \tag{22}
\]

because the two sites of each other label remain contracted and kill the
other two diagonal coordinates.  By (16), the correction is

\[
 h_{S_r}\,\alpha^TN_r\beta\ E_{rr}.                      \tag{23}
\]

Choose all four annihilators equal to `e_r`.  On the dense open set (12),
the left side of (22) is nonzero.  Hence both the resulting cofactor
`kappa_r` and the bilinear form in (23) are nonzero.  Equation (7) gives

\[
 \alpha_r\beta_r=\kappa_r\alpha^TN_r\beta
 \quad\text{on }X_{pq}.                                  \tag{24}
\]

For arbitrary annihilators, subtracting (24) from (22)--(23) and using
that the coordinate ring of `X_pq` is a domain gives (19).  Finally the
bilinear polynomial in (24) vanishes on the irreducible quadric `g=0`.
It has the same bidegree as `g`, so it is a scalar multiple of `g`.  This
is exactly (20). `QED`

The constants in (19) are actual four-site cofactors, not free normalizing
parameters.  This is the compatibility that the zero cross products erase.

## 6. Mixed holes give the next alternative

Let `w in U_c` and `z in U_d` with `c!=d`, and set

\[
 S_{wz}=R\setminus\{w,z\},\qquad
 N_{wz}=a_wb_z^T+a_zb_w^T.                               \tag{25}
\]

At least one vertex of every label remains contracted, so the diagonal
target in (7) is zero.  The correction is supported at the single hole
cell `e_c tensor e_d` and has scalar coefficient
`h_S alpha^T N_wz beta`.  The domain property therefore gives:

**Theorem 6.1 (mixed-hole alternative).**  For every cross-class pair of
holes, at least one of the following holds.

1. The projected four-site cofactor is identically zero:
   \[
    \left\langle H_{S_{wz}}(A),\bigotimes_{u\in S_{wz}}z_u\right\rangle=0
    \quad\text{for all }z_u\in L_u.                      \tag{26}
   \]
2. The symmetrized star matrix vanishes:
   \[
                         N_{wz}=0.                        \tag{27}
   \]

**Proof.**  On `X_pq`, (7) is the product of the polynomial in (26) and
the class of `alpha^T N_wz beta`.  If the first factor is nonzero, the
second vanishes on `X_pq`, hence `N_wz=lambda A_pq`.  But `rank N_wz<=2`
while `A_pq` is invertible, so `lambda=0`. `QED`

Thus (19) for the three same-class deletions is only half of the equality
case.  The twelve cross-class deletions impose a coupled zero pattern
between projected cofactors and star bilinear forms.

### 6.1 A pure four-site tensor has rigid extension annihilators

The following squarefree-algebra lemma controls a component cut even when
every projected edge is singular.  Let `V_0,...,V_3` be two-spaces and
write

\[
 {cal A}_1=\bigoplus_iV_i,\qquad
 {cal A}_2=\bigoplus_{i<j}V_i\otimes V_j,
\]

with multiplication commutative between different sites and zero when two
factors come from the same site.  Thus, if `q in A_2` is the collection of
six edge forms, then `q^2/2 in tensor_i V_i` is its four-site matching
tensor.

**Lemma 6.2 (extension-annihilator lemma).**  Suppose

\[
             q^2/2=\kappa p_0p_1p_2p_3\ne0.             \tag{27a}
\]

If `ell=ell_0+...+ell_3 in A_1` satisfies `q ell=0`, then

\[
                    \ell_i\in\mathbb C p_i              \tag{27b}
\]

at every site.  The dimension of the annihilator need not be one.

**Proof.**  Let `I={i:ell_i!=0}`.  Change basis independently at every
site in `I` so that `ell_i=e_0`, and relabel the sites so that
`I={0,...,k-1}`.  Solving the linear coefficient equations `q ell=0`
gives the following four exhaustive normal forms for the only part needed,
namely `q^2/2`.

* If `k=1` or `k=3`, then `q^2/2=0`.
* If `k=2`, then for some `v_2 in V_2,v_3 in V_3`,
  \[
                 q^2/2=-2e_0e_0v_2v_3.                 \tag{27c}
  \]
* If `k=4`, then
  \[
       q^2/2=2(s^2+st+t^2)e_0e_0e_0e_0                 \tag{27d}
  \]
  for two scalar parameters `s,t`.

Here is the direct coefficient check.  For `k=1`, only the three edges
incident with site zero can occur, so there is no perfect matching.  For
`k=2`, the edge normal form is

\[
 \begin{array}{c|cccccc}
 ij&01&02&12&03&13&23\\ \hline
 q_{ij}&D&-e_0v_2^T&e_0v_2^T&-e_0v_3^T&e_0v_3^T&0,
 \end{array}                                             \tag{27e}
\]

with arbitrary `D`; multiplication gives (28c).  For `k=3`, the equations
leave only edges on the first three sites (in the five-parameter form
obtained by the three cancellations), so again there is no perfect
matching.  For `k=4`, all six edges are scalar multiples of `e_0e_0`, with

\[
        (q_{01},q_{02},q_{03},q_{12},q_{13},q_{23})
        =(t,s,-s-t,-s-t,s,t),                            \tag{27f}
\]

and direct multiplication gives (28d).

The nonzero hypothesis in (27a) leaves only `k=2,4`.  Equations
(27c)--(27d) show that `ell_i` is a factor of `q^2/2` at every site in its
support.  Uniqueness of the four nonzero mode lines of a pure tensor then
gives `ell_i in C p_i`; the zero components satisfy this as well. `QED`

The warning in the statement is genuine.  In (27e), take `D=0` and
`v_2=v_3=e_0`.  Then the matching tensor is nonzero pure, while both
`e_0^(0)+e_0^(1)` and `-e_0^(2)+e_0^(3)` annihilate `q`.

**Corollary 6.3 (pure-`K_4` target apex).**  If `q^2/2` is a nonzero pure
tensor on four two-dimensional sites, then some site `i` is incident only
with forms having the pure factor `p_i` at that endpoint.  In particular,
all three incident forms have rank at most one.

**Proof.**  Normalize the four pure factors to `e_0`.  For each site `i`,
let

\[
             \ell^{(i)}=\partial_{i,e_1^*}q.             \tag{27g}
\]

Contraction is a derivation, so differentiating `q^2/2=kappa e_0^4`
gives `q ell^(i)=0`.  Lemma 6.2 says that every component of every
`ell^(i)` is on its target line `C e_0`.  Consequently each edge matrix,
in the target-first bases at its endpoints, has the shape

\[
                         \begin{pmatrix}a&b\\c&0\end{pmatrix}.  \tag{27h}
\]

If some `ell^(i)=0`, all three matrices incident with `i` have zero
transverse row at that endpoint.  Each is therefore `p_i tensor v_ij`;
this is the desired target apex.

Suppose instead that all four `ell^(i)` are nonzero.  They are supported
away from `i`, so Lemma 6.2 and its four support cases force every support
to have size exactly two.  For fixed `i`, let `m(i)` be its unique
nonsupport neighbor.  The support-two normal form (27e) says that the edge
joining the two complementary sites, namely `i m(i)`, is identically zero.
Hence the missing edges form a perfect matching.  Every other edge belongs
to the supports at both its endpoints; both off-diagonal entries `b,c` in
(27h) are nonzero, so that edge has rank two.  On the other hand, (27e)
also says that every edge from the support of `ell^(i)` to its complement
has rank at most one.  This includes the two nonmissing edges incident with
`i`, a contradiction. `QED`

Form the mixed-cofactor graph `G` on `R`: vertices of different classes
are adjacent exactly when the cofactor in (26) is nonzero.

**Theorem 6.4 (no isolated cofactor vertex).**  The graph `G` has no
isolated vertex.

**Proof.**  Suppose, after permuting classes, that `y in U_0` is isolated,
and let `x` be its mate in `U_0`.  Put `D=U_1 union U_2`.  Let `q` be the
six projected edges on `D`, viewed in the algebra above.  The pure equation
for deleting `U_0` says

\[
                     q^2/2=\kappa_0e_0^{\otimes4}.       \tag{27i}
\]

Let `L_x in L_x tensor A_1(D)` collect the four projected edges from `x`
to `D`.  Since `y` is isolated, deleting `y` and any `v in D` leaves a
zero four-site cofactor on `{x} union (D setminus {v})`.  These are exactly
the four multidegree components of

\[
                              qL_x=0.                    \tag{27j}
\]

Apply Lemma 6.2 to every row of `L_x`.  Every projected edge from `x` to
`v in D` consequently has its factor at `v` on the line `C e_0`.

Now use the pure equation on `U_0 union U_2`.  Quotient both `U_2` planes
by `C e_0`.  Each of the two cross matchings vanishes, because its edge
from `x` has an `e_0` factor at one of those sites.  Only the matching
`xy | U_2` remains, so

\[
                    \bar A_{yx}\ \text{is proportional to}
                    \ e_1\otimes e_1.                   \tag{27k}
\]

The proportionality is nonzero because the target
`kappa_1 e_1^(tensor 4)` is nonzero.  Repeating the argument on
`U_0 union U_1` and quotienting its two sites by `C e_0` instead gives

\[
                    \bar A_{yx}\ \text{is proportional to}
                    \ e_2\otimes e_2,                   \tag{27l}
\]

again nonzero.  The two lines in `L_y tensor L_x` are distinct, a
contradiction. `QED`

The star equations also dispose of a connected two-versus-four component
split without any assumption on the projected edges.

**Theorem 6.5 (no `2+4` component split).**  The graph `G` cannot have
exactly two connected components of sizes two and four.

**Proof.**  A two-vertex component cannot be a same-class pair, since its
vertices would have no possible graph edge and would be isolated.  Thus its
two classes are split across the cut, while the connected four-vertex
component `Y` contains both sites of the third class, say `U_c`.

Recall that every graph edge `uv` has `N_uv=0`, and no site has
`(a_u,b_u)=(0,0)`.  If one `a_u` vanished on `Y`, the zero-`N` edge
equations would propagate this through connected `Y`, making the
same-class matrix `N_c` vanish.  Equation (20) would then make the rank-one
matrix `E_cc` a multiple of the invertible matrix `A_pq`, which is
impossible.  The same argument applies to the `b` vectors.  Thus every
`a_u,b_u` on `Y` is nonzero.  Along its edges the rank-one summands in
`N_uv=0` must be proportional; connectivity puts all `a_u` on one line
and all `b_u` on one line.  In particular `N_c` is nonzero of rank one.

In (20) for color `c`, the left side has rank at most two, so
`lambda_c=0`.  Hence `N_c` is proportional to `E_cc`, and the common
`a`- and `b`-lines on `Y` are both `C e_c`.

Let `d,e` be the other two colors.  Each of `U_d,U_e` has one site in
`Y` and one in the two-vertex component.  It follows that

\[
 N_d=e_cx_d^T+y_de_c^T,\qquad
 N_e=e_cx_e^T+y_ee_c^T                              \tag{27m}
\]

for suitable vectors (with harmless scalar factors absorbed).  Therefore
both matrices vanish in every entry outside row or column `c`.  Put
`M_r=E_rr-kappa_rN_r=lambda_rA_pq`.  Then

\[
 (M_d)_{dd}=1,\quad(M_d)_{ee}=0,
 \qquad
 (M_e)_{dd}=0,\quad(M_e)_{ee}=1.                         \tag{27n}
\]

In particular `lambda_d,lambda_e` are nonzero.  The first pair in (27n)
would give `(A_pq)_{dd}!=0,(A_pq)_{ee}=0`, while the second gives the
opposite, a contradiction. `QED`

Thus any disconnected `G` has components of size at least two, but it has
neither an isolated same-class pair nor a connected `2+4` split.  The only
remaining component patterns are two transversal three-vertex components
or three mixed-class two-vertex components.

### 6.2 Target-apex propagation excludes the transversal cut

We need one elementary propagation rule for a zero four-site cofactor.

**Lemma 6.6 (zero-`K_4` quotient rule).**  Let

\[
 B_{ab}B_{cd}+B_{ac}B_{bd}+B_{ad}B_{bc}=0              \tag{27o}
\]

as a tensor on four sites.  If the factors at `a` of `B_ab` and `B_ac`
both lie in one line `L subset V_a`, then either the factor at `a` of
`B_ad` also lies in `L`, or `B_bc=0`.

**Proof.**  Apply the quotient `V_a -> V_a/L` to (27o).  Its first two
terms vanish, leaving

\[
                  (\bar B_{ad})B_{bc}=0.                 \tag{27p}
\]

A tensor product over a field is zero only if one factor is zero. `QED`

**Theorem 6.7 (no transversal `3+3` split).**  The graph `G` cannot have
two three-vertex components, each containing one site of every class.

**Proof.**  Write `U_c={u_c0,u_c1}` and take the alleged component cut

\[
 X=\{u_{00},u_{10},u_{20}\},\qquad
 Y=\{u_{01},u_{11},u_{21}\}.                             \tag{27q}
\]

The six cross-cut mixed pairs have zero complementary cofactors.  In the
vertex order

\[
 (u_{00},u_{01},u_{10},u_{11},u_{20},u_{21})=(0,1,2,3,4,5),
\]

their four-sets are

\[
 1245, 1234, 0345, 0134, 0235, 0125.                \tag{27r}
\]

The three nonzero pure four-sets are

\[
 P_0=2345,qquad P_1=0145,qquad P_2=0123.               \tag{27s}
\]

By Corollary 6.3, choose on each `P_r` a target apex: all three incident
edge factors there lie on `C e_r`.  There are `4^3=64` choices.  The
following finite propagation is exhaustive.

Record two kinds of facts: an edge is zero, or its factor at a specified
endpoint is on one of that endpoint's two coordinate lines.  Two different
line records at one endpoint make the edge zero.  On each zero set in
(27r), whenever two incident edge factors have the same recorded line,
Lemma 6.6 branches into its two alternatives: record that line on the third
edge, or set the opposite edge to zero.  A branch closes once, for some
`P_r`, every one of its three perfect matchings contains either a zero edge
or an endpoint recorded on the other coordinate line.  Indeed the
`e_r^(tensor 4)` coefficient would then be zero, contradicting (19).

Class permutations and the global interchange `X <-> Y` reduce the 64
apex triples to six orbits.  Here an entry is the apex chosen respectively
for `(P_0,P_1,P_2)`.  The final two columns give the number of leaves and
maximum depth in the lexicographic proof tree generated by the preceding
rule.

\[
\begin{array}{c|c|c|c}
\text{representative}&\text{orbit size}&\text{leaves}&\text{depth}\\ \hline
(u_{10},u_{00},u_{00})&12&38&11\\
(u_{10},u_{00},u_{01})&12&127&15\\
(u_{10},u_{01},u_{00})&12&31&12\\
(u_{10},u_{01},u_{01})&12&27&10\\
(u_{10},u_{20},u_{00})&4&29&10\\
(u_{10},u_{20},u_{01})&12&59&12
\end{array}                                               \tag{27t}
\]

Every leaf closes by the pure-coefficient test, and the orbit sizes sum to
64.  The exact recursion, including the six sets (27r), all disjunctive
branches, the orbit calculation, and the leaf/depth counts, is audited by
`audit_disconnected_apex_propagation` in the checker.  Thus no apex choice,
and hence no transversal cut, is possible. `QED`

The same propagation closes the other `3+3` orbit and the three-component
case.

**Theorem 6.8 (no residual component pattern).**  The graph `G` cannot be
the union of two nontransversal three-vertex components or of three
two-vertex components.

**Proof.**  For a nontransversal `3+3` split, take the components to be
`{0,1,2}` and `{3,4,5}`.  Each contains a full class and one site of another
class.  The eight cross-component mixed pairs give the zero four-sets

\[
 1245, 1235, 1234, 0245, 0235, 0234, 0135, 0134.  \tag{27u}
\]

Choose one target apex on each pure set in (27s) and apply exactly the
quotient branching rule of Theorem 6.7 to (27u).  All 64 apex choices
close by the same pure-coefficient test.

If there are three two-vertex components, each component must join
different classes.  Counting the two vertices of every class shows that
there is exactly one component of each class-pair type.  Up to the pair
symmetries take the component edges to be `02,14,35`.  The other nine mixed
pairs cross components and give

\[
 1245, 1235, 1234, 0345, 0245, 0234,
 0135, 0134, 0125.                                    \tag{27v}
\]

The identical 64-choice propagation again has no surviving branch.  Both
exact exhaustions, including the displayed zero-set lists, are performed
by `audit_disconnected_apex_propagation`.  A separate five-motif scalar
compression of the `2+2+2` calculation is given in
[`common-annihilator-222-boundary.md`](common-annihilator-222-boundary.md).
`QED`

We can now finish the all-zero-cross branch without a projected-rank
assumption.

**Theorem 6.9 (all-zero-cross equality obstruction).**  Under the
hypotheses of Theorem 5.1 and (1), no `n=8` realization exists.

**Proof.**  If `G` were disconnected, Theorem 6.4 excludes a singleton
component; Theorem 6.5 excludes component sizes `2+4`; Theorems 6.7 and
6.8 exclude both types of `3+3` split and the only remaining pattern
`2+2+2`.  Thus `G` is connected.

On every edge of `G`, Theorem 6.1 gives

\[
                    a_ub_v^T+a_vb_u^T=0.                \tag{27w}
\]

No site has `(a_u,b_u)=(0,0)`.  If some `a_u=0`, then `b_u!=0` and
(27w) forces `a_v=0` at every neighbor; connectivity propagates this to
all six sites.  Every same-class `N_r` would vanish, and (20) would make
`E_rr` a multiple of the invertible `A_pq`, impossible.  Hence every
`a_u` is nonzero; symmetrically every `b_u` is nonzero.

Along an edge, equality of the two nonzero rank-one summands in (27w)
makes the two `a` vectors proportional and the two `b` vectors
proportional.  Connectivity puts all six `a_u` on one line and all six
`b_u` on one line.  Consequently all three `N_r` are multiples of one
fixed rank-one matrix `M`.  In (20), each left side has rank at most two,
so `lambda_r=0` because `A_pq` is invertible.  It would follow that the
same matrix `M` is proportional to each of `E_00,E_11,E_22`, an
impossibility. `QED`

### 6.3 Independent dense-chart audit

Theorem 6.9 already closes all projected-rank strata.  The argument below
is retained as an independent earlier audit of the full-rank chart: it uses
nondegenerate Pluecker coordinates instead of target-apex propagation and
provides useful exact cut certificates for comparison.

Let

\[
 \bar A_{uv}:L_u\times L_v\longrightarrow\mathbb C       \tag{28a}
\]

be the restriction of the outside block `A_uv` to the two annihilator
planes.  In this subsection assume that all fifteen forms `bar A_uv` are
nondegenerate.

We use the following standard four-site consequence of the triangle
syzygy.

**Lemma 6.10 (nondegenerate zero `K_4`).**  Let four two-dimensional spaces
carry six nondegenerate bilinear forms `B_ij`.  If their four-site matching
tensor is zero, there are a common two-space `W`, isomorphisms
`phi_i:V_i -> W`, and nonzero scalars `lambda_ij` such that

\[
 B_{ij}(x_i,x_j)=\lambda_{ij}[\phi_i(x_i),\phi_j(x_j)],  \tag{28b}
\]

where `[ , ]` is one fixed alternating bracket.  For ordered vertices
`a<b<c<d`, the edge scalars obey

\[
 \lambda_{ab}\lambda_{cd}
 =-\lambda_{ac}\lambda_{bd}
 = \lambda_{ad}\lambda_{bc}.                            \tag{28c}
\]

If two such zero `K_4`s share three vertices, their bracket charts agree
on the union after rescaling the `phi_i` and `lambda_ij`.

**Proof.**  Fix the argument at one vertex in the zero-hafnian equation.
It becomes a three-term linear syzygy among the three nondegenerate forms
on the opposite triangle.  Normalizing two of those forms to the standard
bracket and comparing the eight trilinear coefficients forces the third
to be the same bracket.  The two-dimensional solution space of the
syzygy consists of brackets against one common vector; varying the fixed
argument therefore produces the fourth map `phi_i`.  Nondegeneracy makes
it an isomorphism.  The ordinary Grassmann--Pluecker relation

\[
 [a,b][c,d]-[a,c][b,d]+[a,d][b,c]=0                     \tag{28d}
\]

then gives (28c).  Three shared nondegenerate forms determine the
identifications up to one common change of basis and site rescalings,
which proves the gluing assertion. `QED`

This is also Lemma 4.1 and Corollary 4.2 of
[`local-algebra.md`](local-algebra.md), specialized to four sites.

Form a graph `G` on the six outside vertices: a cross-class pair `wz` is
an edge exactly when the projected cofactor in (26) is nonzero.  We first
show that `G` is connected.  If not, let `X|X^c` be a component cut.
For every `u in X,v in X^c` of different labels, the four-site cofactor on
`R\setminus{u,v}` is zero.  By Lemma 6.10, each such complementary `K_4`
is an alternating-bracket chart.  The family of these `K_4`s is connected
under three-vertex overlaps, so all its charts glue.

There are only five cuts up to permuting the three pairs, swapping inside
them, and replacing a cut by its complement.  Record a cut by the sorted
numbers of its vertices in the three pairs:

\[
 (0,0,1),\ (0,0,2),\ (0,1,1),\ (0,1,2),\ (1,1,1).       \tag{28e}
\]

The scalar audit on the glued bracket chart is particularly small.  Put
`l_ij=lambda_ij`.  Every zero four-set `a<b<c<d` supplies the two signed
binomials

\[
 {l_{ab}l_{cd}\over l_{ac}l_{bd}}=-1,
 \qquad
 {l_{ab}l_{cd}\over l_{ad}l_{bc}}=1.                    \tag{28f}
\]

For the first four cut types in (28e), multiplying and dividing the
relations (28f) gives `1=-1`.  Exact exponent certificates, with the two
rows of each zero four-set placed consecutively in lexicographic order,
are

\[
\begin{array}{c|l}
X&\text{certificate}\ y\\ \hline
\{0\}&(0,0,1,0,-1,0,1,0)\\
\{0,1\}&(0,0,0,0,0,0,0,0,0,0,1,0,-1,0,1,0)\\
\{0,2\}&(0,-1,0,1,1,-1,0,0,0,0,0,0)\\
\{0,1,2\}&(0,0,0,0,0,-1,0,0,1,0,1,0,-1,1,0,-1).
\end{array}                                               \tag{28g}
\]

In each row the signed sum of exponent vectors is zero, while the sum of
coefficients multiplying the first equation in (28f) is odd.  Thus the
left sides multiply to `1` and the right sides to `-1`.

For the transversal cut `X={0,2,4}`, the binomials are consistent, but
they force a different contradiction.  On the pure four-set
`R\setminus U_0={2,3,4,5}`, write the three bracket matching products as
`P_0,P_1,P_2` in lexicographic matching order and their nonzero scalar
weights as `w_0,w_1,w_2`.  Exact multiplication of (28f) gives

\[
                   {w_0\over w_1}={w_0\over w_2}=-1.     \tag{28h}
\]

Since `P_0-P_1+P_2=0`, its alleged pure cofactor is therefore

\[
 w_0P_0+w_1P_1+w_2P_2=-2w_0P_2.                         \tag{28i}
\]

This is a product of two nondegenerate brackets.  It has mode rank two at
each of its four sites and cannot equal the mode-rank-one tensor in (21).
All five cuts are impossible, proving that `G` is connected.

Connectivity is incompatible with the star equations.  Theorem 6.1 gives

\[
 a_ub_v^T+a_vb_u^T=0\qquad(uv\in E(G)).                  \tag{28j}
\]

No site has `(a_u,b_u)=(0,0)`, because its same-class matrix `N_r` would
vanish, contradicting (20).  If one `a_u` vanishes, (28j) propagates that
vanishing through connected `G`; then every `N_r` vanishes.  The same
holds for the `b_u`.  Hence all `a_u,b_u` are nonzero.  On an edge, equality
of the two nonzero rank-one matrices in (28j) makes the `a` vectors
proportional and the `b` vectors proportional.  Connectivity puts all six
`a_u` on one line and all six `b_u` on one line.  Consequently all three
same-class matrices `N_r` are multiples of one fixed rank-one matrix.

In (20), the left side has rank at most two, so `lambda_r=0`; it would
make that one rank-one matrix proportional to each of
`E_00,E_11,E_22`.  This is impossible.  We have proved:

**Theorem 6.11 (full-rank equality-chart obstruction).**  The `n=8`
all-zero-cross equality branch has no solution for which every projected
outside block (28a) has rank two.

The proof uses all fifteen two-hole equations jointly.  Its exact finite
part is only the five cut types (28e); no support positivity or generic
noncancellation is used.  Its former rank-degenerate boundary is now closed
by the target-apex argument of Theorem 6.9.

## 7. A simultaneous local model for all three pure cofactors

The three equations (19) are not mutually contradictory.  Here is a
rational construction.  Name the outside vertices

\[
 U_c=\{u_{c,0},u_{c,1}\}\qquad(c=0,1,2),                 \tag{28}
\]

and take

\[
 \begin{aligned}
 A_{pq}&=I_3,\\
 A_{p,u_{c,i}}&=E_{cc},\\
 A_{q,u_{c,i}}&=\tfrac12E_{cc}.                           \tag{29}
 \end{aligned}
\]

For distinct labels `c,d`, let `r` be the third color and put

\[
 A_{u_{c,i},u_{d,j}}=
 \begin{cases}
 E_{rr},&i=j,\\
 0,&i\ne j.
 \end{cases}                                             \tag{30}
\]

All three within-class blocks are zero.

For fixed `r`, the four vertices in the other two classes have exactly one
supported perfect matching, namely the two equal-index edges in (30).
Both edges carry color `r`.  Hence

\[
 H_{S_r}\big|_{\otimes L_u}=e_r^{\otimes4},              \tag{31}
\]

so (19) holds with `kappa_r=1`.  Moreover

\[
 N_r=E_{rr},                                              \tag{32}
\]

and (20) holds with `lambda_r=0`.

The support on all six outside vertices is the disjoint union of the two
triangles with fixed index `i`.  Consequently `H_R=0`.  The no-hole and
all six one-hole identities hold, all three same-class two-hole identities
hold by (31)--(32), and the six cross-class pairs with equal indices have
zero complementary cofactor.  Thus nine of the fifteen two-hole identities
hold.

The remaining six pairs are exactly

\[
 \{u_{c,i},u_{d,j}\}:c\ne d,\ i\ne j.                   \tag{33}
\]

For each, the projected cofactor is a nonzero monomial and `N_wz!=0`, so
Theorem 6.1 fails.  For example, take holes `u_00,u_11`, contract the other
four sites respectively by `e_1,e_0,e_0,e_1`, and take
`alpha=e_0,beta=e_1`.  Then `alpha^T beta=0`, the projected cofactor is
`1`, the diagonal target is zero, and the correction is

\[
                         \tfrac12E_{01}\ne0.             \tag{34}
\]

This is an exact local countermodel to any proposed contradiction using
only the three pure cofactors (19).

There is also no way to repair this particular outside network merely by
changing its star vectors.  The six pairs (33) form a connected `6`-cycle
`G`.  If every one of their nonzero cofactors is to obey Theorem 6.1, then

\[
 a_ub_v^T+a_vb_u^T=0\qquad(uv\in E(G)).                  \tag{35}
\]

The same-class matrices `N_r` are nonzero by (20): otherwise a rank-one
matrix `E_rr` would be a scalar multiple of the invertible `A_pq`.
Therefore no site can have `(a_u,b_u)=(0,0)`.

If one site has `a_u!=0,b_u=0`, (35) forces both neighbors, and then the
whole connected graph, to have the same form; all same-class `N_r` would
be zero.  The case `a_u=0,b_u!=0` is symmetric.  Hence every `a_u,b_u` is
nonzero.  Along an edge, equality of the two nonzero rank-one tensors in
(35) forces

\[
 a_v=t_{uv}a_u,\qquad b_v=-t_{uv}b_u.                    \tag{36}
\]

Connectivity makes all `a_u` proportional to one vector and all `b_u`
proportional to one vector.  Every same-class `N_r` is consequently a
multiple of one fixed rank-one matrix.  In (20), the left side has rank at
most two, so `lambda_r=0`; it would then force that one rank-one matrix to
be simultaneously proportional to `E_00,E_11,E_22`, an impossibility.

This last argument diagnoses the local model.  For an arbitrary network the
pure conditions alone do not fix which mixed cofactors vanish; the
target-apex and quotient propagation in Theorems 6.4--6.9 is what supplies
the missing global connectivity statement.

## 8. The `K_8` witness-incidence model is rejected

Consider the zero-one model from
[`witness-incidence-k8-countermodel.md`](witness-incidence-k8-countermodel.md).
For each of its four identity blocks `pq`, every outside site obeys (1),
and its common row line is the coordinate line prescribed by the label
table in that note.  Each color occurs exactly twice, so the model lies
precisely in the equality pattern (15).  Its cross-product contractions
are all zero, which is why all old two-hole equations for the four identity
pairs passed vacuously.

The arbitrary-plane audit gives, over the twelve identity-pair/color
branches:

\[
 \begin{array}{c|ccc}
 \text{projected four-site cofactor}&0&\text{impure}&
       \text{nonzero pure}\\ \hline
 \text{number of branches}&7&4&1.
 \end{array}                                              \tag{37}
\]

The first eleven branches violate (19).  The lone pure branch is
`(p,q,r)=(6,7,2)` and has `kappa_2=1`, but its star matrix is

\[
                         N_2=2E_{01}.                     \tag{38}
\]

Thus `E_22-N_2` is not a scalar multiple of `A_67=I_3`, violating (20).
All twelve branches are therefore excluded.  This is a strict separation
between the zero-cross incidence shadow and the arbitrary-annihilator
equations.

## 9. Exact checker and scope

Run

```text
.venv/bin/python computations/verify_common_annihilator_planes.py
```

The checker performs exact rational and symbolic audits of:

1. the no-, one-, and two-hole matching decompositions with independently
   variable annihilators in six two-planes;
2. the triple-zero and coordinate-row-line structure;
3. all twelve projected-purity and star equations in the old `K_8` model,
   including the `7+4+1` split in (37);
4. the rational local model (29)--(30), its three pure cofactors, and its
   three star identities;
5. the exact `9/6` split of its two-hole equations and the incidence-point
   residual (34); and
6. the four support normal forms in Lemma 6.2 and the sharp two-dimensional
   annihilator example;
7. the pure-`K_4` target-apex argument;
8. the `2+4` star obstruction and all `4^3` apex placements for both
   `3+3` cut types and the `2+2+2` component pattern; and
9. the resulting connected-graph star contradiction, as well as the
   independent full-rank Pluecker-chart audit.

Thus there is no remaining gap inside the all-triple-zero hypothesis (1).
The broader invertible-pair case is not settled by this note: the earlier
colorwise witness counts allow a site to witness only one or two colors,
so the six fixed two-planes and the three overlapping pure `K_4` equations
used here need not exist.

# Diagonal signed models collapse to a binary Pfaffian partition problem

This note isolates a considerably smaller obstruction inside the diagonal
`{0,+1,-1}` model.  On eight vertices the obstruction is already visible
after reducing every entry modulo two: signs and exact signed-count
cardinality constraints are unnecessary.

## 1. Factorization and reduction modulo two

Let `A_r=(a^r_uv)` be the scalar edge matrix for color `r`.  For an even
set `S`, write

\[
 h_r(S)=\operatorname{haf} A_r[S],\qquad h_r(\varnothing)=1. \tag{1}
\]

If a vertex coloring has color classes `S_0,S_1,S_2`, diagonality forces
every matching edge to stay inside one class.  Hence its coefficient is

\[
                         h_0(S_0)h_1(S_1)h_2(S_2).        \tag{2}
\]

An odd class makes (2) zero automatically.  Thus an exact diagonal GHZ
source would have `h_r(V)=1` and, for every proper even ordered partition
`V=S_0 disjoint-union S_1 disjoint-union S_2`, at least one factor in (2)
equal to zero.

Now reduce modulo two.  A signed entry becomes its support bit, the hafnian
is the parity of the supported perfect matchings, and an alternating matrix
`A` is nonsingular exactly when its full Pfaffian is one.  Therefore any
integer signed solution would give three nonsingular alternating matrices
over `F_2` satisfying

\[
 \operatorname{Pf}A_0[S_0]\operatorname{Pf}A_1[S_1]
 \operatorname{Pf}A_2[S_2]=0                             \tag{3}
\]

for every proper even ordered partition.

## 2. Exact eight-vertex binary obstruction

**Finite lemma.**  Let `A_0,A_1,A_2` be alternating `8 by 8` matrices over
`F_2`, with all three matrices nonsingular.  There is a proper even ordered
partition `V=S_0 disjoint-union S_1 disjoint-union S_2` such that every
principal restriction `A_r[S_r]` is nonsingular.  Empty blocks are allowed,
but at least two blocks are nonempty.

The exact exhaustive audit is
`computations/verify_diagonal_n8_mod2_sat.py`.  It uses one Boolean support
variable for each of the `3*28` colored entries.  For each color, even set,
and perfect matching it defines an `active` variable as the conjunction of
the matching-edge variables, then defines the subset Pfaffian as their XOR.
The three full Pfaffians are unit clauses.  Since an odd full matching count
contains a supported perfect matching, a common vertex permutation makes a
color-zero matching canonical; its four support variables are fixed true.
Finally each of the 1,638 proper even ordered partitions gets the clause

\[
 \neg h_0(S_0)\ \vee\ \neg h_1(S_1)\ \vee\ \neg h_2(S_2). \tag{4}
\]

The generated formula has 4,665 variables and 18,334 clauses.  Cadical
1.9.5 returns `UNSAT` (5.88 seconds in the recorded run).  Every auxiliary
gate is encoded in both directions, so this is an exact finite formulation,
not a one-sided relaxation.

It follows immediately from the finite lemma and (2) that no diagonal
`{0,+1,-1}` source realizes `Delta_(8,3)`.  For comparison, the direct
integer PB encoding in
`computations/search_diagonal_signed_n8_relaxed_pb.py` even allows each full
hafnian to be either `+1` or `-1`; its 185,391-variable, 388,345-clause
formula is also `UNSAT` (92.06 seconds).  In that encoding a matching has
exact positive/negative term indicators.  Since

\[
 \#(+)-\#(-)=k
 \quad\Longleftrightarrow\quad
 \#(+)+\#(\text{not }-) = m+k,                            \tag{5}
\]

where `m` is the number of matchings, ordinary exact-cardinality encodings
enforce each desired hafnian value.  A Boolean full-sign selector gates two
fresh encodings for `k=+1` and `k=-1`; one branch is therefore enforced in
every assignment.  A zero selector only implies its exact equality, but the
partition clause requires at least one such selector, which is both sound
and complete.

## 3. Structural consequences of a hypothetical counterexample

For a nonsingular alternating matrix `A` over `F_2`, put

\[
 \mathcal F(A)=\{S\subseteq V:|S|\text{ even and }
                         \operatorname{Pf}A[S]=1\}.       \tag{6}
\]

This is the normal even binary delta-matroid represented by `A`.  Two
elementary Pfaffian identities already impose strong structure.

**Lemma 3.1 (complement and private pivots).**  Suppose nonsingular
`A_0,A_1,A_2` satisfy (3) for every proper even partition.  Then:

1. For distinct `r,s`,

   \[
   \mathcal F(A_r)\cap\mathcal F(A_s^{-1})
                         =\{\varnothing,V\}.              \tag{7}
   \]

2. Define

   \[
   D_r=\{uv:(A_r)_{uv}=(A_r^{-1})_{uv}=1\}.              \tag{8}
   \]

   Every vertex has odd degree in `D_r`.  Moreover, an edge in `D_r`
   occurs in neither `A_s` nor `A_s^{-1}` for `s!=r`.  In particular the
   three `D_r` are pairwise edge-disjoint spanning odd-degree graphs.

3. If `r,s,t` are distinct and `ab` is an edge of `A_r` while `cd` is a
   disjoint edge of `A_s`, then

   \[
   (A_t^{-1})_{ac}(A_t^{-1})_{bd}
   +(A_t^{-1})_{ad}(A_t^{-1})_{bc}=0.                    \tag{9}
   \]

**Proof.**  Jacobi's complementary-principal-minor identity, with signs
irrelevant in characteristic two, says

\[
 \operatorname{Pf}A[V\setminus S]
   =\operatorname{Pf}A\,\operatorname{Pf}A^{-1}[S]
   =\operatorname{Pf}A^{-1}[S].                          \tag{10}
\]

Applying (3) to the two-color partition `S,V\setminus S,empty` proves
(7).  Pfaffian expansion at a fixed vertex `u` gives

\[
 1=\operatorname{Pf}A_r
   =\sum_{v\ne u}(A_r)_{uv}
              \operatorname{Pf}A_r[V\setminus\{u,v\}]. \tag{11}
\]

By (10), the summands equal the indicators of edges `uv` in (8), so every
degree in `D_r` is odd.  Applying (7) in both directions shows that an edge
of `D_r` belongs to neither support associated with another color.

For (9), use the partition `{a,b},{c,d},V\setminus{a,b,c,d}`.  Its first
two Pfaffians are one, so the third is zero.  By (10), the four-vertex
principal Pfaffian of `A_t^{-1}` on `{a,b,c,d}` is zero.  Equation (7)
already makes its `ab` and `cd` entries zero, leaving exactly (9). `QED`

There is also a useful recursive flag.  Expanding a nonzero Pfaffian and
recursing produces an ordered perfect matching `e_1,...,e_m` such that every
residual set

\[
 V,\quad V\setminus e_1,\quad
 V\setminus(e_1\cup e_2),\quad\ldots,\quad\varnothing   \tag{12}
\]

is feasible for that color.  By (7), every proper set in this flag is
infeasible for each other color after taking the complementary inverse.

**Lemma 3.2 (nilpotent pair sums).**  Under the same counterexample
hypothesis, for every permutation `(r,s,t)` of `(0,1,2)` and every nonempty
even `T` one has

\[
 \operatorname{Pf}A_r^{-1}[T]\,
 \operatorname{Pf}(A_s+A_t)[T]=0.                       \tag{13}
\]

Equivalently, if `D_z=diag(z_1,...,z_n)`, then the following multivariate
polynomial is identically constant:

\[
 \operatorname{Pf}\!\left(A_r+
       D_z(A_s+A_t)D_z\right)=1.                         \tag{14}
\]

In particular

\[
                 A_r^{-1}(A_s+A_t)                      \tag{15}
\]

is nilpotent for each `r`.

**Proof.**  In characteristic two, coloring the edges in a Pfaffian
expansion by `s` and `t` gives the minor-convolution identity

\[
 \operatorname{Pf}(A_s+A_t)[T]
 =\sum_{X\mathbin{\dot\cup}Y=T}
       \operatorname{Pf}A_s[X]\operatorname{Pf}A_t[Y],  \tag{16}
\]

where the sum is over even `X,Y`.  If `T` is nonempty and proper and the
first factor in (13) is one, Jacobi says that `A_r[V\setminus T]` is
nonsingular.  Every nonzero summand of (16) would therefore give a forbidden
proper three-color partition.  If `T=V`, all proper splits again vanish;
the two endpoint splits contribute the two constants `1+1=0`.  This proves
(13).

The Pfaffian minor-summation formula and Jacobi give

\[
\begin{aligned}
 \operatorname{Pf}(A_r+D_zQD_z)
  &=\sum_{T\subseteq V}\left(\prod_{v\in T}z_v\right)
       \operatorname{Pf}A_r[V\setminus T]\operatorname{Pf}Q[T]\\
  &=\sum_{T\subseteq V}\left(\prod_{v\in T}z_v\right)
       \operatorname{Pf}A_r^{-1}[T]\operatorname{Pf}Q[T],
\end{aligned}                                             \tag{17}
\]

with `Q=A_s+A_t`; signs disappear over `F_2`.  Equation (13) kills every
term except `T=\varnothing`, proving (14).  Setting every `z_v` equal to one
indeterminate `u` gives `Pf(A_r+u^2Q)=1`.  Substitution by `u^2` is injective
on `F_2[x]`, so `Pf(A_r+xQ)=1`; after squaring and dividing by
`det A_r=1`,

\[
             \det(I+xA_r^{-1}Q)=1.                       \tag{18}
\]

Thus the characteristic polynomial of (15) is `\lambda^n`, and
Cayley--Hamilton proves nilpotence. `QED`

There is a compact operator form, but it also exposes a limitation of a
simultaneous-triangularization strategy.  Put `n=2m` and

\[
 M=A_0+A_1+A_2,\qquad X_r=M^{-1}A_r,\qquad K_r=X_r+I.   \tag{19}
\]

Equation (14), with every diagonal variable set to one, gives
`Pf M=1`.  Since

\[
 A_r^{-1}(A_s+A_t)=A_r^{-1}M+I,
\]

Lemma 3.2 says that `X_r=(I+N_r)^{-1}` is unipotent.  Consequently every
`K_r` is nilpotent, `MK_r=A_s+A_t` is alternating, and

\[
                         K_0+K_1+K_2=0.                 \tag{20}
\]

Thus the `K_r` are self-adjoint for the symplectic form `M`.  Nilpotence
and (20) alone are not enough: for canonical
`M=[[0,I],[I,0]]`, any nonzero alternating matrix `B` gives the square-zero
self-adjoint operator

\[
 K=\begin{pmatrix}0&B\\0&0\end{pmatrix};
\]

taking `K_0=K_1=K` and `K_2=0` satisfies all those operator conditions.
The coordinatewise principal-Pfaffian vanishings remain essential.

In fact, a hypothetical counterexample determines the whole two-parameter
operator pencil.  Expanding a linear combination by its vertex-color
classes gives

\[
 \operatorname{Pf}(x_0A_0+x_1A_1+x_2A_2)
                  =x_0^m+x_1^m+x_2^m.                  \tag{21}
\]

Set

\[
 s=x_0+x_1+x_2,\qquad a=x_0+x_2,\qquad b=x_1+x_2.
\]

Using (19)--(20) in (21), and then squaring, yields

\[
\begin{aligned}
 \operatorname{Pf}\bigl(M(sI+aK_0+bK_1)\bigr)
   &=\Phi_m(s,a,b),\\
 \det(sI+aK_0+bK_1)&=\Phi_m(s,a,b)^2,                  \tag{22}\\
 \Phi_m(s,a,b)
   &:=(s+b)^m+(s+a)^m+(s+a+b)^m.
\end{aligned}
\]

At `s=0` this becomes

\[
 \det(aK_0+bK_1)
  =\bigl(a^m+b^m+(a+b)^m\bigr)^2.                       \tag{23}
\]

The binary form inside the square vanishes identically exactly when `m`
is a power of two.  Hence, if `m` is not a power of two (in particular for
`n=6` and `n=10`), a generic combination `aK_0+bK_1` is invertible over an
extension field.  The two nilpotents can then have no common kernel and
cannot be simultaneously strictly triangularized.  If `m` is a power of
two, (22) reduces to `det(sI+aK_0+bK_1)=s^n`, so every member of the pencil
is nilpotent; this is the only regime in which that direct triangularization
route remains plausible.  Any uniform proof must therefore use the
individual coordinate-partition vanishings, not only the aggregated pencil
identity.

## 4. Uniform target

The natural strengthening is the following binary Pfaffian partition
statement.

> For every even `n>=6`, three nonsingular alternating matrices over `F_2`
> admit a proper even coordinate partition into three nonsingular principal
> restrictions.

It is false at `n=4`: the three perfect-matching matrices in the
one-factorization of `K_4` give exactly the three constant partitions.  For
matrices that themselves are perfect-matching matrices, the statement for
`n>=6` is precisely the known theorem that the union of three perfect
matchings has a fourth, mixed perfect matching.  Lemma 3.1 shows what must
replace edge-disjointness for general alternating matrices.  Turning the
odd private-pivot graphs and the rank-one cross constraints (9) into a
uniform contradiction remains the missing conceptual step.  Lemma 3.2 adds
three mutually constrained nilpotent operators to that prospective
classification; the four-vertex one-factorization realizes the exceptional
case.

There is exact computational evidence through order ten.  The audit
`computations/search_diagonal_mod2_uniform_sat.py` computes all principal
Pfaffians by the shared recurrence

\[
 h_r(S)=\bigoplus_{v\in S\setminus\{u\}}
             (A_r)_{uv}\,h_r(S\setminus\{u,v\}),
 \qquad u=\min S.                                      \tag{24}
\]

It fixes a supported matching of color zero canonically.  Relative to that
matching, the union with a supported color-one matching is classified by
its alternating-cycle lengths, so the exhaustive branches are indexed by
the integer partitions of `n/2`.  This gives three branches at `n=6`, five
at `n=8`, and seven at `n=10`.  All are `UNSAT`.  At `n=10` each branch has
12,294 variables, 54,331 clauses, and all 14,760 proper even ordered
partitions; Kissat 4.0.4 solved the seven branches in 120.12, 135.35,
130.72, 146.62, 147.19, 163.41, and 214.85 seconds.  The symmetry reduction
is exhaustive because a full Pfaffian equal to one contains a supported
perfect matching in each of the first two colors; no support assumption is
made beyond those two fixed supported matchings in a branch.

## 5. Characteristic-free hafnian shadow

Some of the polynomial structure survives before reduction modulo two.
Let `A_r` now be symmetric zero-diagonal edge matrices over an arbitrary
field, write `haf` for the hafnian, and suppose the three full hafnians are
one while every proper partition product vanishes.  The unsigned matching
expansion gives

\[
 \operatorname{haf}(x_0A_0+x_1A_1+x_2A_2)
                  =x_0^m+x_1^m+x_2^m.                  \tag{25}
\]

More strongly, for every permutation `(r,s,t)`,

\[
 \operatorname{haf}\!\left(A_r+
       D_z(A_s+A_t)D_z\right)
       =1+2\prod_{v\in V}z_v.                           \tag{26}
\]

Indeed, the coefficient of `z^T` on the left is

\[
 \operatorname{haf}A_r[V\setminus T]
 \sum_{X\mathbin{\dot\cup}Y=T}
       \operatorname{haf}A_s[X]\operatorname{haf}A_t[Y].
\]

For nonempty proper `T`, every summand is a forbidden mixed partition.  At
`T=V`, the two constant endpoint splits survive and contribute `1+1=2`.
Thus (26) specializes to the constant Pfaffian identity (14) in
characteristic two, but outside characteristic two its top-degree term
prevents the nilpotence argument.

There is a convenient characteristic-free generating algebra for (25).
In the commutative square-zero ring

\[
 R=\mathbb F[z_1,\ldots,z_n]/(z_1^2,\ldots,z_n^2),
\]

one has

\[
 \prod_{i<j}(1+a_{ij}z_i z_j)
   =\sum_{S\text{ even}}\operatorname{haf}A[S],z^S.    \tag{27}
\]

The product for `A+B` is the product of those for `A` and `B`, because all
squares `z_i^2` vanish.  This explains the unsigned minor convolution, but
it supplies no Jacobi-complement or determinant identity analogous to the
Pfaffian one.

A universal signed-edge conversion to Pfaffians is also impossible once
there are at least five vertices.  If signs `sigma_ij` made every induced
hafnian equal its Pfaffian up to a subset-dependent common sign, then for
each `i<j<k<l` the three matching terms would require

\[
 \sigma_{ij}\sigma_{kl}=-\sigma_{ik}\sigma_{jl},\qquad
 \sigma_{ij}\sigma_{kl}= \sigma_{il}\sigma_{jk}.       \tag{28}
\]

Write `sigma_ij=(-1)^{e_ij}`.  Taking both binary equations (28) for the
three quadruples `0123`, `0124`, and `0134` and adding all six makes every
edge variable occur twice, while the three minus signs leave right-hand
side one.  This is the contradiction `0=1`.  Particular sparse supports
may admit Pfaffian orientations, but a signed twist cannot provide a
uniform arbitrary-characteristic replacement for the mod-two reduction.

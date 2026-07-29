# The top collision endpoint is pairwise flexible

## Outcome

The highest three equations of the half-shift hierarchy do not give a
standalone collision obstruction.  On the open scalar chart where every
deleted-pair cofactor of `W` is nonzero, every top-tangent `K` has a unique
pairwise binary correction `q_0`.  There is no compatibility condition
between different pairs at this end.

In particular, for every even `n>=4` there are exact rational examples
satisfying

\[
 H(W)=2^{1-n}Z,
 \qquad {KW^{m-1}\over(m-1)!}=0,
\]

and

\[
 {q_0W^{m-1}\over(m-1)!}
 +{K^2W^{m-2}\over2(m-2)!}=2^{3-n}X_2^{\vee},            \tag{1}
\]

where `X_2^vee` denotes the sum of words with two `x` labels and `z`
everywhere else.  The examples may have `K != 0`.  Their `q_0` deliberately
fails the bottom equation `H(q_0)=2X+Y`, so this does not give a collision
arc.  It proves that any use of the top hierarchy must couple it to the
bottom binary fiber; the top three equations alone neither contradict nor
rigidify it.

## 1. Coordinate form of the top equations

Write

\[
 W=\sum_{i<j}w_{ij}z_iz_j,
 \qquad C^W_{ij}=H_{B\setminus\{i,j\}}(W)\in\mathbb C.
\]

Decompose the unique-binary part of `K` by the binary site and color:

\[
 K_p^a=e_a^{(p)}\sum_{i\ne p}k_{ip}^a z_i.
\]

The coefficient with its sole binary label `a` at `p` in the
`t^{n-1}` equation is exactly

\[
                         \sum_{i\ne p}k_{ip}^aC^W_{ip}=0. \tag{2}
\]

For a binary pair `p,q`, let `B_{pq}^{ab}(K)` be the Hessian contribution
obtained from `K_p^a,K_q^b` and `m-2` copies of `W`.  Equation (1) is

\[
 A_{pq}^{ab}C^W_{pq}+B_{pq}^{ab}(K)
  =2^{3-n}\delta_{a,x}\delta_{b,x}.                      \tag{3}
\]

If all `C^W_pq` are nonzero, (3) simply defines the four binary cells on
each pair independently:

\[
 A_{pq}^{ab}=
 {2^{3-n}\delta_{a,x}\delta_{b,x}-B_{pq}^{ab}(K)
  \over C^W_{pq}}.                                       \tag{4}
\]

Thus the top endpoint has no analogue of the bottom cofactor-quotient
wedge on this open chart: its direct cell spans the whole one-dimensional
two-binary output sector.

## 2. A rational dense family

Put weight one on every scalar edge of `W`, except

\[
 w_{01}={2^{1-n}\over(n-3)!!}-(n-2).                    \tag{5}
\]

Perfect matchings using `01` contribute `(n-3)!! w_01`; those avoiding it
contribute `(n-2)(n-3)!!`.  Hence

\[
                              H(W)=2^{1-n}Z.              \tag{6}
\]

Every deleted-pair cofactor is nonzero.  It is `(n-3)!!` when the deleted
pair is `01` or meets it in one vertex.  For a pair disjoint from `01`, it
is

\[
 (n-5)!!\left(w_{01}+n-4\right)
 =(n-5)!!\left({2^{1-n}\over(n-3)!!}-2\right)\ne0.       \tag{7}
\]

For an explicit nonzero tangent, use only binary color `x` at site zero:

\[
             k_{10}^x=C^W_{02},\qquad
             k_{20}^x=-C^W_{01}.                         \tag{8}
\]

Equation (2) holds by cancellation.  Both cells in (8) meet site zero, so
`K^2=0`.  Formula (4) therefore reduces to the rational dense correction

\[
            A_{pq}^{xx}={2^{3-n}\over C^W_{pq}},
 \qquad     A_{pq}^{xy}=A_{pq}^{yx}=A_{pq}^{yy}=0.       \tag{9}
\]

Equations (5)--(9) prove all three top identities exactly.  They also make
the missing coupling transparent: (9) has no `y` cell, so

\[
                         [Y]H(q_0)=0\ne1.                \tag{10}
\]

The verifier
[`verify_collision_top_endpoint_flexibility.py`](../computations/verify_collision_top_endpoint_flexibility.py)
enumerates every coefficient with `n,n-1,n-2` labels `z` for
`n=6,8,10`, checks all pair cofactors, and checks (10), entirely over the
rationals.  It also enumerates every one-factor support through `n=12` as
an independent audit of Lemma 3.1, and verifies all twelve ranks in (21)
over the rationals.

## 3. A coupled sparse-endpoint obstruction

The bottom equation becomes useful as soon as it restricts the support of
the same `K`.  There is a uniform exact instance.

**Lemma 3.1 (Hamilton bottom, one-factor top).**  Let `n>=6` be even.  If
`q_0` is a least-cell Hamilton base for `2X+Y` and `W` is supported on one
nonzero perfect matching, then the bottom tangent equation and the top
two-binary equation are incompatible.

Explicitly, the hypotheses mean

\[
 q_0=\sum_{uv\in P_x}a_{uv}x_ux_v
       +\sum_{uv\in P_y}b_{uv}y_uy_v,
 \qquad \prod_{e\in P_x}a_e=2,
 \qquad \prod_{e\in P_y}b_e=1,                           \tag{10a}
\]

where all weights are nonzero and `P_x union P_y` is one alternating
Hamilton cycle, and

\[
 W=\sum_{uv\in M}w_{uv}z_uz_v,
 \qquad \prod_{e\in M}w_e=2^{1-n},                       \tag{10b}
\]

where all `w_e` are nonzero and `M` is one perfect matching.  No genericity,
unit-weight normalization, or assumption on how `M` meets the Hamilton
cycle is made.

Let `L union R` be the two shores of the alternating Hamilton cycle.  The
complete bottom tangent classification says that every one-`z` cell of
`K` joins two vertices in the same shore.  Let `M` be the perfect matching
supporting `W`, and write `mu(p)` for the mate of `p` in `M`.

Choose a pair `p,q` which is not an edge of `M`.  Its direct `q_0` term in
the top equation has zero `W` cofactor.  There is only one possible
`K times K` completion by `M`: its two cells have endpoint pairs

\[
                         p\,\mu(q),\qquad q\,\mu(p).      \tag{11}
\]

Both cells in (11) obey the bottom shore restriction precisely when

\[
 \operatorname{shore}\mu(q)=\operatorname{shore}p,
 \qquad
 \operatorname{shore}\mu(p)=\operatorname{shore}q.      \tag{12}
\]

There is always a nonmatching pair for which (12) fails.  If `M` has an
internal edge, take one endpoint `p` and any `q` in the opposite shore;
the first endpoint of that internal edge already violates (12).  If `M`
has no internal edge, all its edges cross the shores; take any two vertices
in one shore.  They are not matched to each other, and both equations in
(12) fail.  On the resulting pair the top all-`x` coefficient is zero,
whereas the target is `2^{3-n}`.

There is an even stronger six-site endpoint fact which does not restrict
`W`.  Each Hamilton shore then has only three vertices.  For a same-shore
binary pair, two bottom-tangent cells contributing to the top Hessian would
have to occupy four distinct vertices of that shore.  This is impossible,
and the direct Hamilton `q_0` cell is absent.  Thus every one of the six
same-shore pair coefficients is zero instead of `1/8`.  In the numerical
least-squares normalization this gives the exact residual cost

\[
                   {1\over2}\,6\left({1\over8}\right)^2
                              ={3\over64}.               \tag{13}
\]

This is the sparse side of an endpoint dichotomy: bottom tangency can kill
the unique top completion term even though neither endpoint equation does
so in isolation.

## 4. Dense `W` cannot be gauge-degenerated to one factor

The rational `W` in (5) also gives an exact obstruction to the most direct
way of reducing the open-cofactor branch to Lemma 3.1.  Every edge of `W`
is nonzero.  Consider a Laurent or Puiseux diagonal gauge on the top local
lines,

\[
                          z_i\longmapsto t^{u_i}z_i,
 \qquad                   \sum_i u_i=0.                  \tag{14}
\]

The last equation is the condition that the top product tensor `Z` retain
nonzero finite weight.  Since every scalar edge is present, a finite limit
requires

\[
                              u_i+u_j\ge0
 \qquad(i<j).                                             \tag{15}
\]

But summing (15) over all pairs gives

\[
       \sum_{i<j}(u_i+u_j)=(n-1)\sum_i u_i=0.             \tag{16}
\]

Every nonnegative summand in (16) is therefore zero.  For `n>=3`, the
relations `u_i+u_j=0` for all pairs force every `u_i=0`.  Thus the complete
support is rigid under every finite diagonal one-parameter degeneration:
not one edge can be removed.

The same conclusion holds for a general Puiseux gauge after taking
valuations.  It also covers the action induced on `W` by the parabolic
local stabilizer of the top line, since only the scalar on that line acts
on the `zz` base.  Hence an all-cofactor top solution is not automatically
gauge-reducible to a one-matching `W`.

This does not rule out a nonlinear deformation inside the scalar hafnian
fiber.  A star-kernel move can reduce the support of `W` while preserving
`H(W)` exactly.  What is missing is a transport theorem which moves the
same `K,q_0` through that deformation while also preserving the bottom
equations.  The dense example proves that such a theorem cannot be replaced
by a target-stabilizer valuation.

## 5. Scalar support descent exists, but top-jet transport can fail

For the scalar base alone there is, in fact, a complete nonlinear support
reduction.

**Lemma 5.1 (scalar hafnian star elimination).**  If `H(W)!=0`, then a
finite sequence of exact affine star-fiber moves takes `W` to a source
supported on one perfect matching, without changing `H(W)`.

Choose a vertex `p` and expand

\[
                         H(W)=\sum_{j\ne p}w_{pj}C^W_{pj}. \tag{17}
\]

Some summand in (17) is nonzero; choose its neighbor `j`, so
`C^W_pj != 0`.  Cofactors in (17) do not depend on any entry in the
`p`-star.  Replace that whole star by

\[
 w'_{pk}=0\ (k\ne j),
 \qquad
 w'_{pj}={H(W)\over C^W_{pj}}.                           \tag{18}
\]

The difference `W'-W` is a star direction and every point on the affine
line has the same hafnian.  At the endpoint, `pj` is forced and

\[
                    H(W)=w'_{pj}H(W|_{B\setminus\{p,j\}}),
\]

so the smaller scalar source has nonzero hafnian.  Repeating (18) on it
terminates after `n/2` steps at one perfect matching.  This proof uses no
genericity and allows zeros and cancellations in the starting `W`.

The lift through `K,q_0` is not formal, even if one ignores the bottom
binary equation.  Return to the rational six-site top solution in Section
2.  At a fixed star, seek a graded affine kernel vector

\[
                         D(r)=D_0+rD_1+r^2D_2,            \tag{19}
\]

where `D_0` has `zz` cells, `D_1` has one binary label, and `D_2` has two.
Preserving all top coefficients through two binary labels is the exact
linear condition

\[
 D(r)\,{(W+rK+r^2q_0)^{m-1}\over(m-1)!}=0\pmod {r^3}.    \tag{20}
\]

On six sites, the matrix of (20) has 73 rows.  Its columns split as five
for `D_0`, twenty for `D_1`, and twenty for `D_2`.  Exact rational row
reduction gives, at every one of the six stars,

\[
 \operatorname{rank}M_{D_0,D_1,D_2}=37,
 \qquad
 \operatorname{rank}M_{D_1,D_2}=32.                     \tag{21}
\]

The five `D_0` columns are therefore independent modulo every possible
`D_1,D_2` correction.  Every solution of (20) has `D_0=0`: not one
nonzero scalar star move lifts through this top two-jet.

This is an exact counterexample to transporting Lemma 5.1 merely from the
top equations.  Its `q_0` has no all-`y` coefficient, so it does not refute
a transport lemma which crucially uses `H(q_0)=2X+Y`; that stronger coupled
statement is precisely the remaining possibility.

## 6. Remaining coupled question

The useful high-order problem is therefore not whether `(W,K,q_0)` can
solve the top three equations; generically it can.  It is whether the same
pairwise-defined `q_0` can also satisfy

\[
 H(q_0)=2X+Y,\qquad dH_{q_0}(K)=0.                        \tag{22}
\]

and then the intervening Bianchi equations.  Numerical probing with the
least-cell Hamilton `q_0` and its complete bottom tangent kernel did not
find a top-end solution, but that observation is not used as a theorem.
The exact obstruction, if one exists, must be a compatibility between the
two endpoint cofactor geometries in (3) and (22).

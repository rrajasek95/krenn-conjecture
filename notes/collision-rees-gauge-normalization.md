# Exact Rees gauges for the color collision

## Outcome

The apparently singular substitution

\[
                         z_i\longmapsto z_i+{a_i\over t}x_i
\]

is completely regular on the Rees source obtained by first replacing
`z_i` by `t z_i`.  It produces an explicit family of binary base points,
and every point away from one elementary discriminant can be centered and
rescaled to the standard half-shift two-jet **without moving the binary
base**.  Thus this construction gives a valid way to move a hypothetical
collision lift inside a particular algebraic family; it is not the
invalid arbitrary base-fiber transport discussed elsewhere.

There is also a sharp limitation.  A branch-stabilizer gauge written in
collision coordinates contains a second term which is often omitted, and
its finite orbit closure need not approach a least-cell binary base.  The
exact four-site three-one-factor source is already rigid in this sense:
all six of its binary cells survive every finite branch-stabilizer
degeneration.  Literal shears can delete one of those cells only on the
discriminant where one entire branch product vanishes, exactly where the
collision second fundamental form loses its nondegenerate complete-pair
shape.  Consequently singular Rees gauges by themselves do not prove a
least-support normalization.

Throughout, work in the squarefree site algebra and write

\[
 H(Q)=Q^{n/2}/(n/2)!,\qquad
 U=\prod_i u_i,\quad V=\prod_i v_i,\quad Y=\prod_i y_i.
\]

Assume hypothetically that

\[
                         H(Q)=U+V+Y.                       \tag{1}
\]

Put

\[
             u_i=x_i-z_i/2,\qquad v_i=x_i+z_i/2.          \tag{2}
\]

## 1. The exact multi-parameter Rees family

First make the collision substitution `z_i -> t z_i` in `Q`.  Since `Q`
is quadratic, the resulting source has the exact form

\[
                       Q(t)=q_0+tZ+t^2W.                  \tag{3}
\]

Now apply the singular-looking shear `z_i -> z_i+a_i x_i/t`.  In the
composite substitution the old `z_i` is simply replaced by
`a_i x_i+t z_i`, so no negative power of `t` occurs in the source.  Set

\[
 p_i=1-a_i/2,\qquad q_i=1+a_i/2,\qquad
 P=\prod_i p_i,\quad R=\prod_i q_i,\quad C=P+R.          \tag{4}
\]

Functoriality of the matching expansion gives the exact identity

\[
\boxed{
 H(Q_a(t))=Y+
   \prod_i(p_i x_i-tz_i/2)+
   \prod_i(q_i x_i+tz_i/2).}                             \tag{5}
\]

In particular,

\[
 Q_a(t)=q_a+tZ_a+t^2W,\qquad
 H(q_a)=Y+C X,                                           \tag{6}
\]

where `q_a` is obtained directly from `Q` by putting `z_i=a_i x_i`.
More generally, putting `z_i=s_i x_i` gives

\[
 H(q(s))=Y+\left[
   \prod_i(1-s_i/2)+\prod_i(1+s_i/2)
                         \right]X.                        \tag{7}
\]

Equations (5)--(7) hold for independent parameters at every site.  They
are identities, not formal lifting assertions.

## 2. Centering a nondegenerate shear

Suppose

\[
                         C\ne0,\qquad PR\ne0.             \tag{8}
\]

The latter condition implies every `p_i q_i` is nonzero.  Factor the two
branches in (5).  Their local slopes are

\[
                         -{1\over2p_i},\qquad {1\over2q_i}.
\]

Make the regular, identity-at-`t=0` local change

\[
 x_i\longmapsto x_i+c_i t z_i,qquad
 c_i={P/p_i-R/q_i\over 2C}.                              \tag{9}
\]

The two centered slopes become

\[
             r_i^-=-{R\over C p_iq_i},\qquad
             r_i^+={P\over C p_iq_i}.                    \tag{10}
\]

Hence the coefficient with one `z` is zero at every site, while the
coefficient with `z` at distinct sites `i,j` is

\[
                  P r_i^-r_j^-+Rr_i^+r_j^+
                    ={PR\over C p_iq_i p_jq_j}.           \tag{11}
\]

Choose a square root and additionally put

\[
 z_i\longmapsto
       \kappa_i z_i,qquad
 \kappa_i=p_iq_i\sqrt{C\over 2PR}.                       \tag{12}
\]

Then every coefficient in (11) becomes `1/2`.  Thus, through order two,

\[
 H(\widetilde Q_a(t))
        =Y+C X+{t^2\over2}X_2+O(t^3),                    \tag{13}
\]

The normalization is actually exact to every order.  Put

\[
 \sigma=\sqrt{C\over2PR},\qquad
 \alpha=-{R\sigma\over C},\qquad
 \beta={P\sigma\over C}.                                \tag{13a}
\]

The two local factors after (9),(12) are

\[
                  p_i(x_i+\alpha t z_i),\qquad
                  q_i(x_i+\beta t z_i).
\]

Consequently

\[
 H(\widetilde Q_a(t))
   =Y+P\prod_i(x_i+\alpha t z_i)
       +R\prod_i(x_i+\beta t z_i),                       \tag{13b}
\]

where

\[
                 P\alpha+R\beta=0,\qquad
                 P\alpha^2+R\beta^2={1\over2}.           \tag{13c}
\]

Thus its first derivative is zero.  Most importantly, (9) is the identity
and (12) only rescales `z` at `t=0`; therefore the binary base remains
**exactly** `q_a`.

On the hypersurface `C=2`, (13) is precisely the half-shift collision
two-jet used in the least-cell obstruction.  For arbitrary nonzero `C`,
one may first normalize the `X` coefficient by local `x` scalings and
then apply the same calculation with the correspondingly rescaled `z`
coordinates.

This proves the valid conditional reduction:

> If the nondegenerate locus `C(a)=2`, `P(a)R(a) != 0` contains a
> least-cell base (or any other base stratum already ruled out by a
> collision two-jet argument), then the hypothetical ternary source is
> impossible.

What is not proved is that this explicit `(n-1)`-dimensional family meets
such a stratum.

## 3. The simple discriminant is a rooted-star jet

Suppose exactly one factor of the first product vanishes.  After exchanging
the two branches, write

\[
 p_r=0,\qquad p_jq_j\ne0\ (j\ne r),\qquad q_r=2,
\]

and put

\[
 A=\prod_{j\ne r}p_j,\qquad B=\prod_{j\ne r}q_j,\qquad
 K={A\over B}.                                           \tag{18a}
\]

Straighten the surviving branch by using the regular local coordinates

\[
 X_i=q_i x_i+t z_i/2.
\]

Formula (5) becomes

\[
 H(Q_a(t))=Y+\prod_iX_i
   -{Kt\over2}z_r\prod_{j\ne r}
       \left(X_j-{t\over p_j}z_j\right).                 \tag{18b}
\]

Finally replace \(X_r\) by \(X_r+Kt z_r/2\).  This kills the complete
first derivative and gives the exact centered identity

\[
\boxed{
 H(\widehat Q_a(t))=Y+X+
 {Kt\over2}z_r\left\{
   \prod_{j\ne r}X_j-
   \prod_{j\ne r}\left(X_j-{t\over p_j}z_j\right)
                         \right\}.}                      \tag{18c}
\]

Its first nonconstant term is

\[
 {Kt^2\over2}\sum_{j\ne r}{1\over p_j}\,
 z_rz_j\prod_{k\ne r,j}X_k.                             \tag{18d}
\]

Every displayed coefficient is nonzero.  Thus a simple point of the
discriminant does not give the complete-pair tensor \(X_2\); it gives a
nonzero **rooted star** centered at the unique killed site.  If several
factors vanish, the first normal term is instead supported on subsets
containing every killed site.

There is a second useful exact view of the same boundary.  Before
straightening, rescale only the root variable by \(z_r\mapsto z_r/t\).
The composite substitution in the original source is

\[
 z_r^{\rm old}=2x_r+z_r,\qquad
 z_j^{\rm old}=a_jx_j+t z_j\quad(j\ne r),
\]

so the transformed source has no pole.  At \(t=0\) its output is

\[
 Y+\left\{2B\,x_r+{B-A\over2}z_r\right\}
                   \prod_{j\ne r}x_j.                   \tag{18e}
\]

This lies in a two-dimensional local subspace at every site.  Projecting
the root onto the span of the displayed vector and \(y_r\) therefore gives
an ordinary exact binary GHZ source.  This is a genuine smaller-palette
specialization, but it gives no support bound: its edge matrices are
arbitrary projections of the original ones.

### 3.1 The rooted star is excluded on the first active excess stratum

The low-support theorem can be strengthened to include (18d).

**Rooted-star lemma.**  Let \(n\ge6\) be even.  Let \(q_0\) be an
inclusion-minimal binary source for a two-term GHZ tensor with at most
\(n+2\) scalar cells.  There are no graded jets \(Z,W\) with

\[
\begin{aligned}
 dH_{q_0}(Z)&=0,\\
 dH_{q_0}(W)+\tfrac12d^2H_{q_0}(Z,Z)
 &=\sum_{j\ne r}c_jz_rz_jX_{\widehat{rj}},
 \qquad c_j\ne0.                                        \tag{18f}
\end{aligned}
\]

For \(n\) cells, choose a second vertex on the same shore of the
alternating Hamilton cycle as \(r\).  The deleted-pair cofactor and the
Hessian restricted to the two tangent kernels both vanish, exactly as in
the least-cell collision proof, while (18f) is nonzero.

For \(n+2\) cells, use the classification in
[color-collision-n-plus-two-obstruction.md](color-collision-n-plus-two-obstruction.md).
There is one monochromatic four-cycle switch.  The following
frozen-edge cover is the only extra observation needed.

* If the switched factor is \(x\), let \(C\) be its four switch vertices
  and \(T\) the other vertices.  The set \(T\) is nonempty.  Every pair in
  \(C\times T\) has zero direct \(W\) cofactor and zero Hessian on the
  complete tangent kernels.
* If the switched factor is \(y\), use the canonical labels (13)--(14) of
  the cited note.  Every pair \(0v\), except \(v=1,2r-1\), is frozen, and
  every pair \(1v\), except \(v=0,2r-2\), is frozen.

Here is a direct forced-matching proof.  In the first case, let \(t^*\) be
the shared \(x\)-matching mate of \(t\in T\).  After deleting
\(c\in C,t\), an all-\(x\) Hessian term must use \(t^*\) as one tangent
endpoint and one switch vertex as the other.  Up to the common product of
the forced tail edges, its coefficient factors as

\[
 \alpha_{t,t^*}L_c(\alpha_c)
       +\alpha_{c,t^*}L_c(\alpha_t).                     \tag{18g}
\]

The all-\(x\) tangent equation gives \(\alpha_{t,t^*}=0\).
For the second factor, color successively by \(y\) the edges of the
unique alternating arc from \(t^*\) to \(c\), and by \(x\) the complement.
Every tail edge is then forced and the remaining four-site expansion is
exactly \(L_c(\alpha_t)\); the tangent equation gives
\(L_c(\alpha_t)=0\).  This proves the first bullet.  Choosing either of
the two \(x\) factors as reference supplies the required alternating arc
for each of the four switch vertices.

In the second case, write \(v'\) for the selected \(x\)-mate of \(v\).
For a nonexceptional pair \(0v\), the all-\(x\) coefficient is

\[
 \alpha_{0,1}\alpha_{v,v'}
       +\alpha_{0,v'}\alpha_{v,1}.                       \tag{18h}
\]

The first product vanishes by the two all-\(x\) tangent equations.
Alternating step colorings along the two arcs from the switched rectangle
to \(vv'\) force at least one factor in the second product to vanish
(both vanish when both switched matching products are nonzero).  At a
matching-product endpoint, use the surviving switched matching as the
reference arc.  This is precisely the path version of the two step
colorings in Section 4 of the cited note.  This proves the assertion for
\(0v\); shifting the starting selected \(x\) edge from \(01\) to its
neighbor gives the stated assertion for \(1v\).  The two omitted pairs are
exactly the ones for which that alternating arc terminates inside the
switched rectangle.

The frozen pairs cover every possible root.  In the first case pair a
switch root with a tail vertex and a tail root with a switch vertex.  In
the second case, pair a root with \(0\), unless it is \(0,1\), or
\(2r-1\); use respectively \(2r,2r-1\), or \(1\) in those three cases.
The right side of (18f) is nonzero on that pair, which proves the lemma.

The verifier
[verify_rooted_boundary_collision.py](../computations/verify_rooted_boundary_collision.py)
computes the complete tangent kernels and checks this frozen-edge cover
for every active switch position at \(n=6,8\) and a representative
ten-site position.  The proof above is uniform; the finite audit is an
independent check rather than an induction step.

The dense rational six-site chart from
[dense-diagonal-collision-spin-obstruction.md](dense-diagonal-collision-spin-obstruction.md)
also rejects every rooted star.  Its homogeneous first kernel has one
coordinate `t_i` at each vertex.  Eliminating all direct `W` cells gives

\[
 t_it_j=c_{ij},\qquad
 c_{ij}\ne0\ \hbox{if }r\in\{i,j\},\qquad
 c_{ij}=0\ \hbox{otherwise}.                             \tag{18j}
\]

Two root edges force `t_r,t_i,t_j` all nonzero, while the nonroot edge
`ij` forces `t_it_j=0`.  This is an immediate contradiction.  The verifier
performs the complete 240-equation elimination for all six choices of the
root.  The same argument works throughout the open one-dimensional-kernel
chart wherever the marked pair quotients remain nonzero; rank-drop boundary
divisors require their own equations.

### 3.2 Why inactive boundary cells still block normalization

The four-site source (18) below gives the sharp warning.  Put
\(a=(2,0,0,0)\), straighten the surviving branch, and center as above.
The exact target is

\[
 Y+X+{t\over2}z_0\left\{
       \prod_{j=1}^3x_j-\prod_{j=1}^3(x_j-tz_j)
                         \right\}.                       \tag{18i}
\]

Its second term is the full rooted star with coefficient \(1/2\).
The binary base has five cells: the four-cell Hamilton realization plus
one \(xx\) cell with zero base cofactor.  Deleting that inactive cell gives
the global least-cell base, but destroys the rooted-star jet.  Thus even
the discriminant family does not justify passing to an inclusion-minimal
base underneath the jet.  This is the boundary form of the exact
base-star transport counterexample.

## 4. What a branch stabilizer actually does

For `t != 0`, let

\[
 u_i(t)=x_i-tz_i/2,\qquad v_i(t)=x_i+tz_i/2.
\]

The diagonal branch stabilizer scales these by

\[
 u_i(t)\mapsto\lambda_i u_i(t),\quad
 v_i(t)\mapsto\mu_i v_i(t),\quad
 y_i\mapsto\nu_i y_i,                                   \tag{14}
\]

with

\[
                 \prod_i\lambda_i=\prod_i\mu_i
                    =\prod_i\nu_i=1.                    \tag{15}
\]

In collision coordinates (14) is

\[
\boxed{
\begin{aligned}
 x_i&\mapsto {\lambda_i+\mu_i\over2}x_i
             +{t(\mu_i-\lambda_i)\over4}z_i,\\
 z_i&\mapsto {\mu_i-\lambda_i\over t}x_i
             +{\lambda_i+\mu_i\over2}z_i,\\
 y_i&\mapsto\nu_i y_i.
\end{aligned}}                                          \tag{16}
\]

The `1/t` shear in the second line is therefore always accompanied by the
`t z_i` term in the first line.  Dropping that companion term changes the
target to (5); it is not an action of the target stabilizer.  Under the
complete transformation (16), the target is preserved exactly, and its
binary base is the restriction

\[
               u_i=\lambda_i x_i,\quad
               v_i=\mu_i x_i,\quad y_i=\nu_i y_i.       \tag{17}
\]

Thus finite or one-parameter versions of (16) give a genuine
lift-preserving orbit, but only that orbit; they do not move freely in the
whole binary fiber.

## 5. Exact obstruction: the four-site orbit is support-rigid

Take the exact `K_4` source

\[
\begin{aligned}
 Q={}&u_0u_1+u_2u_3
     +v_0v_3+v_1v_2\\
    &+y_0y_2+y_1y_3.                                    \tag{18}
\end{aligned}

The three one-factors are the three perfect matchings of `K_4`, hence
`H(Q)=U+V+Y`.  Its branch-stabilizer collision base (17) has the six cells

\[
\begin{array}{c|c}
01;xx&\lambda_0\lambda_1\\
23;xx&\lambda_2\lambda_3\\
03;xx&\mu_0\mu_3\\
12;xx&\mu_1\mu_2\\
02;yy&\nu_0\nu_2\\
13;yy&\nu_1\nu_3.
\end{array}                                               \tag{19}
\]

Consider arbitrary Laurent or Puiseux one-parameter gauges satisfying
(15), and suppose every coefficient in (19) has a finite limit.  The
products in each complementary pair are identically one:

\[
\begin{aligned}
 (\lambda_0\lambda_1)(\lambda_2\lambda_3)&=1,\\
 (\mu_0\mu_3)(\mu_1\mu_2)&=1,\\
 (\nu_0\nu_2)(\nu_1\nu_3)&=1.                           \tag{20}
\end{aligned}

Consequently neither member of any pair can tend to zero.  Every finite
limit therefore retains all six cells.  Yet the binary fiber `2X+Y` has
a four-cell least-cell point.  Hence even an exact lift-preserving
stabilizer orbit closure need not contain a least-cell base.

Literal shears do not repair this example away from the discriminant.
For (18), the four `xx` coefficients at the sheared base are

\[
                 p_0p_1,\quad p_2p_3,\quad
                 q_0q_3,\quad q_1q_2.                  \tag{21}
\]

If `PR != 0`, all four are nonzero, so the base again has six cells.  If
one is deleted, then some `p_i` or `q_i` is zero, and hence `PR=0`.
The normalization (12) is then singular.  This is not merely a bad choice
of formula.  If, for example, `p_i=0` while all `q` factors are nonzero,
then after straightening the surviving `q` product, every quadratic normal
coefficient on a pair avoiding `i` is zero: the `p` product still contains
its zero factor, while the `q` product is a single decomposable arc.  With
several zero factors its first nonzero normal term is supported only on
pairs containing all of them.  The same statement holds with `p,q`
interchanged, and if both products vanish the quadratic support is the
union of these proper pair stars.  For `n>=4` this cannot be changed by
invertible sitewise rescaling into the complete nonzero pair tensor `X_2`.
Thus the support reduction has discarded a branch at the binary base and
cannot be fed into the nondegenerate half-shift obstruction.

For example, the rational choice

\[
                         a=(-6/5,0,0,0)                  \tag{22}
\]

has `P=8/5`, `R=2/5`, and `C=2`.  Formulas (9),(12) are
regular and turn the two branch slopes into the site-independent values
`-1/4` and `1`; therefore the constant, linear, and quadratic target
coefficients are respectively `2`, `0`, and `1/2` on every pair.  All six
cells (21) remain nonzero.  Moving (22) to a zero of one cell makes either
`P` or `R` zero at exactly the same time.

## 6. Consequence for a normalization proof

The Rees family supplies a legitimate and potentially useful replacement
for arbitrary base transport: one may minimize support **inside**

\[
        \{q_a:C(a)=2,\ P(a)R(a)\ne0\}                   \tag{23}

or inside its full branch-stabilizer orbit, and every attained point still
has a normalized collision two-jet.  However, neither (5) nor (16)
implies that this restricted orbit meets the global least-cell locus, or
even an `n+2`-cell locus.  Any proof of that additional assertion needs a
new support theorem using the equations of the hypothetical source.  A
bare singular-gauge argument is blocked by (18)--(21).

The exact audit
[`verify_collision_rees_gauge.py`](../computations/verify_collision_rees_gauge.py)
checks the multi-parameter target formula, the centering identities, the
rational nontrivial point (22), the complete `K_4` matching expansion, and
the six-cell support-rigidity products.

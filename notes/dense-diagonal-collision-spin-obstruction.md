# A dense six-site collision fiber has a signed-cycle obstruction

## Outcome

The collision obstruction is not confined to sparse Hamilton bases.  There
is an exact rational binary base on six sites with fifteen active diagonal
cells and a twelve-edge dense `x`-sector.  Its complete first-jet fiber has
dimension six.  Eliminating every possible `Q_2` correction from the second
jet gives the signed product system

\[
                         4t_it_j=\epsilon_{ij}\quad(i<j), \tag{1}
\]

and four of these equations have an explicit Nullstellensatz contradiction.
This supplies a second, genuinely different exact model for the conjectured
universal implication

\[
        \text{collision two-jet}\quad\Longrightarrow\quad\bot.
\]

The mechanism is a frustrated sign pattern on the six vertex-kernel
parameters, rather than a coefficient frozen termwise by sparse support.

## 1. The dense rational binary base

Partition the vertices into blocks

\[
                        A=01,\qquad B=23,\qquad C=45
\]

and let

\[
                         H=\begin{pmatrix}1&1\\1&-1\end{pmatrix}.
\]

Put no `xx` cell inside a block.  On the three cross-blocks put the `xx`
matrices

\[
                         X_{AB}=-\frac12H,qquad
                         X_{AC}=H,qquad X_{BC}=H.         \tag{2}
\]

Finally put unit `yy` cells on `01,23,45`, and no other binary cells.

Each matrix in (2) has permanent zero.  Therefore every mixed coefficient
whose `y`-vertices form one or two of the three block edges vanishes.  All
other mixed colorings have no supported `y`-matching.  The full `x`
hafnian is

\[
                             \operatorname{Haf}(X)=2,     \tag{3}
\]

while the sole all-`y` matching has weight one.  Thus this is an exact
realization of `2X+Y`.  Unlike the Hamilton base, all twelve cross-block
`xx` cells are nonzero.

## 2. The exhaustive first-jet fiber

There are sixty possible one-`z` cells.  The 192 first-jet coefficient
equations have exact rank 54, hence nullity six.  Half of the infinitesimal
basis change `x -> x+t z` is a particular solution.  A convenient kernel
basis has one parameter `t_i` for each vertex.  Its nonzero entries are:

\[
\begin{array}{c|rrrr}
t_0&(02;zx)/2&(03;zx)/2&(04;zx)&(05;zx)\\
t_1&-(12;zx)/2&(13;zx)/2&-(14;zx)&(15;zx)\\
t_2&(02;xz)/2&(12;xz)/2&(24;zx)&(25;zx)\\
t_3&-(03;xz)/2&(13;xz)/2&-(34;zx)&(35;zx)\\
t_4&-(04;xz)&-(14;xz)&(24;xz)&(34;xz)\\
t_5&(05;xz)&-(15;xz)&-(25;xz)&(35;xz).
\end{array}                                               \tag{4}
\]

Here `(uv;zx)` uses the displayed increasing endpoint order.  The exact
rank and the fact that (4), together with the particular solution, solves
all 192 equations prove that this is the complete affine first fiber; no
one-`z` direction has been omitted.

## 3. Exact elimination of the second jet

For each of the 240 colorings with exactly two `z` labels, form its second
coefficient.  It is quadratic in `t_0,...,t_5` and linear in the fifteen
arbitrary `zz` entries of `Q_2`.  Exact rational row reduction in the
linearized monomials

\[
       1,\quad t_i,\quad t_it_j\ (i\le j),\quad (Q_2)_{uv}
\]

has rank 30.  Eliminating all fifteen `Q_2` columns leaves the following
fifteen independent equations:

\[
\begin{array}{c|rrrrrrrrrrrrrrr}
ij&01&02&03&04&05&12&13&14&15&23&24&25&34&35&45\\ \hline
\epsilon_{ij}
 &+&+&+&-&-&+&+&-&-&+&+&+&+&+&+.
\end{array}                                               \tag{5}
\]

That is, the equation in column `ij` is exactly

\[
                         F_{ij}:=4t_it_j-\epsilon_{ij}=0. \tag{6}
\]

This elimination includes every mixed `x/y` second coefficient and every
possible direct `Q_2` correction, not only the all-`x/z` sector.

The four columns `01,02,14,24` already contradict one another.  Put

\[
 A=F_{01}-F_{02}=4t_0(t_1-t_2),\qquad
 B=F_{14}-F_{24}=4t_4(t_1-t_2)+2.
\]

Then the following is a polynomial identity:

\[
 \boxed{
 1=2t_1\bigl[t_0(F_{14}-F_{24})
                    -t_4(F_{01}-F_{02})\bigr]-F_{01}.}   \tag{7}
\]

Hence (6) has no solution even over an algebraic closure.  Equation (7) is
a four-equation exact certificate, not a real-sign or numerical argument.

The verifier
[`verify_dense_diagonal_collision_obstruction.py`](../computations/verify_dense_diagonal_collision_obstruction.py)
checks all 64 base coefficients, the exhaustive rank-54 first family, all
240 second equations, the exact elimination table (5), and identity (7).
The companion numerical search script independently converges to a
strictly positive residual from every tested start.

## 4. Possible invariant suggested by the example

The kernel in (4) is vertex-indexed, and second-order compatibility asks
whether the edge signs (5) are an outer product of vertex labels.  Such an
outer-product sign pattern has trivial product around every cycle.  The
displayed pattern is frustrated.  A universal proof might therefore seek
a binary spin-flip or discriminant construction which:

1. canonically quotients the first kernel by integrable/gauge directions;
2. associates pair constraints to the second fundamental form modulo the
   `Q_2` image; and
3. shows that a binary base for `2X+Y` necessarily produces a frustrated
   cycle when `n>=6` unless it is already in the Hamilton half-coefficient
   chart.

The next section extends this mechanism to the full dense diagonal
one-`y`-factor chart.  Bases with off-diagonal binary cells remain outside
its scope.

## 5. A Pluecker obstruction on the whole generic dense diagonal chart

The preceding sign table is one point of a three-parameter chart.  The
same calculation has a coordinate-free interpretation as failure of
rank-one tetrads.

Here is the abstract form used below.  Suppose the first tangent kernel
splits into one-dimensional vertex sectors `L_i`, and after quotienting the
two-`z` sector by the direct `Q_2` cofactor line, the pair equation on
`L_i tensor L_j` is a nonzero bilinear equation with nonzero target class.
Choose temporary bases of the `L_i`.  It has the scalar form

\[
                              t_it_j=c_{ij}.               \tag{7a}
\]

Changing the basis of `L_i` rescales every `c_ij` incident with `i` by the
same inverse factor.  Consequently

\[
             \Pi_{ijkl}=c_{ij}c_{kl}-c_{ik}c_{jl}         \tag{7b}
\]

is, up to one common nonzero scale, a coordinate-independent section of
the four dual kernel lines.  If vertex tangents `t_i` solve every pair
equation, then every `Pi_ijkl` vanishes.  Conversely, over an algebraically
closed field, nonzero edge labels on a complete graph satisfying all these
tetrads have the form `c_ij=t_it_j`: choose a square root of
`c_01 c_02/c_12`, then recover the other `t_i` from the edges incident with
vertex zero.  Thus (7b) is exactly the Pluecker/rank-one obstruction in a
one-dimensional-kernel chart, not merely a choice of signs.

Keep the three two-vertex blocks `A=01,B=23,C=45`, assume every cross-block
`xx` cell is nonzero, and keep the unit `yy` block matching.  The mixed
binary equations say that each cross-block `2 by 2` matrix has permanent
zero.  Every such dense matrix has the form

\[
       M_{ij}=r_i s_j(-1)^{ij}.
\]

After diagonal changes of the six `x` coordinates and harmless
redistribution of the three block-pair scalars, the `x` matrices have the
normal form

\[
 \lambda H,\qquad
 \operatorname {diag}(x,1)H,\qquad
 \operatorname {diag}(y,1)H\operatorname {diag}(z,1),     \tag{8}
\]

where `x,y,z` are nonzero and `lambda` normalizes the full hafnian to two.
Before this normalization the hafnian is

\[
 S=-xyz-xy+xz-x-yz+y-z-1.                                \tag{9}
\]

Thus `S` is nonzero.  On the open chart

\[
                   (x^2+1)(y^2+1)(z^2+1)\ne0,             \tag{10}
\]

the complete first kernel is again one-dimensional at every vertex.
Eliminating `Q_2` gives equations

\[
                         t_it_j=c_{ij}\quad(i<j).          \tag{11}
\]

If some `c_ij` is zero, (11) is already impossible: the within-block
equations are

\[
                 t_0t_1=x/4,quad t_2t_3=y/4,quad
                 t_4t_5=z/4,                              \tag{12}
\]

so every `t_i` is nonzero.  We may consequently suppose all `c_ij` are
nonzero.

For four distinct vertices, (11) forces the Pluecker/tetrad identity

\[
                     c_{ij}c_{kl}-c_{ik}c_{jl}=0.          \tag{13}
\]

Three such tetrads, one centered at each two-vertex block, factor as

\[
\begin{aligned}
D_A={}&-{U V H_A G\over
 64(x^2+1)(y^2+1)(z^2+1)},\\
D_B={}& {U W H_B G\over
 64(x^2+1)(y^2+1)(z^2+1)},\\
D_C={}&-{V W H_C G\over
 64(x^2+1)(y^2+1)(z^2+1)},                                \tag{14}
\end{aligned}
\]

where

\[
\begin{aligned}
U&=xy+x-y+1,&V&=xz-x-z-1,&W&=yz-y+z+1,\\
G&=xyz+xy-xz+x+yz-y+z+1=-S,\\
H_A&=xyz-xy+xz+x+yz+y-z+1,\\
H_B&=xyz-xy-xz-x-yz-y-z+1,\\
H_C&=xyz+xy+xz-x-yz+y+z+1.
\end{aligned}                                             \tag{15}
\]

The factors `U,V,W` occur in numerators of individual cross-block
constants `c_ij`.  Their vanishing was excluded immediately after (12),
and `G` is nonzero by (9).  Hence (13)--(15) force

\[
                         H_A=H_B=H_C=0.                   \tag{16}
\]

This is incompatible with `S\ne0` on (10), by an elementary two-case
calculation.  Indeed,

\[
                         H_A-H_B=2(x+y)(z+1).              \tag{17}
\]

If `z=-1`, then `H_A=-2(xy-1)`, `H_C=-2(x-y)`, and
`S=-2(x-y)=0`.  Otherwise (17) gives `y=-x`; now

\[
 H_A=-(x^2+1)(z-1),qquad
 H_C|_{z=1}=2(1-x^2),qquad
 S|_{y=-x,z=1}=2(x^2-1).
\]

Condition (10) forces `z=1`, after which (16) again gives `S=0`, a
contradiction.  This proves:

**Generic dense-diagonal lemma.**  No six-site collision two-jet exists
on the dense diagonal one-`y`-factor chart (8) away from the three
discriminant divisors in (10).

The symbolic script
[`derive_generic_dense_spin.py`](../computations/derive_generic_dense_spin.py)
derives all fifteen constants in (11), factors (14), and independently
checks that the full localized tetrad ideal is the unit ideal.

The divisors in (10) are genuine rank-drop loci, so division by them cannot
be hidden.  They can nevertheless be closed exactly.  By block symmetry it
is enough to put `x^2=-1`; the two signs give conjugate calculations, so
write `x=i`.  Now

\[
                         S=(-1-i)(y-i)(z+i).              \tag{18}
\]

On the open part `(y+i)(z-i)\ne0`, exact elimination in the single pair
sector `{2,4}` gives the literal equation `1=0`.  On the remaining
intersections the same happens as follows:

\[
\begin{array}{c|c}
y=-i,\ z\ne i&\text{pair }\{0,4\},\\
z=i,\ y\ne-i&\text{pair }\{0,2\},\\
y=-i,\ z=i&\text{pair }\{0,2\}.
\end{array}                                               \tag{19}
\]

These are exact row reductions of the sixteen binary second coefficients
in the indicated two-`z` sector, including its direct `Q_2` variable.  No
tangent parameter remains in the constant row.  The calculation for
`x=-i` is identical after conjugation, and permutation of the three blocks
handles the `y` and `z` discriminants.

For example, at `(x,y,z)=(i,-i,i)` all three naive covariance minors vanish
while `S=-4-4i` is nonzero.  The complete 240-equation system drops from
rank 30 to rank 19, but every cross-block pair sector already contains
`1=0`.  Thus the discriminant locus is obstructed by a different component
equation, not by a limiting use of (14).

Combining (14)--(19) proves:

**Dense-diagonal theorem.**  No six-site collision two-jet exists for any
dense diagonal binary base whose `y`-sector is a single perfect matching.

This covers every nonzero point of that diagonal chart, but not vanishing
cross-block cells (boundary strata) or arbitrary off-diagonal binary
entries.

Nor can (7b) be promoted to a bare four-site axiom without its marked
cofactor quotients and one-dimensional kernel hypothesis.
`four-vertex-collision-frustration-countermodel.md` gives an exact switched
six-site base for which all six quotient pair equations on the four-site
core are simultaneously soluble; only equations coupling the core to the
two external vertices fail.  Complement data is therefore essential in
any extension beyond this dense chart.

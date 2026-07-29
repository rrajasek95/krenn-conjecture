# The aligned two-plane boundary is excluded in every zero pattern

## 1. Result

This note completes the residual `dim(P intersection S)=2` locus left in
[`all-dead-corank-two-product-geometry.md`](all-dead-corank-two-product-geometry.md).
Let

\[
 P=\langle p_0,p_1,p_2\rangle ,\qquad
 S=\langle s_0,s_1,s_2\rangle ,\qquad
 U=P+S .                                                   \tag{1}
\]

Thus `dim P=dim S=3`, `dim U=4`, the six off-diagonal products span a
two-space, every named row and column pair is a basis of that two-space,
and every named vector reaches at least three sites.  Suppose also that
the intrinsic ordinary relation belongs to the zero-diagonal relation
four-plane.  Then this configuration is impossible.

The chart in which all three quotient coefficients are nonzero is treated
in Propositions 9.1--9.2 of
[`all-dead-corank-two-product-reduction.md`](all-dead-corank-two-product-reduction.md).
The point here is to retain, rather than silently discard, every zero
pattern on the boundary of that chart.

## 2. The only missing normal forms

Write `N` for the rank-two intrinsic relation.  The calculation

\[
 S=PA+t v^{\mathsf T},\qquad
 N=[u]_\times A^{-\mathsf T},\qquad u=A^{-\mathsf T}v,
                                                               \tag{2}
\]

and `diag N=0` gives

\[
                    A^{-\mathsf T}=D+ur^{\mathsf T}            \tag{3}
\]

with `D` diagonal.  If `D` is invertible, a change of the complement and
diagonal rescaling gives

\[
                    s_c=p_c+v_ct.                              \tag{4}
\]

Since the rank-one term in (3) is killed by `[u]_\times`, one has
`N=[u]_\times D`; thus a singular `D` gives a zero column of `N`.
After interchanging the two stars if necessary, failure of this chart
means that `N` has both a zero row and a zero column.  A rank-two
zero-diagonal `3 by 3` matrix has only the following two relative
positions.  Relabelling and rescaling gives:

\[
\begin{array}{c|c|c|c}
 &P&S&N\\ \hline
 \text{same missing index}
 &(e_0,e_1,e_2)&(e_3,e_1,e_2)&E_{12}-E_{21}\\[2mm]
 \text{different missing indices}
 &(e_0,e_1,e_2)&(e_1,e_3,-a e_1-e_2)
 &aE_{10}+E_{12}+E_{20}
\end{array}                                                  \tag{5}
\]

In the second row `a=0` or `a=1`: every nonzero value is equivalent to
one after diagonal rescaling.  The relation in the first row forces
`s_1` and `s_2` to be the same common scalar multiples of `p_1` and
`p_2`.  In the second row it forces
`s_0=p_1` and `s_2=-a p_1-p_2`, which proves that (5) loses no transition
parameters.

On the regular chart (4), `N=[v]_\times`.  If `v` has one nonzero entry,
`N` has a zero row and column and is already the first row of (5).  Thus
the only regular chart omitted by the existing full-support proof is,
up to rescaling,

\[
                         v=(0,1,1).                    \tag{6}
\]

## 3. Why only two site partitions occur

Let `Z` be the five-dimensional ordinary span of the six lifted
off-diagonal products in `Sym^2 U`.  If `mathscr D` is the
four-dimensional zero-diagonal relation space, then its lifted image is
a three-space in `Z` consisting of same-site tensors.

Put

\[
                         L_0=\bigoplus_i(U\cap V_i).    \tag{7}
\]

Then `L_0=U`.  Indeed, otherwise take a nonzero `x in U^*` annihilating
`L_0` and set `a=P^T x`, `b=S^T x`.  For every `M in mathscr D`,

\[
                         P(Mb)+S(M^{\mathsf T}a)=0.     \tag{8}
\]

Two-regularity makes `a,b` nonzero.  The image of
`M mapsto (Mb,M^T a)` lies in the two-dimensional kernel of
`P direct-sum S to U`, so its kernel in `mathscr D` has dimension at
least two.  After the fixed left and right kernels are removed, this is
a two-dimensional pencil of `2 by 2` matrices.  Over `C` it contains a
nonzero matrix of rank at most one, contradicting row-column avoidance.

The support hypothesis supplies at least three nonzero site summands in
the four-space `U`.  Therefore their dimensions are

\[
                         1+1+1+1\quad\hbox{or}\quad2+1+1.        \tag{9}
\]

For four site lines, the restriction map

\[
                         Z^\perp\longrightarrow
                         \bigoplus_i\operatorname {Sym}^2(U\cap V_i)^*
                                                               \tag{10}
\]

has rank at most one.  For a fat plane `L` and two site lines it has rank
at most two.  These are the only facts about the physical product needed
below.

## 4. A regular relation with one zero coefficient

Use (4) with (6), and take coordinates `(p_0,p_1,p_2,t)` on `U`.  Put

\[
 \ell_0=x_0,\quad \ell_1=x_1,\quad \ell_2=x_2,\quad
 \ell_3=x_1+x_2-x_3,\quad \ell_4=x_3.                 \tag{11}
\]

Direct multiplication gives

\[
 Z^\perp=\langle\ell_0^2,\ell_1^2,\ell_2^2,
                         \ell_3^2,\ell_4^2\rangle,
 \qquad
 \ell_1+\ell_2-\ell_3-\ell_4=0.                     \tag{12}
\]

The six named vectors, in the circuit hyperplane of `C^5`, are

\[
\begin{array}{lll}
 p_0=s_0=(1,0,0,0,0),
 &p_1=(0,1,0,1,0),&p_2=(0,0,1,1,0),\\
 &&s_1=(0,1,0,0,1),\quad s_2=(0,0,1,0,1).
\end{array}                                                  \tag{13}
\]

### Four lines

We use the following elementary cube-section fact.

**Lemma 4.1.**  Let four affinely independent vertices of the four-cube
`{plus-or-minus 1}^4` lie in a central hyperplane whose four coefficients
are nonzero.  Two of the vertices are antipodal.

There is a particularly small exact check.  Among the
`binom(16,4)=1820` four-subsets, 96 have affine rank four, ordinary rank
three, and a full-support nullvector.  Signed coordinate permutations
act transitively on them, with representative

\[
 \begin{pmatrix}
 -1&-1&-1&-1\\
 -1&-1& 1& 1\\
 -1& 1&-1& 1\\
  1&-1& 1&-1
 \end{pmatrix}.                                           \tag{14}
\]

The last two rows are antipodal.  This finite reduction works over every
field of characteristic different from two; the companion verifier
checks the ranks and the single orbit exactly.

Now let `u_0,...,u_3` generate the four site lines.  Rank one in (10)
says that the five vectors

\[
                  (\ell_0(u_i)^2,\ldots,\ell_4(u_i)^2)             \tag{15}
\]

are proportional as `i` varies.  None is zero, and none of their five
coordinates can vanish, because the four `u_i` span `U`.  Rescaling the
`u_i` and taking square roots writes their `ell`-coordinates as

\[
                  (A_0,\epsilon_{i1}A_1,\ldots,
                                      \epsilon_{i4}A_4),           \tag{16}
\]

where every `A_j` is nonzero.  The circuit (12) puts the last four signs
in the central hyperplane with coefficient vector
`(A_1,A_2,-A_3,-A_4)`.  Lemma 4.1 supplies an antipodal pair.  The sum of
the corresponding two vectors in (16) is a nonzero multiple of `p_0`.
Thus `p_0` reaches only two site lines, a contradiction.

### A fat plane and two lines

Let `L` be the fat site.  The nonzero restrictions `ell_j|L` occupy at
most two projective classes, because three distinct squares of binary
linear forms are independent.  There cannot be a zero restriction: the
same coordinate then vanishes on `L` and, by the rank-two joint
restriction, on both outside lines, contradicting that the site summands
span `U`.  There are exactly two classes.

Write their supports as `A,B`.  The circuit must vanish separately on
the two class generators.  Since its coefficient at index zero is zero,
the class containing zero has two further indices, and the other class
has the remaining two:

\[
                         |A|+|B|=3+2,qquad 0\in A.     \tag{17}
\]

Modulo `L`, all vectors whose coordinatewise square lies in the
two-space generated by the two class squares occupy exactly three
projective directions.  This follows by independently twisting signs
on the two classes and imposing the four-term circuit.  For reference,
up to the `S_2 times S_2` symmetry of the positive and negative circuit
indices, the quotient calculation is:

| class containing `0` | named quotient directions | conclusion for any two site directions |
|---|---|---|
| `012` | `p_0=T`; `p_1,s_1=infinity`; `p_2,s_2=0` | one named direction is a chosen axis |
| `013` | `s_2=0` in the quotient | `s_2` is already contained in `L` |
| `034` | `p_0=0`; `p_1,p_2=infinity`; `s_1,s_2=1` | one named direction is a chosen axis |

Here the three possible directions are denoted `0,infinity,T` in the
first row and `0,infinity,1` in the last; the four mixed classes form the
orbit of the middle row.  The two outside site lines must select two
distinct directions.  A named vector on either selected direction has
zero coefficient on the other outside line, so it reaches at most the
fat site and one line.  This again contradicts dense support.

Thus (6) is impossible for both partitions in (9).

## 5. A zero row and a zero column

For the same-missing-index form in (5), the ordinary off-diagonal space
and its annihilator are

\[
\begin{split}
 Z&=\langle e_0e_1,e_0e_2,e_1e_3,e_1e_2,e_2e_3\rangle,\\
 Z^\perp&=\langle x_0^2,x_1^2,x_2^2,x_3^2,x_0x_3\rangle.          \tag{18}
\end{split}
\]

For the different-missing-index form they are

\[
\begin{split}
 Z&=\langle e_0e_3,;a e_0e_1+e_0e_2,;e_1^2,
                                      e_1e_2,;e_2e_3\rangle,\\
 Z^\perp&=\langle x_0^2,x_2^2,x_3^2,x_1x_3,
                                      x_0(x_1-a x_2)\rangle.
                                                               \tag{19}
\end{split}
\]

### Four lines

For (18), the quadratic map

\[
                         F(x)=(x_0^2,x_1^2,x_2^2,x_3^2,x_0x_3)    \tag{20}
\]

has every projective fibre in a three-space: the square coordinates fix
the magnitudes, and the last coordinate fixes the relative sign of
`x_0,x_3`; equivalently the fibre is contained in a hyperplane
`x_3=lambda x_0`, with the zero cases even smaller.  Four independent
site lines cannot have proportional images.

For (19), put

\[
                 F_a(x)=(x_0^2,x_2^2,x_3^2,x_1x_3,
                                           x_0(x_1-a x_2)).       \tag{21}
\]

Its base locus is the single point `[e_1]`.  For `a=1`, every nonzero
projective fibre spans at most a two-plane in the vector space `U`.
Indeed, when either `x_0` or `x_3` is nonzero the two product coordinates
determine `x_1` after choices of the square-root signs, leaving at most
one independent sign; when both vanish the fibre lies in
`span(e_1,e_2)`.

For `a=0` there is one larger possibility: if both product coordinates
vanish because `x_1=0`, independent signs on `x_0,x_2,x_3` can span the
hyperplane `x_1=0`.  Every other nonzero fibre spans at most a two-plane.
Thus four independent site lines would have to consist of three lines in
that exceptional fibre together with the base line `[e_1]`.  The named
vector `e_1=p_1=s_0` would then have one-site support.  Rank one in (10)
is incompatible with dense support in either value of `a`.

### A fat plane and two lines

For (18), let `l_i=x_i|L`.  The four squares span at most a two-space, so
the nonzero `l_i` occupy at most two projective classes.  If `L` contains
a coordinate vector, that named vector has one-site support and we are
done.  Otherwise no restriction is zero, the two classes both have size
two, and `l_0l_3` forces

\[
                             \{0,3\}\mid\{1,2\}.       \tag{22}
\]

The joint rank-two condition fixes the relative sign of coordinates zero
and three on every outside vector.  Hence all allowed outside vectors
lie in

\[
                 \mathbb C y_{03}\oplus\operatorname {span}(e_1,e_2),
                                                               \tag{23}
\]

a three-space.  They cannot supplement `L` to all of `U`.

For (19), the following binary-form classification is immediate from
the five displayed generators.

**Lemma 5.1.**  If their restrictions to a plane `L` span at most two
dimensions, then either `L` contains a coordinate vector, or `a!=0` and,
after taking `a=1`,

\[
                         L=\langle e_0+m e_2, e_1+e_2\rangle,
                         \qquad m\ne0.                 \tag{24}
\]

To see this, the three squares `l_0^2,l_2^2,l_3^2` put their nonzero
linear forms in at most two projective classes.  If there is only one
class then `L` contains `e_1`.  With two classes, the products
`l_1l_3` and `l_0(l_1-a l_2)` must have zero mixed coefficient.  If
`l_3!=0`, this forces three of the `l_i` into one class and hence puts a
coordinate vector in `L`.  If `l_3=0`, then `l_0,l_2` are independent
and

\[
                         l_1-a l_2\ \text{ is proportional to }l_0.
                                                               \tag{25}
\]

For `a=0` this again gives a coordinate vector.  For `a!=0`, absence of
one is exactly (24).

It remains only to test (24).  With binary coordinates `r,s` on `L`,

\[
 (x_0,x_1,x_2,x_3)|_L=(r,s,mr+s,0),                   \tag{26}
\]

and the image of the restricted system is

\[
 \left\langle (1,m^2,0,0,-m),(0,1,0,0,0)\right\rangle.           \tag{27}
\]

The joint rank-two condition forces the value vector (21) of each
outside line to belong to (27).  Its third square coordinate gives
`x_3=0`.  Hence `L` and both outside lines lie in the hyperplane
`x_3=0`, again impossible.

Equations (18)--(27) exclude both zero-row--zero-column forms in (5).
Together with Section 4 and the all-nonzero circuit proof, every aligned
two-plane zero pattern is closed.

## 6. Exact audit

[`verify_aligned_two_plane_boundaries.py`](../computations/verify_aligned_two_plane_boundaries.py)
checks the three ordinary kernels and annihilators, the single 96-element
cube-section orbit in Lemma 4.1, all six class partitions and their three
quotient directions in the fat-plane part of Section 4, and the
exceptional restriction and hyperplane conclusion in (24)--(27).

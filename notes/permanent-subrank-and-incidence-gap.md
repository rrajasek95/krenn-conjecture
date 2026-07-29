# Permanent subrank and the two-shore incidence gap

This note audits a tempting reduction of the perfect-matching problem to the
`m`-way permanent tensor

\[
  \operatorname{Per}_m
   =\sum_{\sigma\in S_m}e_{\sigma(1)}\otimes\cdots\otimes e_{\sigma(m)}.
\tag{1}
\]

There are two separate questions which must not be conflated:

1. does `(1)` have ordinary subrank three? and
2. does a restriction of `(1)` lift to the `2m`-site perfect-matching
   incidence tensor of `K_(m,m)`?

The second implication is false in the useful direction: a one-shore
restriction forgets precisely the inverse-permutation labels on the other
shore.  The converse implication *is* valid and makes an upper bound for
`Q(Per_m)` a necessary obstruction for a bipartite incidence solution.

## 1. The settled base case

**Proposition 1.**  Over `C`,

\[
                         Q(\operatorname{Per}_3)=2.
\tag{2}
\]

**Proof.**  The lower bound is monomial.  Retain the identity permutation
and a three-cycle.  Their union is a single bipartite six-cycle, and hence
has exactly those two perfect matchings.

For the upper bound, a restriction to `Delta_(3,3)` would use three
surjective maps `C^3 -> C^3`, hence three invertible maps.  The first slice
space of `Per_3` is

\[
 \left\{\begin{pmatrix}0&c&b\\c&0&a\\b&a&0\end{pmatrix}:a,b,c\in C\right\}.
\tag{3}
\]

It contains no nonzero rank-one matrix: its three principal two-by-two
minors are `-c^2,-b^2,-a^2`.  The corresponding slice space of
`Delta_(3,3)` contains three independent rank-one matrices.  Invertible
changes in the three factors preserve the rank stratification of a slice
space, a contradiction.  `QED`

The same cycle construction gives `Q(Per_m)>=2` for every `m>=3`: take two
permutations whose quotient is an `m`-cycle.  Their union has exactly two
perfect matchings.

For `m>=4`, the argument above no longer applies because a local map
`C^m -> C^3` has a kernel.  No general proof of `Q(Per_m)<=2`, and no exact
counterexample, was obtained in this audit.  The following exact results
delimit one attractive counterexample mechanism.

## 2. What a termwise Glynn construction would require

Glynn's identity, in tensor form, is

\[
 \operatorname{Per}_m
 =2^{1-m}\!\sum_{\substack{\delta\in\{\pm1\}^m\\\delta_1=1}}
       \left(\prod_{j=1}^m\delta_j\right)
       \bigotimes_{i=1}^m\left(\sum_{j=1}^m\delta_j e_j\right).
\tag{4}
\]

Suppose one chooses rank-three local maps `A_i:C^m -> C^3`.  A sufficient
condition for an exact `Delta_3` restriction is:

* exactly three normalized sign vectors `s_0,s_1,s_2` escape all the
  kernels `ker A_i`; and
* at every site `i`, the three vectors `A_i s_0,A_i s_1,A_i s_2` are a
  basis.

Then independent output basis changes turn the three surviving product
terms in `(4)` into the three diagonal terms.  This condition is only
sufficient.  A genuine restriction could instead use cancellations among
many nonzero Glynn summands.

There is a clean counting obstruction to the termwise construction at
small order.

**Lemma 2.**  A `d`-dimensional linear subspace of `C^m` contains at most
`2^d` vertices of the sign cube `{+/-1}^m`.

**Proof.**  Some projection onto `d` coordinates is injective on the
subspace.  It is therefore injective on its sign vertices, of which the
projected cube has only `2^d`.  `QED`

Each kernel in the proposed construction has dimension `m-3`, so it
contains at most `2^(m-3)` sign vectors, or at most `2^(m-4)` after the
normalization `delta_1=1`.  The `m` kernels can therefore kill at most

\[
                            m2^{m-4}
\tag{5}
\]

normalized Glynn terms.  For `m<=7`, this is strictly less than
`2^(m-1)-3`.  Thus the termwise Glynn construction cannot work for
`m<=7`.

There is another useful exact warning.  Normalize three prospective
survivors to the sign patterns called `0,1,p`, where `0` and `1` are
constant on the non-anchor coordinates.  The complementary pattern
`1-p` satisfies, as sign vectors,

\[
                         s_0+s_1=s_p+s_{1-p}.
\tag{6}
\]

If the images of the first three vectors are independent, `(6)` makes the
image of the fourth nonzero under every local map.  Hence these symmetric
survivors can never leave only three nonzero Glynn summands.

`computations/search_glynn_permanent_restriction.py` implements a broader
exact set-cover search using codimension-three signed-partition kernels.
`computations/verify_permanent_incidence_barriers.py` exhausts the simpler
star-kernel subclass, modulo coordinate permutations, through `m=11`; no
cover using at most `m` kernels exists in that subclass.  This is a barrier
for that construction, not an upper bound on the ordinary subrank.

## 3. Why a one-shore counterexample would not lift

The actual incidence tensor of `K_(m,m)` is

\[
 \mathcal I_m=\sum_{\sigma\in S_m}
  \left(\bigotimes_{i\in L}e_{\sigma(i)}\right)\otimes
  \left(\bigotimes_{j\in R}e_{\sigma^{-1}(j)}\right).
\tag{7}
\]

Contracting every right factor with the all-ones covector turns `(7)` into
`Per_m`.  This contraction is irreversible.  In particular, the
cancellations in `(4)` occur only after the labels `sigma^(-1)(j)` have
been forgotten.  Attaching arbitrary nonconstant right vectors to the
individual permutation terms separates those labels and destroys the
Glynn cancellation.  Consequently

\[
 Q(\operatorname{Per}_m)\ge3
 \quad\not\Longrightarrow\quad Q(\mathcal I_m)\ge3.
\tag{8}
\]

The reverse necessary implication is rigorous.

**Proposition 3.**  If `I_m` restricts to `Delta_(2m,3)`, then `Per_m`
restricts to `Delta_(m,3)`.

**Proof.**  Write the local image of edge `ij` as `a_ij` at left vertex
`i` and `b_ji` at right vertex `j`.  Choose right covectors `lambda_j`
whose three target coordinates are all nonzero.  Contracting the asserted
diagonal identity on the right gives

\[
 \sum_{\sigma\in S_m}\bigotimes_i
 \left(\lambda_{\sigma(i)}(b_{\sigma(i),i})a_{i,\sigma(i)}\right)
 =\sum_{r=0}^2\left(\prod_j\lambda_j(e_r)\right)e_r^{\otimes m}.
\tag{9}
\]

The scalar on each selected edge has simply been absorbed into the
corresponding left column.  The three coefficients on the right are
nonzero and can be rescaled to one.  Equation `(9)` is a restriction of
`Per_m` to `Delta_(m,3)`.  `QED`

Thus a proof that every `Per_m` has subrank two would exclude the complete
bipartite incidence supports, but a permanent-tensor counterexample alone
would not produce a Krenn counterexample.

## 4. The torus-zero reduction for nonbipartite matching tensors

Split `2m` vertices into equal shores `L,R` and contract every vertex in
`L` by a covector `x_i`.  If

\[
                 x_i^T A_{ij}x_j=0\qquad(ij\in\binom L2),
\tag{10}
\]

then every matching containing an internal `L` edge vanishes.  A perfect
matching has equally many internal edges in `L` and `R`, so only all-cross
matchings remain.  The contraction is exactly a vector permanent on `R`.
If every coordinate of every `x_i` is nonzero, the contracted target is a
three-term GHZ tensor with nonzero coefficients.  Therefore `(10)` would
reduce that particular matching identity to the permanent obstruction.

This is not a universal reduction.  It asks for `binom(m,2)` bilinear
equations in only `2m` projective degrees of freedom, and even the
three-vertex case can fail for three rank-two forms (the explicit failure
is recorded in `notes/determinant-split-route.md`).  Contracting only three
vertices isolates a pure permanent only when there are six vertices.  For
`2m>6`, after the three cross edges are chosen, the remaining `2m-6`
vertices still carry an internal matching tensor.  Hence a
"three-vertex torus-zero" argument does not reduce the general Krenn
problem to `(1)`.

## 5. Exact failure of the natural Fourier ansatz on `K_(5,5)`

There is a tempting two-shore cyclic ansatz.  With indices in `Z/5` and a
primitive fifth root `zeta`, map the edge `ij` to vectors whose output
components are

\[
              a_{ij}(r)=\zeta^{rj},\qquad
              b_{ji}(s)=\zeta^{-si}.
\tag{11}

For output colorings `c` on the left and `d` on the right, its coefficient
is

\[
 C(c,d)=\sum_{\sigma\in S_5}
 \zeta^{\sum_i c_i\sigma(i)-\sum_jd_j\sigma^{-1}(j)}.
\tag{12}

Every common constant coloring has coefficient `120`, as desired.  But
take

\[
             c=(0,0,0,0,0),\qquad d=(0,0,1,2,2).
\tag{13}

Exact enumeration gives residue multiplicities

\[
                         (40,20,20,20,20).
\tag{14}

Since `1+zeta+...+zeta^4=0`, `(12)` equals `20`, not zero.  Thus the most
direct cyclic Fourier construction fails on an explicit mixed coloring.

A full symmetric-group character construction has an even simpler
barrier.  The one-dimensional characters of `S_m` are precisely the
trivial and sign characters for `m>=3`, because the abelianization of
`S_m` is `C_2`.  Character orthogonality can therefore separate at most
two monochromatic sectors, never three.  Any successful group-theoretic
ansatz must use higher-dimensional representations together with genuinely
local endpoint factorizations; the elementary Fourier/character route does
not supply a candidate.

## 6. Net conclusion

The permanent route provides one rigorous local obstruction (`m=3`) and a
valid necessary test for bipartite incidence tensors.  It does not yet give
a uniform theorem:

* `Q(Per_3)=2` exactly;
* the general claim `Q(Per_m)<=2` remains undecided here;
* termwise Glynn constructions are impossible through `m=7`, and the
  audited coordinate subclasses remain impossible through `m=11`;
* a one-shore restriction cannot be lifted by restoring inverse labels;
* and the torus-zero contraction needed to reach a permanent from a general
  matching tensor is not automatic.

Accordingly, no step in this note closes Krenn's conjecture, but it prevents
using either a one-shore Glynn construction or a three-vertex contraction as
an unjustified bridge.

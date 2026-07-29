# The uniform dense six-site point has no cyclic cofactor plane

## Outcome

Let

\[
                         C_{ij}=\alpha\qquad(i<j),
             \qquad 15\alpha^3=1.                         \tag{1}
\]

This is the maximally dense six-site leading point: its hafnian is one and
all fifteen pair cofactors are nonzero.  Suppose the six cofactor planes in
the all-three-face normal form are equivariant under cyclic translation of
the vertices.  Then they cannot support all three exact binary faces and
the 120 mixed cubic Bianchi equations.

The proof closes both possible actions of the six-cycle on the two selected
contact lines.

1. If rotation preserves the two lines, each is a one-dimensional cyclic
   character.  The pure cubic equations leave only three projective offset
   profiles.  One quartic equation excludes two of them, and the terminal
   equation excludes the third.
2. If rotation swaps the two lines, diagonalize the swap.  The same cubic
   calculation puts both eigenjets in the three-profile set.  The single
   mixed coefficient `112000` forces their profile parameters to agree.
   Their row vectors are then proportional at every vertex, contradicting
   the two-plane necessity forced by the `12` binary face.

Thus the entire cyclic-equivariant cofactor-plane chart over (1) is empty,
including symmetry realized only up to the local target torus.  The proof
uses the cubic layer structurally and never launches an eight-variable
Groebner calculation.

This does not exclude noncyclic planes at the uniform point or planes over
other cofactor-open leading matrices.

## 1. Cyclic frames have only a preserving or swapping branch

Remove the common scale `alpha`.  Then

\[
             h_\varnothing=15,\qquad h_{ik}=3,
             \qquad h_{ikj\ell}=1,                        \tag{2}
\]

and each cofactor kernel is

\[
             K_i=\left\{(u_j)_{j\ne i}:
                         \sum_{j\ne i}u_j=0\right\}.       \tag{3}
\]

Let `tau(i)=i+1 mod 6`.  A cyclic plane family satisfies

\[
                            L_{\tau i}=\tau L_i.            \tag{4}
\]

Choose at every site an ordered basis `(b_i^1,b_i^2)` which realizes the
three exact binary faces.  Transport by `tau` gives another such basis.
The transition matrices at the six sites therefore stabilize

\[
                     e_1^{\otimes6}+e_2^{\otimes6}.         \tag{5}
\]

The elementary rank-two decomposition lemma says that the local stabilizer
of (5) is monomial: either every transition matrix is diagonal or every one
is anti-diagonal.  Indeed, the only rank-one tensor lines in
\(\operatorname{span}\{e_1^{\otimes5},e_2^{\otimes5}\}\) are its two
displayed coordinate lines, so the two summands in (5) can only be
preserved or exchanged.

The diagonal factors form a cocycle on a six-cycle.  Rescaling the two
selected rows at site `i` by local nonzero scalars changes that cocycle by a
coboundary.  These rescalings may be chosen with product one in each color,
so all three target normalizations remain exact.  Consequently there are
only two normal forms.

* In the preserving branch, each selected section is a cyclic eigenjet

  \[
            b_{i,i+d}=\lambda^i x_d,\qquad \lambda^6=1.    \tag{6}
  \]

* In the swapping branch, a fixed change to eigenvectors gives two sections
  `u,v` with

  \[
       u_{i,i+d}=A\lambda^i x_d,\qquad
       v_{i,i+d}=B(-\lambda)^i y_d,\qquad \lambda^6=1.      \tag{7}
  \]

Here `A,B` are nonzero.  Applying the generator six times gives the
sixth-root condition.  This cocycle normalization is only a target-torus
gauge; it preserves every zero equation and the two-plane dimension.

## 2. The cubic Bianchi tensor is basis-free zero

For every vertex triple `i<k<p`, the two bottom binary faces give

\[
                    \Theta_{ikp}^{111}=\Theta_{ikp}^{222}=0.
                                                                  \tag{8}
\]

The 120 genuinely ternary cubic equations give the other six components.
Hence

\[
          \Theta_{ikp}\big|_{L_i\times L_k\times L_p}=0          \tag{9}
\]

as a trilinear tensor.  In particular, (9) remains true after passing to
the eigenbasis `(u,v)` in the swapping branch.  This is the point at which
all 120 equations enter at once: they make the cubic condition independent
of the chosen contact axes.

## 3. Exact classification of a cyclic cubic eigenjet

For (6), the tangent equation in (3) gives

\[
                        x_5=-x_1-x_2-x_3-x_4.              \tag{10}
\]

The unique pair lift is

\[
 d_{ik}=-{1\over3}
       \sum_{\substack{j,\ell\notin\{i,k\}\\j\ne\ell}}
                    b_{ij}b_{k\ell}.                      \tag{11}
\]

Every coefficient supported on a set `S` is its `lambda=1` coefficient
times the nonzero character factor `lambda^(sum S)`.  Thus the vanishing
ideal of the cubic equations is independent of the sixth root.

For the fixed character, the four cubic rotation orbits have representatives

\[
                  000111,\quad001011,\quad001101,\quad010101.
                                                                  \tag{12}
\]

Let their polynomials generate

\[
                I\subset\mathbb Q[x_1,x_2,x_3,x_4].        \tag{13}
\]

Put

\[
 P=x_1(2x_1^2+3x_1x_2+3x_2^2),\qquad
 J=\langle x_3,x_2+x_4,P\rangle.                          \tag{14}
\]

Exact grevlex reduction gives the compact radical certificate

\[
 I\subset J,\qquad
 x_3^7\in I,\qquad (x_2+x_4)^7\in I,\qquad P^3\in I.      \tag{15}
\]

The polynomial `P` is squarefree: the quadratic factor has discriminant
`-15` and is coprime to `x_1`.  Hence `J` is radical, and (15) proves

\[
                             \sqrt I=J.                    \tag{16}
\]

A nonzero point of (16) has \(x_2\ne0\).  After projective normalization it
is exactly

\[
 (x_1,x_2,x_3,x_4,x_5)=(r,1,0,-1,-r),
       \qquad r(2r^2+3r+3)=0.                              \tag{17}
\]

Thus the 120 cubic equations reduce each cyclic eigenline to three
antisymmetric offset profiles over the algebraic closure.

## 4. The preserving branch is impossible

Each preserved contact line is complete, so it must satisfy the quartic and
terminal binary equations in addition to (17).  On (17), the `010111`
quartic is, up to the nonzero amplitude and character factors,

\[
                            {4r^3(r+6)\over9}.              \tag{18}
\]

If `r` is a root of `2r^2+3r+3`, it is nonzero and not `-6`, so (18) is
nonzero.  The remaining cubic root is `r=0`; there the all-one coefficient
is zero, while its required dimensionless value is 15.  No cyclic
eigencontact is complete.  This excludes the preserving branch.

This short argument sharpens the larger unit-ideal certificate in
[`uniform-dense-cyclic-contact-obstruction.md`](uniform-dense-cyclic-contact-obstruction.md):
the four cubics first classify the projective boundary, after which one
quartic and one terminal value suffice.

## 5. One mixed cubic collapses the swapping branch

In the eigenbasis (7), apply (17) separately to `u` and `v`:

\[
 \begin{aligned}
 u_{i,i+d}&=A\lambda^i p(r)_d,\\
 v_{i,i+d}&=B(-\lambda)^i p(t)_d,\\
 p(z)&=(z,1,0,-1,-z),\\
 r(2r^2+3r+3)&=t(2t^2+3t+3)=0.
 \end{aligned}                                             \tag{19}
\]

Direct substitution in the connection-plus-permanent cubic formula gives
the especially small component

\[
                 \Theta_{012}^{uuv}
                    =-{2\over3}A^2B\lambda^3(r-t).         \tag{20}
\]

All prefactors in (20) are nonzero, so (9) forces `r=t`.  But then, at
every vertex `i`,

\[
                 u_i=A\lambda^i p(r),\qquad
                 v_i=B(-\lambda)^i p(r)                    \tag{21}
\]

are proportional row vectors.  Returning from the eigenbasis cannot change
their span.  Therefore

\[
                       \dim\operatorname{span}
                            \{b_i^1,b_i^2\}=1,              \tag{22}
\]

contradicting the two-plane necessity imposed by the exact `12` face.  The
swapping branch is impossible as well.

The exact audit
[`computations/verify_uniform_dense_cyclic_plane_obstruction.py`](../computations/verify_uniform_dense_cyclic_plane_obstruction.py)
reconstructs the four cubic matching polynomials, verifies every containment
and power membership in (15), checks the quartic and terminal exits, and
derives (20) directly from all fifteen perfect matchings.

# Complete one-pair rows do not force the Fitting cut after semisimple evaluation

## Outcome

For every (h\geq3), over the characteristic-zero field

\[
                         k=\mathbb Q(\lambda),
\]

there is a simultaneous three-fibre coefficient packet with all of the
following properties:

* one common internal element (q=1) and one common direct matrix;
* all nine divided-power pair equations;
* literal rank-one endpoint response (R_{ij}=p_i s_j) and every Segre
  rectangle;
* two rank-three endpoint-star triples;
* three linearly independent target images; and
* the canonical generically active line
  (K(u,v)=uE_{00}+vI).

Nevertheless, two scalar coordinates of its clean error are coprime
degree-(h) binary forms.  Hence their (2h\)-column Sylvester map has full
rank, the simultaneous Bezout kernel is zero, and

\[
                         \bigwedge^h\mathcal M_f\ne0.       \tag{1}
\]

Equivalently, this packet admits no full-rank Hilbert--Burch presentation
whose column degrees sum to less than (h).

This is not a decorated site-square-zero matching source.  Its coefficient
algebra is the reduced product (A=k^3), and multiplication is
coordinatewise.  It is an exact counterguard to a narrower but important
inference:

> the complete one-pair equations, target linear independence, Segre
> response factorization, generic activity, and any commutative-algebra
> consequence preserved by semisimple base change do not force the uniform
> Fitting identity.

Thus the missing positive face must use structure killed by the passage to
(k^3): literal multisite/site-square-zero grading, primitive target-word
support, or a cross-pair restriction--insertion/fusion map which couples
the three coefficient fibres.  Another same-pair resultant, ordinary
Pluecker relation, or formal cap Hasse polarization cannot suffice by
itself.

## 1. The three-fibre full-nine packet

Let (e_0,e_1,e_2) be the primitive orthogonal idempotents of

\[
                   A=k e_0\oplus k e_1\oplus k e_2=k^3,
 \qquad e_i e_j=\delta_{ij}e_i,\qquad \mathbf1=e_0+e_1+e_2. \tag{2}
\]

Put

\[
 q=\mathbf1,\qquad
 D=\operatorname {diag}(1,1,-2),                       \tag{3}
\]

and choose the two endpoint-star triples

\[
 p_i=e_i,\qquad s_i=w_i e_i,
 \qquad (w_0,w_1,w_2)=(1,\lambda,1).                   \tag{4}
\]

Both triples are (k)-bases of (A).  Their response table is

\[
                         R_{ij}=p_i s_j
                            =\delta_{ij}w_i e_i,         \tag{5}
\]

so all rank-one Segre identities

\[
                         R_{ij}R_{k\ell}=R_{i\ell}R_{kj} \tag{6}
\]

hold literally.

Since (q^{[j]}=\mathbf1/j!) in this coefficient quotient, define

\[
 X_i={d_i\mathbf1+h w_i e_i\over h!},
 \qquad(d_0,d_1,d_2)=(1,1,-2).                         \tag{7}
\]

Then, for every (i,j),

\[
 {d_i\delta_{ij}\over h!}\mathbf1
       +{R_{ij}\over(h-1)!}
                         =\delta_{ij}X_i.               \tag{8}
\]

These are exactly all nine scalarized divided-power pair rows, with the
same (q,D,p,s) in every row.

The target images retain the whole three-dimensional target sector.  In
the idempotent basis, their numerator matrix is

\[
 \begin{pmatrix}
 h+1&1&-2\\
 1&1+h\lambda&-2\\
 1&1&h-2
 \end{pmatrix},
 \qquad
 \det=h^2\bigl(1+(h-1)\lambda\bigr)\ne0.              \tag{9}
\]

Thus this is not the earlier one-fibre scalar collapse in which the three
anchors become proportional.  Three fibres are also the smallest possible
semisimple quotient retaining three independent targets.

## 2. The canonical line is active and rootless

Use the same canonical line selected by a nonzero diagonal direct entry,

\[
                 K(u,v)=uE_{00}+vI
                       =\operatorname {diag}(u+v,v,v).  \tag{10}
\]

Because (d_0=1) and (operatorname {tr}D=0), its direct scalar is

\[
                         \sigma(K)=u.                   \tag{11}
\]

Its three diagonal target coefficients are (u+v,v,v).  Hence the activity
polynomial is

\[
        \sigma(K)K_{00}K_{11}K_{22}=u(u+v)v^2,          \tag{12}
\]

which is not identically zero.

The response in the three coefficient fibres is

\[
                         r(K)=(u+v,\lambda v,v).         \tag{13}
\]

Contracting (8) by (K) gives

\[
                         T(K)={\sigma(K)\mathbf1+h r(K)\over h!}. \tag{14}
\]

Therefore the (h!\)-scaled clean error in a fibre with response (r) is

\[
             F_h(\sigma,r)=(\sigma+r)^h
                    -\sigma^{h-1}(\sigma+hr).           \tag{15}
\]

The first two coordinate forms are

\[
\begin{aligned}
 f_0(u,v)
   &=(2u+v)^h-(h+1)u^h-hu^{h-1}v,\\
 f_\lambda(u,v)
   &=(u+\lambda v)^h-u^h-h\lambda u^{h-1}v
     =\sum_{j=2}^h {h\choose j}\lambda^j
             u^{h-j}v^j.                               \tag{16}
\end{aligned}
\]

They are coprime over (k).  Since (lambda) is a unit, divide the
second form by (lambda^2) and specialize the resulting polynomial at
(lambda=0):

\[
 \left.\lambda^{-2}f_\lambda\right|_{\lambda=0}
                   ={h\choose2}u^{h-2}v^2.              \tag{17}
\]

On the other hand,

\[
                         f_0(1,0)=2^h-h-1\ne0,
 \qquad                   f_0(0,1)=1.                   \tag{18}
\]

The homogeneous resultant of (f_0) with the right side of (17) is
therefore nonzero.  The resultant
(operatorname {Res}(f_0,\lambda^{-2}f_\lambda)) is a polynomial in
(lambda) with that nonzero constant term, so it is nonzero in
(mathbb Q(\lambda)).  This proves the claimed coprimality for every
(h\ge3).

Consequently no projective parameter kills all three coordinates of the
clean error.  The line (10) is a generically active rootless line inside a
packet satisfying all nine equations (8).

## 3. Exact Fitting and Hilbert--Burch consequence

The two subspaces

\[
 f_0\operatorname {Sym}^{h-1}k^2,
 \qquad
 f_\lambda\operatorname {Sym}^{h-1}k^2                \tag{19}
\]

have zero intersection: if (f_0A=f_\lambda B) with
(deg A=deg B=h-1), coprimality forces a degree-(h) form to divide a
form of degree (h-1).  Each subspace has dimension (h), so together
they equal (operatorname {Sym}^{2h-1}k^2).  Thus the clean Macaulay map
has rank (2h), its dual kernel is zero, and its top Sylvester/Fitting
minor is nonzero.  This proves (1).

If a source-functorial Hilbert--Burch matrix of full generic rank and total
column degree (B<h) followed from the data (2)--(14), its maximal-minor
vector would force every clean coordinate to share a factor of degree at
least (h-B>0).  Forms (16) contradict that conclusion.  Hence the same
packet also blocks the degree-deficient syzygy route at the one-pair
semisimple level, not just one selected resultant.

## 4. What extra source face is now necessary

The counterguard retains simultaneously:

1. all nine rows, rather than one selected mixed equation;
2. three independent targets, rather than a common scalar target;
3. both full-rank star triples and all their Segre equations;
4. the canonical curvature-line parameter and its activity polynomial; and
5. the whole clean family and its simultaneous Macaulay map.

What it discards is equally precise.  In a physical residual matching
algebra, coefficient fibres are not three independent idempotent summands:
they are evaluations of common labelled edge variables, target words are
primitive top-site monomials, and restriction at one or two sites links
different fibres.  None of those links survives in (k^3).

Therefore a positive proof of
(igwedge^h\mathcal M_f=0) must contain a row or chain face whose image
vanishes under this semisimple specialization but is nonzero physically.
The shortest candidates are now narrowed to:

* a cross-word, site-restriction/insertion comparison coupling at least two
  residual coefficient fibres;
* an overlapping-pair/four-cut face using the same labelled internal edge
  in two cap charts; or
* an occurrence-faithful fusion square which prevents the three response
  colours from splitting into orthogonal idempotent channels.

A construction internal to one scalarized pair presentation cannot work,
even if it treats all nine rows simultaneously.  A formal principal-parts
or Hasse totalization can still be an input, but its decisive differential
must be one of the physical gluing faces above.

## 5. Exact audit

The dependency-free checker
[verify_uniform_three_fibre_full_nine_fitting_counterguard.py](../computations/verify_uniform_three_fibre_full_nine_fitting_counterguard.py)
verifies over exact rationals, at the harmless specialization
(lambda=2), for (3\le h\le15):

* every one of the nine rows (8);
* all (3^4) Segre rectangles and both star ranks;
* the target determinant (9);
* the direct scalar, trace, and activity calculation (11)--(12);
* the clean endpoint values and the specialization (17)--(18); and
* exact Macaulay rank (2h).

The displayed determinant and resultant-specialization arguments prove the
family over (mathbb Q(\lambda)) for every (h\ge3); the finite loop is a
regression audit, not the theorem's scope.  The checker runs unchanged
under normal, optimized, and isolated/no-site Python.

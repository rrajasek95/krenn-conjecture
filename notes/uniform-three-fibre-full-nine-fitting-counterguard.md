# The abstract one-pair presentation does not force the Fitting cut

## Outcome

For every \(h\geq3\), over the characteristic-zero field

\[
                         k=\mathbb Q(\lambda),
\]

there is a simultaneous three-fibre commutative presentation packet with
all of the following properties:

* one common internal element \(q=1\) and one common direct matrix;
* all nine divided-power pair equations;
* literal rank-one endpoint response \(R_{ij}=p_i s_j\) and every Segre
  rectangle;
* two rank-three endpoint-star triples;
* three linearly independent surrogate target vectors; and
* the canonical generically active line \(K(u,v)=uE_{00}+vI\).

Nevertheless, two scalar coordinates of its clean error are coprime
degree-\(h\) binary forms. Hence their \(2h\)-column Sylvester map has full
rank, the simultaneous Bezout kernel is zero, and

\[
                         \bigwedge^h\mathcal M_f\ne0.       \tag{1}
\]

Equivalently, this packet admits no full-rank Hilbert--Burch presentation
whose column degrees sum to less than \(h\).

This is **not** a decorated site-square-zero matching source. Its
presentation algebra is the reduced product \(A=k^3\), with coordinatewise
multiplication. It is also **not** an algebra quotient or base change of
the physical matching algebra: every positive-site-degree element of the
site-square-zero algebra is nilpotent, so every algebra homomorphism to the
reduced algebra \(k^3\) kills it. In particular, such a homomorphism would
kill every physical pure target tensor rather than send it to the nonzero
vectors below.

The construction is an exact counterguard only to the narrower inference

> The abstract one-pair equations, target-vector linear independence,
> Segre response factorization, generic activity, and universal
> commutative-algebra manipulations force the uniform Fitting identity.

They do not. The missing positive face must use structure omitted by this
abstract presentation: literal multisite/site-square-zero grading,
primitive target-word support, or a cross-pair
restriction--insertion/fusion map coupling different physical words.
Another same-pair resultant, ordinary Pluecker relation, or formal cap
Hasse polarization cannot suffice by itself.

### Exact scope ledger

| Requirement | Status in this packet |
|---|---|
| One finite decorated edge array | **Absent** |
| Matching tensor equal to the full ternary GHZ tensor | **Absent** |
| Physical target normalization \(X_i=e_i^{\otimes 2h}\) | **Absent**; the \(X_i\) below are surrogate vectors in \(k^3\) |
| All \(3^{2h}\) residual-word coefficients | **Not represented or checked** |
| Nine abstract vector equations with one common \(q,D,p,s\) | **Exact** |
| Off-diagonal target-zero rows | **Exact in \(k^3\)** |
| Three independent target vectors | **Exact**, but not pure physical words |
| Rank-one Segre response and rank-three star triples | **Exact in \(k^3\)** |
| Canonical active line and clean Macaulay map | **Exact in \(k^3\)** |

Accordingly this packet is not a counterexample to Krenn's conjecture, to
the automatic physical full-nine theorem, or to a theorem using pure
target-word/site incidence. It is a model of the one-pair presentation
after precisely that physical information has been forgotten.

## 1. The three-fibre one-pair packet

Let \(e_0,e_1,e_2\) be the primitive orthogonal idempotents of

\[
 A=k e_0\oplus k e_1\oplus k e_2=k^3,\qquad
 e_i e_j=\delta_{ij}e_i,\qquad
 \mathbf1=e_0+e_1+e_2.                                  \tag{2}
\]

Put

\[
 q=\mathbf1,\qquad D=\operatorname {diag}(1,1,-2),       \tag{3}
\]

and choose the two endpoint-star triples

\[
 p_i=e_i,\qquad s_i=w_i e_i,\qquad
 (w_0,w_1,w_2)=(1,\lambda,1).                            \tag{4}
\]

Both triples are \(k\)-bases of \(A\). Their response table is

\[
                         R_{ij}=p_i s_j
                            =\delta_{ij}w_i e_i,          \tag{5}
\]

so all rank-one Segre identities

\[
                         R_{ij}R_{k\ell}=R_{i\ell}R_{kj} \tag{6}
\]

hold literally.

Since \(q^{[j]}=\mathbf1/j!\) in this presentation algebra, define

\[
 X_i={d_i\mathbf1+h w_i e_i\over h!},\qquad
 (d_0,d_1,d_2)=(1,1,-2).                                \tag{7}
\]

Then, for every \(i,j\),

\[
 {d_i\delta_{ij}\over h!}\mathbf1
       +{R_{ij}\over(h-1)!}
                         =\delta_{ij}X_i.                \tag{8}
\]

These are all nine abstract divided-power pair rows, with the same
\(q,D,p,s\) in every row.

The surrogate target vectors retain a full three-dimensional sector. In
the idempotent basis, their numerator matrix is

\[
 \begin{pmatrix}
 h+1&1&-2\\
 1&1+h\lambda&-2\\
 1&1&h-2
 \end{pmatrix},
 \qquad
 \det=h^2\bigl(1+(h-1)\lambda\bigr)\ne0.                \tag{9}
\]

This is stronger than a one-fibre scalar collapse in which the anchors are
proportional, but it is weaker than physical target purity.

## 2. The canonical line is active and rootless

Use the canonical line selected by the nonzero \(00\) direct entry,

\[
                 K(u,v)=uE_{00}+vI
                       =\operatorname {diag}(u+v,v,v).  \tag{10}
\]

Because \(d_0=1\) and \(\operatorname {tr}D=0\), its direct scalar is

\[
                         \sigma(K)=u.                    \tag{11}
\]

Its three diagonal target coefficients are \(u+v,v,v\). Hence the
activity polynomial is

\[
        \sigma(K)K_{00}K_{11}K_{22}=u(u+v)v^2,           \tag{12}
\]

which is not identically zero.

The response in the three presentation fibres is

\[
                         r(K)=(u+v,\lambda v,v).          \tag{13}
\]

Contracting (8) by \(K\) gives

\[
                         T(K)={\sigma(K)\mathbf1+h r(K)\over h!}. \tag{14}
\]

Therefore the \(h!\)-scaled clean error in a fibre with response \(r\) is

\[
             F_h(\sigma,r)=(\sigma+r)^h
                    -\sigma^{h-1}(\sigma+hr).            \tag{15}
\]

The first two coordinate forms are

\[
\begin{aligned}
 f_0(u,v)
   &=(2u+v)^h-(h+1)u^h-hu^{h-1}v,\\
 f_\lambda(u,v)
   &=(u+\lambda v)^h-u^h-h\lambda u^{h-1}v\\
   &=\sum_{j=2}^h {h\choose j}\lambda^j
             u^{h-j}v^j.                                \tag{16}
\end{aligned}
\]

They are coprime over \(k\). Since \(\lambda\) is a unit, divide the
second form by \(\lambda^2\) and specialize the resulting polynomial at
\(\lambda=0\):

\[
 \left.\lambda^{-2}f_\lambda\right|_{\lambda=0}
                   ={h\choose2}u^{h-2}v^2.              \tag{17}
\]

On the other hand,

\[
                         f_0(1,0)=2^h-h-1\ne0,\qquad
                         f_0(0,1)=1.                    \tag{18}
\]

The homogeneous resultant of \(f_0\) with the right side of (17) is
nonzero. Thus
\(\operatorname {Res}(f_0,\lambda^{-2}f_\lambda)\) is a polynomial in
\(\lambda\) with nonzero constant term, hence is nonzero in
\(\mathbb Q(\lambda)\). This proves coprimality for every \(h\ge3\).

Consequently no projective parameter kills all three coordinates of the
clean error. The line (10) is a generically active rootless line inside
the abstract packet satisfying (8).

## 3. Exact Fitting and Hilbert--Burch consequence

The two subspaces

\[
 f_0\operatorname {Sym}^{h-1}k^2,\qquad
 f_\lambda\operatorname {Sym}^{h-1}k^2                 \tag{19}
\]

have zero intersection. Indeed, if \(f_0A=f_\lambda B\) with
\(\deg A=\deg B=h-1\), coprimality forces a degree-\(h\) form to divide a
form of degree \(h-1\). Each subspace has dimension \(h\), so together
they equal \(\operatorname {Sym}^{2h-1}k^2\). Thus the clean Macaulay map
has rank \(2h\), its dual kernel is zero, and its top Sylvester/Fitting
minor is nonzero. This proves (1).

If a functorial Hilbert--Burch matrix of full generic rank and total column
degree \(B<h\) followed from the abstract data (2)--(14), its
maximal-minor vector would force every clean coordinate to share a factor
of degree at least \(h-B>0\). Forms (16) contradict that conclusion.
Hence the same packet blocks the degree-deficient syzygy route at the
one-pair presentation level, not just one selected resultant.

## 4. What cross-pair gluing remains viable

The counterguard retains simultaneously at the abstract level:

1. all nine rows, rather than one selected mixed equation;
2. three independent surrogate targets, rather than a common scalar;
3. both full-rank star triples and all their Segre equations;
4. the canonical curvature-line parameter and its activity polynomial; and
5. the whole clean family and its simultaneous Macaulay map.

In a physical residual matching algebra, word coefficients instead arise
from common labelled edge variables, target words are primitive top-site
monomials, and restriction at one or two sites links different words and
different pair charts. The surrogate idempotent fibres in \(k^3\) have no
such common lift.

Therefore a positive proof of
\(\bigwedge^h\mathcal M_f=0\) must use a row or chain face which is not
defined on the abstract packet at all. The shortest viable inputs are:

* **Pure-word restriction/insertion.** A comparison must couple at least
  two physical residual words while retaining the primitive equations
  \(X_i=e_i^{\otimes2h}\). It must use site occupation, not merely apply a
  linear functional to the nine rows.
* **Overlapping-pair/four-cut gluing.** Two pair charts must share a literal
  labelled internal edge or star occurrence, and their restriction maps
  must agree in one word/fine/repeated-response grade. Independent copies
  of the same one-pair presentation still admit this counterguard.
* **Occurrence-faithful fusion.** A physical
  Khatri--Rao/reinsertion square must force columns from disjoint shores to
  lift through their common matching occurrences. An output-only
  rank-three factorization or arbitrary identification of the three
  surrogate fibres is insufficient.

Any viable gluing map must fail to extend to the orthogonal-idempotent model
(2)--(5), precisely because that model has no physical site/word lift. It
must also land on the whole clean family, not merely one selected
resultant, and either force the simultaneous Fitting wedge or yield a fully
augmented physical terminal.

A construction internal to one abstract pair presentation cannot work,
even if it treats all nine rows simultaneously. A formal principal-parts or
Hasse totalization can still be an input, but its decisive differential
must be one of these physical gluing faces.

## 5. Exact audit

The dependency-free checker
[verify_uniform_three_fibre_full_nine_fitting_counterguard.py](../computations/verify_uniform_three_fibre_full_nine_fitting_counterguard.py)
verifies over exact rationals, at the harmless specialization
\(\lambda=2\), for \(3\le h\le15\):

* every one of the nine abstract vector rows (8);
* all \(3^4\) Segre rectangles and both star ranks;
* the surrogate-target determinant (9);
* the direct scalar, trace, and activity calculation (11)--(12);
* the clean endpoint values and the specialization (17)--(18); and
* exact Macaulay rank \(2h\).

The checker explicitly records that no decorated source, physical
pure-word normalization, or residual-word enumeration is claimed. The
displayed determinant and resultant-specialization arguments prove the
family over \(\mathbb Q(\lambda)\) for every \(h\ge3\); the finite loop is
a regression audit, not the theorem's scope. The checker runs unchanged
under normal, optimized, and isolated/no-site Python.

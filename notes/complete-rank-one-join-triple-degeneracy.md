# Complete rank-one joins force triple-shore degeneracy

## 1. Outcome

Assume the all-pair source Hessians are gauge-rigid and let \(S\) be the
graph of aggregate blocks of rank at least two.  Lemma 6.8 of
[rank-three-separator-collapse.md](rank-three-separator-collapse.md) says
that two thick connected components of \(S\), when joined at all, are
joined by a complete bipartite family of nonzero rank-one blocks.  At each
vertex, the coordinate zero mask of the rank-one endpoint factor is fixed
across the opposite component.

This note couples that fixed-mask conclusion to the exact triple-shore
normal form.  The conclusion is stronger than the invertible-edge version:
no hypothesis at all is needed on the third block of the triple.  If

\[
 A_{x z}=a_x\otimes b_z,\qquad
 A_{y z}=c_y\otimes d_z
\]

are nonzero rank-one blocks and the two factors at their common endpoint
have the same coordinate support,

\[
       \{r:(b_z)_r\ne0\}=\{r:(d_z)_r\ne0\},              \tag{1}
\]

then the triple shore \(E=\{x,y,z\}\) is necessarily in the named
constant-row degeneracy branch of
[five-set-contamination-normal-form.md](five-set-contamination-normal-form.md).
Equivalently, for some color \(r\), its one-crossing constant row belongs
to the mixed-row span.  Corollary 2.3 of that note supplies a covector
\(\Theta\) which annihilates the complete one-crossing sector and gives the
pure three-crossing response

\[
             (\Theta\otimes\operatorname{id})T_1=0,
 \qquad     (\Theta\otimes\operatorname{id})T_3
                         =e_r^{\otimes(B\setminus\{x,y,z\})}.           \tag{2}
\]

Consequently, if \(C,D\) are adjacent thick \(S\)-components, then
**every** triple having two vertices in one component and one in the other
carries a selector (2).  This includes triples whose within-component
block has rank two, rank one, or zero.  For a fixed \(z\in D\), all
\(\binom{|C|}{2}\) triples \(\{x,y,z\}\) are row-degenerate.

The remaining issue is global alignment of this much larger selector
family.  Its color and covector may a priori depend on the triple.

There is a sharp negative result about recovering that color from the
common mask.  Put

\[
                    T=\{r:\bar\ell_r\ne0\},\qquad
                    M=\operatorname {supp}b_z
                      =\operatorname {supp}d_z.                         \tag{3}
\]

Then \(|T|\le2\).  If two rows survive, the only additional restriction is
\(T\cap M\ne\varnothing\).  Every singleton \(T\), and every two-set
meeting \(M\), occurs in an exact model of the complete three-slice
response equation.  Thus even the complete classification of the
one- and two-surviving-row cases supplies no mask-determined selector
color.

## 2. Equal masks are absent from every nondegenerate normal form

**Lemma 2.1 (endpoint-mask separation).**  Let \(E=\{x,y,z\}\) be a
three-vertex shore in an exact ternary matching tensor.  Suppose
\(A_{xz}\) and \(A_{yz}\) are nonzero rank-one matrices.  If all three
one-cross constant-row residues

\[
                         \bar\ell_0,\bar\ell_1,\bar\ell_2              \tag{4}
\]

are nonzero, then the endpoint factors of \(A_{xz}\) and \(A_{yz}\) at
their common vertex \(z\) have different coordinate supports.

**Proof.**  Apply Theorem 3.1 of the cited normal-form note.  Its
simultaneous color permutation and vertex permutation can be chosen so
that the two rank-one sides meeting at the distinguished common vertex
are still denoted \(xz,yz\).  The normal form has three cases, according
to the dimension of its surviving diagonal space \(S_1\).

If \(\dim S_1=3\), equation (25) of that note gives

\[
               A_{y\mid z}=a_0e_0\otimes e_0,
 \qquad       A_{x\mid z}=a_1e_1\otimes e_1.             \tag{5}
\]

The two supports at \(z\) are \(\{0\}\) and \(\{1\}\).

Suppose \(\dim S_1=2\), and write \(S_1=\ker\theta\).  The tensor \(Z\)
in equations (26)--(29) of that note controls the deviation from the three
pure pivot cells.  Its support has at least two coordinates.

If \(\theta_2=0\), then \(\theta_0\theta_1\ne0\) and

\[
 Z=e_0^{(x)}\otimes e_1^{(y)}\otimes w_z.
\]

The two rank-one assumptions give respectively
\(w_z\in\mathbb Ce_0\) and \(w_z\in\mathbb Ce_1\), so \(w_z=0\).  We are
again in (5).  If
\(\operatorname{supp}\theta=\{0,2\}\), then

\[
 \begin{aligned}
  A_{y\mid z}/a_0&=e_0\otimes e_0+\theta_0v_y\otimes e_2,\\
  A_{x\mid z}/a_1&=e_1\otimes e_1.
 \end{aligned}                                           \tag{6}
\]

Rank one in the first line forces \(v_y\in\mathbb Ce_0\).  Its endpoint
support at \(z\) is therefore either \(\{0\}\) or \(\{0,2\}\), whereas
the second support is \(\{1\}\).  The case
\(\operatorname{supp}\theta=\{1,2\}\) is symmetric.  If all three
coordinates of \(\theta\) are nonzero, then
\(Z=\mu e_0\otimes e_1\otimes e_2\).  Either cross matrix has rank two
when \(\mu\ne0\), so \(\mu=0\), and (5) returns.  Thus the masks are
different throughout the two-dimensional branch.

It remains to consider \(\dim S_1=1\).  Absorb the nonzero coefficients in
the cyclic staircase (32b) into its transfer vectors and write

\[
\begin{aligned}
 M_0&=E_{00}+e_1U^T+Ve_2^T,\\
 M_1&=E_{11}-\rho e_0U^T+We_2^T,\\
 M_2&=E_{22}-\sigma e_0V^T-\tau We_1^T,
 \qquad \tau\rho=\sigma,                                \tag{7}
\end{aligned}
\]

where \(M_0=A_{y\mid z}/a_0\) and
\(M_1=A_{x\mid z}/a_1\); the scalars
\(\rho,\sigma,\tau\) are nonzero.  Write
\(U=(U_0,U_1,U_2)\), and similarly for \(V,W\).  Rank one of \(M_0\),
using its pivot entry \((M_0)_{00}=1\), gives

\[
             V_2=0,\qquad U_1=0,\qquad
             U_2+V_1=U_0V_0.                            \tag{8}
\]

Rank one of \(M_1\), using \((M_1)_{11}=1\), gives

\[
             U_0=0,\qquad W_2=0,\qquad W_0=\rho U_2.    \tag{9}
\]

Put \(t=U_2\), \(\alpha=V_0\), and \(\beta=W_1\).  Equations (8)--(9)
and \(\tau\rho=\sigma\) reduce the staircase to

\[
 \begin{aligned}
  M_0&=e_0\otimes(e_0+\alpha e_2),\\
  M_1&=e_1\otimes(e_1+\beta e_2),\\
  M_2&=\operatorname {diag}(-\sigma\alpha,-\tau\beta,1).
 \end{aligned}                                          \tag{10}
\]

No nonvanishing of \(\alpha,\beta\) is needed.  The two endpoint supports
at \(z\) are \(\{0\}\) or \(\{0,2\}\), and \(\{1\}\) or \(\{1,2\}\),
respectively.  They are always different.  This exhausts the normal form
and proves the lemma. \(\square\)

**Corollary 2.2 (equal-mask triple degeneracy).**  If the two nonzero
rank-one sides \(xz,yz\) have equal coordinate support at \(z\), then for
some color \(r\)

\[
                         \ell_{r^E}\in M_{B\setminus E}.               \tag{11}
\]

Consequently \(E\) has a pure three-cross selector satisfying (2).

**Proof.**  Equality of the masks contradicts Lemma 2.1 if all three
residues survive.  Thus one residue is zero in the quotient, which is
exactly (11).  Corollary 2.3 of the triple-shore note turns (11) into
(2). \(\square\)

## 3. Every triple across a thick complete join degenerates

**Theorem 3.1 (complete-join selector saturation).**  Let
\(H_B(A)=\Delta_{B,3}\), assume all two-deletion Hessians are gauge-rigid,
and let \(C,D\) be distinct connected components of \(S\), each of minimum
internal degree at least two.  Suppose the aggregate support between them
is nonempty.  Then, for every distinct \(x,y\in C\) and every \(z\in D\),
the triple \(E=\{x,y,z\}\) has a color \(r=r(x,y,z)\) for which (11) holds,
and hence a pure three-cross selector (2).  The same conclusion holds with
\(C,D\) interchanged.

In particular, this one component join supplies

\[
       |D|\binom{|C|}{2}+|C|\binom{|D|}{2}              \tag{12}
\]

row-degenerate triples.

**Proof.**  Lemma 6.8 of the separator-collapse note makes both
\(A_{xz}\) and \(A_{yz}\) nonzero rank-one matrices.  The same lemma says
that the endpoint color-zero mask at \(z\) is independent of the chosen
vertex of \(C\).  Their endpoint factors at \(z\) therefore have the same
coordinate support.  Corollary 2.2 gives (11) and (2).  Interchanging the
components proves the symmetric assertion, and counting the two disjoint
types of \(2+1\) triples gives (12). \(\square\)

No support term is discarded here.  The tensors \(T_1,T_3\) contain all
one-cross and three-cross matchings with their complex cancellations, and
the covector \(\Theta\) may be entangled across the three shore sites.

## 4. The mask does not determine the degeneracy color

The preceding result excludes \(T=\{0,1,2\}\).  The smaller possibilities
have one further elementary classification.

**Lemma 4.1 (two-survivor mask intersection).**  With the notation (3), if
\(|T|=2\), then

\[
                              T\cap M\ne\varnothing.                    \tag{13}
\]

There is no restriction on a singleton \(T\).

**Proof.**  Suppose \(T=\{r,s\}\) is disjoint from \(M\).  Choose a
quotient covector \(\varphi\) for which both surviving diagonal
coefficients are nonzero.  In the complete three-slice equation (17) of
the normal-form note, take first the coordinate-\(r\) slice at \(z\).
Both rank-one cross blocks vanish there because \(r\notin M\), leaving

\[
                  Z_{z,r}(\varphi)A_{xy}
                         =b_r(\varphi)e_r\otimes e_r.                  \tag{14}
\]

Thus \(A_{xy}\) is a nonzero scalar multiple of
\(e_r\otimes e_r\).  The coordinate-\(s\) slice gives the same conclusion
with \(s\) in place of \(r\), which is impossible.  This proves (13).
For one surviving row, the third slice alone can supply its pure tensor,
so the same argument gives no restriction. \(\square\)

This condition is sharp already in the exact slice equation, over
\(\mathbb Q\).  Let \(M\ne\varnothing\), and put

\[
 b=\sum_{j\in M}e_j,\qquad d=b+e_h
                                                               \tag{15}
\]

for a chosen \(h\in M\).  Both vectors have support exactly \(M\), and
\(d-b=e_h\).  Put

\[
 A_{y\mid z}=e_h\otimes b,\qquad
 A_{x\mid z}=e_h\otimes d.                                \tag{16}
\]

The center choices

\[
                    Z_x=-e_h,\qquad Z_y=e_h,\qquad Z_z=0              \tag{17}
\]

give exactly \(e_h^{\otimes\{x,y,z\}}\).  For any \(k\ne h\), independently
put \(A_{xy}=e_k\otimes e_k\) and use
\(Z_x=Z_y=0,Z_z=e_k\) to obtain \(e_k^{\otimes\{x,y,z\}}\).
Taking these as two independent quotient-covector responses realizes
\(T=\{h,k\}\).  Hence every two-set meeting \(M\) occurs.  A singleton
\(T=\{k\}\), for arbitrary \(k\), is realized by retaining only the second
response with \(A_{xy}=e_k\otimes e_k\); the two nonzero cross blocks may
be assigned any equal mask and are unused by that response.

Consequently:

* if \(|M|=1\) and exactly two rows survive, the sole degeneracy color is
  outside \(M\), but either outside color can occur;
* if \(|M|\ge2\) and exactly two rows survive, any color can be the sole
  degeneracy color; and
* if exactly one row survives, any pair of colors can be the degeneracy
  pair.

There is therefore no color common to all allowed degeneracy sets for a
fixed nonempty mask.  Alignment must use overlap equations between the
selectors, not their zero masks alone.

## 5. Gauge rigidity does not make the cross lines injective

The fixed mask also cannot be upgraded to a projective-line injection from
all-pair Hessian rigidity alone.  There is an exact eight-site
countermodel.  Split the vertices as

\[
                    C=\{0,1,2,3\},\qquad D=\{4,5,6,7\}.                \tag{18}
\]

Put arbitrary displayed invertible integer matrices on the twelve internal
edges of the two \(K_4\)'s, and nonzero rank-one integer matrices on all
sixteen cross edges.  Every cross endpoint factor has full coordinate
support, so the masks are fixed exactly as in Lemma 6.8.  At vertex \(4\),
however, the two factors on \(04\) and \(14\) are both

\[
                              (1,1,1),                                \tag{19}
\]

so the endpoint lines coincide.

The complete data are in
[verify_complete_join_hessian_countermodel.py](../computations/verify_complete_join_hessian_countermodel.py).
For every one of the \(28\) deleted pairs, it constructs the six-site map

\[
                  Z\longmapsto Zq^2/2
\]

and certifies rank \(130\) in its \(135\)-dimensional quadratic domain
modulo the prime \(1{,}000{,}003\).  The five universal vertex gauges are
independent and killed.  Modular rank gives the characteristic-zero lower
bound, while the gauges give the matching upper bound, so every chart is
gauge-rigid over \(\mathbb Q\).

Thus neither injectivity nor an arc bound on the cross endpoint lines
follows from gauge rigidity, thick components, completeness of the join,
and fixed masks.  The model deliberately fails the target equation: its
mixed coefficient at \(10000000\) is the positive integer
\(433{,}653{,}973{,}029\).  As with the label countermodels above, any
alignment must use the full mixed coefficient or selector-overlap
identities.

## 6. Exact symbolic audit

[verify_complete_join_triple_degeneracy.py](../computations/verify_complete_join_triple_degeneracy.py)
checks the finite normal-form calculation symbolically.  It verifies all
four support cases in the two-dimensional branch, derives (8)--(10) from
the displayed rank-one minors in the one-dimensional branch, and checks
that the two common-endpoint masks are unequal even when either
\(\alpha\) or \(\beta\) vanishes.  It also constructs (15)--(17) for every
nonempty mask, every singleton surviving set, and every two-set satisfying
(13).  The separate eight-site verifier gives the exact Hessian certificate
in Section 5.

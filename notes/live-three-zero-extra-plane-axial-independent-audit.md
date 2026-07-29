# Independent audit of the axial sole-extra-plane closure

No coefficient, balance, normalization, cleanup, or range gap was found in
[live-three-zero-extra-plane-axial.md](live-three-zero-extra-plane-axial.md).
This audit reconstructs the response from the common-power formula rather
than using the proof's counts or its checker.  Below, the exceptional label
called \(c\) in the endpoint argument is renamed \(o\), to distinguish it
from the type-\(10\) centre already called \(c\).

## Response and normalization

Let

\[
 V=E\sqcup A\sqcup\{e\},\qquad |E|=t,\qquad
 |A|=2r+2-t,\qquad |V|=2r+3.
\]

For a word \(w\), a diagonal source colour \(s\), and one fixed coordinate
at \(z_0\), the complete marked part of the response is

\[
 \sum_{\{a,b\}\subset V}
  2(P_a)_{w_as}(P_b)_{w_bs}
  \sum_{i\notin\{a,b\}}Z_{i,w_i}
  \operatorname {haf}Q[w]_{V\setminus\{a,b,i\}}.                 \tag{A1}
\]

The direct term is zero in every row used here because the source is
diagonal and the direct quadratic has zero diagonal.  Formula (A1) also
shows exactly which variables can contaminate a cleanup row.

Upstream, the cyclic ports give \(\mu\ne0\), the extra-capacity lemma gives
\(\beta_e=\mu\), and an exceptional live site has
\(\nu_j\ne\mu\) and a structurally zero \(z_0\)-star.  After setting
\(\mu=1\), all denominators used below are nonzero: \(\nu_j+1\) by the
live--centre equation and \(\nu_j+\nu_k\) by the live--live equation.

For the first axial family, a rank-two matrix with output image
\(\langle e_0,e_1\rangle\) has zero third output row.  Its row plane is

\[
 R=\langle e_0,(0,u,v)\rangle,
\]

where \(v\ne0\), because \(R\cap\langle e_0,e_1\rangle=\mathbb C e_0\).
Changing the basis of its two nonzero output rows, which preserves the
output plane, sets \(v=1\) and gives

\[
 P_e=\begin{pmatrix}1&0&0\\0&u&1\\0&0&0\end{pmatrix}.             \tag{A2}
\]

Thus the second row \(p=(0,u,1)\) has source-\(2\) entry one, including at
\(u=0\).  If one exceptional site \(m\) has output colour \(2\) and every
other site is binary, (A1) has the unique marked pair \(\{m,e\}\), with
coefficient \(2\).  The parameter \(u\) disappears because both sites are
removed before the cofactor is formed.  Swapping colours \(0,1\) treats the
other axial family and preserves the normalized \(H\) and \(D\).

## Binary rows and the endpoint

Put \(\kappa=1/2\).  For \(1\le t\le r+1\), take
\(S\subset A\) of size \(r+2-t\), put \(E\setminus\{m\}\) and \(S\) on
the zero shore, and put \(A\setminus S\) on the one shore.  After deleting
\(\{m,e\}\), a star in \(S\) leaves \(r\) zeros and \(r\) ones; a star
outside \(S\) leaves \(r+1\) zeros and \(r-1\) ones.  Every exceptional
zero is forced to a common-beta one, so the surviving coefficient is

\[
 C_m=2\,r!\left(\prod_{j\ne m}{1\over1+\nu_j}\right)
             \kappa^{r-t+1}.                                    \tag{A3}
\]

There are \(r!\) labelled bijections, and no other matching type.  The
exponent is nonnegative, while
\(1\le r+2-t<2r+2-t\).  Hence the fixed-subset incidence matrix has full
column rank.  Colour swapping has the same coefficient and kills both
binary rows at every site of \(A\).

At \(t=r+2\), fix distinct exceptional sites \(m,o\) and put
\(L=E\setminus\{m,o\}\).  For a target \(i\in A\), the remaining cofactor
is the permanent from the \(r\) exceptional rows \(L\) to the exceptional
column \(o\) and the \(r-1\) common columns \(A\setminus\{i\}\).  Expanding
by the exceptional column gives exactly

\[
 C_{m,o}=2(r-1)!\left(\prod_{\ell\in L}{1\over\nu_\ell+1}\right)
       \sum_{\ell\in L}{\nu_\ell+1\over\nu_\ell+\nu_o}.           \tag{A4}
\]

Fix \(o\), put \(N=E\setminus\{o\}\), and set
\(h_\ell=(\nu_\ell+1)/(\nu_\ell+\nu_o)\ne0\).  The normalized pivots as
\(m\) varies are the coordinates of
\((J-I)h\).  This matrix has eigenvalues \(r,-1,\ldots,-1\) and determinant
\((-1)^r r\ne0\).  Therefore some \(m\) gives a nonzero pivot.  This is a
pointwise argument, so it remains valid under every repetition of beta
values allowed by the nonzero-denominator hypotheses.

## Cleanup and boundary cases

For \(t\ge2\), marking two exceptional sites and taking the extra site as
the star leaves \(r\) zeros and \(r\) ones.  Its coefficient is

\[
 2\,r!\left(\prod_{j\in E\setminus B}{1\over1+\nu_j}\right)
       \kappa^{r-t+2}\ne0.                                      \tag{A5}
\]

For \(t=1\), source \(11\) instead gives

\[
 2{r+2\choose2}r!{1\over1+\nu_1}\kappa^{r-1}\ne0.               \tag{A6}
\]

An arbitrary contraction at \(e\) can create additional marked pairs in
these rows, but every resulting off-star term multiplies an already killed
binary active variable or a structurally zero exceptional star.  Thus this
is a triangular quotient, not a claim that the raw response has only one
term, and (A5)--(A6) kill the full extra block.

Finally give a target \(i\in A\) row \(2\).  If \(i\) is live, the only
source-\(2\) sites are \(m,e,i\).  Pair \(\{m,e\}\) supplies (A3) or
(A4) at the target.  A pair containing \(i\) cannot also use \(i\) as the
star, so all of its variables are extra, exceptional, or active binary
variables already killed.  For a type-\(10\) centre, row \(2\) of \(P_i\)
is zero and no new pair occurs.  This proves the third-row cleanup without
discarding contamination.

The ranges partition exactly as claimed: (A3) covers
\(1\le t\le r+1\), (A4) covers \(t=r+2\), and the ambient bound
\(t\le2r\) is compatible with the endpoint for every \(r\ge2\).  In
particular, \((r,t)=(2,1)\), \(u=0\), and the repeated-beta
\((r,t)=(2,3),(2,4)\) cases require no exception.  The \(t=0\) stratum is
upstream, and the transverse theorem covers the nonaxial row planes for
\(t\ge2\).  After adjoining the structurally zero exceptional stars and
the singular type-\(22\) ports, the graph conclusion therefore has the
stated scope.

[verify_live_three_zero_extra_plane_axial_independent_audit.py](../computations/verify_live_three_zero_extra_plane_axial_independent_audit.py)
implements (A1) independently, retaining exceptional-star columns and
arbitrary extra contractions.  It verifies (A2)--(A6), the endpoint
permanents, the triangular cleanup, symbolic and repeated-beta stress cases,
\(r=2\), \(u=0\), and the \(J-I\) determinant through \(r=12\).

# Two-chart Hamming-one lifts synchronize to one cross-product residue

## 1. Outcome

The sitewise second-polar alternative in the
[Hamming-one routing theorem](full-nine-hamming-one-second-polar-routing.md)
is not independent on the two physical charts selected by one curvature
minor.  At the two cross sites, the two second polars are literally the same
source coefficient with permuted indices.  If both sites obey the bare
fixed-label \(\Gamma\) identity, their complete pure response matrices
synchronize:

\[
 M^{pq}=M^{pr}=\mu e_\delta^{\mathsf T},\qquad
 \phi A_{pq}=\psi A_{pr}
      =(e_\delta-\mu)e_\delta^{\mathsf T}.               \tag{1}
\]

Here \(\delta\) is the pure physical colour and \(\phi,\psi\) are the two
pure hafnian coefficients.  At the level of the bare identity, the cross
sites are forced into one of three exact boundaries:

1. the second direct block vanishes;
2. both direct blocks are proportional rank-one matrices supported in the
   same physical column; or
3. both pure hafnian coefficients vanish.

There is a stronger provenance conclusion.  If both identities are actual
outputs of the Hamming-one theorem, so both direct blocks have the required
nonzero quotient compression, the first two boundaries contradict that
compression.  Therefore

\[
                         \boxed{\phi=\psi=0}.                 \tag{1a}
\]

The simultaneous routed cross-site lift branch is exactly the double
fixed-label hafnian-zero boundary; the direct-free and common-column cases
survive only in the weaker bare-identity ledger.

At a site common to the two residual charts, simultaneous bare identities
then give one uniform source-relative residue

\[
 \boxed{[\Theta_{i,e}z^{[h-2]}]_{\delta^C}=0},             \tag{2}
\]

where

\[
 \Theta_{i,e}
 =x_i(U_{\delta e}y_\delta-Q_{\delta e}t_\delta)
  -v_e(P_{i\delta}t_\delta-R_{i\delta}y_\delta).           \tag{3}
\]

In the weaker common-column ledger, when the pure colour is the two middle
labels of the selected curvature cell, the two parenthesized forms are an
invertible transform with determinant equal to the selected curvature.
Thus (2) is a literal own-edge/cross-product annihilator, not an unspecified
compatibility condition.

This is a genuine reduction, but not the active-clean-cap theorem.  An exact
four-site guard shows that nonzero curvature and (2) do not imply
\(\Theta=0\).  The remaining positive input must use the other fixed-label
rows or source-valid own-edge incidence, rather than universal Bianchi
overlap alone.

## 2. Two charts and their pure response matrices

Let the source have physical site set \(\mathcal V\), with
\(|\mathcal V|=2m\), and put \(h=m-1\ge3\).  Fix three distinct sites
\(p,q,r\).  Write

\[
 P=A_{pq},\qquad R=A_{pr}.                                  \tag{4}
\]

The residual quadratic, endpoint stars, and direct block on the \(pq\)-chart
obey all nine rows

\[
 P_{ij}q_{pq}^{[h]}+p_i^{pq}s_j^{pq}q_{pq}^{[h-1]}
       =\delta_{ij}X_i,                                      \tag{5}
\]

and the \(pr\)-chart has the analogous equations with \(R\).  Fix a pure
physical colour \(\delta\), and put

\[
 \phi=[q_{pq}^{[h]}]_{\delta^{\mathcal V\setminus\{p,q\}}},\qquad
 \psi=[q_{pr}^{[h]}]_{\delta^{\mathcal V\setminus\{p,r\}}}. \tag{6}
\]

The two pure response matrices are therefore

\[
 M^{pq}=E_{\delta\delta}-\phi P,\qquad
 M^{pr}=E_{\delta\delta}-\psi R.                            \tag{7}
\]

Say first that a residual site \(x\) obeys the **bare fixed-label
\(\Gamma\) identity** on a chart when

\[
 \Gamma_x(e)=\delta_{e\delta}M
       \qquad\text{for all physical labels }e.               \tag{8}
\]

No common matching power has been cancelled in this definition.  Reserve
**routed \(\Gamma\)-lift alternative** for the same identity when it is the
third output of the Hamming-one theorem, including that theorem's antecedent

\[
                       a_{I^c,J^c}\ne0.                       \tag{8a}
\]

## 3. The cross sites are the same second polar

Put \(D=\mathcal V\setminus\{p,q,r\}\).  On \(D\), let \(z\) be the internal
quadratic and let \(x_i,y_j,t_k\) be the star rows from \(p,q,r\),
respectively.  The second polar on the \(pq\)-chart at its residual site
\(r\) is

\[
 \Gamma^{pq}_r(k)_{ij}
   =[t_kx_iy_jz^{[h-2]}]_{\delta^D}.                         \tag{9}
\]

On the \(pr\)-chart, the residual site \(q\) has

\[
 \Gamma^{pr}_q(j)_{ik}
   =[y_jx_it_kz^{[h-2]}]_{\delta^D}.                         \tag{10}
\]

The square-zero algebra is commutative, so (9)--(10) are the same scalar
coefficient:

\[
                    \Gamma^{pq}_r(k)_{ij}
                    =\Gamma^{pr}_q(j)_{ik}.                  \tag{11}
\]

**Theorem 3.1 (cross-site synchronization).**  If \(r\) obeys the bare
fixed-label \(\Gamma\) identity on the \(pq\)-chart and \(q\) obeys it on
the \(pr\)-chart, then (1) holds for a uniquely determined column vector
\(\mu\).

**Proof.**  Substituting (8) on both sides of (11) gives, for every
\(i,j,k\),

\[
 \delta_{k\delta}M^{pq}_{ij}
       =\delta_{j\delta}M^{pr}_{ik}.                         \tag{12}
\]

Set \(k=\delta\).  Then \(M^{pq}\) vanishes away from column \(\delta\),
and its \(\delta\)-column is the \(\delta\)-column of \(M^{pr}\).  Setting
\(j=\delta\) proves the transposed assertion for \(M^{pr}\).  Hence there
is one vector \(\mu\) such that

\[
                         M^{pq}=M^{pr}=\mu e_\delta^{\mathsf T}.
\]

Equations (7) now give (1).  \(\square\)

## 4. Exact curvature routing

Add a fourth site \(s\), and fix a selected curvature cell

\[
 A=P_{ab}\ne0,\quad B_0=R_{ac},\quad
 F=Q_{bd},\quad U_0=U_{cd},\quad
 \kappa=AU_0-B_0F\ne0,                                     \tag{13}
\]

where \(Q=A_{qs}\) and \(U=A_{rs}\).  Theorem 3.1 gives the following
exhaustive scalar split.

* If \(\phi\ne0\) and \(\psi=0\), then (1) first gives
  \(\mu=e_\delta\) and then \(P=0\), contradicting \(A\ne0\).  This branch
  is impossible.
* If \(\phi=0\) and \(\psi\ne0\), then \(\mu=e_\delta\) and \(R=0\).
  Hence \(B_0=0\) and
  \(\kappa=AU_0\).  This is exactly the direct-free second-chart boundary
  in the [tilted-chart theorem](tilted-second-chart-activity-and-zero-block-boundary.md).
* If \(\phi\psi\ne0\), then \(P\) and \(R\) are proportional nonzero
  rank-one matrices supported only in column \(\delta\).  Since
  \(P_{ab}\ne0\), necessarily \(b=\delta\).  If \(c\ne\delta\), then
  \(B_0=0\) and again \(\kappa=AU_0\).  If \(c=\delta\), put
  \[
                \lambda=\psi U_0-\phi F.
  \]
  The \((a,\delta)\)-entry of (1) gives
  \(\phi A=\psi B_0\), and therefore
  \[
                     \boxed{\psi\kappa=A\lambda\ne0}.       \tag{14}
  \]
* If \(\phi=\psi=0\), both pure response matrices equal
  \(E_{\delta\delta}\).  If the nonzero-compression hypotheses of the
  Hamming-one theorem hold on both charts, both Hamming-one cohafnian
  covectors are zero by its equation (4).  This is the double fixed-label
  hafnian-zero \(\Gamma\)-lift boundary.  Calling it the aligned singleton
  boundary would additionally require \(I=J=\{\delta\}\) on both charts.

**Corollary 4.1 (routed cross-site closure).**  Let
\(I_{pq},J_{pq}\) and \(I_{pr},J_{pr}\) be the two pure-colour endpoint
channel sets on the respective charts.  Suppose both cross-site identities
are routed \(\Gamma\)-lift alternatives, so

\[
 P_{I_{pq}^c,J_{pq}^c}\ne0,
 \qquad R_{I_{pr}^c,J_{pr}^c}\ne0.                           \tag{15}
\]

Then \(\phi=\psi=0\).

**Proof.**  The branch \(\phi\ne0,\psi=0\) gives \(P=0\), contradicting
the first compression in (15), while \(\phi=0,\psi\ne0\) gives \(R=0\),
contradicting the second.

Suppose \(\phi\psi\ne0\).  Theorem 3.1 says that \(P,R\) have only column
\(\delta\) and

\[
                         \phi P_{i\delta}=\psi R_{i\delta}.   \tag{16}
\]

On the \(pq\)-chart, the \(p\)-endpoint star at the residual site \(r\)
has local pure coefficient

\[
                         p^{pq}_{i,r}(e_\delta)=R_{i\delta}.  \tag{17}
\]

Thus \(i\notin I_{pq}\) implies \(R_{i\delta}=0\), hence
\(P_{i\delta}=0\) by (16).  Since every other column of \(P\) already
vanishes, every row indexed by \(I_{pq}^c\) is zero.  This makes
\(P_{I_{pq}^c,J_{pq}^c}=0\), contrary to (15).  If either complement is
empty, the displayed compression is empty and hence still zero, so there is
no boundary exception.  Only \(\phi=\psi=0\) remains.  \(\square\)

### 4.2 The surviving double-zero packet

On the branch of Corollary 4.1,

\[
                         M^{pq}=M^{pr}=E_{\delta\delta}.       \tag{17a}
\]

The fixed-label support of the two pure response matrices gives

\[
 \delta\in I_{pq}\cap J_{pq}\cap I_{pr}\cap J_{pr}.          \tag{17b}
\]

Every complement in (15) is nonempty, because an empty row or column
complement would make the corresponding compression zero.  Hence both
compressions lie entirely in the other two physical labels.  The
Hamming-one theorem also gives zero for every one-defect hafnian coefficient
and for both cohafnian covectors.

At the cross sites, the unique nonzero second-polar coefficient is

\[
 [t_\delta x_\delta y_\delta z^{[h-2]}]_{\delta^D}=1.        \tag{17c}
\]

The literal local visibility conditions are

\[
\begin{array}{ll}
 i\notin I_{pq}\Rightarrow R_{i\delta}=0,
   &j\notin J_{pq}\Rightarrow(A_{qr})_{j\delta}=0,\\
 i\notin I_{pr}\Rightarrow P_{i\delta}=0,
   &k\notin J_{pr}\Rightarrow(A_{qr})_{\delta k}=0.
\end{array}                                                   \tag{17d}
\]

These conditions alone do not contradict curvature or goodness.  The
following exact guard shows that the two other diagonal anchors are the
first omitted data capable of closing this packet.

**Proposition 4.2 (good-star seven-row guard).**  Use eight sites

\[
                         p,q,r,s,a_0,b_0,c_0,d_0.
\]

Set

\[
 A_{pa_0}=A_{qb_0}=A_{rs}=A_{c_0d_0}=E_{00}.                \tag{17e}
\]

Let \(P=A_{pq}\), \(R=A_{pr}\), and \(T=A_{qr}\) be supported on
physical labels \(\{1,2\}\), with each \(2\times2\) restriction
invertible, and set every other block to zero.  The complete tensor of this
packet is exactly \(X_0\).  Indeed its only perfect matching is

\[
                         pa_0\mid qb_0\mid rs\mid c_0d_0.    \tag{17f}
\]

Any matching using one edge of the \(pqr\)-triangle leaves at least one of
the corresponding private partners \(a_0,b_0,s\) unmatched.  Thus, on each
of the \(pq\)- and \(pr\)-full-nine systems, all six off-diagonal rows and
the complete \(00\) row hold; precisely the \(11\) and \(22\) diagonal
target rows are missing.  This is not a ternary GHZ source.

For pure colour \(0\), all four channel sets are \(\{0\}\), while the two
compressions are the nonzero \(\{1,2\}\)-blocks \(P\) and \(R\).  Both pure
hafnian coefficients vanish, and the two cross-site tensors are exactly

\[
 \Gamma^{pq}_r(k)_{ij}=\delta_{k0}\delta_{i0}\delta_{j0},
 \qquad
 \Gamma^{pr}_q(j)_{ik}=\delta_{j0}\delta_{i0}\delta_{k0}.   \tag{17g}
\]

All four deleted endpoint-star maps of the \(pq\)- and \(pr\)-charts are
injective.  The two \(p\)-endpoint maps get their label-zero row from
\(pa_0\), the \(q\)-endpoint map gets it from \(qb_0\), and the
\(r\)-endpoint map gets it from \(rs\); their label-one/two rows come from
the invertible triangle blocks.  The block \(c_0d_0\) is internal padding,
not an endpoint row.

Finally choose any nonzero \(P_{\alpha\beta}\), use \(s\) as the fourth
site, and take the selected middle/fourth colours \(c=d=0\).  Then

\[
 A=P_{\alpha\beta}\ne0,\qquad B_0=R_{\alpha0}=0,
 \qquad F=(A_{qs})_{\beta0}=0,\qquad U_0=(A_{rs})_{00}=1,
\]

so \(\kappa=A\ne0\).  Taking the \(\{1,2\}\)-restriction of \(P\) to be
the identity puts this bare direct/curvature cell on the diagonal, while
taking it to be the swap matrix puts it off diagonal.  In the first case the
corresponding diagonal full row is itself one of the omitted rows; the guard
does not contain a supplied diagonal anchor there.  Hence the placement of
the bare curvature cell does not close the seven-row packet.

The guard proves that seven rows are insufficient and that the omitted
diagonal sector cannot be ignored.  It does not prove that either missing
anchor is individually necessary, or that adjoining both is sufficient.
Moreover its displayed cross-site \(\Gamma\) identities are bare identities,
not routed outputs of the full-nine theorem, precisely because the \(11\)
and \(22\) rows fail.

The dependency-free checker
[`verify_double_zero_cross_gamma_guard.py`](../computations/verify_double_zero_cross_gamma_guard.py)
enumerates the exact eight-site tensor for both selected-cell orientations
and verifies the two compressions, four good stars, cross-site \(\Gamma\)
coefficients, and curvature.

Thus simultaneous bare identities cannot remain a generic
``deconcentrated'' packet, and simultaneous routed lifts are sharper still:
they force the double-zero boundary before any root or rank argument.

## 5. Common sites leave one explicit residue

Retain the four sites \(p,q,r,s\), and put
\(C=\mathcal V\setminus\{p,q,r,s\}\).  On \(C\), use the all-label notation

\[
 z,\qquad x_i,\ y_j,\ t_k,\ v_e                         \tag{18}
\]

for the internal quadratic and the four star rows.  Assume the two cross
sites satisfy Theorem 3.1 and that the common residual site \(s\) obeys the
bare fixed-label \(\Gamma\) identity on both charts.

To compute the \(pq\)-second polar at \(s\), scalarize the remaining site
\(r\) at \(\delta\).  Its four possible occupations are by the \(s\)-star,
the \(p\)-star, the \(q\)-star, or the internal quadratic.  At \(j=\delta\)
this gives

\[
\begin{aligned}
 \Gamma^{pq}_s(e)_{i\delta}
 ={}&[\bigl(U_{\delta e}x_iy_\delta
       +R_{i\delta}v_ey_\delta
       +(A_{qr})_{\delta\delta}v_ex_i\bigr)z^{[h-2]}]_{\delta^C}\\
 &+[v_ex_iy_\delta t_\delta z^{[h-3]}]_{\delta^C}.     \tag{19}
\end{aligned}
\]

The analogous expansion on the \(pr\)-chart, scalarizing \(q\), is

\[
\begin{aligned}
 \Gamma^{pr}_s(e)_{i\delta}
 ={}&[\bigl(Q_{\delta e}x_it_\delta
       +P_{i\delta}v_et_\delta
       +(A_{qr})_{\delta\delta}v_ex_i\bigr)z^{[h-2]}]_{\delta^C}\\
 &+[v_ex_it_\delta y_\delta z^{[h-3]}]_{\delta^C}.     \tag{20}
\end{aligned}
\]

The two internal-occupation terms and the two \(qr\)-direct terms cancel.
By synchronization, the bare-identity right sides of (19)--(20) are both
\(\delta_{e\delta}\mu_i\).  Their difference is therefore zero and proves
(2)--(3).

This residue is a literal piece of the all-label Bianchi connection.  With

\[
\begin{aligned}
 f_{i\delta}&=P_{i\delta}z+x_iy_\delta,\\
 g_{i\delta}&=R_{i\delta}z+x_it_\delta,\\
 H_{i\delta;e}&=P_{i\delta}v_e+E_{ie}y_\delta
                         +Q_{\delta e}x_i,\\
 N_{i\delta;e}&=R_{i\delta}v_e+E_{ie}t_\delta
                         +U_{\delta e}x_i,
\end{aligned}                                               \tag{21}
\]

where \(E=A_{ps}\), direct expansion gives

\[
\begin{aligned}
 \Theta_{i,e}
 &=y_\delta N_{i\delta;e}-t_\delta H_{i\delta;e}\\
 &=U_{\delta e}f_{i\delta}-Q_{\delta e}g_{i\delta}
   -(P_{i\delta}t_\delta-R_{i\delta}y_\delta)v_e\\
 &\hspace{13mm}
   -(P_{i\delta}U_{\delta e}-R_{i\delta}Q_{\delta e})z.
                                                               \tag{22}
\end{aligned}
\]

Put

\[
 D_i=P_{i\delta}t_\delta-R_{i\delta}y_\delta,\qquad
 \kappa_{i,e}=P_{i\delta}U_{\delta e}
                  -R_{i\delta}Q_{\delta e}.                 \tag{23}
\]

Multiplying (22) by \(z^{[h-2]}\), taking the pure coefficient, and using
(2) gives the correctly normalized top Bianchi consequence

\[
 [\bigl(U_{\delta e}f_{i\delta}
       -Q_{\delta e}g_{i\delta}-D_iv_e\bigr)z^{[h-2]}]_{\delta^C}
   =(h-1)\kappa_{i,e}[z^{[h-1]}]_{\delta^C}.                 \tag{24}
\]

The factor \(h-1\) is forced by
\(z z^{[h-2]}=(h-1)z^{[h-1]}\); no common power has been cancelled.

In the common-column branch with \(b=c=\delta\), take \(i=a,e=d\) and
put

\[
 D_0=At_\delta-B_0y_\delta,\qquad
 G_0=U_0y_\delta-Ft_\delta.                                \tag{25}
\]

The map \((t_\delta,y_\delta)\mapsto(D_0,G_0)\) has matrix

\[
       \begin{pmatrix}A&-B_0\\-F&U_0\end{pmatrix}
\]

and determinant \(\kappa\ne0\).  Hence

\[
                         \Theta_{a,d}=x_aG_0-v_dD_0          \tag{26}
\]

is an honest cross-product after an invertible reparameterization of the
transition pair \((t_\delta,y_\delta)\).  This does not assert that those
two linear forms are themselves independent.  For
\(h=3\), equation (2) is the four-site top coefficient

\[
                         [\Theta_{a,d}z]_{\delta^C}=0.       \tag{27}
\]

## 6. Low-rank cover after synchronization

Assume the nonzero-compression hypotheses of the Hamming-one theorem on the
charts under discussion.  That theorem also makes failure of
synchronization structural.  At the cross sites, unless both routed
\(\Gamma\)-lifts occur and Theorem 3.1 applies, at least one of

\[
\begin{gathered}
 \operatorname{rank}A_{pr}\le |I_{pq}|,\qquad
 \operatorname{rank}A_{qr}\le |J_{pq}|,\\
 \operatorname{rank}A_{pq}\le |I_{pr}|,\qquad
 \operatorname{rank}A_{rq}\le |J_{pr}|
                                                               \tag{28}
\end{gathered}
\]

holds, with the channel sets taken in the corresponding pure slice.  Once
Theorem 3.1 applies, at a common residual site either both sitewise bare
identities hold and give (2), or one chart takes a corresponding low-rank
alternative.  In particular, if all relevant channel sets are singletons,
every common residual site is incident to a physical block of rank at most
one or carries the explicit residue (2).  The two cross sites are governed
separately by (1), Corollary 4.1, or (28); they do not carry (2).

This is a sitewise cover.  It does not assert that one of the alternatives
holds globally at all sites.

## 7. Sharp local guard

Nonzero curvature does not let one cancel \(z^{[h-2]}\) from (2).  Already
at \(h=3\), work in the square-zero algebra on four scalar sites with
generators \(w_1,w_2,w_3,w_4\).  Take

\[
 P=R=U=1,\qquad Q=0,\qquad
 y=w_2,\quad t=w_1+w_2,\quad x=w_3,\quad v=w_4,              \tag{29}
\]

and

\[
                         z=w_1w_4+w_2w_3.                    \tag{30}
\]

Then

\[
 \kappa=PU-RQ=1,\qquad D_0=t-y=w_1,\qquad G_0=y=w_2,
\]

so

\[
                         \Theta=w_2w_3-w_1w_4\ne0.           \tag{31}
\]

Nevertheless

\[
 \Theta z=(w_2w_3-w_1w_4)(w_1w_4+w_2w_3)=0                 \tag{32}
\]

by square-zero cancellation.  This is a local source/Bianchi packet, not a
complete full-nine GHZ source.  It guards only the invalid implication
\([\Theta z]=0\Rightarrow\Theta=0\).  A positive continuation may use the
remaining fixed-label rows, the two labelled anchors, or a source-provenant
own-edge comparison; it cannot use bare curvature and common-power
cancellation alone.

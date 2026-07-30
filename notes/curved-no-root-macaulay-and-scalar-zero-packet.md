# A rootless curved line has a six-row Macaulay certificate and a nonnilpotent scalar-zero packet

## 1. Outcome

This note isolates the branch which is not reached by the two-root
polarization argument: the canonical line

\[
                         K(u,v)=uE_{ab}+vI                         \tag{1}
\]

has denominator-cleared clean error with coordinate gcd one.  At the first
boundary, where the residual set has six sites, this is no longer an
unstructured collection of 729 cubics.

There are three exact consequences.

1. The unique scalar-zero point of (1) carries a direct-free physical
   response.  If \(a\ne b\), its cap matrix is invertible and

   \[
       r_*q^{[2]}=-a_{ab}\Delta_{6,3},\qquad r_*^{[3]}\ne0.       \tag{2}
   \]

   Thus gcd one forces a **nonnilpotent three-channel response packet**, not
   the zero-data point used by the curved guard.  For \(a=b\), the same
   statement is ternary unless one explicit trace equation holds; on that
   trace hyperplane it is a binary packet.
2. A vector-valued binary cubic has no projective zero if and only if its
   degree-two Macaulay multiplication matrix has rank six.  Applied to the
   clean error, gcd one therefore has a nonzero \(6\times6\) minor involving
   six shifted columns drawn from at most six scalar coefficient rows.
   Equivalently, two linear combinations of that bounded row set have
   nonzero classical cubic resultant.
3. On any fixed two-site cut, every entry of this Macaulay matrix is given
   explicitly by the clean polynomial minus \(s^2\) times the physical row,
   as displayed in (24)--(26).  The target cancels.  Hence the rank-six
   certificate lives entirely in one literal four-site transverse ledger;
   it is not a generic functional on an unspecified tensor space.

Good-star injectivity supplies the final routing rule.  An injective
three-row star either has a selector on three distinct residual sites, or
it has one of two sharp sparse forms: it is supported on at most two sites,
or its restriction away from one exceptional site has rank at most one.
In the selector branch, two selector sites can be used as the transverse
cut.  The full rank-six ledger is then indexed by a cut on which the star
has rank at least two and retains a third independent direction on the
four-site complement.  This does **not** assert that the six columns of a
particular nonzero minor themselves use the selector coordinates; coupling
those columns to the selector is part of the remaining problem.  The sparse
alternatives contain the mechanism of the known full-good-fan guard.

This does not yet contradict gcd one.  It replaces it by the following
minimal algebraic residual:

\[
 \boxed{\begin{gathered}
 \text{a nonnilpotent direct-free scalar-zero packet}\quad\mathbf{and}\quad
 \text{a nonzero six-row four-cut Macaulay minor,}\\
 \text{together with an endpoint selector}\quad\mathbf{or}\quad
 \text{an explicit one-site/two-site concentration.}
 \end{gathered}}                                                \tag{3}
\]

These objects are stable under relabeling and give a bounded target for
coupling two first-boundary curvature lines.  At higher order the analogous
response identity and Macaulay certificate have degree \(h\) and rank
\(2h\), rather than automatically contracting to this cubic ledger; see
[the uniform response-resultant theorem](curved-rootless-line-uniform-response-resultant.md).

## 2. Pair equations and the cubic factorization

Let \(W\) be the six residual sites.  Write \(q\) for the internal
quadratic, \(p_i,s_j\in({\cal R}_W)_1\) for the two endpoint-star triples,
and \(a=(a_{ij})\) for the direct block.  The complete physical pair rows
of an exact source are

\[
       a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
       \qquad 0\le i,j\le2.                                  \tag{4}
\]

For a pair covector \(K=(K_{ij})\), put

\[
\begin{aligned}
 s(K)&=\sum_{ij}K_{ij}a_{ij},&
 r(K)&=\sum_{ij}K_{ij}p_i s_j,\\
 T(K)&=\sum_iK_{ii}X_i,&
 F(K)&=s(K)q+r(K).
\end{aligned}                                                   \tag{5}
\]

Summing (4) gives the full physical equation

\[
                     s(K)q^{[3]}+r(K)q^{[2]}=T(K).              \tag{6}
\]

At this boundary the clean error is

\[
                         {\cal E}(K)=F(K)^{[3]}-s(K)^2T(K).
                                                                    \tag{7}
\]

Substitute (6) into (7) and use the divided-power binomial formula.  The
terms \(s^3q^{[3]}\) and \(s^2rq^{[2]}\) cancel exactly, leaving

\[
 \boxed{\quad
        {\cal E}(K)=r(K)^{[3]}+s(K)q\,r(K)^{[2]}
        ={r(K)^2\bigl(r(K)+3s(K)q\bigr)\over6}.
       \quad}                                                   \tag{8}
\]

The second expression is only a compact ordinary-power notation for the
first; all products remain in the site-square-zero algebra.  Formula (8)
is useful because at a scalar-zero cap it retains exactly one datum:

\[
                   s(K_*)=0\quad\Longrightarrow\quad
                   {\cal E}(K_*)=r(K_*)^{[3]}.                  \tag{9}
\]

## 3. The scalar-zero point is a physical response packet

Write

\[
                         \tau=\operatorname {tr}a,
                         \alpha=a_{ab}\ne0.                     \tag{10}
\]

The last inequality is exactly the nonzero direct entry selected when the
curvature minor produces the canonical line.  Homogenously,

\[
                  s(K(u,v))=\alpha u+\tau v.                    \tag{11}
\]

Its unique zero is represented by

\[
                         K_*=\tau E_{ab}-\alpha I.               \tag{12}
\]

### 3.1 Off-diagonal selected entry

Assume \(a\ne b\).  Then every diagonal entry of \(K_*\) is
\(-\alpha\), so

\[
                         T(K_*)=-\alpha\Delta_{6,3}.             \tag{13}
\]

Moreover \(E_{ab}\) is nilpotent and

\[
                         \det K_*=(-\alpha)^3\ne0.               \tag{14}
\]

Equations (6), (9), and the gcd-one hypothesis now give precisely

\[
 \boxed{
       r_*q^{[2]}=-\alpha\Delta_{6,3},\qquad
       r_*^{[3]}\ne0,qquad r_*=\sum_{ij}(K_*)_{ij}p_i s_j.}
                                                                    \tag{15}
\]

The first equality uses every transverse target row.  The second is not
an extra genericity assumption: if \(r_*^{[3]}=0\), then \([\tau:-\alpha]\)
would be a projective clean root, contrary to gcd one.  If both endpoint
star maps are injective, the invertibility of \(K_*\) makes (15) a
nondegenerate pairing of two independent star triples.

### 3.2 Diagonal selected entry

If \(a=b\), the target coefficients at (12) are

\[
              \kappa_a(K_*)=\tau-\alpha,qquad
              \kappa_c(K_*)=-\alpha\quad(c\ne a).               \tag{16}
\]

Thus (15), with the right side replaced by
\((\tau-\alpha)X_a-\alpha\sum_{c\ne a}X_c\), remains a ternary
direct-free packet when \(\tau\ne\alpha\).  Its cap matrix is then
invertible.  The sole exceptional equation

\[
                              \tau=\alpha                         \tag{17}
\]

makes \(K_*\) rank two and leaves the exact binary target
\(-\alpha\sum_{c\ne a}X_c\).  In both cases gcd one still forces
\(r_*^{[3]}\ne0\).  Hence the diagonal route has one explicit binary
trace guard rather than an unspecified scalar-zero degeneration.

For reference, the full nine equations (4) also impose the audited
six-site incidence bounds \(|D_c|\ge4\) and the site cover on the incident
spaces of \(q\).  Thus every packet above already lies on the global
rank-budget side of the six-site response frontier; (15) adds the
invertible direct-free response and its nonnilpotence.

## 4. Gcd one is exactly a rank-six Macaulay condition

The following elementary lemma is the promised finite resultant form of
the no-root branch.

**Lemma 4.1 (binary-cubic Macaulay criterion).**  Let \(V\) be a finite
dimensional complex vector space and

\[
               E(u,v)=u^3E_0+u^2vE_1+uv^2E_2+v^3E_3
                         \in V\otimes\operatorname {Sym}^3\mathbb C^2.
                                                                    \tag{18}
\]

Let \(L\subseteq\operatorname {Sym}^3\mathbb C^2\) be the image of
\(V^*\) under \(\lambda\mapsto\lambda(E)\), and define

\[
 \mu_E:L\otimes\operatorname {Sym}^2\mathbb C^2
             \longrightarrow\operatorname {Sym}^5\mathbb C^2,
             \qquad f\otimes h\longmapsto fh.                   \tag{19}
\]

Then the following are equivalent.

1. \(E(u,v)\ne0\) for every \([u:v]\in\mathbb P^1\).
2. The nonzero scalar coordinate cubics of \(E\) have gcd one.
3. \(\mu_E\) is surjective, equivalently \(\operatorname {rank}\mu_E=6\).
4. Two scalar linear combinations \(f,g\in L\) have nonzero classical
   cubic resultant.

**Proof.**  The first two assertions are equivalent because every
positive-degree homogeneous binary gcd has a projective zero over
\(\mathbb C\).  If the coordinate cubics have a common linear factor
\(\ell\), then the image of (19) lies in the five-dimensional space
\(\ell\operatorname {Sym}^4\mathbb C^2\), so (19) is not surjective.

Conversely, choose any nonzero \(f\in L\).  At each of its at most three
projective roots, gcd one says that some member of \(L\) does not vanish.
A linear combination outside the resulting finite union of hyperplanes
therefore gives \(g\in L\) with \(\gcd(f,g)=1\).  Now

\[
 f\operatorname {Sym}^2\mathbb C^2
       \cap g\operatorname {Sym}^2\mathbb C^2=0:                \tag{20}
\]

indeed \(fh=gk\), with \(\deg h=\deg k=2<3\), and coprimality force
\(h=k=0\).  The two summands in (20) each have dimension three, so their
sum is all of the six-dimensional \(\operatorname {Sym}^5\mathbb C^2\).
This proves surjectivity.  The same map restricted to the two summands is
the cubic Sylvester map; its determinant is the resultant of \(f,g\).
\(\square\)

Choose a basis of \(V\), and write a scalar coordinate as

\[
                          e(u,v)=c_0u^3+c_1u^2v+c_2uv^2+c_3v^3. \tag{21}
\]

In the monomial bases of degrees two and five, its three columns in the
matrix of (19) are the Toeplitz block

\[
 \begin{pmatrix}
 c_0&0&0\\
 c_1&c_0&0\\
 c_2&c_1&c_0\\
 c_3&c_2&c_1\\
 0&c_3&c_2\\
 0&0&c_3
 \end{pmatrix}.                                                \tag{22}
\]

Consequently gcd one is certified by one nonzero \(6\times6\) minor of
the concatenation of (22).  Such a minor uses only six shifted columns,
hence at most six scalar coordinate rows.  This is the promised bounded
certificate.

## 5. The certificate is a literal transverse four-cut determinant

Fix residual sites \(x,y\), put \(D=W\setminus\{x,y\}\), and fix endpoint
colours \(c,d\).  Decompose the selected coefficients of \(q\) and
\(F(K(u,v))\) as

\[
\begin{aligned}
 q&=z+e_{x,c}t_c+e_{y,d}v_d+e_{x,c}e_{y,d}U_{cd}+\cdots,\\
 F&=f+e_{x,c}L_c+e_{y,d}H_d+e_{x,c}e_{y,d}M_{cd}+\cdots.
\end{aligned}                                                   \tag{23}
\]

Here \(z,t_c,v_d,U_{cd}\) are fixed physical coefficients of \(q\),
whereas \(s,f,L_c,H_d,M_{cd}\) are homogeneous linear forms in \((u,v)\).
At \(h=3\), formulas (15)--(16) of the four-cut ledger become

\[
\begin{aligned}
 P_{cd}={}&M_{cd}z^{[2]}
 +(L_cv_d+H_dt_c+fU_{cd})z+ft_cv_d\\
 &\quad-2s\bigl(U_{cd}z^{[2]}+t_cv_dz\bigr)
       =\delta_{cd}\kappa_cX_c^D,                              \tag{24}\\
 C_{cd}={}&M_{cd}f^{[2]}+L_cH_df
       =s^2\delta_{cd}\kappa_cX_c^D
                         \quad\hbox{at a clean point}.           \tag{25}
\end{aligned}
\]

The coefficient of the global clean error on this selected row is
therefore the homogeneous cubic

\[
 \boxed{\quad
                          \epsilon_{cd}=C_{cd}-s^2P_{cd}.
       \quad}                                                   \tag{26}
\]

This identity is unconditional: (24) is the physical pair equation, so
its right side is the actual selected coefficient of \(T\); subtracting
\(s^2P_{cd}\) from the selected coefficient of \(F^{[3]}\) gives (7).
In particular the pure target on the right of (24) cancels, and no target
row is discarded.

For a word \(\omega\) on the four sites of \(D\), let
\(\epsilon_{cd,\omega}(u,v)\) be its scalar coefficient in (26).  As
\((c,d,\omega)\) vary, these are exactly all scalar coordinates of
\({\cal E}(K(u,v))\), merely regrouped by the fixed cut \(x,y\).  Applying
Lemma 4.1 gives:

**Corollary 5.1 (six-row four-cut certificate).**  The canonical line has
coordinate gcd one if and only if, for every fixed residual pair \(x,y\),
the matrix obtained by placing the Toeplitz blocks (22) of the explicit
polynomials (26) side by side has rank six.  In that case one of its
\(6\times6\) minors is nonzero and uses six shifted columns drawn from at
most six coefficient rows \((c,d,\omega)\).

Thus the no-root obstruction can be transported through a four-site cut
without choosing representatives modulo a Hessian annihilator.  Equation
(24) retains the physical direct and star data; equation (26) is the exact
target-free determinant input.

## 6. Good-star injectivity gives a selector or a sharp sparse shore

The aggregate rank-three condition has one sitewise consequence which is
particularly well matched to Corollary 5.1.

**Lemma 6.1 (three-site selector dichotomy).**  Let

\[
                    \Psi:\mathbb C^3\longrightarrow
                         \bigoplus_{x\in W}V_x                 \tag{27}
\]

be injective, with \(|W|=6\).  Either type 1 occurs, or at least one of
types 2--3 occurs (the two sparse types may overlap).

1. There are three distinct sites \(x,y,z\), and covectors on their local
   spaces, whose three pullbacks through \(\Psi\) are linearly independent.
2. \(\Psi\) is supported on at most two sites.
3. For some exceptional site \(x_0\), the restriction of \(\Psi\) to the
   other five sites has rank at most one.

**Proof.**  For each site let

\[
          L_x=\operatorname {im}\bigl(V_x^*\to(\mathbb C^3)^*\bigr). \tag{28}
\]

The first alternative asks for an independent transversal of size three
from the six subspaces \(L_x\).  The rank form of the linear Hall--Rado
lemma says that such a transversal fails exactly when some
\(J\subseteq W\) satisfies

\[
                    \dim\sum_{x\in J}L_x+|W\setminus J|\le2.    \tag{29}
\]

Since the full sum has dimension three, (29) can occur only as follows:
\(|J|=4\) and the sum on \(J\) is zero, giving type 2, or \(|J|=5\) and
the sum on \(J\) has dimension at most one, giving type 3.  The case
\(|J|=6\) contradicts injectivity, and smaller \(J\) cannot satisfy
(29).  Conversely either sparse type plainly prevents a three-site
independent transversal.  \(\square\)

For a good deleted pair, apply Lemma 6.1 separately to its two endpoint
star maps.  In type 1 choose the transverse cut to be the first two
selector sites \(x,y\).  The restriction of the star to these two sites
has rank at least two, while the four-site complement contains the third
selector direction and raises the total rank to three.  Corollary 5.1 says
that the **whole** Macaulay matrix in this cut ledger has rank six.  It does
not say that one can choose its nonzero minor entirely from coordinate
rows exposed by the selector; that incidence statement is an additional
lemma, not a consequence of injectivity.

The curved full-good-fan guard lies in the sparse side of this lemma: away
from its distinguished residual site, each displayed endpoint star has at
most one surviving row direction.  Hence aggregate rank three alone does
not remove types 2--3, while the selector branch does remove the guard's
mechanism.

## 7. Exact residual for the next coupling argument

The preceding statements package as one precise alternative.

**Theorem 7.1 (first-boundary rootless-line packet).**  Assume the complete
pair equations (4), let \(a_{ab}\ne0\), and suppose both endpoint star maps
are injective.  If the clean-error coordinates on (1) have gcd one, then:

1. the scalar-zero cap (12) satisfies the direct-free response and
   nonnilpotence equations (15), with the modified target following (16)
   in the diagonal case; its only failure there to be ternary and invertible
   is the explicit binary trace guard (17);
2. on every residual two-site cut, the matrix formed from (22) and the
   physical four-cut polynomials (24)--(26) has rank six, hence has a
   nonzero \(6\times6\) minor using six shifted columns drawn from at most
   six coefficient rows;
3. each endpoint star independently has either a three-site selector or
   one of the two sparse forms in Lemma 6.1.  In the selector case the
   full rank-six ledger can be indexed by a cut where that endpoint has a
   rank-two restriction and a third independent complementary direction;
   no support claim is made about the columns of the witnessing minor.

**Proof.**  Item 1 is (9)--(17), item 2 is Lemma 4.1 and Corollary 5.1,
and item 3 is Lemma 6.1.  No generic-rank or dimension assertion is used.
\(\square\)

At the first boundary, the gcd-one branch of a nonzero canonical curvature
line is therefore reduced to finite data.

* At the scalar-zero point it has the nonnilpotent packet (15), or the
  diagonal binary trace guard (17).
* On every four-cut it has a nonzero \(6\times6\) determinant formed from
  the displayed physical polynomials (24)--(26).
* At each good endpoint it either has a three-site selector meeting such a
  cut, or one of the two explicit sparse shores in Lemma 6.1.

Therefore a positive continuation need not prove a common-root theorem for
an arbitrary vector cubic.  It is enough to prove one of the following
bounded statements across two curvature lines sharing a fan centre:

1. the two scalar-zero packets cannot both be nonnilpotent while their
   complete transverse target rows agree;
2. the selector coordinates meet every possible rank-six Macaulay minor,
   and the resulting common-edge syzygy forces all such minors to vanish;
   or
3. a type-2/type-3 sparse endpoint propagates to the already registered
   low-degree or one-neighbour star contradiction.

No executable is needed.  The only polynomial assertion, Lemma 4.1, is
the six-dimensional Sylvester identity; (8), (15), and (24)--(26) are
literal divided-power expansions of the physical pair equations.

There is also a sharp scope reason not to advertise a one-pair
countermodel satisfying all of (4).  Given \(q,p_i,s_j,a_{ij}\), attach two
new sites \(p,q\) with these internal, star, and direct blocks.  Sorting
eight-site perfect matchings by the colours at \(p,q\) gives exactly the
nine equations (4).  Thus a physical countermodel to the complete
six-site transverse system is already an exact eight-site Krenn
counterexample.  Formal guards may omit a row of (4), a power condition,
or common-edge provenance; none can refute Theorem 7.1 while retaining the
complete physical system.

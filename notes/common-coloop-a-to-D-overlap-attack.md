# The common-coloop \(A\)-to-\(D(z)\) overlap attack

## 1. Verdict

Let \(x\) be a common coloop and use the literal full-nine notation

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                                    \tag{1}
\]

Put \(q=q_0+\rho\), \(A=q_0^{[h-1]}\), and let

\[
 D_{\bar K}(z)=(zq_0+\bar r)^{[h-1]}-z^{h-1}A.             \tag{2}
\]

The exact affine-fibre formula shows that the nine anchor rows act through
multiplication by \(A\), whereas cleanliness acts through multiplication by
\(D_{\bar K}(z)\).  This note records three sharply separated conclusions.

1. **Theorem (exact projected obstruction).**  In an aligned one-corner
   branch, the missing-axis polynomial is an unavoidable necessary
   condition at the *same attainable scalar* \(z\).  The scalar and the
   tangent response cannot be chosen independently, and the three diagonal
   base loci remain separate affine hyperplanes.
2. **Conditional reduction.**  At \(h=3\), for a curvature-only missing row
   with zero missing local response, the whole missing-axis obstruction is
   the second-polar tensor

   \[
                    z\rho_t\bar r^{[2]}.                    \tag{3}
   \]

   Thus an active clean cap would force
   \(\rho_t\bar r^{[2]}=0\).
3. **False lemma.**  The \(A\)-level anchor consequences do **not** force
   this second-polar vanishing.  Section 5 gives an exact rational
   five-site guard with one actual \(q_0\), \(A=q_0^{[2]}\ne0\), a target
   class outside \(\mathcal R_1A\), three exact \(A\)-annihilators, an
   endpoint-decomposable response \(\bar r=ps\), and the exact missing
   diagonal row, but

   \[
                  \rho_t\bar r^{[2]}={3\over2}Y_t\ne0.      \tag{4}
   \]

The guard proves that the natural implication from the *missing-row*
\(A\)-annihilations and curvature anchor to the \(D(z)\)-equation is
false.  It is **not** a literal full-nine source: the two other diagonal
anchor rows and a nonflat second physical chart are not supplied.
Consequently a theorem using those rows before multiplication by \(A\)
remains possible and is exactly what is still required.

## 2. The exact affine-fibre and activity ledger

Let \(c,d\) span the two off-\(x\) kernel lines and put

\[
 \mathcal T=(\mathbb Cc)\otimes D+C\otimes(\mathbb Cd).
\]

Write

\[
 L=c\eta^{\mathsf T}+\xi d^{\mathsf T},\qquad
 b=c^{\mathsf T}a,\qquad g=ad.                              \tag{5}
\]

For a fixed representative \(K_0\), the direct scalar and the three
diagonal coordinates on \(K_0+\mathcal T\) are

\[
 \boxed{
 \begin{aligned}
 z&=\sigma_0+b\eta+\xi^{\mathsf T}g,\\
 \kappa_i&=\kappa_i^0+c_i\eta_i+\xi_i d_i.
 \end{aligned}}                                             \tag{6}
\]

The same parameters determine the tangent response:

\[
 w(L)=u\,\bar S(\eta)+\bar P(\xi)\,v.                       \tag{7}
\]

Equations (6)--(7) are the coupling which must be retained.  In particular,
solving a tensor equation for an arbitrary pair \((z,w)\) is not a valid
affine-fibre argument.

Suppose \(t\) is the missing label in a singleton or binary one-corner
branch.  Then

\[
                    c_t=d_t=0,
 \qquad             \kappa_t=\kappa_t^0.                   \tag{8}
\]

On the aligned branch, \(u,v\) have no \(e_t^{(x)}\)-component, so

\[
                          w(L)_t=0.                          \tag{9}
\]

There are four activity factors, with no genericity convention:

\[
                  z\kappa_0\kappa_1\kappa_2.                \tag{10}
\]

Thus the scalar base locus is the affine hyperplane given by the first
line of (6), while each diagonal base locus is the corresponding affine
hyperplane in the second line.  If \(c=e_r\) and \(d=e_s\), \(r\ne s\),
then more explicitly

\[
 \kappa_r=\kappa_r^0+\eta_r,
 \qquad
 \kappa_s=\kappa_s^0+\xi_s,
 \qquad
 \kappa_t=\kappa_t^0.                                      \tag{11}
\]

For binary \(c,d\), both nonmissing diagonal forms are the corresponding
linear combinations in (6); the missing diagonal is still fixed.  Over
\(\mathbb C\), avoiding the three diagonal hyperplanes is legitimate only
*after* the clean system has been solved on its affine solution space.

## 3. The projected missing-axis theorem

Decompose the response of \(K_0\) and the local part of \(q\) as

\[
 r(K_0)=\bar r+\chi,
 \qquad
 \rho=\sum_i e_i^{(x)}\rho_i,
 \qquad
 \chi=\sum_i e_i^{(x)}\chi_i.                              \tag{12}
\]

The exact clean error on the affine fibre is

\[
 \mathcal E(K_0+L)
  =(z\rho+\chi+w)D_{\bar K}(z)
       -z^{h-1}\bar r\rho q_0^{[h-2]}.                     \tag{13}
\]

Projecting (13) onto the missing local axis and using (9) gives

\[
 \boxed{
 \Theta_t(z)=
   \chi_tD_{\bar K}(z)
   +\rho_t\sum_{j=2}^{h-1}
       z^{h-j}\bar r^{[j]}q_0^{[h-1-j]}.
 }                                                           \tag{14}
\]

The fixed diagonal row is

\[
 (z\rho_t+\chi_t)A
       +\rho_t\bar r q_0^{[h-2]}
             =\kappa_t^0Y_t.                                \tag{15}
\]

If \(z\) varies on the fibre, (15) first gives \(\rho_tA=0\), and its
remaining part is independent of \(z\).

**Theorem 3.1 (exact missing-axis obstruction).**  Let \(Z_{\rm att}\)
be the image of the first affine functional in (6).  If

\[
                 \Theta_t(z)\ne0
       \quad\hbox{for every }z\in Z_{\rm att}\setminus\{0\}, \tag{16}
\]

then the fibre contains no active clean cap.

**Proof.**  Every clean cap must satisfy every local-axis projection of
(13), hence (14).  Every active cap has \(z\ne0\) by (10), and its \(z\)
belongs to \(Z_{\rm att}\) by (6).  This contradicts (16).  Notice that no
claim about the other two local-axis equations, or about the diagonal
hyperplanes, is needed for this one-way obstruction.  \(\square\)

The converse is false without the rest of the affine system: a nonzero
root of (14) is only a necessary condition.  One must still solve (13)
with the coupled response (7) and then check all three diagonal
noncontainments.

## 4. The first-boundary conditional reduction

At \(h=3\), equations (2) and (14) are

\[
 \begin{aligned}
 D_{\bar K}(z)&=z\bar r q_0+\bar r^{[2]},\\
 \Theta_t(z)&=
   \chi_t(z\bar r q_0+\bar r^{[2]})
       +z\rho_t\bar r^{[2]}.
 \end{aligned}                                               \tag{17}
\]

Consider the exact subcase

\[
 \chi_t=0,
 \qquad
 \rho_tA=0,
 \qquad
 \rho_t\bar r q_0=\kappa_t^0Y_t,
 \qquad \kappa_t^0\ne0.                                    \tag{18}
\]

The last equation is the curvature-only form of the fixed missing
diagonal anchor (15).  Then

\[
                  \boxed{\Theta_t(z)=z\rho_t\bar r^{[2]}.}   \tag{19}
\]

This is a **conditional reduction**, not an active-cap theorem:

* if \(\rho_t\bar r^{[2]}\ne0\), Theorem 3.1 excludes every active clean
  cap in the fibre;
* if \(\rho_t\bar r^{[2]}=0\), only the missing local-axis equation has
  disappeared; the other local axes, the \(z/w\) incidence, and all
  diagonal hyperplanes still remain.

For a missing diagonal row represented by \(K_0=E_{tt}\), one naturally
has an endpoint-decomposable off-site response

\[
                         \bar r=ps.                           \tag{20}
\]

The binary and zero-power singleton anchor equations can also give
\(pA=sA=0\).  The tempting \(A\)-to-\(D\) shortcut is therefore the
following assertion.

> **False lemma (anchor-to-second-polar transfer).**  If
> \(A=q_0^{[2]}\), \(Y_t\notin\mathcal R_1A\),
> \(\rho_tA=pA=sA=0\), and the exact curvature anchor
> \(\rho_t(ps)q_0=\kappa_tY_t\ne0\) holds, then
> \(\rho_t(ps)^{[2]}=0\), or at least (19) has a nonzero root.

Section 5 disproves both conclusions with rational coefficients.

## 5. An exact consecutive-power counterguard

Let the odd set be \(K=\{0,1,2,3,4\}\).  At each site use two independent
physical axes

\[
                 a_i=e_0^{(i)},\qquad x_i=e_2^{(i)}.
\]

All products are in the site-square-zero algebra.  Define the actual
quadratic

\[
 q_0=x_0x_1+x_0x_2+x_0x_3+x_0x_4+a_1a_2.                   \tag{21}
\]

Only the last edge is disjoint from either \(x_0x_3\) or \(x_0x_4\).
Consequently its literal second divided power is

\[
 A=q_0^{[2]}
   =x_0a_1a_2x_3+x_0a_1a_2x_4.                             \tag{22}
\]

Put

\[
 \ell=-x_0-x_1-x_2-x_3+x_4,
 \qquad
 \rho_t=-x_1-x_2,                                         \tag{23}
\]

and take the two endpoint forms and their response to be

\[
                 p={1\over4}\ell,qquad s=\ell,qquad
                 \bar r=ps={1\over4}\ell^2.                \tag{24}
\]

Equations (22)--(23) give, coefficient for coefficient,

\[
 \ell A=
   x_0a_1a_2x_3x_4-x_0a_1a_2x_3x_4=0,
 \qquad
 \rho_tA=0.                                                 \tag{25}
\]

Hence \(pA=sA=\rho_tA=0\).  Nevertheless, if

\[
                         Y_t=x_0x_1x_2x_3x_4,                \tag{26}
\]

then direct multiplication gives

\[
 \boxed{
   \rho_t\bar r q_0=Y_t,
   \qquad
   \rho_t\bar r^{[2]}={3\over2}Y_t.
 }                                                           \tag{27}
\]

Here is a coefficient audit which keeps the divided powers visible.
The \(a_1a_2\)-term in the first product in (27) vanishes because
\(\rho_t\) is supported at sites \(1,2\).  In the all-\(x\) component,

\[
 [\rho_t\ell^2(x_0x_1+x_0x_2+x_0x_3+x_0x_4)]_{Y_t}=4,
\]

which becomes \(1\) after the factor \(1/4\) in (24).  Also

\[
 \bar r^{[2]}={\ell^4\over32},
 \qquad
 [\rho_t\ell^4]_{Y_t}=48,
\]

giving \(48/32=3/2\).  No positivity or termwise noncancellation is being
used; these are exact rational tensor equalities.

The target in (26) is genuinely missing from the \(A\)-image:

\[
                         Y_t\notin\mathcal R_1(K)A.           \tag{28}
\]

Indeed, every monomial of \(A\) has the independent \(a_1,a_2\) axes at
sites \(1,2\), and multiplication by one linear form cannot change either
occupied local factor into \(x_1,x_2\).

Now add the exposed site \(x\), write
\(\epsilon=e_2^{(x)}\), and set

\[
                   q=q_0+\epsilon\rho_t.                    \tag{29}
\]

Because \(\rho_tA=0\), the consecutive powers are

\[
 q^{[3]}=0,
 \qquad
 q^{[2]}=A+\epsilon\rho_tq_0.                               \tag{30}
\]

The response (24) supplies the exact missing diagonal row

\[
              \bar r q^{[2]}
                  =\epsilon\rho_t\bar r q_0
                  =\epsilon Y_t=:X_t.                       \tag{31}
\]

Thus (31) is not a formal independent-\((A,B)\) packet: it uses one actual
quadratic and its literal consecutive divided powers, and its response is
the product of two endpoint forms.

For any direct scalar \(z\), put

\[
                         F_z=zq+\bar r.                       \tag{32}
\]

The physical row (31) is independent of \(z\), since \(q^{[3]}=0\).  A
direct expansion, or (19) and (27), yields

\[
 \boxed{
 F_z^{[3]}-z^2X_t={3\over2}zX_t.
 }                                                           \tag{33}
\]

Consequently the row is clean only at \(z=0\), where the direct scalar is
inactive.  Equivalently,

\[
 D_{\bar K}(z)=z\bar r q_0+\bar r^{[2]},
 \qquad
 \Theta_t(z)={3\over2}zY_t.                                 \tag{34}
\]

This proves that the false lemma in Section 4 is false.

## 6. Exact interaction with \(z/w\) coupling and diagonals

The guard does not promote \(z\) to a freely selectable auxiliary
variable.  In a physical common-coloop fibre it must still be the affine
functional in (6), and \(w\) must still be (7).  What makes the guard
decisive for the proposed shortcut is (9): no allowed tangent response has
an \(e_t^{(x)}\)-component.  Therefore no choice of \(w\) can cancel the
nonzero missing-axis coefficient in (34).

There are only two possibilities for the attainable scalar set.

* If \(\sigma|_{\mathcal T}\ne0\), every \(z\in\mathbb C\) is attainable,
  but (34) forces \(z=0\), which lies on the scalar activity hyperplane.
* If \(\sigma|_{\mathcal T}=0\), the sole attainable value is
  \(z=\sigma_0\).  It is either zero and inactive, or nonzero and excluded
  by (34).

The fixed missing diagonal in the guard is \(\kappa_t=1\).  The two other
diagonal forms are exactly those in (6), or (11) in the disjoint singleton
normalization.  They may or may not be avoidable on a full solution fibre;
that question cannot rescue the guard, because the missing-axis equation
has already forced the scalar activity factor to vanish.  Conversely, the
guard makes no claim that a point satisfying (34) would automatically avoid
those diagonal hyperplanes.

## 7. What is proved, what is conditional, and what remains open

The logical status is as follows.

* **Proved theorem:** The projected equation (14), the attainable-scalar
  obstruction in Theorem 3.1, and the complete activity ledger
  (6)--(11).
* **Proved conditional reduction:** Under (18), the first-boundary missing
  equation is exactly (19).  Its vanishing is necessary but not sufficient
  for an active clean cap.
* **Proved false lemma:** The exact data (21)--(31) satisfy
  \(A=q_0^{[2]}\ne0\), \(Y_t\notin\mathcal R_1A\),
  \(pA=sA=\rho_tA=0\), the decomposable missing anchor
  \(\rho_t(ps)q_0=Y_t\), and yet the second polar is nonzero.  Thus
  multiplication by \(A\) does not control multiplication by
  \(D_{\bar K}(z)\).
* **Not proved or disproved:** A literal full-nine active-cap lemma.  The
  guard does not supply the two nonmissing diagonal target rows, a complete
  matrix \(a\), or a second source-provenant chart with nonzero overlap
  curvature.  In particular it is not an eight-site Krenn source.

The omitted rows are not cosmetic.  They would have to rule out the exact
second-polar defect in (27) while retaining their representatives before
multiplication by \(A\).  The guard does not decide whether the two
nonmissing lift equations can do this; it proves only that the displayed
missing-row annihilations and flat transport cannot.  A successful
full-nine proof must therefore extract from the omitted anchor
representatives, or from a nonflat physical overlap, a genuinely
source-relative relation involving \(\rho_t\bar r^{[2]}\) (and, for
\(h>3\), the higher terms in (14)), together with the same coupled
\((z,w)\) parameters and the three diagonal noncontainment tests.

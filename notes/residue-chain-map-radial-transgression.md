# The Hermite lift reduces to one radial-to-response transgression

## 1. Outcome

Let \(d\geq1\), let

\[
 \Omega\in V\otimes\mathbb C[t,u]_d,
 \qquad H\in V^*\otimes\mathbb C[t,u]_d,
 \qquad \langle H,\Omega\rangle=(tu)^d,                 \tag{1}
\]

and let \(0\ne\widehat\zeta_c\in C\) be the normalized odd residue on a
routed inactive line.  Thus \(d=h-1\) on a one-clean off-diagonal line and
\(d=h-2\) when both endpoints are clean.  The torus--Koszul calculation
requires a physical correction \(G_c\in C\otimes\mathbb C[t,u]_{2d}\)
with

\[
                         [t^du^d]G_c=-\widehat\zeta_c.    \tag{2}
\]

This note separates (2) into two stages and solves the second stage
uniformly.

Suppose the filtered overlap supplies a **radial-to-response
transgression**

\[
 \tau_c(\gamma(a,b)z)=\gamma(a,b)\widehat\zeta_c,        \tag{3}
\]

on its curvature-normal quotient.  Here \(z\) is the common internal
quadratic and

\[
             \gamma(a,b)=\kappa a+\lambda b,
             \qquad \kappa=AU-BF\ne0,                    \tag{4}
\]

is the physical curvature form on the tilted overlap line.  Take the
ordered complementary endpoint form

\[
                         \ell={b\over\kappa}.             \tag{5}
\]

For the alternating bracket normalized by \([a,b]=1\), equations
(4)--(5) give \([\gamma,\ell]=1\).  The explicit prolongation

\[
 \boxed{
 G_c=-[\gamma,\ell]\,\widehat\zeta_c
                         \langle H,\Omega\rangle
     =-\widehat\zeta_c(tu)^d }                            \tag{6}
\]

has degree \(2d\), is linear in the curvature carrier after (3), is
independent of the chosen bounded certificate, and satisfies the full
coefficient equation

\[
       \widehat\zeta_c\langle H,\Omega\rangle+G_c=0.      \tag{7}
\]

Thus it satisfies not only (2), but the torus--Koszul equation with zero
primitive.  There is no remaining all-order Hermite interpolation problem
after (3).  The same construction on the direct-free packet uses

\[
 \tau_c(AUz)=AU\widehat\zeta_c,
 \qquad
 G_c=-(AU)^{-1}\tau_c(AUz)\langle H,\Omega\rangle,        \tag{8}
\]

where \(AU\ne0\).

The substantive point is that (3) is not furnished by the raw triangular
identity.  On the odd overlap, the ordinary residue of the radial
quadratic \(z=q_0\) is zero.  Consequently every prolongation obtained by
coefficientwise scalar multiplication of

\[
                         C_4-Dv=AUz                         \tag{9}
\]

has zero odd residue.  A nonzero map (3) must therefore retain more of the
source filtration than the radial associated graded.  Section 6 identifies
the exact source-valid response--target syzygy exposed by the two canonical
cap lifts:

\[
            \left(\alpha^{-1}R_{\rm ev},
                         -\Delta_{2h,3}\right),           \tag{10}
\]

whose quadratic coordinate has residue

\[
 \operatorname {res}_{q_0}(\alpha^{-1}R;t_c)
                    =-\overline Y_c=\widehat\zeta_c.      \tag{11}
\]

Equation (10), not its response coordinate alone, is the legal literal
object.  The caps compare two lifts of \(\tau q\), where
\(\tau=\operatorname {tr}A\).  If \(\tau\ne0\), then after dividing by the
common radial scalar and by the canonical cap factor \(h\), their normalized
lift-difference per copy of \(q\) is \(R/(\alpha\tau)\), not
\(\alpha^{-1}R\).  If \(\tau=0\), both radial symbols are zero and the caps
define no transgression out of \(q\) at all.  Thus Section 6 does not prove
(3).

It also proves that no literal quadratic identity on the same
\(q\)-complement can cancel the target in (10) without cancelling the
response: the target coefficient and odd residue are locked.  The remaining
route isolated here is therefore a comparison between genuinely different
\(q\)/power quotients, with target cancellation taking place in a mapping
cone rather than inside one literal quadratic row.  Constructing that
comparison is an order-zero source-filtration problem, not a degree-\(2d\)
coefficient problem.  It is not proved here, and the conjecture remains
open.

In the minimum-order reduction, the separate
[odd-residue survival lemma](odd-residue-minimality-survival.md) proves
that at least one \(\overline Y_c\), and hence at least one
\(\widehat\zeta_c\), is nonzero on the off-diagonal scalar-zero packet.
Thus the nonzero hypothesis above is automatic on that branch; the
transgression is the effective obstruction rather than a potentially
vacuous target.

## 2. The radial annihilation lemma

Let \(K\) be the odd set of \(2h-1\) sites and put

\[
 A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},\qquad
 C_{q_0}={{\cal R}_{2h-1}(K)\over {\cal R}_1(K)A}.        \tag{12}
\]

For a linear form \(T\) on \(K\), write

\[
              \rho_T(Z)=[TZB]\in C_{q_0}.               \tag{13}
\]

Divided-power multiplication gives

\[
                         q_0B=(h-1)A.                     \tag{14}
\]

It follows immediately that

\[
 \boxed{\rho_T(q_0)=(h-1)[TA]=0.}                         \tag{15}
\]

The near-perfect gauge identity also gives

\[
                         \rho_T(Z_{q_0}^{\beta})=0        \tag{16}
\]

for every vertex-gauge quadratic \(Z_{q_0}^{\beta}\).  Hence \(\rho_T\)
annihilates the whole radial/gauge subspace

\[
 {\cal N}_{q_0}=\mathbb Cq_0+
                 \Gamma_{q_0}(\mathfrak t_K)\subseteq
                 {\cal R}_2(K).                           \tag{17}
\]

Tensoring with binary coefficients does not change this:

\[
 (\rho_T\otimes1)(Q(t,u))=0
 \quad\text{for every}\quad
 Q\in{\cal N}_{q_0}\otimes\mathbb C[t,u].               \tag{18}
\]

**Radial annihilation lemma.**  Any proposed overlap correction whose
quadratic representative is, coefficient by coefficient, a scalar
multiple of \(z=q_0\) plus a vertex gauge has zero odd residue in every
binary degree.  In particular, applying the canonical odd residue after
any scalar polynomial prolongation of (9) cannot satisfy (2) when
\(\widehat\zeta_c\ne0\).

This is stronger than saying that the triangular split does not define a
prolongation.  It shows that the most literal such prolongation is the
wrong kind: it factors through a subspace killed by the target functor.
The desired map must retain a filtration extension which is lost after
replacing the left side of (9) by \(AUz\).  In homological language, the
needed class is a connecting morphism, not the map induced on the radial
associated graded.

For the off-diagonal scalar-zero response, equation (11) proves that the
quadratic \(-\alpha^{-1}R\) has the residue required by (2).  Algebraically,
it is sufficient modulo the kernel of the one fixed residue functional: if
a quadratic-valued middle coefficient \(Q_c\) is used, then (2) is exactly

\[
 \rho_{t_c}(Q_c)=-\widehat\zeta_c,
 \quad\text{so one may take}\quad Q_c=-\alpha^{-1}R.      \tag{19}
\]

No injectivity of the residue map and no physical provenance for this
quadratic alone are asserted.  Its opposite
\(+\alpha^{-1}R\) has residue \(+\widehat\zeta_c\), while the outer minus
in (6) would make the correction representative
\(-\alpha^{-1}R\), whose residue is \(-\widehat\zeta_c\) as in (19).
Section 6 shows that the literal cap source ties the former quadratic to
the target \(-\Delta_{2h,3}\); it does not supply the hypothesized map (3).

## 3. Why the curvature form needs one odd endpoint input

Let \(U_\parallel\) be the clean-pencil parameter space and
\(U_\perp\) the independent tilted-auxiliary parameter space.  Put
\(S_n^\parallel=\operatorname {Sym}^nU_\parallel^*\) and
\(S_n^\perp=\operatorname {Sym}^nU_\perp^*\).  The certificate scalar is

\[
 P=\langle H,\Omega\rangle\in S_{2d}^\parallel,          \tag{20}
\]

whereas the curvature carrier is
\(\gamma\in S_1^\perp\).  The target \(S_{2d}^\parallel\) is trivial under
\(SL(U_\perp)\), so there is no nonzero natural operation

\[
 S_1^\perp\otimes S_{2d}^\parallel
          \longrightarrow S_{2d}^\parallel.              \tag{21}
\]

The central element \(-I\in SL(U_\perp)\) already proves this.  Thus a
linear chain map cannot silently remove the odd transverse curvature
factor.  It needs one additional odd transverse input.  The ordered
endpoint form \(\ell=b/\kappa\) in (5) is exactly such an input and is
available because \(\kappa\ne0\).

Moreover,

\[
 \dim\left(S_1^\perp\otimes S_1^\perp\right)^{SL(U_\perp)}
 =1.                                                       \tag{22}
\]

The invariant is the alternating bracket.  Writing

\[
 \gamma=\kappa a+\lambda b,\qquad
 \ell=ca+eb,\qquad P=t^du^d,                              \tag{23}
\]

gives

\[
                         [\gamma,\ell]=\kappa e-\lambda c. \tag{24}
\]

Consequently the unique natural operation which remains on the central
certificate line is

\[
                         (\gamma,\ell;P)\longmapsto
                              [\gamma,\ell]P.             \tag{25}
\]

If one additionally chooses a projective identification
\(U_\perp\simeq U_\parallel\), there is a second equivariant operation,
the first transvectant \((\gamma\ell,P)_1\).  It is not available from the
two independent lines without that extra identification, and in any case
it has zero middle coefficient:

\[
\begin{aligned}
 (\gamma\ell,P)_1
   &=2d\kappa c\,t^{d+1}u^{d-1}
       -2d\lambda e\,t^{d-1}u^{d+1},\\
 [t^du^d](\gamma\ell,P)_1&=0.
\end{aligned}                                             \tag{26}
\]

Thus the bracket in (6) is not an arbitrary interpolation.  It is the
unique natural transverse contraction affecting the middle line.  For
full \(GL(U_\perp)\) naturality it carries the determinant character; the
ordered endpoint coordinates trivialize that line.

## 4. The transverse Euler test on the literal overlap

The preceding odd input has an equivalent Koszul interpretation which can
be tested directly on the all-label overlap.  Give the clean pencil
coordinates \(t,u\), and give the tilted auxiliary line independent
coordinates \(a,b\).  On

\[
 M_d=C\otimes S_{2d}(t,u)\otimes S_1(a,b)                 \tag{28}
\]

consider the two commuting Euler operators

\[
 \mathscr D_{\parallel}=t\partial_t-u\partial_u,
 \qquad
 \mathscr D_{\perp}=a\partial_a-b\partial_b.             \tag{29}
\]

The monomial

\[
                   t^{2d-n}u^na^{1-j}b^j
 \quad(0\leq n\leq2d,\ j=0,1)                            \tag{30}
\]

has joint weight

\[
                         (2(d-n),1-2j).                    \tag{31}
\]

The second coordinate is always \(1\) or \(-1\).  Hence there is no joint
weight-zero monomial, and the two-Euler Koszul complex

\[
 0\longrightarrow M_d
 \mathop{\longrightarrow}^{(-\mathscr D_\perp,
                              \mathscr D_\parallel)}
 M_d^{\oplus2}
 \mathop{\longrightarrow}^{(\mathscr D_\parallel,
                              \mathscr D_\perp)}
 M_d\longrightarrow0                                      \tag{32}
\]

is exact, weight by weight.

In particular, after granting (3), the transported certificate class on
the tilted line is

\[
 Q_c=\widehat\zeta_c(tu)^d(\kappa a+\lambda b),
 \qquad \mathscr D_\parallel Q_c=0.                       \tag{33}
\]

It has the explicit transverse primitive

\[
 Q_c=\mathscr D_\perp
       \bigl(\widehat\zeta_c(tu)^d(\kappa a-\lambda b)\bigr). \tag{34}
\]

Thus an active transverse chart genuinely removes the one-line Euler
cokernel; no higher Hermite coefficient can survive as a joint Koszul
class.  Contracting the transverse \(S_1\)-slot against the normalized
endpoint direction (5) is the bracket construction (6).

It is essential, however, to apply this test to the literal source row.
Write the all-label curvature identity schematically, after moving its
ordinary connection term to the left, as

\[
                     \mathcal B_{bd}(K)=\Gamma_{bd}(K)z. \tag{35}
\]

On \(K(a,b)=aE_{ac}+bJ\), its right side is
\((\kappa a+\lambda b)z\).  Restricting \(z\) to the odd common quadratic
\(q_0\) and applying the canonical residue gives, by (15),

\[
 (\rho_{t_c}\otimes1)
       \bigl((\kappa a+\lambda b)q_0\bigr)=0.             \tag{36}
\]

Therefore the literal row followed by the ordinary odd-residue functor
does **not** produce (33).  The two-Euler mechanism becomes operative only
after a source-filtered connecting morphism supplies (3).  This is a
concrete failure on the displayed all-label identity, not merely an
abstract bicomplex analogy.

The direct-free packet has a sharper limitation.  In

\[
                         C_4-Dv=AUz                         \tag{37}
\]

the curvature coefficient \(AU\) has transverse order zero.  On
\(C\otimes S_{2d}(t,u)\otimes S_0(a,b)\), the element
\(\widehat\zeta_c(tu)^d AU\) has joint weight \((0,0)\), so the second
Euler operator supplies no primitive.  One may formally tag (37) by an
external \(a\)-factor, but proving that this tag belongs to the same
filtered physical comparison is exactly new provenance, not a consequence
of triangularity.  Hence:

* an active tilted auxiliary has no coefficient-level joint-weight
  obstruction once (3) is known;
* the literal residue still kills its radial carrier before (3); and
* a genuinely direct-free auxiliary retains the joint middle class unless
  a filtered transgression or a source-provenant transverse line is added.

## 5. The coefficient prolongation theorem

The preceding calculation can be packaged independently of the physical
source complex.

**Theorem 5.1 (certificate-bracket prolongation).**  Let \(C\) be a vector
space, \(d\geq1\), and let (1) hold.  Fix
\(\gamma,\ell\in S_1^\perp\) with \([\gamma,\ell]\ne0\).  If a linear filtered
normal map produces

\[
                         \tau(\gamma z)=\gamma\zeta
                         \quad(\zeta\in C),               \tag{38}
\]

then

\[
 \mathcal P_{\ell,H,\Omega}(\tau(\gamma z))
   :=-[\gamma,\ell]^{-1}
       [\tau(\gamma z),\ell]\,\langle H,\Omega\rangle
   =-\zeta(tu)^d                                           \tag{39}
\]

is a degree-\(2d\) correction satisfying

\[
 \zeta\langle H,\Omega\rangle+
 \mathcal P_{\ell,H,\Omega}(\tau(\gamma z))=0.           \tag{40}
\]

More invariantly, before normalizing the source carrier, the numerator is
\(-[\gamma,\ell]\zeta\langle H,\Omega\rangle\), and one divides only by
the known nonzero scalar \([\gamma,\ell]\).  No site form, matching power,
or polynomial in \(t,u\) is divided out.

**Proof.**  Equation (1) turns the right side of (39) into
\(-\zeta(tu)^d\).  This has the required degree and cancels the certificate
term coefficient by coefficient.  Linearity in the carrier follows from
linearity of the alternating bracket.  If \(H'\) is another certificate,
then both contractions equal \((tu)^d\), so the output is unchanged.
\(\square\)

Here \([\tau(\gamma z),\ell]\) means applying the alternating bracket to
the \(S_1^\perp\)-slot of (38).  In the physical tilted normalization (4), take
(5), so no displayed division remains in (6).  The theorem does not assert
(38).  Rather, it
shows that all of the higher Hermite shifts and the torus--Koszul primitive
are formal once that one filtered normal value is known.

## 6. The cap lift-difference and the same-complement lock

The scalar-zero cap makes the domain and filtration of the missing map
explicit.  Expose one site \(x\), let \(D\) be the remaining odd
complement, and write

\[
\begin{aligned}
 q&=q_0+\sum_j e_j^{(x)}t_j,\\
 r(K)&=\overline r(K)+\sum_j e_j^{(x)}n_j(K).
\end{aligned}                                               \tag{41}
\]

In the raw normalization the canonical cap is

\[
                        {\cal P}(K)=h\,r(K)+s(K)q.         \tag{42}
\]

Its internal and colour-\(c\) normal pieces are

\[
\begin{aligned}
 p(K)&=h\,\overline r(K)+s(K)q_0\in{\cal R}_2(D),\\
 \ell_c(K)&=h\,n_c(K)+s(K)t_c\in{\cal R}_1(D).
\end{aligned}                                               \tag{43}
\]

The coefficient at \(x,c\) of the literal cap equation is the two-step
filtered multiplication

\[
 \boxed{
 d_c(\ell,p):=\ell A+p\,t_cB=h\,T_c(K).}                  \tag{44}
\]

Here the normal submodule \({\cal R}_1(D)A\) is filtration one and the
internal response \(p\,t_cB\) is filtration zero.  Passing to \(C_{q_0}\)
gives the exact associated-quotient formula

\[
 \pi_{q_0}d_c(\ell_c(K),p(K))
   =\rho_{t_c}(p(K))
   =h\,\rho_{t_c}(\overline r(K)),                         \tag{45}
\]

because the \(s(K)q_0\) summand is radial and vanishes by (15).

At the off-diagonal scalar-zero point \(K_1\),

\[
 s(K_1)=0,\qquad \overline r(K_1)=R,\qquad
 T_c(K_1)=-\alpha Y_c.                                    \tag{46}
\]

Consequently

\[
\begin{aligned}
 p(K_1)&=hR,\qquad \ell_c(K_1)=h n_c,\\
 d_c(hn_c,hR)&=-h\alpha Y_c,\\
 (h\alpha)^{-1}\rho_{t_c}(p(K_1))
    &=-\overline Y_c=\widehat\zeta_c.                     \tag{47}
\end{aligned}
\]

Thus the scalar-zero contraction does supply the response representative
\(\alpha^{-1}R\) and its residue.  It does **not** supply a map from the
radial carrier \(z=q_0\) to that response.  At \(s(K_1)=0\), the \(q_0\)
term has disappeared from (43); equation (42) contains \(hR\), not a
relation between \(R\) and \(q_0\).

The existing overlap confirms this failure rather than repairing it.  The
power-free connection has the form

\[
                    P_{pq}t-P_{pr}y=Dq_0.                \tag{48}
\]

Applying the one-site cap quotient to (48) gives equality of the two cap
residues, because the right side has zero residue.  This is precisely the
flat transport law already proved for the odd corner.  Likewise the
curvature row gives

\[
                  \rho_{t_c}(\Gamma(K)q_0)=0.            \tag{49}
\]

Concretely, contracting the all-label normal connection by
\(K_1=\tau E_{ab}-\alpha I\) gives on its two cap terms

\[
\begin{aligned}
 \sum_{i,j}(K_1)_{ij}
   \operatorname {res}_{q_0}(P_{pq}^{ij};t_c)
   &=h(K_1)_{cc}\overline Y_c=-h\alpha\overline Y_c,\\
 \sum_{i,j}(K_1)_{ij}
   \operatorname {res}_{q_0}(P_{px}^{ic};y_j)
   &=h(K_1)_{cc}\overline Y_c=-h\alpha\overline Y_c.
\end{aligned}                                             \tag{49a}
\]

Only the constant word \(i=j=c\) survives in either sum; the off-diagonal
entry of \(K_1\) contributes zero residue.  Thus the two ordinary terms
cancel each other exactly while the radial right side contributes zero.
This direct test proves that the normal identity transports the response
but does not transgress the \(q_0\)-carrier to it.

Hence neither the scalar-zero cap nor the literal connection, separately
or together under the ordinary residue functor, yields (3).  The formal
guard in the inactive-Omega note reaches the same conclusion from the
other direction: it permits the transgression to be zero while retaining
nonzero curvature and the triangular identity.

There is, however, a canonical source-valid response--target syzygy.  Before
exposing \(x\), write the nine canonical cap quadratics on the even pair
complement as

\[
                    {\cal P}_{ij}=a_{ij}q+h p_i s_j,
 \qquad {\cal P}_I=\sum_i{\cal P}_{ii}
                  =\tau q+h\sum_i p_i s_i.               \tag{50}
\]

For the selected off-diagonal entry \(\alpha=a_{ab}\ne0\), the two cap
lifts of the same radial scalar \(\tau q\) have the exact difference

\[
\boxed{
 {\,\tau\over\alpha}{\cal P}_{ab}-{\cal P}_I
   =h\left({\tau\over\alpha}p_a s_b-\sum_i p_i s_i\right)
   ={h\over\alpha}R_{\rm ev}.}                           \tag{51}
\]

No common power is used in (51).  It is a kernel element in the formal
short exact cap filtration, before evaluation in the site algebra,

\[
0\longrightarrow
   \langle p_i s_j\rangle_{\rm formal}
 \longrightarrow
   \mathbb Cq\oplus\langle p_i s_j\rangle_{\rm formal}
 \mathop{\longrightarrow}^{\rm rad}
   \mathbb Cq
 \longrightarrow0                                       \tag{52}
\]

where \({\cal P}_{ij}\) is the displayed lift of \(a_{ij}q\).  Both terms
on the left of (51) lift the radial scalar \(\tau q\).  This normalization
matters.  When \(\tau\ne0\), division of the two lifts by their common
radial scalar gives

\[
 {1\over\alpha}{\cal P}_{ab}-{1\over\tau}{\cal P}_I
       ={h\over\alpha\tau}R_{\rm ev}.                    \tag{52a}
\]

Thus, after also dividing by the canonical cap factor \(h\), the
cap-normalized lift-difference per copy of \(q\) is
\(R_{\rm ev}/(\alpha\tau)\).  Multiplying this cap-normalized response by
\(\tau\) recovers the quadratic coordinate in (10), but simultaneously
changes the radial carrier from \(q\) to \(\tau q\).  When \(\tau=0\), both
radial symbols in (51) are zero, (52a) is undefined, and (51) is only a
kernel syzygy; it defines no map from \(q\).  This is the exact trace-zero
guard.

Evaluate the kernel difference on the scalar syzygy
\((\tau/\alpha)E_{ab}-I=\alpha^{-1}K_1\).  Since the off-diagonal product
\(\overline p_a\overline s_b\) has zero target residue and
\(\rho_{t_c}(\overline p_i\overline s_i)=\delta_{ic}\overline Y_i\),
restricting (51) away from \(x\) gives
\(\overline R_{\rm ev}=R\) and

\[
 \rho_{t_c}\!\left(
  h^{-1}\left(
    {\tau\over\alpha}\overline{\cal P}_{ab}
      -\overline{\cal P}_I\right)
 \right)
 =\rho_{t_c}(\alpha^{-1}R)
 =-\overline Y_c=\widehat\zeta_c.                         \tag{53}
\]

Equation (53) identifies the desired residue, but only on the quadratic
coordinate of the source syzygy.  Multiplying (51) by \(\Gamma(K)/h\)
gives that coordinate

\[
 \Xi_c^{\rm cap}(K)
  :={\Gamma(K)\over h}
       \left({\tau\over\alpha}{\cal P}_{ab}-{\cal P}_I\right)
   =\Gamma(K)\alpha^{-1}R_{\rm ev},                       \tag{54}
\]

whose odd restriction has residue precisely
\(\Gamma(K)\widehat\zeta_c\).  Its legal literal source datum still includes
the target coordinate displayed next; \(\Xi_c^{\rm cap}(K)\) alone is not
an admitted zero-target row and is not the value of a proved transgression.

The remaining obstruction is now a single target-grade term.  The
canonical cap rows satisfy

\[
 {\cal P}_{ij}q^{[h-1]}=h\delta_{ij}X_i.
\]

Therefore (51)--(54) give

\[
 \Xi_c^{\rm cap}(K)q^{[h-1]}
       =-\Gamma(K)\Delta_{2h,3}.                          \tag{55}
\]

After taking the \(x,c\) coefficient, this is exactly

\[
 \Gamma(K)\alpha^{-1}
       \bigl(n_cA+Rt_cB\bigr)
       =-\Gamma(K)Y_c
       =\Gamma(K)\widehat\zeta_c
       \quad\text{in }C_{q_0}.                            \tag{56}
\]

Thus the literal cap calculation proves the response--target pair

\[
 \boxed{\left(\Xi_c^{\rm cap}(K),
                   -\Gamma(K)\Delta_{2h,3}\right).}       \tag{56a}
\]

Its first coordinate has the desired internal residue, but it is not a
zero-target overlap boundary and does not by itself define (3).  In fact,
the obstruction to separating the first coordinate is stronger than
flatness of the known connection.

Let \(\Theta\) be any literal quadratic on this same even
\(q\)-complement, not necessarily a combination of canonical caps, and
write its restriction at \(x\) as

\[
                 \Theta=\overline\Theta+
                       \sum_j e_j^{(x)}L_j.
\]

Suppose it has a diagonal target

\[
             \Theta q^{[h-1]}=\sum_i\Lambda_iX_i.        \tag{57}
\]

The coefficient at \(x,c\) is forced to be

\[
                L_cA+\overline\Theta\,t_cB=\Lambda_cY_c.
\]

The first term lies in \({\cal R}_1(D)A\).  Passing to \(C_{q_0}\)
therefore gives the universal implication

\[
 \boxed{
 \Theta q^{[h-1]}=\sum_i\Lambda_iX_i
 \quad\Longrightarrow\quad
 \rho_{t_c}(\overline\Theta)=\Lambda_c\overline Y_c.}   \tag{58}
\]

This argument is coefficientwise, so the \(\Lambda_i\) may themselves
carry clean or transverse parameters.  Equation (58) is the
**same-complement target--residue lock**.  For (54),
every \(\Lambda_i=-\Gamma(K)\), and (58) recovers
\(\Gamma(K)\widehat\zeta_c\).  Conversely, every literal quadratic on the
same \(q\)-complement with target \(+\Gamma(K)\Delta_{2h,3}\) has residue

\[
                  +\Gamma(K)\overline Y_c
                    =-\Gamma(K)\widehat\zeta_c.           \tag{59}
\]

It necessarily erases the response when added to (54).  After multiplying
by the central certificate \((tu)^d\), the term in (59) has nonzero middle
coefficient whenever \(\widehat\zeta_c\ne0\), so it cannot be hidden in
\(\operatorname {im}{\mathscr D}_\parallel\).  Therefore a
target-cancelling companion inside the literal quadratic module of this
one \(q\)-complement does not merely remain unconstructed: it is
impossible.

The trace anchor is the canonical example.  Put

\[
 \Theta_c^{\rm tr}(K)={\Gamma(K)\over h}{\cal P}_I.
\]

Then

\[
\begin{aligned}
 \operatorname {tgt}\Theta_c^{\rm tr}(K)
   &=+\Gamma(K)\Delta_{2h,3},\\
 \rho_{t_c}(\overline\Theta_c^{\rm tr}(K))
   &=+\Gamma(K)\overline Y_c
     =-\Gamma(K)\widehat\zeta_c,\\
 \Xi_c^{\rm cap}(K)+\Theta_c^{\rm tr}(K)
   &={\Gamma(K)\tau\over h\alpha}{\cal P}_{ab}.
\end{aligned}                                             \tag{60}
\]

The last cap is off-diagonal, so both its target and its odd residue are
zero.  The former cap-span lock is thus a special case of (58), not the
full scope of the obstruction.

The qualifier ``same complement'' is essential.  Equations (57)--(58)
concern a single quadratic multiplied by the same \(q^{[h-1]}\), followed
by the quotient \(C_{q_0}\).  They do not identify the residue quotients
attached to two different chart quadratics, nor do they rule out a
homotopy defect in a comparison between those quotients.  Consequently a
target-cancelled transgression assembled from literal quadratic companions
cannot remain inside this one complement.  The route formulated below
retains the two chart complexes separately and cancels their target grades
only in a mapping cone.  Merely rewriting curvature, direct-double, or
anchor rows as one more literal identity on the first complement cannot
work.

This also matches the independent
[sum-channel guard](two-chart-selector-provenance-sum-channel-guard.md):
the known Bianchi/normal/direct-double packet transports its response
between filtration grades but does not split it into a source-valid row.
Thus naming those rows does not yet supply the required cross-quotient
comparison.

The remaining **target-cancelled transgression lemma** is now the following
mapping-cone construction.  One must exhibit a second literal filtered
chart complex \({\mathscr C}_{q'}\), a filtered comparison
\(\Phi:{\mathscr C}_{q'}\to{\mathscr C}_{q}\), and a cross-chart companion
\(\Theta'_c(K)\) such that:

* the target of \(\Theta'_c(K)\) cancels (55) after applying the target
  component of \(\Phi\);
* \((\Xi_c^{\rm cap}(K),\Theta'_c(K))\) has literal mapping-cone
  provenance, with no separated associated-graded row declared admissible;
* the induced comparison of the two odd residue quotients, including its
  filtration homotopy, leaves the middle class
  \(\Gamma(K)\widehat\zeta_c\) rather than identifying it with the locked
  residue (59); and
* after the certificate-bracket operation, every mapping-cone boundary
  maps to a \({\mathscr D}_\parallel\)-boundary and, on an active tilted
  auxiliary, the comparison intertwines with the two-Euler differential
  in (32).

None of these cross-quotient data are constructed here.  Any such map must
have transverse binary degree zero \(S_1^\perp\to S_1^\perp\), preserve
quadratic site degree before residue, and account explicitly for the one
filtration step whose associated-graded radial value is zero by (15) but
whose cap-lift value is (53).

The smallest statement which actually closes the routed branch is the
**off-diagonal filtered comparison exactness lemma**: the mapping-cone map
above is a filtered comparison to the two-Euler Koszul complex (or to a
source-provenant triangular contraction on the direct-free boundary) and
is injective on the one-dimensional physical target line
\(\mathbb C\widehat\zeta_c\).  On an active tilted auxiliary, Section 4
proves that the target Koszul complex is acyclic.  On the direct-free
boundary, the second clause is a genuine additional requirement because
the joint weight-zero class persists.

If that exactness lemma holds, simultaneous all-inactivity forces
\(\widehat\zeta_c=0\), contradicting the minimum-order survival lemma.  It
is localized to the already routed off-diagonal all-inactive branch; it
does not repackage the whole conjecture.  Theorem 5.1 would then supply
every Hermite shift uniformly.  Conversely, same-complement target
cancellation, scalar multiplication of the radial right side of (9), or
use of the even certificate without a transverse endpoint direction
cannot work by Sections 2--6.

## 7. Scope

The proved statements are:

* the radial/gauge annihilation (15)--(18);
* the parity no-go (20)--(21);
* the independent-line bracket uniqueness (21)--(25), together with the
  optional identified-line transvectant guard (26);
* the exact two-Euler coefficient complex, together with the separate
  literal radial-row vanishing (36);
* the exact certificate-bracket prolongation conditional on (38);
* the canonical cap lift-difference and response--target syzygy
  (50)--(56a), including the \(\tau\ne0\) normalization and exact
  \(\tau=0\) guard;
* the flat-normal obstruction (49a), which shows why that representative
  is not already a target-cancelled chain row; and
* the same-complement target--residue lock (57)--(59), of which the
  one-chart cap calculation (60) is a special case.

The unproved statements are the radial-to-response map (3), the
cross-quotient target-cancelled mapping-cone companion, its chain property,
and filtered comparison exactness on the surviving target line.  This note
neither constructs the decorated overlap complex nor proves that its
exactness yields an active clean point.  Its gain is to remove the apparent
all-\(h\) Hermite ledger, identify the exact source-valid
response--target pair, and prove that no same-complement literal-quadratic
target cancellation can separate that pair.  The remaining physical class is
the pair
\((\Gamma(K)\alpha^{-1}R,-\Gamma(K)\Delta_{2h,3})\), which
the proposed mapping-cone route would resolve across genuinely different
quotient complexes without erasing the response
\(\Gamma(K)\widehat\zeta_c\).

The dependency-free checker
[`verify_residue_chain_map_radial_transgression.py`](../computations/verify_residue_chain_map_radial_transgression.py)
audits the parity and Clebsch--Gordan multiplicities, the two natural
operations and their middle coefficients, the curvature normalization,
the exact correction for both possible values of \(d\), the divided-power
and near-perfect gauge coefficient normalizations, and the formal
radial/gauge quotient ledger.  It also checks the cap lift-difference,
the \(\tau=0\) guard and \(\tau\ne0\) per-\(q\) normalization, its
normalized residue and diagonal target, and the flat-normal cancellation
and same-complement target--residue lock.  It does not certify the
unconstructed radial transgression, target-cancelling mapping-cone
companion, or filtered comparison.

# A diagonal inactive line has three boundaries but a two-boundary saturation

## 1. Outcome

Let a canonical physical cap line be selected at a diagonal entry

\[
             \alpha=A_{pq}(a,a)\ne0,
             \qquad \tau=\operatorname {tr}A_{pq},
             \qquad \beta=\tau-\alpha .                       \tag{1}
\]

Put

\[
 K_0=E_{aa},\qquad K_1=\tau E_{aa}-\alpha I,
 \qquad K(t,u)=tK_0+uK_1.                                    \tag{2}
\]

The exact activity polynomial on this line is, up to the displayed
nonzero scalar,

\[
 \boxed{\operatorname {Act}(t,u)
       =\alpha^3t u^2(t+\beta u).}                            \tag{3}
\]

Thus there are two geometrically different cases.

* If \(\beta\ne0\), the reduced activity boundary consists of three
  distinct points:

  \[
  \begin{array}{c|c|c|c}
  \text{point}&\text{equation}&\text{cap matrix}
       &\text{reason for inactivity}\\ \hline
  P_0&u=0&K_0=E_{aa}&\text{two target coordinates vanish},\\
  P_1&t=0&K_1=\tau E_{aa}-\alpha I&\text{the direct scalar vanishes},\\
  P_2&t+\beta u=0&K_2=\alpha(E_{aa}-I)
       &\text{the }a\text{-target vanishes}.
  \end{array}                                                \tag{4}
  \]

* If \(\beta=0\), then \(P_1=P_2\),
  \(K_1=K_2=\alpha(E_{aa}-I)\), and the reduced boundary is just
  \(tu=0\).  This trace collision is exactly the previously used
  unary--complementary diagonal packet.  Its activity polynomial has the
  nonreduced form \(\alpha^3t^2u^2\).

This geometry gives an exhaustive coefficient-level routing theorem for
the diagonal all-inactive branch.  Let \({\cal E}(t,u)\) be its degree
\(h\) clean error, assume it has a clean point, and assume every clean
point on the line is inactive.  Factor one copy of the linear equation of
each distinct clean boundary point.  If there are \(m\) such points, then

\[
                         {\cal E}=P_Z\Omega_Z,
             \qquad \deg\Omega_Z=d=h-m.                       \tag{5}
\]

For \(\beta\ne0\), with

\[
                         B_\beta=tu(t+\beta u),                \tag{6}
\]

there is a bounded certificate

\[
 \boxed{H\in V^*\otimes\mathbb C[t,u]_{2d},\qquad
                  \langle H,\Omega_Z\rangle=B_\beta^d.}       \tag{7}
\]

For \(\beta=0\), the sharper two-boundary certificate is

\[
 \boxed{H\in V^*\otimes\mathbb C[t,u]_d,\qquad
                  \langle H,\Omega_Z\rangle=(tu)^d.}          \tag{8}
\]

There is also a sharper **asymmetric** certificate when \(\beta\ne0\).
Choose a two-boundary coordinate pair containing a clean point, remove the
full coordinate-gcd multiplicity of the third boundary factor, and call
the resulting residual \(\Xi\) of degree \(e\).  Then

\[
 \boxed{H_{\rm sat}\in V^*\otimes\mathbb C[x,y]_e,
             \qquad\langle H_{\rm sat},\Xi\rangle=(xy)^e.}   \tag{8a}
\]

Thus (7) is the symmetric three-boundary certificate, while (8a) is the
lighter certificate comparable to the off-diagonal theorem.  Section 5
proves both formulations and states exactly what was divided out.

Consequently the factorization degrees are \(h-1,h-2,h-3\) when one,
two, or three distinct generic boundary points are clean.  In the
collision case they are \(h-1,h-2\).  Higher vanishing at a boundary is
harmless: it remains in the coordinate gcd of \(\Omega_Z\) and is
absorbed by (7) or (8).

The generic line has two exact normalized boundary jets.  If \(\rho_i\)
denotes the odd response residue of \(K_i\), then

\[
 \rho_0=(\delta_{ca}\overline Y_c)_c,
 \qquad
 \rho_2=(-\alpha(1-\delta_{ca})\overline Y_c)_c,
 \qquad
 \rho_1=\beta\rho_0+\rho_2.                                  \tag{9}
\]

The scalar-zero jet and the binary-boundary jet normalize to

\[
 \boxed{Z_1=\beta\rho_0+\rho_2,\qquad
        Z_2=-\beta\rho_0+(h-1)\rho_2.}                        \tag{10}
\]

For \(\beta\ne0\), their coefficient matrix has determinant
\(h\beta\ne0\), and hence

\[
 \boxed{\rho_2={Z_1+Z_2\over h},\qquad
        \rho_0={(h-1)Z_1-Z_2\over h\beta}.}                  \tag{11}
\]

The symmetric three-point packet naturally has two residue channels.
This agrees with the elementary fact that
\(\mathbb P^1\setminus\{P_0,P_1,P_2\}\) has two independent logarithmic
residues.  In the collision \(\beta=0\), the second normalization is
singular, the first nonzero scalar-zero target jet moves to order
\(h-1\), and (10) reduces to the familiar complementary class

\[
             Z_{1,a}=0,\qquad
             \alpha^{-1}Z_{1,c}=-\overline Y_c\quad(c\ne a).  \tag{12}
\]

Thus diagonal coefficient routing is complete.  The symmetric formulation
does not directly enter the already proved one-dimensional torus--Koszul
residue calculation, but the saturated chartwise formulation (8a) gives a
precise candidate entry into it.  The
[odd-residue survival lemma](odd-residue-minimality-survival.md) supplies
at least one nonzero \(\overline Y_c\) when the cap comes from a
minimum-order exact ternary source.  In the generic case, every coefficient
in each of the two rows (10) is nonzero, so **either jet detects every
possible surviving colour**.  There is no additional generic colour-choice
gap.  At the collision, however, (12) is blind to colour \(a\), and
minimum-order survival alone does not exclude the possibility that only
\(\overline Y_a\) survives.

Proof closure still requires either a theorem forcing a collision together
with complementary-colour survival, a selection theorem avoiding diagonal
lines, or a literal source-filtered comparison which validates the
third-boundary saturation in (8a) and transports the appropriate jet.  A
symmetric comparison could instead supply corrections for both classes in
(11).  The conjecture remains open.

## 2. Exact activity geometry

Write

\[
                         \Delta_{\bar a}=\sum_{c\ne a}X_c.
\]

The direct contraction and target row of (2) are

\[
 \boxed{s(t,u)=\alpha t,\qquad
        T(t,u)=(t+\beta u)X_a-\alpha u\Delta_{\bar a}.}        \tag{13}
\]

Indeed, the diagonal entries of \(K(t,u)\) are
\(t+\beta u\) at \(a\) and \(-\alpha u\) at the other two labels.
Therefore

\[
 \det K(t,u)=\alpha^2u^2(t+\beta u),
 \qquad s(t,u)\det K(t,u)=\alpha^3tu^2(t+\beta u),           \tag{14}
\]

which proves (3).  At the scalar-zero point,

\[
 K_1=\operatorname {diag}(\beta,-\alpha,-\alpha)
       \quad\text{in the ordering }a,\bar a,                 \tag{15}
\]

so it is invertible exactly when \(\beta\ne0\).  At the third point,

\[
 K_1-\beta K_0=\alpha(E_{aa}-I)=K_2,                         \tag{16}
\]

whose diagonal target is binary.  Its direct scalar is
\(-\alpha\beta\), so it is distinct from and complementary to the
scalar-zero point precisely when \(\beta\ne0\).

The multiplicity two of \(u\) in (3) records the two missing target
labels at \(K_0\).  It does not give two clean-error factors.  Clean-error
divisibility is governed by the reduced projective points in (4), not by
the multiplicities of the activity polynomial.

## 3. Scalar-zero expansion and its order-\((h-1)\) jet

Use the standard physical data

\[
 s=s(K),\qquad r=r(K),\qquad F=sq+r,
 \qquad {\cal E}(K)=F(K)^{[h]}-s(K)^{h-1}T(K).                \tag{17}
\]

Put

\[
                         F=F(K_0),\qquad R=F(K_1)=r(K_1).
\]

Linearity gives \(F(K(t,u))=tF+uR\).  Expanding in divided powers gives

\[
                 {\cal E}(t,u)=\sum_{j=0}^h
                              t^{h-j}u^j C_j,                 \tag{18}
\]

where

\[
\boxed{
\begin{aligned}
C_0&=F^{[h]}-\alpha^{h-1}X_a,\\
C_1&=RF^{[h-1]}-\alpha^{h-1}\beta X_a
                         +\alpha^h\Delta_{\bar a},\\
C_j&=R^{[j]}F^{[h-j]}\qquad(2\le j\le h).
\end{aligned}}                                               \tag{19}
\]

The complete physical row at the scalar-zero point is

\[
                   Rq^{[h-1]}=\beta X_a-\alpha\Delta_{\bar a}.
                                                                    \tag{20}
\]

It gives the unconditional boundary-polar identity

\[
\boxed{
 RF^{[h-1]}-C_1
   =\alpha^{h-1}(\beta X_a-\alpha\Delta_{\bar a})
   =\alpha^{h-1}Rq^{[h-1]}.}                                 \tag{21}
\]

Relative to \(K_0\), this is the first inward coefficient.  Relative to
the scalar-zero point \(K_1\), it is the order-\((h-1)\) inward target
jet: the factor \(s^{h-1}\) vanishes to that order there.  Cleanliness of
neither endpoint is used in (21).

Expose a residual site \(x\), and write

\[
 q=q_0+\sum_c e_c^{(x)}t_c,qquad
 R=r+\sum_c e_c^{(x)}n_c,qquad
 A=q_0^{[h-1]},\quad B=q_0^{[h-2]}.                           \tag{22}
\]

In the quotient

\[
 C_{q_0}={{\cal R}_{2h-1}\over {\cal R}_1A},\qquad
 \operatorname {res}_{q_0}(r;t_c)=[rt_cB],                  \tag{23}
\]

the \((x,c)\)-coefficient of (20) proves

\[
 \boxed{\operatorname {res}_{q_0}(r;t_c)
       =(\beta\delta_{ca}-\alpha(1-\delta_{ca}))\overline Y_c.}
                                                                    \tag{24}
\]

The same calculation works for an arbitrary cap matrix \(K\), not just a
scalar-zero one.  If its response is
\(r_K=r+\sum_c e_c^{(x)}n_c\), the exposed physical row is

\[
       (s(K)t_c+n_c)A+rt_cB=K_{cc}Y_c.
\]

The first parenthesis is killed in (23), so
\(\operatorname {res}_{q_0}(r;t_c)=K_{cc}\overline Y_c\).
This proves the response-residue interpretation of every \(\rho_i\) in
(9); no scalar-zero assumption is hidden in that notation.

Equivalently, applying \(\pi_{q_0}\partial_{x,c}\) to (21) and dividing
only by \(\alpha^{h-1}\) gives the first vector in (10):

\[
 Z_{1,c}:=\alpha^{1-h}\pi_{q_0}\partial_{x,c}
              (RF^{[h-1]}-C_1)
   =\begin{cases}
       \beta\overline Y_a,&c=a,\\
       -\alpha\overline Y_c,&c\ne a.
     \end{cases}                                             \tag{25}
\]

No matching power has been cancelled in this calculation.

## 4. The binary-boundary first jet

For the third boundary point use coordinates

\[
                         v=t+\beta u,\qquad w=u.              \tag{26}
\]

Then

\[
 K=vK_0+wK_2,qquad
 s=\alpha(v-\beta w),\qquad
 T=vX_a-\alpha w\Delta_{\bar a}.                             \tag{27}
\]

Put

\[
                         G=F(K_2)=R-\beta F.
\]

The clean error in these coordinates is

\[
 {\cal E}(v,w)=(vF+wG)^{[h]}
 -\alpha^{h-1}(v-\beta w)^{h-1}
                   (vX_a-\alpha w\Delta_{\bar a}).           \tag{28}
\]

Its endpoint coefficient and first inward coefficient at \(K_2\) are

\[
\begin{aligned}
D_h={}&G^{[h]}-(-1)^h\alpha^h\beta^{h-1}\Delta_{\bar a},\\
D_{h-1}={}&FG^{[h-1]}-Q_2,                                   \tag{29}
\end{aligned}
\]

where

\[
\boxed{
 Q_2=\alpha^{h-1}\left(
       (-\beta)^{h-1}X_a
       -(h-1)\alpha(-\beta)^{h-2}\Delta_{\bar a}\right).}   \tag{30}
\]

Thus \(K_2\) is clean exactly when \(D_h=0\), in which case
\(v\mid{\cal E}\) and the residual value at \(K_2\) is \(D_{h-1}\).
Again, the boundary-polar difference

\[
                         FG^{[h-1]}-D_{h-1}=Q_2              \tag{31}
\]

is unconditional.

When \(\beta\ne0\), put \(s_2=-\alpha\beta\).  Let
\(\rho(K)_c=K_{cc}\overline Y_c\), and abbreviate
\(\rho_i=\rho(K_i)\).  Formula (30) can be written intrinsically as

\[
 \pi_{q_0}\partial_x Q_2
   =s_2^{h-2}\bigl(s_2\rho_0+(h-1)\alpha\rho_2\bigr).        \tag{32}
\]

Therefore normalization by the selected-entry scalar, together with the
nonzero direct scalar at \(K_2\), gives

\[
\begin{aligned}
 Z_2&:=\alpha^{-1}s_2^{2-h}\pi_{q_0}\partial_x
                    (FG^{[h-1]}-D_{h-1})\\
    &=-\beta\rho_0+(h-1)\rho_2.                              \tag{33}
\end{aligned}
\]

In components,

\[
 Z_{2,c}=\begin{cases}
       -\beta\overline Y_a,&c=a,\\
       -(h-1)\alpha\overline Y_c,&c\ne a.
     \end{cases}                                             \tag{34}
\]

Together, (25) and (34) prove (10)--(11).  In particular, no common
scalar normalization makes all surviving colours and both boundary jets
equal.  Label-by-label division by the nonzero diagonal entries of
\(K_1\) would hide this fact and becomes illegal at the collision.

There is nevertheless no colour blindness on the generic stratum.  Since
\(\alpha\ne0\), \(\beta\ne0\), and the ground field has characteristic
zero, (25) and (34) show

\[
 \begin{array}{c|cc}
 &c=a&c\ne a\\ \hline
 Z_{1,c}/\overline Y_c&\beta&-\alpha\\
 Z_{2,c}/\overline Y_c&-\beta&-(h-1)\alpha
 \end{array}                                                 \tag{35}
\]

with all four displayed scalars nonzero.  Therefore, if minimum-order
survival gives any colour \(c\) with \(\overline Y_c\ne0\), then both
\(Z_{1,c}\) and \(Z_{2,c}\) are nonzero.  The distinction from the
off-diagonal universal class is transport, not detection: the diagonal
coefficients depend on the selected/complementary label and the chart
parameter \(\beta/\alpha\).

If \(\beta=0\), then \(s_2=0\), so (33) must not be specialized after
division.  Formula (28) shows directly that the first target contribution
at the collided point occurs at order \(h-1\), not order one.  It is
exactly the term \(-\alpha^h\Delta_{\bar a}\) in (21), proving (12).
The selected class \(\overline Y_a\) is invisible in this stratum, so the
survival lemma by itself does not yet provide a nonzero routed defect.

## 5. Clean factors and exhaustive gcd routing

For \(\beta\ne0\), associate the pairwise coprime boundary factors

\[
                 p_0=u,\qquad p_1=t,\qquad
                 p_2=t+\beta u.                              \tag{36}
\]

Equations (19) and (29) give

\[
\begin{array}{c|c}
P_i\text{ is clean}&\text{equivalent divisibility}\\ \hline
P_0&u\mid{\cal E},\\
P_1&t\mid{\cal E},\\
P_2&t+\beta u\mid{\cal E}.
\end{array}                                                   \tag{37}
\]

The last equivalence is just the homogeneous remainder theorem applied
coordinatewise.  Hence, if \(Z\subseteq\{0,1,2\}\) is the set of
distinct clean boundary points,

\[
              P_Z=\prod_{i\in Z}p_i,qquad
              {\cal E}=P_Z\Omega_Z,qquad
              \deg\Omega_Z=h-|Z|.                            \tag{38}
\]

In the roots-exist/all-inactive branch, \(Z\ne\varnothing\).  Moreover
\({\cal E}\) cannot be identically zero, because (3) has a nonempty
active locus and an identically zero error would make every active point
clean.  After (38), \(\Omega_Z\) has no common zero on
\(D(B_\beta)\).

Choose coordinates of \(\Omega_Z\), ignore identically zero coordinates,
and let their gcd be

\[
                         g=t^au^b(t+\beta u)^c.               \tag{39}
\]

Every common root lies on the three-point boundary, so (39) is exhaustive;
also \(a+b+c\le d\).  Divide by \(g\).  The reduced degree is

\[
                         e=d-a-b-c,                           \tag{40}
\]

and the reduced coordinate forms have gcd one.  If \(e>0\), two linear
combinations \(L,M\) of them can be chosen coprime.  The binary complete
intersection \((L,M)\) contains every form of degree at least \(2e-1\).
But

\[
 \deg {B_\beta^d\over g}=3d-a-b-c\ge2e-1,                   \tag{41}
\]

and each multiplier of \(L,M\) has degree

\[
             (3d-a-b-c)-e=2d.                               \tag{42}
\]

Multiplying back by \(g\) proves (7).  The case \(e=0\), including
\(d=0\), is immediate.  Conversely, (7) excludes a common zero wherever
\(B_\beta\ne0\), so it is an exact certificate for the all-inactive
condition.

When \(\beta=0\), the reduced boundary factors are only \(t,u\).  Repeating
the same proof with \(g=t^au^b\) gives

\[
 \deg{(tu)^d\over g}=2d-a-b\ge2(d-a-b)-1,                   \tag{43}
\]

and multiplier degree \(d\), proving (8).  The collision therefore
recovers exactly the degree of the established two-boundary bounded
certificate, even if only one of its two endpoints is clean.

### 5.1 The sharper two-boundary saturation

The symmetric target \(B_\beta^d\) is useful because it treats all three
boundary points without choices.  It is not the smallest coefficient
certificate.

First suppose at least one of \(P_0,P_1\) is clean, and retain the
coordinates \((t,u)\).  Let

\[
 r_2=\operatorname {ord}_{t+\beta u}
                 \gcd(\text{coordinates of }\Omega_Z),
 \qquad
 \Omega_Z=(t+\beta u)^{r_2}\Xi,qquad e=d-r_2.               \tag{43a}
\]

After the full third-boundary multiplicity is removed, every common root
of \(\Xi\) is supported at \(t=0\) or \(u=0\).  The ordinary two-boundary
proof therefore gives

\[
 H_{01}\in V^*\otimes\mathbb C[t,u]_e,qquad
                    \langle H_{01},\Xi\rangle=(tu)^e.        \tag{43b}
\]

Equivalently,

\[
       \langle H_{01},\Omega_Z\rangle
                  =(t+\beta u)^{r_2}(tu)^e.                 \tag{43c}
\]

The relevant physical defect is \(Z_1\).  This includes the one-clean-root
orientations at either \(P_0\) or \(P_1\), as well as every multiple-root
specialization.  If \(P_2\) is also clean, its first factor is already in
\(P_Z\); only its excess multiplicity appears in \(r_2\).

If the only distinct clean point is \(P_2\), use instead

\[
                         v=t+\beta u,\qquad w=u.
\]

The endpoint axes are now \(P_2,P_0\), the third boundary is
\(t=v-\beta w=0\), and the natural defect is \(Z_2\).  Removing the full
\((v-\beta w)\)-gcd multiplicity gives a residual \(\Xi'\) of degree
\(e'\) and

\[
 H_{20}\in V^*\otimes\mathbb C[v,w]_{e'},\qquad
                    \langle H_{20},\Xi'\rangle=(vw)^{e'}.    \tag{43d}
\]

In this only-\(P_2\)-clean stratum the third-boundary multiplicity is in
fact zero, because a common zero at \(P_1\) would make \(P_1\) clean.
The formulation with saturation is retained because it also applies after
further boundary factors have already been removed.

Equations (43a)--(43d) prove that a single two-boundary certificate exists
on every generic all-inactive stratum.  This is a coefficient operation:
division is only by an explicitly determined factor of the scalar
coordinate gcd in \(\mathbb C[t,u]\), never by a matching power or a
site-algebra element.  What remains unproved is that this division and the
choice between \(Z_1,Z_2\) lift through the literal source filtration and
the overlapping-cap comparison.  Until that is constructed, (8a) is a
candidate one-residue route, not a completed chain-level reduction.

## 6. Symmetric residues versus the chartwise saturation

On the affine chart \(t\ne0\), put \(z=u/t\).  For \(\beta\ne0\), the
active locus is

\[
                \mathbb P^1\setminus
                   \{z=0,\ z=-1/\beta,\ z=\infty\}.          \tag{44}
\]

The two logarithmic forms

\[
                     {dz\over z},\qquad
                     {\beta\,dz\over1+\beta z}              \tag{45}
\]

have residue triples

\[
                         (1,0,-1),\qquad(0,1,-1).             \tag{46}
\]

They are independent, and every logarithmic residue triple has sum zero.
Thus the symmetric logarithmic coefficient complex of the three-punctured
line has a two-dimensional obstruction space.  This is the coefficient
counterpart of the invertible two-by-two system (10)--(11).

At \(\beta=0\), the binary boundary \(z=-1/\beta\) merges projectively
with the scalar-zero point at infinity, (44) becomes \(\mathbb G_m\), and
only the usual one-dimensional \(dz/z\) residue remains.  Correspondingly,
(8) has total degree \(2d\) and feeds the existing torus-weight
calculation.  In the generic case, (7) has total degree \(3d\) and
multiplier degree \(2d\); there is no projective change of coordinates
that turns three distinct boundary points into two.

This does not prove that a particular literal source overlap realizes the
full logarithmic complex, nor does it make two correction classes
unavoidable.  The asymmetric saturation (43a)--(43d) removes the third
common boundary factor and leaves an ordinary two-boundary certificate.
If that scalar-gcd division is source-filtered and the corresponding jet
is transported, the old single-middle-coefficient calculation can apply
to \(\Xi\) or \(\Xi'\).  If it is not compatible with the source complex,
then a symmetric closure must instead identify two correction coefficients
(or prove a physical relation that kills one channel).  This is now the
exact fork, rather than an assumed two-residue obstruction.

## 7. Exact scope

The positive result is complete at coefficient level:

1. every diagonal activity-boundary point and collision is explicit;
2. every clean boundary point gives its exact linear factor;
3. every all-inactive diagonal residual has the bounded certificate (7)
   or (8), and the lighter chartwise certificate (8a); and
4. the scalar-zero and binary-boundary polars give the exact normalized
   classes (10).

The result does **not**:

1. produce a complementary nonzero class in the collision case (although
   minimum-order survival produces some nonzero class, and both generic
   jets detect it);
2. prove that third-boundary scalar-gcd division is compatible with the
   source filtration and chart transport;
3. construct the resulting one-residue correction, or alternatively show
   that the two symmetric residue channels obey the needed physical
   relation;
4. force \(\beta=0\), or force the selected entry to be off diagonal; or
5. turn the three-boundary certificate into an active clean cap.

Accordingly, the generic diagonal branch has both a symmetric two-class
description and a sharper candidate one-class saturation route, while the
trace-collision branch is routed to the already isolated one-class
obstruction.  No source correction is constructed here.

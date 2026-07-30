# Diagonal boundary division is a literal principal-parts obstruction

## 1. Outcome

Fix \(h\geq3\) and a diagonal selected cell

\[
 \alpha=a_{aa}\ne0,\qquad \tau=\operatorname {tr}(a_{ij}),
 \qquad \beta=\tau-\alpha,
\]

and the three cap directions

\[
 K_0=E_{aa},\qquad K_1=\tau E_{aa}-\alpha I,
 \qquad K_2=\alpha(E_{aa}-I).
 \tag{1}
\]

The coefficient calculation on the diagonal inactive line produces the
two normalized odd jets

\[
 Z_1=\beta\rho_0+\rho_2,
 \qquad Z_2=-\beta\rho_0+(h-1)\rho_2,
 \tag{2}
\]

where \(\rho_i=((K_i)_{cc}\overline Y_c)_c\).  The first result of this
note is that (2) already has an exact lift through the literal full-nine
cap filtration.  Put

\[
 J_1=K_1=\beta K_0+K_2,
 \qquad J_2=-\beta K_0+(h-1)K_2.                 \tag{3}
\]

Then the canonical cap contractions \({\cal P}(J_1)\) and
\({\cal P}(J_2)\) have odd residues exactly \(Z_1\) and \(Z_2\).
No boundary polynomial, matching power, site form, or diagonal target
entry is divided out.  For \(\beta\ne0\), either row sees every physical
label and can be normalized label by label using only a known nonzero
scalar.  The literal overlap transports the resulting class
\(\overline Y_c\) without relabelling.

The second result identifies precisely what is *not* supplied by this
cap lift.  Let \(\ell=t+\beta u\) be the third boundary factor, and suppose
a scalar-coordinate calculation gives

\[
                         \Omega=\ell^r\Xi.             \tag{4}
\]

For a filtered literal source module \(M\), literal boundary submodule
\(N\), and evaluation map \(\epsilon:M\to V\), division in (4) lifts to
the source quotient \(M/N\) if and only if the first \(r\) transverse
principal parts of a source representative of \(\Omega\) lie in \(N\),
not merely in \(\ker\epsilon\).  Equivalently, on the specified filtered
family \({\mathscr U}\subseteq M\otimes S\), the required relative
saturation criterion is

\[
 \epsilon^{-1}\bigl(\ell^r(V\otimes S)\bigr)\cap{\mathscr U}
 =\bigl(N\otimes S+\ell^r(M\otimes S)\bigr)\cap{\mathscr U}.
                                                               \tag{5}
\]

This is the exact relative Rees-saturation condition for that family; no
global equality is asserted when \(\ker\epsilon\ne N\).  Scalar coordinate divisibility proves
only that the principal parts lie in \(\ker\epsilon\).  The difference

\[
                         \ker\epsilon/N                 \tag{6}
\]

is the source-provenance obstruction.  The criterion is uniform in the
multiplicity \(r\); no root or coefficient enumeration is needed.

When \(\epsilon\) is ordinary odd-residue evaluation, the radial quadratic
exhibits the kernel phenomenon measured by (6): ordinary odd residue kills
it, while the lower symbol of a scalar-zero cap relation is the response
row.  This observation alone does not assert that the radial class is
nonzero in \(\ker\epsilon/N\).  Nor is it a map from the radial generator to
the response, and the response still carries its diagonal target.  In fact,
every quadratic companion against the same divided power which cancels that
target also cancels its odd residue.  Thus the first genuinely noncommuting
step is a secondary comparison of the two adjacent-power pieces in the
exposed cap row.  The existing off-diagonal transgression problem and the
diagonal third-boundary division have the same principal-parts shape.  The
generic diagonal calculation supplies the required lower-symbol
representative, but not that secondary chain comparison.

At the trace collision \(\beta=0\),

\[
                  J_2=(h-1)J_1=(h-1)K_2.               \tag{7}
\]

Both cap residues vanish on label \(a\).  This is not a bad normalization:
the selected target term has transverse order \(h\) at the collided
boundary, while the complementary target has order \(h-1\).  Hence every
target-grade boundary-polar comparison of order at most \(h-1\) is
intrinsically blind to \(\overline Y_a\).  Division by \(\beta\), or specialization of a
formula derived after such division, is invalid.  Minimum-order survival
does not repair the issue: if only \(\overline Y_a\) survives, the two
vanishing complementary classes assemble, after projection away from the
selected colour, an allowed exact binary source, not a smaller forbidden
ternary source.

Consequently the generic source-normalization ledger is closed at the
quadratic cap level, but the conjecture is not.  The exact remaining
diagonal statement is a literal relative-saturation/target-cancelled
comparison proving (5) for the clean-error representative and carrying one
of the rows (3) through the overlap.  At \(\beta=0\) it must additionally
carry the unary anchor through the order-\(h\) principal part, or else prove
that a complementary odd class survives.  Neither statement follows from
the current literal rows.

## 2. The literal full-nine cap filtration

On the complement of a physical pair, the original endpoint-ordered source
equations are

\[
 a_{ij}q^{[h]}+p_i s_jq^{[h-1]}=\delta_{ij}X_i
 \qquad(0\le i,j\le2).                                  \tag{8}
\]

Define the unnormalized canonical cap rows

\[
              {\cal P}_{ij}=a_{ij}q+h p_i s_j.           \tag{9}
\]

Since \(q q^{[h-1]}=h q^{[h]}\), all nine literal equations become

\[
              {\cal P}_{ij}q^{[h-1]}=h\delta_{ij}X_i.    \tag{10}
\]

For a matrix \(L=(L_{ij})\), put

\[
\begin{aligned}
 \sigma(L)&=\sum_{i,j}L_{ij}a_{ij},\\
 r(L)&=\sum_{i,j}L_{ij}p_i s_j,\\
 {\cal P}(L)&=\sum_{i,j}L_{ij}{\cal P}_{ij}
              =\sigma(L)q+h r(L),\\
 T(L)&=\sum_iL_{ii}X_i.
\end{aligned}                                             \tag{11}
\]

Thus

\[
                         {\cal P}(L)q^{[h-1]}=hT(L).     \tag{12}
\]

This is a literal contraction of the nine rows; endpoint order and every
diagonal target are retained.

Expose one residual site \(x\), let \(D\) be the remaining \(2h-1\)
sites, and write

\[
\begin{aligned}
 q&=q_0+\sum_c e_c^{(x)}t_c,\\
 {\cal P}(L)&=p_L+\sum_c e_c^{(x)}\lambda_{L,c}.
\end{aligned}                                             \tag{13}
\]

Set

\[
 A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},\qquad
 C_{q_0}={{\cal R}_{2h-1}(D)\over {\cal R}_1(D)A}.       \tag{14}
\]

The \((x,c)\)-coefficient of (12) is the exact two-step filtered row

\[
           \lambda_{L,c}A+p_Lt_cB=hL_{cc}Y_c.            \tag{15}
\]

After quotienting by \({\cal R}_1A\), define

\[
 \operatorname {CapRes}_c(L)
       ={1\over h}[p_Lt_cB]\in C_{q_0}.                  \tag{16}
\]

Equation (15) proves

\[
                 \boxed{\operatorname {CapRes}_c(L)
                         =L_{cc}\overline Y_c.}          \tag{17}
\]

Only the nonzero characteristic-zero scalar \(h\) was divided out.  In
particular, the radial summand \(\sigma(L)q_0\) in \(p_L\) contributes
nothing because

\[
 q_0B=(h-1)A,\qquad [t_cq_0B]=0.                         \tag{18}
\]

For overlapping physical charts, the power-free cap connection identifies
the two occurrences of the same constant-word coefficient.  Equivalently,
each side of the transported cap row has residue
\(h\delta_{ij}\delta_{ic}\overline Y_i\).  Therefore (17) is transported
in the unchanged physical label \(c\); the charts are not independently
relabelled.

The same calculation gives a useful lock which is not restricted to cap
contractions.  If an arbitrary literal quadratic row on this same
complement satisfies

\[
                       Qq^{[h-1]}=\sum_c\lambda_cX_c,     \tag{18a}
\]

then its off-\(x\) restriction obeys

\[
                  [t_c\overline Q B]=\lambda_c\overline Y_c.
                                                               \tag{18b}
\]

Indeed, the other exposed coefficient of (18a) is a linear form times
\(A\), exactly as in (15).  Consequently two same-power quadratic rows
whose targets cancel have cancelling ordinary odd residues.  Any
target-cancelled transgression retaining a response class must act before
the two terms of (15) are collapsed to the quotient (16).

## 3. Both generic diagonal jets are literal cap rows

The diagonal entries and direct scalars of (1) are

\[
\begin{array}{c|c|c}
 &\operatorname {diag}&\sigma\\ \hline
 K_0&(1,0,0)\text{ in the }a,\bar a\text{ ordering}&\alpha\\
 K_1&(\beta,-\alpha,-\alpha)&0\\
 K_2&(0,-\alpha,-\alpha)&-\alpha\beta.
\end{array}                                                \tag{19}
\]

The identities \(K_1=\beta K_0+K_2\) and (17) immediately give

\[
 \operatorname {CapRes}(J_1)
       =\beta\rho_0+\rho_2=Z_1.                            \tag{20}
\]

Likewise

\[
 \operatorname {CapRes}(J_2)
       =-\beta\rho_0+(h-1)\rho_2=Z_2.                      \tag{21}
\]

This supplies the source representative which was not visible in the
coefficient derivation of the binary-boundary jet.  In particular, the
factor \(s_2^{\,2-h}=(-\alpha\beta)^{2-h}\) used to *derive* the normalized
coefficient formula is not needed to represent the result.  One must not
specialize that derivation at \(\beta=0\); the division-free row (21) is
the legitimate specialization of the algebraic cap combination.  It is
not a normalized binary-boundary first jet there, because that
normalization has ceased to exist.

The scalar-zero row also has the explicit cap-filtration form

\[
 {\tau\over\alpha}{\cal P}_{aa}-\sum_i{\cal P}_{ii}
       ={1\over\alpha}{\cal P}(K_1)
       ={h\over\alpha}r(K_1).                              \tag{22}
\]

The only division is by the selected nonzero entry \(\alpha\).  Formula
(22) is the diagonal version of the lower-symbol calculation on an
off-diagonal scalar-zero line.  Its domain is the scalar relation
\(\alpha^{-1}K_1\in\ker\sigma\); it must not be renamed as a connecting
map \(q\mapsto\alpha^{-1}r(K_1)\).  If \(\tau\ne0\), one may compare two
normalized lifts of the radial symbol and obtains an extra factor
\(\tau^{-1}\).  If \(\tau=0\), the first term in (22) vanishes and the
trace cap has radial coefficient \(\sigma(I)=\tau=0\); both terms therefore
have zero radial symbol, and no radial transition exists.

When \(\beta\ne0\), the diagonal entries of both \(J_1\) and \(J_2\) are
nonzero:

\[
\begin{array}{c|cc}
 &c=a&c\ne a\\ \hline
 (J_1)_{cc}&\beta&-\alpha\\
(J_2)_{cc}&-\beta&-(h-1)\alpha.
\end{array}                                                \tag{23}
\]

Their direct scalars and literal targets, including both occurrences of
the factor \(h\), are

\[
\begin{aligned}
 \sigma(J_1)&=0,
 &T(J_1)&=\beta X_a-\alpha\Delta_{\bar a},\\
 \sigma(J_2)&=-h\alpha\beta,
 &T(J_2)&=-\beta X_a-(h-1)\alpha\Delta_{\bar a},\\
 {\cal P}(J_r)q^{[h-1]}&=hT(J_r)&& (r=1,2).
\end{aligned}                                             \tag{23a}
\]

Hence for either \(r=1,2\), and for any surviving label \(c\),

\[
        (J_r)_{cc}^{-1}\operatorname {CapRes}_c(J_r)
                            =\overline Y_c.                 \tag{24}
\]

Every denominator in (24) is displayed and nonzero on the generic
stratum.  Alternatively, the two cap rows recover the original channels
by

\[
 \rho_2={Z_1+Z_2\over h},\qquad
 \rho_0={(h-1)Z_1-Z_2\over h\beta}.                       \tag{25}
\]

Thus source representation and flat label transport of the normalized
generic jets are complete.  What (20)--(25) do not do is make their
nonzero diagonal targets into literal overlap boundaries.

## 4. A relative Taylor--Rees division lemma

The following elementary statement is the exact audit needed whenever a
scalar coordinate gcd is removed.

> **Lemma 4.1 (literal principal-parts criterion).**  Let \(k\) be a field,
> let \(N\subseteq M\) be vector spaces, put \(S=k[v,w]\), and write
> \[
>        P=\sum_{j=0}^d v^jw^{d-j}p_j\in M\otimes S_d.
> \]
> For \(0\le r\le d\), the following are equivalent.
>
> 1. There is \(Q\in M\otimes S_{d-r}\) such that
>    \(P-v^rQ\in N\otimes S_d\).
> 2. \(p_0,\ldots,p_{r-1}\in N\).
>
> When these conditions hold, the quotient is represented canonically by
> \[
>            Q=\sum_{j=r}^d v^{j-r}w^{d-j}p_j,             \tag{26}
> \]
> modulo \(N\otimes S_{d-r}\).  If \(M,N\) are filtered and \(N\) is a
> filtered subspace, (26) preserves every filtration grade.

**Proof.**  Reduce the asserted equality modulo \(v^r\).  The monomials
\(w^d,vw^{d-1},\ldots,v^{r-1}w^{d-r+1}\) are linearly independent, so the
equality can hold only if the first \(r\) coefficients belong to \(N\).
Conversely, with \(Q\) as in (26), the difference is exactly the sum of
those first \(r\) terms and lies in \(N\otimes S_d\).  If two quotients
work, their difference multiplied by \(v^r\) lies in \(N\otimes S\), so
their classes modulo \(N\) agree.  The formula never mixes coefficients,
which proves the filtered assertion. \(\square\)

For an arbitrary nonzero linear factor \(\ell\), choose \(v=\ell\) and
any complementary coordinate \(w\).  This is an invertible linear change
of binary coordinates, not localization at \(\ell\).  Lemma 4.1 then
applies verbatim.

Now let \(\epsilon:M\to V\) be evaluation of formal filtered source rows,
with \(N\subseteq\ker\epsilon\).  Scalar divisibility

\[
                    \epsilon(P)\in v^r(V\otimes S)        \tag{27}
\]

is equivalent to

\[
                         p_0,\ldots,p_{r-1}\in\ker\epsilon.
                                                                    \tag{28}
\]

By Lemma 4.1 it lifts through the literal source quotient if and only if
the stronger memberships

\[
                         p_0,\ldots,p_{r-1}\in N           \tag{29}
\]

hold.  Canonically, the obstruction is the truncated principal-parts class

\[
       \operatorname {obs}_{v,r}(P)
       =[P\bmod v^r]
       \in {\ker\epsilon\over N}\otimes_k(S/(v^r))_d.     \tag{30}
\]

Relative to the chosen complementary coordinate \(w\), its coordinates are
\(([p_0],\ldots,[p_{r-1}])\).  That tuple changes triangularly when \(w\)
is changed, but its vanishing and the class (30) are coordinate-independent.

Equations (27)--(30) prove (5) and show why a scalar gcd computation alone
cannot certify source-valid division.  They also handle the full
third-boundary multiplicity at once.

There is a two-dimensional exact guard.  Take
\(M=\langle z,r\rangle\), \(N=0\), and
\(\epsilon(z)=0,\epsilon(r)=1\).  Then

\[
                           P=wz+vr                       \tag{31}
\]

has \(\epsilon(P)=v\), but it is not divisible by \(v\) in \(M\otimes S\).
Its obstruction is the nonzero class of \(z\).  This is the formal shape
of the radial problem; adding the relation \(z\in N\) would make the
division valid.

## 5. Application to the third diagonal boundary

Let \(\widetilde\Omega_Z\) be a filtered source representative of the
diagonal clean residual after the factors of its distinct clean boundary
points have been removed.  Such a representative must retain the
direct/star/internal grades and the literal target rows.  On the generic
stratum, write

\[
 \ell=t+\beta u,\qquad
 \widetilde\Omega_Z=
       \sum_{j=0}^d\ell^jw^{d-j}P_j                     \tag{32}
\]

in any complementary coordinate \(w\).  If the evaluated coordinate gcd
has \(\ell\)-order \(r\), then

\[
                         P_0,\ldots,P_{r-1}\in\ker\epsilon. \tag{33}
\]

The chartwise residual \(\Xi\) used by the scalar two-boundary certificate
is source-valid precisely when

\[
                         P_0,\ldots,P_{r-1}\in N_{\rm lit}.
                                                                    \tag{34}
\]

No division by \(\ell\) is authorized before (34).  If (34) holds,
Lemma 4.1 gives the quotient by tail extraction (26), and the old
two-boundary certificate applies to that quotient.  If (34) fails, the
symmetric three-boundary complex has retained a genuine specialization
class which the asymmetric saturation discards.

The ordinary odd-residue functor has exactly the kind of kernel seen in
(31).  Equation (18) kills \(q_0\); the near-perfect gauge identity in
[the flat odd-residue note](common-coloop-odd-residue-and-flat-overlap.md)
kills all vertex-gauge quadratics.  The scalar relation (22) has lower
symbol \(r(K_1)\), whose residue is \(Z_1\), but it does not define a map
out of the radial generator.  Also, (12) gives

\[
              {\cal P}(J_r)q^{[h-1]}=hT(J_r)
              \qquad(r=1,2).                              \tag{35}
\]

Thus the cap representative has a nonzero target grade.  By
(18a)--(18b), *every* quadratic companion on the same complement and
against the same power with target \(-hT(J_r)\) has unnormalized ordinary
residue \(-hZ_r\), exactly opposite the residue \(hZ_r\) of
\({\cal P}(J_r)\).  After the common legal normalization by \(h\), these are
\(-Z_r\) and \(Z_r\).  The companion therefore erases the response rather
than making it a nonzero secondary class.
The literal curvature/anchor overlap must therefore supply a homotopy in
the adjacent-power mapping cone

\[
 d_c(\lambda,p)=\lambda A+pt_cB,                           \tag{35a}
\]

before passage to (16), or use a genuinely different odd quotient.  It
must null-homotope the target in the \(\lambda A\) grade while retaining
the lower-symbol class in the \(pt_cB\) grade and intertwine that homotopy
with the torus--Koszul differential.  This is the exact target-cancelled
transgression condition, now with the unequal diagonal vectors in (23).

Accordingly, the source-normal form (3) solves the representative and
normalization part of the generic diagonal jet.  It does not prove the
relative saturation memberships (34), nor the target-cancelled chain
property.  Those are the minimal remaining literal statements; replacing
them by coordinatewise division proves only (33).

## 6. The collision is an order-\(h\) blind-colour boundary

Use coordinates at the binary boundary

\[
                         v=t+\beta u,\qquad w=u.
\]

The direct scalar and target are

\[
             s=\alpha(v-\beta w),\qquad
             T=vX_a-\alpha w\Delta_{\bar a}.              \tag{36}
\]

Hence the two target components of the clean error correction have
transverse factors

\[
\begin{aligned}
 s^{h-1}T_a
   &=\alpha^{h-1}v(v-\beta w)^{h-1}X_a,\\
 s^{h-1}T_{\bar a}
   &=-\alpha^h w(v-\beta w)^{h-1}\Delta_{\bar a}.
\end{aligned}                                             \tag{37}
\]

If \(\beta\ne0\), the first expression has \(v\)-order one and the
second has order zero.  The first boundary jet therefore sees label
\(a\), and (21) gives its literal normalized cap representative.

If \(\beta=0\), (37) becomes

\[
 \alpha^{h-1}v^hX_a,
 \qquad -\alpha^h wv^{h-1}\Delta_{\bar a}.                \tag{38}
\]

The first selected-colour principal part occurs at order \(h\); the first
complementary part occurs at order \(h-1\).  At the same time, (3) gives

\[
 J_1=K_2=\alpha(E_{aa}-I),\qquad
 J_2=(h-1)J_1,                                            \tag{39}
\]

and therefore

\[
 \operatorname {CapRes}_a(J_1)
 =\operatorname {CapRes}_a(J_2)=0.                        \tag{40}
\]

Equations (38)--(40) prove that the blind colour is a genuine collision
of filtration orders.  It cannot be repaired by rescaling the first jet.
The unary anchor \({\cal P}(K_0)\) does have residue
\(\overline Y_a\), but it is outside the one-dimensional collided
boundary-polar span and must be connected through the order-\(h\) principal
part in (38).

Finally, minimum-order survival cannot force a complementary class in this
case.  Suppose

\[
                         \overline Y_b=\overline Y_c=0
                    \qquad(b,c\ne a).                     \tag{41}
\]

Then there are linear forms \(z_b,z_c\) on \(D\) with

\[
                   z_bq_0^{[h-1]}=Y_b,\qquad
                   z_cq_0^{[h-1]}=Y_c.                    \tag{42}
\]

On \(D\cup\{x\}\), put

\[
       \widetilde q=q_0+e_b^{(x)}z_b+e_c^{(x)}z_c.          \tag{43}
\]

The added part squares to zero because every one of its monomials uses
\(x\), and \(q_0^{[h]}=0\) because \(D\) has only \(2h-1\) sites.  Thus

\[
                    \widetilde q^{[h]}=X_b+X_c.            \tag{44}
\]

The aggregate \(\widetilde q\) can still contain cells carrying colour
\(a\), so (44) alone is not yet a palette statement.  Let \(\pi_{bc}\)
project every local colour space onto the \(b,c\) axes and put
\(q_{bc}=\pi_{bc}(\widetilde q)\).  Functoriality of divided powers gives

\[
                         q_{bc}^{[h]}=X_b+X_c.             \tag{45}
\]

Writing the nonzero pair cells of \(q_{bc}\) as decorated edges now gives
an exact source with palette exactly \(\{b,c\}\): no other colour occurs,
and the two unit constant coefficients ensure that both \(b\) and \(c\)
do occur.  Binary sources are allowed at every even order under
consideration, so (45) is not a ternary-minimality contradiction.
Therefore the case in which only \(\overline Y_a\) survives is a real
logical possibility at the present spine.

## 7. Exact remaining statement and scope

The new proved statements are:

1. both generic normalized jets have the division-free literal cap
   representatives (3), with exact residues (20)--(21);
2. generic labelwise transport uses only the displayed nonzero scalars in
   (23), and never a boundary factor;
3. Lemma 4.1 gives the necessary and sufficient all-multiplicity criterion
   for lifting scalar gcd saturation through any specified literal source
   quotient; and
4. at \(\beta=0\), selected-colour detection first occurs in order \(h\),
   the two ordinary jet rows collapse, and minimality alone cannot force a
   visible complementary class.

The exact positive lemma still needed on the diagonal branch is:

> For the actual filtered overlap module generated by the full-nine cap,
> connection, normal, curvature, direct-double, and diagonal-anchor rows,
> the principal parts in (33) belong to its literal boundary submodule as
> in (34), and one normalized cap row (3) admits a secondary
> adjacent-power target null-homotopy with the required torus--Koszul chain
> property.  A same-power quadratic companion is excluded by
> (18a)--(18b).  In the
> collision stratum, either the same comparison carries the unary anchor
> through the order-\(h\) principal part (38), or a separate physical
> argument forces a surviving complementary label.

This is narrower than the whole clean-point bridge and is common with the
off-diagonal target-cancelled transgression.  It has not been proved here.
In particular, Lemma 4.1 is a criterion, not an assertion that the current
literal boundary module is relatively saturated.  The conjecture remains
open.

The dependency-free checker
[`verify_diagonal_rees_saturation_cap_jet_bockstein.py`](../computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py)
audits the matrices and direct scalars, the cap-residue representatives,
the generic inverse and every permitted division (including the
\(\tau=0\) no-transition case), the collision rank drop, the same-power
target--residue lock with its factor of \(h\), the target valuations through
\(h=64\), the complementary-colour palette projection, and exact positive
and negative instances of Lemma 4.1 at several multiplicities.  The proof
above, rather than those finite checks, is uniform.

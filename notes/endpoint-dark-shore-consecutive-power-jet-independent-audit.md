# Independent audit: endpoint-dark consecutive-power jet

## 1. Verdict

**PASS after exact hypothesis and collision-language corrections.**  Every
numbered calculation in
[the source note](endpoint-dark-shore-consecutive-power-jet.md), including
the dark contractions, literal divided-power coefficients, the bounded
\(N_B/\Gamma_B\) criterion, the \(b=3\) Schur completion and four-column
catalecticant, both guards, and the one-bright jet, is correct under the
source's now-explicit off-diagonal anchor hypothesis.

The audit required five corrections to the source.

1. The canonical entry must satisfy \(a\ne b\), not merely
   \(a_{ab}\ne0\).  Without this, \(\operatorname{diag}K_*=-\alpha I\),
   \(\det K_*=(-\alpha)^3\), the uniform scalar target in (3), and the Schur
   step using \(K_*^{-1}\) need not hold.
2. The scalar identity in (3) comes from the off-diagonal contraction,
   whereas \(r^{[h]}\ne0\) is the separate rootless input.
3. A projective \(E_A\)-collision is contradictory only when the target
   values are not related by the same scalar.  A kernel witness is
   equivalent to an affine equal-image collision; a nonzero projective
   collision is a sufficient version, not an unconditional reformulation.
4. A transverse local label pair raises
   \(\operatorname{rank}\beta_A\) only when both corresponding
   tensor-product functionals survive at every other shore site.
5. The six-site guard retains one scalar contraction, not one distinguished
   physical row plus “the other eight physical rows.”  The corrected scope
   is the full-nine information beyond that scalar contraction.

Audited source SHA-256:

    5bf3ed8c346b38254e43b2c0170263f72304b13d389e67c5a30fa416f743e028

This is a hand algebra and matching audit.  The cofactor-overlap target in
Section 9 of the source remains open.  Nothing here proves that target,
closes the endpoint-dark branch, or proves the Krenn conjecture.

## 2. Algebra and canonical scalar contraction: PASS

The calculation takes place in the multilinear site algebra: a monomial
using one site twice vanishes, and for a quadratic \(q\),
\(q^{[k]}=q^k/k!\) is the weighted sum of \(k\)-edge matchings, with each
unordered matching occurring once.

Write \(\tau=\operatorname{tr}a\) and assume the corrected hypotheses

\[
 a\ne b,\qquad \alpha=a_{ab}\ne0,\qquad
 K_*=\tau E_{ab}-\alpha I.
\tag{A1}
\]

Because \(E_{ab}\) is off diagonal,

\[
 \sum_{i,j}(K_*)_{ij}a_{ij}
   =\tau a_{ab}-\alpha\operatorname{tr}a=0,
 \qquad (K_*)_{ii}=-\alpha.
\tag{A2}
\]

Moreover \(E_{ab}^2=0\), so

\[
 \det K_*=(-\alpha)^3\ne0.
\tag{A3}
\]

Multiplying the nine rows of source (1) by \((K_*)_{ij}\) and summing gives

\[
 rq^{[h-1]}=-\alpha(X_0+X_1+X_2).
\tag{A4}
\]

No implication from (A4) to \(r^{[h]}\ne0\) is used: the latter is the
rootless/gcd-one input.  This verifies source (2), (3), (17), and the later
use of invertibility.

## 3. Dark coefficient spaces and all-nine contractions: PASS

For \(K_x=\ker(P_x^*\oplus S_x^*)\), every
\(\lambda_x\in K_x\) kills every local \(p_i\)- and \(s_j\)-component.  On
a decomposable coefficient
\(\theta=\bigotimes_{x\in A}\lambda_x\), the target coefficient is

\[
 \beta_{A,i}(\theta)
  =\prod_{x\in A}\lambda_x(e_i^{(x)}).
\tag{A5}
\]

This verifies source (10)--(14).  A tensor-product functional
\(\beta_{A,i}\) is nonzero precisely when every local factor is nonzero.
Two nonzero such functionals are proportional precisely when their local
factors are proportional site by site.  The corrected source therefore
requires both global functionals to survive before one transverse site is
used to infer rank at least two.

Because \(|A|=2h-b\), contraction has the exact degrees

\[
 F_A:\mathcal K_A\longrightarrow({\cal R}_B)_b,
 \qquad
 E_A:\mathcal K_A\longrightarrow({\cal R}_B)_{b-2}.
\tag{A6}
\]

In \(p_i s_jq^{[h-1]}\), any summand placing either marked endpoint on
\(A\) has zero coefficient by darkness.  Both endpoints must lie on \(B\),
and contraction gives

\[
 a_{ij}F_A(\theta)+p_i^Bs_j^BE_A(\theta)
 =\delta_{ij}\beta_{A,i}(\theta)X_i^B.
\tag{A7}
\]

This proves source (6)/(16) first for decomposable coefficients and then,
by linearity, for all of \(\mathcal K_A\).  Applying (A2) to (A7) gives

\[
 r_BE_A(\theta)
   =-\alpha\sum_i\beta_{A,i}(\theta)X_i^B.
\tag{A8}
\]

The three \(X_i^B\) are linearly independent.  Hence
\(\ker E_A\subseteq\ker\beta_A\), and factorization through
\(\mathcal K_A/\ker E_A\) gives

\[
 \operatorname{rank}\beta_A\le\operatorname{rank}E_A.
\tag{A9}
\]

This verifies source (4)--(8) and (15)--(17) without a no-cancellation or
support assumption.

## 4. The two-site consecutive-power jet: PASS

At \(h=3\), expose \(A=\{x,y\}\) and put \(D=W\setminus A\).  A matching in
\(q^{[2]}\) covering \(x,y\) has exactly one of two forms:

* it uses \(xy\) and one edge in \(D\); or
* it uses one \(x\)-to-\(D\) edge and one \(y\)-to-\(D\) edge.

The second product automatically discards coincident \(D\)-endpoints in
the site algebra.  Thus, with source notation \(u,t,v'\), and \(T=tv'\),

\[
 E_A(v,w)=uz+T.
\tag{A10}
\]

For \(q^{[3]}\), the direct-edge branch leaves a two-edge matching in \(D\),
whereas the two-star branch leaves one \(D\)-edge.  Consequently

\[
 F_A(v,w)=uz^{[2]}+Tz.
\tag{A11}
\]

There are no factors \(2\), \(1/2\), or \(3\): division by \(k!\) leaves
each matching once.  Substitution into (A7) is exactly source (20).

If

\[
 E_A(\widetilde v,\widetilde w)=cE_A(v,w)\ne0,
\tag{A12}
\]

then their scaled difference lies in \(\ker E_A\), so (A8) forces

\[
 (\widetilde v_i\widetilde w_i)_i=c(v_iw_i)_i.
\tag{A13}
\]

This is the exact collision criterion.  In the cited coefficient-dark
lemma both \(T\)'s vanish; the two nonzero diagonal rows force both \(u\)'s
and \(z\) to be nonzero, so the \(E_A\)-values lie on \(\mathbb Cz\), while
the crossed target incidence violates (A13).  Thus the complete-cofactor
collision criterion really is weaker than requiring \(T=0\).

The three bilinear functions \(v_iw_i\) are the restrictions of the three
linear functionals \(\beta_{\{x,y\},i}\) to decomposable tensors.  Since
decomposable tensors span \(K_x\otimes K_y\), rank at least two yields two
decomposable probes with nonproportional nonzero target vectors.  It does
not yield an \(E_A\)-collision.  This verifies source (18)--(23) and its
stated limitation.

## 5. Minimal-circuit and support claims: PASS

For a one-element circuit of the union matroid, the site is a loop of both
endpoint matroids.  Every \(p_i\) and \(s_j\) therefore has zero component
there.  The response \(r\) is supported on the other five sites, so a
three-edge matching is impossible and \(r^{[3]}=0\), contradicting the
separate rootless input.

For a two-element minimal circuit of type \((0,1)\), the first endpoint
vanishes on both sites and the two nonzero second-endpoint row images are
the same line.  Thus source (25), (26) follow.  In its displayed example,

\[
 K_x=\{v_0=0\},\qquad K_y=\{w_1=0\},
\]

so \(\beta_0=0\), \(\beta_1=0\), and only \(\beta_2\) survives.  The
claimed rank-one target is correct.

For three exposed sites, a two-edge matching covering all three contains
one internal exposed edge and one star from the remaining exposed site.
This gives exactly

\[
 E_A=u_{xy}t_z+u_{xz}t_y+u_{yz}t_x.
\tag{A14}
\]

If the three dark lines are the three different coordinate-covector axes,
every constant-colour triple product vanishes.  The source therefore
records darkness without claiming target incidence or a kernel witness.

## 6. The bounded \(N_B/\Gamma_B\) criterion: PASS

For \(|B|=3\), \(E_A\) takes values in the nine-dimensional degree-one
space.  Because the anchor \((a,b)\) is off diagonal, its contracted row is

\[
 \alpha F_A+p_a^Bs_b^BE_A=0.
\tag{A15}
\]

Multiplying the \((i,j)\) row by \(\alpha\) and subtracting \(a_{ij}\)
times (A15) gives

\[
 \begin{cases}
  (\alpha p_i^Bs_j^B-a_{ij}p_a^Bs_b^B)E_A=0,&i\ne j,\\
  (\alpha p_i^Bs_i^B-a_{ii}p_a^Bs_b^B)E_A
       =\alpha\beta_{A,i}X_i^B,&i=j.
 \end{cases}
\tag{A16}
\]

These are exactly the definitions of \(G_{ij}\), \(D_i\), \(N_B\), and
\(\Gamma_B\).  Uniqueness of \(\Gamma_B(e)_i\) follows from \(X_i^B\ne0\),
and (A16) proves

\[
 \operatorname{im}E_A\subseteq N_B,
 \qquad
 \Gamma_BE_A=\alpha\beta_A.
\tag{A17}
\]

Therefore

\[
 \operatorname{rank}\beta_A
 \le\operatorname{rank}\Gamma_B
 \le\dim N_B\le9.
\tag{A18}
\]

This verifies source (29)--(31d).  In particular, the source does not
reverse the needed inequality: closure would require a target rank larger
than the admissible multiplier rank or dimension.

## 7. The \(b=3\) Schur completion and catalecticant: PASS

In the high-order \((1,1)\) branch,

\[
 p_i|_A=\lambda_iU,\qquad s_j|_A=\mu_jV,
\]

so \(r_A=\kappa UV\), with
\(\kappa=\lambda^{\mathsf T}K_*\mu\).  If \(h>3\) and this tensor vanished,
every response edge incident with one of the \(2h-3>3\) shore sites would
have to end in \(B\).  No perfect matching could exist, contradicting
\(r^{[h]}\ne0\).  Hence \(\kappa\ne0\) and \(UV\ne0\), exactly in the
stated \(h>3\) range.

Expanding the complete response gives

\[
 r=\kappa UV+U\ell+mV+r_B,
 \quad
 \ell=\lambda^{\mathsf T}K_*S_B,
 \quad
 m=P_B^{\mathsf T}K_*\mu.
\tag{A19}
\]

With

\[
 \widehat U=U+\kappa^{-1}m,\quad
 \widehat V=V+\kappa^{-1}\ell,\quad
 \widehat r_B=r_B-\kappa^{-1}m\ell,
\]

direct multiplication gives

\[
 r=\kappa\widehat U\widehat V+\widehat r_B.
\tag{A20}
\]

Also

\[
 \widehat r_B=P_B^{\mathsf T}\widehat K S_B,\qquad
 \widehat K
 =K_*\bigl(I-\kappa^{-1}\mu\lambda^{\mathsf T}K_*\bigr).
\tag{A21}
\]

The parenthesized factor is an idempotent rank-two projection because
\(\lambda^{\mathsf T}K_*\mu=\kappa\).  Since \(K_*\) is invertible,
\(\widehat K\) has rank two, with
\(\lambda^{\mathsf T}\widehat K=0\) and \(\widehat K\mu=0\).
Source (33a) and both radical claims are correct.

Any two quadratic edges supported on three sites collide, so
\(\widehat r_B^{[2]}=0\).  The divided-power binomial formula yields

\[
 r^{[h]}
  =\kappa^h(\widehat U\widehat V)^{[h]}
   +\kappa^{h-1}(\widehat U\widehat V)^{[h-1]}\widehat r_B,
\tag{A22}
\]

with coefficient one on both terms.  For linear forms,

\[
 (\widehat U\widehat V)^{[h]}
     =h!\,\widehat U^{[h]}\widehat V^{[h]},
 \qquad
 (\widehat U\widehat V)^{[h-1]}
     =(h-1)!\,\widehat U^{[h-1]}\widehat V^{[h-1]}.
\tag{A23}
\]

Let \(m_A=2h-3\) and \(C_t=U^{[t]}V^{[m_A-t]}\).  Filling all shore sites
leaves the following \(B\)-parts:

| \(t\) | first term of (A22) | second term of (A22) |
|---|---|---|
| \(h-3\) | \(h!\widehat U_B^{[3]}\) | \(0\) |
| \(h-2\) | \(h!\widehat U_B^{[2]}\widehat V_B\) | \((h-1)!\widehat U_B\widehat r_B\) |
| \(h-1\) | \(h!\widehat U_B\widehat V_B^{[2]}\) | \((h-1)!\widehat V_B\widehat r_B\) |
| \(h\) | \(h!\widehat V_B^{[3]}\) | \(0\) |

Restoring \(\kappa^h\) and \(\kappa^{h-1}\) gives exactly the four \(D_t\)'s
in the source and hence

\[
 r^{[h]}=\sum_{t=h-3}^{h}C_t\otimes D_t.
\tag{A24}
\]

No factorial or exponent in source (33b), (33c) is missing.  Since each
shore-local factor lies in \(\langle U_x,V_x\rangle\), the asserted local
flattening rank bound two is also correct.

If \(j\) is the number of cross edges and \(k\) the number of
\(B\)-internal edges in a perfect matching, the three \(B\)-sites impose
\(j+2k=3\).  The only solutions are \((j,k)=(1,1)\) and \((3,0)\), with
respectively \(h-2\) and \(h-3\) \(A\)-internal edges.  Divided-power
multinomial coefficients cancel, yielding source (34) with coefficient one
on each parity layer.

## 8. Six-site scalar-rootless guard: PASS with non-full-nine scope

For source (36), the response derived from (37) and \(K_*=I\) is

\[
 r=a_0x_0+a_0y_1+b_1x_0+b_1y_1+c_2d_2.
\tag{A25}
\]

There are precisely three choices of an \(r\)-edge and two \(q\)-edges
covering all six sites:

\[
 ax\mid yd\mid bc,\qquad
 by\mid xc\mid ad,\qquad
 cd\mid xa\mid yb.
\]

They give \(X_0,X_1,X_2\), respectively.  Each matching occurs once in
\(q^{[2]}\), so

\[
 rq^{[2]}=X_0+X_1+X_2.
\tag{A26}
\]

The two \(r\)-perfect matchings \(ax\mid by\mid cd\) and
\(ay\mid bx\mid cd\) give the same mixed word with the same sign.  Its
coefficient in \(r^{[3]}\) is exactly \(2\), proving nonnilpotence.

The endpoint triples are injective: \(p_0,p_1,p_2\) have independent
components visible at \(b,a,c\), and \(s_0,s_1,s_2\) have independent
components visible at \(x,a,d\).  On \(A=\{x,y\}\), \(P\) vanishes and the
two nonzero local \(S\)-row images are the same row-index line.  Each
singleton has combined rank one, so this is a minimal \((0,1)\) circuit;
its deletion ranks also make it the maximal \(b=4\) witness.

The dark planes are exactly

\[
 K_x=\langle\epsilon_1^{(x)},\epsilon_2^{(x)}\rangle,
 \qquad
 K_y=\langle\epsilon_0^{(y)},\epsilon_2^{(y)}\rangle.
\]

The four basis coefficients of \(E_A\) in source (43) live on the four
different site pairs \(cd,cb,ad,ab\), so
\(\operatorname{rank}E_A=4\).  Only the colour-two target survives, so
\(\operatorname{rank}\beta_A=1\).  Multiplication by \(r_B=c_2d_2\) kills
the first three terms and sends the last to \(v_2w_2X_2^B\), verifying
source (44).

Taking \(a=-E_{01}\) gives \(\alpha=-1\), trace zero, and \(K_*=I\), so
(A26) is exactly the canonical scalar contraction.  The guard is not full
nine:

\[
 p_0s_0q^{[2]}=X_0+X_1\ne X_0.
\tag{A27}
\]

Thus every positive property claimed for this guard is present, and the
source explicitly disclaims the missing full-nine information.

## 9. Uniform fully-dark equality guard: PASS with contracted scope

For \(h\ge4\), the source sets \(|A|=2h-3\) and
\(B=\{b_1,b_2,b_3\}\).  The endpoint restrictions on \(A\) have aggregate
ranks \((1,1)\), and those ranks remain one after any shore-site deletion.
Moreover

\[
 \sum_i c_ip_i=c_0U+(c_0+c_1+c_2)x+c_1z_1,
\]

and

\[
 \sum_j d_js_j=d_1V+(d_0+d_1+d_2)y+d_2z_2.
\]

Both expressions vanish only for the zero coefficient vector, proving
both endpoint triples injective.  At each shore site, the local endpoint
span is \(\langle e_1,e_2\rangle\), so

\[
 K_x=\mathbb C\epsilon_0^{(x)},\qquad
 \beta_A=(1,0,0).
\tag{A28}
\]

Also \(3+\rho_P(A)+\rho_S(A)=5\), while moving any shore site into \(B\)
raises this to \(6\); the claimed maximal deletion-stable shore is genuine.

The quadratic in source (52) is one monochromatic perfect matching: the
\(b_1b_2\) edge together with the perfect matching \(M\) on
\(A\cup\{b_3\}\).  Contracting \(q^{[h]}\) by the unique dark generator
leaves \(X_0^B\).  In \(q^{[h-1]}\), the only matching covering every shore
site is \(M\), which leaves \(z_0\).  Source (53) is therefore the literal
pair of consecutive cofactors of the same \(q\), each with coefficient one.

Here \(a=E_{00}-J\), so \(a_{00}=0\), every other entry is \(-1\),
\(\alpha=-1\), and \(K_*=I-2E_{01}\).  For all \(i,j\),

\[
 p_i^Bs_j^Bz_0=X_0^B,
\]

because every \(z_1\) or \(z_2\) term collides with \(z_0\).  Thus the
\((0,0)\) contracted row equals \(X_0^B\), and each of the other eight rows
is \(-X_0^B+X_0^B=0\).  All nine fully dark contracted rows really hold.
Since \(\mathcal K_A\) is one-dimensional, checking its generator checks
the entire contracted jet.

The bounded admissible space is exact.  Two off-diagonal equations are

\[
 xz_2e=0,\qquad z_1ye=0.
\]

They kill the \(b_2\)- and \(b_1\)-components of \(e\), respectively.
Then \(D_0=-xy\), and \(D_0e\in\mathbb CX_0^B\) restricts the remaining
\(b_3\)-component to \(\mathbb Cz_0\).  Therefore

\[
 N_B=\mathbb Cz_0,\qquad
 \Gamma_B(z_0)=(-1,0,0)=\alpha\beta_A.
\tag{A29}
\]

Thus all three ranks in source (54) are one.

Expanding \(\sum_{i,j}(I-2E_{01})_{ij}p_is_j\) gives source (55):

\[
 r=-2UV-Uy-xV+Vz_1+xy+xz_2+z_1y.
\tag{A30}
\]

For the word in source (56), \(xz_2\) is forced, one of the \(h-1\)
colour-one shore sites must use \(-Uy\), and the remaining two shore colour
classes are paired bijectively through \(-2UV\).  There are
\((h-1)(h-2)!\) such matchings, all with the same weight
\(-(-2)^{h-2}\).  The exact coefficient is therefore

\[
 -(h-1)(-2)^{h-2}(h-2)!\ne0.
\tag{A31}
\]

The three-cross layer cannot contribute because the prescribed colour two
at \(b_3\) forces the \(B\)-internal edge \(xz_2\).  Thus \(r^{[h]}\ne0\)
is genuinely established.

The guard does not satisfy the uncontracted full-nine system, exactly as
the source says.  If \(u\in A\) is paired with \(b_3\) in \(M\), then

\[
 E_u=e_0^{(u)}z_0+xy,\qquad
 F_u=e_0^{(u)}xyz_0.
\]

In the \((0,2)\) row, the \(e_0^{(u)}xyz_0\) terms cancel, while the \(xy\)
cofactor contributes the surviving off-diagonal word

\[
 e_1^{(u)}xyz_2\ne0.
\tag{A32}
\]

This verifies both the positive guard ledger and its advertised first
failure.  It guards only the fully dark jet; it is not a global full-nine
counterexample.

## 10. The one-bright jet: PASS

Leaving \(x\in A\) free and contracting \(2h-4\) sites gives degrees four
and two, exactly as in source (57).  Replacing the three-site complement by
\(C_x=B\cup\{x\}\) in the anchor elimination proves source (58), and
successive coefficient contraction proves (59).

Every degree-two element on \(C_x\) decomposes uniquely as

\[
 E_x=H_x+T_x,\qquad
 H_x\in({\cal R}_B)_2,\qquad
 T_x\in V_x\otimes({\cal R}_B)_1.
\]

Expanding
\((p_i^B+\lambda_iU_x)(s_j^B+\mu_jV_x)(H_x+T_x)\) leaves exactly

\[
 p_i^Bs_j^BT_x,\qquad
 \lambda_iU_xs_j^BH_x,\qquad
 \mu_jp_i^BV_xH_x.
\tag{A33}
\]

The \(p_i^Bs_j^BH_x\) term has degree four on only three sites; terms with
a local endpoint and \(T_x\) repeat \(x\); and \(U_xV_x=0\).  Thus source
(61) has no omitted term.  Applying the same off-diagonal anchor
elimination gives precisely \(G_{ij},D_i,C_{ij,x}\) in source (62), (63),
with no extra scalar or sign.

## 11. Exact scope

The audit establishes the following, and only the following.

* The dark contraction of a genuine full-nine packet factors all fixed
  target functionals through the literal consecutive cofactor \(E_A\).
* The two-site formulas, the \(N_B/\Gamma_B\) criterion, Schur response,
  four-column catalecticant, parity split, and one-bright compatibility
  system are exact identities.
* The Section 7 guard satisfies the scalar-rootless, actual-power,
  injectivity, and minimal-dark-shore claims, but not full nine.
* The Section 8 guard satisfies all nine fully dark contracted rows, actual
  consecutive powers, maximal deletion-stable \((1,1)\) darkness,
  injectivity, equality in the bounded rank test, and response
  nonnilpotence, but not the first one-bright full-nine jet.

The desired kernel coefficient in source Section 9 is not produced by any
argument audited here.  The source correctly leaves it as the next
source-overlap target rather than claiming conjecture closure.

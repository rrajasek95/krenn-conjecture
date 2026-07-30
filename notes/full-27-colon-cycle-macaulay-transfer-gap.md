# The last overlap row completes a colon cycle, not a cancellation

## 1. Outcome

On an odd common complement of size \(2h-1\), write the complete triple
rows as

\[
 \mathscr R^{(h)}_{ijk}:=
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[h-1]}
 +x_iy_jt_kz^{[h-2]}-\mathbf1_{i=j=k}X_i .              \tag{1}
\]

Assume the target-centred kernel cross, with

\[
 \operatorname {supp}\xi=\{e,a\},\qquad
 \operatorname {supp}\eta=
 \operatorname {supp}\eta'=\{e,b\},\qquad
 \{e,a,b\}=\{0,1,2\},                                  \tag{2}
\]

and

\[
 \xi^{\mathsf T}P=\xi^{\mathsf T}R=0,\qquad
 P\eta=0,\qquad R\eta'=0.                               \tag{3}
\]

Order the \(\{e,a\}\)-compression as

\[
 T_{\{e,a\}}=\begin{pmatrix}A&B\\ C&D\end{pmatrix},
 \qquad B=T_{ea},\quad C=T_{ae},                         \tag{4}
\]

and put

\[
 \omega=C\,y_et_a-B\,y_at_e.                            \tag{5}
\]

The left-kernel rectangle proves, without cancellation,

\[
              L\omega z^{[h-2]}=0,\qquad L=x(\xi).       \tag{6}
\]

Restoring the previously omitted literal row \((b,e,a)\) does **not**
strengthen (6) to \(\omega=0\).  Its exact, uniform consequence is the
filtered cycle

\[
 \boxed{
 x_b\omega z^{[h-2]}+\Gamma_bz^{[h-1]}=0,}              \tag{7}
\]

where

\[
 \Gamma_b=
 C(P_{be}t_a+R_{ba}y_e)
 -B(P_{ba}t_e+R_{be}y_a).                               \tag{8}
\]

There is no factor of \(h-1\) in (7).  The radial terms cancel before
the divided-power normalization is used.

An exact rational packet below has all 27 rows, rank-two \(P,R\), the
noncoordinate kernels (2)--(3), three normalized nonzero diagonal target
coefficients, invertible \(T_{\{e,a\}}\), injective endpoint stars, and
nonzero selected curvature.  Nevertheless

\[
       \omega z^{[h-2]}\ne0,\qquad
       L\omega z^{[h-2]}=0,                              \tag{9}
\]

while (7) holds.  The construction suspends uniformly to every
\(h\ge3\).  Thus the last row converts the explicit colon class into a
literal direct--star source cycle; it does not kill that class.

The guard is deliberately a scalar square-zero projection of the
decorated matching algebra.  It retains every displayed row and target
coefficient, but

\[
                         X_0=X_1=X_2=\Omega_h             \tag{10}
\]

are collinear scalar top classes, not three independent physical
pure-colour tensors.  It is therefore not a monochromatic graph and not a
counterexample to a theorem using full target-purity provenance.  Its
precise force is:

> No argument using only the static site-algebra rows (1), the displayed
> kernels, ranks, curvature, and divided-power identities can deduce
> \(\omega=0\) or a Macaulay rank defect.  A positive proof must use the
> decorated source provenance discarded by the scalar projection.

That missing input can now be named exactly: a decorated
filtered-to-Hankel chain map which sends the source cycle
\((\omega,\Gamma_b)\) to one nonzero common dual of the
degree-\((2h-1)\) clean Macaulay map.  Section 6 states the required map.
The conjecture remains open.

## 2. Exact general-\(h\) weighted residual

The two relevant residuals are

\[
\begin{aligned}
 \mathscr R^{(h)}_{bea}
  ={}&(P_{be}t_a+R_{ba}y_e+B x_b)z^{[h-1]}
       +x_by_et_az^{[h-2]},\\
 \mathscr R^{(h)}_{bae}
  ={}&(P_{ba}t_e+R_{be}y_a+C x_b)z^{[h-1]}
       +x_by_at_ez^{[h-2]} .                              \tag{11}
\end{aligned}
\]

Both target terms are zero because \(b,e,a\) are distinct.  Multiply the
first row by \(C\), the second by \(B\), and subtract.  The two radial
terms \(CBx_bz^{[h-1]}\) and \(BCx_bz^{[h-1]}\) cancel literally.  What
remains is

\[
 \boxed{
 C\mathscr R^{(h)}_{bea}-B\mathscr R^{(h)}_{bae}
 =x_b\omega z^{[h-2]}+\Gamma_bz^{[h-1]}.}                \tag{12}
\]

This proves (7) when the two literal rows hold.  In particular, (12) is
not obtained by dividing through \(Lz^{[h-2]}\), \(x_b\), or any power of
\(z\).

For comparison, contracting (1) by \(\xi_i\) first gives

\[
 L\left(y_jt_k+{T_{jk}\over h-1}z\right)z^{[h-2]}
       =\delta_{jk}\xi_jX_j.                              \tag{13}
\]

The \(C\)-weighted \((e,a)\) member minus the \(B\)-weighted \((a,e)\)
member of (13) is exactly (6).  Equation (12) is the unsuspended lift of
that colon relation at the complementary first label \(b\).

## 3. The selector conic sees exactly this cycle

Assume

\[
                         \Delta_T=AD-BC\ne0.              \tag{14}
\]

The isotropic rank-one selectors on the \(\{e,a\}\)-square have the
parametrization

\[
 u(s,t)=\binom{s}{t},\qquad
 v(s,t)=\binom{-(Bs+Dt)}{As+Ct}.                          \tag{15}
\]

Their two diagonal target coefficients are

\[
                 f_e=-Bs^2-Dst,\qquad f_a=Ast+Ct^2.      \tag{16}
\]

The quadratic covector

\[
                    \vartheta_2=(-DC,BC,-AB)             \tag{17}
\]

annihilates both (16).  Applied to the matrix
\(H=u(s,t)v(s,t)^{\mathsf T}\), it has only two nonzero entries:

\[
 \vartheta_2(H_{ea})=-C\Delta_T,\qquad
 \vartheta_2(H_{ae})=B\Delta_T.                          \tag{18}
\]

Now contract the fixed-\(b\) rows of (1) by \(H\).  Since
\(u^{\mathsf T}T_{\{e,a\}}v=0\) and the \(b\)-target is absent on this
two-label selector, this is the literal quadratic source family

\[
 \bigl((P_bu)t(v)+(R_bv)y(u)\bigr)z^{[h-1]}
       +x_by(u)t(v)z^{[h-2]}=0.                           \tag{19}
\]

Equations (18)--(19) give

\[
 \vartheta_2(\text{equation }(19))
 =-\Delta_T\bigl(x_b\omega z^{[h-2]}
                         +\Gamma_bz^{[h-1]}\bigr).        \tag{20}
\]

Thus the restored row does something precise and useful: it realizes the
third selector-conic direction as a filtered literal cycle.  But
\(\vartheta_2\) has selector parameter degree two.  It is not a functional
on \(\operatorname {Sym}^{2h-1}\mathbb C^2\), and (20) supplies no
canonical comparison with the parameter of the clean degree-\(h\) line.

## 4. A rank-two/rank-two 27-row exact guard

Work first at \(h=3\) in

\[
 {\cal A}_5=\mathbb Q[u_0,u_1,u_2,u_3,u_4]/(u_0^2,\ldots,u_4^2),
 \qquad \Omega=u_0u_1u_2u_3u_4.                          \tag{21}
\]

Take \(e=0,a=1,b=2\) and

\[
 z_0=4u_1u_2+u_1u_3+u_2u_4,
 \qquad z_0^{[2]}=u_1u_2u_3u_4.                          \tag{22}
\]

Use the three star triples

\[
\begin{array}{lll}
 x_0=\frac18u_4,&
 x_1=-\frac13(u_0+u_4),&
 x_2=\frac12u_3,\\[2mm]
 y_0=u_0+u_2,&y_1=-u_1,&y_2=u_1+u_2-u_3,\\
 t_0=-u_2+u_3+u_4,&t_1=u_4,&
 t_2=-u_0-u_1-u_2+u_3.
\end{array}                                               \tag{23}
\]

All three \(3\times5\) coefficient matrices in (23) have rank three.  Set

\[
 P=\begin{pmatrix}
 -3/8&0&3/8\\ 1&0&-1\\ 3/2&1/2&-3/2
 \end{pmatrix},\qquad
 R=\begin{pmatrix}
 5/8&0&-5/8\\ -5/3&0&5/3\\ -2&-2&2
 \end{pmatrix},                                          \tag{24}
\]

and

\[
 T=\begin{pmatrix}
 -9&-1&0\\ 1&-3&1\\ 2&3&-2
 \end{pmatrix}.                                          \tag{25}
\]

Finally take

\[
 \xi=(-8,-3,0)^{\mathsf T},\qquad
 \eta=\eta'=(1,0,1)^{\mathsf T},\qquad
 X_0=X_1=X_2=\Omega                                      \tag{26}
\]

in this scalar projection.  Exact substitution gives

\[
 \boxed{
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z_0^{[2]}
 +x_iy_jt_kz_0=\mathbf1_{i=j=k}\Omega
 \quad\text{for all }i,j,k.}                            \tag{27}
\]

Thus all 27 rows hold, including both \((b,e,a)\) and \((b,a,e)\), and
each diagonal coefficient is normalized to one.  Moreover

\[
\begin{gathered}
 \operatorname {rank}P=\operatorname {rank}R=2,\\
 \xi^{\mathsf T}P=\xi^{\mathsf T}R=0,\qquad
 P\eta=R\eta'=0,\qquad L=x(\xi)=u_0.                     \tag{28}
\end{gathered}
\]

The selector square is genuinely generic:

\[
 T_{\{e,a\}}=\begin{pmatrix}-9&-1\\1&-3\end{pmatrix},
 \qquad \det T_{\{e,a\}}=28,\qquad (B,C)=(-1,1).          \tag{29}
\]

Here

\[
\begin{aligned}
 \omega&=y_0t_1+y_1t_0\\
 &=u_0u_4+u_2u_4+u_1u_2-u_1u_3-u_1u_4,                  \tag{30}\\
 \omega z_0&=4u_0u_1u_2u_4+u_0u_1u_3u_4\ne0,\\
 L\omega z_0&=0.                                        \tag{31}
\end{aligned}
\]

The companion (8) is

\[
 \Gamma_b=-2u_0+2u_1-\frac52u_2+\frac12u_3+2u_4.        \tag{32}
\]

Since \(x_b=u_3/2\), equations (22), (30), and (32) give the nontrivial
cancellation

\[
                    x_b\omega z_0=2\Omega,
 \qquad \Gamma_bz_0^{[2]}=-2\Omega.                      \tag{33}
\]

This is (7), with neither summand zero.  Thus even the restored literal
row does not kill the colon class.

The selected physical curvature also survives.  At site \(u_4\), use

\[
 A_{\rm sel}=P_{be}=\frac32,\qquad
 B_{\rm sel}=R_{ba}=-2,\qquad
 F=[u_4]y_e=0,\qquad U=[u_4]t_a=1.
\]

Then

\[
                         A_{\rm sel}U-B_{\rm sel}F
                              ={3\over2}\ne0.             \tag{34}
\]

No source minor has been substituted for this literal scalar.

## 5. Uniform suspension to every odd complement

For \(h>3\), adjoin \(2h-6\) square-zero variables
\(v_1,\ldots,v_{2h-6}\), put

\[
 q_h=\sum_{r=1}^{h-3}v_{2r-1}v_{2r},\qquad
 z_h=z_0+q_h,\qquad
 V_h=\prod_{r=1}^{2h-6}v_r.                              \tag{35}
\]

Keep (23)--(26) unchanged and replace every target by
\(\Omega_h=\Omega V_h\).  The divided-power binomial formula is

\[
 (z_0+q_h)^{[m]}=\sum_{r=0}^{m}z_0^{[r]}q_h^{[m-r]}.     \tag{36}
\]

Every row has total degree \(2h-1\), the number of available sites.  A
surviving monomial must therefore use every \(v_r\).  In a direct term,
this forces the unique summand
\(z_0^{[2]}q_h^{[h-3]}\).  In a cubic-star term, the old five sites leave
room for exactly one copy of \(z_0\), so the unique summand is
\(z_0q_h^{[h-3]}\).  Since the \(h-3\) edges of \(q_h\) are disjoint,

\[
                         q_h^{[h-3]}=V_h.                 \tag{37}
\]

Consequently

\[
\begin{aligned}
 \ell z_h^{[h-1]}&=\ell z_0^{[2]}V_h
       &&\text{for every old linear form }\ell,\\
 x_iy_jt_kz_h^{[h-2]}&=x_iy_jt_kz_0V_h.                 \tag{38}
\end{aligned}
\]

Equation (27) therefore tensors by \(V_h\), proving all 27 instances of
(1) for every \(h\ge3\).  There is no hidden binomial coefficient in
(38): divided powers are exactly what makes the coefficient in (36)
equal to one.

The colon class and its completed cycle tensor in the same way:

\[
\begin{aligned}
 \omega z_h^{[h-2]}&=(\omega z_0)V_h\ne0,\\
 L\omega z_h^{[h-2]}&=(L\omega z_0)V_h=0,\\
 x_b\omega z_h^{[h-2]}+\Gamma_bz_h^{[h-1]}
   &=(x_b\omega z_0+\Gamma_bz_0^{[2]})V_h=0.             \tag{39}
\end{aligned}
\]

This proves the promised all-order static guard.  It is not a finite-\(h\)
case census.

## 6. The genuinely missing decorated filtered-to-Hankel map

Let \(S=\mathbb C[s,t]\), and let \({\cal E}\subseteq S_h\) be the scalar
coordinate space of the clean degree-\(h\) error on the canonical binary
line.  The rootless contradiction requires a nonzero

\[
 \theta=(\theta_0,\ldots,\theta_{2h-1})
       \in\ker\left(
       \mu_{\cal E}^{*}:(S_{2h-1})^*
          \longrightarrow({\cal E}\otimes S_{h-1})^*
                  \right).                               \tag{40}
\]

If

\[
             f_\alpha(s,t)=\sum_{k=0}^{h}c_{\alpha,k}
                                  s^{h-k}t^k\in{\cal E},
\]

then (40) is the common Hankel system

\[
 \boxed{
 \sum_{k=0}^{h}c_{\alpha,k}\theta_{k+j}=0
 \quad\text{for every }\alpha\text{ and }0\le j\le h-1.} \tag{41}
\]

The restored overlap row supplies instead the site-algebra cycle

\[
 \zeta_h=(\omega,\Gamma_b),\qquad
 d_h(\omega,\Gamma_b):=
 x_b\omega z^{[h-2]}+\Gamma_bz^{[h-1]}=0.                \tag{42}
\]

A sufficient positive continuation is therefore a source-derived map

\[
 \boxed{
 \operatorname {Tr}_h:
 H^{\rm filt}_1(\text{decorated triple-row packet})
       \longrightarrow\ker(\mu_{\cal E}^{*})}            \tag{43}
\]

with the following three properties.

1. The literal cycle represented by \(\zeta_h\) has a well-defined image;
   changing it by direct/star/internal filtered row boundaries does not
   change that image.
2. \(\operatorname {Tr}_h([\zeta_h])\ne0\).
3. Its one image satisfies all of (41), for every clean coordinate and
   every one of the \(h\) shifts.  In particular, it is not a separate
   functional for each target anchor or each chart.

Here \(H^{\rm filt}_1\) is notation for the homology of the actual
grade-preserving decorated source-row complex to be constructed; it is
not asserted to follow from the scalar site algebra.  Formula (20)
identifies the candidate class on the selector side.  What is absent is
the comparison between the selector-conic parameter and the canonical
clean-line parameter which turns its three quadratic coefficients into
the \(2h\) Hankel coefficients in (41).

The necessity of source provenance is exact.  Independently decorate the
static packet by the two formal clean forms

\[
                              f=s^h,\qquad g=t^h.          \tag{44}
\]

Then

\[
 fS_{h-1}=\langle s^{2h-1},\ldots,s^ht^{h-1}\rangle,
 \qquad
 gS_{h-1}=\langle s^{h-1}t^h,\ldots,t^{2h-1}\rangle,     \tag{45}
\]

and the two spaces in (45) form the entire monomial basis of
\(S_{2h-1}\).  Thus \(\mu_{\langle f,g\rangle}\) has rank \(2h\) and its
dual kernel is zero for every \(h\).  Decoration (44) is not claimed to
come from the same Krenn source.  It proves the narrower logical point:
the static identities (6)--(7), even with all 27 rows, do not define the
transfer (43).  Establishing its source compatibility is the remaining
theorem, not an automatic prolongation.

## 7. Exact scope and checker

The positive result is the exact general-\(h\) residual (12), together
with its selector-conic interpretation (20).  The sharp negative result
is the uniform rank-two/rank-two scalar guard (21)--(39).  It rules out
all of the following static inferences:

* cancelling \(Lz^{[h-2]}\) in (6);
* cancelling \(x_b\) or \(z^{[h-2]}\) in (7);
* deducing \(\omega=0\) from the restored row;
* deducing a common Macaulay dual merely because both site degree and
  parameter degree equal \(2h-1\).

The guard does **not** identify the scalar copies of \(\Omega_h\) with
three independent residual pure-colour tensors.  Hence it does not rule
out a proof of (43) that essentially uses their decorated independence,
and it is not a complete source or a counterexample to Krenn's
conjecture.

The dependency-free checker
[verify_full_27_colon_cycle_guard.py](../computations/verify_full_27_colon_cycle_guard.py)
audits over exact rationals:

* all 27 rows for \(h=3,\ldots,8\), including the restored row;
* both rank-two direct blocks, all four kernels, and the normalized
  diagonal target coefficients;
* the two complete kernel contractions with coefficient \(1/(h-1)\);
* the nonzero colon class and the nontrivial weighted cycle;
* the selector-conic identity (20); and
* the full formal Macaulay rank \(2h\) for \(h=3,\ldots,10\).

The displayed tensoring argument proves the checked identities for every
\(h\ge3\); the finite loop is only an implementation audit.

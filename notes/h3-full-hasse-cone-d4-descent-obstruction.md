# The four-cube closes in the Hasse cone but does not descend to a physical \(d_4\)

Exact coupled construction and descent obstruction. This note builds the
smallest squarefree fourth-principal-parts target cone containing the
physical two-row Koszul cell, the strict \(pq/pr\) chart comparison, the
complete denominator presentation, and the split cap. In that prolonged
cone the target-active residual combines canonically with \(-T\) and
produces the desired \(Yw\) boundary with zero cap ordinary residue.

The construction does **not** descend to the old physical row complex. The
diagonal projection has exact chain-map defect
\((H_0-u)e_0\), and the selected fourth operator does not descend to a
nonzero source quotient because it sends the source equation \(H_m\) to
one. Thus the \(q\)-zero four-cube is a genuine formal Hasse-cone face, but
not an actual \(d_4\) of the old physical Rees cone. A physical fourth
Hasse--Schmidt/Spencer lift remains new source data.

This note does not construct that physical lift, an ordinary-residue
comparison on the physical quotient, or a proof of Krenn's conjecture.

## Outcome

Put

\[
 A=H_m,\qquad B=H_0-u,\qquad
 K_m^{\rm phys}=A r_0-B r_m,                            \tag{1}
\]

where \(m=01211222\). The row differential is

\[
 d r_0=B e_0,\qquad d r_m=Ae_0,
\qquad dK_m^{\rm phys}=0.                               \tag{2}
\]

Fix a deleted odd site \(v\) and an internal matching
\(N=\{z_1,z_2\}\in\operatorname {PM}(F_v)\). Let

\[
 z_3=a_{xv}^{0m_v},\qquad z_4=a_{pq}^{22},\qquad
 I=\{1,2,3,4\}.                                         \tag{3}
\]

The four selected edges form a perfect matching of all eight sites, so

\[
 \partial_I A=1,\qquad \partial_S B=0
 \quad(\varnothing\ne S\subseteq I).                    \tag{4}
\]

Let \(r_0[U],r_m[U],e_0[U]\) denote the squarefree Hasse generators indexed
by \(U\subseteq I\). The genuine prolonged differential is

\[
\begin{aligned}
 d\,r_0[U]&=B e_0[U],\\
 d\,r_m[U]&=\sum_{S\subseteq U}
              (\partial_SA)e_0[U\setminus S].
\end{aligned}                                           \tag{5}
\]

Every coefficient in (5) is derived from (2) by the Hasse product rule.
It is not an assigned fourth readout. Define

\[
 s_I=\sum_{S\subseteq I}
        (\partial_SA)r_0[I\setminus S]-B r_m[I].         \tag{6}
\]

Equations (5) give the exact cancellation

\[
 d s_I=
 B\sum_{S\subseteq I}(\partial_SA)e_0[I\setminus S]
 -B\sum_{S\subseteq I}(\partial_SA)e_0[I\setminus S]
 =0.                                                    \tag{7}
\]

The physical target of \(r_0\) is the constant one. Its positive Hasse
derivatives vanish, while \(r_m\) has target zero. By (4), only the
\(S=I\) term in (6) contributes, and hence

\[
                  \operatorname {tgt}(s_I)=1.           \tag{8}
\]

The split cap is derived as in commit e9962c0:

\[
 dT=-Yw,\qquad d\rho=w,\qquad
 \operatorname {tgt}(T)=1,\qquad
 \operatorname {ores}_{\rm cap}(T)=0.                  \tag{9}
\]

Therefore the coupled chain

\[
                         \boxed{n_I=s_I-T}              \tag{10}
\]

satisfies in the prolonged target cone

\[
 d n_I=Yw,\qquad
 \operatorname {tgt}(n_I)=0,\qquad
 \operatorname {ores}_{\rm cap}(n_I)=0.                \tag{11}
\]

Curvature multiplication gives

\[
 d(\kappa n_I)=\kappa Yw                                \tag{12}
\]

with the same two zero augmentations. This is the precise simultaneous
repair that was impossible in the bare
\(R\langle T,\rho\rangle\) span: the additional term is not a declared cap
generator, but the full Hasse prolongation of the physical Koszul cycle.

However, (11) is a statement in the prolonged cone. Let \(\pi_\Delta\)
forget every positive jet generator. Then

\[
 \pi_\Delta(s_I)=r_0,\qquad
 \pi_\Delta(n_I)=r_0-T.                                 \tag{13}
\]

The projection is not a chain map:

\[
\begin{aligned}
 d\,\pi_\Delta(n_I)&=B e_0+Yw,\\
 \pi_\Delta(d n_I)&=Yw,\\
 \boxed{[d,\pi_\Delta](n_I)&=(H_0-u)e_0\ne0.}           \tag{14}
\end{aligned}
\]

The term \(-B r_m[I]\), together with the proper Hasse faces in (6), is
exactly what cancels (14) in the prolonged complex. Those generators do
not exist in the old physical row complex.

There is also no valid shortcut obtained by imposing the source equations.
The selected fourth operator

\[
                  \Psi_I=\partial_{z_1}\partial_{z_2}
                          \partial_{z_3}\partial_{z_4}
\]

satisfies

\[
                         \Psi_I(H_m)=1.                 \tag{15}
\]

Hence \(\Psi_I\) does not preserve the source ideal. If
\(\bar R=R/(H_m,H_0-u,\ldots)\) is nonzero, the zero class of \(H_m\)
would be sent to the nonzero unit. Setting \(H_0-u=0\) after applying
\(\Psi_I\) therefore does not turn (13) into a well-defined physical
comparison. If \(\bar R=0\), the source stratum is already empty and no
\(d_4\) argument is needed.

The exact conclusion is:

\[
\boxed{
\begin{array}{l}
\text{formal fourth Hasse target-cone chain (10): constructed;}\\
\text{actual physical/Rees }d_4\text{ with zero target and residue:
not constructed;}\\
\text{descent obstruction: }(H_0-u)e_0
\text{ and }\Psi_I(H_m)=1.
\end{array}}                                             \tag{16}
\]

## 1. The smallest genuine prolonged cone

For the selected face and matching, let
\(\mathscr J_I(K)\) be the free squarefree Hasse prolongation of the
two-row complex (2), with generators and differential (5). Let
\(\mathscr R_v^{pq/pr}\) be the strict relative chart complex generated by

\[
 K_v=r_{c_v}^{pq}-r_{c_v}^{pr},\qquad dK_v=0,            \tag{17}
\]

where \(c_v\) is zero on \(x,v,p,q\) and agrees with \(12112\) on \(F_v\).
Let \(\mathscr D_v\) be the Hasse prolongation of the complete denominator
presentation

\[
 \delta(d_{s,a})
   =\sum_{c:c_s=a}
      \operatorname {Haf}(q_c|_{D\setminus\{s\}})e_c.   \tag{18}
\]

Finally let \(\mathscr G_v\) be the cap complex (9). The smallest genuine
ambient filtered cone is

\[
 \mathscr C_{v,N}^{(4)}
   =\mathscr J_I(K)\oplus
     \mathscr R_v^{pq/pr}\oplus
     \mathscr D_v\oplus
     \mathscr G_v,                                      \tag{19}
\]

with the Hasse, strict-relative, presentation, and cap differentials
displayed above. All four diagonal blocks square to zero. The target cone
identifies the constant target of \(s_I\) with \(T\), producing (10).

An off-diagonal comparison from (18) to the cap is a genuine mapping-cone
map only when its Hom differential vanishes. The polynomial face values
below specify the proposed comparison, but do not by themselves define it.
Thus (19) is the smallest honest ambient cone; an actual physical mapping
cone exists only after the diagonal/chart and denominator comparisons
descend.

The formal construction (10) lives entirely in the first and fourth
summands of (19), so it is unaffected by assigning a cap readout to a
hypothetical new generator. Its cap ordinary residue is zero because
\(\mathscr J_I(K)\) is an EqSystem jet summand and \(T\), unlike \(\rho\),
has zero ordinary-response augmentation. This is a derived direct-sum
statement inside (19), not yet an ordinary-residue map on the physical odd
quotient.

## 2. Strict chart and endpoint faces

The two external directions in (3) use the physical endpoint colours
\((0,m_v)\) and \((2,2)\). The zero-endpoint chart square instead uses

\[
 u_v=a_{xv}^{00},\qquad t=a_{pq}^{00}.                  \tag{20}
\]

For every internal matching \(N\),

\[
\begin{aligned}
 \partial_N\partial_{a_{xv}^{0m_v}}
             \partial_{a_{pq}^{22}}H_m&=1,\\
 \partial_N\partial_{u_v}\partial_tH_{c_v}&=1.          \tag{21}
\end{aligned}
\]

The endpoint bridge is not a word relabelling. It is the order-two
differential operator

\[
 E_v=M_{u_vt}
       \partial_{a_{xv}^{0m_v}}\partial_{a_{pq}^{22}},
 \qquad
 \partial_{u_v}\partial_tE_v\partial_NH_m=1.            \tag{22}
\]

The Hasse module in (19) is what makes the product-rule faces of (22)
literal generators. Applying only its top coefficient would again be a
non-\(R\)-linear operation.

In the direct-free row, the chart top in (21) lies in the \(pq\)-direct
sector. The \(pr\)-direct sector is zero, so the same coefficient lies in
the \(pr\)-two-star sector. The strict global chart boundary is
\(H_{c_v}-H_{c_v}=0\). Consequently the chart comparison transports the
top associated-Rees symbol but has no global EqSystem boundary capable of
cancelling (14).

## 3. The complete denominator faces

The exact top support remains the positive fact from ed60e2c:

\[
 \partial_NP_m\delta(d_{s,a})
  =\begin{cases}
    Y_0,&(s,a)=(v,m_v),\\
    0,&(s,a)\ne(v,m_v).
   \end{cases}                                          \tag{23}
\]

But a genuine Hasse cone must retain every proper face. For a fixed
two-edge matching \(N=\{z_1,z_2\}\), the numbers of nonzero selected
denominator columns are

\[
\begin{array}{c|c}
\text{internal derivative subset}&
\text{number of nonzero columns}\\ \hline
\varnothing&5\\
\{z_1\}&3\\
\{z_2\}&3\\
\{z_1,z_2\}&1.
\end{array}                                             \tag{24}
\]

Thus the top has no leakage, while both one-edge faces do. The full
fifteen-column prolongation in (18), not only \(d_{v,m_v}\), is required
for a square-zero denominator totalization. This is why top support alone
does not define an ordinary-residue comparison.

Even granting a sign-compatible denominator attachment which sends the
last line of (24) to \(-Yw\), its boundary lives in the cap row \(w\). The
physical descent defect (14) lives in the independent pure EqSystem row
\(e_0\). Neither denominator faces nor the strict chart cycle can cancel
it in the smallest cone.

## 4. Why the formal construction does not violate the bare-cap lock

Commit e9962c0 proved that a chain
\(aT+b\rho\) with boundary \(Yw\), zero target, and zero ordinary residue
does not exist. Equation (10) adds the source term \(s_I\):

\[
 \operatorname {tgt}(s_I-T)=1-1=0,\qquad
 d(s_I-T)=0-(-Yw)=Yw.                                   \tag{25}
\]

Thus the formal Hasse cone bypasses the bare-cap lock exactly as a
simultaneous higher construction should. It does not contradict that
lock, because \(s_I\notin R\langle T,\rho\rangle\).

After diagonal projection, however, \(s_I\) becomes \(r_0\) and acquires
the source boundary in (14). A target-zero physical correction in the old
two-row span would have the form \(b r_m\) and would require

\[
                         bH_m=H_0-u.                    \tag{26}
\]

No polynomial \(b\) exists. Specializing every mixed-colour edge variable
to zero kills \(H_m\) and retains the nonzero polynomial \(H_0-u\).
Strict chart differences have zero global boundary, and the denominator
and cap blocks occupy different boundary summands. Hence (26) is the exact
smallest-complex obstruction.

The cap ordinary residue of (10) is zero in the prolonged direct sum, but
an ordinary-residue comparison on the physical odd quotient would also
have to descend through (18). The support ladder (24) shows that retaining
only the \(q\)-zero top is not such a descent. The same-power
ordinary-residue lock is therefore not bypassed on the physical quotient.

## 5. Spectral-sequence interpretation and first missing type

The full chain \(s_I\) contains sixteen Hasse faces. Its associated top
coefficient is the tempting \(r_0\), and after target coning it becomes
\(r_0-T\). Calling that coefficient a physical \(d_4\) discards the
proper faces which make (7) hold.

Equivalently, if one inserts the proposed fourth component into the old
physical cone differential, then

\[
       (D_0D_4+D_4D_0)(K_m^{\rm phys})
                 =(H_0-u)e_0,                           \tag{27}
\]

even after the cap \(Yw\) face is paired. Hence \(D^2\ne0\), so there is
no filtered physical complex and no induced \(d_4\).

The smallest missing source type is not another cap symbol. It is the
fourth mixed-row Spencer generator \(r_m[I]\), together with all its
proper faces, with differential

\[
 d\,r_m[I]=\sum_{S\subseteq I}
             (\partial_S H_m)e_0[I\setminus S].         \tag{28}
\]

The terminal term \((\partial_IH_m)e_0=e_0\) lets
\(-B r_m[I]\) cancel the defect (14). A complete tower begins already with
the order-one proper faces, but its first component capable of supporting
the \(q\)-zero unit is the order-four generator (28).

Such a generator exists functorially in the formal principal-parts
complex. To use it physically, one must construct a fourth
Hasse--Schmidt lift of the actual full source which preserves every
EqSystem equation and makes the chart and denominator comparisons commute.
Equation (15) proves that the coordinate translation used here is
transverse, not such a source lift.

## 6. Exact verification and scope

The dependency-free checker
[verify_h3_full_hasse_cone_d4_descent_obstruction.py](../computations/verify_h3_full_hasse_cone_d4_descent_obstruction.py)
verifies for all five deleted faces and all three internal matchings:

- the literal 90-term direct-free rows and \(\partial_IH_m=1\);
- the full Hasse differential (5) and cycle cancellation (7);
- the derived formal chain (10)--(12);
- the diagonal defect (14);
- the non-\(R\)-linearity and source-ideal defect (15);
- both strict chart sectors and the endpoint bridge (21)--(22);
- every denominator support count in (24);
- separation of \(H_0-u\) from the target-zero two-row boundary ideal; and
- the curvature-scaled boundary \(\kappa Yw\).

Its frozen certificate digest is

    d3ec081e117cd2fd6cef08030b1abcd4deb19ddb41ca86848ef3ad7a2cd5f038

The verified positive statement is confined to the formal Hasse target
cone. The verified no-go is confined to diagonal descent into the old
physical two-row/chart/denominator/cap complex. A larger full-source
Hasse--Schmidt tower could supply (28); this calculation neither constructs
nor excludes it.

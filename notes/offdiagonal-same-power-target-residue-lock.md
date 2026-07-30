# A same-power target companion necessarily erases the odd response

## 1. Outcome

Let an off-diagonal physical pair cap be written in the canonical
unnormalized form

\[
 \mathcal P_{ij}=a_{ij}q+h x_i y_j,
 \qquad
 \mathcal P_{ij}q^{[h-1]}=h\delta_{ij}X_i,
 \qquad h\geq3.                                      \tag{1}
\]

Fix \(a\ne b\), put

\[
 \alpha=a_{ab}\ne0,
 \qquad \tau=\operatorname {tr}(a),
 \qquad K_*=\tau E_{ab}-\alpha I,
 \qquad R=\sum_{i,j}(K_*)_{ij}x_i y_j.                \tag{2}
\]

The canonical cap identity is exactly

\[
 \boxed{\tau\mathcal P_{ab}-\alpha\operatorname {tr}(\mathcal P)
                  =hR.}                                \tag{3}
\]

After division by the known nonzero scalar \(h\alpha\), (3) is the
legal literal row

\[
 \boxed{(\alpha^{-1}R)q^{[h-1]}=-\Delta_{2h,3}.}       \tag{4}
\]

Thus the lower symbol of the normalized scalar-zero *relation*
\(\alpha^{-1}K_*\) is indeed \(\alpha^{-1}R\).  However, (3) does not
by itself define a connecting morphism

\[
                         q\longmapsto\alpha^{-1}R.      \tag{5}
\]

There are two independent reasons.

1. As literally written, the two cap terms in (3) lift
   \(\alpha\tau q\).  After the legal division by \(\alpha\), the terms
   \((\tau/\alpha)\mathcal P_{ab}\) and
   \(\operatorname {tr}(\mathcal P)\) lift \(\tau q\), not \(q\).  If
   \(\tau\ne0\), the difference of the two normalized lifts of \(q\) has
   lower symbol \(R/(\alpha\tau)\).  If \(\tau=0\), both radial symbols
   vanish, so (3) compares two lifts of zero and supplies no lift transition
   on \(q\) at all.
2. In the literal source-row complex the normalized scalar-zero object is
   the pair

   \[
                     (\alpha^{-1}R,-\Delta_{2h,3}),      \tag{6}
   \]

   not the response \(\alpha^{-1}R\) with zero target.

More strongly, every same-complement attempt to cancel the target in (6)
necessarily cancels its odd residue as well.  Let \(W\) be the even cap
complement, expose one site \(x\), put \(D=W\setminus\{x\}\), and write

\[
 q=q_0+\sum_c e_c^{(x)}t_c,
 \qquad
 A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},
 \qquad
 C_{q_0}={\mathcal R_{2h-1}(D)\over\mathcal R_1(D)A}.   \tag{7}
\]

Also write \(X_c=e_c^{(x)}Y_c\) and
\(\overline Y_c=[Y_c]\in C_{q_0}\), and set

\[
 \rho_c(Q)=[t_cQB]\in C_{q_0}.                          \tag{8}
\]

The uniform lock proved below is:

> **Same-power target--residue lock.**  If a literal quadratic row on
> this same cap complement satisfies
> \[
>                      Qq^{[h-1]}=\sum_c\lambda_cX_c,    \tag{9}
> \]
> then, for the restriction \(\overline Q=Q|_{D}\),
> \[
>                 \boxed{\rho_c(\overline Q)
>                         =\lambda_c\overline Y_c}       \tag{10}
> \]
> for every label \(c\).

Consequently (4) has

\[
 \rho_c(\alpha^{-1}\overline R)=-\overline Y_c.        \tag{11}
\]

Any same-power companion with target \(+\Gamma\Delta_{2h,3}\) has
residue \(+\Gamma\overline Y_c\), and therefore erases the residue of
the curvature-weighted row
\(\Gamma(\alpha^{-1}R,-\Delta_{2h,3})\) exactly.  This applies to the
entire scalar-parameter span of literal quadratic rows on the same
complement, not just to the nine canonical caps.

Hence the missing construction cannot be a target-cancelling quadratic
\(\Theta\) against the same \(q^{[h-1]}\), followed by the ordinary odd
residue.  It must be a secondary chain comparison retaining adjacent
divided-power layers (or genuinely different odd quotients) before target
cancellation.  Flat transport between charts using the same odd quotient
does not evade the lock.  No such secondary comparison is constructed
here, and Krenn's conjecture remains open.

## 2. Canonical normalization and legal source rows

Before canonical normalization, the original pair coefficient equations
are

\[
 a_{ij}q^{[h]}+x_i y_jq^{[h-1]}=\delta_{ij}X_i.          \tag{12}
\]

Since

\[
                         q q^{[h-1]}=h q^{[h]},          \tag{13}
\]

multiplication of (12) by \(h\) gives (1).  Thus each
\((\mathcal P_{ij},h\delta_{ij}X_i)\) is a literal source row.  Scalar
linear combinations of these rows are legal; on the selected open chart,
division by the scalar \(\alpha\ne0\) is legal as well.  No site form,
quadratic, or matching power is divided out.

The radial coefficient of the left side of (3) is

\[
                         \tau\alpha-\alpha\tau=0,        \tag{14}
\]

and its lower piece is

\[
 h\left(\tau x_a y_b-\alpha\sum_i x_i y_i\right)=hR.   \tag{15}
\]

The target of the off-diagonal row is zero, while the trace row has target
\(h\Delta_{2h,3}\).  Therefore the target of (3) is
\(-h\alpha\Delta_{2h,3}\), proving (4), including its sign and all
factors of \(h\) and \(\alpha\).

There is a useful formal filtration statement which is valid but weaker
than (5).  Let

\[
 s(C)=\sum_{i,j}C_{ij}a_{ij},qquad
 r(C)=\sum_{i,j}C_{ij}x_i y_j.                           \tag{16}
\]

The cap attached to \(C\) is

\[
                         \mathcal P(C)=s(C)q+h r(C).     \tag{17}
\]

Since \(s(\alpha^{-1}K_*)=0\), passage from the radial symbol of (17) to
its lower symbol gives

\[
                   \operatorname {low}(\alpha^{-1}K_*)
                         =\alpha^{-1}R.                  \tag{18}
\]

Equation (18) is the exact cap-filtration value computed by (3).  Its
domain is the scalar relation \(\alpha^{-1}K_*\in\ker s\), not the radial
generator \(q\).

Indeed, at a complex point with \(\tau\ne0\), the two actual cap lifts of
\(q\) are

\[
                    \alpha^{-1}\mathcal P_{ab},
              \qquad \tau^{-1}\operatorname {tr}(\mathcal P),
\]

and their difference is

\[
 {1\over\alpha}\mathcal P_{ab}
   -{1\over\tau}\operatorname {tr}(\mathcal P)
       ={h\over\alpha\tau}R.                             \tag{19}
\]

The kernel coordinate in (17) is \(h r(C)\).  Identifying that kernel with
the response space by \(h r\mapsto r\), the transition value in (19) is
\(R/(\alpha\tau)\).  When \(\tau=0\), the trace cap has zero radial symbol
and (19) is unavailable.  This is why (18) cannot be renamed (5) without
an additional chain-level identification.  Over a parameter ring the same
statement holds on the localization where \(\tau\) is a unit; a merely
nonzero but nonunit \(\tau\) does not give a global normalized lift.

## 3. Proof of the same-power target--residue lock

Let \(D=W\setminus\{x\}\), and decompose an arbitrary quadratic as

\[
 Q=\overline Q+\sum_c e_c^{(x)}\ell_c.                  \tag{20}
\]

All products of two terms supported at \(x\) vanish in the site-square-zero
algebra.  Hence the divided-power binomial identity has coefficient one:

\[
 q^{[h-1]}
   =q_0^{[h-1]}
      +\left(\sum_c e_c^{(x)}t_c\right)q_0^{[h-2]}
   =A+\sum_c e_c^{(x)}t_cB.                              \tag{21}
\]

There is no ordinary binomial factor \(h-1\) in (21).  Taking the
coefficient of \(e_c^{(x)}\) in (9) gives the literal equation

\[
                         \ell_cA+\overline Q\,t_cB
                              =\lambda_cY_c.             \tag{22}
\]

The first term belongs to the quotient denominator
\(\mathcal R_1(D)A\).  Reducing (22) proves (10).  The only related
factorial identity is

\[
                         q_0B=(h-1)A,                    \tag{23}
\]

which shows separately that \(\rho_c(q_0)=0\); it does not alter (21) or
(22).

The proof is stable under scalar extension to any commutative
\(\mathbb C\)-algebra \(S\), with the quotient in (7) formed over \(S\).
Thus \(q,Q\), the coefficients \(\lambda_c\), and \(\Gamma\) may be
polynomial or localized-regular families in clean-line or auxiliary-chart
parameters.  If \(\alpha\) is itself a parameter, (4) is asserted only
over \(S[\alpha^{-1}]\); no \(\lambda_c\) or \(\Gamma\) is inverted.  The
argument also works with an arbitrary right side: if its \(x,c\)
coefficient is \(Z_c\), then

\[
                         \rho_c(\overline Q)=[Z_c].       \tag{24}
\]

Target decomposability specializes (24) to (10).

Apply (10) to the normalized scalar-zero row (4), for which
\(\lambda_c=-1\).  This proves (11).  If

\[
                         \Theta q^{[h-1]}
                              =+\Gamma\Delta_{2h,3},      \tag{25}
\]

then (10) gives

\[
                         \rho_c(\overline\Theta)
                              =+\Gamma\overline Y_c.      \tag{26}
\]

On the other hand, multiplying (11) by \(\Gamma\) gives
\(-\Gamma\overline Y_c\).  Their sum is zero before any torus--Koszul
prolongation.  Thus changing the choice of same-power target companion,
adding targetless same-power rows, or taking another scalar linear
combination cannot retain the desired odd class.

## 4. Exact scope across overlaps

The lock concerns three simultaneous features:

1. the same even cap complement and the same internal quadratic \(q\);
2. multiplication by the same divided power \(q^{[h-1]}\); and
3. application of the ordinary odd quotient (7)--(8) after exposing one
   site.

It is therefore stronger than a one-chart statement but not an
all-complex impossibility.

If two charts restrict to the same odd quadratic \(q_0\) and their
power-free connection gives an explicit linear identification of their
ordinary residue quotients carrying one \(\overline Y_c\) to the other,
then each chart satisfies (10).  A cross-chart scalar combination whose
physical targets cancel consequently has zero residue after that specified
transport.  The conclusion does not apply merely from target cancellation
when the odd quotients have not been identified.  In the identified case,
taking a difference of two scalar-zero rows or two target companions does
not evade the lock.

Likewise, multiplication by scalar polynomials in clean-line parameters
does not evade it: the proof is coefficientwise over the parameter ring.
Multiplication by a site-algebra factor is covered only after specifying
the corresponding higher-degree quotient; it is not part of the
quadratic lock (9) as stated.

What can evade the lemma is precisely what it omits: a literal row which
mixes adjacent matching powers before passing to the quotient.  The
complete three-site rows have the schematic form

\[
 L_{ijk}q_0^{[h-1]}+x_i y_jt_kq_0^{[h-2]}
                   =\mathbf1_{i=j=k}Y_i,                \tag{27}
\]

and the power-free cap connection relates their two filtration pieces.
These rows naturally belong to the two-term adjacent-power complex defined
by

\[
 d_c:\mathcal R_1(D)\oplus\mathcal R_2(D)\longrightarrow
             \mathcal R_{2h-1}(D),
 \qquad
 d_c(\ell,Q)=\ell A+Qt_cB.                              \tag{28}
\]

A viable transgression must therefore be a **secondary** map on a chain
complex extending this two-term map (or on a cross-chart cone with genuinely
different odd quotients).  It must do all of the following:

* take the normalized scalar relation \(\alpha^{-1}K_*\), whose lower
  symbol is (18), to the class of \(\alpha^{-1}R\) modulo
  \(\ker\rho_c\);
* null-homotope the diagonal target in a different chain degree, instead
  of adding a quadratic row of the form (25); and
* intertwine the literal connection/curvature rows with the target
  torus--Koszul differential.

Equivalently, the missing datum is a homotopy-corrected comparison of the
two summands in (28), not a map induced after quotienting (28) by
\(\mathcal R_1A\).  The cap syzygy (3) fixes the only possible response
normalization for such a comparison, but it neither constructs the
comparison nor proves its chain property.

## 5. The overlap ledger has Bockstein shape, but no Bockstein is constructed

The adjacent-power escape in Section 4 has an exact first-jet model.  This
explains the Gauss--Manin/Bockstein analogy, but an adjacent-power identity
alone is not a Bockstein connecting morphism.

Let \(\epsilon^2=0\) be a central scalar parameter, let \(\nu\) have the
same quadratic degree as \(q\), and take a first-order deformation

\[
 q_\epsilon=q+\epsilon\nu,\qquad
 Q_\epsilon=Q+\epsilon\dot Q,\qquad
 \lambda_\epsilon=\lambda+\epsilon\dot\lambda.          \tag{29}
\]

The divided-power derivative has coefficient one:

\[
 q_\epsilon^{[h-1]}
   =q^{[h-1]}+\epsilon\nu q^{[h-2]}.                     \tag{30}
\]

Consequently the first jet of a target-bearing identity

\[
 Q_\epsilon q_\epsilon^{[h-1]}
       =\lambda_\epsilon\Delta
\]

is the exact mixed-power row

\[
 \boxed{\dot Qq^{[h-1]}+Q\nu q^{[h-2]}
                         =\dot\lambda\Delta.}            \tag{31}
\]

When the target is fixed, (31) is an exact targetless mixed-power relation.
It lies outside the same-power lock because its two summands live at
adjacent divided powers.  Differentiating a representative
\(\ell q^{[h-1]}\) of the moving denominator contributes
\(\ell\nu q^{[h-2]}\), which need not lie in the old denominator.  This is
the candidate first-variation term.  Calling its class a Gauss--Manin
derivative or Bockstein requires a specified family of complexes (or a
short exact sequence), a cycle and lift, and a proof that the resulting
class is independent of representatives.  None of those chain data are
constructed here.

The literal overlap rows do supply an exact ledger of this adjacent-power
shape, including a cancellation one layer lower.  Use the notation of the
power-free pair-cap connection, writing
\(\mathsf A,\mathsf B,\mathsf F,\mathsf U\) for the selected direct
scalar entries (to distinguish them from the divided powers \(A,B\) in
(7)):

\[
 P_{pq}t-P_{pr}y=\delta z,\qquad
 \delta=\mathsf A t-\mathsf B y.                        \tag{32}
\]

Expose a fourth site with star \(v\).  Put

\[
 \kappa=\mathsf A\mathsf U-\mathsf B\mathsf F,\qquad
 Z_0=z^{[h-1]},\quad Z_1=z^{[h-2]},\quad Z_2=z^{[h-3]}. \tag{33}
\]

The literal normal, curvature, and direct-double rows give, with the
orientations in (32),

\[
\begin{aligned}
 L_{pq;r}-L_{pr;q}&=-(h-1)\delta,\\
 M_{pq;rs}-M_{pr;qs}&=-(h-1)\kappa,\\
 \mathsf U P_{pq}+tL_{pq;s}-\mathsf F P_{pr}-yL_{pr;s}
     &=\delta v+\kappa z.                                \tag{34}
\end{aligned}
\]

Taking the \(pq\)-presentation minus the \(pr\)-presentation and using
(32)--(34), without cancelling a power, gives

\[
\begin{aligned}
0={}&-(h-1)\kappa Z_0
 +\bigl(-(h-1)\delta v+\delta v+\kappa z\bigr)Z_1
 +\delta zvZ_2\\
={}&
 \boxed{\kappa\bigl(zZ_1-(h-1)Z_0\bigr)
       +\delta v\bigl(zZ_2-(h-2)Z_1\bigr).}             \tag{35}
\end{aligned}
\]

Both brackets vanish by divided-power multiplication, but they vanish in
different adjacent layers:

\[
                         zZ_1=(h-1)Z_0,\qquad
                         zZ_2=(h-2)Z_1.                  \tag{36}
\]

Formula (35) is an exact adjacent-power overlap syzygy.  The first bracket
is the curvature/direct-double pair; the second is its connection/normal
cancellation.  The coefficient of the selected curvature is
\(+\kappa\), the direct-double coefficient is \(-(h-1)\kappa\), and there
is no extra factorial.  More explicitly, the four contributions are
\(-(h-1)\kappa Z_0\) from the direct-double row,
\(-(h-1)\delta vZ_1\) from the normal difference,
\(+\delta vZ_1+\kappa zZ_1\) from curvature, and
\(+\delta zvZ_2\) from the power-free connection.  Reversing the oriented
presentation difference
reverses \(\delta\), \(\kappa\), and the whole displayed ledger.  These facts
make (35) a possible source representative for a future Bockstein
construction, but no source complex or connecting map has yet made it a
Bockstein class.

The rows also do **not** compute the required odd response.  If (35) is first
collapsed using (36), its ordinary residue is zero.  To obtain the
nonzero class, a future construction would have to pair the first bracket
with the cap-filtration relation (18) before making that collapse.  If the
relevant extension classes and chain maps exist, the hoped-for homological
interpretation would be a Yoneda-type product of

\[
 \{\text{curvature/direct-double adjacent-power class}\}
 \quad\text{and}\quad
 \{\text{scalar-zero cap-filtration class}\}.            \tag{37}
\]

Set \(\widehat\zeta_c:=-\overline Y_c\).  For the selected orientation,
any such pairing that extends the lower-symbol residue is forced to have
the normalization

\[
 \boxed{
 \mathfrak B_c\bigl(\kappa,\alpha^{-1}K_*\bigr)
   =\kappa\,\rho_c(\alpha^{-1}R)
   =-\kappa\,\overline Y_c
   =\kappa\,\widehat\zeta_c.}                            \tag{38}
\]

Here \(\mathfrak B_c\) is notation for the required, presently undefined
operation.  It would have to be defined on a literal adjacent-power chain
complex, send the \(\delta v\)-bracket in (35) to a chain boundary, and be
independent of changing cap or overlap representatives by literal
boundaries.  A tilted curvature form would replace \(\kappa\) in (38)
coefficientwise.  Only after those properties are proved would the later
certificate-bracket construction supply the outer minus needed for the
final correction.

Equation (38) is therefore a forced, conditional value, not a constructed
Yoneda value.  The cap syzygy fixes the only possible normalization and
(35) supplies the adjacent-power sign ledger, but no existing identity
defines the two extension classes, their Yoneda product, or a
source-faithful representative of it.
In particular, the direct-double row alone does not overcome the
\(\tau=0\) lift issue in Section 2, and the same-power companion ruled out
by Section 3 is not a substitute for \(\mathfrak B_c\).

The dependency-free checker
[`verify_offdiagonal_same_power_target_residue_lock.py`](../computations/verify_offdiagonal_same_power_target_residue_lock.py)
audits the divided-power coefficient in (21), the factor in (23), the cap
syzygy and target signs, both the \(\tau=0\) and \(\tau\ne0\) lift
normalizations, the same-power cancellation ledger, and the two exact
adjacent-power brackets in (35).  The proof above, not its finite sparse
examples, is uniform in \(h\).

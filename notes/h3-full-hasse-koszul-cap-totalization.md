# Independent generating-function audit of the full Hasse lower faces

This independently complements the
[indexed Hasse-cone construction](h3-full-hasse-cone-d4-descent-obstruction.md).
It reconstructs that cycle by square-zero generating functions, then checks
every lower face against both strict charts and all fifteen odd denominator
columns.  In particular, it verifies the exact proper-face maps, not only
their support counts.  It agrees with the indexed calculation's diagonal
physical-descent obstruction.  It does not identify the totalization with
the underived physical source or prove Krenn's conjecture.

## 1. Outcome

Let \(R\) be the universal direct-free labelled-edge ring and let

\[
 d r_0=H_0-u,\qquad d r_m=H_m,\qquad
 dT=-Yw,\qquad d\rho=w.                               \tag{1}
\]

The target and ordinary-residue maps on this combined presentation are

\[
 \begin{array}{c|rrrr}
       &r_0&r_m&T&\rho\\ \hline
 \operatorname {tgt}&1&0&1&0\\
 \operatorname {ores}&0&0&0&1.
 \end{array}                                            \tag{2}
\]

Fix a deleted odd site \(v\) and a perfect matching
\(N=\{e,f\}\) of \(F_v=D\setminus\{v\}\).  The four marked mixed-edge
directions are

\[
 a_{xv}^{0m_v},\qquad a_{pq}^{22},\qquad e,\qquad f.   \tag{3}
\]

Over the square-zero Hasse algebra

\[
 B=R[\epsilon_u,\epsilon_t,\epsilon_e,\epsilon_f]
       /(\epsilon_u^2,\epsilon_t^2,
         \epsilon_e^2,\epsilon_f^2),                   \tag{4}
\]

let \(\tau\) replace each marked variable \(z_i\) by
\(z_i+\epsilon_i\).  Base-change the **differential as well as the
coefficients** along \(\tau\).  Then

\[
 \boxed{
 \mathcal N(\epsilon)
   =\tau(H_m)(r_0-T)-\tau(H_0-u)r_m }                  \tag{5}
\]

is the generating form of the translated presentation chain, and direct
calculation gives

\[
 \boxed{
 d\mathcal N(\epsilon)=\tau(H_m)Yw,\qquad
 \operatorname {tgt}\mathcal N(\epsilon)=
 \operatorname {ores}\mathcal N(\epsilon)=0. }         \tag{6}
\]

The coefficientwise Hasse/Spencer meaning is essential.  For
\(U\subseteq I=\{u,t,e,f\}\), let \(r_0[U],r_m[U],e_{\rm Eq}[U]\)
be the Boolean-face row copies with

\[
\begin{aligned}
 d r_0[U]&=(H_0-u)e_{\rm Eq}[U],\\
 d r_m[U]&=\sum_{S\subseteq U}
     (\partial_S H_m)e_{\rm Eq}[U\setminus S].
\end{aligned}                                          \tag{6a}
\]

Expanding (5) at total order \(I\) gives the honest prolonged cycle

\[
 s_I=\sum_{S\subseteq I}
       (\partial_S H_m)r_0[I\setminus S]
       -(H_0-u)r_m[I],\qquad ds_I=0.                   \tag{6b}
\]

Since the target is constant on \(r_0\), only \(r_0[0]\) has target one.
The unit \(\partial_IH_m=1\) therefore gives
\(\operatorname {tgt}(s_I)=1\), and

\[
 n_I=s_I-T,\qquad
 (d,\operatorname {tgt},\operatorname {ores})(n_I)
       =(Yw,0,0).                                      \tag{6c}
\]

In generating notation, the top fourfold coefficient is

\[
 [\epsilon_u\epsilon_t\epsilon_e\epsilon_f]\mathcal N=r_0-T,
 \qquad
 [\epsilon_u\epsilon_t\epsilon_e\epsilon_f]d\mathcal N=Yw. \tag{7}
\]

Thus the formal \(s-T\) found by coefficientwise Reynolds selection is the
top of one explicit total chain; its missing Leibniz terms are precisely the
other fifteen Hasse coefficients of (5).

The response is also derived on the whole totalization.  Put

\[
 \mathcal Z(\epsilon)=\kappa\bigl(
       \mathcal N(\epsilon)-\tau(H_m)Y\rho\bigr).       \tag{8}
\]

Then

\[
 d\mathcal Z=0,\qquad \operatorname {tgt}\mathcal Z=0,\qquad
 \operatorname {ores}\mathcal Z=-\kappa\tau(H_m)Y,     \tag{9}
\]

and its top coefficient is

\[
 \kappa(r_0-T-Y\rho),\qquad
 \operatorname {ores}=-\kappa Y.                       \tag{10}
\]

Equations (5)--(10) no longer assume a top column
\((\kappa Y,0,0)\).  They construct its entire derived-presentation Hasse
lift and derive its response.

There is nevertheless a sharp remaining obstruction.  The mixed equation
\(H_m=0\) is a target-zero equation on the underived physical source, but

\[
 [\epsilon_u\epsilon_t\epsilon_e\epsilon_f]\tau(H_m)=1. \tag{11}
\]

Therefore \(\tau\) does **not** factor through the underived physical source
ring: if it did, \(\tau(H_m)\) would vanish, contradicting (11).  The
construction is the fourth transgression in the derived
presentation/Hasse filtration.  Promoting it to an actual physical \(d_4\)
in the source spectral
sequence still requires a derived comparison (or corrected source-valid
Hasse--Schmidt lift), not merely the four independent ambient shifts.

Equivalently, let \(\pi_{\rm top}\) discard every proper Hasse face.  With
the original, untranslated differential,

\[
 d\,\pi_{\rm top}n_I=(H_0-u)e_{\rm Eq}+Yw,\qquad
 \pi_{\rm top}d_{\rm tot}n_I=Yw,
\]
\[
 \boxed{[d,\pi_{\rm top}]n_I=(H_0-u)e_{\rm Eq}.}       \tag{11a}
\]

Thus the top symbol does not descend diagonally even though the full
totalization is a chain.  This is the chain-level form of (11).

## 2. Why translating the differential is essential

The physical two-row Koszul cell is

\[
 K_m=H_mr_0-(H_0-u)r_m.                                \tag{12}
\]

If one translates only the displayed coefficients while keeping the old
row differential, its boundary contains

\[
             (\tau(H_m)-H_m)(H_0-u),                   \tag{13}
\]

which is generally nonzero.  The Hasse totalization instead uses

\[
 d_\tau r_0=\tau(H_0-u),\qquad d_\tau r_m=\tau(H_m).   \tag{14}
\]

The marked variables in (3) all have mixed colours, so they are disjoint
from \(H_0\) and \(\tau(H_0-u)=H_0-u\).  Nevertheless (14), rather than an
untranslated differential, is the functorial reason the two Eq terms cancel:

\[
 \begin{split}
 d_\tau \mathcal N
   &=\tau(H_m)\tau(H_0-u)
     -\tau(H_0-u)\tau(H_m)
     +\tau(H_m)Yw\\
   &=\tau(H_m)Yw.
 \end{split}                                            \tag{15}
\]

This equality packages every second-order Leibniz commutator found in the
top-symbol audit.  Truncating (5) to (7) before taking its differential loses
the cancellations in (15).

## 3. All lower Hasse coefficients

For every subset \(S\) of the four marked directions, multi-affinity gives

\[
 [\epsilon_S]\tau(H_m)=\partial_S H_m.                 \tag{16}
\]

The checker verifies (16) for all \(16\) subsets in each of the fifteen
choices \((v,N)\).  In particular, the lower coefficients of (5) are not
optional \(A_\infty\) guesses: they are the unique Hasse product-rule terms
of the translated Koszul identity.

The top unit follows because the four marked edges form a perfect matching
of all eight sites.  The corresponding monomial occurs once in \(H_m\), and
the direct-free forbidden edge \(pr\) is absent:

\[
 \partial_e\partial_f
 \partial_{a_{xv}^{0m_v}}\partial_{a_{pq}^{22}}H_m=1.  \tag{17}
\]

All three matching choices on \(F_v\) have the same top (7).  Their lower
coefficients differ, but those differences lie on proper Hasse faces.  Thus
the normalized Reynolds average preserves (7) only after the full faces in
(5) have been retained.

## 4. The fifteen denominator columns

The complete odd denominator presentation has columns \(d_{s,a}\), with

\[
 P_m\delta(d_{s,a})=
 \begin{cases}
 h_sY_0,&a=m_s,\\
 0,&a\ne m_s,
 \end{cases}
 \qquad
 h_s=\operatorname {Haf}(q_m|_{F_s}).                  \tag{18}
\]

Fix the internal directions \(e,f\) from (3).  For every site \(s\), take
the external \((a_{xs}^{0m_s},a_{pq}^{22})\)-face of the same universal
chain (5), while retaining the full internal Hasse square.  Denote it by

\[
 \Phi_s(\epsilon_e,\epsilon_f)
   =[\epsilon_{u_s}\epsilon_t]\mathcal N_s.            \tag{19}
\]

Coefficient extraction from (6) gives the exact totalized face equation

\[
 d_{\rm tot}\Phi_s
    =\tau_{e,f}(h_s)Yw,\qquad
 \operatorname {tgt}\Phi_s=
 \operatorname {ores}\Phi_s=0.                        \tag{20}
\]

Here \(d_{\rm tot}\) includes the lower external faces inherited from (5).
Equation (20) must not be misread as the ordinary differential of the
isolated coefficient \(h_s(r_0-T)\); that isolated coefficient has an extra
Eq boundary.  The totalization is what cancels it.

The proper-face support is not Kronecker.  Among the five selected-colour
columns \((s,m_s)\), the exact support counts are

\[
 \begin{array}{c|cccc}
 \text{internal Hasse coefficient}
      &1&\epsilon_e&\epsilon_f&\epsilon_e\epsilon_f\\ \hline
 \#\text{ nonzero selected columns}&5&3&3&1.
 \end{array}                                            \tag{21}
\]

The ten columns with \(a\ne m_s\) vanish on every face.  At the top,

\[
 [\epsilon_e\epsilon_f]\tau_{e,f}(h_s)=\delta_{sv},   \tag{22}
\]

so (21) ends in the familiar no-leakage statement.  Equations (19)--(21)
are the stronger result: all proper-face leakage is present and is matched
by \(\mathcal N\).  A top-only Reynolds truncation does not descend, whereas the full
Boolean Hasse presentation does.

## 5. Strict \(pq/pr\) chart descent

Partition every term of \(H_m\) by the chart sector.  Every coefficient in
(19) contains the marked \(pq\) edge, hence lies in the \(pq\)-direct
sector.  The same perfect matching cannot contain \(pr\); in the direct-free
presentation it lies in the \(pr\)-two-star sector.  This remains true for
all four internal coefficients in (19).

Let \(\mathcal N^{pq}\) and \(\mathcal N^{pr}\) be (5) in the two row
presentations, using the
same cap generator \(T\).  Their difference is

\[
 \begin{split}
 \mathcal N^{pq}-\mathcal N^{pr}
  ={}&\tau(H_m)(r_0^{pq}-r_0^{pr})\\
    &-\tau(H_0-u)(r_m^{pq}-r_m^{pr}).                  \tag{23}
 \end{split}
\]

The \(T\)-terms cancel.  Because the two chart rows have identical global
polynomial boundaries, (23) is closed, target-zero, and ordinary-residue
zero coefficient by coefficient.  Thus neither strict chart gluing nor the
fifteen denominator columns obstruct the **derived-presentation**
totalization.

## 6. What has and has not become an actual \(d_4\)

Filter the translated presentation by Hasse order.  Equations (16) and (15)
give the complete four-stage lift, and (7) is its order-four transgression.
In that prolonged filtered cone the algebraic fourth transgression is

\[
                         d_4[r_0-T]=[Yw],               \tag{24}
\]

with the response refinement (10).  The result is independent of the three
matching choices at the top, and its full lower faces satisfy the denominator
and chart equations.

This does not yet prove that (24) is the \(d_4\) of the physical source
spectral sequence.  Equation (11) proves that the naive underived
identification is impossible, and (11a) gives its exact comparison
commutator.  One still needs one of the following:

1. a comparison from this derived Eq/Koszul Hasse totalization to the actual
   filtered source resolution, preserving target and ordinary residue; or
2. source-valid Hasse--Schmidt correction terms which make the translated
   full EqSystem vanish while retaining the top class (7).

The first option is now sharply constrained but no longer obstructed by the
Leibniz commutators, the \(pq/pr\) sector transfer, or any of the fifteen
denominator columns.  The second cannot use only the four independent shifts
in (3), by (11).

## 7. Exact verification

Run

```sh
.venv/bin/python computations/verify_h3_full_hasse_koszul_cap_totalization.py
```

The dependency-free checker works over exact sparse rational polynomials and
the square-zero Hasse algebra.  It checks all \(15\times16\) Hasse
coefficients, the translated module differential, target and residue maps,
the response cycle, every strict chart sector, every Boolean face of all
fifteen denominator columns, the \(5,3,3,1\) support census, the cubical
signs, the unit obstruction (11), and the diagonal commutator (11a).  Its
terminal line is

```text
PASS: prolonged-cone fourth transgression; physical d4 needs a derived lift
```

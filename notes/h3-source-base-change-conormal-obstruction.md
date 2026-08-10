# Source base change creates the tempting lift but not the missing source row

## Outcome

In the actual selected full-nine row module, retain the normalized pure
source row, cap, ordinary response, and physical normal-incidence chain

\[
 dr_0=F_0e_{\rm Eq},\quad F_0=H_0-u,
 \qquad dT=-Yw,\qquad d\rho=w,
 \qquad (d,{\rm tgt},{\rm ores})(\mathcal M)=(\kappa w,0,\kappa).
                                                               \tag{1}
\]

The last type is the exact mixed bar--curvature output of `55f10f2`, with
the selected polar normalized to one.  Combining every correction term gives
the genuinely source-labelled candidate

\[
 \boxed{
 \mathcal N=Y\mathcal M-\kappa Y\rho-\kappa T+\kappa r_0.}       \tag{2}
\]

There is no sign ambiguity left in (2): direct substitution in (1) gives

\[
 \boxed{
 (d,{\rm tgt},{\rm ores})(\mathcal N)
   =(\kappa F_0e_{\rm Eq}+\kappa Yw,0,0).}                      \tag{3}
\]

Thus the proposed chain is almost the missing adjacent-chart row, but its
first uncancelled literal face is exactly `kappa*F0*Eq`.

If one first base-changes by the source ideal (J), then (F_0=0), and
(3) becomes the desired invisible boundary.  This operation is algebraically
valid as a computation in the derived fibre, but it is not a new source
identity.  Its connecting class is

\[
       \boxed{\delta[\mathcal N]=\kappa[F_0]\in J/J^2,}          \tag{4}
\]

and this class is nonzero.  Consequently neither
`kappa*(r0-T)` nor (2) lifts to the underived polynomial source module.
Using (F_0=0) to erase (4) before proving the missing row is precisely the
circular step: it kills the generator whose conormal class measures the
failure to lift.

## Literal full-nine conormal theorem

Work over the coefficient ring in the selected direct-chart scalars
`A,B,F,U,Y`, localized at

\[
                         \kappa=AU-BF\ne0,\qquad Y\ne0.
\]

Filter the full source ring by the selected internal edge variables and the
homogenizing target variable (u).  Let

\[
 \ell(P)=[u]P\big|_{\text{all internal edges}=u=0}.              \tag{5}
\]

The exact `3^8` literal-word census gives

\[
 \ell(F_w)=-\mathbf1_{w=0^8}.                                  \tag{6}
\]

Indeed every hafnian monomial contains four literal edges, while the only
selected-(u) term is the target subtraction in the pure `0^8` row.  In
particular, (ell) vanishes on (J^2), so it descends to the conormal
module (J/J^2), and

\[
                         \ell(\kappa[F_0])=-\kappa\ne0.          \tag{7}
\]

All 6,558 mixed full-nine words have zero value under (5).  This includes:

- the twenty literal three-set rows used in
  `cd52b2b` and `9dac232`;
- every response companion (M_S) and landing defect occurring in the
  companion-corrected class
  (K=\sum_S(M_S+\alpha D_S));
- the complete mixed word `1211222` in the bar--curvature chain;
- every target-zero normal-incidence or adjacent-chart reinsertion.

Thus no such literal row can cancel (7).  More generally, any target-zero
correction (C) whose cap boundary equals its ordinary-residue readout has
the graph form

\[
        (d_w,{\rm tgt},{\rm ores})(C)=(c,0,c).
\]

Adding (-c\rho) removes both of its cap coordinates.  The desired
remaining (w)-boundary then forces the cap coefficient to be
(-\kappa T); target cancellation forces (+\kappa r_0).  Hence every
literal correction of this type has the same unavoidable conormal face
(kappa[F_0]).  This is the promised no-go for reinserting the committed
normal/bar and target-zero adjacent-chart rows.

## The minimal missing source packet

The genuine source-level problem is therefore smaller than another Hasse,
Spencer, or support layer.  A positive identity must supply one new
source-labelled chain (C_{\rm rel}) satisfying

\[
 \ell(dC_{\rm rel})=+\kappa,qquad
 ({\rm tgt},{\rm ores})(C_{\rm rel})=(0,0),                    \tag{8}
\]

so that its Eq boundary cancels `kappa*F0` **before** quotienting by (J).
At the middle-word level this is exactly the missing companion-corrected
row

\[
                  K=\sum_{|S|=3}(M_S+\alpha D_S)=0,             \tag{9}
\]

not the separately internal statement (sum_SD_S=0).  Existing literal
full-nine rows have zero selected-(u) conormal value, so none supplies
(8).  Equation (8), with its literal endpoint fine grade and target
normalization, is the precise minimal packet still absent.

This does not prove that no larger future source resolution can contain
such a chain.  It proves that the tempting base-change argument and every
reinsertion from the committed literal target-zero families do not contain
it: the obstruction is the nonzero conormal class (4).

## Verification

Run

    python3 computations/verify_h3_source_base_change_conormal_obstruction.py
    python3 -O computations/verify_h3_source_base_change_conormal_obstruction.py

The checker pins the seven load-bearing artifacts, enumerates all 6,561
eight-site words and their 105 perfect matchings, checks the twenty
source-labelled three-set words and the complete bar word, reconstructs
(2)--(3) over the exact coefficient ring, verifies the underived cokernel
functional, and evaluates the conormal class at three active rational
packets including the direct-free case.

The frozen ledger digest is

    9b6178c94784f4493b25b9bdbcfa6bae90b179355bd77ffa8f20f93502c69efc

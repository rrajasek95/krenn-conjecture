# Full-star action on the explicit cap totalization: the Eq square is the descent commutator

## Result

For the canonical physical cap cube

\[
 M=01{:}01\,23{:}21\,45{:}12\,67{:}22,
 \qquad w=01211222,
\]

the literal full Hasse totalization

\[
 N=\tau(H_m)(r_0-T)-\tau(H_0-u)r_m
\]

does carry the corrected site-zero full-star action.  If

\[
 E_0=\sum_{i=1}^7x_{0i}\partial_{0i},
 \qquad
 \widehat E_0=E_0+u\partial_u+epsilon_{01}\partial_{\epsilon_{01}},
\]

then the checker proves coefficientwise

\[
 \widehat E_0N=N,
 \qquad dN=\tau(H_m)Yw,
 \qquad \operatorname{target}(N)=\operatorname{ores}(N)=0.
\]

This is source-provenant on the translated cube: the diagonal trigger identity
is \(I_{0i}D_{0i}=x_{0i}\partial_{0i}\), and every perfect matching has exactly
one site-zero edge.  Physical Euler without its divided-Hasse and homogenizer
directions does not act: on \(\tau(H_m)\) its exact 24-term error is

\[
 -\epsilon_{01}\,\tau_{\mathrm{other}}(\partial_{01}H_m).
\]

## The decisive top-projection computation

Let \(\pi_{\mathrm{top}}\) take the coefficient of all four Hasse variables.
The 17-term indexed Hasse cycle has top \(r_0-T\), and its denominator support
by internal face is exactly \([5,3,3,1]\).  In the original underived cap
complex,

\[
 d\pi_{\mathrm{top}}N=(H_0-u)e_{\mathrm{Eq}}+Yw,
 \qquad
 \pi_{\mathrm{top}}dN=Yw.
\]

Therefore

\[
 [d,\pi_{\mathrm{top}}]N=(H_0-u)e_{\mathrm{Eq}}\ne0.
\]

The normalization is literal: \(H_0-u\) has 91 monomials and the coefficient
of \(u\) is \(-1\).  Thus the desired transported response-to-Eq square has
been identified exactly, but it appears as the first failure of descent (or
module associativity), not as the boundary of a physical Eq/P2 filler.

## Proper faces and downstream forced data

The same cube supplies, before coarsening, the two sigma-paired codimension-one
faces

\[
 q_{23{:}21}(r_0-T),\qquad q_{45{:}12}(r_0-T).
\]

This does **not** identify either universal Hasse coefficient with the required
occurrence-local P2 vector.  Conditional on that still-missing landing, the
literal Leibniz rule

\[
 d(q_{23}a)=q_{23}d(a)+dq_{23}a
\]

forces the endpoint-even 12-coordinate \(0102/dq_{23{:}21}\) conormal.  Its
augmentation and ordinary-residue aggregate are zero, while the primitive
detector \(+e_0+e_3-e_1-e_6\) has value \(35/72\).  Sigma gives the
\(0121/dq_{45{:}12}\) mate with the same normalized value.

The augmented target pair already closes, so there is no independent target
obstruction.  At the root-even cap top, \(B_E=(r_0-T)_E\) has
\((\mathrm{Eq},Yw,W,\mathrm{target},\mathrm{ainc})=(E,E,E,0,0)\).  A physical
raw C-plus landing must additionally carry the hidden labelled faces

\[
 (\mathrm{lower/private},\mathrm{word\text{-}ores})=(-E,+E),
\]

as well as the complete Eq residual \(-\delta_+\) and labelled residue
\(v=(B_1+B_4)/2\).  Those data are not created by \(N\) merely because its
aggregate target and ordinary residue vanish.

## Consequence and next exact test

The full-star action is strict on the complete translated Hasse object and
fails precisely at the passage to the underived physical Eq/P2 object.  The
shortest remaining positive attack is therefore not another coefficient
identity.  It is an explicit strong deformation retract of the translated
Hasse cube and homological transfer of the action.  One must compute whether
the first correction \(pAhAi\) has boundary \((H_0-u)e_{\mathrm{Eq}}\) and,
more stringently, whether its two proper faces land in the literal
\(0112/q_{23{:}21}\) and \(0121/q_{45{:}12}\) P2 objects.  If that correction
stays in derived/off-grade Hasse rows, the commutator above is the terminal
physical obstruction.

## Scope

This is an exact rational theorem for the canonical cube, all 17 indexed Hasse
terms, all proper-face support, the endpoint-even quotient, the q23 face and
sigma mate, and the protected Eq/Yw/W/target/ainc plus hidden lower/ores
signatures.  It does not construct the occurrence-local P2 placement, an SDR
transfer, or the global response-to-cap comparison.

Run:

```bash
python3 computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py --mode all
python3 computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py --mode cube
python3 computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py --mode action
python3 computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py --mode defect
python3 computations/verify_h3_full_star_cap_totalization_eq_orbit_gate.py --mode faces
```

Frozen ledger:

```text
5da0aa4be82c58333e181bb324245453077ba39791f070bb322518351f139841
```

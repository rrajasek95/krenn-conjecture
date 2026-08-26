# Strengthened Conjecture 6.2 at the labelled X23 interface

Status: **THE EXACT CONDITIONAL INTERFACE IS PROVED SUFFICIENT; THE TWO
PHYSICAL FILLERS AND THEIR AB/AC PLACEMENTS ARE NOT CONSTRUCTED.**

Parent manifest: `00899a99e57e9ced9eed7e3346cf54431037f688caab92f29a7e59d72ad95dc9`.
Scope: canonical `h=3` only.

## Exact strengthened statement

For `rho in {AB,AC}` and `c in {23,45}`, require a source-valid cell
`Lambda_c^rho` in one identical physical word, fine, repeated/Hasse,
fixed-`C4`-tail, operation-idempotent, and root-labelled grade, with

\[
d\Lambda_c^\rho=A_{[a|b],c}^\rho-B_c^\rho
                    +A_{[b|a],c}^\rho-C_c^\rho.       \tag{1}
\]

Require a source-labelled placement `J_c^rho` whose four displayed faces are

```text
A_[a|b]  -> P_f,
B         -> K_Eq,L,
A_[b|a]  -> K_Eq,R,
C         -> D4.
```

It must commute with the differential, restriction, reinsertion, every
protected readout `(target,q,anchor,W,ores,ridge,eta,sigma)`, root transport
`tau_AB,AC`, and cut involution `sigma`.  In particular

\[
\begin{aligned}
dJ(\Lambda)&=Jd(\Lambda)=P_f-K_L+K_R-D_4,\\
\tau J^{AB}&=J^{AC}\tau,\\
\sigma J_{23}&=J_{45}\sigma,
\qquad \sigma\Lambda_{23}^\rho=-\Lambda_{45}^\rho.   \tag{2}
\end{aligned}
\]

Under these hypotheses `kappa_c^rho=J_c^rho(Lambda_c^rho)` has exactly the
previously forced mixed-square boundary, AB/AC naturality, and sigma sign.
Thus this statement is sufficient.  It is strictly stronger than the
character-level filler branch of Conjecture 6.2.

## The best existing candidate

Put the two ordered direct faces in separate chart coordinates and let the
presentation-safe relative switch graphs satisfy

\[
 dG_B=t_B-(B-A_{[a|b]}),\qquad
 dG_C=t_C-(C-A_{[b|a]}).                              \tag{3}
\]

If a physical absolute carrier satisfies

\[
                    d(E_B+E_C)=t_B+t_C,               \tag{4}
\]

then

\[
 \boxed{\Lambda=G_B+G_C-E_B-E_C},\qquad
 d\Lambda=A_{[a|b]}-B+A_{[b|a]}-C.                  \tag{5}
\]

The checker verifies (5) literally.  The relative graphs in (3) are the
constructed part; (4) is not present in the pinned source inventory.  The
earlier Gate-II notes call precisely this missing absolute carrier the
physical saturation.  Consequently (5) is a conditional formula, not a
construction of either `Lambda^AB` or `Lambda^AC`.

The standard Koszul candidate `epsilon wedge theta` does not repair this:
its private and reduced-Eq readouts are tied, hence its balanced charge is
zero.  A Conjecture-6.2 filler has primitive balanced charge one.

## Components that do commute

In chart order `(A_[a|b],B,A_[b|a],C)`, the balanced charge is
`(1,-1,1,-1)`.  The displayed placement sends it coordinatewise to the edge
cycle `(P_f,K_L,K_R,D4)=(1,-1,1,-1)`.  The four edge boundaries cancel at
all four vertices and have rank three.  This proves the coefficient-level
`d^2=0` and fixes every sign.

The intrinsic `q23` delete/reinsert route and delete-first response route
agree coefficientwise on all 90 pinned descendants.  Root transport sends
the AB coefficient packet to AC with coefficient `+1`.  The cut involution
sends the decorated `q23` monomial to `q45` with coefficient `+1`, but sends
`D_root tensor B1` to `-D_root tensor B4`; this is the source of the
required sigma coefficient `-1`.  These are genuine commuting components.

They do not construct `J`.  The strong diagonal source grant has rank 24;
adding AB, AC, their unlabelled sum, and both labelled sections gives the
exact ladder

```text
24, 25, 25, 25, 26.
```

Thus two independent `e_C A e_R` placement sections are missing.  A
root-forgetting aggregate supplies only one.

## First unproved equations

The earliest physical obligation is already degree zero: source-labelled
maps `Phi^AB` and `Phi^AC` must realize the coefficient chain-map formula

\[
 \Phi_1^\rho(\epsilon_s^\rho)=r_0^\rho,\qquad
 \Phi_0^\rho(c_f^\rho)=-E^\rho,
 \qquad d\Phi_1^\rho=\Phi_0^\rho d.                  \tag{6}
\]

The signs in (6) work, but the operation matrix units do not exist in the
pinned grammar.  Granting (6), the first placement equation for the filler
is

\[
 d_{edge}J_2^\rho(\Lambda^\rho)
   =J_1^\rho d_{chart}(\Lambda^\rho)
   =P_f-K_L+K_R-D_4.                                  \tag{7}
\]

Granting (7) as well, the first literal reinsertion equation occurs on the
word-`0102` occurrence-local section:

\[
 J_{23}^\rho\,Ins_{23}(s_{0102}^\rho)
    =Ins_{23}\,J_{\widehat{23}}^\rho(s_{0102}^\rho).  \tag{8}
\]

After every already known lower and ordinary-residue cancellation, the
unmatched projection of (8) is exactly

\[
D_{root}\otimes B_1\otimes(H_0-u)e_{Eq},              \tag{9}
\]

with lower/private, ordinary residue, `W`, target, and anchor coordinates
zero.  Its sigma mate is the corresponding `B4` term with the pinned minus
sign.  Equation (9), separately for AB and AC, is the first precise
reinsertion/readout counter-obligation.

## Minimal countermodel

Take two labelled chart complexes, each with a cell `Lambda^rho` bounding
(1).  Take two labelled target squares containing the four edges and their
primitive cycle, but no operation-changing degree-two generator.  Let tau
be `+identity` from AB to AC, sigma be `-identity` from `q23` to `q45`, and
set all protected external readouts to zero.

All character identities, `d^2=0`, tau/sigma covariance, and protected
readout equations hold.  Yet any placement with the specified degree-one
map would require

\[
0=dJ_2(\Lambda)=J_1d(\Lambda)=P_f-K_L+K_R-D_4\ne0.
\]

Therefore character-level labelled fillers do not imply the physical
placement.  This is a logical countermodel to the implication, not a GHZ
counterexample.

## Scope guard

No `Lambda`, `J`, `Phi`, or `kappa` is promoted.  This note does not prove
the filler branch of Conjecture 6.2, `Q23`, `PAComp(3)`, uniform `PAComp(h)`,
or the Krenn–Gu conjecture.

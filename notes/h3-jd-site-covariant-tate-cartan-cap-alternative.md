# Cartan removes the four standard cap classes; the Tate top does not remove the aggregate

## Exact decomposition

The physical word/ridge cap calculation leaves

\[
        P=\mathbb Z\{\lambda_1,\ldots,\lambda_5\}\simeq\mathbb Z^5,
        \qquad
        \epsilon(\gamma)=\sum_v\gamma_v.                 \tag{1}
\]

The five cyclic translates of the source-provenant physical Cartan prism
project to the oriented edges of a pentagon.  Their image is exactly the
saturated lattice

\[
                  P_{\mathrm{std}}=\ker\epsilon,          \tag{2}
\]

of rank four.  The gcd of the nonzero maximal minors is one.  Thus site/face
covariance really does remove every **projected standard component**; this
is not merely a rational rank observation.

This statement has an augmented-row guard.  A physical Cartan edge also has

```text
ordinary residue       (-1,+1,+1,-1),
D,W,target,anchor,Eq    0,
terminal               labelled -dOmega eta/sigma packet.
```

Consequently (2) is a theorem in the cap projection.  It is not by itself a
clean differential in the full residue/Eq/q/ridge/terminal complex.

## Why the top cell does not supply the fifth direction

On the five-cycle torus the minimal companion resolution is the cellular
resolution of a pentagon:

\[
 dE_i=e_i-e_{i+1},\qquad dF=\sum_i E_i.                \tag{3}
\]

Therefore

\[
                 d_1dF=\sum_i(e_i-e_{i+1})=0.          \tag{4}
\]

The unique degree-five Tate top is the compatibility among the five Cartan
or principal-parts edge comparisons.  It adds no face image.  In particular,
it does **not** map to

\[
                       (1,1,1,1,1)\in P.               \tag{5}
\]

The fine grading makes the distinction literal.  Each first-Tor face has a
`P3+K2` site profile, a permutation of `(2,1,1,1,1)`.  The Tate top has
profile `(2,2,2,2,2)`.  Calling it a primitive face augmentation would both
change homological degree and forget this repeated-site grade.

The alternating line of the seven-occurrence normalized Hasse cobar cannot
repair this through the natural order-forgetting readout.  Reordering the
seven occurrences acts by sign on `Alt7`, whereas the ordinary commutative
word/ridge face readout is invariant under occurrence order.  Exactly,

\[
 \operatorname{Hom}_{S_7}(\mathrm{sgn},P_{\rm order\text{-}trivial})=0.
                                                               \tag{6}
\]

Equivalently, after fixing a deleted face, pair every ordering of the six
remaining occurrences by an odd spectator transposition.  The alternating
coefficients cancel.  Thus an `Alt7`-to-aggregate transgression would need a
new orientation-twisted comparison cell (or an explicitly constructed
non-forgetful occurrence-to-site transgression); it is not furnished by the
normalized cube or the symmetric face readout.

This does not silently identify two different symmetries.  `S7` here
permutes the seven occurrences in one cobar top; physical site covariance
permutes deleted sites and the decorated edges they meet.  No committed
comparison identifies those actions.  The literal `C5` Tate calculation
above is the separate check in the actual selected face cycle.

## The exact remaining one-dimensional alternative

Let `p` be the cap projection of a candidate reduced response cell.  Four
Cartan edge columns together with `p` have determinant, up to orientation,

\[
                            \epsilon(p).                \tag{7}
\]

Hence:

* over characteristic zero, they span all of `P` exactly when
  `epsilon(p) != 0`;
* integrally, they span all of `P` exactly when `epsilon(p)=+/-1`;
* if `|epsilon(p)|=m>1`, the residual class is `Z/m`; and
* if every available reduced column has `epsilon=0`, the unique projected
  dual is `epsilon=sum_v lambda_v`.

If one source-valid `p` with nonzero aggregate exists in a covariant source
family, take its five cyclic translates and correct their standard parts by
the Cartan edges.  This constructs the complete equivariant reduced family
at the **projected** level.  Thus five unrelated new constructions are not
needed: the missing information is one aggregate scalar together with
covariant transport.

## What is still genuinely missing

Neither side of the projected alternative has yet been promoted through
the complete physical rows.

For the positive side, one needs a source-valid reduced response column in
the forced word/fine/repeated grade with primitive aggregate and its exact
`Eq`, physical `q`, labelled residue, ridge, `W`, `eta`, and `sigma` caps.
The Cartan corrections must cancel, rather than export, their residue and
terminal packets.

For the dual side, one needs a covector on the complete physical codomain
satisfying

\[
 i^*\widetilde\epsilon=\epsilon,
 \qquad J_{\mathrm{phys}}^*\widetilde\epsilon=0.        \tag{8}
\]

The eta/sigma numbers of the physical Cartan packet are compatible with
such a lift after a facewise `Omega/r` comparison, but that comparison is
precisely what remains unconstructed.  A source column with a 360-feature
boundary is not a covector lift.  Therefore the present theorem gives the
smallest exact construction-or-dual interface, but does not claim a fully
typed reduced response family or a physical terminal.

Verification:

```text
python3 computations/verify_h3_jd_site_covariant_tate_cartan_cap_alternative.py
python3 -O computations/verify_h3_jd_site_covariant_tate_cartan_cap_alternative.py
python3 -I -S computations/verify_h3_jd_site_covariant_tate_cartan_cap_alternative.py
```

The checker pins the normalized cap homology, physical Cartan descent,
cyclic covariance bridge, exact five-cycle resolution, augmented grade
guard, and face-epsilon terminal-typing guard.

Frozen ledger SHA-256:

```text
7465cab5fabb96a7e898384a4c80adf8c4a2f6cfb8deb43f8d4902365cff284d
```

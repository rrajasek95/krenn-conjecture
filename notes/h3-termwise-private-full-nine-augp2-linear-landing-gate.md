# The strongest linear `A_Gamma` system has a unique tied solution

## Outcome

There is no linear or naturality obstruction to the desired mixed-jet-to-cap
augmentation.  On the literal two-word carrier, the most general normalized
two-root ansatz has `18` parameters.  Chain-map, `A/B <-> A/C` naturality,
monic normalization, and compatibility with all site-repeating pair rows
have rank `11`.  The remaining seven parameters are exactly the diagonal
copy of the known shadow-zero carrier residual.

The literal private full-nine insertion/restriction square detects all seven.
Adding its termwise landing equations raises the rank from `11` to `18`.
Thus the formal enriched category has one solution:

\[
 \Phi_1(\epsilon_{AB})=r_{0,AB},\qquad
 \Phi_0(c_{AB})=-E_{AB},
\]

\[
 \Phi_1(\epsilon_{AC})=r_{0,AC},\qquad
 \Phi_0(c_{AC})=-E_{AC},
\]

with both seven-dimensional residual components zero.  Its cap signature is
`B=Eq` on each root, so it is `Psi`-dark.

Exact checker:
[`verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py`](../computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py).

## 1. Literal reconstruction of residual seven

The checker rebuilds the two complete direct-free coefficient rows

```text
pure word   11111111       90 matching monomials
mixed word  11211211       90 matching monomials
```

from the current source constructors.  On their `180`-dimensional literal
matching space, the complete codimension-two pair-shadow matrix has rank
`159`, hence fibre dimension `21`.  The checker then imposes the actual
committed readouts:

1. endpoint oddness;
2. tail-Weyl oddness;
3. the four corner residues;
4. complete word and fine-degree augmentations; and
5. every single-cell incidence readout.

The combined matrix has rank `173`.  Equivalently, the extra readouts have
rank `14` on the raw fibre, leaving

\[
                   180-173=21-14=7.                 \tag{1}
\]

This is an exact rational reconstruction, rather than a seven-dimensional
normal-form placeholder.

## 2. Why the `159` site-repeating rows do not decide this fibre

Every vector in (1) has zero *complete* pair shadow.  It therefore has zero
value on every subset of pair coordinates, including the `159`
site-repeating coordinates forced by the universal order-six replay.  Their
rank on residual seven is exactly zero.

This does not make the `159` rows dispensable.  They carry rank `153` on the
universal constrained order-six image at both checked primes and are required
for the whole-module target.  It only says that, after restricting to the
particular physical lift fibre, their compatibility equations are automatic.

Thus the two roles are distinct:

```text
universal order-six support repair       159 rows, rank 153 mod both primes
selected two-word lift ambiguity          7 rows still needed
```

## 3. The private insertion/restriction square is split monic

Let `M` be one of the `180` matching monomials and let `P_priv` be the fixed
two-cell private multiplier on `12|34`.  The literal full-nine boundary
feature is

\[
                         I_{priv}(M)=P_{priv}M.       \tag{2}
\]

The private restriction deletes precisely the two labelled factors of
`P_priv`.  The checker verifies on all `180` monomials that

\[
                         R_{priv} I_{priv}(M)=M.      \tag{3}
\]

All `180` features in (2) are distinct.  Consequently the termwise private
readout is injective on the whole matching space and has rank seven on (1).
By contrast, aggregating those coordinates back into the two scalar rows
`H_pure,H_mixed` has rank zero on (1); those aggregates were already among
the committed readouts.  The load-bearing datum is therefore **termwise**
`H_w`/private full-nine, not one more aggregate coefficient equation.

Equations (2)--(3) also give the exact restriction/insertion compatibility:
the needed readout is not an arbitrary seven-coordinate detector chosen
after row reduction.  It is the restriction of a literal split-monic source
face map.

## 4. The complete two-root affine system

Write the most general lift parameters as

\[
 (a_{AB},b_{AB},a_{AC},b_{AC},x_{AB},x_{AC}),
 \qquad x_{AB},x_{AC}\in\mathbb Q^7.                 \tag{4}
\]

Here

\[
 \Phi_1(\epsilon_\rho)=a_\rho r_{0,\rho}+x_\rho,
 \qquad
 \Phi_0(c_\rho)=b_\rho E_\rho,
\]

where `x_rho` records the literal shadow-zero freedom in the carrier lift.
The homogeneous chain-map equations and root naturality are

\[
 a_\rho+b_\rho=0,\qquad
 a_{AB}=a_{AC},\qquad b_{AB}=b_{AC},\qquad
 x_{AB}=x_{AC}.                                      \tag{5}
\]

Add the monic normalization `a_AB=1`.  The rank ledger is

```text
unknowns                                                        18
rank after chain map + full root naturality + monic             11
freedom (the diagonal residual seven)                             7
rank after the AB termwise private landing                       18
rank after both AB and AC termwise landings                      18.
```

The last equality is the useful naturality statement: once the full
`AB <-> AC` covariance graph is genuinely part of the augmentation, a
termwise landing on one root representative determines the other root.

Without that covariance, the two root labels remain independent:

```text
two separately normalized chain maps                  rank 4 / 18
+ AB termwise landing                                 rank 11 / 18
remaining AC ambiguity                                dimension 7
+ AC termwise landing                                 rank 18 / 18.
```

Hence neither an unlabelled sum nor a single ad hoc root section is enough.
One *natural* schema is enough.

## 5. Unique tied solution

The full rank system has the unique solution

```text
a_AB = a_AC =  1
b_AB = b_AC = -1
x_AB = x_AC =  0.
```

The sign `b=-1` is forced by `d epsilon=-c` and `d r0=E`.  In the mapping
cone convention this gives the same positive occurrence coefficient in the
private `B` and reduced `Eq` blocks.  Thus each root instance has

```text
(B,Eq)=(1,1),       Psi=0.
```

There is no remaining scalar, sign, residual, or root-transport ambiguity in
the linear enriched problem.

## 6. Why this is still formal

The first failure is not another rank condition.  It is the operation
idempotent equation.  The desired map must satisfy

\[
                         e_C A_\Gamma e_R=A_\Gamma,   \tag{6}
\]

where `e_R` is the response mixed-jet object and `e_C` is the `AugP2/K_Eq`
cap object.  In the current source-derived operation algebra,

\[
                              e_C A e_R=0.            \tag{7}
\]

Adding pair or private readout coordinates changes the codomain, but it does
not create the nonzero matrix unit required by (6).  The formal solution has
coefficient one on precisely that missing matrix unit.

The nearest literal multiplicative relation is

\[
                         H_w r_0-(H_0-u)r_w.           \tag{8}

Its typed `(ainc,word,target,ores)` value is

```text
(-H_w,0,H_w,0).
```

Relation (8) is a genuine source Koszul `S`-pair, but it is cap-internal and
off the receiving-section grade.  Physical target zero kills its `H_w`
target and anchor together.  Treating its termwise factors as the missing
response-to-cap map would change the operation idempotent by declaration;
restriction/insertion naturality does not authorize that change.

Therefore the exact remaining physical assertion is:

> The matching species carries a mixed divided-Hasse module action whose
> private insertion/restriction square is (2)--(3) and whose operation
> component is a natural nonzero `e_C A e_R` map.

If that source-derived action is constructed, the present calculation shows
that no additional choice remains: it is automatically the unique normalized
tied `A_Gamma` and supplies both root-labelled receiving sections.

## Scope

The residual, private-readout, and affine ranks are exact over `Q` for the
canonical `h=3` two-word/two-root packet.  The universal `159/153` support
calculation retains its matching two-prime scope.  This note proves uniqueness
conditional on the physical mixed divided-Hasse action; it does not prove the
existence of that operation or a full-source all-`h` comparison.

## Verification

```text
python3 computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py --mode all
python3 computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py --mode residual
python3 computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py --mode linear
python3 computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py --mode physical
python3 -O computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py --mode all
python3 -I -S computations/verify_h3_termwise_private_full_nine_augp2_linear_landing_gate.py --mode all
```

Frozen ledger SHA-256:

```text
0cc7b94a5d54da346ef3650213016fad5c080caf1a58cbc882f497f1a54c1cf5
```

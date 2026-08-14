# The minimal mixed-jet enrichment constructs `PSQJet_01`, but not its cap landing

## Outcome

There is a canonical source-derived closure below a hand-added `Phi` arrow.
Take the reduced universal divided-Hasse envelope of the literal endpoint-odd
polynomial

\[
  F_{01}^{-}=(p_0s_1-p_1s_0)q_{01}H_{2345},
  \qquad
  H_{2345}=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34},       \tag{1}
\]

and enlarge its target by the site-repeating `P3/P4` pair rows forced by the
whole-module order-six calculation.  Call this reduced envelope

\[
                  J^{\rm red,rep}_{PS/q}(\mathrm{EqSystem}).             \tag{2}
\]

The universal first jet of (1) is exactly the proposed `PSQJet_01`.  It has
the complete signed `6+6+3` product-rule packet, and combining it with the
endpoint-even response selects the six literal `db01` terms.  No new
off-diagonal arrow has been declared.

Inside the initial object (2), a primitive with zero termwise jet shadow is
zero.  Thus the abstract rank-nine `omega` does not occur in the minimal
reduced jet envelope.

However, the target-row enlargement does not construct an operation-changing
map.  The current cap `r0` has no termwise `H_w` or private full-nine values in
the root-carrier grade, and the literal operation graph still has

\[
        \operatorname{Hom}^0(\mathrm{response},\mathrm{cap})=0.           \tag{3}
\]

The root-labelled carrier therefore does **not** yet map to `r0`; the exact
two-word comparison retains seven dimensions invisible to every committed
readout.

This leaves one precise missing axiom:

> **Reduced termwise-faithful mixed-jet cap augmentation.** Construct an
> augmentation-preserving natural dg map
> \[
> A_{\Gamma}:J^{\rm red,rep}_{PS/q}(\mathrm{EqSystem})
>       \longrightarrow C_{\mathrm{AugP2},\Gamma},                       \tag{4}
> \]
> natural for literal restriction, insertion, endpoint transpose and the
> eight one-root labels, with
> `A_Gamma(epsilon_s)=r0`, `A_Gamma(c_f)=-E`, retaining all site-repeating,
> termwise `H_w`, and private full-nine rows, and with the joint termwise
> readout injective on the reduced primitive off-diagonal kernel.

This is one representable source-operation axiom, not a declared finite
grammar.  Under (4), zero-shadow `omega` is forced to vanish and the relative
degree-one quotient is exactly the eight standard `Psi`-dark `kappa` classes.

The literal right side needed for terminal promotion is also now fixed.  It
is the target-cancelled Gate-II balanced packet

\[
                         b_{\rm GII}=i(B_\delta),
             \qquad \delta=(1,1,-1,-1),                              \tag{5}
\]

in the complete `Gamma_*` codomain, with every protected non-`B` row zero.
The normalized two-block and covariantly completed `Psi` representatives both
read (5) as one.  What remains open is the source-valid construction placing
(5) in the image of the same exhaustive augmented map.

Focused checker:
[`verify_h3_reduced_site_repeating_mixed_jet_augp2_enrichment_rhs_gate.py`](../computations/verify_h3_reduced_site_repeating_mixed_jet_augp2_enrichment_rhs_gate.py).

Current-tree whole-module replay:
[`verify_h3_order6_site_repeating_target_enrichment_current_tree.py`](../computations/verify_h3_order6_site_repeating_target_enrichment_current_tree.py).

## 1. The universal jet gives `PSQJet_01`

The polynomial (1) has six squarefree monomials.  Apply the reduced universal
derivation, with no empty/constant jet:

\[
                         d(fg)=df\,g+f\,dg.                              \tag{6}
\]

Its thirty literal first-jet terms split as follows:

| differentiated factor | literal terms | signed pairs |
|---|---:|---:|
| endpoint `dB-dC` | 12 | 6 |
| tail `q01*dH` | 12 | 6 |
| `dq01*H` | 6 | 3 |

This is precisely the required `6+6+3` face inventory.  In particular,

\[
 B={1\over2}\bigl((B+C)+(B-C)\bigr),                                  \tag{7}
\]

so the same half-sum applied to the endpoint-even complete response and the
endpoint-odd jet leaves the fifteen selected-`B` first faces.  Its tail part
is exactly

\[
 p_0s_1\sum_{23|45,24|35,25|34}
   (dq_e q_{e'}+q_e dq_{e'}),                                           \tag{8}
\]

the selected six-term `db01` packet.

The thirty reduced jet terms form a literal free basis of the initial
envelope.  The termwise jet readout is the identity matrix on that basis.
Consequently

\[
 \ker\bigl(J^{\rm red}_{1}\longrightarrow
              \mathbb Q^{30}_{\rm termwise\ jet}\bigr)=0.              \tag{9}
\]

Equation (9) is the exact minimality statement.  An independently adjoined
`omega` with zero coefficient and termwise jet shadow belongs to a larger
square-zero extension, not to the initial reduced jet object.

## 2. Why the direct-free target is too small

The current-tree replay reconstructs all `8,580` order-six operator columns
from the pinned source constructors and computes

\[
                  S=D_2(\ker(\mathrm{source},D_1)).                     \tag{10}
\]

At both primes `1,000,003` and `999,983`, the exact ledger is

```text
dim S                                      488
site-repeating pair coordinates hit        159
rank of the site-repeating projection       153
intersection with direct-free coordinates   335.
```

A pair in the shadow of a direct-free matching must use four distinct sites.
The first forbidden row hit by (10), for example, contains cells `(01)` and
`(07)`, which repeat site `0`.  No linear combination of direct-free matching
chains can have such a coordinate.

Therefore a whole-module jet comparison cannot land in the old direct-free
target.  The minimal coordinate enlargement adds exactly the `159`
site-repeating rows met by (10); the constrained image uses `153` independent
directions among them.

This is a necessity theorem, not a construction of the target differential.
Adding row coordinates says where a universal jet is allowed to land; it does
not say what physical chain or cap generator realizes each row.

## 3. The exact remaining ambiguity after adding the rows

For the selected two-word root-carrier comparison, the pair-shadow fibre has
dimension `21`.  All committed parity, corner, aggregate, and coarse readouts
have rank `14`, leaving

\[
                            21-14=7                                  \tag{11}
\]

explicit shadow-zero directions.  Termwise full-nine or equivalent `H_w`
readouts are load-bearing precisely because they are injective on the
grade-refined freedom; the current `r0` constructor does not define their cap
values in this grade.

The operation problem is independent and even earlier.  Site-repeating rows
enlarge the target object, but do not add an edge in the operation category.
Thus (3) remains true after the `159`-row enlargement.  Neither `PSQJet_01`
nor its seven-dimensional ambiguity has a physical image in `r0`.

This answers the requested test:

```text
universal reduced jet contains PSQJet_01       yes
site-repeating rows remove support obstruction yes
current data map the root carrier to r0         no
current data decide bright versus dark value   no; residual dimension 7
```

## 4. Why axiom (4) is the minimal missing enrichment

Axiom (4) has four source-level requirements:

1. naturality for the actual restriction/insertion and endpoint/root-labelled
   maps;
2. the already forced monic chain-map normalization
   `epsilon_s -> r0`, `c_f -> -E`;
3. retention of all `159` site-repeating rows and the termwise `H_w` and
   private full-nine coordinates; and
4. faithfulness of those termwise rows on the reduced primitive kernel.

The first two construct `Phi` from the universal jet rather than adding a
matrix unit by hand.  The third makes the whole-module map defined.  The
fourth is the minimality clause that excludes a hidden square-zero summand.

Indeed, the rank-nine counterguard `omega` has zero universal coefficient,
jet, and existing-constructor shadow.  Under the faithfulness clause it must
be zero.  Conversely, dropping faithfulness permits the old completion
`P_Phi+omega` without changing any currently implemented source datum.
Therefore no weaker assertion about the existing rows excludes `omega`.

After (4), the only mixed relative first-degree features are word change and
`K_Eq`.  Their simultaneous interchanges occur at the eight one-root words

```text
0012  0102  0110  0111  0122  0212  1112  2112.
```

Strict multiplicativity through tied `r0` gives `(v_i,v_i)` in `(B,Eq)`, so
all eight have `Psi=0`.  This is the desired essential-surjectivity theorem,
conditional on one geometrically meaningful augmentation, rather than on a
list of allowed generator names.

## 5. The literal augmented right side

The formal Gate-II cylinder has the two faces

\[
 X=(\chi_w,+\delta_{\rm target}),
 \qquad
 Y=(0,-\delta_{\rm target}),
 \qquad
 X+Y=(\chi_w,0).                                      \tag{12}
\]

After the source-labelled `C4/AugP2` placement, the terminal candidate is
not the raw target face `Y`, nor an abstract eight-coordinate vector.  It is
the complete target-cancelled output (5) in the literal grade

```text
word       01211222
fine       six t*q_(v,N) P3+K2 occurrence degrees
repeated   P3+K2, retaining site-repeating jet rows
operation  C4/AugP2 mixed orbit/K_Eq
window     2345 with literal occurrence labels.
```

Its complete protected values are

```text
B                         ( 1,  1, -1, -1)
Eq                        ( 0,  0,  0,  0)
target, W, ordinary residue                    all 0
M, ainc, q, P_f                                all 0
ridge, eta, sigma, global W, tail escape       all 0.
```

On the old cap quotient, one may use

\[
 \Psi_{B/Eq}={1\over4}\delta\cdot(B-Eq).              \tag{13}
\]

Its covariant completion through the known `r0/T/rho/K` packet is

\[
 \widetilde\Psi={1\over4}
   \bigl(\delta_B-\delta_{target}-\delta_W+\delta_{ores}\bigr),          \tag{14}
\]

with zero coefficient on `Eq`, `M`, `ainc`, `q`, `P_f`, ridge, eta and
sigma.  Both representatives satisfy

\[
                   \Psi_{B/Eq}(b_{\rm GII})
                 =\widetilde\Psi(b_{\rm GII})=1.                       \tag{15}
\]

Thus the accepted Macaulay/Fredholm contradiction has a completely explicit
input.  It requires, in one and the same full codomain,

\[
 \widetilde\Psi J_{\rm phys,\Gamma_*}=0,
 \qquad
 b_{\rm GII}\in\operatorname{im}J_{\rm phys,\Gamma_*},
 \qquad
 \widetilde\Psi(b_{\rm GII})=1.                                      \tag{16}
\]

The first two equations in (16) contradict the third.  Axiom (4) is designed
to make the first equality exhaustive.  The remaining positive/source task is
to construct the target-cancelled physical cylinder (12) and thereby prove
the middle membership statement.  At present (5) is the exact required RHS,
but that membership is not proved, so no contradiction is claimed.

## Sharp frontier

What is proved:

```text
PSQJet_01 from universal reduced Hasse jet       yes
zero-shadow omega inside the initial jet         no
direct-free whole-module target sufficient       no
necessary new target coordinates                 159 (rank 153 image)
termwise ambiguity after committed readouts      7
literal full terminal RHS                        i(B_delta), explicitly typed
normalized Psi value on that RHS                 1.
```

What is not proved:

```text
reduced termwise-faithful jet->AugP2 map          open, one axiom (4)
root-labelled carrier maps to r0                  open
target-cancelled RHS belongs to the physical image open
accepted Macaulay/Fredholm contradiction          not yet.
```

## Verification

The focused checker is fast and should pass normally, optimized, and in an
isolated/no-site interpreter.  The whole-module current-tree audit is
deliberately expensive because it rebuilds all `8,580` columns and performs
both modular eliminations; use its `--mode structural` option for the fast
predicate/pin audit and its default `--mode full` for the complete replay.

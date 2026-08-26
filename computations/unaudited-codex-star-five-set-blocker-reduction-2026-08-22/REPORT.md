# Universal five-set annihilator removes every star selector

Status: **UNAUDITED exact source-level theorem audit**.  The proposed
simplification is correct.  No polynomial system was solved.

## Outcome

On the normalized full `X5` system, every one of the 168 response-star
carriers has at least one **diagonal** blocker.  This requires no carrier
rank split, no localizer, no minimum-norm equation, and no assumption on the
direct pair block.

Consequently the all-blocked incidence residual reduces exactly to the 560
triangle clauses:

```text
normalized X5 + all 728 star/triangle carriers blocked
  <=>
normalized X5 + all 560 triangle carriers blocked.        (1)
```

In the Hermitian Gram system this removes 168 selector variables and
`168*9=1512` carrier Gram variables.  The nontrivial carrier incidence now
uses 560 selectors and 5,040 Gram variables.

## 1. Canonical star and its outside five-set

Fix a cap pair `p,q` and a residual star centre `v`.  Put

```text
W = B \ {p,q,v},                 |W|=5,
C = {p,q,v},                     |C|=3.
```

Let `L_pqv(A)` be the frozen `90x9` response-star matrix.  Its rows are the
nine endpoint-colour cells on each of the ten residual edges internal to
`W`.  Thus

```text
K in ker L_pqv(A)
```

means exactly that every response edge internal to `W` vanishes.

Apply the universal five-set annihilator theorem to the ten source blocks
internal to `W`.  It gives a functional

```text
beta in V_W^*,
beta(V_u tensor h_u)=0             for every u in W,
b=delta_W(beta) !=0,               b in C^3.              (2)
```

This theorem is unconditional over arbitrary complex endpoint-ordered
blocks and is a formal consequence of the certified six-site obstruction.

## 2. Literal contraction identity

Take an arbitrary `K in ker L_pqv(A)` and contract the exact eight-site
matching tensor by `K` on `p,q` and by `beta` on `W`, leaving the colour slot
at `v` exposed.

Every perfect matching has an odd number of edges across the `3|5` cut
`C|W`, hence exactly one or three.  The checker reconstructs all 105 source
matchings as the disjoint union

```text
T1: 3*5*PM(4) = 45 matchings,
T3: C(5,2)*3! = 60 matchings.                             (3)
```

### The one-crossing sector

A one-crossing matching exposes a unique `u in W`; the remaining four sites
of `W` contribute the internal cofactor `h_u`.  Therefore its complete
contraction factors through

```text
beta(V_u tensor h_u),
```

which is zero by (2).  This kills `T1` cofactor by cofactor, with no
cancellation between exposed sites.

### The three-crossing sector

A three-crossing matching leaves one internal edge `ab` of `W`.  Fix the
endpoint `u in W` matched to the exposed centre `v`; call the remaining two
crossing endpoints `x,y`.  The two assignments of `p,q` to `x,y`, after
contraction by `K`, give precisely

```text
sum_(i,j) K_ij (
  A_px[i,alpha] A_qy[j,beta]
 +A_py[i,beta]  A_qx[j,alpha]),                           (4)
```

the literal frozen response row on the outside edge `xy`.  Since `x,y` are
in `W` and `K in ker L_pqv(A)`, (4) vanishes in every endpoint-colour cell.
This kills `T3` row by row.  The audit checks both endpoint orientations and
all 60 three-crossing source matchings.

Hence the contracted source tensor is zero.

## 3. The target forces a diagonal blocker

On normalized `X5`, the complete output is

```text
Phi(A)=Delta_8=sum_(c=0)^2 e_c^(tensor 8).
```

The same contraction on the target equals

```text
sum_(c=0)^2 b_c K_cc e_c^(v).                             (5)
```

The three exposed vectors are independent, so comparison with the zero
source contraction gives

```text
b_c K_cc=0,                     c=0,1,2,                  (6)
```

for every `K in ker L_pqv(A)`.  Since `b!=0`, choose one fixed colour `c`
with `b_c!=0`.  Then

```text
K_cc=0 for every K in ker L_pqv(A).
```

Finite-dimensional annihilator duality now gives

```text
K_cc in rowspan L_pqv(A).                                 (7)
```

Thus the star carrier has a diagonal blocker.  No division appears in the
identity: nonzero `b_c` is used only to select which one of the three exact
coordinate functionals lies in the row space.

The argument is invariant under `S8 x S3`, so the canonical calculation
transports to all

```text
28 cap pairs * 6 residual centres = 168
```

star carriers.

## 4. Precise scope

“`X5`” in (1) means the full normalized exact system: all 6,558 mixed
amplitudes vanish and the three pure amplitudes equal one.  Equation (5) is
where the pure target normalization is used.  The statement is not claimed
for `X4`; the six active W40 stars remain the correct hostile control because
W40 omits the off-count-five equations.

The proof uses the certified six-site theorem through the universal
five-set annihilator.  This is not circular: the six-site obstruction is the
certified base of the eight-to-six proof spine.

The theorem is stronger than merely knowing that some one of the four star
blockers exists: it removes the direct-pair blocker from consideration and
selects one of the three diagonal blockers.  It does not select a uniform
colour across different stars.

## 5. Reduced triangle-only normal-cone target

The singular minimum-norm system from
`../unaudited-codex-singular-normal-cone-gram-system-2026-08-22/REPORT.md`
can now be replaced by

```text
(FIBRE)       Phi(A)=Delta_8.

(NORMAL)      (A,-A) lies in the reduced real conormal closure CN(X_R).

(BLOCK-MIN)   A_E=L_E^*L_E eta_E
              for all 8 full stars and all 56 site triangles.

(BALANCE)     the 21 site-colour target-torus moment equalities.

(TRI-BLOCK)   p(sigma_C)=0 and
              L_C^*L_C z_C=sum_i d_i(sigma_C) ell_C,i^*
              for the 560 triangle carriers only.         (8)
```

Every hypothetical exact fibre minimum satisfies (8), so inconsistency of
this reduced system still proves the conjecture.  Conversely, within the
normalized `X5` locus the omitted 168 star clauses follow from (2)--(7), so
(8) loses no all-blocked incidence information.

For the cancellation-free support mechanism, every pairwise-intersecting
response-support graph lies in a star or a triangle.  Since the star case is
universally blocked on normalized `X5`, any remaining active carrier of this
type must be witnessed by a triangle.  This does not claim to cover a clean
cap whose wider response support cancels in the cap error.

The smallest remaining incidence question is therefore triangle-specific:
whether the 560 triangle blocker Gram clauses, together with the full mixed
equations and the reduced normal cone, are inconsistent or force a wider
cancellation-clean cap.

## Replay

```sh
python3 computations/unaudited-codex-star-five-set-blocker-reduction-2026-08-22/audit_star_five_set_blocker_reduction.py --write-results
python3 -O computations/unaudited-codex-star-five-set-blocker-reduction-2026-08-22/audit_star_five_set_blocker_reduction.py
python3 -I -S computations/unaudited-codex-star-five-set-blocker-reduction-2026-08-22/audit_star_five_set_blocker_reduction.py
```

The hostile `--mutate-crossed-orientation` run must fail.  The standard run
returns logical SHA-256
`9f06b516ca81c4c32485c59cf602aaff1380f87c64ae7a75e5490e4d29ad5b0d`.

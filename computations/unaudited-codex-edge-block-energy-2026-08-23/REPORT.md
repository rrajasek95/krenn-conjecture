# Edge-block minimum-norm recurrence and energy collapse

Status: **exact block formula proved; the summed identity is terminal.**  The
regular KKT sum is the already archived Euler trace, while its only positive
refinement is the first perfect-matching incidence-Gram / centered star-frame
SOS.  It neither forces an invisible block nor contains the quadratic response
data needed to force a clean cap.

## 1. Literal edge block

Let `n=2m`, let `e={p,q}`, and write

```text
C_e = Phi_(V\e)(A) in tensor_(v notin e) C^3,
h_e = ||C_e||^2.
```

After putting the endpoint sites back in their source order, the derivative
with respect to the nine cells of `A_e` is

```text
T_e(X) = X tensor C_e.
```

Thus the column `(e;i,j)` is `e_i^p tensor e_j^q tensor C_e`.  The nine
endpoint word supports are pairwise disjoint and

```text
                         T_e^* T_e = h_e I_9.             (1)
```

This is stronger than a mere column-disjointness statement: all nine columns
are orthogonal copies of the same six-site cofactor vector.

Let `B_e` be the sum of matching terms that avoid `e`.  The exact fibre
equation is

```text
                         Y-B_e = T_e(A_e).                (2)
```

At a minimum of source norm on the fibre, (1)--(2) give the regularity-free
block rule

```text
h_e=0       => A_e=0,
h_e nonzero => A_e=h_e^(-1) T_e^*(Y-B_e).                (3)
```

The first implication is the archived invisible-block deletion rule.  The
second is not a new constraint: when `h_e` is nonzero, `T_e` is injective and
(3) is just (2) after applying its Moore--Penrose left inverse.

With the Hermitian product linear in its second argument, the literal cell
formula for ternary GHZ is

```text
h_e A_e[i,j]
 = delta_(i,j) conjugate(C_e[i,i,i,i,i,i])
   - sum_r conjugate(C_e[r]) B_e[i,j,r].                 (4)
```

Here `r` runs over the `3^6` residual words.  The checker replays (4), before
simplification by (2), for all nine cells in every control edge.

## 2. KKT sum

At a regular global fibre minimum for the objective `(1/2)||A||^2`, a single
output multiplier satisfies

```text
                         A_e=T_e^* Lambda                 (5)
```

for every edge.  Since every perfect matching contains `m` edges,

```text
sum_e T_e(A_e)=mY.
```

Pairing (5) with `A_e` and summing gives only

```text
                 ||A||^2 = m <Lambda,Y>.                 (6)
```

This is exactly the global conormal Euler trace already ranked second and
retired in the Hermitian-star audit.  In Fritz--John form it is
`alpha||A||^2=m<Lambda,Y>`; the `alpha=0` branch does not permit normalization
to (6).

## 3. The positive edge energy

Put

```text
U_e=T_e(A_e),
E=sum_e ||U_e||^2=sum_e h_e||A_e||_F^2.
```

Every matching has four edges and exactly one edge at each site, so for `N=8`

```text
sum_e U_e=4Y,                   sum_(e incident v) U_e=Y. (7)
```

Completing the square over the 28 edge contributions gives the exact identity

```text
E = 12/7 + sum_e ||U_e-Y/7||^2                         (8)
```

when `Y` is normalized ternary GHZ (`||Y||^2=3`).  Equivalently, summing the
seven-term centered identity at all eight sites gives twice the SOS in (8).

There is no vanishing conclusion in (8).  It is a lower bound.  Equality
would force `U_e=Y/7` for every edge, which makes every contribution visible,
the opposite of an invisible-block conclusion.  A zero `U_e` merely gives one
strictly positive centered summand.

This is also exactly the first perfect-matching incidence Gram sector.  If
`t_M` is the tensor contributed by matching `M`, then

```text
E=sum_(M,N) |M intersect N| <t_N,t_M>.                   (9)
```

On the 105 matchings of `K8`, the incidence kernel has eigenvalue `60` on
`[8]`, eigenvalue `18` on `[6,2]`, and zero on the other three matching
modules.  Therefore (8) is the fixed trivial energy `12/7` plus the
nonnegative `[6,2]` energy.  This is within the already screened
association-scheme Gram route; it supplies no coupling that kills the
`[6,2]` part.

Finally, (1)--(9) see only one edge block and its complementary cofactor.
They contain none of the products between the two endpoint-star families
that define a carrier response matrix.  No clean-cap rank or membership
condition can be read from this scalar energy without an additional
source-relative theorem.

## 4. Mandatory exact controls

The exact `n=4` ternary GHZ global minimum has

```text
six edges:                      h_e=1, ||A_e||^2=1,
all six blocks visible/nonzero,
||Y||^2=3,                      E=6,
centered floor/slack:           2 + 4.
```

The exact multiplier `Lambda=Y` satisfies `T_e^*Lambda=A_e` on all six
blocks.  Thus even at an exact GHZ global minimum the edge SOS is strict and
does not select an invisible block.

For the frozen phased `n=6` block-injective local minimum of its own non-GHZ
output, exact `Q(omega)` replay gives

```text
source norm squared:            63
output norm squared/support:    1529 / 645
all 15 blocks visible/nonzero
(h_e,||A_e||^2) profile:        (19,1)^6, (81,1)^3,
                                (87,9)^3, (90,9)^3
edge energy:                    5136
centered floor/slack:           4587/5 + 21093/5.
```

This control has exact pure normalization, actual phased mixed cancellation,
block injectivity, and local minimum behavior, yet the positive edge slack is
large.  It confirms that block normality and Hermitian positivity do not
produce the missing global sign/equality theorem.

## 5. Replay and terminal verdict

```sh
python3 computations/unaudited-codex-edge-block-energy-2026-08-23/audit_edge_block_energy.py --write-results
python3 -O computations/unaudited-codex-edge-block-energy-2026-08-23/audit_edge_block_energy.py
python3 -I -S computations/unaudited-codex-edge-block-energy-2026-08-23/audit_edge_block_energy.py
```

All modes replay every literal block numerator and return logical digest
`3445ff27cc1feb184d2c8c41221804922ef474c2c9375077b8f23544bd8f3db9`.
The hostile `--mutate-n4-energy` mode fails.

**Verdict:** retire the minimum-norm edge-block recurrence as a global bridge.
It contributes exactly invisible-block deletion on `h_e=0`, the old Euler KKT
trace, and the old Hermitian/matching-Gram centered SOS on `h_e!=0`; none forces
a cap or contradicts an all-visible hypothetical `N=8` GHZ preimage.

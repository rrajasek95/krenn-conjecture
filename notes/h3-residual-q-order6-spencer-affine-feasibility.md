# An exact first-flat representative exists; second-flatness is the wrong target

## Exact positive result

Inside the complete 8,580-column quadratic-coefficient/order-six affine
space, there is an exact rational representative which simultaneously

```text
kills all three quadratic source products,
has the prescribed sixteen-coordinate -delta shadow,
and has zero first coefficient-prolonging face.
```

One reconstructed solution has 343 terms.  The exact constraint rank is
1,328, and its coefficient denominators divide products of `2,3,5`.  The
solution digest is

```text
7517c75e964058a1ba4f9cbb285d94a61c6fa7da98e9536cc760d9ddc5f6afae
```

The result disproves the idea that the private singleton face of a chosen
sparse representative is an invariant obstruction.  Affine freedom in the
complete order-six source block removes every first face at once.

The reconstructed shadow has two nonzero fine-shift components.  They are
the two source-word weights subsequently shown to acquire one common total
source-module degree in the endpoint-composition theorem.

## Second-layer diagnostic

The first-flat representative still has 3,288 nonzero second faces.  A
separate diagnostic imposes zero first and second faces simultaneously.
Over `F_1000003` its exact sparse ranks are

```text
constraint rank    8102,
augmented rank     8103,
equations         51057.
```

This proves incompatibility over that finite field only.  It is not by
itself a characteristic-zero obstruction, because a rational solution may
have denominator divisible by the chosen prime.

More importantly, simultaneous second-flatness is stronger than the proof
requires.  The complete Hasse tower has a nonzero pair layer and necessarily
nonzero coherent higher layers, while the universal
[Euler contraction](h3-universal-spencer-euler-contraction.md) proves that
the positive-degree total Spencer complex is contractible.  The rank jump is
therefore evidence that one fixed operator representative cannot replace
the relative total complex.  It is not a reason to enumerate the third
layer.

## Scope

The exact theorem concerns the three quadratic source products in the
bounded order-six block.  It does not physically type the repeated grade,
construct the relative terminal comparison, or prove a characteristic-zero
second-flat no-go.

Verification:

```text
python3 computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py
python3 -O computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py
python3 -I -S computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py
python3 computations/verify_h3_residual_q_order6_spencer_affine_feasibility.py --second-row-elim
```

Frozen default ledger SHA-256:

```text
f1c28deafd72892f58f1d7a0f9e8d14c30b16725297f7344e388f65389651985
```


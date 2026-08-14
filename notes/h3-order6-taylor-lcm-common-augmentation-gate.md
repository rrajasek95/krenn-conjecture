# The response complement is a divided Taylor--Spencer family

## Outcome

The frozen rank-`77` complement is almost, but not literally, an ordinary
degree-two Taylor family.

Every off-diagonal pivot is realized by two literal matching parents.  Its
minimal uncoloured lcm graph is

\[
                         2K2+C4.                     \tag{1}
\]

But the complement also contains diagonal decorated pairs `(a,a)`.  Their
minimal two-parent graph is `4K2`; the squarefree lcm contains `a` only once,
so its ordinary same-cell second Hasse face is zero.  Those rows require a
divided-power/Tate diagonal cell.

Thus the minimum common response constructor has two face types:

```text
off diagonal     ordinary two-parent Taylor lcm, topology 2K2+C4;
diagonal         divided-power gamma_2(iota_a), topology 4K2.
```

One *divided Taylor--Spencer family* contains both.  An ordinary Taylor
complex alone does not.

Checker:
[`verify_h3_order6_taylor_lcm_common_augmentation_gate.py`](../computations/verify_h3_order6_taylor_lcm_common_augmentation_gate.py).

## Exact parent census

The occurrence-parent module has `180` generators:

```text
pure word 11111111                     90
mixed word 11211211                    90.
```

For every pair row in the fixed response image, the checker searches all
literal pairs of parents, forms the decorated squarefree lcm, and minimizes
its cell degree and uncoloured alternating-union topology.

The full `159`-coordinate support is

| kind | coordinates | minimum graph topology |
|---|---:|---|
| off diagonal | 152 | `2K2+C4` |
| diagonal `(a,a)` | 7 | `4K2` |

Of these, `156` have minimum decorated lcm degree six and three have degree
five.  The latter arise when pure and mixed parents have the same uncoloured
matching and differ in only one decorated edge; they remain in the `4K2`
parent topology.

All `159` coordinates occur in the pure response shift.  `112` also occur
in the mixed shift, so the exact shift-support split is

```text
pure only                              47
pure and mixed                        112.
```

No mixed-only coordinate occurs in this pinned block.

## The canonical rank-77 complement

After inserting the rank-`76` first-seed basis, lexicographic elimination
adds `77` monic constrained response vectors.  Their pivot rows are

| pivot kind | count | minimum topology |
|---|---:|---|
| off diagonal | 73 | `2K2+C4` |
| diagonal | 4 | `4K2` |

Their shift support is

```text
pure only                              20
pure and mixed                         57.
```

The parent-word choices of the minimizing lcms are

```text
pure/pure                              13
pure/mixed                             18
mixed/pure                             19
mixed/mixed                            27.
```

The chain-level rank refinement is important:

| module | total rank | off-diagonal projection | diagonal projection |
|---|---:|---:|---:|
| full response image | 153 | 146 | 7 |
| first-seed image | 76 | 74 | 3 |
| canonical complement vectors | 77 | 77 | 7 |

The two coordinate projections need not sum to the total rank because one
source vector can couple both kinds of face.  In particular, the
off-diagonal projection of the complement already has rank `77`.  Therefore
the ordinary Taylor rows detect a full-rank quotient after diagonal rows are
forgotten.  They do **not** reproduce the full boundary: the same `77`
vectors carry a rank-seven diagonal shadow which needs divided-power mates.

This is the sharp answer to whether one Taylor family spans the complement:

```text
as an off-diagonal quotient readout       yes, rank 77;
as a literal full chain family             no, diagonal rank 7 remains;
as one divided Taylor--Spencer family       yes, with two face types.
```

## Why the two seed types do not generate it

The pure and mixed first-face seed families, including every raw operator
containing `(01:11) wedge (07:11)`, have internal rank `76`.  The committed
residual swap, endpoint transpose and tail Weyl do not enlarge that space in
the fixed labelled grade; their nontrivial transports land in conjugate
components.

The complement has both new off-diagonal Taylor pivots and diagonal divided
pivots.  Hence full word transport of the two seeds does not generate all
relative Taylor syzygies in the canonical component.  A shifted component
identification could change this, but that is precisely an additional
constructor, not an existing symmetry.

## Common augmentation module

The smallest response-side common object exposed by the calculation is

\[
              \mathrm{DivTaylorSpencer}_{rep}.        \tag{2}
\]

It contains:

1. ordinary degree-two Taylor cells on the `180` labelled pure/mixed
   matching parents;
2. divided diagonal cells `gamma_2(iota_a)` for the seven diagonal pair
   directions used by the constrained image;
3. the literal `D0`, singleton `D1`, and pair-shadow `D2` faces; and
4. the fixed rank-`153` quotient, with its rank-`76` seed submodule and
   rank-`77` complement.

Its response augmentation is canonical: Taylor boundaries land on the two
matching parents and the divided cells land on the same-cell Hasse face.

There is not yet a common augmentation with the cap complex.  What remains
is a word/fine/repeated-labelled dg-bimodule map

\[
 \mathrm{DivTaylorSpencer}_{rep}
       \longrightarrow C_{AugP2}                     \tag{3}
\]

carrying the relevant rows to the selected `P3+K2` faces and the tied
`r0/E` incidence.  Equation (3) must also supply the absent operation
component `response -> cap`.  The lcm classification neither constructs nor
obstructs that component; it identifies the smallest response domain on
which it must be defined.

## Verification

The full mode performs one modular reconstruction of the already
two-prime-stable complement and then exact combinatorial parent/lcm tests.

```text
python3 computations/verify_h3_order6_taylor_lcm_common_augmentation_gate.py --mode full
python3 computations/verify_h3_order6_taylor_lcm_common_augmentation_gate.py --mode structural
python3 -O computations/verify_h3_order6_taylor_lcm_common_augmentation_gate.py --mode structural
python3 -I -S computations/verify_h3_order6_taylor_lcm_common_augmentation_gate.py --mode structural
```

Frozen ledger SHA-256:

```text
9f7c1d2949410714ed0e4ebaf0c2056bd74d832ed020f8f047b328ecaddfe50d
```

The `153/76/77` ranks are modular.  The parent/lcm topology and diagonal
squarefree-versus-divided distinction are exact combinatorial statements.

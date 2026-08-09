# Exact-ten integral signed quotient: least-extra block 6

This additive audit continues the chart-26 exact-ten frontier beyond blocks
0--5.  It exhausts the supports whose lexicographically least added cell is

\[
                         01;21.
\]

The checker uses the full endpoint-colour fibres on all 105 physical perfect
matchings.  It retains the corrected 16-cell sharp seed, the eleven original
singleton obligations, the exact 1,498 direct repairs through nine added
cells, inclusion minimality, and the cap of exactly ten added cells.

## Exact result

There are exactly **712** inclusion-minimal exact-ten supports in block 6.
For each support the checker forms the integral augmented row lattice

\[
 \widetilde L=\langle(d_j,1),(0,2)\rangle\subseteq\mathbb Z^{252}
 \oplus\mathbb Z,
\]

using FLINT row Hermite normal form.  This is an integral lattice normal
form, not a rational row-echelon reduction.  The exact outcome is

\[
             \boxed{667\text{ odd-sign units}+45\text{ one-class units}.}
\]

There is no consistent all-multiclass third type in this block.  Every odd
case kills the sign generator `(0,1)` in the augmented quotient.  In each
remaining case the checker finds a complete mixed fibre whose terms reduce
to one signed Laurent class with nonzero integer coefficient, and replays
that fibre against the same HNF.  The preferred one-class witnesses have
term-count census

\[
 3:6,\quad4:7,\quad6:3,\quad7:13,\quad8:7,\quad9:2,\quad11:7.
\]

The sorted support/HNF/witness ledger has SHA-256

```text
a8df813c3eeb425d6ea0e48844b9a4ecccd926f11a3c54c5a15a236dc1fbf9fa
```

Together with blocks 0--5 this gives **5,262** exact-ten supports:

\[
             4022\text{ odd-sign units}+1240\text{ one-class units},
\]

still with no third type.  This remains a bounded chart-26 theorem, not an
exhaustion of all least-cell blocks and not an eight-site Krenn proof.

## Reproduction

```sh
uv run python computations/verify_n8_sharp_exact10_augmented_group_block6.py
uv run python -O computations/verify_n8_sharp_exact10_augmented_group_block6.py
```

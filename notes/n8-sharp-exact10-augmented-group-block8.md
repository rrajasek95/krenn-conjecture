# Exact-ten integral signed quotient: least-extra block 8

The exact mate-hypergraph cutoff identifies block 8, with least optional
cell `02;00`, as the next nonempty exact-ten block after block 6; block 7 is
structurally empty.

The checker is a thin parameter wrapper around the block-6 integral-HNF
audit.  It therefore uses the identical corrected sharp seed, full 105-term
endpoint-colour fibres, eleven mate obligations, exact lower-frontier
exclusions, inclusion-minimality tests, and row-Hermite reduction of

\[
 \langle(d_j,1),(0,2)\rangle\subseteq\mathbb Z^{253}.
\]

## Exact result

Block 8 contains exactly **6,316** inclusion-minimal exact-ten supports.  The
complete coefficient split is

\[
             \boxed{4501\text{ odd-sign units}+1815\text{ one-class units}.}
\]

No consistent all-multiclass third type occurs.  The most informative
one-class fibre on each support has term-count census

```text
1:1, 3:79, 4:35, 5:12, 6:1004, 7:129, 8:433,
9:37, 10:17, 11:42, 14:26.
```

The sorted support/HNF/witness ledger has SHA-256

```text
da126cf5bb01a265d18d9445c7e6a21c45fade305ac6dc22e274b83b2cbb6450
```

Cumulatively, blocks 0--8 contain **11,578** certified exact-ten supports:

\[
              8523\text{ odd-sign units}+3055\text{ one-class units}.
\]

The exact cutoff leaves 44 possible nonempty least-cell blocks after block
8.  This remains bounded chart-26 progress, not a complete chart-26 or N=8
proof.

## Reproduction

```sh
uv run python computations/verify_n8_sharp_exact10_augmented_group_block8.py
uv run python -O computations/verify_n8_sharp_exact10_augmented_group_block8.py
```

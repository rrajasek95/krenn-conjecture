# Exact-ten augmented signed quotient: least-extra blocks 0 and 1

The exact-ten counterguard shows that unsigned incidence and alternating
cycles do not determine which coefficient obstruction occurs.  The correct
common invariant is the augmented signed exponent group

\[
 \widetilde G=
 \bigl(\mathbb Z^{252}\oplus\mathbb Z/2\epsilon\bigr)
 \Big/\langle(d_j,\epsilon):j\text{ a mixed binomial fibre}\rangle .
                                                               \tag{1}
\]

This note freezes the first source-faithful exhaustive blocks of the
resulting non-exclusive theorem.  The checker is

```text
computations/verify_n8_sharp_exact10_augmented_group_block01.py
```

## Certificate alternative

For each inclusion-minimal ten-cell repair, enumerate every supported mixed
fibre and every binomial exponent difference `d_j`.

* If the class of `epsilon` is zero in (1), the binomial character has odd
  holonomy.  This is the exact signed-lattice contradiction.
* Otherwise reduce every remaining mixed polynomial in (1).  If some fibre
  has one signed Laurent class with a nonzero integer coefficient, it cannot
  vanish on the support torus.
* A genuine third type would have consistent sign and at least two nonzero
  signed classes in every mixed fibre.

The checker retains the full row-HNF quotient in each certificate digest;
it does not canonicalize through the invalid unsigned incidence signature.
Every sign-unit and one-class witness is independently replayed before the
support enters the ledger.

## Exact block partition

Order all 236 cells outside the corrected 16-cell seed lexicographically and
partition exact-ten supports by their least added cell.

* Block 0, least cell `01;01`, is empty.
* Block 1, least cell `01;02`, has exactly **2,972** supports.

The SAT projection fixes the eleven original mate obligations, blocks the
already certified 46 size-eight and 1,452 size-nine minimal transversals, and
uses the global 26-cell cap.  Every returned model is then rechecked to have
ten additions and to be inclusion-minimal.  Exact support-blocking clauses
exhaust block 1 independently of model order.

The augmented-group outcome is

\[
 \boxed{2028\text{ sign-unit supports}+944\text{ one-class supports},}
                                                               \tag{2}
\]

with no third type.  The frozen ledger hashes the sorted ten-cell support,
the complete augmented HNF, and the exact witness word/class/coefficient.
Its digest is

```text
7bc2097e5c153dea896a8fea37eef725a60f205ad9f7cf0ca40f08f87d1e2826
```

The one-class witnesses are usually genuinely multi-term rather than merely
the already visible singleton obstruction.  Preferring the largest
available one-class fibre on each support gives the exact term-count census

```text
1:1, 3:83, 4:121, 5:22, 6:454, 7:114, 8:139, 9:5, 10:5.
```

This proves the non-exclusive signed theorem on two complete lexicographic
blocks.  It is not yet the whole cap-26 stratum; blocks beginning at later
cells remain.  The stopping rule is sharp: if a later block produces a
consistent quotient with two or more nonzero classes in every fibre, freeze
that exact support immediately as the first third type rather than extending
the two-branch claim.

Reproduce with

```bash
PYTHONPATH=computations .venv/bin/python \
  computations/verify_n8_sharp_exact10_augmented_group_block01.py
```

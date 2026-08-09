# N=8 D1: complete m=10 4+4+2 shadow closure

The exact checker `computations/verify_n8_d1_m10_442_4_full_shadow.py`
expands the smallest palette survivor `442:4` to the complete support
shadow: all 6,561 eight-site words, 729 words on each six-site domain, and
81 residue words.  The monolithic encoding has 1,080,299 variables and
4,266,956 clauses (DIMACS SHA-256
`be2ac535904a94bfcac66f52d412401f9f4e74887844db6e27e02b416cd7b05c`).

The checked proof uses an exact specialization decomposition instead of
asking a native solver to duplicate that four-million-clause input.  The
necessary repair conditions reduce the 7,140 possible pairs of additional
off-Sigma cells to 36.  Every one of those 36 complete ten-cell supports has
a displayed mixed word fibre with exactly one live matching, and that
matching consists entirely of mandatory cells.  Thus `442:4` is rigorously
UNSAT at the complete 8,100-fibre Boolean level; there is no coefficient
problem to derive for it.

The same proof architecture is then tested across the full 265-branch
frontier.  Exactly 22 branches have the transferable `4+4+2` pair form; the
other 243 have three or four additions and are recorded as cardinality
nonmatches.  Across the 22 applicable branches, 157,080 raw pairs reduce to
28,879 repair survivors.  Direct unique-fibre certificates close 28,868.
The remaining 11 specialized complete shadows have checked root unit
propagation conflicts, i.e. deletion-free unit-RUP refutations.  Hence all
22 remaining `4+4+2` branches are empty and the m=10 symbolic frontier falls
from 265 to at most 243, entirely in the `3+3+4`, `3+4+3`, and `4+3+3`
families.

Run the compact exact checker in normal and optimized modes:

```text
python3 computations/verify_n8_d1_m10_442_4_full_shadow.py
python3 -O computations/verify_n8_d1_m10_442_4_full_shadow.py
```

The optional `--build-global-442-4` mode reconstructs and hash-checks the
monolithic CNF; it is memory-intensive and is not needed for the compact
certificate.  Frozen checked-ledger SHA-256:
`dc0c9226c2ab5db5115a8e3258918c49957ff99a132e168dddc9f2c882fa7dac`.

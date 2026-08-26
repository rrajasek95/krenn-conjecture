# Chart 26 / legacy 29: source-faithful mixed cutoff-7 closure

Status: unaudited implementation specification.  This is designed to answer
the actual truncated question

`H0 H1 H2 in I_mix + K^7`

on the fixed chart, not membership in a chosen lower-source component.

## Seed format

`chart26_cutoff7_seed.txt` has:

- magic `KRENN_ANCHOR_K_CUTOFF_SEED_V1`;
- `CUTOFF 7` (retain rows of K-degree 0 through 6);
- the twelve named anchor cell IDs;
- all sixteen site/colour stabilizer actions;
- `TARGET row_hex numerator denominator` for every invariant target-row
  orbit below the cutoff.

The target coefficient is the literal coefficient on an actual monomial
times the row-orbit size.  This is the same exact orbit-average convention
replayed over Q by `audit_degree5_chart26.py`; anchors are not assigned the
value one.

## Required Rust closure

The current `orbit_closure.rs` cannot represent this system: it has one
fixed `DEGREE`, admits only columns of exactly that minimum degree, and emits
only their outputs in that same degree.  A mixed-cutoff port must instead:

1. Start from every `TARGET` row in the seed.
2. For each frontier row, enumerate every literal incident `X_w` source
   column exactly as the current port does.
3. Canonicalize the column under the sixteen actions and retain it iff its
   minimum K-degree is strictly less than `CUTOFF`.
4. Emit all 105 perfect-matching outputs of that source column whose actual
   K-degree is strictly less than `CUTOFF`, canonicalizing rows and retaining
   multiplicity when several outputs have the same representative.
5. Add every new retained row to the frontier and continue to closure.

This single closure automatically includes the previously omitted intrinsic
minimum-degree-five kernels (including differences of duplicate singleton
columns), the 3,274 lower-kernel directions, and any remote lower component
whose higher-degree tail enters the target component.  No preselected Morse
matching or correction column is part of the definition.

## Matrix and exactness contract

- Rows are the closed row orbits of K-degree below seven, ordered by their
  twelve-byte labels.
- Columns are all closed source-column orbits, ordered by the existing Python
  `repr` key; record word and eight multiplier cell IDs.
- An entry is the integer number of retained literal matching outputs in the
  row orbit.  Never convert repeated outputs to a set.
- The target is copied from the seed.  Missing target coordinates are zero.
- Cascading singleton peeling is valid over Q, but its pivot provenance must
  be retained so a positive modular solution can be expanded to literal
  source columns and replayed over Q.
- Run at two primes.  Modular membership is discovery only; replay a positive
  certificate over Q.  A modular nonmembership is nonterminal without an
  exact rational left dual.

Control test: in fixed-degree compatibility mode, the port must still
reproduce the frozen degree-six census
`140578/361406/22 -> 7149/8889` before the mixed-cutoff result is trusted.

The source matrix has total degree twelve, so a successful cutoff-7 identity
is exactly the next ladder statement `H0 H1 H2 in I_mix + K^7`; it is not yet
full localized-chart control.  Cutoffs 8 through 13 would remain.

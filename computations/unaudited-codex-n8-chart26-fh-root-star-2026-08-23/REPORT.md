# Normalized degree-12 pure-product root star

The first target-rooted test for the actual homogeneous pure product `F^h`
is exact and small, but it does not close.  In the implicit degree-12
encoding the row `""` means `t^12`.  Exactly one invariant mixed-column
orbit is incident to it (two actual columns); its 56 output orbits have
degree histogram

```text
degree 0: 1, degree 2: 7, degree 3: 18, degree 4: 30.
```

The root coefficient in this column is two.  Among its 56 rows, the actual
`F^h` target meets exactly `""` and `75c6`, each with coefficient one.
The two-row functional

```text
lambda("")       =  1
lambda("0576cc") = -2
```

annihilates the root column and pairs to one with `F^h`; the repair row is
target-free.  This is the smallest local target dual.

The complete incident scan of that selected functional has 10 invariant
column orbits, of which nine pair nontrivially.  The lex-first killing cell
is the literal word `00000012` with multiplier `07`, i.e.
`x_01^(2,1)`.  It contains `0576cc` with coefficient one and pairs to
`-2`.  Its actual orbit mate is word `00012000` with multiplier `05`.

Thus the two-row target class survives only the root star; it does not
survive the next incident boundary.  No closure of the nine violating
columns was attempted, so this is neither membership nor nonmembership of
`F^h` in the full homogeneous mixed ideal.

Reproduce with:

```sh
python3 computations/unaudited-codex-n8-chart26-fh-root-star-2026-08-23/audit_fh_root_star.py --check-results
python3 -O computations/unaudited-codex-n8-chart26-fh-root-star-2026-08-23/audit_fh_root_star.py --check-results
python3 -I -S computations/unaudited-codex-n8-chart26-fh-root-star-2026-08-23/audit_fh_root_star.py --check-results
```

Logical SHA: `57a5bb5aa092a6edb79644be16f8b07908f8533b6c59e33e1ef4727771b6aad1`.

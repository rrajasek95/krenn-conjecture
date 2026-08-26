# Chart-26 degree-eight factorization threshold

Status: **UNAUDITED exact bounded structural result**.

## Verdict

The proposed threshold is true only in its target-specific filtered form.
At total source degree eight, a column whose encoded-`y` multiplier has
length below four contains at least one `t`; it is therefore `t` times a
degree-seven column.  The frozen degree-seven target-rooted closure has
10,411 columns, all 10,411 private-row pivots, and kernel dimension zero.
Consequently no `|u_y|<4` column can produce the requested target pivot.

This is not a factorization theorem.  The chart-26 decorated source already
has a nonzero exchange at multiplier length one:

```text
M = 0948c6f4,  N = 0948c6f5,  lcm = 0948c6f4f5.
```

The two raw perfect matchings have the same physical edges
`02|13|45|67`; only the colour decoration on edge `67` changes.  Their
degree-five S-polynomial has the frozen nonzero 180-term remainder.  Thus
“`|u|<4` implies peelable by matching factorization” is false even before
the degree-eight target is introduced.

The sharpened unique-perfect-matching selection is also false, even after
restricting to target-derived decorated multipliers and requiring literal
word compatibility.  Among all target submonomials through `|U|=5`, the
numbers admitting at least one compatible/private provider are:

| `|U|` | compatible multipliers | with a private provider |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 7 | 6 |
| 2 | 23 | 17 |
| 3 | 48 | 31 |
| 4 | 70 | 40 |
| 5 | 71 | 36 |

The smallest counterexample is the single decorated cell
`U=01=A_01[0,1]`.  It has six literal compatible providers and none has a
unique leading-PM divisor.  For example,

```text
word 10012000: M = 0376d5ea, target incident term 2049;
word 01012000: N = 0176d5ea.
```

The multiplier supplies `01`, so `N | M*U`.  The two matchings have the same
physical skeleton `01|23|46|57`; only the decoration of edge `01` changes.
The other five compatible providers fail by the same exact label-only
mechanism.  In total 89 target-derived multipliers through degree five lack
any compatible private provider.  Thus neither Kotzig uniqueness nor a
contracted-forest choice proves the d6--d9 peel in the decorated source.

## Exact degree-eight seed census

The new `t`-free head consists of the 205 literal `|u_y|=4` seed columns
from the authoritative degree-eight incidence file.  There is no direct
`y^8` target row.

For the leading row of each seed, every alternative original leading
divisor was enumerated.  This gives 95 exchange pairs, all 95 physically
`LABEL_ONLY`; all 95 have a nonzero `y^7*t` or `y^6*t^2` target-tail
coefficient.

The complete one-hop top-incidence audit then uses every degree-four
matching term of all 205 seed providers, not only each provider's leading
term.  It finds:

| physical exchange type | exits | exits feeding a shorter target tail |
|---|---:|---:|
| decorated `LABEL_ONLY` | 106 | 106 |
| `C4` | 54 | 54 |
| `C6` | 0 | 0 |
| `C8` | 0 | 0 |

Hence the first source-labelled exchange packet is not classified solely
by physical `C4/C6/C8`: decorated same-matching relabellings are
load-bearing.  Among genuine physical cycles, only `C4` directly feeds the
`y^10*t^2` shorter tails in this complete first-shell census.  A `C6` may
occur later in the transitive inverse-incidence closure, but it is not a
direct shorter-tail feeder; no such later claim is made here.

One literal C4 feeder is

```text
word 10012000, term 306c76cc, multiplier 011120f8
word 01012012, lead 0176ccf8, multiplier 1120306c
shorter target row 0111202049f8, coefficient 1.
```

The two matchings share exact decorated edges `23` and `45`; the other four
sites form a C4.

## Why C8 is impossible

The target monomial

```text
0111202020494f4f50f8
```

contains no coordinate incident to site 5.  Thus every target-rooted
multiplier `u` contains no site-5 cell.  A product `M*u` contains exactly
the unique site-5 cell of the perfect matching `M`.  Any alternative
perfect-matching divisor `N` of that product must use that same decorated
cell.  Therefore `M` and `N` agree on a physical edge incident to site 5
and cannot differ on all eight vertices.  A C8 symmetric difference is
impossible.  The checker verifies this for every enumerated exit.

This invariant also propagates to later inverse-incidence columns: after a
top exchange the complementary multiplier still contains no site-5 cell.
It excludes C8 throughout the target-rooted top closure, although it does
not by itself exclude later C6 exchanges.

## Scope and replay

The census covers all 205 literal `t`-free target-rooted seeds, every
degree-four matching term in those provider polynomials, and every
alternative original leading divisor of the resulting top rows.  It is not
the transitive degree-eight closure or a membership computation.

```sh
python3 computations/unaudited-codex-n8-orbit26-d8-factorization-threshold-2026-08-23/audit_d8_factorization_threshold.py --write-results
python3 computations/unaudited-codex-n8-orbit26-d8-factorization-threshold-2026-08-23/audit_d8_factorization_threshold.py --check-results
python3 -O computations/unaudited-codex-n8-orbit26-d8-factorization-threshold-2026-08-23/audit_d8_factorization_threshold.py --check-results
python3 -I -S computations/unaudited-codex-n8-orbit26-d8-factorization-threshold-2026-08-23/audit_d8_factorization_threshold.py --check-results
```

Hostile `--mutate` must fail.  Logical digest:
`f8281f05ec1e328283577dfa999127f7e8196516965bf7b6430b911f60abbd68`.

# N8 chart-26: first possible target obstruction after degree 7

## Result

For the frozen normalized target

```text
C10 = 0111202020494f4f50f8 * t^2
```

the target is exact standard through total degree 7.  The first degree at
which a genuinely new top-kernel test is possible is total degree 8, and the
first filtration slice to test is `y^7*t`.

This is a theorem about the first *possible* obstruction.  It is not a
degree-8 membership/nonmembership result.

## Structural proof

Every target divisor misses physical site 5.  Every `y^4` term of an
original normalized mixed generator is a decorated perfect matching and
therefore uses all eight sites.  Hence no t-free source term can divide any
t-free target divisor, at any degree in this target-rooted chart.

A one-t target divisor can be reached only through a `y^3*t` source term
whose omitted normalized support edge contains site 5.  The canonical first
provider is

```text
d7: q = 0111202049f8, code 2327,
    source term 2049f8 * t, multiplier 011120,
    omitted support edge A25[00].

d8: q = 011120202049f8, code 2327,
    source term 2049f8 * t, multiplier 01112020,
    omitted support edge A25[00].
```

At degree 7 these raw incidences do not create a class.  The independent
target-rooted computation has 10,411 columns and 605,815 top `y^7` rows;
all columns singleton-peel, so the head kernel is zero.  Every remaining
degree-7 column is `t` times the exact-standard degree-6 module.

Degree 8 is the first universal top-syzygy degree: for degree-4 top forms
`g4,h4`, the source-labelled Koszul relation

```text
h4*g - g4*h
```

cancels in `y^8`; its first Bockstein is

```text
t * (h4*g3 - g4*h3),
```

which lies in `y^7*t`.  Thus `y^7*t` is the first new slice.  The
`y^6*t^2` slice is the next boundary and should be inspected only after the
first Bockstein.

## Exact degree-8 seed census

There are exactly 205 primitive columns with t-free degree-4 multipliers:

| target slice | primitive columns | top rows | multifactor top rows | physical exchange pairs | decoration-only pairs |
|---|---:|---:|---:|---|---:|
| `y^7*t` | 61 | 4,136 | 1,173 | `C4`: 408 | 1,567 |
| `y^6*t^2` | 144 | 8,822 | 2,992 | `C4`: 1,526; `C6`: 184 | 4,020 |
| union | 205 | 12,958 | 4,165 | `C4`: 1,934; `C6`: 184 | 5,587 |

Every one of the 12,958 top rows contains exactly one cell incident to site
5.  Every alternative source matching must reuse that decorated cell.
Consequently neither a physical `C8` exchange nor `C4+C4` can occur in the
target-rooted seed packet.  In particular, the first `y^7*t` test reduces to
`C4` matching exchanges plus same-physical-matching decoration swaps; `C6`
appears only in the lower `y^6*t^2` slice.

## Provenance

- Structural checker: `audit_first_possible_degree.py`.
- Exact degree-7 authority:
  `../unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_y10_d7_staged_blocks.json`,
  logical digest `30e98f20fd4f5f7a08b43295cf6eb93b46cefc96a232dc44ed0a03c72538251a`,
  file SHA-256 `90a107b47957ec102a74994fd460a861b66e0c8e6aaffbc3e546919f0ecda2f4`.
- Structural checker logical digest:
  `5f010bd72d286423464cefe6b8c78bee6f212167b52827f6f29372eaef1a5c12`.

The exchange-pair counts are incidence counts inside the target-rooted seed
top rows, not orbit counts and not ranks.

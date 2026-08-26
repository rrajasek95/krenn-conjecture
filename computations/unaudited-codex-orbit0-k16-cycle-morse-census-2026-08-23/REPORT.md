# K16 literal cycle-Morse census

## Verdict

The proposed physical-perfect-matching pivot gives a strict cycle-count descent on
`751,988 / 1,848,174` frozen K16 target `H`-orbits, but it is not a global
contraction: `1,096,186` target orbits are unpivotable by this criterion.

This is an exact exhaustive streaming census of the frozen weighted DAFSA.  It is
only a literal support-pivot test; no closure, incidence-rank computation, or
inference about the full K16 ideal is made.

## Criterion and descent lemma

For a target row, form its 2-regular graph on the 24 coloured ports.  A row is
declared pivotable when this graph contains a physical perfect matching on the
eight sites whose four edges:

1. lie in four distinct cycles of the 2-regular graph; and
2. have a mixed endpoint-colour word.

Deleting these four edges cuts four distinct cycles into four paths.  Any other
perfect-matching completion must join at least two of those paths, and therefore
has strictly fewer cycles.  Thus every reported witness is a source-faithful
strict Morse descent.

## Exact census

| cycles | target orbits | pivotable | unpivotable |
|---:|---:|---:|---:|
| 2 | 249,824 | 0 | 249,824 |
| 3 | 639,996 | 0 | 639,996 |
| 4 | 572,891 | 371,376 | 201,515 |
| 5 | 276,757 | 271,934 | 4,823 |
| 6 | 86,787 | 86,759 | 28 |
| 7 | 18,849 | 18,849 | 0 |
| 8 | 2,768 | 2,768 | 0 |
| 9 | 296 | 296 | 0 |
| 10 | 6 | 6 | 0 |
| **total** | **1,848,174** | **751,988** | **1,096,186** |

The unpivotable split is exact:

- `889,820` rows have fewer than four cycles;
- `206,366` have at least four cycles but no physical perfect matching across
  four distinct cycles;
- no row failed merely because all eligible perfect matchings had pure endpoint
  colour words.

The result JSON contains the complete 120-cycle-partition ledger.  In particular,
every row with at least seven cycles is pivotable.  At six cycles only 28 rows
remain; they all have partition `2,2,2,2,4,12` and form the smallest high-cycle
boundary exposed by this test.

Stored-orbit coefficient masses are also recorded exactly: total signed mass
`118,692,864`, unpivotable signed mass `54,680,640`; total absolute mass
`1,134,990,336`, unpivotable absolute mass `658,170,240`.

## Literal controls

The lexicographically first blocker is

```
09090d152135484c515e60747d7d93c0cacecedce2f3f7fb
```

with coefficient `-384`, cycle partition `2,2,2,18`, and no physical perfect
matching across four distinct cycles.

The first positive witness is

```
row        09090d0d1821484c4c5160627d96c3cacacee0e3f3f7f7fb
word       00001100
multiplier 090d0d18214c4c5160627d96c3cacee0e3f7f7fb
cells      0948caf3
```

The independent verifier checks the aggregate ledger, replays both literal
controls, and confirms that the witness cells form a physical perfect matching
in distinct cycles with a mixed word.  Standard, optimized, and isolated modes
agree.  A hostile mutation of the first input row is rejected.

## Reproduction

```sh
rustc -O census_k16_cycle_morse.rs -o census_k16_cycle_morse
./census_k16_cycle_morse
python3 verify_cycle_morse_census.py
python3 -O verify_cycle_morse_census.py
python3 -I -S verify_cycle_morse_census.py
python3 verify_cycle_morse_census.py --mutate  # must fail
```

Canonical logical digest of the result JSON:

`ba1e0e39def4378e5d0b2da7a8600a6d5486d44b0bfb23a264aadf65449612af`


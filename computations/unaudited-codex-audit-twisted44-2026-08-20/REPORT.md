# Independent audit: fixed twisted-4+4 full-exactness obstruction

## Verdict

**PASS for the fixed endpoint-ordered representative and its explicit
target-preserving symmetry orbit, with one required certificate-metadata
correction.**  The 21 coefficient equations give a division-free triangular
contradiction, and the stored integer multipliers give a Nullstellensatz
identity `1` after the producer's canonical per-generator sign normalization.
Both arguments work over every field.

This does **not** prove that every binary source with the twisted-4+4
combinatorial support is in the audited orbit.  No W33 orbit-classification
claim was imported.

The metadata correction is precise: `certificate.json` says

```text
sum(multiplier_i * raw_word_equation_i) = 1,
```

but with the standard raw convention `raw_word_equation = H_w - delta_w`,
that sum has 346 nonzero terms and constant `-1`, rather than being `1`
(residual SHA-256
`6035a83e546d2028761db954ba1fcdfbae2b4dfee79c4464d491aec933adaf73`).
The stored identity is exactly `1` when each raw equation is first multiplied
by the unique sign making its smallest exponent-vector monomial positive.
The theorem is unaffected because multiplying a generator by `-1` does not
change its ideal.  Before promotion, the certificate should record these 21
signs or absorb them into its multipliers.

## Independence and reconstruction

The audit read the binding 33-item hazards ledger.  Its only producer inputs
were `REPORT.md` and `certificate.json`; no producer Python, polynomial code,
or amplitude routine was imported or copied.

`independent_check.py` reconstructs the 105 perfect matchings as the four-edge
subsets of the 28 edges of `K_8` whose vertex degrees are all one.  This is
neither a first-vertex recursion nor a subset DP.  Polynomials are represented
by integer coefficient maps on exponent vectors.  All 21 cited equations are
expanded directly from the matching definition.

The fixed binary cells, with endpoint order always `(smaller vertex, larger
vertex)`, are

```text
A01[0,0] = A23[0,0] = A45[0,0] = A67[0,0] =  1
A03[1,1] = A12[1,1] = A47[1,1] = A56[1,1] =  1
A04[0,1] = A05[1,0] =  1
A17[0,1] = A34[1,0] = -1
```

Every unlisted binary cell is zero and all 140 cells containing color `2`
are independent variables.  Direct expansion verifies all 256 binary words.
Transposing every endpoint lookup makes four words fail (first:
`00001111`, amplitude `1` instead of `0`), so the endpoint-order control is
live.  Changing `A34[1,0]` from `-1` to `1` makes `11110000` have amplitude
`2`, so the fixed-sign control is live.

## The triangular contradiction

Canonical signs are used in the following table only to make the displayed
pivots uniform; their signs are units and no division is used.

The twelve literal rows are:

| word | resulting zero |
|---|---|
| `20000000` | `x0120` |
| `21000000` | `x0121` |
| `20010111` | `x0220` |
| `20110111` | `x0221` |
| `21100000` | `x0320` |
| `21111111` | `x0321` |
| `20000111` | `x0420` |
| `21110100` | `x0521` |
| `20000001` | `x0620` |
| `20000011` | `x0621` |
| `21110110` | `x0720` |
| `21110111` | `x0721` |

The independently reconstructed row for `21110000` is

```text
x0321 - x0520 = 0,
```

so it supplies the thirteenth zero, `x0520=0`.

Reducing the next seven raw matching equations by those thirteen literal
zeros gives:

| word | profile | reduced row |
|---|---:|---|
| `22000000` | `(6,2)` | ` x0122` |
| `20210111` | `(4,2,2)` | `-x0222` |
| `21120000` | `(4,2,2)` | ` x0322` |
| `20002111` | `(3,3,2)` | `-x0422` |
| `21110200` | `(3,3,2)` | ` x0522` |
| `20000021` | `(5,2,1)` | `-x0622` |
| `21110112` | `(5,2,1)` | ` x0722` |

Thus the two and only two `(3,3,2)` rows enter at the fourth and fifth
pure-edge eliminations: `20002111` kills `x0422`, and `21110200` kills
`x0522`.  This pinpoints why the four-parameter level-4 family survives until
full exactness is imposed.

Every matching monomial in `H_22222222` contains exactly one of
`x0122,...,x0722`, because every perfect matching has exactly one edge at
vertex 0.  Hence that amplitude is zero, contradicting its required target
value one.  Equivalently, the canonically signed pure generator reduces to
the unit `1`.

## Integer certificate and controls

Let `f_w=H_w-delta_w`, and let `epsilon_w` be the canonical sign described
above.  Independent expansion verifies exactly

```text
sum_w multiplier_w * epsilon_w * f_w = 1 in Z[x_1,...,x_140].
```

The positive-sign generator IDs are

```text
2163 2169 2209 2225 2335 2629 2749 2799 2824 2859 3127
```

and the negative-sign IDs are

```text
2164 2166 2171 2495 2805 2807 2808 2809 2813 3773
```

The certificate has 21 nonzero multipliers and 781 multiplier monomials.
Flipping the normalized pure generator sign leaves a 106-term nonidentity;
deleting its multiplier leaves a 105-term nonidentity.  Replacing the pure
raw equation `H-1` by `H+1` also leaves 106 terms.  Declared and executed
control manifests agree exactly.  Reduction modulo `2,3,5,7` was checked,
although the integer identity already proves the result after base change to
every field.  The triangular proof independently has only `+/-1` pivots and
is likewise characteristic-free.

Frozen digests are:

| object | SHA-256 |
|---|---|
| producer certificate input | `50eb546c0e6d0382e3376204aa82788725994605a9c3152c0a11d57d7b46eba5` |
| independently rebuilt source/matchings | `6916c2fa2fbefe6878c3158d67933d3290f16ff5ca041bc80f126cf3a2314a75` |
| 21 raw equations | `44d0b3e832f0208756eb103c12ad9e0c1fc70f8f87e01037612a2c9192f2fb74` |
| 21 sign-normalized equations | `f935a5361c80a26315614ac9ed29baa1504e7eb99da953f693dda5989c62bb22` |
| canonical result payload | `ccdfb6368d75992bb1df4e9256f213502a37d62d54333c271259a7a6748e8954` |

## Exact transport scope

For nonzero diagonal site-color parameters, define

```text
(g A)_uv[a,b] = lambda_(u,a) lambda_(v,b) A_uv[a,b].
```

Every matching contributing to word `w` uses every vertex once, so term by
term

```text
H_w(g A) = (product_v lambda_(v,w_v)) H_w(A).
```

Within diagonal gauges, this action preserves the normalized ternary target
**if and only if**

```text
product_v lambda_(v,c) = 1  for c=0,1,2.
```

The checker verifies the amplitude law at a nontrivial rational gauge and
arbitrary rational source point for all 6,561 words.  For a normalized binary
orbit member, the analogous product conditions for colors `0,1` are forced
by its two pure equations; setting every `lambda_(v,2)=1` extends its inverse
gauge to a target-preserving ternary gauge.

All 40,320 site permutations preserve the target.  When relabeling makes an
edge's canonical order reverse, its cell is transposed; omitting this is the
endpoint-order error detected above.  All six **global** palette permutations
also preserve the ternary target.  If the statement keeps the distinguished
binary palette literally equal to `{0,1}`, only its two-element stabilizer
(`identity` and `0<->1`) acts internally; the other four permutations give
the same theorem relabelled to another binary palette.

Consequently the proved transport is the orbit under target-preserving
diagonal gauges, site permutations, and global palette permutations.  It
does not cover independent palette permutations at different sites,
non-diagonal color mixing, or any twisted-4+4 support member lacking an
explicit orbit map.

## Reproduction

All three modes pass with the same frozen result digest:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  computations/unaudited-codex-audit-twisted44-2026-08-20/independent_check.py \
  --write-results

PYTHONDONTWRITEBYTECODE=1 python3 -O \
  computations/unaudited-codex-audit-twisted44-2026-08-20/independent_check.py

PYTHONDONTWRITEBYTECODE=1 python3 -I -S \
  computations/unaudited-codex-audit-twisted44-2026-08-20/independent_check.py
```

Artifacts:

- `independent_check.py` — independent source/equation/certificate checker;
- `results.json` — triangular row maps, controls, scope, and frozen digests.

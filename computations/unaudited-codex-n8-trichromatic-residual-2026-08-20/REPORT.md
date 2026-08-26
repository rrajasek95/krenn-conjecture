# N=8 trichromatic residual audit

Status: **UNAUDITED exact finite/source-support lemmas.** No certified or
spine file was changed. This lane does not prove universal N=8 nonexistence.

## Headline

The 1,680 full-only `(3,3,2)` rows have a useful exact organization relative
to every fixed cap pair, and they give a cheap characteristic-independent
support filter:

> **NO-SINGLETON-332.** Over a field (indeed an integral domain), the live
> support of a fully exact eight-site source cannot give any `(3,3,2)` word
> exactly one supported perfect matching.

The proof is literal: such a zero-target amplitude would be the product of
four nonzero source cells and therefore could not vanish. This conclusion is
not available from X4 alone because `(3,3,2)` is exactly the omitted shell.

This filter completely closes two fixed open supports against full exactness:

* W40 has only four supported `(3,3,2)` words. Three are singleton unit
  monomials, so any one of their equations is already a Laurent unit
  certificate against full exactness on the 20-cell open support.
* W25 has only 25 supported `(3,3,2)` words, of which 20 are singleton unit
  monomials. Thus its fixed open support is independently impossible as a
  full source, in addition to the known fact that its pinned point fails X4.

The fixed twisted-4+4 triangular contradiction was also rebuilt. Exactly two
of its seven late unit pivots are full-only rows: `20002111` and `21110200`.

## 1. Exact 510-packet organization

Fix a cap pair `p,q`, and write `z` for the six residual colours. Partition
the 729 residual words by their multiplicity profile. The 219 words with a
colour occurring at least four times are X4-complete: all nine endpoint
extensions `(i,j,z)` are already X4 rows.

The other 510 residual words carry the 1,680 missing coefficients exactly
once:

| residual profile | packets | missing endpoint slots per packet | rows |
|---|---:|---:|---:|
| `(3,3,0)` | 60 | 1 | 60 |
| `(3,2,1)` | 360 | 3 | 1,080 |
| `(2,2,2)` | 90 | 6 | 540 |
| **total** | **510** | | **1,680** |

For every residual word—not only the 219 X4-complete words—the raw matching
partition gives the linear-in-`K` slice identity

```text
delta_z(K)
 = H6(z) <K,A_pq>
   + sum_{a<b in U} H4(z|U\{a,b}) R_ab(K)[z_a,z_b].
```

Indeed a perfect matching either contains `pq`, or pairs `p,q` to one unique
unordered residual pair `a,b`, in one of the two endpoint-ordered ways. Full
exactness extends this identity from the 219 X4-complete packets to all 729;
the table is the exact complement. The checker verifies the literal formula
on all `28*1680=47,040` central pair/word instances for each of W40 and W25.

This aligns the full residual directly with the response-map/blocker attack.
It is an organization of the missing equations, not yet a proof that all 728
carrier failures are incompatible with them.

## 2. W40: a one-row Laurent obstruction

On the globally classified W40 20-cell support, raw enumeration finds only:

```text
H_01110222 = x06_02 x12_11 x34_10 x57_22,

H_10210021 =
  (x03_11 x45_00 + x05_10 x34_10)
  (x12_02 x67_21 + x17_01 x26_22),

H_12221000 = x05_10 x13_22 x24_21 x67_00,

H_20002111 = x04_22 x17_01 x23_00 x56_11.
```

Every other `(3,3,2)` amplitude vanishes by support. The three displayed
monomials are units after localizing at the 20 named support cells. Thus, for
example,

```text
(x06_02 x12_11 x34_10 x57_22)^-1 H_01110222 = 1
```

is a one-generator Laurent certificate that the full source locus is empty
on this open support, over every field.

The four-term row is already forced to zero by X4. Directly,

```text
H_10210000
 = x12_02 x67_00 (x03_11 x45_00 + x05_10 x34_10),
```

and the prefactor is a unit on the stratum. At the integral W40 point the
only central failures are exactly

```text
H_01110222 = 1,
H_12221000 = 1,
H_20002111 = -1.
```

Relative to pair `67`, all three are least-frequency diagonal coefficients
in three residual `(3,2,1)` packets, one for each palette colour. This is the
precise way in which the central shell cuts W40; it does not conflict with
W40's uniform active response-star cap.

## 3. W25 lower control

A fresh rational replay of the pinned W25-F8 point finds precisely 25
supported central words. All 25 amplitudes are nonzero: 20 have one live
matching and five have two live matchings. Consequently the fixed open W25
support violates NO-SINGLETON-332 in 20 separate rows. The complete word,
value, and matching-count ledger is in `results.json`.

W25 remains only a lower control: its pinned point also fails 78 X4 rows, so
this calculation neither constructs nor rules out a general all-blocked X4
source.

## 4. Twisted-4+4 pivot audit

The script independently restates the twelve fixed binary cells and treats
all 140 colour-2 cells as variables. It rebuilds the cited triangular rows
from the 105 raw matchings:

1. Twelve literal unit rows kill twelve variables.
2. `H_21110000 = x0321-x0520` kills `x0520`.
3. Seven further rows kill `x0122,...,x0722` with unit pivots.
4. Exactly the two rows
   `20002111 -> -x0422` and `21110200 -> x0522`
   have profile `(3,3,2)`.
5. `H_22222222-1` then reduces to `-1`.

This confirms the division-free triangular proof over every field. It does
not enlarge the already stated orbit scope of the twisted-4+4 theorem and
does not repair the separate sign-metadata issue in its stored polynomial
certificate.

## 5. Controls and reproduction

The checker uses an explicit 105-matching engine and an independent subset-DP
hafnian engine. It retains endpoint order at every reversed edge. Deliberately
omitting the required transpose changes 86 W40 and 302 W25 slice instances;
flipping W40's forced `x34_10` sign also changes the central failure census.
All declared controls executed.

Standard, optimized, and isolated/no-site runs give the same result digest:

```text
04e048265dbef8cb58c961b9b963fae006cf7e107b1a7796e6583f041efa780c
```

Replay from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  computations/unaudited-codex-n8-trichromatic-residual-2026-08-20/audit_trichromatic_residual.py --write-results

PYTHONDONTWRITEBYTECODE=1 python3 -O \
  computations/unaudited-codex-n8-trichromatic-residual-2026-08-20/audit_trichromatic_residual.py

PYTHONDONTWRITEBYTECODE=1 python3 -I -S \
  computations/unaudited-codex-n8-trichromatic-residual-2026-08-20/audit_trichromatic_residual.py
```

Artifacts:

* `audit_trichromatic_residual.py` — independent raw checker;
* `results.json` — frozen exact ledgers, controls, and hashes.

## 6. Honest support-filter survivor census

The pre-existing `m=25,...,28` material uses two different models. The
diagonal-support SAT family does **not** align with this residual: every
supported diagonal matching pairs equal word colours, so every colour class
has even cardinality. It has zero live `(3,3,2)` occurrences even on full
diagonal support, making NO-SINGLETON-332 vacuous there.

The W8/W15 residual templates do use the full endpoint-ordered `3x3` cell
model. I restated their four named supports and checked the honest elementary
minimum-source filters with two independent fibre engines. All four survive:

| live edge blocks `m` | occupied cells `sigma` | positive balance `mu` | pure fibres | minimum `(3,3,2)` fibre |
|---:|---:|---:|---|---:|
| 25 | 129 | `(21,14,13)` | `(9,10,9)` | 8 |
| 26 | 138 | `(15,14,15)` | `(12,13,12)` | 11 |
| 27 | 147 | `(15,14,22)` | `(13,14,14)` | 12 |
| 28 | 156 | `(15,14,15)` | `(18,18,18)` | 16 |

Explicit positive integer weights certify BAL exactly at all 24 site-colour
ports. Every mixed fibre—not only the central shell—has size different from
one. Standard, optimized, and isolated runs agree on digest

```text
01d397a8a666db934903813c593bf9852bd34ddb90b2376d4933bde577c30fe8
```

Replay:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  computations/unaudited-codex-n8-trichromatic-residual-2026-08-20/audit_support_survivors.py --write-results
```

This is a useful negative conclusion: positive balance, pure liveness, and
even full mixed-singleton-freeness do not make the support residual small.
Coefficient-level X4 equations and carrier conditions are indispensable.
These four objects are support controls, not X4 points or exact sources;
`m` counts live edge blocks, while global minimum support concerns `sigma`.

Artifacts added by this census are `audit_support_survivors.py` and
`results_support_survivors.json`.

## 7. Full 129-cell `m=25` support: five-row X4 Laurent closure

The support-only survivor verdict above is now sharpened decisively for the
smallest named endpoint-cell support.  Its **open coefficient locus is empty
already under the mixed X4 equations**.  This is a statement about all 129
nonzero cells, not the earlier scalar-block/rank-one ansatz.

There are 4,878 mixed X4 generators (and three pure rows).  Every X4 fibre
has at least eight live matchings, so the previously proposed
binomial/trinomial Laurent-lattice first step is genuinely absent.  The
replacement is a matched five-row certificate at the unique site with only
two full neighbours, site 6.

Use the fixed tuple `(y5,y7)=(0,0)` and abbreviate

```text
a_t = x56_0t,              b_t = x67_t0,
D = a_0 b_1 - a_1 b_0,
alpha = a_2 b_1 - a_1 b_2,
beta  = a_0 b_2 - a_2 b_0.
```

The three mixed X4 words

```text
00001000,  00001010,  00001020
```

vary only the site-6 colour.  Edge `(0,6)` fires only in the last row, and
raw matching partition gives

```text
D H_00001020 - alpha H_00001000 - beta H_00001010 = D U06,

U06 = x06_02 x13_00 x25_00 x47_10.
```

This identity was expanded literally as a sparse polynomial from the 105
perfect matchings; its residual has zero terms.  Since all three `H` rows
vanish and `U06` is a monomial in live cells, it forces `D=0` in the Laurent
localization.

Now use the two mixed X4 words

```text
10200000,  10200010.
```

Only edge `(2,6)` fires in the second.  With `Q26` the literal cofactor
polynomial for the `67` slice,

```text
a_0 H_10200010 - a_1 H_10200000 = D Q26 + U26,

U26 = x56_00 x26_21 x07_10 x13_00 x45_00.
```

Combining, without division, gives the five-generator certificate

```text
U06 (a_0 H_10200010 - a_1 H_10200000)
 - Q26 (D H_00001020 - alpha H_00001000 - beta H_00001010)
 = U06 U26.
```

The right side is the product of nine live cells (with `x13_00` appearing
twice), hence a unit after localizing at the 129 support variables.  This
proves the open `m=25` X4 locus empty over every field, indeed every integral
domain.  There is consequently no point or stratum on which to test the 728
star/triangle carriers.

The script finds the `(0,6)` minor packet and `(2,6)` unit packet not merely
at `(0,0)`, but at all nine `(y5,y7)` tuples.  It stores every word, row term
count, determinant, singleton prefactor, and exact sparse-identity verdict.
The five-row certificate supersedes the interim scalar-block computation:
the latter did give a unit ideal inside an 18-variable ansatz, but it is no
longer load-bearing and must not be described as closing the 129-cell locus.

For completeness, that superseded interim imposed one scalar on every full
`3x3` block, kept the twelve singleton scalars, and used vertex gauge to set
the seven edges `0v` to one.  The 4,878 mixed rows deduplicated to 201
polynomials in 18 Laurent variables.  Adding a Rabinowitsch inverse for all
18 variables and the three pure amplitudes gave Singular `slimgb = [1]` over
`Q`, with the same verdict modulo 32003.  No explicit multiplier certificate
was extracted.  This was an exact subfamily no-go, never a proof that X4
forced the ansatz; the five-row raw certificate is the replacement.

### Controls and replay

The checker restates the raw 28-entry template with bit `3*a+b`, where `a`
belongs to the smaller endpoint.  Transposing that convention changes nine
of the twelve directed singleton cells, including both load-bearing cells
`x06_02` and `x26_21`.  All nine deliberately sign-mutated Cramer identities
leave nonzero residuals.  Audit conditions use explicit runtime checks, not
Python `assert`, so optimized replay is load-bearing.

Standard, optimized, and isolated/no-site runs give the same core digest:

```text
287f4a6cfd1f0592cbd26eabf429cb6cb17ada345f9fa3b8ac00997988eee9cc
```

Replay:

```sh
python3 computations/unaudited-codex-n8-trichromatic-residual-2026-08-20/audit_m25_x4_closure.py
python3 -O computations/unaudited-codex-n8-trichromatic-residual-2026-08-20/audit_m25_x4_closure.py
python3 -I -S computations/unaudited-codex-n8-trichromatic-residual-2026-08-20/audit_m25_x4_closure.py
```

Artifacts are `audit_m25_x4_closure.py` and
`results_m25_x4_closure.json`.

### Exact transport test to `m=26,27,28`

The same checker exhausts every site, incident singleton target, and all
`3^7` fixed colours on the other sites.  It asks for exactly the support
conditions used above: a mixed-X4 three-row packet, one incident singleton
spike, a monomial nonzero spike cofactor, exactly two effective full-neighbour
cofactors, and a second packet with a different spike colour at the same
effective-neighbour/endpoint-colour key.

At `m=25` this finds 248 two-column packets and 3,856 ordered spike-packet
pairs across all nine keys, providing a positive control.  At each of
`m=26,27,28` it finds **zero** two-column packets, even before pairing.  The
minimum full-block site degrees rise from 2 at `m=25` to 3, 3, and 4; the
exhaustive cofactor test confirms that no recolouring or site relabelling
makes the extra columns disappear.

This is only a rigorous non-transport verdict.  It does not say that the
larger supports contain X4 points.  Their next structured layer must handle
three- or four-column slice matrices rather than reusing the five-row
two-column Cramer certificate.

## Scope

NO-SINGLETON-332 is a necessary support condition, not sufficient for full
exactness. A word with two or more live matchings can still fail because its
terms do not cancel. Conversely, passing the filter does not imply that
coefficients can be chosen. No conclusion is inferred from absence of a
search hit.  The new X4 conclusion is exactly the named 129-cell `m=25` open
support; no universal carrier-evasive stratum and no `m=26,27,28` coefficient
locus is claimed closed here.

# Adversarial `X4`-to-cap falsifier lane

Status: **UNAUDITED EXACT BOUNDED EXCLUSIONS; NO `X4` CARRIER-EVASIVE
SOURCE WAS CONSTRUCTED.**  The universal `X4`-to-cap statement remains open.
No certified or spine file was edited.

## Headline

This lane searched away from W40's audited local gauge component and reached
two exact bounded terminals.

1. The 19,528 pinned W33 rational binary records have only 30 compatible
   ternary occupied-support strata after exact diagonal-layer joining.  Every
   one of those strata contains 7--10 mixed `X4` words with exactly one live
   perfect matching.  The corresponding raw equation is a nonzero Laurent
   monomial on the open support, so **all 30 open strata are `X4`-empty over
   every field**, independently of the pinned coefficients.
2. Up to conjugacy, exactly 12 one-generator fixed loci for the covariant
   `S8 x S3` action have at most 33 endpoint-cell orbits.  Exact
   characteristic-zero elimination makes ten of the twelve ideals unit.
   All ten now have retained Singular source lifts.  The remaining two
   33-variable classes timed out and are explicitly undecided.

No `X4` point survived either terminal, so there was no candidate on which
to run the 28 nonlinear cap Rabinowitsch ideals.  This is a vacuous carrier
audit, not an inference that arbitrary `X4` sources have caps.

## 1. Exact binary-pool join

Every `X4` source has three exact binary restrictions.  The finite audit in
`audit_binary_pool_join.py` loads and hashes the two W33 inventories:

```text
pool A:  9,751 records
pool B:  9,777 records
total:  19,528 records
```

Each binary record is included in both color orientations.  A vertex is a
literal diagonal color layer (its occupied edge support), and a directed
edge is a stored exact binary face.  Three faces can be assembled only along
a directed triangle of layer supports.  The exact census is:

```text
10,759 support-layer vertices
25,994 directed support pairs
12 directed support-layer triangles
42 compatible record triples
42 triples compatible under exact rational site-color gauge alignment
36 distinct assembled rational ternary sources
30 distinct occupied-cell supports
```

The gauge solver checks every cycle ratio.  All 42 joins have square
parameter `t^2=1`, so the alignment is rational; no numerical root choice is
hidden.  Raw evaluation of all 4,881 `X4` equations rejects every one of the
36 coefficient points in 7--12 rows.

The stronger result is support-theoretic.  The 30 supports have sizes 19,
20, or 23, and each has 7, 8, or 10 mixed `X4` words supported by exactly one
perfect matching.  On the torus where every displayed cell is nonzero, that
word amplitude is a single nonzero monomial.  Therefore the whole open
support is disjoint from `X4` over any field.  There is no residual
coefficient ideal on these supports.

Scope is load-bearing: the W33 inventories are experimental finite pools,
not an exhaustive classification of exact binary sources.  The theorem is
only about the 30 literal support joins arising from the pinned records.
Independent site relabellings of the three faces were not exhaustively
joined.

## 2. Joint shift/color-cycle certificate

The strongest fixed-locus result uses the covariance

```text
A_(u+1,v+1)[sigma(a),sigma(b)] = A_(u,v)[a,b],
sigma = (0 1 2), sites modulo 8,
```

where reversing endpoint order also transposes the two color indices.  The
joint generator has order `lcm(8,3)=24` on the 252 endpoint cells.  Its cell
orbits have sizes 12 and 24, with exactly 11 orbits.  Conversely, the
displayed covariance identifies exactly the cells in those orbits, so one
free coordinate per orbit is exhaustive for this ansatz.

All 4,881 raw `X4` equations reduce over `Z` to 121 distinct nonzero
polynomials in those 11 coordinates.  `audit_cycle012_equivariant.py`
builds them directly from all 105 perfect matchings and checks a deterministic
134-row spread with a second recursive hafnian engine.  Singular returns an
exact source lift

```text
1 = sum_(j=1)^121 multiplier_j * generator_j
```

with 80 nonzero multipliers.  The complete active row labels, multipliers,
and hashes are retained in `certificate_cycle012.json`.  Singular verifies
the identity before emission.  Deleting the first active generator from the
left side breaks that same identity, a must-fire mutation control.

Thus the 11-dimensional joint shift/three-cycle fixed locus contains no
`X4` point over characteristic zero.

## 3. Exhaustive small fixed-locus sweep

Conjugacy classes of single elements of `S8 x S3` are exactly pairs of a
partition of 8 and a partition of 3.  `sweep_equivariant_actions.py`
enumerates all `22 * 3 = 66` pairs, constructs their literal endpoint-cell
orbits, and retains every class with at most 33 orbits.  There are exactly
12:

| site cycle type | color cycle type | variables | result over `Q` |
|---|---|---:|---|
| `8` | `3` | 11 | UNIT + source lift |
| `7+1` | `3` | 12 | UNIT + source lift |
| `5+2+1` | `3` | 17 | UNIT + source lift |
| `5+3` | `2+1` | 20 | UNIT + source lift |
| `7+1` | `2+1` | 20 | UNIT + source lift |
| `4+4` | `3` | 22 | UNIT + source lift |
| `5+1+1+1` | `3` | 24 | UNIT + source lift |
| `5+3` | `3` | 24 | UNIT + source lift |
| `4+2+2` | `3` | 27 | UNIT + source lift |
| `4+2+1+1` | `3` | 28 | UNIT + source lift |
| `8` | `1+1+1` | 33 | **TIMEOUT / no verdict** |
| `8` | `2+1` | 33 | **TIMEOUT / no verdict** |

Every UNIT record stores the generator-list hash and a separately verified
source-lift hash.  The two timeouts are exactly the site-cyclic/color-fixed
and site-cyclic/color-transposition systems; they are not counted as
negative evidence.  No class returned NONUNIT, so no algebraic `X4` point
required extraction or carrier screening.

The endpoint-order mutation deliberately omits the required transpose when
an edge reverses.  It changes the joint shift/three-cycle quotient from 11
orbits to 12 (orbit histogram from `12:1,24:10` to `12:3,24:9`), confirming
that the convention affects the exact ansatz.

## 4. Mandatory controls

The finite-pool audit independently rebuilds both named boundary controls.

* **W40:** all 4,881 `X4` rows pass; exactly six of the 168 star carriers
  pass; no triangle carrier passes.  Its support has the expected three
  singleton `(3,3,2)` words, which obstruct full exactness but not `X4`.
* **W25-F8:** exactly 78 level-four rows fail; all 728 star/triangle carriers
  fail.  Its support has the expected twenty singleton `(3,3,2)` words.

These controls distinguish the positive `X4`/cap boundary from an all-blocked
object below `X4`.  They do not use failed random search as evidence.

An unconstrained dense Boolean search and the two 33-variable
characteristic-zero systems produced no terminal.  The former was stopped;
the latter are the explicit timeouts above.  No claim is based on either.

## 5. Artifacts and replay

| artifact | purpose |
|---|---|
| `audit_binary_pool_join.py` | exact 19,528-record join, raw `X4`, support singletons, W40/W25 carriers |
| `results_binary_pool_join.json` | all 36 coefficient profiles and 30 support-stratum certificates |
| `audit_cycle012_equivariant.py` | dedicated 11-variable source-lift certificate |
| `certificate_cycle012.json` | 80 active source rows and exact multipliers |
| `sweep_equivariant_actions.py` | exhaustive 66-class conjugacy enumeration and bounded elimination |
| `results_equivariant_sweep.json` | ten UNIT classes, ten lifts, two isolated timeouts |
| `classify_equivariant.py` | raw fixed-locus polynomial constructor |

Replay from the repository root:

```text
PYTHONDONTWRITEBYTECODE=1 python3 computations/unaudited-codex-x4-cap-falsifier-2026-08-20/audit_binary_pool_join.py
PYTHONDONTWRITEBYTECODE=1 python3 computations/unaudited-codex-x4-cap-falsifier-2026-08-20/audit_cycle012_equivariant.py
PYTHONDONTWRITEBYTECODE=1 python3 computations/unaudited-codex-x4-cap-falsifier-2026-08-20/sweep_equivariant_actions.py --max-variables 33 --decision-timeout 10 --lift-timeout 30
```

Standard, optimized, and isolated/no-site replay is recorded in
`replay_results.json`.  All exact outputs agree across the three modes; the
two declared timeout classes remain timeouts in every mode.

## 6. Honest residual

No counterexample to `X4`-to-cap was found.  This lane removes 30 concrete
remote support strata and ten small symmetry-fixed linear families.  An
actual falsifier must lie outside those supports and outside those ten fixed
loci; it may still lie in either undecided 33-variable fixed locus or have
no such single-generator symmetry.  The universal problem remains the
simultaneous cross-carrier algebra on arbitrary `X4`, not further local
deformation of W40.

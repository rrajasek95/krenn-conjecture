# The normalized pure-amplitude cone still misses degree-13 mixed X5

Status: **UNAUDITED exact characteristic-zero nonmembership theorem**.

## Target and exhaustive fine grade

Let `Delta` be the canonical degree-9 carrier minor from the
[degree-9 audit](../unaudited-codex-carrier-minor-degree9-x5-2026-08-23/REPORT.md):

```text
triangle/cofactor columns = 01,02,12
residual colour           = 0
cap response rows         = 01,11,21.
```

The final normalized target requested here is

```text
F_00000000 * Delta,
```

where `F_00000000` is the full 105-term pure colour-0 amplitude.  Literal
source multiplication gives

```text
degree            : 13
distinct monomials: 664,776
coefficients      : +/-1,+/-2,+/-3,+/-4,+/-5,+/-6,+/-8
target SHA-256    : 90397081d79e8172c1b0af67f41b96b31d5c9ef37c155c0888976b2908caaf8e.
```

Its fine weight is the same as for a single pure-matching cone:

```text
sites 0,1,2 : (2,0,0)
sites 3,4,5 : (4,0,0)
site  6     : (2,1,1)
site  7     : (1,3,0).
```

The complete compatible word list is

```text
00000000 (pure; not a homogeneous mixed-X5 generator)
00000001  00000010  00000011  00000020  00000021.
```

Therefore the five mixed amplitudes shown are the exhaustive generator
family in this fine grade.

## Exact verdict

Cancellation among the 105 pure matching components does not rescue the
proposed membership:

```text
F_00000000 * Delta notin (all mixed X5 amplitudes)_13 over Q.
```

The exact replay rationally reconstructs the terminal modular dual with
denominators `{1,2}`.  Clearing denominator 2 gives a primitive integer
functional with

```text
support        : 44 monomials
coefficient set: {-2,-1,1,2,3}
target pairing : 2.
```

Exactly 52 translated rows can touch its support:

```text
00000001 : 10
00000011 : 26
00000021 : 16
00000010 :  0
00000020 :  0.
```

Every one of those 52 literal integer pairings is zero.  All remaining
degree-9 translates are support-disjoint.  This is an exhaustive exact
characteristic-zero separator; it also works in every characteristic other
than 2.

## Lazy discovery ledger

The bounded discovery used the empty-seed version of the exact lazy CEGAR
theorem, so no 664,776-column target-touching matrix was materialized.  Over
`F_32003` it terminated as follows:

```text
growth rounds               : 190
terminal zero-crossing scan : round 191
final rank                  : 1,405
tracked columns             : 729,001
basis nonzero entries       : 6,507,602
terminal dual support       : 44.
```

Naively centering the modular residues is deliberately *not* accepted: it
leaves nine row pairings equal to `+/-32003`.  Rational reconstruction maps
the five residue classes to

```text
1, -1, +1/2, -1/2, +3/2,
```

after which clearing denominator 2 yields the exact primitive separator
above.

## Consequence and scope guard

Even with pure normalization `F_00000000=1`, the desired first step

```text
F_00000000*Delta in mixed X5  =>  Delta=0
```

cannot be invoked because the homogeneous membership premise is false.
This retires both the single-matching cone and the full pure-amplitude cone
as direct degree-13 routes.

This does not decide radical membership, higher-degree multipliers, or an
argument that explicitly uses the inhomogeneous equation
`F_00000000-1`; those are different ideal-membership problems.

## Replay

```bash
python3 computations/unaudited-codex-carrier-minor-pure-amplitude-degree13-x5-2026-08-23/audit_pure_amplitude_carrier_minor_separator.py --check-results
python3 -O computations/unaudited-codex-carrier-minor-pure-amplitude-degree13-x5-2026-08-23/audit_pure_amplitude_carrier_minor_separator.py --check-results
python3 -I -S computations/unaudited-codex-carrier-minor-pure-amplitude-degree13-x5-2026-08-23/audit_pure_amplitude_carrier_minor_separator.py --check-results
```

The hostile mutation `--mutate-separator` fails on literal `00000011` and
`00000021` translates.

Frozen logical digest:
`478e82aa56681de9bbc9d2e662bdeea5d41c721cc77339188beb8832ef36d8b3`.

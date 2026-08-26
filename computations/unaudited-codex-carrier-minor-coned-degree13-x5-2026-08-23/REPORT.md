# A pure-matching cone does not put the canonical carrier minor in mixed X5

Status: **UNAUDITED exact-Z nonmembership theorem**.

## Literal target

Use the canonical carrier minor already frozen in the adjacent
[degree-9 audit](../unaudited-codex-carrier-minor-degree9-x5-2026-08-23/REPORT.md):

```text
triangle/cofactor columns = 01,02,12
residual colour           = 0
cap response rows         = 01,11,21
Delta                     = determinant of that 3x3 cofactor matrix
```

Cone it by the pure colour-0 matching

```text
M = A01_00 A23_00 A45_00 A67_00.
```

The target `M*Delta` has degree 13, 6,900 signed monomials, and SHA-256
`757ec6347b959dd4e920d676a84281f273bb33a0ee31b0502c86235515798c82`.
Its fine site-colour weight is

```text
sites 0,1,2 : (2,0,0)
sites 3,4,5 : (4,0,0)
site  6     : (2,1,1)
site  7     : (1,3,0).
```

Exactly six word amplitudes can enter this fine grade:

```text
00000000 (pure; excluded from the homogeneous mixed-X5 ideal)
00000001  00000010  00000011  00000020  00000021.
```

Thus the five displayed mixed words are the exhaustive generator list.

## Exact verdict

The proposed containment is false:

```text
M*Delta notin (all mixed X5 amplitudes)_13.
```

The exact checker freezes an integer functional with 23 monomial
coordinates and coefficients in `{+1,-1}`.  It pairs with `M*Delta` as `1`
and annihilates every degree-9 monomial translate of all five compatible
mixed amplitudes.  Its digest is

```text
9423469a2fd3280203e99a8ed039c500b21b4f5f73e49c3ebba9fc1a3c5eed77.
```

Only 28 translated rows can touch those 23 coordinates:

```text
00000001 :  9
00000011 :  9
00000021 : 10
00000010 :  0
00000020 :  0.
```

Their 28 literal integer pairings are all zero.  Every other translate is
support-disjoint, so this is an exhaustive source-level replay rather than a
one-prime inference.  Because the target pairing is `1`, the separator works
over every field.

## Discovery ledger

The lazy computation over `F_32003` began with every target-touching row:

```text
target-touching translates : 5,484 = 1,828 x 3
initial outside columns    : 258,321
initial rank               : 5,484
initial total columns      : 265,221.
```

Fourteen crossing rounds added 84 independent rows.  The fifteenth scan
stalled with

```text
rank                 : 5,568
columns              : 267,859
basis nonzero entries: 720,738
terminal dual support: 23.
```

The centered modular coefficients were already `+/-1`; the independent
exact checker then replayed the 28 possible crossings over `Z`.

## Consequence and guard

The attractive normalized argument

```text
M*Delta in mixed X5,  M != 0  =>  Delta = 0
```

cannot be used: its first premise fails for the canonical matching chart.
By symmetry, transporting this nonmembership gives the analogous guard for
the transported matching/carrier configuration.

This audit does **not** decide radical membership, higher-degree
multipliers, or consequences that also use the inhomogeneous normalization
row `H_0-1`.  Those are strictly different targets.

## Replay

Exact theorem and stored-result checks:

```bash
python3 computations/unaudited-codex-carrier-minor-coned-degree13-x5-2026-08-23/audit_coned_carrier_minor_separator.py --check-results
python3 -O computations/unaudited-codex-carrier-minor-coned-degree13-x5-2026-08-23/audit_coned_carrier_minor_separator.py --check-results
python3 -I -S computations/unaudited-codex-carrier-minor-coned-degree13-x5-2026-08-23/audit_coned_carrier_minor_separator.py --check-results
```

The hostile mutation `--mutate-separator` fails on a literal
`00000021` translate.  The modular discovery script is deterministic in
`std`, `-O`, and `-I -S`; its result SHA-256 is
`6b37fd469f548fc5f799701754cb17fbd97cffab22085bbd0a8b11528bffa29d`.

Frozen exact logical digest:
`a51934968d1a35ac8d99d42baf8177acf181bf892bba6fabb2b4eab59535e0f5`.

# The 44-term separator is rank-5, non-character, and not cyclically prolongable

Status: **UNAUDITED exact inverse-system theorem**.

## Character test: exact failure

Let `lambda` be the primitive 44-term integer separator for
`F_00000000*Delta`.  It is not a scalar multiple of a monoid character, even
when restricted to its nonzero support.

Number the 44 stored support monomials from zero in their frozen order.  The
first exact toric countercircuit is

```text
m_1 m_6 = m_0 m_7                 (equal exponent vectors)

lambda(m_1),lambda(m_6) =  1, 2   product 2
lambda(m_0),lambda(m_7) = -2,-2   product 4.
```

An evaluation functional would require the two products to agree.  Thus the
separator is not evaluation-like; this conclusion does not rely on any of
its zero coordinates.  The four literal monomials are frozen in the result
file.

## Pure-matching Hankel rank

Form the exact contraction/catalecticant

```text
H(p,q) = lambda(pq),
```

with rows indexed by the 105 pure colour-0 perfect-matching monomials `p`
and columns by the degree-9 quotients `q` occurring in the separator.

Exactly five rows are live:

```text
index  matching                         row support
  0    01|23|45|67                           17
  6    01|25|34|67                            5
 15    02|13|45|67                            1
 30    03|12|45|67                            3
 33    03|14|25|67                            6.
```

The other 100 pure matching contractions vanish.  On five explicit frozen
quotient columns the live-row minor is

```text
[-2  0  0  1  0]
[ 0 -2  0  0  0]
[ 0  0 -2  0  0]
[ 0  0  0 -2  0]
[ 0  0  0  2  2]
```

with determinant `32`.  Hence the pure Hankel rank is exactly `5`, not `1`.
A character/evaluation all-k explanation is therefore impossible.

The pairing `lambda(F_00000000*Delta)=2` is carried only by two of those
five channels:

```text
01|23|45|67 :  4
01|25|34|67 : -2
other three :  0.
```

## Failure of a cyclic pure module at k=2

The most literal finitely generated continuation would seek a degree-17
functional `Lambda` supported on

```text
supp(lambda) * supp(F_00000000)
```

such that inverse contraction by `F_00000000` equals `lambda`.  The shell
has 4,559 variables.  The exact 74-row, coefficient-`+/-1` contraction
certificate gives

```text
combined left-hand side  = 0
combined right-hand side = 2.
```

Thus no such one-step cyclic lift exists.  In the full contraction space,
the certified rows expose 5,949 outside repair variables; adjoining all of
them enlarges the shell to 10,508 variables.  Consequently any k=2
continuation needs genuinely new monomials, not merely pure multiples of the
44-term support.

## Verdict and guard

There is no structural all-k separator obtained from a single evaluation,
a rank-one moment sequence, or cyclic pure multiplication of this
functional.  The exact invariant is instead a five-channel Hankel object,
and its first cyclic lift is obstructed.

This does not rule out a higher-rank finitely generated inverse module after
adjoining the 5,949 repair variables, and it does not settle global
`F_00000000^2*Delta` membership.  Those remain the precise larger targets.

## Replay

```bash
python3 computations/unaudited-codex-pure-separator-inverse-system-2026-08-23/audit_pure_separator_inverse_system.py --check-results
python3 -O computations/unaudited-codex-pure-separator-inverse-system-2026-08-23/audit_pure_separator_inverse_system.py --check-results
python3 -I -S computations/unaudited-codex-pure-separator-inverse-system-2026-08-23/audit_pure_separator_inverse_system.py --check-results
```

The hostile mutation `--mutate-separator` destroys the frozen first
countercircuit check.

Frozen logical digest:
`62033703253f54026919a66d48006edde004660046edc846031cbdfcafda6dc0`.

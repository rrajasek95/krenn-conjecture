# Proof-theoretic scope of chart-26 standardness through degree nine

Status: **UNAUDITED exact scope audit**.

## What is proved

Let

```text
T = 0111202020494f4f50f8 * t^2
```

in the frozen chart-26 homogeneous mixed ideal with the frozen `t`-last
order.  The degree-nine theorem proves that no certified initial monomial
of total degree at most nine divides `T`.  Equivalently, `T` survives every
target-relevant homogeneous reduction certified through degree nine.

This is a local standardness statement about one monomial.  It does not
prove that `T` is standard for the full initial ideal, that its coefficient
`-4` survives the complete normal form of the 140,185,881-term `C10`
representative, or that `C10` is nonzero in the quotient.

## What remains in fixed total degree twelve

Only degrees 10, 11, and 12 remain, but all three are genuine:

| relation degree | target divisors by `t` exponent | new `t`-free multiplier degree |
|---:|---|---:|
| 10 | `t^0:1, t^1:7, t^2:23` | 6 |
| 11 | `t^1:1, t^2:7` | 7 |
| 12 | `t^2:1` | 8 |

The positive-`t` part at degree `d` is `t*M_(d-1)` and is inherited from
the preceding theorem.  However, every degree has a new `t`-free head.  A
kernel in that head may descend into one of the displayed target tails, so
degree-nine standardness does not decide any of these three heads.

## No upward term-order lemma

Standard monomials form a divisor-closed order ideal.  This propagates
standardness downward, not upward.  A minimal generator of the initial
ideal of degree 10, 11, or 12 may still divide `T`.  For example,

```text
J = <x^10>,    T = x^10*t^2
```

has no initial-ideal divisor through degree nine but fails at degree ten.
Thus finite target degree only bounds the remaining work; it does not make
degree nine terminal.

A valid shortcut would require a separately proved statement such as
`reg(I)<=9`, or that the chart-26 initial ideal is generated through degree
nine.  No such statement is frozen, and the existing degree-five and later
exchange cells give no basis for assuming it.

## C10, chart, and global guards

`C10` is the residual of one specified deterministic monic right inverse
through `y^9`.  Its own authoritative artifact says that alternative
lower-degree kernel choices may change it.  A selected coordinate being
standard through degree nine is not a full-row Macaulay separator.

Even a complete negative answer at fixed degree twelve would remain weaker
than affine/localized nonmembership: after dehomogenizing `t=1`, membership
may homogenize only as `t^k F^h in I^h` for some `k>0`.  A negative fixed
degree therefore needs a `t`-saturation theorem before it can become a
chart-level nonmembership statement.

Finally, chart 26 is one of the 31 pure-matching-triple chart orbits.
Nothing here covers the other 30 charts or decides global X5.  A negative
membership result would not produce an X5 point; a positive certificate
would only provide the corresponding orbit-26 localized obstruction unless
transport/coverage is separately proved.

Replay:

```sh
python3 computations/unaudited-codex-n8-d9-proof-theory-audit-2026-08-23/audit_d9_proof_scope.py --write-results
python3 computations/unaudited-codex-n8-d9-proof-theory-audit-2026-08-23/audit_d9_proof_scope.py --check-results
python3 -O computations/unaudited-codex-n8-d9-proof-theory-audit-2026-08-23/audit_d9_proof_scope.py --check-results
python3 -I -S computations/unaudited-codex-n8-d9-proof-theory-audit-2026-08-23/audit_d9_proof_scope.py --check-results
```

Hostile `--mutate` must fail. Logical digest:
`3a0b31a26c79b2ff55bad9f58fb6d45742d5e695524ac07ec06bd6e41d55e5f6`.

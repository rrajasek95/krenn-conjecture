# Actual degree-12 post-correction residual audit

## Exact tail correction

Let `S` be the complete literal source correction used after the frozen
degree-five certificate, and let

```text
Rfull = Fh - S = C10 + C11 + C12.
```

The 20-row functional from the degree-12 dual artifact annihilates every
homogeneous degree-12 mixed source column.  This was independently replayed
on all 22 incident columns and on the explicit 90-column lower-kernel vector.
Consequently it annihilates `S` for the actual chosen correction, without
needing to expand the y11/y12 tail.

Direct normalized expansion gives 1,157,625 terms in `Fh`, zero of which meet
the functional's 20-row support.  Therefore

```text
lambda(Rfull)       = lambda(Fh) = 0,
lambda(C10)                      = -4,
lambda(C11 + C12)                = +4.
```

This is the exact missing-tail audit.  In particular `C10` by itself is not
a representative of the target class in the full degree-12 quotient.

Authorities:

- degree-12 dual logical digest:
  `cde136aef242841bc78bc9b7da8e56323ab0b273bb637a30253902e9b2729aed`;
- full-tail/Fh referee logical digest:
  `0942f658d68bf670f17af93e6201414a55d25611c84a88a623021f411be2eee8`;
- factored C10 logical digest:
  `e15fb02c5ba4b4b0dadefb0f536953c785d7d07b658b7195a976fc5c145bcd93`.

## Bounded sparse-dual attempt

I enumerated the lex-first 100 y-degree-ten monomials occurring in the exact
normalized target that have no degree-ten primitive source incidence.  For
each seed, I applied the same exact private-top-row dual extension used for
the 20-row functional.

| terminal stage | seeds |
|---|---:|
| coupled crossing core at degree 11 | 77 |
| exact private extension through 11, then core at 12 | 23 |
| complete target-pairing dual through degree 12 | 0 |

The first seed is `0408095a79a1aab4d3d8`; it has nine D11 crossings, and
the private peel leaves the crossing column
`code=216, multiplier=040879a1b4d3d8`.  The first seed reaching D12 is
`0408095a94a1a6aab4d8`; it has 13 D11 crossings, all privately repaired,
then 177 D12 crossings with a nonempty coupled core.

## Verdict and scope

`UNRESOLVED`: no target-supported sparse dual and no literal source solve was
obtained within the bounded screen.  The exact positive statement is only
the missing-tail cancellation above.  The 100-seed failure rules out this
specific private-row construction, not an arbitrary coupled dual, membership,
nonmembership, saturation, or a global theorem.  No degree-13 computation is
used in this audit.

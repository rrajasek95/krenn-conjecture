# Face `0:31:15`, open `R=0` branch structural reduction

Status: **exact fraction-free reduction and first sound split frozen.**

No Gröbner basis, F4SAT, msolve, rank, or sampling computation was run.

## Exact source reduction

On `d2-1 != 0`, the already-live factor `b4` makes

```text
A = b4*(d2-1)
```

live. Raw 16 is `A*a2+B`, so the branch is faithfully parametrized by
`a2=-B/A`. Substitution into every literal raw row and primitive numerator
clearing produces denominators containing only powers of `b4` and `d2-1`.
Raw 16 becomes zero, while raw 11 becomes the frozen irreducible 29-term,
degree-six resultant `R`; this report imposes `R=0` explicitly.

The remaining 14 source numerators are raw

```text
6,7,8,9,10,12,13,14,15,17,18,19,20,21.
```

Their term counts, in shortest-factor order, are

```text
raw9:7, raw7:10, raw15:10, raw20:10, raw6:16, raw14:16,
raw18:17, raw12:25, raw8:32, raw10:32, raw13:38, raw19:43,
raw17:52, raw21:76.
```

Exact Q factorization finds each displayed numerator irreducible; no declared
live factor was silently removed. The original live factors involving `a2`
become the explicit numerators `B` and `A-B*d2` and are retained in the
profile.

## Shortest new consistency equation

The unique shortest reduced source row is raw 9 (`t_123`). Its irreducible
seven-term numerator is

```text
F = a3*a4*b4*d3 + a3*b3 + a4*a5*b3*b4*b5*d3 + a4*b4
    + a5^2*b3*b4^2*d3 - a5*b3^2*b5 - 2*a5*b3*b4.
```

It admits the exact short split

```text
J = a4*b4*d3-b3,
S = a3*a4*b4*d3+a3*b3+a4*b4
    +a5^2*b3*b4^2*d3-2*a5*b3*b4,
U = 2*a3*d3+a5^2*b4^2*d3^2-2*a5*b4*d3+1,

F    = a5*b3*J*b5 + S,
d3*S = b3*U + J*(a3*d3+1).
```

Because `a5,b3,d3` are already live, this is a sound two-way gate:

- on `J != 0`, raw 9 solves `b5=-S/(a5*b3*J)`;
- on `J = 0`, raw 9 is equivalent to the four-term residual `U=0`.

This is a structural reduction only. Neither side of the `J` split is
closed, and no radical or emptiness conclusion follows.

The `J=0,U=0` side now has a frozen faithful full-source characteristic-zero
gate. It retains all 15 literal post-substitution source rows, adds `J,U`,
and localizes every surviving original live numerator. The sole exact run
timed out at 600.555 seconds with zero-byte output and no sentinel, so this
side remains open. See
`../unaudited-codex-face03115-R-J0-char0-2026-08-21/REPORT.md`.

The complementary `J!=0` side also has a faithful full-source gate after
using raw 9 to solve `b5=-S/(a5*b3*J)`. It retains all 14 nonzero literal
source numerators and every surviving original live numerator. Its sole exact
run timed out at 600.688 seconds with zero-byte output and no sentinel, so it
too remains open. See
`../unaudited-codex-face03115-R-Jopen-char0-2026-08-21/REPORT.md`.

## Reproducibility

Standard, `-O`, and isolated `-I -S` executions agree on logical digest
`fb1fe640b268d27d10276a1c69d2a69e48316a71d1433029cf8965c98b912fab`.
The producer and result file SHA-256 values are
`4445ab44fb397215efab42987ae7d88d52f3490f9032a3c30fb9a5382d21922f`
and `812622c9496a197f30da4702d47068a1b8987a067d28128e4b8e3db5d2f4a841`.
Resultant-sign and `d2-1 -> d2+1` mutations fire.

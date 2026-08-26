# Joint face `0:31:15` bounded modular lead

Status: **exact source export and a two-row fraction-free reverse split are
frozen; the sole large-prime F4SAT gate timed out.**

No algebraic conclusion is claimed.

## Literal face and normalization

The state is `(B,T,D)=(0,31,15)`. In edge order
`01,02,03,12,13,23`, edges `01,02,03,12` remain both-live, edge `13`
is selected offdiagonal/aligned, and edge `23` is selected diagonal/aligned.
It is the triangle-plus-pendant codimension-one face of the k5 start and has
labelled multiplicity four.

The selected-offdiagonal edges `01,02,03` form a spanning tree. The live site
torus sets

```text
b0=b1=b2=1,  d0=1.
```

The first three equations fix the three site ratios; the residual common
scale fixes the live `d01` over the algebraic closure. This preserves every
literal source zero and every live condition. The remaining geometric
variables are

```text
a0,a1,a2,a3,a4,a5,b3,b4,b5,d1,d2,d3.
```

All six permanent rows vanish under their solved block substitutions. The 16
triangle/cofactor rows `6,...,21` survive and are linearly independent over
Q as polynomial coefficient vectors (140 distinct monomials, rank 16).

## Square reverse core and live product

The bounded gate uses the canonical 12-row nonpivot compatibility core

```text
raw 7,8,12,13,14,15,16,17,18,19,20,21.
```

These are triangles `t013,t023` plus all ten cofactor rows away from the
gauged pivot edge `01`. The omitted rows are triangles `6,9` and pivot-edge
cofactors `10,11`. The cheapest omitted cofactor to reverse is raw 11,
`cofactor_0_3`, with 10 terms (raw 10 has 15 terms).

“Smallest” here means the canonical dimension-square, pivot-omitted source
core. No ideal-theoretic row minimality is inferred without a completed
solve.

The exact full logically live product after gauge is

```text
F = H
    * (a5*b3*b4)
    * (a0*a1*a2*a3*d1*d2*d3)
    * (1+a0)*(1+a1*d1)*(1+a2*d2)*(1+a3*d3).
```

Its factor profiles are: `H` 98 terms, selected base and both-live monomials
one term each, remaining-c product 16 terms, and expanded `F` 1,248 terms.
No factor was discarded or inferred live from a sample.

## Sole modular gate

The coefficient-first strict input
`face03115_base12_full_live_p1073741827.msolve` has SHA-256
`6965e1bc84235b14778cc4644a2b5f7422e5391346baaead9f46f3f2fb1d5d4b`.
It contains 12 exact source rows and the expanded full-live polynomial as the
final native F4SAT saturator. The strict parser reports no invalid equations;
source and saturator sign mutations fire.

Exactly one run was launched:

```text
p = 1073741827, native -S, DRL, -g 2, 8 threads, cap 300 seconds.
```

It timed out after 300.268 seconds, was terminated with return code `-15`,
and left a zero-byte basis file. Therefore:

- there is no modular UNIT claim;
- there is no NONUNIT, dimension, or component signature;
- no second prime or characteristic-zero run was launched;
- no altered saturator or row set was tried.

The timeout manifest SHA-256 is
`d86f08f08fecde7e0849515e6c075d95d026a4b46f0270b38628cbc62ebc7a18`.
The exact source-export logical digest is
`4d305c2455781479fafecab69119b4e7d8e011e1c5c5a69cb7c50ae6d81727b4`.

## Exact raw16/raw11 fraction-free split

Profiling the 12 normalized core rows against variables also occurring in
the cheapest omitted cofactor raw 11 finds the unique shortest core row,
raw 16 (`cofactor_3_0`, eight terms). It is linear in `a2`:

```text
raw16 = A*a2+B,       A=b4*(d2-1),
raw11 = C*a2+D.
```

The factor `b4` is already in the declared live product. Exact elimination
therefore introduces only the sound split `d2-1`. The script proves the
literal fraction-free identity

```text
A*raw11 - C*raw16 = R,
```

where `R=A*D-B*C` has 29 terms, total degree six, and is irreducible over Q.
On `d2-1 != 0`, raw16 gives `a2=-B/A`, and raw11 vanishes exactly when
`R=0`. On the complementary branch `d2=1`, raw16 instead becomes

```text
a5*(d1+1)*(b4-1)+b4+1 = 0,
```

and does not solve `a2`. Thus this is a compact exact reverse gate, not a
closure of either branch. Cross-term-sign and `d2-1 -> d2+1` mutations fire.
Standard, `-O`, and isolated `-I -S` replays all give logical digest
`724c1879dfcedfa714335541ab98246d1e47bcbff3938a865e7ea9530ffc9325`.
The producer and frozen result files have SHA-256
`f3d584c4f0befb378086c4c4077b5e7eb8723fa32fe77a7e9fbb971cd6c60756`
and `31e4696802de427f85aec0976b641aa360c2b3d0fe908ee12e08723eebedac15`.

## Scope

This package concerns only `0:31:15`. It does not touch `0:31:30`, any k6
state, or the ordinary triangle-plus-pendant `P26!=0` lane. The timeout is a
resource result, not evidence for or against emptiness. The fraction-free
identity is exact, but leaves the irreducible `R=0` open branch and the
explicit `d2=1` residual; it is not an emptiness claim.

The `d2=1` residual now has a faithful full-source exact characteristic-zero
interface. Solving raw16 uses `raw16=K*(b4-1)+2` with
`K=a5*(d1+1)+1`, so `b4=N/K` has a forced-live denominator. All other 15
raw rows and every surviving original live factor are present. The sole exact
run timed out at 600.397 seconds with zero-byte output and no sentinel; this
branch therefore remains open. See
`../unaudited-codex-face03115-d2eq1-char0-2026-08-21/REPORT.md`.

The sibling `d2-1 != 0, R=0` branch has also been reduced structurally, with
no ideal solver. Fraction-free substitution `a2=-B/[b4(d2-1)]` leaves 14
literal source numerators plus `R`. The shortest is the irreducible seven-
term raw 9 equation. Writing `J=a4*b4*d3-b3`, it either solves `b5` on
`J!=0`, or reduces on `J=0` to the four-term equation
`2*a3*d3+a5^2*b4^2*d3^2-2*a5*b4*d3+1=0`. See
`../unaudited-codex-face03115-R-branch-2026-08-21/REPORT.md`.

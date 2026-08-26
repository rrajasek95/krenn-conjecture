# C10 modulo the full lower-kernel image

## Exact corrected invariant

Work in the frozen normalized orbit-26 chart and homogeneous total degree
12.  Let `E` be the space of all literal mixed source columns and split the
output map as

```text
M=(L,H): E -> R_(y<=9) + R_(y>=10).
```

Put `K=ker(L)` and `B=H(K)`.  A terminal residual is canonical only as a
class in

```text
Qrel = R_(y>=10) / B.
```

Thus the sound fixed-target question is `[C10] != 0` in `Qrel`, equivalently
whether `(0,C10)` is outside `im(M)`.  Its exact dual formulation is to find
`lambda` and `mu` such that

```text
H^T lambda = L^T mu,        lambda(C10) != 0.
```

Indeed the first equation says precisely that `lambda` annihilates `H(K)`;
equivalently `(-mu,lambda)` is a dual of the full degree-12 source map.  This
avoids constructing a basis of `K`, but without an additional sparsity or
symmetry theorem it is the full degree-12 Macaulay dual problem in transpose
form, not a smaller solve.

## Mandatory target-scope correction

The later complete degree-12 replay constructs such a 20-row functional and
finds

```text
lambda(C10) = -4,          lambda(Fh) = 0.
```

The normalized `Fh` has 1,157,625 terms, and none of the 20 functional rows
occurs in it.  Since the same functional annihilates every homogeneous
degree-12 mixed source column, these unequal pairings prove both that the
fixed class `[C10]` is nonzero and that **`C10` is not congruent to `Fh`**
modulo the normalized mixed ideal.  The omitted y11/y12 part of the actual
post-correction residual pairs by `+4` and cancels the fixed-C10 pairing.

Consequently every statement below concerns only the fixed `C10` or the
single monomial `m`.  It supplies no nonzero `Fh` class, no `Fh`
nonmembership, and no `Fh` t-saturation obstruction.  The exact target-scope
referee is
[`REPORT.md`](../unaudited-codex-n8-degree13-full-dual-referee-2026-08-23/REPORT.md),
logical digest
`0942f658d68bf670f17af93e6201414a55d25611c84a88a623021f411be2eee8`.

## Exact counterguard to a coordinate invariant

The frozen 90-column source combination replays to zero in every output row
of y-degree at most 9 and to a 714-row y10 vector `v0`, with coefficient `+1`
at

```text
m = 0111202020494f4f50f8 * t^2.
```

Hence `v0` lies in `B` and the coordinate functional `delta_m` does not
descend to `Qrel`.  Since the deterministic C10 has coefficient `-4` at `m`,
adding `-4 v0` cancels that coefficient and moves the residue into the other
713 rows.  The smallest audited finite relative quotient is therefore

```text
R_y10 / <v0>,             support(v0)=714,
```

but it is only a one-dimensional sub-boundary and gives no verdict on the
full lower-kernel quotient.

## What descends from the degree-12 monomial theorem

The certified result `m not in im(M)` implies exactly that `[m] != 0` in
`Qrel`: if `m=H(k)` for some `k in ker(L)`, then `M(k)=(0,m)`, a
contradiction.  Equivalently, finite-dimensional separation guarantees a
full dual `(-mu,lambda)` with `lambda(m) != 0`, and this `lambda` annihilates
`B`.

At the restricted-owner stage this descent was only existential, and
`lambda(m) != 0` alone did not imply `lambda(C10) != 0`.  The later complete
20-row dual closes that fixed-C10 question with pairing `-4`.  This does not
rescue the failed coordinate functional `delta_m`, and—by the scope
correction above—it says nothing nonzero about `Fh`.

## Finite interface and scope

The smallest sound next interface is the target-rooted relative system

```text
L(k)=0,                   H(k)=C10,
```

or its transpose above, closed under every source column incident to the
current functional support.  The earlier capped coordinate audit exposed
13,451 lower rows and 306,729 owner columns but left 283,468 active columns
unexpanded.  That capped route did not close the interface, but the later
20-row full-column replay did: `[C10] != 0` in the normalized degree-12
quotient.  No corresponding `Fh` nonmembership, t-saturation, or global-chart
conclusion is claimed.

Replay:

```text
python3 computations/unaudited-codex-n8-c10-relative-cokernel-audit-2026-08-23/audit_c10_relative_cokernel.py --check-results
```

Logical digest:
`330ba2a83da282ec93efa7df009318b03fd6e7c3d48676b728e5639caec9af5e`.
This digest identifies the original relative-cokernel checker/result; the
scope correction is pinned separately by the referee digest above.

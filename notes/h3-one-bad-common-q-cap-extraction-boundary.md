# The genuine common-q tower does not itself extract the one-edge cap

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_common_q_cap_extraction_boundary.py`

## Verdict

At `h=3`, the genuine common-q cofactor tower and the four one-bad response
equations do not yet contain a grade-correct operation which extracts the
intrinsic single-edge cap of `a67ec1d`.

This is not a counterexample to the desired extraction theorem. It is an
exact boundary theorem for the operations currently present in the proof:

1. after genuine cofactors are substituted, the Euler/Hessian tower rows
   are identities in `q`, not new equations on the endpoint stars;
2. a physical response row is `r_ij q^[2] = delta_ij X_i`, while the
   required support statement concerns the raw response `r_K`;
3. ordinary row combinations cannot lower internal-q degree, and one
   audited pair/cofactor deletion lowers degree two only to degree one; and
4. the first source-labelled mixed common-hole row can vanish while its
   bright star is genuinely multisite.

Thus the first possible missing operation is a second-order,
source-tangent principal-parts attachment coupling the remaining target row
to the mixed common-hole row. Another Euler recurrence cannot supply it.

## Endpoint-use and internal-degree obstruction

For the one-bad pair, give the two deleted endpoint stars bidegrees

```text
deg p_i=(1,0),  deg s_j=(0,1),  deg q=(0,0).
```

Every literal physical row has endpoint-use grade `(0,0)` (direct) or
`(1,1)` (two-star response). The desired sufficient concentration
identities have grades

```text
p_i^[2] : (2,0),   s_j^[2] : (0,2),
R_K^[2] : (2,2).
```

Those are not physical matching grades at the selected pair. This is the
same provenance obstruction as in the multisite-cap audit, now combined
with the common-q tower.

There is also a sharper `h=3` filtration. The four response rows have
internal-q degree two:

```text
r_ij q^[2] = delta_ij X_i.
```

The intrinsic landing asks that a scalar-zero pure-target combination
`r_K` be supported on one physical edge, a statement of internal-q degree
zero. Polynomial multipliers only raise degree. One literal pair/cofactor
contraction removes one q-edge and leaves degree one. Reaching the raw
response therefore requires principal-parts depth at least two. Formally
differentiating the displayed equality twice is not valid: it differentiates
the source point away from the exact fibre. The two deletions must be
completed by source-labelled correction rows which keep all nine equations
and the target fixed.

## Literal common-hole counterguard

On five common sites `0,...,4`, with colours `(a,c,t)=(0,1,2)`, take the
genuine quadratic

```text
01:00 = 1,   34:00 = 1,
13:11 = 1,   24:11 = 1,
12:10 = 1,   02:10 = -1.
```

Put

```text
Q_c = e1@0 + e1@1,
R_a = e0@2,
P_t = e2@3.
```

Literal matching expansion gives

```text
Q_c q^[2] = X_c,
R_a q^[2] = X_a,
P_t Q_c R_a q = 0.
```

The first equality is a real two-hole cancellation: `Q_c^[2] != 0`.
Moreover `P_t q^[2] != 0`, so the source-labelled mixed common-hole row

```text
P_t (D_ca q^[2] + Q_c R_a q) = 0
```

forces `D_ca=0` but does not concentrate `Q_c`. Hence the crucial mixed row
from the common-hafnian packet, by itself, is not the missing nullhomotopy.

This is genuine common-q provenance through the asserted level. It is
deliberately only a partial two-chart packet: it omits the remaining `(t,t)`
target row and its associated zero rows. Consequently it is not a one-bad
source, not a Krenn counterexample, and not a logical counterexample to the
full extraction lemma.

## Precise missing overlap operation

On the shared-reciprocal packet, the already proved rows are

```text
Q_c K = X_c,                   R_a K = X_a,
P_t (D_ca K + Q_c R_a q) = 0,
P_t (D_tt K + Q_t R_t q) = X_t,
```

with `K=q^[2]`. The missing object is not another Euler row. It is a
source-provenant relative operation on these rows which:

1. performs the two q-edge deletions needed to reach internal degree zero;
2. uses the mixed row to cancel the deletion tails;
3. retains the nonzero target in the last row; and
4. lands in the off-one-edge coefficients of a scalar-zero pure-target
   response `r_K`.

Equivalently, it is a second-principal-parts/cofactor nullhomotopy in the
two-chart source resolution. Its conclusion may instead be the four
self-square identities, but those have the same repeated-endpoint grade and
therefore require the same provenance change.

Once such an operation produces one-edge support, `a67ec1d` gives the
ordinary determinant units or the inactive pure-edge cap immediately.
Without it, maximum-anchor/minimum-support is only an extremal selection;
it does not add a coefficient row and cannot justify differentiating the
response equations.

## Scope

This closes only the proposed route "common-q recurrence plus the first
mixed overlap row directly implies concentration." The full one-bad
clean-cap extraction lemma remains theorem-strength and, at `N=8`, is a
proof-completing statement. No support face, Groebner search, or formal
independent cofactor was used here.

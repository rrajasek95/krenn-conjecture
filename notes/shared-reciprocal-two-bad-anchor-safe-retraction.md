# The zero-row retraction is anchor-safe and forces the one-bad packet

## The caveat is discharged

The affine retraction in
[`shared-reciprocal-two-bad-zero-row-affine-retraction.md`](shared-reciprocal-two-bad-zero-row-affine-retraction.md)
was initially scoped only as an ordinary-source reduction because it might
have lowered the mutual-anchor count.  In the shared-endpoint two-bad packet
that caveat is false:

> **Anchor-safe retraction theorem.**  The zero-row specialization preserves
> every old mutual coordinate anchor.  If either scaled outer-row family is
> nonzero, it creates the corresponding diagonal direct arm as a new mutual
> anchor.  Hence a maximum-mutual-anchor exact source already has both
> outer-row families identically zero.

This is the requested anchor-preserving nine-row source modification.  It
does not yet contradict the remaining one-bad packet, but it removes all
three fixed-pair quotient branches as separate cases on the synchronized
representative: that representative is automatically in the doubly
projection-degenerate branch.

The exact audit is
`computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py`.

## Why no removed cell is an anchor

Keep the shared bad arms

\[
             A_{pq}=\lambda E_{aa},\qquad
             A_{pr}=\mu E_{cc}.                         \tag{1}
\]

The shared-endpoint flags already say that the coordinate vertices `(p,a)`
and `(p,c)` have degree one in the scalar support graph: their only cells
are the two cells in (1).

The first retraction deletes cells in

\[
        Q_a\ \cup\ \{D_{a0},D_{a1},D_{a2}\}.           \tag{2}
\]

Every cell in (2) is incident to `(q,a)`, which is also incident to the
preserved cell `pq:aa`.  If any cell in (2) is nonzero, `(q,a)` has degree
at least two.  Therefore no deleted cell in (2) is a mutual anchor.  After
all of (2) is deleted, `(q,a)` has degree one, so `pq:aa` is a new mutual
anchor.  Every old anchor on a retained cell remains: deleting unrelated
edges cannot raise either of its endpoint degrees, and its degrees were
already one.

The same proof applies to

\[
        R_c\ \cup\ \{D_{0c},D_{1c},D_{2c}\},           \tag{3}
\]

using `(r,c)` and the preserved cell `pr:cc`.  The common cell `D_ac`
belongs to both families and causes no exception: while it is present,
both of its selected coordinate endpoints have degree at least two; when
it is removed, both direct cells can become anchors.

Writing `nu` for the mutual-anchor count, the exact zero limit therefore
satisfies

\[
 \nu(A_0)\geq\nu(A)
 +\mathbf1_{(Q_a,D_{a*})\ne0}
 +\mathbf1_{(R_c,D_{*c})\ne0}.                          \tag{4}
\]

At maximum `nu`, both indicators must vanish.  Thus

\[
 Q_a=0,\quad D_{a*}=0,\qquad
 R_c=0,\quad D_{*c}=0.                                 \tag{5}
\]

In particular

\[
                  \pi_t(Q_a)=\pi_t(R_c)=0.             \tag{6}

\]

The common-radical quotient branch cannot occur on the synchronized
maximum-anchor representative.  It remains a valid algebraic branch away
from that representative, so its committed audits are not false; they are
simply no longer theorem-completing for the anchor-synchronized route.

## Exact one-bad normal form left behind

Consider the pair `pq`.  The shared flag kills its residual `p_a` row and
(5) kills its residual `q`-endpoint `s_a` row.  The complete nine pair rows
reduce to

\[
\boxed{
\begin{aligned}
 \alpha q^{[h]}&=X_a,\\
 p_i s_jq^{[h-1]}&=\delta_{ij}X_i
                 &&(i,j\in\{b,c\}),                  \tag{7}\\
 E_{aj}=E_{ia}&=0
                 &&(i,j\ne a).
\end{aligned}}

\]

The direct cell `pq:aa` is a mutual anchor.  Equation (7) is precisely the
unary-top/binary-response scalar-unit packet.  It retains all common
matching provenance; no cofactor or response tensor has been declared
independently.

The zero-coordinate charge theorem in
[`scalar-unit-binary-residual-target-branch.md`](scalar-unit-binary-residual-target-branch.md)
now applies with top support `S={a}`.  On `2h` residual sites it forces

\[
             |\operatorname{supp}q|\ge
             h+(h-1)+(h-1)=3h-2.                       \tag{8}

\]

At `N=8`, `h=3`, so the six-site internal quadratic has at least seven
nonzero scalar cells: one unary perfect-matching charge and one
near-perfect charge for each complementary response colour.  This is a
sharp support boundary, not a contradiction.

## What remains open

The anchor issue for the **retraction** is now solved.  The anchor issue for
an internal Hamiltonization of (7) is different and remains open.  Such a
replacement can delete internal cells which really are mutual anchors and
must also preserve all four binary adjacent-power rows.  The exact next
theorem is therefore:

> construct an anchor-preserving source modification of (7), or prove that
> the unary perfect matching and the two charged near-perfect matchings
> force an incompatible mixed coefficient in the full `2 x 2` response
> matrix.

No raw support-layer enumeration is needed to state that target.  The
present theorem removes the common-radical and one-sided projection charts
from the synchronized proof dependency; it does not solve Krenn's
conjecture or the unary-top/binary-response packet.

## Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py
PYTHONOPTIMIZE=1 uv run python computations/verify_shared_reciprocal_two_bad_anchor_safe_retraction.py
```

Both modes freeze the ledger hash printed by the checker.

# Scalar visibility lands only with physical support and activity typing

## Outcome

Assume the complete dark equality

\[
                            \widehat JG=\widehat JC,y                  \tag{1}
\]

and suppose the two-root Cartan image is nonzero in both one-dimensional
deficient endpoint quotients.  The terminal-safe cancellation theorem then
puts the scalar expansion into one of two forms:

* one occupied scalar column is visible in both quotients; or
* two occupied scalar columns are separately visible at the two endpoints.

This visibility alternative is not yet a physical landing theorem.  Locality
makes the first case completely rigid: the unique double-visible scalar is
the diagonal `(c,c)` cell on the selected edge `e=uv`.  It fills both missing
head lines, but it does not satisfy the offdiagonal hypothesis of the active
private-site identity and supplies no second physical pair.

The split case also needs extra typing.  Two split-visible columns may be
diagonal, anchor-contained, or two decorations of the same physical pair.
They give a four-good active overlap only when their fine labels identify an
off-anchor crossed wedge with distinct centre heads and nonzero cofactor
witnesses.

Thus the exact positive theorem is conditional on physical activity, and the
failure branch is precisely the already isolated pure-coloop or injective
no-wedge five-lock residual.  Visibility alone implies neither activity nor
anchor-safe descent.

Checker:
[`verify_dark_cartan_scalar_visibility_physical_landing_gate.py`](../computations/verify_dark_cartan_scalar_visibility_physical_landing_gate.py).

## 1. Why the double-visible scalar is diagonal on `e`

Let both endpoint quotient covectors select the same missing colour `c`.
An original scalar cell can affect the quotient at `u` only if its physical
edge is incident with `u` and its `u`-head has nonzero `c` coordinate.  The
same statement holds at `v`.  A single physical edge incident with both is
necessarily `uv`.  For a coordinate scalar column, double visibility
therefore forces

\[
                             A_{uv}^{cc}.                            \tag{2}

The checker audits all `28*9=252` decorated cells at `N=8`; (2) is the unique
double-visible type.

This is a rank statement only.  The target-augmented activity identity is

\[
             \sum_s \Delta_{us}C_s=-A_{uv}^{ba},\qquad b\ne a.       \tag{3}

Its right side is explicitly offdiagonal.  The cell (2) has `b=a=c`, so (3)
does not make it active.  Moreover it lies on `e` itself and cannot be the
second physical pair needed for a four-good overlap.

This is the smallest exact guard against the inference

```text
double quotient visibility => active physical landing.
```

At the augmented local-module level the guard already satisfies the assumed
complete equality: take one scalar column `JC=(1,1)`, `y=1`, and
`JG=(1,1)`, with zero terminal on the unit kernel.  Labeling that scalar by
(2) changes none of these equations, but supplies no activity coordinate.
This is a local typed guard, not a standalone complete GHZ source packet.

## 2. Pure-`c` reselection repairs rank, not activity

Suppose a nonzero pure-`c` matching avoids `e` and replace the selected
pure-`c` anchor by it.  Since the other two pure anchors already avoid `e`,
the edge is absent from the new anchor union.  The three selected diagonal
columns give rank three at both deleted endpoint stars:

\[
                         \operatorname{rank}P_e
                      =  \operatorname{rank}S_e=3.                    \tag{4}

The reselection changes no graph coefficient, so it does not delete an
anchor or infer new activity.

The marked critical occurrence on `e` is offdiagonal.  After reselection it
is an off-anchor cell, so (3) makes it good and forces at least one nonzero
determinant/cofactor fan witness.  If one such active mate lies outside the
new anchor union, its two deleted-star ranks are also three.  Together with
`e`, it gives the desired distinct-pair four-good active landing.

The double-visible diagonal scalar (2) does not improve this alternative.
It lands exactly when the separately forced active fan has an escaping mate;
if all nonzero mates remain anchor-contained, the Hall residual survives.

## 3. Exact split-visible classification

Let `C_u` be visible only in the `u` quotient and `C_v` only in the `v`
quotient.  Visibility records one local head on each column.  It does not
record:

1. whether their physical pairs are distinct;
2. whether those pairs avoid the reselected anchor union;
3. whether the columns are offdiagonal and hence enter (3);
4. whether they share the crossed centre required by the five-lock wedge;
5. whether their centre heads are distinct; or
6. whether both cofactor witnesses are nonzero.

The checker freezes two literal type guards.

* The two occupied diagonal cells of the selected pure-`c` avoiding matching
  at `u` and `v` have exactly the required split visibility, but are
  anchor-contained and have no activity forced by (3).
* The two offdiagonal cells `A_uv^{c d}` and `A_uv^{d c}` are split-visible
  in opposite quotients, but they occupy the same physical pair and cannot
  form a four-good wedge.

The split guard also satisfies (1) in the smallest augmented quotient
module: `JC_1=(1,0)`, `JC_2=(0,1)`, `y=(1,1)`, and `JG=(1,1)`, with the
terminal killing the unit kernel.  Hence complete equality does not supply
the missing support/cofactor data.

The exact positive split theorem is the pinned crossed-wedge statement:

> If the two fine-labelled scalar components occupy distinct off-anchor
> pairs, share a physical centre, have distinct centre heads, and carry
> nonzero cofactors, then the four deleted-star ranks are three and their
> centre minor is nonzero.  They form a distinct-head four-good active
> overlap.

Every phrase in this hypothesis is necessary; none follows from quotient
visibility alone.

## 4. The smallest residual is unchanged

There are two branches before the positive landing.

### Pure-target coloop

If no nonzero pure-`c` matching avoids `e`, then `e` is a literal coloop of
the pure-`c` matching support.  The physical `E2` alternative gives an
alternate target or an exchange carrier.  At `h=3`, the only
non-recombining four-hole carriers have a single cycle:

```text
C6 : 1
C8 : 6
```

The two `C4+C4` types recombine.  The sharp coloop residual is therefore an
anchor-contained source-typed `C6/C8` carrier.

### Avoiding matching, but no escaping active wedge

If pure-`c` reselection is available yet every nonzero private-site mate is
anchor-contained, apply the same-star five-lock theorem.

* A lock kernel is an exact simultaneous anchor-safe switch.
* A complementary crossed off-anchor pair is the positive four-good wedge.
* Otherwise the lock is injective and has no complementary crossed wedge.

The third item is the smallest Hall residual.  The scalar visibility
alternative adds no missing hypothesis to it: the unique double-visible
cell is diagonal on `e`, while split-visible cells can remain inside the
same injective incidence module.

Hence the complete failure statement is

\[
 \boxed{
 \begin{array}{l}
 \text{pure-}c\text{ coloop with anchor-contained }C_6/C_8\text{ carrier},
 \\
 \text{or injective five-lock, all active mates anchor-contained,}\ \\
 \text{and no complementary crossed off-anchor wedge.}
 \end{array}}
\tag{5}
\]

## 5. Proof-frontier consequence

The complete dark cancellation and double-quotient visibility now reduce to
the following physically honest flow:

```text
JG=JC*y and G double-visible
        |
        +-- no avoiding pure-c matching --> coloop C6/C8 carrier
        |
        `-- pure-c reselection --> e has rank (3,3), marked offdiag e is active
                                      |
                         +------------+-------------+
                         |                          |
                 active mate escapes       all active mates trapped
                         |                          |
                 four-good landing       lock kernel / crossed wedge /
                                          injective no-wedge residual
```

The scalar double/split alternative helps locate candidate physical columns,
but does not bypass the active-mate test.  The next constructive target is
therefore the residual carrier typing: identify the anchor-contained
`C6/C8` exchange with a column of the bidirectional lock complex, or prove
that an injective no-wedge lock cannot support the complete Cartan equality
(1).

## Scope

This theorem pins commits `00db7ee`, `ea8c864`, and `605f625` and audits
their rank, terminal-cancellation, pure-reselection, activity, crossed-wedge,
and coloop interfaces.  It proves the positive landing under explicit
physical support/cofactor hypotheses and gives exact counterguards to the
visibility-only shortcut.  It does not infer nonzero cofactors, off-anchor
incidence, or activity from visibility alone.

Run:

```text
python3 computations/verify_dark_cartan_scalar_visibility_physical_landing_gate.py
python3 -O computations/verify_dark_cartan_scalar_visibility_physical_landing_gate.py
python3 -I -S computations/verify_dark_cartan_scalar_visibility_physical_landing_gate.py
```

Frozen ledger SHA-256:

```text
e00c992ff68837327c9d6d2dc77daadbd2b65e670f086aebe0a6e415f7c47418
```

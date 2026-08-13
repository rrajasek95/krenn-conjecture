# The E14 private return has one silent primitive-placement branch

## Exact fork

For the canonical chart-`(1,1)` unary S-pair, write

\[
 a=1-v_{04}^{00},\qquad
 g=(p_{1,0}^1s_{1,1}^1)u_{35}^{11}v_{24}^{11}.
\]

The pinned sparse identity is

\[
                 B_{E14}=U+a g,\qquad R_{E14}=a g.       \tag{1}
\]

This gives an exhaustive localization fork.

1. On `V(a)`, `v04_00=1`, so `R_E14=0` and `B_E14=U`.  The target class is
   already represented by the old unary row.  Moreover `q04` is nonzero, so
   the literal complete-response path `O11--C21(q04)--O22` is present.
2. On `D(a)`, multiplication by `a` is invertible, so landing `R_E14` is
   equivalent to landing `g`.  The part with `v04 != 0` again has the crossed
   response path.  On the remaining closed fibre `v04=0`, one has `a=1` and
   `R_E14=g` exactly.

The identity `v04+(1-v04)=1` certifies exhaustivity.  Hence every branch is
response-bright except the literal silent fibre

```text
v04_00=0,       (H0-u)e_Eq ->
                (p1_0_1*s1_1_1)u35_11*v24_11.          (2)
```

Checker:
[`verify_h3_e14_private_return_localization_unit_fork.py`](../computations/verify_h3_e14_private_return_localization_unit_fork.py).

## What the complete E14 units do—and do not—prove

The existing complete-row theorems are very strong in their actual domain:

```text
minimal E14 bright charts                         9/9 units
one new internal cell after minimal E14      1,020/1,020 units
two new internal cells after minimal E14     57,291/57,291 units.
```

Thus, once (2) is realized as a complete physical row in the canonical
word/fine/repeated grade with core endpoints and at most two new internal
cells, an ordinary response/unary/`G22` source unit closes the packet.  No
separate active-rank theorem is needed in that envelope.

This cannot be invoked from the coefficient equality (1) alone.  The
`K_Eq` object and the E14 occurrence live in different source summands until
a physical `P2/iota` comparison supplies:

- a source-labelled map, not only a coefficient pushforward;
- the word/fine/repeated-grade agreement;
- all proper faces and endpoint components; and
- a bound placing any contamination in the zero/one/two-cell E14 envelope.

An unknown extra word component can contaminate both rows of an ordinary
unit.  Likewise a multisite or three-new-cell boundary is outside the exact
scope of the pinned unit theorems.  Therefore the units terminalize a
**typed** placement, but they cannot prove that placement.

## Response-bright branches

Any nonzero `q04` cell gives the source-labelled crossed base

```text
C21 = P3 | S1 | 04 | 25
```

and the two-C4 path `O11--C21--O22`, with complete physical word labels and
target zero on the crossed row.  In the pinned E14 zero/one/two-cell envelope
this is already an ordinary unit.  Outside that envelope it is a typed
response landing, not automatically a global terminal; later contaminants
can still require the active/diagonal-lock comparison.

The branch `V(1-v04)` is therefore harmless at coefficient level and
response-bright physically.  The only genuinely constructive branch is
`v04=0`, where no denominator or Bockstein issue remains: the return is the
primitive occurrence `g` itself.

## Shortest remaining theorem

Construct, on the silent fibre `v04=0`, the complete same-grade physical row
whose principal boundary is (2), retaining every forced target, labelled
residue, anchor, `q`, `W`, eta and sigma face.  If its support stays in the
pinned E14 envelope, the complete-row unit closes it.  Otherwise the first
extra component must be sent through the already typed crossed-response or
full augmented dual alternative.

This shows that word/fine placement is logically prior.  The remaining
problem is not division by `1-v04` and not the singleton companion; it is
source provenance for one primitive silent-fibre occurrence row.

## Scope

This is exact for the canonical `h=3`, word-`000101` E14 S-pair.  It does not
construct the physical row (2), bound arbitrary global contamination, or
promote the crossed-response landing outside the pinned local E14 fibres to
a final terminal.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
a805413bad45f999f08c183984432ca242d3ba8462da7b1f1aed14ad0fc91425
```

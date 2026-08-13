# Every determinant-bright zero mixed row reaches four-good or a coloop

## Result

Let `e` and `f` be the two adjacent physical pairs in a nonzero,
distinct-head, source-provenant active fan.  For each pure target colour
`c`, let `M_c` be the complete family of nonzero literal pure-`c` matching
monomials.  Then exactly one of the following holds.

1. Both `e` and `f` are avoided by some member of every `M_c`.  The two
   pairs have deleted-star ranks three at both endpoints, so the fan is a
   distinct-head active four-good overlap.
2. One of `e,f` is contained in every member of some `M_c`.  That physical
   pair is a literal pure-colour target coloop.

This removes two hypotheses from the evaluated-determinant landing.  The
nonzero offdiagonal Laplace factor need not be a simple edge of one chosen
anchor triple, and its active fan need not leave that chosen anchor union.
Those were sufficient ways to exhibit three surviving pure columns, but the
complete pure supports give the exact criterion.

It also lands the balanced-only determinant quotient on an actual zero
mixed row.  Balanced brightness need not contain an offdiagonal Laplace
factor.  Instead, the mixed hafnian equation forces some offdiagonal cell
elsewhere in the same row, and that cell enters the same private-site fan.

Checker:
[`verify_h3_active_fan_coloop_or_four_good.py`](../computations/verify_h3_active_fan_coloop_or_four_good.py).

## 1. Exact complete-support rank formula

Fix a physical pair `p=uv`.  If `Q in M_c` avoids `p`, then at endpoint
`u` it supplies the literal deleted-star coordinate

```text
(Q(u),c).
```

It supplies `(Q(v),c)` at `v`.  Coordinates with different target colours
belong to disjoint rows, even when two matching witnesses use the same
physical neighbour.  Consequently the rank certified at either endpoint is

\[
 \operatorname {rank}_{\rm pure}(p)
   =\#\{c:\text{some }Q\in M_c\text{ avoids }p\}.       \tag{1}
\]

Thus both endpoint ranks of `p` are three unless `p` is a coloop of one of
the complete pure matching supports.  Apply (1) separately to `e` and `f`.
If neither is a coloop, all four deleted-star ranks are three.  The fan's
already nonzero transition determinant, common hafnian cofactor, and
distinct centre heads give the required active four-good overlap.

The proof uses different pure matching witnesses for `e` and `f` when
necessary.  There is no requirement that one selected anchor triple avoid
both pairs simultaneously.

For the six-site packet, the checker exhausts all `2^15-1=32,767` nonempty
pure matching supports relative to adjacent pairs `e=01`, `f=02`.  Their
statuses are

```text
neither coloop       32,753
e coloop                  7
f coloop                  7
both coloops               0.
```

The last zero is structural: one perfect matching cannot contain adjacent
edges.  Across three colours this leaves 27 status assignments.  Exactly
the all-`neither` assignment is four-good by (1); each of the other 26 has a
literal named coloop.

## 2. The evaluated determinant entry is exhaustive

The evaluated unbalanced determinant theorem `5a12d88` supplies a nonzero
offdiagonal physical cell `e`.  The complete target-augmented private-site
identity and its transpose supply a nonzero distinct-head active fan at its
two endpoints.  Apply (1) to any one of the literal nonzero fan summands:

```text
unbalanced evaluated determinant
        |
        v
offdiagonal cell + physical private-site fan
        |
        +-- neither fan edge is a pure coloop --> four-good
        |
        `-- one fan edge is a pure coloop ------> coloop normalization gate.
```

There is one extra step for the balanced determinant quotient isolated by
`aeb7e75`.  On the word `001122`, the only physical perfect matching whose
three decorated cells are all diagonal is

```text
01:00 | 23:11 | 45:22.
```

It crosses each of the four balanced cuts.  Therefore, if every
offdiagonal cell of the mixed row vanished, its hafnian and each balanced
determinant would be, up to determinant sign, the same product

\[
                    A_{01}^{00}A_{23}^{11}A_{45}^{22}.             \tag{2}
\]

The actual source equation is `H_001122=0`.  Hence a nonzero balanced
determinant forces some nonzero offdiagonal cell somewhere in the complete
mixed row.  Applying the target-augmented private-site identity to that
cell gives the active fan, and then (1) gives four-good or a literal
pure-colour coloop.

This is deliberately a row-level argument.  The offdiagonal cell need not
be a Laplace factor of the chosen balanced determinant.  Determinant
brightness and the source equation are used together before the
private-site identity.

The exact guard from `aeb7e75` demonstrates the distinction.  It has
hafnian zero, six zero unbalanced determinants, and four balanced
determinants equal to three.  It nevertheless has ten nonzero offdiagonal
cells.  Thus it blocks an unbalanced-Laplace proof, but it enters the
source-row fan proof above.

The complete entry fork is consequently

```text
nonzero unbalanced determinant -> offdiagonal Laplace factor -> active fan
balanced-only determinant      -> H_mixed=0 -> offdiagonal row cell -> active fan
active fan                     -> four-good or literal pure-colour coloop.
```

Therefore these selected-anchor descriptions are no longer independent
determinant residuals:

* a non-simple selected edge;
* a wholly anchor-contained determinant/fan; and
* an injective five-lock with no complementary wedge.

The first two do not affect (1).  The five-lock is a useful selected-anchor
support-deletion theorem, but if its injective branch remains non-four-good
after all complete pure supports are admitted, (1) identifies the reason as
a literal pure-colour coloop.

## 3. What the existing target-coloop chain already consumes

The old `C6/C8` name should not be retained after source-labelled
normalization.

* `0556512` applies the shared-edge hybrid row to all 110 normalized
  target-coloop label packets.  It forces pure-target reselection, a
  nonanchor offdiagonal arm, or the decorated-anchor exchange.  Its last
  one-shared, anchor-contained multisite outcome lands on the already named
  global affine/Hall concentration interface; the theorem does not call
  that interface a four-good pair.
* `5a01b0a` uses the target-augmented punctured-C4 identity on the final
  sixteen zero-support rectangles.  It forces an alternate pure-one target
  matching or an offanchor offdiagonal exit.
* `0f2e367` uses the two conjugate hybrid rows to close its 270 normalized
  double-coloop packets by reselection or a distinct-head active four-good
  Hall wedge.

Thus a coloop already placed in those exact endpoint/common-`q` packets has
no remaining `C6/C8` topology or label-census branch.  It is routed to
reselection, four-good, decorated exchange, or the already named global
affine/Hall interface.  The last interface remains a source-landing theorem,
not a new `C6/C8` case.

## 4. The exact remaining coloop theorem

What is not proved is that an arbitrary coloop found by (1) has the physical
role assumed in those normalized packets.  The missing statement is:

> **Active-fan coloop normalization and landing.**  A literal pure-colour
> coloop on one edge of a source-provenant private-site fan either admits an
> anchor-safe complete-row relation or a free active carrier, or the complete
> mixed/response rows place it in the normalized target-coloop or conjugate
> double-coloop packet above.  In the one-shared multisite outcome of the
> normalized hybrid row, the same complete rows must furnish a target-line
> point, a free active carrier, or an anchor-preserving relation in the
> star/triangle/rectangle Hall normal forms.

The normalization conclusion includes common-`q` tail provenance, the
endpoint port orientation, the compatible response heads, and the relevant
four-hole or conjugate-hybrid rows.  None follows from the pure matching
matroids alone.  Even after those labels are available, `0556512` shows
precisely where an arbitrary-multisite affine/Hall landing can still be
needed.  The punctured-C4 and conjugate-double-coloop theorems close their
more specialized normalized outputs, but do not manufacture this data for
an arbitrary active-fan coloop.

The checker freezes the smallest sharp guard.  On six sites take

```text
M0 = 01 | 23 | 45,
M1 = 02 | 13 | 45,
M2 = 03 | 12 | 45.
```

Then `01` is a colour-zero coloop and adjacent `02` is a colour-one coloop;
both belong to the selected anchor union.  Give the local private-site data

\[
 p_e=q_e=p_f=C_f=1,\qquad q_f=0.
\]

The transition determinant is `Delta_ef=-1`, so the exact local identity

\[
                         q_e+\Delta_{ef}C_f=0           \tag{2}
\]

holds and the two centre heads are distinct.  Nevertheless (1) gives ranks
two on both physical pairs.  This is a matching-support and local
private-site guard, not a complete GHZ source.  It proves that no pure
matroid augmenting-path potential can establish the missing normalization;
one must use the complete mixed/response rows named in the theorem.

## Scope

The coloop-or-four-good theorem is uniform and source-exact once the
nonzero physical fan is supplied.  Both unbalanced and balanced-bright
determinant branches now supply such a fan on an actual zero mixed row.  The
finite audit is at the canonical six-site determinant grade.  The replayed
coloop closures are exact for their committed normalized `h=3` packets.
This note does not use terminal comparison data and does not silently
identify an arbitrary internal fan with an endpoint-affine target-coloop
packet.

Run:

```text
python3 computations/verify_h3_active_fan_coloop_or_four_good.py
python3 -O computations/verify_h3_active_fan_coloop_or_four_good.py
python3 -I -S computations/verify_h3_active_fan_coloop_or_four_good.py
```

Frozen ledger SHA-256:

```text
16840906f77635714d34915378e48c2d7c8902ba1a4ed520186aa28e49ab9f1a
```

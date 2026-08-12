# The silent unary C6 has one exact response-lock landing

## Result

Keep the exact minimum endpoint block and the silent extension

```text
R = 03 | 14 | 25
```

from `c44d784`.  The response rows see `R` only through its localized cell
`q25^00`.  That cell, together with the localized old direct cells
`q01^00,q34^00`, forces two literal nonzero augmented response bases:

```text
O11 = P0 | S1 | 25 | 34   in G11, word 110000,
O22 = P3 | S4 | 01 | 25   in G22, word 000220.
```

They share the identical decorated tail `q25^00`; after removing it, their
symmetric difference is the single alternating cycle

```text
P - 0 - 1 - S - 4 - 3 - P.                         (1)
```

The three distance-three chords of (1) are exactly `PS,04,13`.  The reduced
one-bad packet has no direct `PS` edge.  Therefore exactly one of the
following occurs.

1. Some decorated cell on `q13` is nonzero.  It gives the crossed base

   ```text
   C12 = P0 | S4 | 13 | 25
   ```

   and the literal typed path `O11--C12--O22` of two C4s.
2. Some decorated cell on `q04` is nonzero.  It gives

   ```text
   C21 = P3 | S1 | 04 | 25
   ```

   and the typed path `O11--C21--O22`.
3. Both physical edge tables `q13,q04` vanish.  Then (1) is one chordless,
   source-labelled two-chart diagonal C6 lock.  There is no further first-order
   matching shortcut hidden in the packet.

This is the requested complete response landing of the formerly silent
separator: crossed decoration synchronization, a direct-cap exit if that
edge is restored, or one finite diagonal lock.  Checker:
`computations/verify_h3_four_base_silent_c6_response_lock.py`.

## Literal source provenance

The four displayed zero-target coefficients are

```text
G11[110000] contains p1@0^1 s1@1^1 q25^00 q34^00,
G22[000220] contains p2@3^2 s2@4^2 q01^00 q25^00,
G12[100020] contains p1@0^1 s2@4^2 q13^00 q25^00,
G21[010200] contains p2@3^2 s1@1^1 q04^00 q25^00.
```

The first two products are localized by the selected endpoint entries, the
old pure-zero bases, and the nonzero monomial `R`.  For the two crossed
edges, `00` is only the displayed control coordinate: any nonzero decorated
entry of the same physical edge produces the same augmented matching base
in its corresponding literal crossed word.

For `q13`, consecutive bases share respectively

```text
{P0,q25} and {S4,q25};
```

for `q04` they share

```text
{S1,q25} and {P3,q25}.
```

Thus every arrow is a single physical C4 with the same decorated
complementary tail.  This is source-labelled matching exchange, not a
formal relabelling of response cofactors.

## Completeness of the split

Delete the common edge `25` and enumerate the fifteen perfect matchings on
`{P,S,0,1,3,4}`.  Exactly three are C4-adjacent to both diagonal
orientations:

```text
P0 | S4 | 13,       P3 | S1 | 04,       PS | 01 | 34.
```

The checker performs this enumeration and verifies the shared tails and
all four literal word labels.  Hence no other one-cell or one-chord response
repair has been omitted.

## Scope

- This theorem uses the complete unary plus four-response source labels;
  it does not replace an aggregate nonzero row by a chosen monomial.
- It classifies the exact first landing.  It does **not** claim that an
  arbitrary chordless diagonal lock web is closed; that is a separately
  named Theorem-A obligation.
- Extra terms in the four coefficient rows remain allowed.  They may give
  an earlier off-anchor/carrier exit, but cannot change the three-chord
  classification of (1).
- If the endpoint stars are literally concentrated, `7ccff7c` excludes the
  whole packet by the permanent-null cap before this split is needed.

## Verification

```text
python3 computations/verify_h3_four_base_silent_c6_response_lock.py
python3 -O computations/verify_h3_four_base_silent_c6_response_lock.py
python3 -I -S computations/verify_h3_four_base_silent_c6_response_lock.py
```

Frozen ledger SHA-256:

```text
9a87cb6b4f0a860de0fd3594e83be0e2050caba2668ce328118fd4cb0423df9b
```

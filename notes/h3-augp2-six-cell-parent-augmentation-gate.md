# The six cap cells augment only to unordered parents

## Outcome

Grant the coefficient-level physical formulas

```text
face 3 -> B4,       face 5 -> B1,
p_v+n_v=(Q,target,ores)=(0,0,-1).
```

Then the six selected `t*q_(v,N)` cells map with rank six to the six
unordered labels `(B4,N)` and `(B1,N)`.  This is a positive coefficient
augmentation.

It is not a literal augmentation to the ordered matching module

\[
 V_{parent}=\mathbb Q\{(p,s,N):p\ne s\}.             \tag{1}
\]

Every unordered `(B,N)` has two parent candidates, obtained by exchanging
the `P` and `S` endpoint roles.  Endpoint-role forgetting therefore has
rank six on the selected twelve parents and a six-dimensional odd kernel.
Neither the `AB` nor the `AC` colour-root path chooses one endpoint
orientation.

Even choosing the canonical rational endpoint-even section does not give a
chain augmentation.  The first enriched boundary is

\[
 dG_0=(H-u)_{response},\qquad
 dr_0=(H-u)_{Eq,cap}.                                 \tag{2}
\]

These become equal only after forgetting the operation and `Eq` labels.
With those labels retained they have rank two, separated by `(1,-1)`.

Exact checker:
[`verify_h3_augp2_six_cell_parent_augmentation_gate.py`](../computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py).

## Literal parent enumeration

Use six intrinsic sites `0,...,5`.  The fixed labels are

```text
B1={0,1},       B4={2,3}.
```

For a hole `{p,s}`, let `N` run through the three perfect matchings of its
four-site complement.  The selected cells and their two parents are:

| cap cell | parent (M^+) | parent (M^-) |
|---|---|---|
| `t*q_(3,01|45)` | `P2|S3|01|45` | `P3|S2|01|45` |
| `t*q_(3,04|15)` | `P2|S3|04|15` | `P3|S2|04|15` |
| `t*q_(3,05|14)` | `P2|S3|05|14` | `P3|S2|05|14` |
| `t*q_(5,23|45)` | `P0|S1|23|45` | `P1|S0|23|45` |
| `t*q_(5,24|35)` | `P0|S1|24|35` | `P1|S0|24|35` |
| `t*q_(5,25|34)` | `P0|S1|25|34` | `P1|S0|25|34` |

Here the first three are `face 3/B4`, and the last three are `face 5/B1`.
All twelve displayed parents are distinct members of the canonical
90-occurrence module.

For the first cell, the earliest ambiguity is

\[
 P2|S3|01|45\quad\text{versus}\quad P3|S2|01|45.     \tag{3}
\]

The primitive covector

\[
 (P2|S3|01|45)^*-(P3|S2|01|45)^*                   \tag{4}
\]

kills the endpoint-even image and reads `+1` or `-1` on either termwise
choice.  The other five cells give five disjoint translates of (4).

## Exact ranks

The granted `B4/B1` label has rank two, while the residual matching label
has rank three.  Their Cartesian product has rank six:

```text
six cap cells -> six unordered (B,N) parents       rank 6.
```

On the ordered parent module:

```text
selected ordered parents                            12
endpoint-forgetting rank                             6
endpoint-odd kernel                                  6
termwise sections                                  2^6
rank of every termwise section                        6.
```

No termwise section is fixed by endpoint transpose.  Over (mathbb Q),
the unique normalized endpoint-even section is

\[
             (B,N)\longmapsto {M^+_{B,N}+M^-_{B,N}\over2}. \tag{5}
\]

It is split monic after endpoint forgetting and has rank six, but it is an
average rather than reinsertion to one literal matching parent.

The (K_{Eq}) correction does not alter this result.  It changes the
selected cap signature from

```text
p=(-1,0,-1),       n=(+1,0,0),       p+n=(0,0,-1)
```

in `(Q,target,ores)`, and has no endpoint-orientation coordinate.  Thus it
closes the scalar `Q` face but cannot choose between the two parents in
(3).

## Word/root paths do not repair the lift

Attaching the root label gives four formal candidates per cap cell:

```text
AB:M+, AB:M-, AC:M+, AC:M-.
```

The root labels distinguish the two colour-root receiving sections; they
do not distinguish `P/S` orientation.  In the strongest quotient granting
every diagonal word/head/fine/repeated/operation repair, the exact ranks are

```text
diagonal base                                      24
+ AB section                                       25
+ AC section                                       25
+ one root-forgetting aggregate                    25
+ both separately labelled sections                26.
```

The two surviving characters are
`omega_AB^Hom` and `omega_AC^Hom`.  Current root/Weyl and cap operations
generate only the diagonal corners, so `Hom(response,cap)=0`.

## First chain boundary and next protected face

Suppose nevertheless that one chooses the symmetric section (5).  In the
smallest enriched parent base retaining operation and `Eq`, equation (2)
has columns

```text
coordinate order       (H-u)_response  (H-u)_Eq,cap
dG0                              1                0
dr0                              0                1.
```

They have rank two.  The primitive separator `(1,-1)` proves that the
coefficient-common occurrence module is not a common *chain* base.  This is
the first boundary after the rank-six coefficient augmentation.

After adjoining that mixed boundary, the next protected obstruction is the
known pair of target normals.  The two local diagonal target lines have
rank two; adjoining the `0112` and `0121` mixed normals raises the rank to
four.  They are independently detected by

```text
X_00211122^*,       X_00111222^*,
```

with pairing matrix `diag(2,2)` on the two normals.  The scalar
`B4/B1`/`K_Eq` formulas do not supply these target cone faces.

## Frontier

The shortest positive datum is one two-root, endpoint-even word-changing
mapping cylinder whose degree-zero face lifts the six unordered `(B,N)`
labels and whose first boundary identifies the two rows in (2).  It must
also carry the two mixed-target cone faces.  This object is precisely the
literal cap augmentation `epsilon_C`; it is not a consequence of the
coefficient label or (K_{Eq}) identities.

Verification:

```text
python3 computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py --mode full
python3 computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py --mode structural
python3 -O computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py --mode structural
python3 -I -S computations/verify_h3_augp2_six_cell_parent_augmentation_gate.py --mode structural
```

Frozen ledger SHA-256:

```text
67385fda43c7c65bbf72d0ccb4f656f0dc21b86f8a3231f798b3d83b18732b50
```

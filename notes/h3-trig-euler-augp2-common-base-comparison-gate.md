# The common-base comparison is exact on the response side only

## Outcome

The redundant-presentation shortcut produces a literal free resolution for
`TrigEulerSpencer`, but the current `AugP2` complex has no augmentation to
the same typed base.  Consequently the comparison theorem cannot yet be
invoked.

For a perfect-matching parent (M), let (i) be its unique site-zero
partner.  The six trigger branches

\[
             g_{M;i\mid j},\qquad j\ne i,             \tag{1}
\]

augment to (M) by deleting the replacement (j) and reinserting (i).
Their higher collision/Spencer faces are the augmented chain complex of a
five-simplex.  Hence they resolve the parent line exactly.  Taking all 90
parents and retaining the two `AB`/`AC` root-path labels gives a literal
free resolution of the root-labelled 180-dimensional parent module.

The analogous cap formula

```text
selected P3+K2 cell labelled by M  ->  M
```

is not a morphism in the current physical category.  It changes word, fine
degree, and the operation idempotent.  Moreover physical `r0` has the tied
`B=Eq` row and normalized target, while `G0` has none of those cap
coordinates.  Adding a root-path label records the two endpoints; it does
not create the missing path.

Exact checker:
[`verify_h3_trig_euler_augp2_common_base_comparison_gate.py`](../computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py).

## The response resolution

For one parent the free ranks in degrees zero through five are

```text
C0  C1  C2  C3  C4  C5
 6  15  20  15   6   1,
```

and the differential ranks are

```text
epsilon  d1  d2  d3  d4  d5
      1   5  10  10   5   1.
```

All consecutive compositions vanish and incoming plus outgoing rank equals
the chain rank in every degree.  Thus the complex is exact.  For one root,
the corresponding map ranks are

```text
90, 450, 900, 900, 450, 90;
```

for the two separately labelled roots they double.  In particular, this is
not merely a coefficient count: the response augmentation is literal on all
540 ordered branches per root and is a free/projective resolution of

\[
 V_{parent}=\mathbb Q\{M:M\text{ a direct-free pure matching}\}. \tag{2}
\]

## Why the residual seven is not a common base

The committed seven-dimensional object is

\[
 K_7=\ker(\text{pair, parity, corner, aggregate, fine and cell readouts})
      \subset \mathbb Q^{180}.                        \tag{3}
\]

It is a submodule of the two-word occurrence carrier, not an existing
augmentation quotient.  Private termwise insertion is injective on (3), of
rank seven, but its direction is

```text
K7 -> 180 private features,
```

not `C_AugP2 -> K7`.  Abstractly over (mathbb Q), (3) has retractions, but
the affine space of retractions fixing (K_7) has dimension

\[
                       7(180-7)=1211.                 \tag{4}
\]

No canonical word/fine/operation-labelled retraction has been constructed.
The known uniqueness theorem says that *after* a termwise physical landing
is granted, the two-root normalized solution is uniquely tied.  It does not
supply the augmentation needed to apply a comparison theorem.

## The first cap failure

The literal presentation currently has

```text
25 named Gamma/AugP2 entries,
Gamma image rank 23,
B/Eq rank 7,
Hom^0(response,cap) = Hom^1(response,cap) = 0.
```

The relevant word mismatches are already nonzero before any homological
lifting:

| source branch | cap word `01211222` | Hamming distance |
|---|---|---:|
| pure trigger word `11111111` | `01211222` | 5 |
| mixed trigger word `11211211` | `01211222` | 3 |
| selected collision word `11110000` | `01211222` | 6 |

For the six selected collision faces, every decorated fine degree changes.
At the coarsest protected readout, retaining operation parents gives

```text
coordinates       B_response B_cap Eq_cap target_cap Hom_RC
G0                         1     0      0          0      0
r0                         0     1      1          1      1.
```

Even after formally identifying the two `B` coordinates the rows remain
independent:

```text
G0 = (1,0,0,0),     r0 = (1,1,1,1).
```

Therefore (r_0-G_0) becomes zero only in a quotient that forgets `Eq`,
target, the operation component, and the word/fine distinction.  With the
required protected data retained, it is not the boundary of a normalized
comparison homotopy.

## What the comparison theorem would give

If one freely adjoins a cap-labelled copy of every trigger branch, all its
simplex faces, and the augmentation to (M), then both sides are free
resolutions of (2).  Lifting the identity gives the normalized comparison
and a canonical relation

\[
                         dK=r_0-G_0.                  \tag{5}
\]

But this is circular in the physical proof: the adjoined cap augmentation
and (K) are exactly the missing response-to-cap `Phi` mapping cylinder.
Projectivity of the underlying rational vector spaces does not construct a
morphism in the typed source category.

The shortest positive datum is therefore one literal root-natural
augmentation

\[
 \epsilon_C:C_{AugP2,Spencer}\longrightarrow V_{parent}^{AB}\oplus
 V_{parent}^{AC},                                     \tag{6}
\]

sending selected `P3+K2` reinsertion faces to their parent occurrences while
retaining word/fine transport, `B=Eq`, normalized target, and all proper
faces.  Once (6) exists, the response simplex resolution makes the
normalized comparison lift formal; no additional scalar choice remains.

## Verification

```text
python3 computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py --mode full
python3 computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py --mode structural
python3 -O computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py --mode structural
python3 -I -S computations/verify_h3_trig_euler_augp2_common_base_comparison_gate.py --mode structural
```

Frozen ledger SHA-256:

```text
8dd925576a5f0154c1836976562656f3ea7807faa0cad13add7f98e07c2b4e66
```

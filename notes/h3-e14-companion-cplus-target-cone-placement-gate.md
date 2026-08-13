# A singleton C-plus companion kills the first dual but not the E14 target

## Result

Grant the strongest literal placement of the generic even Cartan/`C+`
principal face at the one E14 target coordinate seen by the old 22-support
dual:

```text
(p1_0_1,s1_1_1) u05_01 v13_01 v24_11.
```

This kills that dual, but the complete twelve-tail target is still outside
the augmented image:

```text
old complete rows                  rank 269
+ singleton companion             rank 270
+ complete E14 target             rank 271.
```

The two-term reduced E14 target is unchanged. A new rational covector with
support 42 kills all 269 old columns and the granted companion, while reading
`-1` on the target. Its primitive integral normalization reads `-60`.

Checker:
[`verify_h3_e14_companion_cplus_target_cone_placement_gate.py`](../computations/verify_h3_e14_companion_cplus_target_cone_placement_gate.py).

## Where the obstruction moves

The old covector concentrated its entire target pairing on the displayed
companion. After adjoining that unit, the new covector vanishes there and its
target pairing is

```text
decorated core  u05_01 v24_11 v34_10       -1/4
new mate        u05_01 v23_01 v24_11       -3/4.
```

Thus the common decorated core becomes visible only after the first
companion direction is supplied. This is a genuine rotation of the cokernel,
not closure of the E14 landing.

There is a stronger target-tail statement. Modulo the 269 old rows, the
twelve canonical target-coordinate unit classes are independent. Adjoining
any eleven of them still leaves a nonzero target remainder; all twelve are
required. Therefore no strict subset of the canonical target tails, and in
particular no singleton coordinate section, can represent the full E14
target.

This conclusion is restricted to new principal columns supported on those
twelve canonical coordinates. A source cell with additional off-target E14
coordinates could satisfy different relations and is not ruled out.

## The Cartan–Koszul proper faces

Let

```text
E = 2 D_root tensor v,
D_root=(-1,1,-1,1),
v=(B1+B4)/2.
```

In the rows `(principal E14, lower/private, reduced Eq, mixed target,
word-resolved ores)`, the formal target/Eq triangle is

```text
lower endpoint path       = (0,0, 0,+E, 0)
C_plus/J* Cartan          = (c,0,-E,-E, 0)
clean K_Eq correction     = (0,0,+E, 0, 0)
sum                       = (c,0, 0, 0, 0).
```

So the `+2D(H0-u)Eq` correction has the correct sign and cancels the reduced
Eq face exactly. The failure is not an Eq-sign error.

The nearest checked physical lift of the clean Eq correction is instead

```text
(lower/private, Eq, target, word-ores)=(+E,+E,0,-E).
```

After adding the Cartan and endpoint terms, the first proper-face residual is

```text
lower/private +E,    word-resolved labelled ores -E,
```

on eight nonzero root-label coordinates. The old-block primitive detectors
are the labelwise `lower-Eq` and `-Eq+W+target-ores` covectors.

Conditional hidden faces `lower=-E` and root-decorated `d_even` with
`ores=+E` cancel this pair. Even after granting both, however, a singleton
principal companion remains insufficient by the 42-support dual above.

## Relation to the positive private-return assembly

The positive theorem in commit `5006a00` uses a different principal
placement. It proves the exact identity

```text
B_E14 = U[000101]*v24_11 + R_E14,
R_E14 = (p1_0_1*s1_1_1)u35_11 v24_11(1-v04_00).
```

Here `R_E14` is precisely the full two-term quotient residual of the old
E14 target, not the visible companion unit. Placing the physical `K_Eq`
lower/private face on `R_E14` and adding the already physical unary column
produces all twelve E14 tails, including the companion. That construction is
not contradicted by this no-go; it is the correct way around it.

The comparison is therefore sharp:

```text
direct placement on companion          fails; new 42-support dual survives
placement on private return R_E14      lands the full target conditionally
```

After the private-return placement, the first remaining proper row is the
word-resolved labelled ordinary residue `-E`.

## What remains after the positive placement

Neither `z_cap` nor an aggregate scalar residue is the required labelled
section:

- `z_cap` is one scalar ordinary-residue coordinate in the cap grade;
- `d_even` is the fixed-plane six-label vector `(B1+B4)/2`, repeated with
  root coefficients `2D_root`.

They occupy independent row blocks. A pure same-grade `d_even` section
cancels `-E`; `z_cap` does not. Conversely, `d_even` has zero scalar cap
residue and cannot supply `z_cap`.

The current `d_even` frontier is still conditional. The physical Cartan
residue span is detected in every root word by

```text
chi=(0,1,-1,0,1,-1),       chi(v)=1.
```

Thus sigma-evenized odd Cartan cells cannot replace `d_even`. The direct-free
denominator packet has both conditional face-3/`B4` and face-5/`B1`
memberships; the tilted packet has only one. No committed full-source
occurrence-to-label map promotes those coefficient memberships to the needed
protected-zero section.

The exact next residue theorem is therefore:

> After the private-return placement, construct one same-grade pure
> `d_even` section (equivalently both fixed `B1` and `B4` sections), or extend
> the fixed-plane covectors through the complete augmented comparison.

Separately, the cap lane still needs the scalar `z_cap` placement, or its
Omega/rootless eta-compatible Fredholm mate. These are two distinct rows of
the eventual three-object mapping cone.

## Scope

This is exact for the canonical chart-`(1,1)` word-`000101` E14 first-hit
module and the generic `alpha*beta != 0` `C+` packet. It does not construct
the private-return placement, the pure `d_even` or `z_cap` sections, the
`beta=0` family, or a global physical terminal.

Run normally, optimized, and isolated/no-site. Frozen ledger SHA-256:

```text
8ac9ba66d12df11541b785f0abf1578054aec292dc6dd523c28bad8fbad03e52
```

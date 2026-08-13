# `1-v04` is a mixed-row coefficient, not a restriction of `H0-u`

## Result

The conditional placement

\[
 (H_0-u)e_{\rm Eq}\longmapsto
 (p_1s_1)u_{35}v_{24}(1-v_{04})
\]

is coefficient-exact but has no direct source provenance in the committed
charts.

In the canonical universal E14 presentation, the genuine normalized pure
unary source row is

\[
 U_{000000}-1=v_{04}^{00}v_{13}^{00}.                \tag{1}
\]

By contrast,

\[
 -1+v_{04}^{00}                                      \tag{2}
\]

is only the coefficient of the pivot `u35_11` inside the complete mixed
word-`000101` unary row, which has fourteen terms.  The proposed
`1-v04_00` is minus (2).

Extracting one monomial coefficient from a mixed row is linear but not
multiplicative, hence is not an algebra/source-presentation map.  Therefore
(2) cannot be declared the restriction or cofactor of `H0-u`.

Checker:
[`verify_h3_e14_keq_private_factor_localization_provenance_gate.py`](../computations/verify_h3_e14_keq_private_factor_localization_provenance_gate.py).

## 1. The two polynomials are genuinely different

Two specializations already separate (1) and the proposed factor:

```text
v04=0:       v04*v13=0,   1-v04=1,
v04=v13=1:  v04*v13=1,   1-v04=0.
```

Moreover, coefficient extraction cannot define a ring map: if `c` extracts
the coefficient of `u35`, then

```text
c(u35)=1,      c(u35^2)=0 != c(u35)^2.
```

The type mismatch agrees with the existing source separator:

```text
reduced-Eq normal source word   01211222 (internal 12112),
E14 mixed unary word            000101.
```

The shared decorated `2K2` core is real, but no committed map transports the
whole word/fine/repeated source row.  Selecting (2) is precisely the missing
`P2/iota` operation, not a chart restriction already present.

## 2. The localization split

Put `A=1-v04`.

### On `D(A)`

At the exact witness `v04=0`, `A=1`.  The specialized first-hit module has
rank 224, and the E14 target remainder equals the same nonzero private
generator.  Thus inverting `A` merely identifies the target and private
classes; it does not kill either.

There is a sharp ideal-theoretic alternative.  If a source-presentation map
really sent the source equation `H0-u` to `A`, then after localizing at `A`
the target source ideal would contain the unit `A/A=1`.  That is the scalar
unit arm, not a nontrivial `K_Eq` comparison.  Hence a positive direct map on
`D(A)` either closes immediately by a unit or cannot have the proposed ideal
image.

### On `V(A)`

At `v04=1`, the specialized first-hit rank is 257.  The E14 target reduces
to the old unary column, but the private generator still has nonzero
remainder.  Ordinary restriction sends the proposed image of `H0-u` to
zero, so it supplies no private/conormal face.

Retaining a nonzero conormal would require a derived excess/Gysin class for
the divisor `A=0`.  That is a new construction, and `A` is not itself a
complete physical source equation whose conormal is already available.

There is a useful branch shift: `v04=1` makes the physical `q04` table
nonzero.  Under the pinned silent-C6 response-lock hypotheses this gives the
literal crossed path

```text
O11 -- C21(q04) -- O22.
```

That is an existing crossed-C4 landing, not the desired pointed comparison.

## 3. What the E14 unit theorems do cover

Once a class is physically placed in a canonical E14 chart, the exact unit
theorems close every one-, two-, or three-new-internal-cell support.  The
two- and three-cell counts are

```text
57,291,
2,126,208.
```

The three-cell result exhausts the local internal monomial degrees, but it
explicitly does not prove arbitrary simultaneous-cell emptiness: the unit
witness changes with the support, and there is no universal two-row
identity.

Consequently these theorems give a positive sparse-support exit only after
the missing physical word/fine/repeated placement is constructed.  Neither
localizing at `A` nor extracting (2) performs that placement, and the unit
theorems do not close a fully contaminated first-hit chart.

## Shortest remaining alternatives

- On sparse E14 supports, construct the actual `P2/iota` map; the existing
  unit theorem then terminalizes the branch.
- On `D(A)`, an ideal-preserving map with image `A` is automatically the
  scalar-unit arm.
- On `V(A)`, use the crossed-`q04` response landing where applicable, or
  construct the genuinely derived excess conormal.
- On arbitrary simultaneous E14 support, a universal triangular/standard-
  basis exhaustivity theorem is still required in addition to placement.

## Scope

This is exact for the canonical chart `(1,1)`, its `v04=0,1` first-hit
specializations, the direct-free/E14 word separator, and the pinned sparse
E14 unit results.  It is not a no-go against a new derived excess map or a
future full-support standard basis.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
1055ec63a7f6bcbef1025afa0108121473f4891095b14712e8505544028d5a70
```

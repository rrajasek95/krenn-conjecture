# Original-Hasse duality gives a local separator, not yet a physical terminal

## Verdict

One may run exact duality on an exhaustive physical boundary map in the
original `Hasse[2](D,Q01)` response object. If the selected second-Hasse
class is outside its image, this produces a genuine local output covector.
This avoids constructing a primal filler before discovering the dual.

It does **not** by itself produce the accepted physical terminal. The latter
is a covector on the complete augmented correction codomain and must
annihilate every admitted physical source column. Extending the local
covector by zero fails already on the old cap column

\[
 r0_j=B_j+Eq_j+\operatorname{target}_j-\operatorname{ainc}.
\]

If the local covector has value `mu_j` on the cap corner, its zero extension
has value `mu_j` on `r0_j`. The known-row extension is forced:

```text
target_j = -mu_j,   W_j = -mu_j,   ores_j = mu_j,
ridge = -sum_j alpha_j*mu_j,       q = ainc = Eq = 0,
alpha = (-1,1,1,-1).
```

For the Gate-II character `delta=(1,1,-1,-1)`, `alpha.delta=0`. Thus its
ridge, `q`, eta and sigma coefficients all vanish. The obstruction is not a
new nonzero ridge face; it is extension across the complete physical map.

Checker:
[`verify_h3_gate_ii_h2_local_duality_terminal_typing_shortcut_gate.py`](../computations/verify_h3_gate_ii_h2_local_duality_terminal_typing_shortcut_gate.py).

## The proposed inclusion is not definitional

The notation `B` hides two different objects.

The original second-Hasse survivor is

```text
source head        11:110000 parent fan response block
operator grade     Hasse[2](D,Q01)
residual sites     2345
local face         q23*q45 + q24*q35 + q25*q34
coordinates        three matching occurrences
operation profile  DQ (or transported PS), retained.
```

The corners in the cap extension are instead

```text
source word        1211222 after deleting the distinguished endpoint
source type        relative r0/T/rho plus Cartan/HPL
relative grade     labelled repeated P3+K2, faces-(3,5)
coordinates        four cap corners
literal boundary   90 complete features per B_j, 360 in alpha aggregate
extra rows         Eq,target,ainc,W,ores,ridge,eta,sigma,q.
```

These are different word/fine/direction/repeated idempotents and even have
different occurrence arities. The three occurrences of `H2345` are not the
four complete `B_j^cap` boundaries. The definition of `r0_j` starts only
after a cap corner has been selected; it does not identify a DQ-tagged
Hasse tail with that corner.

Accordingly, the map

\[
                 i:Y_{H2}\longrightarrow Y_{aug}
\]

in the augmented-duality theorem is a hypothesis, not a definitional
inclusion already supplied by the Hessian obstruction. It must be a
source-labelled comparison preserving the word, fine, repeated and common
tail data. Equivalently, one may bypass a primal `i` only by directly
constructing a covector on the complete augmented map whose restriction is
the local Hasse covector.

## What the shortcut does and does not remove

The order of work can legitimately be reversed:

```text
exhaustive original Hasse[2] map
  -> selected class is filled, or obtain local psi_H2
  -> extend psi_H2 across the full augmented map
  -> accepted physical terminal.
```

So “placement before duality” is not logically necessary. What remains
necessary is the typed comparison/dual-extension theorem. The explicit
`4373ae6` formula settles all known cap/Cartan rows once the four corner
values are physically defined, and on `delta` it adds no ridge or terminal
packet. It does not define those corner values or prove annihilation of the
remaining literal response/block-projector and downstream columns.

The sharp remaining statement is therefore one of:

1. construct the source-labelled Hasse-to-augmented comparison `i`; or
2. extend the local Hasse covector directly over the exhaustive augmented
   source map, retaining its detected value.

Without one of these, the local covector is an exact coefficient/Fredholm
obstruction in the original Hasse object, but not the source-terminal or
Macaulay functional used by the global proof.

## Scope

This is exact for the canonical `h=3` original Hasse packet and normalized
cap--Cartan packet. It does not construct the comparison or assert that the
displayed known-row covector annihilates every unenumerated same-grade
physical column.

Run normally, optimized, and isolated/no-site. The checker records the
frozen ledger digest.

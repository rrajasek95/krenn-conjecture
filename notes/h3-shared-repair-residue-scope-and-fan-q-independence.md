# Gate I still needs two labelled-residue images; the fan `q` square does not supply them

## Result

The shared-repair anchor-fibre alternative of `8e1f858` is conditional on a
source-typing statement which was granted in its generous 25-row cone but is
not in the committed physical inventory.  It uses six columns

\[
                         d_{{\rm ores},i},\qquad 0\le i<6,
\]

whose ordinary-residue images are the six pure-multiplier units.  The
committed clean inventory and the `abcde` target-normalization theorem have
only one aggregate scalar ordinary-residue column.  They do not define a
section from that scalar row into the six multiplier labels.

The endpoint-odd Cartan cell is physical in the correct canonical
faces-`(3,5)` repeated grade, but it contributes only the line

\[
                         (1,0,1,-1,0,-1).             \tag{1}
\]

Even after adjoining the guessed aggregate direction `(1,1,1,1,1,1)`, the
known residue span has rank two.  It contains none of the four normalized
shared-repair directions

\[
 e_1,\quad e_4,\quad {e_0+e_5\over2},\quad
 {e_2+e_3\over2}.                                   \tag{2}
\]

Thus the exact remaining source statement is two orbit images: one fixed
choice from `e1/e4` and one paired choice from the last two vectors in (2),
modulo the physical Cartan line (1).

Checker:
[`verify_h3_shared_repair_residue_scope_and_fan_q_independence.py`](../computations/verify_h3_shared_repair_residue_scope_and_fan_q_independence.py).

## Why the anchor-fibre theorem does not remove this input

For a physically constructed labelled residue companion, the old columns
would give

\[
 x_v=R_v-T_v-\rho_v+d_{{\rm ores},v}
     =(\operatorname {low}=v,\operatorname {ainc}=-1,
       W=\operatorname {tgt}=\operatorname {ores}=0). \tag{3}
\]

Then the desired protected-zero repair `U_v` differs from `x_v` by pure
physical anchor incidence.  Nonzero anchor on the protected kernel gives
the existing relative generator; zero anchor gives the physical primitive
dual, refined by `99f926a` to separator or unit-kernel outcomes.

But this dichotomy begins after (3) is a source chain.  A scalar symbol
`d_ores` does not attach a fixed or paired pure-multiplier label to it.
Without that labelwise source column, `U_v-x_v` is not a typed kernel
element and the anchor alternative cannot be invoked.

## The fan `Phi/q` theorem is logically independent

Gate II asks for a protected comparison

\[
                         J_0\Phi=A J                  \tag{4}
\]

and literal dual readouts

\[
                         q=M-a.                       \tag{5}
\]

Equations (4)--(5) constrain a comparison of protected maps and one
covector class in `L*/row(J)`.  The missing Gate-I datum is instead a
primal section of a six-dimensional labelled ordinary-residue map.

The checker freezes this distinction exactly.  Keep `Phi=I`, the protected
square, `M`, `a`, and hence `q=M-a` fixed.  Compare two ordinary-residue
maps on the same six-dimensional source:

```text
good map: identity, rank 6;
bad map:  every coordinate lands on (1,1,1,1,1,1), rank 1.
```

Both have identical, defect-zero `q` comparison data.  The bad map contains
none of the four directions (2).  Therefore the fan-grade protected `Phi`
and literal `q=M-a` rows do not imply the two labelled-residue sections,
even as linear algebra.

## What a genuinely uniform theorem would say

The two gates can still be unified, but only by strengthening the source
theorem.  A uniform **augmented odd shifted-label theorem** would have to:

1. transport the central word idempotents, fine grade, endpoint orientation,
   and common tail;
2. prove the protected square (4) and the physical `q` comparison (5); and
3. prove a separate labelled ordinary-residue square whose image contains
   one fixed and one paired direction from (2).

The third clause is not a consequence of the first two.  This also explains
why a relabeling/base change is insufficient: the Gate-I cut involution
exchanges its two physical word blocks, whereas the fan endpoint
transposition fixes each pure/mixed word block.  A uniform construction
must be a relative word-changing source cell, not merely an isomorphism of
the abstract odd sign representations.

## Scope and verification

This is an exact source-scope correction and independence guard.  It does
not rule out the two residue chains in a larger relative source resolution.

Run:

```text
python3 computations/verify_h3_shared_repair_residue_scope_and_fan_q_independence.py
python3 -O computations/verify_h3_shared_repair_residue_scope_and_fan_q_independence.py
python3 -I -S computations/verify_h3_shared_repair_residue_scope_and_fan_q_independence.py
```

Frozen ledger digest:

```text
ec9df0c2cd44e7631adeaa0ea9f4454a9598ad596ed8820dd580e551a93e8188
```

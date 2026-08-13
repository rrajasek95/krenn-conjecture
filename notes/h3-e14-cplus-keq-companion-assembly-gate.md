# The Cartan–Eq triangle reaches the E14 companion exactly after one private placement

## Result

The endpoint-even target-bearing cone and the canonical reduced-Eq face do
not by themselves construct the E14 word change.  In the quotient rows

```text
(lambda_E14, reduced Eq, mixed target, word-resolved ores),
```

one normalized nonzero root/label component is

```text
C_plus target cone     = ( 0,-1,-1, 0),
clean K_Eq face        = ( 0,+1, 0, 0),
sum                    = ( 0, 0,-1, 0).
```

The required E14 boundary has first coordinate `-1`.  Therefore the known
two columns have rank two and the required boundary raises the rank to
three.  The primitive dual `(1,0,0,0)` proves that the first unfilled row is
the occurrence/private row, before residue, anchor, or ridge.

Checker:
[`verify_h3_e14_cplus_keq_companion_assembly_gate.py`](../computations/verify_h3_e14_cplus_keq_companion_assembly_gate.py).

## The exact canonical S-pair identity

Let `B_E14` be the twelve-tail first-hit target and let `U` be the old
word-`000101` unary column multiplied by `v24_11`.  Exact sparse subtraction
gives

\[
 B_{E14}=U+R_{E14},                                   \tag{1}
\]

where

\[
 R_{E14}=(p_{1,0}^1s_{1,1}^1)
          u_{35}^{11}v_{24}^{11}(1-v_{04}^{00}).      \tag{2}
\]

The companion

```text
(p1_0_1,s1_1_1) u05_01 v13_01 v24_11
```

has coefficient `-1` in both `U` and `B_E14`, and coefficient zero in
`R_E14`.  The first-hit functional has values

```text
lambda(U)=0, lambda(R_E14)=-1, lambda(B_E14)=-1.
```

This explains exactly what the Eq comparison must do.  It need not create
the companion directly.  It must place its lower/private face on (2); the
already physical unary column then supplies every tail of `B_E14`, including
the companion with the required coefficient.

The obstruction is not another target-normal coordinate.  Even after
adjoining independent unit columns on all 24 unary and `G11` target-readout
coordinates, the old rank rises `269 -> 293` but the reduced target remains
exactly (2).

## Candidate private placement

The necessary selected-component label map is

\[
 H_0-u\longmapsto1-v_{04}^{00},\qquad
 e_{\rm Eq}\longmapsto
 (p_{1,0}^1s_{1,1}^1)u_{35}^{11}v_{24}^{11}.          \tag{3}
\]

The coefficient normalization is exact: in

\[
 2D_{\rm root}\otimes(B_1+B_4)/2
\]

all eight nonzero word-label coefficients are `+/-1`, so (3) has no scalar
or denominator mismatch.  What is missing is its source provenance: the
central derived Eq object and the E14 private occurrence are different
word/operation summands until `P2/iota` supplies (3).

Thus the full first-hit count for the formal cone is

```text
269 + 2 = 271  ->  272
```

after adjoining the desired E14 boundary.  This is the exact occurrence
rank jump, not a projected target/Eq defect.

## What happens if the occurrence placement is granted

The nearest checked physical dressing of the Eq face has

```text
(lower/private, Eq, W, target, word-ores, anchor)
       =(+E,          +E, 0, 0,      -E,       0).
```

Under (3), its selected quotient column is

```text
placed K_Eq = (-1,+1,0,-1).
```

Adding the target cone gives

```text
(-1,0,-1,-1).
```

Equation (1) proves that its E14 principal boundary has the companion with
coefficient `-1` exactly.  The desired clean boundary is
`(-1,0,-1,0)`, so the sole remaining row in this quotient is the
word-resolved labelled residue.  The primitive covector

```text
lambda_E14 - ores_word = (1,0,0,-1)
```

kills both placed columns and reads `-1` on the clean boundary.  A pure
same-word labelled-residue section makes the desired boundary enter the
span.  Hence the ordering is sharp:

```text
current formal cone       -> missing occurrence/private placement (3)
after (3)                 -> missing word-resolved labelled residue
after labelled residue    -> anchor/ridge/q/W terminal completion
```

Anchor is zero on the nearest lift, and `W` and target are zero
coefficientwise there.  Physical `q` is handled by the committed defect
alternative once the fully augmented comparison exists.  The Kähler ridge
commutes with the Hasse tower but still needs its labelled shifted physical
placement.  None of those rows precedes (3) or the labelled residue debt.

## Scope

This is exact for the canonical `h=3`, word-`000101` first-hit packet and
one normalized nonzero component of the generic root-even cone.  It does not
construct (3), the residue section, the beta-zero family, or a global
physical terminal.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
c044c59891a25d2618cf0a881150089117bd4da1f273f020eca7d20e11b96885
```

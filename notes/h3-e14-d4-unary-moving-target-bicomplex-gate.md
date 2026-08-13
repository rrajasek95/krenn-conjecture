# The old D1--D3 response faces do not fill the E14 unary proper face

## Result

On the silent canonical E14 branch, the fourth global-root Hasse face takes
the marked response occurrence from word `110000` to its pure target mate
in word `111111`.  The complete unary S-pair then has boundary

\[
 v_{24}^{11}U_{000101}=-R_{E14}+T_{12},
 \qquad R_{E14}=g-v_{04}^{00}g.
\]

The signed Boolean `D0`--`D4` face complex has profile `1,4,6,4,1` and
does satisfy `d^2=0`.  That formal identity does **not** say that the
already present `D1`--`D3` response faces fill `T12`.

Checker:
[`verify_h3_e14_d4_unary_moving_target_bicomplex_gate.py`](../computations/verify_h3_e14_d4_unary_moving_target_bicomplex_gate.py).

## Literal occurrence comparison

The four root directions recolour residual sites `2,3,4,5`.  The fourteen
proper response-face words are

```text
110001  110010  110011  110100  110101  110110  110111
111000  111001  111010  111011  111100  111101  111110.
```

The unary source row remains tagged by word `000101`, so it is not one of
these faces.  More importantly, every marked `D1`--`D3` occurrence face
contains the same two residual q edges with partially recoloured endpoint
labels.  Its q-degree is two.  The twelve nonprivate terms of `T12` are ten
cubics and two quartics.  Therefore none of the fourteen literal marked
occurrence faces is a `T12` term.

## Complete-row test

The degree argument alone would be too weak because one may multiply a
complete response row before inserting it in the comparison.  The stronger
test reconstructs the full target-augmented first-hit module.  It contains
269 independent physical columns: every complete response row in every word
and every complete unary row, with every monomial multiplier capable of
hitting `T12`.

Among these are 53 columns coming from the fourteen `D1`--`D3` response
words.  The exact rational first-hit dual kills all 53 of those columns,
and indeed all 269 columns, while pairing `-1` with `T12`.  Exact reduction
is still

```text
T12 -> R_E14,
```

not zero.  Hence the proper-face quotient contains one surviving
graded/private class

\[
 [T_{12}]=[R_{E14}].
\]

On `v04=0`, this is the marked private class `[g]`.

## Moving target and cap

Keep the cap graph in the moving orbit-relative presentation.  At normalized
cap parameter it has signature

```text
T+rho: boundary 0, target 1, Q 0, scalar ores 1.
```

It therefore repairs the common factor-90 target/scalar-residue
normalization after the cross-word placement.  It has no literal unary-tail
coordinate, so it cannot change the `T12` class.

A freely adjoined PP/Tate bicomplex can make `d^2=0` tautological by adding
the missing horizontal cross-operation two-cell.  The physical inventory
currently contains only the vertical `D1`--`D3` response faces and the
moving cap graph; it does not contain the horizontal maps on those faces.
Thus formal totalization identifies the exact new cell required rather than
constructing it.

## Shortest positive addition and scope

The remaining input is one source-labelled orbit-relative PP/Tate
cross-operation cell whose complete proper boundary is `T12`.  It must also
carry the target/cap, physical-q, shifted-ridge, anchor, eta, and sigma
readouts.  This statement is exact for canonical `h=3`, chart `(1,1)`, and
the silent `v04=0` E14 occurrence.  It is a no-go only for cancellation by
the existing complete `D1`--`D3` response faces, not for such an enlarged
cell.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
a3eafe3cf538fd9329a212c685089de3f74d3e327ff53aa9f0ae9eb42fce1246
```

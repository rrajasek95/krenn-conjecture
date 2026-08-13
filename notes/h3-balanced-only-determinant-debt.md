# The determinant entry fork has one balanced diagonal debt

## Result

The alternating part of the six-site matching module is five-dimensional,
but the evaluated-fan theorem uses only the six colour-unbalanced cuts.  The
exact ranks are

\[
 \operatorname{rank}D_{\rm bal}=4,\qquad
 \operatorname{rank}D_{\rm unbal}=4,\qquad
 \operatorname{rank}(D_{\rm bal}+D_{\rm unbal})=5.
\]

Moreover the four balanced determinant covectors have the same image modulo
the span of the six unbalanced covectors.  Hence there is exactly one
balanced-only quotient class.

This class is physically realizable at the level of one complete mixed row.
For word `001122`, in lexicographic edge order

```text
01 02 03 04 05 12 13 14 15 23 24 25 34 35 45
```

take

```text
-1  1  1 -1 -1  0  0 -1 -1 -1 -1 -1 -1 -1  0.
```

The hafnian is zero, all six unbalanced `3|3` determinants vanish, and all
four balanced determinants equal `3`.  Therefore the unbalanced
Laplace-factor theorem does not by itself exhaust determinant-bright
physical rows.

There is, however, an additional source-equation observation.  If every
offdiagonal edge cell in word `001122` vanished, the only possible matching
term would be the diagonal product

\[
                         A_{01}^{00}A_{23}^{11}A_{45}^{22}.
\]

Every balanced determinant would equal this product up to sign, and the
complete mixed source equation would force it to vanish.  Consequently a
nonzero balanced-only determinant on an actual zero mixed row still forces
some nonzero offdiagonal physical cell somewhere in the six-site packet.
The private-site identity can then build an active fan from that cell.  What
is missing from the balanced determinant itself is only the choice of a
nonzero offdiagonal Laplace factor; it is not a separate diagonal terminal.

Checker:
[`verify_h3_balanced_only_determinant_debt.py`](../computations/verify_h3_balanced_only_determinant_debt.py).

## Shifted source-entry fork

For the evaluated matching profile of an actual zero mixed coefficient, the
exact first split is now

```text
all ten determinants zero
        -> determinant-dark cut-permanent sector
        -> filtered tangent-Hasse cycle
        -> protected physical comparison

some unbalanced determinant nonzero
        -> offdiagonal Laplace factor
        -> private-site active fan
        -> four-good or pure-target-coloop accessibility

all unbalanced determinants zero, balanced class nonzero
        -> mixed source equation forces some offdiagonal cell
        -> private-site active fan
        -> four-good or pure-target-coloop accessibility
```

This is the complete `1+9+5` entry decomposition.  The last line is only one
scalar, not a new family of C4/C6 support cases.  It is also not removable by
calling the balanced determinant abstract: the displayed rational row is an
actual edge evaluation satisfying the mixed hafnian equation.  Its many
nonzero offdiagonal entries are exactly what the source-equation argument
must exploit.

## Interpretation

A balanced cut has one site of each output colour on both shores.  Its
determinant can therefore be nonzero on a purely diagonal matching block;
there need not be an offdiagonal **Laplace factor in that determinant**.
But a purely diagonal complete packet would make the determinant equal the
zero mixed coefficient.  Thus an offdiagonal cell exists elsewhere and the
balanced scalar rejoins the transverse fan proof after one source-equation
step.

The result prevents two overclaims:

1. the six unbalanced determinants do not span the entire tangent-Euler
   correction debt; and
2. a nonzero evaluated balanced determinant need not contain an offdiagonal
   factor in its own Laplace expansion.

The proof-completing statement is the same as for the unbalanced branch:
after the offdiagonal private-site fan is constructed, prove four-good rank
or normalize the resulting literal pure-target coloop into the global
affine/Hall accessibility theorem.  More enumeration of balanced support
patterns would not prove that landing.

## Scope and verification

The guard is one exact mixed coefficient, not a complete ternary GHZ source.
Other source rows may rule it out or force the missing lock companion; that
is precisely the open source-exhaustivity theorem.

Run:

```text
python3 computations/verify_h3_balanced_only_determinant_debt.py
python3 -O computations/verify_h3_balanced_only_determinant_debt.py
python3 -I -S computations/verify_h3_balanced_only_determinant_debt.py
```

Frozen ledger SHA-256:

```text
1ba2fd09c0185a7cdfb96d348f33638cff6f0e5fd2c99e5dd988aff7b97bda50
```
